---
создал заметку: 2026-11-07T22:47:00
author: WhiteK0T
tags:
  - Gentoo
  - Portage
  - Сборка
  - distcc
  - tmpfs
  - OpenRC
  - Логирование
Источник:
  - https://www.distcc.org/man/distcc_1.html
  - https://www.distcc.org/man/distccd_1.html
  - https://github.com/distcc/distcc
  - https://wiki.gentoo.org/wiki/Portage_TMPDIR_on_tmpfs
  - https://github.com/gentoo/portage/blob/master/lib/portage/package/ebuild/prepare_build_dirs.py
  - https://github.com/gentoo/portage/blob/master/bin/ebuild.sh
  - https://raw.githubusercontent.com/gentoo/portage/master/man/make.conf.5
  - https://github.com/autotools-mirror/libtool/blob/master/m4/libtool.m4
  - https://www.kernel.org/doc/html/latest/filesystems/tmpfs.html
  - https://man7.org/linux/man-pages/man8/mount.8.html
  - https://raw.githubusercontent.com/OpenRC/openrc/master/local.d/README
---

# distcc на Gentoo: tmpfs для сборки и логи

Эксплуатационная шпаргалка к заметке [distcc — распределённая сборка Gentoo на мощный VPS](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md). Здесь:
- сборки в tmpfs вместе с distcc;
- откуда после перезагрузки берётся `mkdir '…/.distcc/lock' failed`;
- как включать и выключать логи клиента и `distccd`;
- почему любой лишний вывод distcc в stderr может незаметно испортить `configure`.

Установка, транспорт (SSH или туннель) и совместимость компиляторов описаны в основной заметке. Команды выполняются от root, система — Gentoo с OpenRC, пользователи `portage` и `distcc` уже есть. Поведение проверено по исходникам distcc 3.4 и Portage и на `sys-devel/distcc-3.4-r9`.

## 1. Кто что делает

| Компонент | Где работает | Куда пишет |
| :--- | :--- | :--- |
| клиент `distcc` | вызывается вместо компилятора внутри `emerge`; при `FEATURES=userpriv` — от пользователя `portage` | stderr, то есть `build.log` пакета, или файл `DISTCC_LOG` |
| сервер `distccd` | служба на помогающей машине | syslog или файл `--log-file` |

В обычном режиме (без pump) препроцессор и линковка остаются на клиенте, на сервер уходит только компиляция. Компиляторы Go и Rust distcc не распределяет: через него проходят только C/C++-части таких пакетов.

## 2. Клиент: минимальная настройка

`/etc/portage/make.conf`:

```bash
FEATURES="${FEATURES} distcc"
```

`DISTCC_DIR` задавать не нужно. Portage сам использует `/var/tmp/portage/.distcc` (`${PORTAGE_TMPDIR}/portage/.distcc`) и создаёт этот каталог перед сборкой. А явное значение попадает в окружение всех фаз, в том числе `pkg_pretend`, для которой Portage каталог не создаёт (раздел 4).

`/etc/distcc/hosts` для уже поднятого туннеля:

```text
127.0.0.1:3632/10 localhost/4
```

- `127.0.0.1:3632` — вход в туннель, `/10` — до 10 заданий одновременно. `localhost/4` — до 4 заданий на самом клиенте, без сети.
- Порядок важен: distcc предпочитает хосты из начала списка, поэтому быстрые ставят первыми.
- Проверить, как distcc понял список: `distcc --show-hosts`.
- Туннель должен работать **до** начала сборки. Иначе distcc компилирует локально и пишет об этом в stderr, а это опасно для `configure` (раздел 6).

`MAKEOPTS="-j…"` выбирайте с учётом RAM, места в tmpfs и линковки: удалённые слоты не снимают с клиента препроцессор и линковку.

Компиляторы на обеих машинах должны совпадать по версии. Для multilib (`-m32`, например `sys-libs/libxcrypt` с `abi_x86_32`) сервер тоже должен уметь собирать 32-битный код. Подробно об этом — в разделе 5 основной заметки.

## 3. tmpfs для сборок

### Два варианта

| | Весь `/var/tmp` | Только `/var/tmp/portage` (так в Gentoo Wiki) |
| :--- | :--- | :--- |
| строка в `/etc/fstab` | `tmpfs /var/tmp tmpfs size=12G,nr_inodes=1M,mode=1777 0 0` | `tmpfs /var/tmp/portage tmpfs size=12G,nr_inodes=1M,uid=portage,gid=portage,mode=775 0 0` |
| что ещё попадает в RAM | временные файлы всех программ из `/var/tmp`, а при `FEATURES=ccache` без своего `CCACHE_DIR` — и кэш ccache (по умолчанию `/var/tmp/ccache`), который тогда обнуляется при каждой перезагрузке | только сборки Portage |
| после перезагрузки | пуст весь `/var/tmp`, хотя по FHS он должен переживать перезагрузку | остальной `/var/tmp` на диске не трогается |
| каталог для больших пакетов | на диске вне `/var/tmp` | `/var/tmp/notmpfs` рядом |

`PORTAGE_TMPDIR` менять не нужно ни в одном варианте: подкаталог `portage` Portage добавляет сам.

Параметры:
- `size=12G` — потолок, а не резерв: память занимается по мере записи, страницы tmpfs могут уходить в swap. 12 ГБ — пример: память одновременно нужна tmpfs, компиляторам и системе.
- `nr_inodes=1M` — лимит числа файлов. Множество мелких файлов исчерпает его раньше места.
- `mode`, `uid`, `gid` — права корня ФС при первом монтировании. На `remount` они не действуют, потом права меняются через `chmod` и `chown`.
- `noexec` не ставить: `configure` и тесты запускают собранные программы.
- Монтирование поверх каталога скрывает его прежнее содержимое до размонтирования.

### Большие пакеты — на диск

Если пакет не помещается в tmpfs, его временный каталог можно перенести на диск через `package.env`.

`/etc/portage/env/notmpfs.conf`:

```bash
PORTAGE_TMPDIR="/var/tmp/notmpfs"   # при tmpfs на весь /var/tmp — каталог на диске вне его, например /var/cache/notmpfs
```

```bash
install -d -o portage -g portage -m 775 /var/tmp/notmpfs
```

`/etc/portage/package.env`:

```text
app-office/libreoffice  notmpfs.conf
www-client/chromium     notmpfs.conf
```

### Применить без перезагрузки

```bash
findmnt -T /var/tmp          # или /var/tmp/portage — что сейчас смонтировано
```

- tmpfs уже смонтирован: `mount -o remount /var/tmp`. Параметры берутся из `fstab`. `size` и `nr_inodes` меняются без потери файлов, но уменьшить их ниже занятого не получится.
- tmpfs ещё не смонтирован: `mount /var/tmp`, **только когда не идёт `emerge`**. Новый пустой tmpfs закроет каталоги текущей сборки, включая `.distcc` (раздел 4).
- `mount -a` уже смонтированный tmpfs пропускает: новые размеры так не применятся.

### Контроль места, inode и памяти

```bash
df -h /var/tmp
df -i /var/tmp
free -h
swapon --show
```

При `No space left on device` проверять и байты, и inode: свободная RAM лимиты tmpfs не отменяет.

## 4. Каталоги `.distcc` после перезагрузки

Ошибка в выводе `emerge`:

```text
distcc[12345] (dcc_mkdir) ERROR: mkdir '/var/tmp/portage/.distcc/lock' failed: No such file or directory
distcc[12345] (dcc_build_somewhere) Warning: failed to distribute, running locally instead
```

**Механизм.** Если `DISTCC_DIR` задан, distcc сам этот каталог не создаёт, а делает `mkdir` только для `lock` и `state` внутри него (`src/tempfile.c`). Каталога нет — получаем `No such file or directory`. Этот файл distcc компилирует локально, и сборка идёт дальше.

**Что делает Portage.** При `FEATURES=distcc` он создаёт `DISTCC_DIR` вместе с `lock` и `state` (группа `portage`, setgid) в начале сборки каждого пакета (`_prepare_features_dirs` в `prepare_build_dirs.py`). Исключение — фазы `pretend`, `info` и `fetch`. При этом сам distcc подставлен в `PATH` во всех фазах.

**Когда ошибка всё же появляется в `emerge`:**
- **`pkg_pretend` сразу после перезагрузки.** Фазы `pkg_pretend` всех пакетов выполняются до сборки первого из них. Если ebuild проверяет там компилятор (например, поддержку OpenMP), distcc уже в `PATH`, а каталога на свежем tmpfs ещё нет. Это случается, если `DISTCC_DIR` явно задан в `make.conf`. Без него distcc в этой фазе берёт `$HOME/.distcc` во временном домашнем каталоге сборки и создаёт его сам.
- **tmpfs смонтирован поверх `/var/tmp` во время `emerge`.** Созданные Portage каталоги оказываются под новым пустым tmpfs.
- **distcc запущен вручную** с экспортированным в терминале `DISTCC_DIR`: тест, `distccmon-text`.

**Чем это плохо.** Сам файл просто соберётся локально, но строки `ERROR` и `Warning` уйдут в stderr. В `pkg_pretend` это обычно безвредно, во время `configure` опасно (раздел 6).

**Что сделать:**
1. Убрать `DISTCC_DIR` из `make.conf`, если там стоит значение по умолчанию.
2. Не монтировать tmpfs во время сборки.
3. Если distcc нужен сразу после загрузки и вне `emerge`, создавать каталоги при загрузке. Файл `/etc/local.d/distcc.start`:

```sh
#!/bin/sh
set -eu

# Не создавать каталоги на диске под точкой монтирования, если tmpfs не смонтирован.
# При tmpfs только на /var/tmp/portage — проверять его.
mountpoint -q /var/tmp

# Владелец и setgid как у Portage — иначе при первой сборке он «поправит» права с предупреждением.
install -d -o portage -g portage -m 2775 \
    /var/tmp/portage \
    /var/tmp/portage/.distcc \
    /var/tmp/portage/.distcc/lock \
    /var/tmp/portage/.distcc/state
```

```bash
chmod +x /etc/local.d/distcc.start
rc-update add local default
/etc/local.d/distcc.start
```

Служба `local` запускает `*.start` при загрузке, ближе к концу уровня `default`. Если сборку раньше неё запускает другая служба, нужен свой порядок запуска.

## 5. Логи клиента

Что и куда пишет клиент (по `src/traceenv.c`, проверено на distcc 3.4):

| `DISTCC_LOG` | `DISTCC_VERBOSE` | Куда и что |
| :--- | :--- | :--- |
| не задан | `0` (по умолчанию) | stderr, только предупреждения и ошибки |
| не задан | `1` | stderr, вся отладка — десятки строк на каждый вызов компилятора |
| файл открывается | `0` | файл; кроме ошибок ещё и информационные строки (`compile … completed ok` на каждый файл) |
| файл открывается | `1` | файл, вся отладка |
| файл **не** открывается | любой | stderr: `failed to open logfile …: Permission denied` при **каждом** вызове компилятора, плюс остальное по `DISTCC_VERBOSE` |

Без отдельного файла сообщения попадают в лог сборки `/var/tmp/portage/<категория>/<пакет-версия>/temp/build.log`. На tmpfs он не переживает перезагрузку. Чтобы логи сборок оставались на диске, задайте `PORTAGE_LOGDIR="/var/log/portage"` в `make.conf`.

### Обычный режим

- В `make.conf` нет `DISTCC_LOG`. `DISTCC_VERBOSE="0"` — значение по умолчанию, строку можно не писать.
- Переменные, экспортированные в терминале для ручных тестов, перекрывают `make.conf` для `emerge`, запущенного из этого терминала. Перед сборкой их нужно убрать:

```bash
unset DISTCC_LOG DISTCC_VERBOSE DISTCC_DIR
```

### Временная диагностика в файл

Подготовить файл на диске, вне tmpfs:

```bash
install -d -o root -g root -m 755 /var/log/distcc
touch /var/log/distcc/client.log
chown portage:portage /var/log/distcc/client.log
chmod 660 /var/log/distcc/client.log
```

Временно в `/etc/portage/make.conf`:

```bash
DISTCC_LOG="/var/log/distcc/client.log"
DISTCC_VERBOSE="1"
```

```bash
tail -f /var/log/distcc/client.log
```

- Пишет в файл не root, а `portage`: при `userpriv` компиляция идёт от него, даже если `emerge` запущен от root.
- Sandbox Portage открывает на запись каталог из `DISTCC_LOG` сам (`addwrite "${DISTCC_LOG%/*}"` в `ebuild.sh`), так что путь может быть любым. Важны только права на сам файл и проход через родительские каталоги.
- Для разового ручного теста вне `emerge` подходит и `DISTCC_LOG=/tmp/distcc.log`, как в основной заметке. Для `emerge` файл должен быть доступен на запись `portage`, иначе — последняя строка таблицы выше.

После диагностики вернуть обычный режим: новые настройки клиента подхватят новые сборки, перезапускать `distccd` не нужно. Если оставляете лог постоянно, настройте ротацию с сохранением владельца, например `create 660 portage portage` в `logrotate`.

## 6. Почему шум distcc в stderr ломает `configure`

libtool проверяет флаги компилятора, в том числе `-fPIC`, макросом `_LT_COMPILER_OPTION`. Он компилирует тестовый файл с флагом и сравнивает stderr с выводом обычной компиляции:

```sh
# m4/libtool.m4
# The compiler can only warn and ignore the option if not recognized
# So say no if there are warnings other than the usual output.
$ECHO "$_lt_compiler_boilerplate" | $SED '/^$/d' >conftest.expsym
$SED '/^$/d; /^ *+/d' conftest.err >conftest.er2
if test ! -s conftest.er2 || diff conftest.expsym conftest.er2 >/dev/null; then
  $2=yes
fi
```

В строках distcc есть PID (`distcc[12345] …`), так что с эталоном они не совпадут никогда, и флаг объявляется неподдерживаемым. Для `-fPIC` это значит, что объекты разделяемой библиотеки собираются без PIC. Тогда линковщик выдаёт `relocation R_X86_64_32 against … recompile with -fPIC` или `read-only segment has dynamic relocations`.

Откуда берётся шум:
- `DISTCC_LOG` недоступен на запись (раздел 5);
- `DISTCC_VERBOSE=1` без файла;
- нет каталога `.distcc` (раздел 4);
- сервер недоступен: `failed to connect to 127.0.0.1:3632: Connection refused` и следом `failed to distribute, running locally instead`.

Правило: во время сборки distcc должен молчать. Лог пишется либо в доступный файл, либо никуда; туннель поднят; каталоги на месте.

Признак в логе сборки:

```bash
grep 'PIC flag' /var/tmp/portage/<категория>/<пакет-версия>/temp/build.log
# норма: checking if x86_64-pc-linux-gnu-gcc PIC flag -fPIC -DPIC works... yes
```

### Разобранный случай: `sys-libs/libxcrypt`

Ошибка записи в лог distcc, multilib-сборка `libxcrypt`, линковка упала на `read-only segment has dynamic relocations`. После исправления логирования `-fPIC` появился, и 32- и 64-битная `libcrypt` слинковались. Это согласуется с механизмом выше, хотя без прежнего `config.log` всю цепочку доказать нельзя.

После исправления пересобирать с `configure`, а не только линковку:

```bash
emerge --oneshot --usepkg=n sys-libs/libxcrypt
```

- `--usepkg=n` — не брать бинарный пакет, собранный с испорченной проверкой.
- При `keepwork` и других настройках, которые сохраняют рабочее дерево, убедиться, что результаты старого `configure` не используются повторно.
- Не добавлять `-fPIC` глобально, чтобы скрыть проблему.

## 7. Логи сервера `distccd`

Параметры — в `/etc/conf.d/distccd`. Остальные настройки (`--allow`, `--listen`, порт) не трогать:

```bash
DISTCCD_OPTS="${DISTCCD_OPTS} --log-file /var/log/distcc/server.log --log-level warning"
```

Если в файле уже есть `--log-file` или `--log-level`, замените их, а не добавляйте второй раз.

Файл для пользователя демона:

```bash
install -d -o root -g root -m 755 /var/log/distcc
touch /var/log/distcc/server.log
chown distcc /var/log/distcc/server.log    # или пользователь из --user
chmod 640 /var/log/distcc/server.log
```

Применить между сборками:

```bash
rc-service distccd restart
tail -f /var/log/distcc/server.log
```

| Уровень | Что пишется |
| :--- | :--- |
| `critical`, `error` | только сбои |
| `warning` | плюс предупреждения; тихий вариант для постоянной работы |
| `notice` | **по умолчанию**: плюс одна итоговая строка на каждое задание (`COMPILE_OK`, код выхода, время) и отказы в доступе (`access denied`) |
| `info` | плюс подробности по каждому заданию (`job complete` и т. п.) |
| `debug` | всё; `--verbose` — то же, что `--log-level=debug` |

- Без `--log-file` сообщения идут в syslog. `--log-stderr` — только для отладки, не в режиме inetd.
- При постоянном файловом логе нужна ротация.
- **SSH-режим** (`@host` в списке хостов): `distccd --inetd` запускает sshd при каждом подключении, `conf.d` не читается. Параметры логов дописывают в саму команду, например в `command="distccd --inetd --log-file … --log-level warning"` у ключа в `authorized_keys`.
- **Gentoo на systemd:** сначала `systemctl cat distccd` — `/etc/conf.d/distccd` используется, только если юнит его читает. Журнал: `journalctl -u distccd -n 100 -f`.

## 8. На других системах

Переменные клиента (`DISTCC_LOG`, `DISTCC_VERBOSE`, `DISTCC_DIR`) и механизм из раздела 6 одинаковы везде: это тот же distcc. Без `DISTCC_DIR` клиент использует `~/.distcc` и создаёт его сам.

| | Debian / Ubuntu | Arch |
| :--- | :--- | :--- |
| служба | `distcc.service`, от пользователя `distccd` | `distccd.service`, от пользователя `distcc` |
| параметры | `/etc/default/distcc`: `ALLOWEDNETS`, `LISTENER`, `JOBS`, `NICE` — других ключей юнит не передаёт | `/etc/conf.d/distccd`: `DISTCC_ARGS="… --log-level warning --log-file …"` |
| лог по умолчанию | журнал: `journalctl -u distcc` | журнал: `journalctl -u distccd` |
| лог в файл | `systemctl edit distcc` → переопределить `ExecStart` с `--log-file /var/log/distccd.log --log-level warning`; ротация для этого пути уже есть в `/etc/logrotate.d/distcc` | добавить `--log-file` в `DISTCC_ARGS`, файл — на запись пользователю `distcc` |
| сборка в RAM | `dpkg-buildpackage` собирает там, где лежат исходники: распаковать их в tmpfs. В Debian 13 `/tmp` — уже tmpfs, в Ubuntu нет | `makepkg`: `BUILDDIR=/tmp/makepkg` в `/etc/makepkg.conf` (`/tmp` в Arch — tmpfs по умолчанию); distcc — `BUILDENV=(distcc …)` и `DISTCC_HOSTS` там же |

## 9. Как читать сообщения

| Сообщение | Уровень | Значение и действие |
| :--- | :--- | :--- |
| `compile f.c on 127.0.0.1:3632/10 completed ok` | info — видно в файле `DISTCC_LOG` | файл скомпилирован на сервере через туннель |
| `compile f.c on localhost completed ok` | info | скомпилирован локально: слот `localhost` или откат |
| `failed to distribute, running locally instead` | warning — видно в stderr | сервер не взял задание, файл собран локально; причина — в строке выше |
| `failed to connect to 127.0.0.1:3632: Connection refused` | error | туннель или `distccd` не работают |
| `mkdir '…/.distcc/lock' failed: No such file or directory`, `failed to lock` | error | нет `DISTCC_DIR` — раздел 4 |
| `failed to open logfile …: Permission denied` | error | `DISTCC_LOG` недоступен `portage` — раздел 5 |
| `called for link?  i give up` | info | вызов для линковки — всегда локально, норма |
| `-E call for cpp must be local` | debug | препроцессор — локально, норма |
| `… is busy` (файл в `.distcc/lock/`) | debug | слот занят, distcc берёт следующий — норма |
| `not reading …/hosts: No such file or directory` | debug | этого файла хостов нет — норма, если дальше прочитан `/etc/distcc/hosts` |
| `compile conftest.c on … failed` | — | обычно задуманно отрицательная проба `configure`; смотреть `config.log` |
| `checking if … PIC flag -fPIC -DPIC works... no` | вывод `configure` | признак шума в stderr — раздел 6 |
| `relocation R_X86_64_32 … recompile with -fPIC`, `read-only segment has dynamic relocations` | линковщик | объекты без PIC — раздел 6 |
| `>>> Completed (1 of 1) …` | вывод `emerge` | пакет установлен |

Успешная удалённая компиляция одного файла ещё не значит, что весь пакет слинкуется и установится.

## Связанные заметки

- [distcc — распределённая сборка Gentoo на мощный VPS](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) — установка, SSH-режим, что должно совпадать на машинах, `distccmon-text`
- [ccache — кэш компилятора на Gentoo](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md) — кэш держат на диске, а не в tmpfs: иначе он обнуляется при каждой перезагрузке
- [binhost — свой сервер бинарных пакетов Gentoo](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) — часто выгоднее distcc

## Ссылки

- man distcc(1): https://www.distcc.org/man/distcc_1.html
- man distccd(1): https://www.distcc.org/man/distccd_1.html
- Исходники distcc (`src/traceenv.c`, `src/tempfile.c`): https://github.com/distcc/distcc
- Gentoo Wiki, Portage TMPDIR on tmpfs: https://wiki.gentoo.org/wiki/Portage_TMPDIR_on_tmpfs
- Portage, создание служебных каталогов: https://github.com/gentoo/portage/blob/master/lib/portage/package/ebuild/prepare_build_dirs.py
- Portage, `addwrite` для `DISTCC_LOG`: https://github.com/gentoo/portage/blob/master/bin/ebuild.sh
- make.conf(5): https://raw.githubusercontent.com/gentoo/portage/master/man/make.conf.5
- libtool, `_LT_COMPILER_OPTION`: https://github.com/autotools-mirror/libtool/blob/master/m4/libtool.m4
- tmpfs: https://www.kernel.org/doc/html/latest/filesystems/tmpfs.html
- mount(8): https://man7.org/linux/man-pages/man8/mount.8.html
- OpenRC local.d: https://raw.githubusercontent.com/OpenRC/openrc/master/local.d/README

#Gentoo #Portage #distcc #tmpfs #Сборка #OpenRC #Логирование
