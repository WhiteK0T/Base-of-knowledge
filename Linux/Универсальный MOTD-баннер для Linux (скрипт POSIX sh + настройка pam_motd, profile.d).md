---
создал заметку: 2026-10-02T13:00:00
author: WhiteK0T
tags:
  - Linux
  - MOTD
  - Shell
  - PAM
  - Gentoo
  - Debian
---

# 🖥️ Универсальный MOTD-баннер для Linux

Готовый скрипт-баннер при входе (**MOTD**, message of the day) + как подключить его на разных дистрибутивах. Скрипт **кроссдистрибутивный** (чистый POSIX sh, все данные из `/proc` + базовые утилиты) — работает на Gentoo/Debian/Ubuntu/Arch/Alpine и под busybox. Ниже также разобрано, почему типовой «дебиановский» MOTD-скрипт пришлось переписать.

## ⚙️ Как это устроено

Показ MOTD делает PAM-модуль **`pam_motd`**: при каждом **входе** (консоль и SSH) один раз печатается **статический файл `/etc/motd`**. Сам pam_motd скрипты **не запускает** — только читает файл.
- **Gentoo** (pam ≥1.7): в `/etc/pam.d/system-login` → `session optional pam_motd.so motd=/etc/motd`.
- **Debian/Ubuntu**: pam_motd указывает на `/run/motd.dynamic`, который генерит `run-parts /etc/update-motd.d/` — туда и кладут исполняемые скрипты (самый простой путь на Debian).

Два способа подключить **динамический** скрипт:

| Хочу | Способ |
| :--- | :--- |
| **Живой** баннер (uptime, нагрузка, память) при каждом входе | **A. `/etc/profile.d`** (любой дистрибутив) или **`/etc/update-motd.d/`** (Debian) |
| Классический MOTD «один раз до шелла», одинаково SSH/консоль | **B. писать в `/etc/motd`** + регенерация (OpenRC `local.d` / cron / `pam_exec`) |

Для баннера с живыми данными (скрипт ниже) — **вариант A**.

---

## ⚠️ Почему дебиановский скрипт не работает на Gentoo

Исходный скрипт (ниже) написан под Debian/Ubuntu. На Gentoo ломается в трёх местах (проверено на живой системе):

1. **`cat /etc/debian_version`** — файла в Gentoo **нет** → ошибка. Замена: `/etc/gentoo-release` и/или `PRETTY_NAME` из `/etc/os-release`.
2. **`hostname --all-ip-addresses`** — у Gentoo `hostname` из **net-tools**, он такого флага **не знает** (это опция coreutils/Debian-hostname). Замена: `ip -o addr show scope global`.
3. **`#!/bin/sh` + `echo "\033[..."`** — в Gentoo **`/bin/sh → bash`**, а `echo` в bash **не интерпретирует** `\033` → вместо цветов печатается литеральное `\033[...`. Замена: `printf '%b'` (или shebang `#!/bin/bash` + `echo -e`).

`lsb_release` на этой машине есть (`sys-apps/lsb-release`), но он опционален — надёжнее брать `os-release`.

---

## 📜 Исходный скрипт (Debian-ориентированный, автор WhiteK0T)

<details><summary>раскрыть оригинал</summary>

```sh
#!/bin/sh
# Text Color Variables http://misc.flogisoft.com/bash/tip_colors_and_formatting
tcLtG="\033[00;37m"; tcDkG="\033[01;30m"; tcLtR="\033[01;31m"
tcLtGRN="\033[01;32m"; tcLtBL="\033[01;34m"; tcLtP="\033[01;35m"
tcLtC="\033[01;36m"; tcW="\033[01;37m"; tcRESET="\033[0m"; tcORANGE="\033[38;5;209m"

HOUR=$(date +"%H")
if [ $HOUR -lt 12  -a $HOUR -ge 0 ]; then TIME="morning"
elif [ $HOUR -lt 17 -a $HOUR -ge 12 ]; then TIME="afternoon"
else TIME="evening"; fi

uptime=`cat /proc/uptime | cut -f1 -d.`
upDays=$((uptime/60/60/24)); upHours=$((uptime/60/60%24)); upMins=$((uptime/60%60))

SYS_LOADS=`cat /proc/loadavg | awk '{print $1}'`
MEMORY_USED=`free -b | grep Mem | awk '{print $3/$2 * 100.0}'`
SWAP_USED=`free -b | grep Swap | awk '{print $3/$2 * 100.0}'`
NUM_PROCS=`ps aux | wc -l`
IPADDRESS=`hostname --all-ip-addresses`

echo $tcLtG "================================================================="
echo $tcLtG " Good $TIME !                                   $tcORANGE by WhiteK0T."
echo "\e[39m================================================================="
echo $tcLtGRN " - Server Date/Time  :$tcLtBL `date '+%a %d %b %Y / %X %Z'`"
echo $tcLtGRN " - Hostname          :$tcLtBL `hostname -f 2>/dev/null`"
echo $tcLtGRN " - IP Address        :$tcLtBL $IPADDRESS"
echo $tcLtGRN " - OS Release        :$tcLtBL $(lsb_release -s -d)[$(cat /etc/debian_version)]"
echo $tcLtGRN " - Kernel Release    :$tcLtBL `uname -r` "
echo $tcLtGRN " - Users             :$tcLtBL Currently `users | wc -w` user(s) logged on"
echo $tcLtGRN " - System load       :$tcLtBL $SYS_LOADS / $NUM_PROCS processes running"
echo $tcLtGRN " - Memory used %     :$tcLtBL $MEMORY_USED"
echo $tcLtGRN " - Swap used %       :$tcLtBL $SWAP_USED"
echo $tcLtGRN " - System uptime     :$tcLtBL $upDays days $upHours hours $upMins minutes"
echo $tcLtG "================================================================="
echo $tcRESET ""
```
</details>

---

## ✅ Универсальная версия (проверено на Gentoo и Debian)

С цветным баром памяти/свопа (зелёный <70%, жёлтый ≥70%, красный ≥90%) и списком ников залогиненных.

```bash
#!/bin/sh
#==============================================================================
#  motd.sh — универсальный MOTD-баннер для Linux (баннер при входе)
#  Хост, IP, ОС, ядро, CPU (ядра/потоки), пользователи, нагрузка, память, аптайм.
#  Кроссдистрибутивный: все данные из /proc + базовые утилиты, чистый POSIX sh
#  (работает под bash/dash/busybox-ash, на Gentoo/Debian/Ubuntu/Arch/Alpine...).
#
#  Автор:  WhiteK0T
#  GitHub: https://github.com/WhiteK0T/motd
#==============================================================================
tcLtG="\033[00;37m"; tcLtGRN="\033[01;32m"; tcLtBL="\033[01;34m"
tcORANGE="\033[38;5;209m"; tcRESET="\033[0m"; tcDkG="\033[01;30m"

# повтор символа N раз (POSIX, корректно с UTF-8)
rep() { _n=$1; _c=$2; _s=''; while [ "$_n" -gt 0 ]; do _s="$_c$_s"; _n=$((_n-1)); done; printf '%s' "$_s"; }

# цветной бар: $1=процент (float/int), $2=ширина. Цвет по порогам.
bar() {
  _p=${1%.*}; [ -z "$_p" ] && _p=0
  _w=${2:-24}
  _f=$(( _p * _w / 100 )); [ "$_f" -gt "$_w" ] && _f=$_w; [ "$_f" -lt 0 ] && _f=0
  _e=$(( _w - _f ))
  if   [ "$_p" -ge 90 ]; then _c="\033[01;31m"
  elif [ "$_p" -ge 70 ]; then _c="\033[01;33m"
  else                        _c="\033[01;32m"; fi
  printf '%b' "${_c}$(rep "$_f" '█')${tcDkG}$(rep "$_e" '░')${tcRESET} ${_c}${_p}%${tcRESET}"
}

HOUR=$(date +%H)
if   [ "$HOUR" -lt 12 ]; then TIME="morning"
elif [ "$HOUR" -lt 17 ]; then TIME="afternoon"
else TIME="evening"; fi

up=$(cut -d. -f1 /proc/uptime)
upDays=$((up/86400)); upHours=$((up/3600%24)); upMins=$((up/60%60))

SYS_LOADS=$(awk '{print $1}' /proc/loadavg)
set -- /proc/[0-9]*; NUM_PROCS=$#                      # процессы напрямую из /proc
MEMORY_USED=$(awk '/^MemTotal:/{t=$2}/^MemAvailable:/{a=$2} END{if(t>0)printf "%.1f",(t-a)/t*100; else print "0.0"}' /proc/meminfo)
SWAP_USED=$(awk '/^SwapTotal:/{t=$2}/^SwapFree:/{f=$2} END{if(t>0)printf "%.1f",(t-f)/t*100; else print "0.0"}' /proc/meminfo)
NUM_USERS=$(who 2>/dev/null | wc -l)
USERS_LIST=$(who 2>/dev/null | awk '{print $1}' | sort -u | paste -sd' ')

IPADDRESS=$(ip -o addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | paste -sd' ')
[ -z "$IPADDRESS" ] && IPADDRESS=$(hostname -I 2>/dev/null)

HOSTN=$(hostname -f 2>/dev/null); [ -z "$HOSTN" ] && HOSTN=$(hostname 2>/dev/null)
[ -z "$HOSTN" ] && HOSTN=$(cat /etc/hostname 2>/dev/null || uname -n)

OS_REL=$( . /etc/os-release 2>/dev/null; printf '%s' "$PRETTY_NAME" )
[ -z "$OS_REL" ] && OS_REL=$(uname -o 2>/dev/null || echo Linux)
[ -r /etc/gentoo-release ] && OS_REL="$OS_REL [$(cat /etc/gentoo-release)]"
[ -r /etc/debian_version ] && OS_REL="$OS_REL [$(cat /etc/debian_version)]"

THREADS=$(grep -c '^processor' /proc/cpuinfo)
CORES=$(awk -F: '/^physical id/{p=$2}/^core id/{s[p":"$2]=1} END{n=0;for(k in s)n++;print n}' /proc/cpuinfo)
[ "${CORES:-0}" -le 0 ] && CORES=$THREADS

SEP="======================================================================"
printf '%b\n' "${tcLtG}${SEP}"
printf '%b\n' "${tcLtG} Good ${TIME}!                                           ${tcORANGE}by WhiteK0T.${tcRESET}"
printf '%b\n' "${tcLtG}${SEP}"
printf '%b\n' "${tcLtGRN} - Server Date/Time  :${tcLtBL} $(date '+%a %d %b %Y / %X %Z')"
printf '%b\n' "${tcLtGRN} - Hostname          :${tcLtBL} ${HOSTN}"
printf '%b\n' "${tcLtGRN} - IP Address        :${tcLtBL} ${IPADDRESS}"
printf '%b\n' "${tcLtGRN} - OS Release        :${tcLtBL} ${OS_REL}"
printf '%b\n' "${tcLtGRN} - Kernel            :${tcLtBL} $(uname -r)"
printf '%b\n' "${tcLtGRN} - CPU Cores/Threads :${tcLtBL} ${CORES} / ${THREADS}"
printf '%b\n' "${tcLtGRN} - Users             :${tcLtBL} ${NUM_USERS} logged on"
printf '%b\n' "${tcLtGRN} - Logged in         :${tcLtBL} ${USERS_LIST}"
printf '%b\n' "${tcLtGRN} - System load       :${tcLtBL} ${SYS_LOADS} / ${NUM_PROCS} processes"
printf '%b\n' "${tcLtGRN} - Memory used       :${tcLtBL} $(bar "$MEMORY_USED" 24)"
printf '%b\n' "${tcLtGRN} - Swap used         :${tcLtBL} $(bar "$SWAP_USED" 24)"
printf '%b\n' "${tcLtGRN} - Uptime            :${tcLtBL} ${upDays}d ${upHours}h ${upMins}m"
printf '%b\n' "${tcLtG}${SEP}${tcRESET}"
```

Пример вывода (бар зелёный при малой загрузке):
```
 - Users             : 1 logged on
 - Logged in         : claude
 - System load       : 0.08 / 223 processes
 - Memory used       : █░░░░░░░░░░░░░░░░░░░░░░░ 7%
 - Swap used         : ░░░░░░░░░░░░░░░░░░░░░░░░ 0%
```

**Сделано универсальным** (любой дистрибутив, чистый POSIX sh — bash/dash/busybox): все данные берутся из `/proc` + базовые утилиты, без распределённо-специфичных команд. `printf '%b'` вместо `echo` (цвета в любом shell); память/своп из `/proc/meminfo` (без `free`), процессы из `/proc` (без `ps`), пользователи через `who`; кроссдистрибутивный OS Release (`PRETTY_NAME` + точная версия: `/etc/gentoo-release` **и** `/etc/debian_version`); `hostname -f`→короткое→`/etc/hostname`→`uname -n` с откатами; IP через `ip -o addr` с откатом на `hostname -I`; CPU — ядра/потоки из `/proc/cpuinfo`. Цветной бар памяти/свопа (порог 70/90 %) и строка **Logged in** с никами залогиненных.

> [!note] Пустой Hostname
> Если `hostname -f` ничего не выводит (FQDN не резолвится — нет записи в `/etc/hosts`/DNS), строка Hostname будет пустой. Поэтому в версии выше — переменная `HOSTN` с откатом на короткое имя: `HOSTN=$(hostname -f 2>/dev/null); [ -z "$HOSTN" ] && HOSTN=$(hostname)`.

> [!tip] Если бар отображается «кракозябрами»
> Символы `█`/`░` требуют **UTF-8**-терминала и locale. Если выводится мусор — заменить в `bar()` на ASCII: `f="$f#"` и `e="$e-"`.

---

## 🔌 Подключение (вариант A — живой баннер при входе)

**Любой дистрибутив — через `/etc/profile.d`:**
```bash
sudo install -m 0755 motd.sh /usr/local/bin/motd.sh
printf '%s\n' '[ -x /usr/local/bin/motd.sh ] && /usr/local/bin/motd.sh' \
  | sudo tee /etc/profile.d/zz-motd.sh >/dev/null
```
- `zz-` → выполнится последним; вызываем скрипт **отдельным процессом**, чтобы переменные (`tcLtG`…) не утекали в сессию.
- Работает для всех **login-shell**: SSH и вход в консоль. Для себя одного — та же строка в `~/.bash_profile`.
- Не сработает для non-login shells (новые вкладки терминала в DE читают `.bashrc`).

**Debian/Ubuntu — через `/etc/update-motd.d`** (нативный механизм; печатается один раз до шелла):
```bash
sudo install -m 0755 motd.sh /etc/update-motd.d/99-motd
# показывается через pam_motd из /run/motd.dynamic; проверить: run-parts /etc/update-motd.d/
```

**Вариант B** (классический `/etc/motd`, прочие дистрибутивы): писать вывод в файл и регенерировать —
```bash
# при загрузке, OpenRC:  /etc/local.d/motd.start
#!/bin/sh
/usr/local/bin/motd.sh > /etc/motd
```
```bash
sudo chmod +x /etc/local.d/motd.start && sudo rc-update add local default
# или периодически: crontab -e →  */5 * * * * /usr/local/bin/motd.sh > /etc/motd
# или свежо при входе: в /etc/pam.d/system-login НАД pam_motd добавить
#   session optional pam_exec.so quiet /usr/local/bin/motd.sh ... (пишущий /etc/motd)
```

> [!warning] Не тяжели
> Вариант A гоняет скрипт **при каждом входе** — не вставляй туда долгих команд (сетевые запросы и т.п.), иначе будет лаг логина.

---

## 📦 Зависимости

Универсальная версия намеренно обходится **минимумом** — почти всё из `@system`/base, плюс `ip` и `hostname`:

| Утилита | Откуда (Gentoo / Debian) | Примечание |
| :--- | :--- | :--- |
| `date cut paste sort wc cat uname who` | `coreutils` / `coreutils` | базовые |
| `grep`, `awk` | `grep`+`gawk` / `grep`+`gawk\|mawk` | ядра/потоки, парсинг |
| `ip` | `sys-apps/iproute2` / `iproute2` | IP-адреса (есть и в busybox) |
| `hostname` | `sys-apps/net-tools` / `inetutils`\|`hostname` | FQDN; есть фоллбэки |

> [!tip] Работает и на busybox (Entware/роутер)
> Поскольку всё берётся из `/proc` + POSIX sh, скрипт теперь **заводится и под busybox** (`who`, `ip`, `grep`, `awk`, `/proc` там есть). `free`/`ps`/`users` больше **не нужны** — память из `/proc/meminfo`, процессы из `/proc`, пользователи через `who`.

## 🔗 Связанные заметки

- Службы и автозапуск в Gentoo (OpenRC `local.d`, `rc-update`) — см. раздел Gentoo.
- Цвета в терминале используют ANSI-escape (`\033[...`), интерпретируемые `printf '%b'`.

## 🔗 Ссылки

- Цвета/форматирование: [misc.flogisoft.com/bash/tip_colors_and_formatting](https://misc.flogisoft.com/bash/tip_colors_and_formatting)

#Linux #MOTD #Shell #PAM #Gentoo #Debian
