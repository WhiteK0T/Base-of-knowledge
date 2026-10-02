---
создал заметку: 2026-10-02T13:00:00
author: WhiteK0T
tags:
  - Linux
  - Gentoo
  - MOTD
  - PAM
  - Shell
---

# 🖥️ MOTD в Gentoo — динамический баннер входа

Как в Gentoo выводить баннер при входе (**MOTD**, message of the day) и как подключить свой скрипт. Плюс разбор, почему типовой «дебиановский» MOTD-скрипт на Gentoo не заводится как есть, и рабочая адаптированная версия.

## ⚙️ Как это устроено

Показ MOTD делает PAM-модуль **`pam_motd`**. В Gentoo (pam ≥1.7) в `/etc/pam.d/system-login`:
```
session  optional  pam_motd.so motd=/etc/motd
```
То есть при каждом **входе** (консоль и SSH) один раз печатается **статический файл `/etc/motd`**. Сам pam_motd скрипты **не запускает** — только читает файл. Отсюда два способа подключить динамический скрипт:

| Хочу | Способ |
| :--- | :--- |
| **Живой** баннер (uptime, нагрузка, память) при каждом входе | **A. `/etc/profile.d`** — скрипт печатает вывод при логине |
| Классический MOTD «один раз до шелла», одинаково SSH/консоль | **B. писать в `/etc/motd`** + регенерация (OpenRC `local.d` / cron / `pam_exec`) |

Для баннера с живыми данными (как скрипт ниже) — **вариант A**.

---

## ⚠️ Почему дебиановский скрипт не работает на Gentoo

Исходный скрипт (ниже) написан под Debian/Ubuntu. На Gentoo ломается в трёх местах (проверено на `whitek0t.tehlab.org`):

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

## ✅ Gentoo-версия (проверено запуском)

С цветным баром памяти/свопа (зелёный <70%, жёлтый ≥70%, красный ≥90%) и списком ников залогиненных.

```bash
#!/bin/bash
# MOTD-баннер — Gentoo-адаптация. Исходник: WhiteK0T.
tcLtG="\033[00;37m"; tcLtGRN="\033[01;32m"; tcLtBL="\033[01;34m"
tcORANGE="\033[38;5;209m"; tcRESET="\033[0m"; tcDkG="\033[01;30m"

# Цветной бар: $1=процент (float/int), $2=ширина. Цвет по порогам.
bar() {
  local pct=${1%.*}; [ -z "$pct" ] && pct=0
  local width=${2:-24}
  local filled=$(( pct * width / 100 )); (( filled > width )) && filled=$width
  local empty=$(( width - filled )); (( empty < 0 )) && empty=0
  local c
  if   (( pct >= 90 )); then c="\033[01;31m"     # красный
  elif (( pct >= 70 )); then c="\033[01;33m"     # жёлтый
  else                      c="\033[01;32m"; fi  # зелёный
  local f= e= i
  for ((i=0;i<filled;i++)); do f="$f█"; done
  for ((i=0;i<empty;i++));  do e="$e░"; done
  printf '%b' "${c}${f}${tcDkG}${e}${tcRESET} ${c}${pct}%${tcRESET}"
}

HOUR=$(date +%H)
if   [ "$HOUR" -lt 12 ]; then TIME="morning"
elif [ "$HOUR" -lt 17 ]; then TIME="afternoon"
else TIME="evening"; fi

up=$(cut -d. -f1 /proc/uptime)
upDays=$((up/86400)); upHours=$((up/3600%24)); upMins=$((up/60%60))

SYS_LOADS=$(awk '{print $1}' /proc/loadavg)
MEMORY_USED=$(free -b | awk '/Mem/{printf "%.1f", $3/$2*100}')
SWAP_USED=$(free -b | awk '/Swap/{if($2>0) printf "%.1f", $3/$2*100; else printf "0.0"}')
NUM_PROCS=$(($(ps aux | wc -l) - 1))
NUM_USERS=$(users | wc -w)
USERS_LIST=$(users | tr ' ' '\n' | sort -u | paste -sd' ')   # уникальные ники
# реальные IP (net-tools hostname не умеет --all-ip-addresses):
IPADDRESS=$(ip -o addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | paste -sd' ')
# ОС без debian_version/lsb:
OS_REL=$( . /etc/os-release 2>/dev/null; printf '%s' "$PRETTY_NAME" )
[ -r /etc/gentoo-release ] && OS_REL="$OS_REL [$(cat /etc/gentoo-release)]"
# Физические ядра / логические потоки (HT):
THREADS=$(grep -c '^processor' /proc/cpuinfo)
CORES=$(awk -F: '/^physical id/{p=$2} /^core id/{seen[p":"$2]=1} END{n=0; for(k in seen) n++; print n}' /proc/cpuinfo)
[ "${CORES:-0}" -le 0 ] && CORES=$THREADS   # ARM/без core id → ядра=потоки
# FQDN, с откатом на короткое имя (hostname -f пуст, если FQDN не резолвится):
HOSTN=$(hostname -f 2>/dev/null); [ -z "$HOSTN" ] && HOSTN=$(hostname)

printf '%b\n' "${tcLtG}================================================================="
printf '%b\n' "${tcLtG} Good ${TIME}!                                   ${tcORANGE}by WhiteK0T.${tcRESET}"
printf '%b\n' "${tcLtG}================================================================="
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
printf '%b\n' "${tcLtG}=================================================================${tcRESET}"
```

Пример вывода (бар зелёный при малой загрузке):
```
 - Users             : 1 logged on
 - Logged in         : claude
 - System load       : 0.08 / 223 processes
 - Memory used       : █░░░░░░░░░░░░░░░░░░░░░░░ 7%
 - Swap used         : ░░░░░░░░░░░░░░░░░░░░░░░░ 0%
```

Что изменено против оригинала: `printf '%b'` вместо `echo` (цвета в bash), `/etc/os-release`+`/etc/gentoo-release` вместо `lsb_release`/`debian_version`, `ip -o addr` вместо `hostname --all-ip-addresses`, корректный подсчёт процессов (`-1` на заголовок `ps`), ядра/потоки из `/proc/cpuinfo` (физические ядра и логические потоки HT). **Добавлено:** функция `bar()` — цветной индикатор загрузки (память и своп, порог 70/90 %), и строка **Logged in** с уникальными никами залогиненных (`users | sort -u`).

> [!note] Пустой Hostname
> Если `hostname -f` ничего не выводит (FQDN не резолвится — нет записи в `/etc/hosts`/DNS), строка Hostname будет пустой. Поэтому в версии выше — переменная `HOSTN` с откатом на короткое имя: `HOSTN=$(hostname -f 2>/dev/null); [ -z "$HOSTN" ] && HOSTN=$(hostname)`.

> [!tip] Если бар отображается «кракозябрами»
> Символы `█`/`░` требуют **UTF-8**-терминала и locale. Если выводится мусор — заменить в `bar()` на ASCII: `f="$f#"` и `e="$e-"`.

---

## 🔌 Подключение (вариант A — живой баннер при входе)

```bash
sudo install -m 0755 motd-gentoo.sh /usr/local/bin/motd.sh
printf '%s\n' '[ -x /usr/local/bin/motd.sh ] && /usr/local/bin/motd.sh' \
  | sudo tee /etc/profile.d/zz-motd.sh >/dev/null
```
- `zz-` → выполнится последним; вызываем скрипт **отдельным процессом**, чтобы переменные (`tcLtG`…) не утекали в сессию.
- Работает для всех **login-shell**: SSH и вход в консоль. Для себя одного — та же строка в `~/.bash_profile`.
- Не сработает для non-login shells (новые вкладки терминала в DE читают `.bashrc`).

**Вариант B** (классический `/etc/motd`): писать вывод в файл и регенерировать —
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

## 📦 Зависимости (emerge)

| Нужно | Пакет |
| :--- | :--- |
| `hostname -f` | `sys-apps/net-tools` |
| `free`, `ps`, `uptime` | `sys-process/procps` |
| `ip` | `sys-apps/iproute2` |
| `users`, `date`, `cut`, `paste`, `sort`, `tr` | `sys-apps/coreutils` |
| `grep`, `awk` (ядра/потоки из /proc/cpuinfo) | `sys-apps/grep`, `sys-apps/gawk` (базовые) |
| (опц.) `lsb_release` | `sys-apps/lsb-release` |

На Debian/Ubuntu работает и оригинал (там `/etc/debian_version`, dash-`/bin/sh` интерпретирует `\033`, coreutils-`hostname` знает `--all-ip-addresses`). На **Entware/роутере** — `printf` и `/proc` есть (busybox), но часть утилит (`free`, net-tools-`hostname`) урезаны; CPU-метод через `/proc/cpuinfo` (grep/awk) работает и там; баннер проще держать на десктопе/сервере.

## 🔗 Связанные заметки

- Службы и автозапуск в Gentoo (OpenRC `local.d`, `rc-update`) — см. раздел Gentoo.
- Цвета в терминале используют ANSI-escape (`\033[...`), интерпретируемые `printf '%b'`.

## 🔗 Ссылки

- Цвета/форматирование: [misc.flogisoft.com/bash/tip_colors_and_formatting](https://misc.flogisoft.com/bash/tip_colors_and_formatting)

#Linux #Gentoo #MOTD #PAM #Shell
