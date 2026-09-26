---
создал заметку: 2026-09-26T21:40:00
author: WhiteK0T
tags:
  - mv
  - Linux
  - Coreutils
  - Файловые_системы
  - Шпаргалка
Источник:
  - https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html
  - https://github.com/coreutils/coreutils/blob/v9.11/src/mv.c
  - https://github.com/coreutils/coreutils/blob/v9.11/src/copy.c
  - https://github.com/coreutils/coreutils/blob/v9.11/NEWS
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/mv.html
  - https://man7.org/linux/man-pages/man2/rename.2.html
---

# 🚚 mv — перемещение и переименование: что он делает на самом деле

`mv` из **GNU coreutils** — это на самом деле **две разные команды под одним именем**:

1. **В пределах одной ФС** — один системный вызов `rename()`. Данные не трогаются, меняется только запись в каталоге. Мгновенно при любом размере и **атомарно**.
2. **Между разными ФС** — `rename()` падает с `EXDEV`, и `mv` **копирует файл, а затем удаляет исходник** (по сути `cp -a` + `rm -r`). Долго, неатомарно, и при сбое можно потерять **файл назначения**.

Снаружи не видно, какой из режимов сработает, а от этого зависит почти всё: скорость, безопасность, поведение открытых файлов и что останется на диске после ошибки.

Заметка написана **по исходникам** `coreutils v9.11` (`src/mv.c`, `src/copy.c`) и проверена руками на Gentoo с `mv (GNU coreutils) 9.11`. Для сравнения собраны и прогнаны на тех же тестах **BusyBox 1.37.0** (как на роутере) и **uutils 0.10.0** (Rust-реализация, по умолчанию в Ubuntu 26.04). Всё, что помечено «проверено», реально запускалось.

> [!info] Версии на момент написания (26.09.2026)
> | Где | Что за `mv` |
> | :--- | :--- |
> | **Gentoo** (проверялось здесь) | GNU coreutils `9.11-r1` |
> | **Arch** | GNU coreutils `9.11-2` |
> | **Debian** | GNU: forky/sid `9.10-1` · trixie `9.7-3` · bookworm `9.1-1` |
> | **Ubuntu** | 24.04 noble — GNU `9.4` · **25.10 и 26.04 — по умолчанию uutils** (`rust-coreutils`, в 26.04 `0.10.0`) |
> | **Entware** (`armv7sf-k3.2`) | `coreutils-mv 9.9-2` |
> | **BusyBox** в прошивке роутера | `1.37.0` — **свой `mv`, не coreutils** |

## 📋 Опции — полный список (из `mv --help` 9.11)

| Опция | Что делает |
| :--- | :--- |
| `-f`, `--force` | не спрашивать перед перезаписью |
| `-i`, `--interactive` | спрашивать перед **каждой** перезаписью |
| `-n`, `--no-clobber` | не перезаписывать существующие файлы (в исходнике помечена `/* Deprecated. */`) |
| `--update[=UPDATE]` | `all` (по умолчанию без опции) / `none` (= `-n`) / `none-fail` (пропустить **и** вернуть ошибку) / `older` (= `-u`) |
| `-u` | заменять, только если назначение **старше** источника |
| `-b`, `--backup[=CONTROL]` | резервная копия заменяемого файла: `simple` (`файл~`), `numbered` (`файл.~1~`), `existing`, `none` |
| `-S`, `--suffix=SUFFIX` | суффикс вместо `~` (или через `SIMPLE_BACKUP_SUFFIX`) |
| `-t`, `--target-directory=DIR` | переместить все источники **в** каталог DIR |
| `-T`, `--no-target-directory` | считать назначение **именем**, а не каталогом |
| `--exchange` | **атомарно поменять местами** источник и назначение (с 9.5) |
| `--no-copy` | не копировать, если `rename()` не удался: между ФС — ошибка (с 9.2) |
| `--strip-trailing-slashes` | убрать завершающие `/` у источников |
| `--debug` | объяснить, как копируется файл (включает `-v`) |
| `-v`, `--verbose` | печатать, что делается |
| `-Z`, `--context` | выставить SELinux-контекст по умолчанию |

Из `-i`, `-f`, `-n` действует **последняя** указанная. Рекурсивной опции нет: каталоги `mv` переносит всегда.

## 🧬 Главное: `rename()` или «скопировать и удалить»

`mv` не проверяет заранее, та же ФС или нет. Он просто пробует `rename()` и смотрит на ошибку. В `mv.c`, при ровно двух операндах, первая попытка делается ещё до разбора, каталог ли назначение:

```c
      if (n_files == 2 && !x.exchange)
        x.rename_errno = (renameatu (AT_FDCWD, file[0], AT_FDCWD, lastfile,
                                     RENAME_NOREPLACE)
                          ? errno : 0);
```

`RENAME_NOREPLACE` — флаг `renameat2()`: переименовать, **только если назначения нет**. Если получилось, работа закончена за один вызов. Если нет, дальше `copy.c` решает по `errno`:

```c
      if (rename_errno != EXDEV || x->no_copy || x->exchange)
        {
          ...
          error (0, rename_errno, _("cannot move %s to %s"), ...
          return false;
        }
```

Только `EXDEV` («Invalid cross-device link», то есть разные ФС) включает копирование. Любая другая ошибка (`EACCES`, `ENOTEMPTY`, `EISDIR`...) сразу завершает `mv` с ошибкой.

```bash
# проверено:
$ stat -c %i a; mv a b; stat -c %i b
4593177
4593177                         # тот же инод — файл не трогали, сменилось имя

$ stat -c '%i dev=%d' c; mv c /dev/shm/c; stat -c '%i dev=%d' /dev/shm/c
4593176 dev=64772
11 dev=28                       # другой инод на другом устройстве — это новый файл

$ mv -v d /dev/shm/             # -v честно показывает режим (с 8.28)
copied 'd' -> '/dev/shm/d'
removed 'd'
```

В той же ФС `-v` печатает `renamed 'a' -> 'b'`, между ФС — `copied` + `removed`. Это самый простой способ узнать, какой режим сработал.

Разница в скорости (tmpfs ↔ ext4, один прогон):

| Что | Та же ФС | Между ФС |
| :--- | :--- | :--- |
| файл 1 ГБ | **0,001 с** | 0,67 с |
| каталог из 50 000 пустых файлов | **0,001 с** | 1,13 с |

Между ФС время растёт с объёмом (здесь это RAM-диск; на HDD умножайте на порядки), в той же ФС оно всегда одно и то же.

> [!note] «Другая ФС» — это не только другой диск
> `EXDEV` возникает на границе **любой точки монтирования**: подтом Btrfs, `bind`-монтирование, `/tmp` на tmpfs, `/home` отдельным разделом, overlayfs в контейнере. `mv ~/Загрузки/iso /tmp/` на системе с tmpfs в `/tmp` — это полное копирование через RAM.

## ⚛️ Атомарность: почему `mv` — основа безопасной записи

В пределах одной ФС `rename()` **атомарен**: любой процесс в любой момент видит либо старый файл целиком, либо новый целиком, но никогда не половину. Поэтому стандартный способ безопасно обновить конфиг, файл состояния или бинарник — записать во временный файл **рядом** и переименовать поверх:

```bash
tmp=$(mktemp "/etc/app/app.conf.XXXXXX")   # в том же каталоге = на той же ФС
generate-config > "$tmp" && sync "$tmp" && mv -f -- "$tmp" /etc/app/app.conf
```

- `mktemp` **в том же каталоге**: `mktemp` без пути создаст файл в `/tmp`, а это часто другая ФС, и атомарность пропадёт;
- `sync "$tmp"` (coreutils ≥ 8.24 умеет синхронизировать один файл): `rename()` атомарен, но без сброса на диск после сбоя питания можно получить новое имя с пустым содержимым;
- права и владелец берутся от **нового** файла. При необходимости выставьте их до `mv`: `chmod --reference=старый "$tmp"`.

### Открытые файлы и запущенные бинарники

Процесс, открывший файл, держит **инод**, а не имя. Поэтому `mv` в той же ФС ведёт себя с открытыми файлами прямо противоположно `cp`:

```bash
# проверено — лог продолжает писаться в переименованный файл:
$ echo log1 > app.log; exec 9>>app.log
$ mv app.log app.log.1
$ echo after >&9; cat app.log.1
log1
after                                # запись ушла в app.log.1, app.log не появился

# проверено — замена работающего бинарника:
$ ./mysleep 30 &
$ cp /bin/true mysleep
cp: cannot create regular file 'mysleep': Text file busy
$ cp /bin/true mysleep.new && mv mysleep.new mysleep     # exit=0
$ ls -l /proc/$!/exe
... /proc/95588/exe -> .../mysleep (deleted)    # процесс работает со старым инодом
```

Именно так обновляют программы пакетные менеджеры: новый файл кладётся рядом и переименовывается поверх, а запущенные процессы доживают на старом иноде. Оттуда же пометка `(deleted)` в `lsof` после обновления — см. [lsof](lsof.md).

> [!tip] Отсюда два режима logrotate
> - `create` — лог **переименовывается** (`mv`), создаётся новый пустой, а программе шлют сигнал (`HUP`), чтобы она переоткрыла файл. Без сигнала программа так и пишет в `app.log.1`, как в примере выше.
> - `copytruncate` — лог копируется и **обрезается на месте**. Сигнал не нужен, но строки, записанные между копированием и обрезкой, теряются.
>
> По той же причине `tail -f app.log` после ротации «замирает» (следит за инодом), а `tail -F` переоткрывает файл по имени.

## 💥 Между ФС: файл назначения удаляется **до** копирования

Это главная неочевидная опасность `mv`. Когда `rename()` вернул `EXDEV`, `copy.c` сначала **удаляет существующий файл назначения** и только потом начинает копировать:

```c
      /* The rename attempt has failed.  Remove any existing destination
         file so that a cross-device 'mv' acts as if it were really using
         the rename syscall.  ... */
      if ((unlinkat (dst_dirfd, drelname,
                     S_ISDIR (src_mode) ? AT_REMOVEDIR : 0)
           != 0)
          && errno != ENOENT)
```

Если копирование не дойдёт до конца (кончилось место, отвалился USB-диск, `Ctrl+C`), старого файла уже нет, а новый недописан:

```bash
# проверено: файл 3 МБ переносится на tmpfs размером 2 МБ, где уже лежит важный файл с тем же именем
$ cat mnt/big
OLD IMPORTANT
$ mv big mnt/big
mv: error writing 'mnt/big': No space left on device
exit=1
$ ls -l big mnt/big
-rw-r--r-- 1 root root 3145728 big        # источник цел (mv удаляет его только после успеха)
-rw------- 1 root root 2097152 mnt/big    # старый файл УНИЧТОЖЕН, на его месте 2 МБ обрезка
```

Обратите внимание и на права `-rw-------`: при копировании `mv` сначала создаёт файл без прав для группы и остальных (`omitted_permissions` в `copy.c`) и выставляет их только в конце. Недописанный файл так и остаётся с урезанными правами.

С каталогом то же самое, только остаётся **половина дерева**:

```bash
# проверено: каталог src (a = 1 МБ, b = 3 МБ) → tmpfs 2 МБ
$ mv src mnt/
mv: error writing 'mnt/src/b': No space left on device
exit=1
# mnt/src/a — 1 МБ (целый), mnt/src/b — 1 МБ (обрезан); src/ — полностью на месте
```

Исходник при этом **никогда** не теряется: `mv.c` вызывает удаление источника (внутренний `rm()` из того же `remove.c`, что и у команды [rm](rm.md)) только если `copy()` вернул успех. Под угрозой именно **назначение**.

> [!danger] Практический вывод
> При переносе **между дисками поверх существующих файлов** `mv` не надёжнее, чем `rm` + `cp`. Безопаснее в два шага, с проверкой:
> ```bash
> rsync -a --info=progress2 src/ /mnt/usb/dst/ \
>   && rsync -a --checksum --dry-run --itemize-changes src/ /mnt/usb/dst/   # пустой вывод = всё совпало
> rm -rf src/
> ```
> `rsync` пишет каждый файл во временный `.имя.XXXXXX` и переименовывает поверх только после успешной записи. Старая версия файла назначения доживает до конца его копирования.

## 📦 Каталоги: `mv` не умеет сливать

```bash
# проверено:
$ mkdir -p s1 dst/s1 && touch dst/s1/x
$ mv s1 dst/
mv: cannot overwrite 'dst/s1': Directory not empty    # exit=1 — слияния нет

$ mkdir -p s2 dst/s2 && mv s2 dst/                    # exit=0 — ПУСТОЙ каталог заменяется

$ mv dd dd/sub
mv: cannot move 'dd' to a subdirectory of itself, 'dd/sub'

$ mkdir e1; touch e2; mv e2 e1                        # файл уехал ВНУТРЬ e1: e1/e2
$ mkdir e3; touch e4; mv -T e3 e4
mv: cannot overwrite non-directory 'e4' with directory 'e3'
```

Между ФС сообщение другое, но результат тот же:

```text
mv: inter-device move failed: 'cf' to '/dev/shm/gt/cf'; unable to remove target: Directory not empty
```

Слить два дерева — задача не для `mv`:

```bash
rsync -a --remove-source-files src/ dst/ && find src -type d -empty -delete
# или без rsync, в пределах одной ФС: жёсткие ссылки мгновенны (проверено)
cp -al --remove-destination src/. dst/ && rm -rf src
```

В обоих вариантах при совпадении имён **побеждает источник**. Без `--remove-destination` `cp -al` на первом же совпадении падает с `cannot create hard link ... File exists`.

## 🔐 Права: снова важен каталог — и у каталогов есть ловушка

Как и удаление, перемещение — это **изменение каталогов**: нужна запись в каталог-источник (убрать имя) и в каталог-назначение (добавить имя). Права самого файла не важны. Но у **каталогов** есть дополнительное условие:

```bash
# проверено (обычный пользователь):
$ mkdir -p p1/sub p2 && chmod 555 p1/sub
$ mv p1/sub p2/
mv: cannot move 'p1/sub' to 'p2/sub': Permission denied     # exit=1
$ mv p1/sub p1/sub2                                         # exit=0 — в том же родителе можно
```

Перенос каталога в **другой** родительский каталог меняет запись `..` внутри него, поэтому ядро требует права записи **на сам перемещаемый каталог**. Переименование на месте `..` не трогает, и этого права не нужно.

> [!tip] Sticky bit
> В каталоге с битом `t` (`/tmp`) переименовывать и уносить чужие файлы нельзя, как и удалять: ядро проверяет то же условие (владелец файла, владелец каталога или root).

## ❓ `-i`, `-n`, `-u` — и история с кодом возврата

### Без опций `mv` тоже может спросить — но только в терминале

В `copy.c` функция `abandon_move()` задаёт вопрос, если выбран `-i` **или** если опций нет, stdin является терминалом, а файл назначения защищён от записи:

```c
          || ((x->interactive == I_ASK_USER
               || (x->interactive == I_UNSPECIFIED
                   && x->stdin_tty
                   && ! writable_destination (dst_dirfd, dst_relname,
                                              dst_sb->st_mode)))
```

```bash
# проверено:
$ chmod 444 d; mv s d                 # в терминале (через script):
mv: replace 'd', overriding mode 0444 (r--r--r--)?     # n → файл цел

$ chmod 444 d; mv s d </dev/null      # в скрипте — exit=0, перезаписан МОЛЧА
```

Ловушка та же, что у `rm`: **в скриптах, cron и конвейерах эта защита не срабатывает никогда**.

### Код возврата при отказе/пропуске

```bash
# проверено на 9.11:
$ mv -n s d;                 echo $?    # 0 — пропущен молча, s на месте
$ mv --update=none-fail s d; echo $?    # mv: not replacing 'd' → 1
$ echo n | mv -i s d;        echo $?    # 1 — отказ = ошибка
$ mv -u s d;                 echo $?    # 0 — d новее, пропущен молча, s на месте
```

> [!caution] `-i` и `-I` у `rm` и `mv` ведут себя противоположно
> Отказ на запрос `rm -I` возвращает **0**, а отказ на запрос `mv -i` (с 9.2, как требует POSIX) возвращает **1**. Во всех случаях с `-n` и `-u` пропущенный файл **остаётся на месте источника**: `mv` отработал «успешно», а файл никуда не переехал. Проверяйте результат, а не `$?`.

С `-n` в coreutils было три разных поведения подряд, и все три встречаются на живых системах:

| Версия coreutils | `mv -n` при существующем файле | Где встречается |
| :--- | :--- | :--- |
| до 9.1 | молча пропустить, **exit 0** | Debian bookworm (`9.1`) |
| 9.2 | пропустить, **exit 1** | — |
| 9.3–9.4 | пропустить, сообщение `not replacing`, **exit 1** | **Ubuntu 24.04 LTS** (`9.4`) |
| с 9.5 | снова молча, **exit 0** | Debian trixie, Arch, Gentoo, Entware |

Поэтому в NEWS 9.5 прямо сказано: *«The -n,--no-clobber option is best avoided due to platform differences»*. Для переносимых скриптов пишите явно, что нужно:

```bash
mv --update=none      src dst   # пропустить молча, exit 0 (coreutils ≥ 9.3)
mv --update=none-fail src dst   # пропустить и вернуть ошибку (≥ 9.5)
```

### Резервные копии вместо вопросов

```bash
# проверено:
$ mv -b u t                     # старый t сохранён как t~
$ mv --backup=numbered u t      # t.~1~, t.~2~, ... — ничего не затирается
```

`-b` удобен в скриптах: вопросов нет, данные не теряются. С `-n` и `--exchange` не сочетается: `cannot combine --backup with --exchange, -n, or --update=none-fail`.

## 🔁 `--exchange` и `--no-copy` — новые опции

`--exchange` (coreutils 9.5) вызывает `renameat2(..., RENAME_EXCHANGE)`: два имени **атомарно меняются местами**. Без временного файла и без момента, когда одного из них нет:

```bash
# проверено:
$ echo AAA>a; echo BBB>b; mv --exchange a b; cat a b
BBB
AAA
$ mv -T --exchange x y          # каталоги — только с -T
$ mv --exchange x y
mv: cannot exchange 'x' and 'y/x': Unknown error -1    # без -T ищет y/x, сообщение невнятное
$ mv --exchange q /dev/shm/q
mv: cannot exchange 'q' and '/dev/shm/q': Invalid cross-device link   # только в одной ФС
```

Полезно для атомарного переключения каталогов (`release-new` ↔ `release-current`) без симлинков.

`--no-copy` (9.2) запрещает запасной путь через копирование: `mv --no-copy big /mnt/usb/` вернёт `Invalid cross-device link` вместо многочасового копирования. Хорошая страховка в скриптах, которые рассчитывают на мгновенный атомарный `rename()`.

## ⚠️ Типичные ловушки

**1. Опечатка в имени каталога — и файл переименован.** Если последнего аргумента не существует, `mv` считает его **новым именем**:

```bash
# проверено:
$ mv f1 newdir                 # newdir не существует → файл f1 стал файлом newdir
$ mv f2 newdir2/
mv: cannot move 'f2' to 'newdir2/': Not a directory    # слеш в конце спасает
$ mv -t nodir f2
mv: target directory 'nodir': No such file or directory
```

Переносите в каталог с `/` на конце или через `-t КАТАЛОГ`. Переименование, которое никогда не уедет внутрь каталога, делайте через `-T`.

**2. Имена с дефисом в глобе.** Как и у `rm`, файлы, начинающиеся с `-`, становятся опциями:

```bash
# проверено:
$ touch -- -n a b; mv * ../dest     # shell раскрыл в: mv -n a b ../dest
$ echo $?; ls
0
-n                                   # файл -n «съеден» как опция и молча остался
$ mv -- * ../dest                   # правильно (или mv ./* ../dest)
```

Файл с именем `-t` ещё хуже: он перехватывает следующий аргумент как каталог назначения.

**3. Скрытые файлы.** `mv src/* dst/` не трогает `src/.hidden`: глоб `*` не раскрывается в имена с точкой. В bash нужен `shopt -s dotglob`, либо переносите каталог целиком.

**4. Слеш на конце символической ссылки.**

```bash
# проверено:
$ ln -s tgt lnk; mv lnk/ newname
mv: cannot move 'lnk/' to 'newname': Not a directory    # ни ссылка, ни tgt не тронуты
$ mv lnk lnk2                                           # переименована сама ссылка
```

**5. Относительные ссылки ломаются.** `mv` переносит ссылку как есть. `../file` после переноса указывает уже в другое место. Перед переносом дерева со ссылками проверьте их через `find . -type l -lname '../*'`.

**6. Жёсткие ссылки на один файл.** POSIX требует, чтобы `rename()` ничего не делал, если оба имени указывают на один инод. GNU `mv` (с 8.24) явно отказывается:

```bash
# проверено:
$ ln sf hl; mv sf hl
mv: 'sf' and 'hl' are the same file       # exit=1
```

## ✅ Проверка утверждений

| Утверждение | Вердикт | Пояснение |
| :--- | :--- | :--- |
| «`mv` мгновенный» | ⚠️ Только в одной ФС | Между ФС — полное копирование: 1 ГБ за 0,67 с даже на RAM-диске |
| «`mv` атомарен» | ⚠️ Только в одной ФС | `rename()` атомарен; между ФС — копирование + удаление, промежуточные состояния видны |
| «Если `mv` упал, ничего не пропало» | ❌ **Нет** | Между ФС файл назначения удаляется **до** копирования (`unlinkat` в `copy.c`); проверено: `OLD IMPORTANT` заменён 2 МБ обрезком |
| «Источник при ошибке сохранится» | ✅ Да | Удаляется только после успешного `copy()` |
| «`mv dir existing_dir/` сольёт каталоги» | ❌ Нет | `Directory not empty`; заменяется только **пустой** каталог |
| «Чтобы переместить каталог, хватит прав на родителей» | ❌ Не всегда | В другой родитель — нужна запись и в **сам** каталог (меняется `..`) |
| «`mv` спросит перед затиранием read-only файла» | ⚠️ Только в терминале | `x->stdin_tty` в `abandon_move()`; в скрипте затрёт молча |
| «`mv -n` при конфликте вернёт ошибку» | ⚠️ Зависит от версии | 9.2–9.4 (Ubuntu 24.04) — `exit 1`, до и после — `0` |
| «Отказ на `mv -i` — это успех, как у `rm -I`» | ❌ Нет | С 9.2 — `exit 1` |
| «Замена бинарника через `cp` безопасна» | ❌ Нет | `Text file busy`; через `mv` поверх — работает, процесс остаётся на старом иноде |
| «Процесс продолжит писать в старое имя» | ❌ Нет | Дескриптор привязан к иноду; запись идёт в переименованный файл |
| «`mv a b` с жёсткими ссылками — no-op» | ⚠️ Смотря какой `mv` | GNU и uutils: ошибка `are the same file`; BusyBox: молча `exit 0`, оба имени остаются |
| «`mv -v` показывает, что сделано» | ⚠️ Не везде | GNU — честно (`renamed` / `copied`+`removed`); uutils пишет `renamed` и между ФС; BusyBox печатает строку даже при ошибке |
| «На роутере `mv` такой же» | ❌ Нет | BusyBox: только `-f -i -n -T -t -v`, без `-u`, `-b`, `--exchange` — см. ниже |

## 💻 На твоих системах

`mv` входит в **coreutils** — базовый пакет, который есть везде (на Gentoo это `@system`, на Debian `Essential: yes`).

| Система | Что делать |
| :--- | :--- |
| **Gentoo** | Уже стоит (`sys-apps/coreutils`, у меня `9.11-r1`). Для массовых переименований рядом: `rename` из `sys-apps/util-linux` (уже стоит, простая замена подстроки), `emerge dev-perl/rename` → `perl-rename` (регулярки Perl), `emerge sys-apps/renameutils` → `qmv` (переименование в текстовом редакторе) |
| **Debian / Ubuntu** | Уже стоит. **Проверьте, какой именно**: `mv --version`. На Ubuntu 24.04 это GNU 9.4 с `-n` → `exit 1`; на Ubuntu 25.10/26.04 по умолчанию `mv (uutils coreutils)`, вернуть GNU — `sudo apt install coreutils-from-gnu`. `rename` на Debian — это Perl-версия (`apt install rename`), util-linux-версия называется `rename.ul` |
| **Arch** | Уже стоит (`core/coreutils`, `9.11-2`). Perl-rename: `sudo pacman -S perl-rename` |
| **Entware / RT-AX56U** | ⚠️ По умолчанию `mv` — апплет **BusyBox 1.37.0**. Полноценный: `opkg install coreutils-mv` (версия `9.9-2`, 53 КБ в пакете / 110 КБ установленный; тянет базовый `coreutils` и `libacl`). Для переноса на USB-диск с проверкой — `opkg install rsync` (`3.4.1-3`) |

### ⚠️ BusyBox `mv` на роутере — проще и местами врёт

Апплет `coreutils/mv.c` из BusyBox 1.37.0 умещается в 190 строк. Весь парсер опций:

```c
	flags = getopt32long(argv, "^"
			"finTt:v"
```

Есть `-f -i -n -T -t -v` (длинные `--force`, `--interactive`, `--no-clobber`, `--target-directory`, `--no-target-directory`). **Нет** `-u`, `-b`/`--backup`, `--exchange`, `--no-copy`, `--update=...`. Логика та же: `rename()`, при `EXDEV` — `unlink(dest)`, затем `copy_file()` и `remove_file()`. Потеря файла назначения при нехватке места воспроизводится один в один:

```bash
# проверено на собранном BusyBox 1.37.0 (defconfig):
$ busybox mv big mnt/big
mv: write error: No space left on device     # старый mnt/big уже удалён
```

Отличия от GNU, найденные на тестах:

```bash
# проверено:
$ busybox mv -n -v s d
's' -> 'd'                  # ПЕЧАТАЕТ «перемещено», хотя ничего не сделано (d не тронут)
$ busybox mv -v nonexist zz
mv: can't rename 'nonexist': No such file or directory
'nonexist' -> 'zz'          # и при ошибке тоже
$ echo n | busybox mv -i s d; echo $?
0                           # отказ = успех (у GNU — 1)
$ ln sf hl; busybox mv sf hl; echo $?
0                           # оба имени на месте, ни слова (у GNU — ошибка)
$ busybox mv q q/sub
mv: can't rename 'q': Invalid argument          # без объяснения «в самого себя»
$ busybox mv cf /dev/shm/bbt/                   # каталог между ФС поверх существующего
mv: can't remove '/dev/shm/bbt/cf': Is a directory
```

Причина с `-v` видна в исходнике: метка `RET_0:` с `printf("'%s' -> '%s'\n", ...)` стоит **после** `RET_1:`, поэтому до неё доходят и пропуски, и ошибки. **Вывод `-v` в BusyBox не показывает, что произошло.** Опция `-v` вообще есть только при `CONFIG_FEATURE_VERBOSE`, а в прошивке её может и не быть.

```bash
# на роутере
opkg install coreutils-mv
which mv          # ожидается /opt/bin/mv (Alternatives: 300:/opt/bin/mv:/opt/libexec/mv-coreutils)
mv --version      # mv (GNU coreutils) 9.9
```

> [!note] Как и с `rm`, подмена действует только на твою сессию
> `/opt/bin` в `PATH` стоит перед `/bin`, но скрипты прошивки вызывают `/bin/mv` и получают BusyBox. Подробнее про `Alternatives` — в [OPKG](../Package-Manager/OPKG.md).

> [!warning] Внутренняя flash → USB-диск — это всегда «между ФС»
> `/jffs`, `/tmp` (tmpfs в RAM) и `/opt` (USB) — разные ФС. `mv /tmp/big.tar /opt/` на роутере с 512 МБ RAM — это копирование, и при заполненном USB-диске файл назначения теряется. Для больших переносов надёжнее `rsync`.

### uutils (Ubuntu 25.10+) — совместим, но с оговорками

Проверено на `mv (uutils coreutils) 0.10.0` (та же версия, что в Ubuntu 26.04): `-n` → exit 0, отказ на `-i` → exit 1, `are the same file` для жёстких ссылок, `--exchange` работает. Отличия:

- `-v` между ФС пишет `renamed 'c' -> '/dev/shm/uuc'`, хотя файл был скопирован;
- при нехватке места сообщение **`mv: Permission denied`** вместо `No space left on device`, при этом файл назначения теряется так же, как у GNU.

## 🔗 Ссылки

- Документация: [GNU coreutils — `mv` invocation](https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html) · [POSIX `mv`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/mv.html) · [`rename(2)` — `RENAME_NOREPLACE`, `RENAME_EXCHANGE`](https://man7.org/linux/man-pages/man2/rename.2.html) · локально `info '(coreutils) mv invocation'`
- Исходники: [`src/mv.c`](https://github.com/coreutils/coreutils/blob/v9.11/src/mv.c) · [`src/copy.c`](https://github.com/coreutils/coreutils/blob/v9.11/src/copy.c) · [`NEWS`](https://github.com/coreutils/coreutils/blob/v9.11/NEWS) · BusyBox [`coreutils/mv.c`](https://git.busybox.net/busybox/tree/coreutils/mv.c?h=1_37_stable)
- Связанные: [rm — парная заметка про удаление](rm.md) · [cp — почему `cp` поверх файла не атомарен](cp.md) · [lsof — кто держит старый инод после `mv`](lsof.md) · [strace — увидеть `renameat2` / `EXDEV` своими глазами](strace.md) · [git mv — совсем другая команда](../../VCS/Git/mv.md) · [Btrfs — подтома тоже граница `EXDEV`](../Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md) · [OPKG](../Package-Manager/OPKG.md)

#mv #Linux #Coreutils #Файловые_системы #Шпаргалка
