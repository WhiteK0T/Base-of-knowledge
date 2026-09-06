---
создал заметку: 2026-09-06T23:30:00
author: WhiteK0T
tags:
  - Gentoo
  - Portage
  - Сборка
  - distcc
  - SSH
  - VPS
  - Оптимизация
Источник:
  - https://wiki.gentoo.org/wiki/Distcc/ru
  - https://wiki.gentoo.org/wiki/Distcc
  - https://xakep.ru/2010/11/10/53558/
  - https://github.com/distcc/distcc
  - https://bugs.gentoo.org/702146
---

# distcc — распределённая сборка на мощный VPS

> [!info] Задача
> Локальная машина на Gentoo за NAT (серый IP), удалённый VPS — **AMD Ryzen 9 7950X3D, 8 ядер, 16 ГБ RAM**. Хочется отдавать компиляцию туда, а на месте оставить только препроцессинг и линковку.
>
> Три вещи, которые нужно знать до начала: **pump-режим в Gentoo вырезан** и все советы про `,cpp,lzo` из старых статей мертвы; **серый IP не мешает вообще** и реверс-туннель здесь не нужен — соединение инициирует клиент; и главный подводный камень не сеть, а **совпадение версий gcc и флагов `-march`**.

---

## 1. Что distcc делает и, главное, чего не делает

Сборка C/C++ распадается на этапы. distcc в обычном (не-pump) режиме забирает себе ровно один из них:

| Этап | Где выполняется | Комментарий |
| :--- | :--- | :--- |
| `./configure`, cmake, meson | **локально** | сотни мелких запусков компилятора, часто последовательно |
| Препроцессинг (`cpp`) | **локально** | нужны заголовки и вся структура проекта |
| **Компиляция `.i` → `.o`** | **удалённо** | ← это и есть весь профит |
| Ассемблирование | удалённо | вместе с компиляцией |
| **Линковка** | **локально** | требует все объектники и библиотеки |
| Установка, QA-проверки Portage | локально | |

Отсюда следуют все ограничения. Пакет, где много мелких файлов и тяжёлая оптимизация, ускорится сильно. Пакет, где полчаса идёт `./configure`, а потом линкуется один огромный бинарь, — почти нет.

Из man-страницы `distcc(1)`, про выбор `-j`:

> *«As a rule of thumb, the `-j` value should be set to about twice the total number of available server CPUs but subject to client limitations.»*

---

## 2. Что устарело в источниках

### Статья на «Хакере» (10 ноября 2010)

Ей шестнадцать лет. Общая идея верна, конкретика — нет:

| Что в статье | Как сейчас |
| :--- | :--- |
| `FEATURES="ccache"` в Portage | ✅ работает до сих пор, `dev-util/ccache` **4.13.5** |
| Советы про pump-режим | ❌ в Gentoo вырезано полностью (раздел ниже) |
| `MAKEOPTS="-j8"` при 4 ядрах | ⚠️ формула для distcc другая, см. раздел 7 |
| `CFLAGS='-O0'` для скорости сборки | ⚠️ верно как приём, но с distcc теряет смысл: компиляцию вы и так отдали |
| Сборка во `tmpfs` даёт «в среднем 10%» | ✅ приём живой, и с distcc он даже полезнее — локально остаётся линковка |
| Настройка под FreeBSD с симлинками на gcc | ⚠️ на Gentoo этим занимается `eselect compiler-shadow` |

### Gentoo Wiki

Актуальна и остаётся основным источником, но и в ней есть исторические куски про pump, о чём она сама предупреждает.

### Сам distcc

Проект **жив, но заморожен**: `distcc/distcc`, 2303 звезды, GPL-2.0, **163 открытых issue**. Последний релиз — **v3.4 от 11 мая 2021 года**, пять лет назад. Коммиты в 2026 году есть (6 мая, 17 февраля, 9 января), но между 2022 и 2026 — почти пустота. Gentoo тянет ту же 3.4, но с девятью ревизиями патчей: `sys-devel/distcc-3.4-r9`, стабильна на amd64.

---

## 3. Pump-режим: почему его больше нет

Это первое, обо что спотыкаются по старым гайдам. Pump-режим отдавал на удалённую машину ещё и препроцессинг — то есть весь профит, ради которого его и включали.

**Ebuild говорит прямым текстом.** Из `pkg_postinst` в `distcc-3.4-r9.ebuild`:

```bash
elog "distcc-pump is broken and no longer installed."
```

**Portage опции больше не знает.** В `lib/portage/const.py` списка `SUPPORTED_FEATURES` слова `pump` нет ни разу: есть `distcc`, `ccache`, `icecream`, `getbinpkg`, `buildpkg` — и всё.

**Причина — баг [Gentoo #702146](https://bugs.gentoo.org/702146)**, «sys-apps/portage: consider removing FEATURES=distcc-pump feature from portage», заведён 6 декабря 2019, закрыт RESOLVED FIXED 21 октября 2021. Из первого комментария (slyfox):

> *«Me and mattst88 spent some time debugging miscompilation of glibc on #gentoo-mips. We found out distcc-pump to be the failure trigger.»*

И дальше цитата из документации самого pump:

> *«Note that distcc's pump-mode assumes that sources files will not be modified during the lifetime of the include server, so modifying source files during a build may cause inconsistent results.»*

> *«I don't think it holds even for ./configure scripts.»*

Во втором комментарии — почему это неизбежно ломается: pump добавили в `src_configure()`, что напрямую нарушает допущение о неизменности исходников; а `gcc` вообще собирает stage2 и stage3 в одном каталоге, порождая промежуточные исходники и заголовки по ходу дела.

> [!caution] Практический вывод
> Если в гайде встречается `,cpp` в списке хостов, `pump emerge` или `FEATURES="distcc-pump"` — гайд написан до 2021 года. Опции `,cpp` в `/etc/distcc/hosts` просто не сработает: бинарника `pump` в системе нет.

---

## 4. Направление соединения — про реверс-туннель

Тут важная поправка к постановке задачи.

### Кто кому звонит

```
  Локальная Gentoo (серый IP, за NAT)          VPS (белый IP)
  ┌───────────────────────────────┐            ┌──────────────────┐
  │ emerge → Portage              │            │                  │
  │   └─ gcc → distcc (КЛИЕНТ) ───┼──исходящее→│ distccd (СЕРВЕР) │
  │      препроцессинг, линковка  │            │ компиляция .i→.o │
  └───────────────────────────────┘            └──────────────────┘
```

**Клиент — это ваша локальная машина**, и именно она устанавливает соединение. Серый IP на стороне клиента не мешает ровно так же, как он не мешает открыть сайт в браузере. NAT пропускает исходящие соединения.

**Реверс-туннель (`ssh -R`) нужен в обратной ситуации** — когда за NAT находится тот, к кому надо подключиться. Здесь это не так: у VPS белый IP, он и есть цель. Если вы уже держите `ssh -R` с локальной машины на VPS для управления ею снаружи — это отдельная история, к distcc она отношения не имеет и её трогать не надо.

### Три рабочих варианта транспорта

**Вариант A — родной SSH-режим distcc. Рекомендую.**

Ни одного открытого порта, демон на VPS вообще не запускается. Из `distccd(1)`:

> *«For SSH connections, distccd must be installed on the volunteer but should not run as a daemon — it will be started over SSH as needed.»*

Клиент на каждое задание запускает `ssh vps distccd --inetd`. В списке хостов это префикс `@`:

```
@build@vps.example.com/16
```

**Вариант B — демон на TCP только на loopback плюс проброс порта.**

```bash
# на VPS: демон слушает только себя
DISTCCD_OPTS="--listen 127.0.0.1 --allow 127.0.0.1 --port 3632 ..."

# на локальной машине: прямой проброс (-L, не -R!)
ssh -f -N -L 3632:127.0.0.1:3632 build@vps.example.com
```

и в списке хостов `127.0.0.1:3632/16`. Смысл варианта — одно TCP-соединение на всё вместо SSH-сессии на каждый файл, поэтому по накладным расходам он быстрее A. Минус — надо следить за живучестью туннеля (`autossh` или systemd-юнит).

**Вариант C — реверс-туннель `ssh -R`.** Нужен, только если роли перевернутся: VPS станет клиентом и будет собирать что-то для себя вашими руками. Для описанной задачи — не нужен.

### Обязательно: мультиплексирование SSH

В варианте A distcc поднимает **отдельную SSH-сессию на каждый компилируемый файл**. При `-j16` это шестнадцать параллельных рукопожатий, и на крупном пакете накладные расходы съедают выигрыш. Лечится мультиплексированием — в `~/.ssh/config`:

```
Host vps
    HostName vps.example.com
    User build
    IdentityFile ~/.ssh/id_ed25519_distcc
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 10m
    Compression no
    ServerAliveInterval 30
```

`Compression no` — намеренно: distcc умеет сжимать сам (`,lzo`), а двойное сжатие только жжёт CPU. Мастер-соединение поднимается один раз, остальные идут по нему без рукопожатия.

> [!tip] Проверка, что мультиплексирование работает
> ```bash
> ssh -O check vps        # Master running (pid NNNN)
> ```

---

## 5. Что обязано совпадать на обеих машинах

Это главный источник боли, а не сеть.

### Версия GCC

Клиент препроцессирует своими заголовками и своим gcc, а компилирует `.i` — **удалённый** gcc. Разные мажорные версии дают либо ошибки на незнакомых встроенных функциях и прагмах, либо, что хуже, тихо другой объектный код. Из Gentoo Wiki:

> *«mixing 3.3.x (where the x varies) is okay, but mixing 3.3.x with 3.2.x may result in compilation errors or runtime errors»*

Проверять на обеих машинах:

```bash
gcc --version
gcc -dumpmachine        # CHOST, должен совпадать: x86_64-pc-linux-gnu
ld --version | head -1  # binutils тоже сверить
```

На Gentoo: `eselect binutils list` и `gcc-config -l`.

### Флаги `-march` — почему `native` категорически нельзя

Механика, которую вики просто постулирует, а понимать её стоит: distcc передаёт удалённому gcc **ту же командную строку**, включая `-march=native`. Удалённый gcc честно раскрывает `native` в **свой** процессор. У вас на VPS Zen 4 (7950X3D) с AVX-512; если локальная машина старше, вы получите объектники с инструкциями, которых локальный процессор не знает, и `SIGILL` в рантайме — иногда через недели, в редко вызываемой функции.

Как выяснить, что раскрывает `native` на каждой машине:

```bash
gcc -march=native -Q --help=target | grep -E '^\s+-march=|^\s+-mtune='
emerge -av app-misc/resolve-march-native && resolve-march-native
```

Дальше — общий знаменатель в `/etc/portage/make.conf` **на клиенте**:

```bash
# вариант «по уровню», безопасно и переносимо
COMMON_FLAGS="-O2 -pipe -march=x86-64-v3 -mtune=native"

# либо явная микроархитектура, если обе машины одного поколения
# COMMON_FLAGS="-O2 -pipe -march=znver4 -mtune=znver4"

CFLAGS="${COMMON_FLAGS}"
CXXFLAGS="${COMMON_FLAGS}"
FCFLAGS="${COMMON_FLAGS}"
FFLAGS="${COMMON_FLAGS}"
```

Уровни `x86-64-v2` / `v3` / `v4` — это фиксированные наборы: `v3` примерно AVX2 и подходит для всего, что новее Haswell и Excavator; `v4` требует AVX-512, то есть на VPS пройдёт, а на большинстве домашних процессоров нет. `-mtune` безопасен: он влияет только на планировщик инструкций, а не на набор.

> [!warning] Ловушка
> `-mtune=native` тоже раскроется на удалённой стороне в её собственный процессор. Код останется рабочим, но затюненным под Zen 4. Если хочется строгости — пишите `-mtune` явно.

---

## 6. Установка и настройка

### Клиент — локальная Gentoo

```bash
emerge -av sys-devel/distcc
```

Пакет `sys-devel/distcc-3.4-r9`, EAPI 8, `IUSE="gssapi gui hardened ipv6 selinux xinetd zeroconf"`. Из зависимостей интересны две: `acct-user/distcc` — **системный пользователь `distcc` создаётся автоматически**, руками заводить не надо; и `>=dev-util/shadowman-4` — механизм подмены компилятора.

Список хостов:

```bash
distcc-config --set-hosts "@build@vps/16 localhost/4"
# или напрямую в /etc/distcc/hosts
```

Подключение к Portage, `/etc/portage/make.conf`:

```bash
FEATURES="${FEATURES} distcc"
MAKEOPTS="-j20 -l8"
```

Как это работает: `FEATURES="distcc"` заставляет Portage подставить `/usr/lib/distcc/bin` в начало `PATH`. Там лежат симлинки `gcc`, `g++`, `cc`, `c++` на `/usr/bin/distcc`, созданные через `eselect compiler-shadow update distcc`. Ebuild делает это сам в `pkg_postinst`.

### Сервер — VPS

Если VPS на Gentoo, всё симметрично. Если на Debian/Ubuntu или Arch — ставится штатным пакетом, но **версию gcc придётся подгонять** (раздел 5). Самый чистый вариант при разных дистрибутивах — поднять на VPS Gentoo-контейнер или chroot с тем же профилем: тогда совпадение toolchain'а гарантировано, и заодно можно собирать бинарные пакеты (раздел 10).

**Для варианта A (SSH) демон не нужен вообще.** Нужны только:

```bash
# отдельный непривилегированный логин для distcc
useradd -m -s /bin/bash build
mkdir -p /home/build/.ssh && chmod 700 /home/build/.ssh
# положить публичный ключ клиента с ограничениями:
# command="distccd --inetd",no-agent-forwarding,no-port-forwarding,no-pty,no-X11-forwarding ssh-ed25519 AAAA...
```

Ограничение `command=` в `authorized_keys` — важная деталь: этот ключ сможет запускать **только** distccd, и никакой интерактивной оболочки не даст. Ради «посмотреть, что distcc работает» логиньтесь вторым, обычным ключом.

**Для варианта B (TCP + туннель)** правится `/etc/conf.d/distccd`. Gentoo кладёт туда шаблон, в котором по умолчанию стоит `--allow 192.168.0.0/24` — его надо заменить:

```bash
DISTCCD_OPTS="--port 3632"
DISTCCD_OPTS="${DISTCCD_OPTS} --log-level notice --log-file /var/log/distccd.log"
DISTCCD_OPTS="${DISTCCD_OPTS} --listen 127.0.0.1 --allow 127.0.0.1"
DISTCCD_OPTS="${DISTCCD_OPTS} --jobs 16 -N 5"
```

```bash
touch /var/log/distccd.log && chown distcc:root /var/log/distccd.log
rc-update add distccd default && rc-service distccd start   # OpenRC
systemctl enable --now distccd                              # systemd
```

> [!danger] Никогда не выставляйте distccd в интернет
> Из документации Gentoo дословно: *«Anyone who can connect to the distcc server port can run arbitrary commands on that machine as the distccd user.»* Аутентификации в TCP-режиме нет вообще. На VPS с белым IP порт 3632 наружу — это готовая точка входа. Только `--listen 127.0.0.1` плюс туннель, либо SSH-режим.

Значения по умолчанию, о которых полезно знать: `--jobs` по умолчанию равен **числу CPU + 2**, `--nice` по умолчанию **+5** (Gentoo в своём шаблоне ставит `-N 15`, что для выделенного билд-сервера избыточно — там компиляция и есть основная работа).

### Синтаксис списка хостов

Полная грамматика из `distcc(1)`:

```
HOSTSPEC = LOCAL_HOST | SSH_HOST | TCP_HOST | OLDSTYLE_TCP_HOST | GLOBAL_OPTION | ZEROCONF
LOCAL_HOST = localhost[/LIMIT] | --localslots=<int> | --localslots_cpp=<int>
SSH_HOST   = [USER]@HOSTID[/LIMIT][:COMMAND][OPTIONS]
TCP_HOST   = HOSTID[:PORT][/LIMIT][OPTIONS]
OPTION     = lzo | cpp | auth[=AUTH_NAME]
```

Что из этого пригодится:

| Запись | Смысл |
| :--- | :--- |
| `@build@vps/16` | SSH-режим, пользователь `build`, до 16 заданий |
| `127.0.0.1:3632/16` | TCP через проброшенный порт |
| `localhost/4` | локальные задания, идут напрямую без демона |
| `,lzo` | LZO-сжатие — включать, канал до VPS не бесплатный |
| `--localslots=2` | сколько «нераспределяемых» работ (линковка) идёт параллельно локально |
| `--localslots_cpp=8` | сколько препроцессоров параллельно; **по умолчанию 8** |

**Порядок важен.** distcc предпочитает хосты в начале списка. Из man:

> *«As a general rule, if the aggregate CPU speed of the client is less than one fifth of the total, then the client should be left out of the list.»*

То есть если ваша локальная машина заметно слабее VPS — `localhost` из списка стоит убрать совсем, оставив только `--localslots`.

---

## 7. MAKEOPTS под 8 ядер VPS

Формула из вики: `-jN` где N = (удалённые ядра × 2) + (локальные ядра × 2) + 1, и `-lM` где M = число локальных ядер.

Для VPS с 8 ядрами и, скажем, 4-ядерного локального ноутбука: N = 16 + 8 + 1 = **25**. Но 25 параллельных заданий — это ещё и 25 препроцессоров локально, а препроцессинг никуда не делся. Практичнее начать скромнее и померить:

```bash
MAKEOPTS="-j20 -l8"
```

`-l` (load average) здесь важнее, чем `-j`: он не даёт make плодить новые задания, когда локальная машина уже задыхается на препроцессинге и линковке.

**Про память на VPS.** 16 ГБ на 8 ядер — это 2 ГБ на задание, чего хватает почти всегда, но не всегда: LTO-линковка chromium, rust-bootstrap и webkit-gtk отъедают куда больше. Впрочем, линковка выполняется **локально**, так что на VPS прилетают только компиляции отдельных единиц трансляции — там 2 ГБ на задание с запасом. Ограничение `--jobs 16` на сервере не даст перегрузить его, даже если клиент попросит больше.

---

## 8. Как убедиться, что оно реально работает

Ради этого и заводится отдельный пользователь на VPS — чтобы зайти и посмотреть.

### На клиенте: монитор

Portage хранит состояние distcc не в домашнем каталоге, поэтому `distccmon-text` без переменной покажет пустоту. Правильная команда прямо из `pkg_postinst` ebuild'а:

```bash
DISTCC_DIR="/var/tmp/portage/.distcc" distccmon-text 5
```

Обновляется каждые 5 секунд, показывает по строке на задание: PID, фаза (`Preprocess`, `Compile`, `Receive`), файл и хост. Если все строки с `localhost` — распределение не работает.

### На клиенте: подробный лог одной сборки

```bash
export DISTCC_VERBOSE=1
export DISTCC_LOG=/tmp/distcc.log
emerge -av1 какой-нибудь-пакет
grep -c "would prefer to run" /tmp/distcc.log
```

Быстрая проверка без Portage:

```bash
echo 'int main(){return 0;}' > /tmp/t.c
DISTCC_VERBOSE=1 distcc gcc -c /tmp/t.c -o /tmp/t.o
```

В выводе должно быть видно имя удалённого хоста. Если написано `failed to distribute, running locally` — читайте причину рядом, она всегда указана.

### На VPS: смотрим со стороны сервера

```bash
# кто пришёл и что делает
tail -f /var/log/distccd.log

# живые процессы компиляции
watch -n1 'ps -eo user,pcpu,etime,args | grep -E "cc1|distccd" | head -20'

# нагрузка
htop
```

В SSH-режиме процессы будут висеть под пользователем `build`, в TCP-режиме — под `distcc`.

### Контрольный замер

Честнее всего мерить не «время emerge», а один и тот же пакет дважды:

```bash
time emerge -1 --nodeps sys-apps/file        # с FEATURES="distcc"
FEATURES="-distcc" time emerge -1 --nodeps sys-apps/file
```

Берите что-нибудь среднее по размеру — на мелких пакетах накладные расходы съедят всё, и вывод будет ложным.

---

## 9. Что не поедет через distcc

| Что | Почему |
| :--- | :--- |
| **Rust** (`dev-lang/rust`, всё на cargo) | distcc понимает только C/C++/Objective-C. `rustc` мимо |
| **Go** | своя система сборки, компилятор не gcc |
| **Ядро Linux** | технически можно, но `make` ядра плохо дружит с большими `-j` при distcc; проще собирать локально |
| **LTO** | основная работа переезжает на этап линковки, а он локальный. Профит почти обнуляется |
| `sys-devel/gcc`, `sys-libs/glibc` | Portage сам исключает часть тулчейн-пакетов; и это правильно — собирать компилятор чужим компилятором чревато |
| `./configure`-стадия любых пакетов | тысячи мелких запусков, все локально |
| Пакеты с `RESTRICT` на распределение | редко, но встречается |

Отдельно: **если в CFLAGS остался `-march=native`, distcc опасен для всего** — см. раздел 5.

---

## 10. Чем это часто лучше заменить

Честный разбор: для сценария «одна слабая машина + один мощный сервер, обе на Gentoo» distcc — не лучший инструмент.

### Бинарный хост (binhost) — обычно выигрывает

Идея: VPS собирает **пакеты целиком** в chroot с вашим профилем и раздаёт их по HTTP. Локальная машина ничего не компилирует вообще.

```bash
# на VPS, в chroot с идентичным make.conf:
FEATURES="buildpkg"
BINPKG_FORMAT="gpkg"        # значение по умолчанию, подписи работают только с ним
# раздать /var/cache/binpkgs любым http-сервером

# на клиенте: /etc/portage/binrepos.conf/myvps.conf
# [myvps]
# priority = 9999
# sync-uri = https://vps.example.com/binpkgs
# verify-signature = true
FEATURES="getbinpkg"
emerge -avuDNg @world
```

> [!note] Не `PORTAGE_BINHOST`
> Переменная `PORTAGE_BINHOST` из `make.conf` **объявлена устаревшей** — `make.conf(5)`: *«The PORTAGE_BINHOST variable is deprecated in favor of the binrepos.conf configuration file»*. Новые конфиги пишутся в `/etc/portage/binrepos.conf`, где есть приоритеты источников и попакетная проверка подписи.

Подробный разбор — в [отдельной заметке про binhost](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md).

Почему это лучше distcc в вашем случае:

| Критерий | distcc | binhost |
| :--- | :--- | :--- |
| Линковка | локально | на сервере |
| `./configure` | локально | на сервере |
| Rust, Go, ядро | не ускоряет | ускоряет |
| Совпадение gcc | обязательно | не требуется |
| Задержка сети | на каждый файл | один раз на пакет |
| Нагрузка на клиент | заметная | почти нулевая |
| Сложность настройки | средняя | средняя |
| Требует `-march` общий | да | да, профиль должен совпадать |

Ограничение binhost — USE-флаги и профиль на сервере должны совпадать с клиентскими, иначе пакеты не подойдут. Зато при совпадении локальная машина превращается в потребителя готового, как Debian.

### icecream (icecc)

Всё ещё поддерживается Portage — `FEATURES="icecream"` есть в `SUPPORTED_FEATURES`. Умнее distcc в балансировке и, главное, **сам раздаёт тулчейн на узлы**, снимая проблему совпадения gcc. Смысл появляется от трёх машин; для схемы «клиент + один сервер» усложнение не окупается.

### ccache — не замена, а дополнение

`dev-util/ccache` 4.13.5, `FEATURES="ccache"`. Ускоряет **повторную** сборку того же кода, distcc — первую. Работают вместе, но связывать их надо через `CCACHE_PREFIX="distcc"`, а не строкой вида `CC="ccache distcc gcc"`: во втором случае ccache начнёт хешировать бинарник distcc вместо настоящего компилятора и перестанет замечать обновления gcc.

Гентушная вики при этом **не советует включать ccache глобально** — попаданий на обычном `@world` почти не бывает. Подробности и правильная настройка — в [отдельной заметке про ccache](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md).

---

## 11. По системам

**Gentoo (клиент и, желательно, сервер):**

```bash
emerge -av sys-devel/distcc
distcc-config --set-hosts "@build@vps/16 --localslots=2"
# make.conf: FEATURES="distcc", MAKEOPTS="-j20 -l8", -march без native
rc-update add distccd default   # только если TCP-режим
```

**Debian / Ubuntu (если VPS на них):**

```bash
apt install distcc
# /etc/default/distcc: STARTDISTCC="true", ALLOWEDNETS="127.0.0.1",
#                      LISTENER="127.0.0.1", JOBS="16"
systemctl enable --now distcc
gcc --version   # сверить с клиентом — здесь основная засада
```

**Arch (планируется с июня 2026):**

```bash
pacman -S distcc
# /etc/conf.d/distccd: DISTCC_ARGS="--allow 127.0.0.1 --listen 127.0.0.1 --jobs 16"
systemctl enable --now distccd
# для makepkg: в /etc/makepkg.conf снять комментарий с DISTCC_HOSTS и
# добавить distcc в BUILDENV
```

**Entware / ASUS RT-AX56U:** в репозитории `armv7sf-k3.2` пакета `distcc` **нет**. Да он там и не нужен: роутеру нечего компилировать, а как узел-помощник armv7 с 512 МБ ОЗУ бесполезен. Если когда-нибудь понадобится собирать **для** роутера — это задача кросс-компиляции через `crossdev` на большой машине, а не distcc на самом роутере.

---

## 12. Кому стоит и когда не стоит

| Ситуация | Вердикт |
| :--- | :--- |
| Локальная машина — слабый ноутбук, VPS мощный, обе на Gentoo | **Стоит попробовать, но сначала оцените binhost** — он закроет задачу полнее |
| Локальная машина сама быстрая, VPS — довесок | Профит небольшой, накладные расходы съедят часть |
| Канал до VPS узкий или с большими задержками | **Не стоит.** Каждый `.i`-файл едет по сети; на 20 мс RTT и `-j20` это заметно |
| VPS на другом дистрибутиве | Сначала решите вопрос с версией gcc, иначе получите тихую порчу объектников |
| Собираете в основном Rust/Go/ядро | **Не стоит**, distcc их не трогает |
| Нужен один разовый большой пакет | Проще собрать его на VPS целиком и забрать бинарь |

Разумный порядок действий: сначала **binhost** — он закрывает задачу целиком и не требует совпадения версий gcc; потом distcc, если хочется именно распределённой сборки в реальном времени; `ccache` — точечно и скорее на сборочном сервере, чем на клиенте.

---

## Связанные заметки

- [Kernel — сборка или обновление ядра](../Gentoo/Kernel%20-%20%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%D0%BB%D0%B8%20%D0%9E%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%8F%D0%B4%D1%80%D0%B0.md) — то, что distcc как раз не ускорит
- [SSH-Ключи](../../Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md) — ключ для пользователя `build` с ограничением `command=`
- [SSH — продвинутое руководство](../../Network/SSH/SSH-%D0%9F%D1%80%D0%BE%D0%B4%D0%B2%D0%B8%D0%BD%D1%83%D1%82%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md) — `ControlMaster`, `authorized_keys`-ограничения
- [SSH — визуальное руководство по туннелям](../../Network/SSH/SSH-%D0%92%D0%B8%D0%B7%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE%20%D0%BF%D0%BE%20%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8F%D0%BC.md) — разница `-L` и `-R` картинками, ровно про раздел 4
- [sshm (Gu1llaum-3)](../../Network/SSH/sshm%20%28Gu1llaum-3%29%20%E2%80%94%20TUI-%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20SSH-%D1%85%D0%BE%D1%81%D1%82%D0%BE%D0%B2%20%D0%BD%D0%B0%20Go%20%D0%BF%D0%BE%D0%B2%D0%B5%D1%80%D1%85%20~-.ssh-config.md) — держать VPS в списке хостов
- [Сравнение команд менеджеров пакетов](../Package-Manager/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2.md) — если VPS не на Gentoo
- [Learning Rust (dumindu)](../../Programming/Rust/Learning%20Rust%20%28dumindu%29%20%E2%80%94%20%D1%81%D0%B6%D0%B0%D1%82%D1%8B%D0%B9%20%D1%83%D1%87%D0%B5%D0%B1%D0%BD%D0%B8%D0%BA%20%D0%BF%D0%BE%20Rust%20%E2%80%94%2031%20%D0%B3%D0%BB%D0%B0%D0%B2%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%C2%AB%D0%B7%D0%B0%20%D0%BC%D0%B5%D1%81%D1%8F%D1%86%C2%BB%20%D0%B8%20%C2%AB%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%C2%BB%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F%20NON-AI%2C%20%D1%87%D0%B5%D0%BC%20%D0%B4%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D1%8C%29.md) — почему `dev-lang/rust` distcc не ускорит

## Ссылки

- Gentoo Wiki, distcc (RU): https://wiki.gentoo.org/wiki/Distcc/ru
- Gentoo Wiki, distcc (EN, свежее): https://wiki.gentoo.org/wiki/Distcc
- Gentoo Wiki, кросс-компиляция через distcc: https://wiki.gentoo.org/wiki/Distcc/Cross-Compiling
- Баг о вырезании pump-режима: https://bugs.gentoo.org/702146
- Upstream distcc: https://github.com/distcc/distcc
- Ebuild `distcc-3.4-r9`: https://gitweb.gentoo.org/repo/gentoo.git/tree/sys-devel/distcc
- man distcc(1): https://github.com/distcc/distcc/blob/v3.4/man/distcc.1
- man distccd(1): https://github.com/distcc/distcc/blob/v3.4/man/distccd.1
- Gentoo Wiki, бинарные пакеты: https://wiki.gentoo.org/wiki/Binary_package_guide
- Gentoo Wiki, ccache: https://wiki.gentoo.org/wiki/Ccache
- Статья на «Хакере» (2010, во многом устарела): https://xakep.ru/2010/11/10/53558/

#Gentoo #Portage #distcc #ccache #Сборка #Компиляция #SSH #VPS #Оптимизация #binhost
