---
создал заметку: 2026-09-28T11:00:00
author: WhiteK0T
tags:
  - Security
  - Forensics
  - DFIR
  - Linux
  - BlueTeam
  - Шпаргалка
Источник:
  - https://t.me/c/2675453029/1499
---

# 🛡️ Linux-команды для ИБ — шпаргалка (аудит, разбор инцидентов, поиск персистентности)

Расширенная версия шпоры из поста: команды поста сохранены и **поправлены** (устаревшее помечено), плюс добавлены разделы, которых там не было, — **поиск персистентности**, **таймлайн изменений**, **проверка целостности пакетов**, **скрытые процессы/файлы**. Всё под задачу «пришёл на систему — быстро понять состояние и найти следы».

> [!danger] Критично для основной системы владельца (Gentoo/OpenRC) и роутера (Entware)
> Половина команд поста — **systemd-специфичны** (`journalctl`, `systemctl`). На **Gentoo с OpenRC их нет**, на **Entware (busybox) — тоже**. Ниже везде даю кросс-дистрибутивные варианты, а в конце — отдельная таблица различий. Путь `/var/log/auth.log` — это **Debian/Ubuntu**; на Gentoo/RHEL он другой или логов нет без настроенного syslog.

---

## 🔍 Разведка системы

```bash
uname -a                      # ядро, архитектура
cat /etc/os-release           # дистрибутив и версия
hostnamectl                   # хост/ОС (systemd); иначе: hostname; uname -a
id ; whoami                   # кто я и мои группы
ip a          # интерфейсы (совр.);  ifconfig — устарел (net-tools, часто не стоит)
ip route ; ip neigh           # маршруты и ARP-таблица (замена route -n / arp -a)
ss -tulpn                     # СЛУШАЮЩИЕ порты и чьи (совр. замена netstat)
lsblk ; df -h ; mount         # диски, разделы, точки монтирования
```

## 👤 Пользователи, права, эскалация

```bash
getent passwd                 # все пользователи (лучше, чем cat /etc/passwd — учитывает LDAP)
awk -F: '($3==0){print $1}' /etc/passwd   # 🚩 аккаунты с UID 0 (скрытый root!)
sudo -l                       # что МНЕ можно через sudo (точнее, чем cat /etc/sudoers)
cat /etc/sudoers /etc/sudoers.d/*         # полная картина sudo (нужен root)
sudo cat /etc/shadow          # хеши паролей (root); пустое 2-е поле = вход без пароля
find / -perm -4000 -type f 2>/dev/null    # SUID-бинарники → privesc (см. GTFOBins)
find / -perm -2000 -type f 2>/dev/null    # SGID-бинарники (пост забыл)
getcap -r / 2>/dev/null       # файловые capabilities (cap_setuid и т.п.) — тоже privesc
find / -writable -type f -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null  # записываемые (сузил шум)
```
SUID/SGID/caps сверять по [GTFOBins](../../Pentest/Linux/GTFOBins%20%E2%80%94%20%D1%81%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1%87%D0%BD%D0%B8%D0%BA%20Unix-%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B0%20%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B8%20privesc%20%28%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B7%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8C%D1%81%D1%8F%29.md): если бинарник там есть с shell-функцией — это дыра.

## ⚙️ Процессы и сеть

```bash
ps aux --sort=-%mem           # топ по памяти (busybox: просто ps -w или ps aux)
ps -ef --forest               # дерево процессов — видно «родителя» подозрительного
ss -tunap                     # все соединения с PID (быстрая замена netstat -antp)
ss -tp state established       # только установленные TCP
lsof -i -P -n                 # открытые сетевые сокеты (см. Linux/Commands/lsof)
lsof +L1                      # 🚩 удалённые, но открытые файлы (частый приём malware)
lsof -p <PID>                 # что держит открытым конкретный процесс
ls -la /proc/<PID>/exe /proc/<PID>/cwd    # реальный путь и рабочая папка процесса
cat /proc/<PID>/cmdline | tr '\0' ' '     # полная командная строка (даже если скрыта в ps)
```
> [!tip] Если инструменты подменены (rootkit)
> При подозрении на руткит `ps`/`ss`/`netstat` могут врать. Смотреть напрямую в ядро: `cat /proc/net/tcp` (порты в hex), листинг `/proc/[0-9]*` для процессов, сверять с выводом утилит.

## 📜 Логи и аудит

```bash
# systemd (Debian/Ubuntu/Arch):
journalctl -u sshd --since "1 hour ago"   # логи SSH (юнит: sshd; в Debian бывает ssh)
journalctl -p err -b                      # ошибки с текущей загрузки
journalctl -k                             # сообщения ядра (замена dmesg)

# файловые логи (Debian: auth.log; RHEL/др.: secure):
grep "Failed password" /var/log/auth.log 2>/dev/null || \
  grep "Failed password" /var/log/secure 2>/dev/null   # брутфорс SSH
grep -i "accepted" /var/log/auth.log      # успешные входы

last -20                      # последние входы (wtmp)
lastb -20                     # 🚩 НЕудачные входы (btmp) — пост забыл, а это про брутфорс
lastlog                       # последний вход каждого пользователя
who ; w                       # кто сейчас в системе и что делает
ausearch -m USER_LOGIN ; aureport --auth   # если стоит auditd
```

## 🕵️ Персистентность — где закрепляются (раздела в посте не было)

```bash
crontab -l ; sudo crontab -l -u root       # cron текущего/root
ls -la /etc/cron* /var/spool/cron/*        # системный cron, задания
systemctl list-timers --all                # systemd-таймеры (аналог cron)
systemctl list-unit-files --state=enabled  # что стартует само (systemd)
ls -la ~/.ssh/authorized_keys /root/.ssh/authorized_keys  # 🚩 подсаженные SSH-ключи
cat ~/.bashrc ~/.bash_profile /etc/profile.d/*  # автозапуск при входе
cat /etc/rc.local /etc/ld.so.preload 2>/dev/null # rc.local, LD_PRELOAD-руткит
lsmod ; cat /etc/modules-load.d/*          # загруженные модули ядра
env | grep -Ei 'LD_PRELOAD|LD_LIBRARY_PATH' # подмена библиотек
alias                                       # вредоносные алиасы в шелле
```

## 🧬 Поиск, анализ файлов, IOC

```bash
grep -rniI "password" /etc/ 2>/dev/null     # пароли в конфигах (-I пропускает бинарники)
file suspicious_file                        # что за файл (см. TrID для экзотики)
strings -n 8 file.bin | grep -Ei 'http|/bin/|[0-9]{1,3}(\.[0-9]{1,3}){3}'  # URL/IP/пути
sha256sum file                              # хеш для VirusTotal
find / -newermt "2026-09-27 00:00" -type f -not -path "/proc/*" 2>/dev/null # 🚩 таймлайн: что менялось с даты
find /tmp /dev/shm /var/tmp -type f -executable 2>/dev/null  # исполняемое во временных папках
find / -name ".*" -type f 2>/dev/null | grep -v -E '/home/|/root/'  # скрытые файлы вне домашних
stat file                                   # метки времени MAC (atime/mtime/ctime)
lsattr file                                 # флаг immutable (i) — часто у спрятанного
```

## 🔒 Проверка целостности пакетов (не был в посте — а зря)

Подменённый системный бинарник — классика. Штатные средства пакетного менеджера:

```bash
# Debian/Ubuntu:
debsums -c                         # изменённые файлы пакетов (нужен пакет debsums)
dpkg -V                            # то же средствами dpkg
# Arch:
paccheck --md5 ; pacman -Qkk       # проверка файлов пакетов
# Gentoo:
equery check <пакет>               # (app-portage/gentoolkit) сверка контрольных сумм
qcheck                             # (app-portage/portage-utils) быстрее
# RHEL-подобные:
rpm -Va                            # все изменения относительно RPM-базы
```

---

## 🧭 Различия по системам владельца (важное)

| Задача | systemd (Debian/Ubuntu, Arch) | **Gentoo (OpenRC)** | **Entware (busybox)** |
| :--- | :--- | :--- | :--- |
| Логи | `journalctl …` | ❌ нет journalctl. Логи syslog: `/var/log/messages`, `/var/log/auth.log` (если настроен syslog-ng/rsyslog); ядро — `dmesg` | `logread` (busybox syslogd), если запущен; иначе логов нет |
| Службы | `systemctl status/list-units` | `rc-status`, `rc-service <s> status`, `rc-update show` | `/opt/etc/init.d/S*` , `ls /opt/etc/init.d/` |
| Автозапуск | `systemctl list-unit-files --state=enabled`, `list-timers` | `rc-update show`, cron | init.d-скрипты `/opt/etc/init.d/`, cron busybox |
| ps/ss | полные GNU-версии | полные GNU-версии | **урезанный busybox**: `ps aux --sort` не работает (просто `ps`), `ss`/`lsof` может не быть → `netstat -tulpn` (busybox) |
| find | GNU find | GNU find | busybox find: нет `-newermt`, часть флагов урезана |
| Аудит логинов | `last/lastb/lastlog` | то же (sys-apps/shadow, util-linux) | часто отсутствуют (нет wtmp/btmp) |

> [!note] Практика для роутера RT-AX56U
> На стоковой прошивке + Entware для триажа реально доступны: `ps`, `netstat -tulpn`, `logread`, `cat /proc/*`, `crontab -l`, просмотр `/opt/etc/init.d/`. Тяжёлых DFIR-инструментов там нет — базовый осмотр делается «руками» через `/proc` и busybox-утилиты.

---

## ⚡ Мини-плейбук «пришёл на подозрительную машину»

1. **Кто и откуда:** `w`, `last -20`, `lastb -20`, `ss -tunap`.
2. **Что запущено:** `ps -ef --forest`, `ss -tulpn`, `lsof +L1`.
3. **Персистентность:** cron, автозапуск служб, `authorized_keys`, `ld.so.preload`, `~/.bashrc`.
4. **Свежие изменения:** `find / -newermt "<дата инцидента>"`, `/tmp` и `/dev/shm`.
5. **Эскалация:** SUID/SGID/caps → сверка с GTFOBins; UID 0 в passwd.
6. **Целостность:** проверка пакетов (`debsums`/`equery check`/`rpm -Va`).
7. **Фиксация:** хеши подозрительных файлов (`sha256sum`) → VirusTotal, `file`/TrID для неизвестных.

> [!warning] Право и осторожность
> Команды **read-only** и безопасны для аудита своей системы. При реальном разборе инцидента помни: обращение к файлу меняет `atime`, а активные действия могут затереть следы — на «боевом» кейсе сначала снимают образ диска/памяти. Аудит чужих систем — только с авторизацией (ст. 272 УК РФ).

## 🔗 Связанные заметки

- SUID/sudo/capabilities → эксплуатация и защита: [GTFOBins](../../Pentest/Linux/GTFOBins%20%E2%80%94%20%D1%81%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%D1%87%D0%BD%D0%B8%D0%BA%20Unix-%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%D0%B0%20%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B8%20privesc%20%28%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B7%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8C%D1%81%D1%8F%29.md)
- Открытые файлы/сокеты подробно: [lsof](../../Linux/Commands/lsof.md)
- Определить тип неизвестного файла/образца: [TrID](TrID%20%28Marco%20Pontello%29%20%E2%80%94%20%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%B8%D0%BF%D0%B0%20%D1%84%D0%B0%D0%B9%D0%BB%D0%B0%20%D0%BF%D0%BE%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D0%BE%D0%B9%20%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B5%20%28freeware%2C%2022k%20%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%BE%D0%B2%29.md)

## 🔗 Ссылки

- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Security #Forensics #DFIR #Linux #BlueTeam #Шпаргалка
