---
создал заметку: 2026-10-18T14:00:00
author: WhiteK0T
tags:
  - Network
  - NTP
  - chrony
  - Linux
  - Gentoo
  - OpenRC
Источник:
  - https://chrony-project.org/
  - https://chrony-project.org/doc/4.9/chrony.conf.html
  - https://chrony-project.org/comparison.html
  - https://wiki.gentoo.org/wiki/Chrony
  - https://wiki.gentoo.org/wiki/Network_Time_Protocol
  - https://wiki.archlinux.org/title/Chrony
  - https://bugs.gentoo.org/962880
---

# ⏱️ chrony — синхронизация времени

**chrony** — реализация протокола **NTP** (Network Time Protocol): клиент, который держит системные часы точными по серверам времени, и одновременно сервер, раздающий время другим машинам. Работает в Linux, FreeBSD, NetBSD, macOS, Solaris, а с версии 4.9 — и в OpenBSD. Лицензия GPL-2.0.

Состоит из двух программ:

| Программа | Что делает |
| :--- | :--- |
| **`chronyd`** | демон: опрашивает источники времени, подстраивает часы ядра, при желании раздаёт время |
| **`chronyc`** | консоль управления и мониторинга: состояние, источники, ручная коррекция |

| | |
| :--- | :--- |
| Последний выпуск | **4.9** (27.08.2026) |
| В дистрибутивах | Gentoo: 4.8 стабильная, 4.9 в `~amd64` · Debian 13: 4.6.1 · Arch: 4.9 · Entware: 4.8 |
| По умолчанию | RHEL/Fedora, SUSE, Ubuntu Server (с 25.10 — с NTS), Debian предлагает как замену `systemd-timesyncd`/`ntp` |

---

## 1. Почему именно сейчас: `net-misc/ntp` уходит из Gentoo

При `emerge` на Gentoo с октября 2026 появляется предупреждение:

```
!!! The following installed packages are masked:
- net-misc/ntp-4.2.8_p18-r3::gentoo (masked by: package.mask)
# Unmaintained, abandoned by maintainer.
# You can look at net-misc/ntpsec or net-misc/chrony as replacement.
# Removal on 2027-01-04. Bug #962880, and many more.
```

Что за этим стоит:

- **Классический ntpd** (эталонная реализация ntp.org, пакет `net-misc/ntp`) почти не развивается: последний выпуск **4.2.8p18 — 2024 год**, новых нет.
- В Gentoo пакет **остался без мейнтейнера** и оброс багами: не собирается на GCC 15 без правок, тесты падают с OpenSSL 3.4+, `ntpd` «запускается и зависает» (#965690), `ntp-client` при загрузке не может разрешить имена (#930071) — всего около двадцати открытых багов.
- Тикет на удаление (**#962880**) открыт ещё в сентябре 2025; маска появилась 06.10.2026, когда замены (`chrony`, `ntpsec`) получили ключевые слова на тех же архитектурах.
- **Удаление из дерева — 04.01.2027.** Установленный пакет продолжит работать, но обновлений и исправлений безопасности больше не будет, а с новыми GCC и OpenSSL его не пересобрать.

Предупреждение появляется, даже если служба `ntpd` не запущена: достаточно, что пакет есть в `@world`. Перед заменой стоит проверить, синхронизирует ли что-то время вообще:

```bash
rc-update show | grep -E 'ntp|chrony'   # Gentoo/OpenRC: какие службы времени в автозагрузке
sntp pool.ntp.org                        # разовая проверка смещения (из пакета ntp), без изменения часов
```

Бывает, что `ntp` стоит, а ни `ntpd`, ни `ntp-client` не добавлены в автозагрузку. Тогда часы держатся только за счёт гипервизора (`kvm-clock` на VPS), и после долгой работы или миграции ВМ их некому поправить.

**Чем заменить** — Gentoo предлагает два пакета:

| | chrony | ntpsec |
| :--- | :--- | :--- |
| Что это | независимая реализация (Red Hat, Miroslav Lichvar) | форк ntp.org с вычищенным кодом |
| Конфигурация | свой `chrony.conf` | **тот же `ntp.conf`**, `ntpq` |
| Когда брать | **почти всегда**: сервер, VPS, ноутбук, роутер | нужна совместимость с конфигами старого ntp или экзотические эталонные часы |

Переход на chrony на Gentoo — в разделе 3.

---

## 2. Чем chrony лучше старого ntpd

- **Быстро сходится**: при старте с `iburst` выходит на точное время за секунды, а не за десятки минут.
- **Терпим к плохим условиям**: прерывистая сеть, ноутбук, засыпание, ВМ с плавающей частотой процессора, сильно сбитые часы.
- **Один демон вместо двух**: заменяет и `ntpd` (постоянная подстройка), и `ntpdate` (разовая установка: `chronyd -q`).
- **NTS** (Network Time Security, RFC 8915) — защищённый NTP: ответы сервера подписаны, подменить время по пути нельзя. В старом ntp NTS нет.
- **Аппаратные метки времени** на сетевых картах — точность до десятков наносекунд в локальной сети.
- **Эталонные часы**: GPS через PPS, PTP-часы сетевой карты (PHC), часы гипервизора (`ptp_kvm`), RTC, SHM от `gpsd`.
- **Безопасность по умолчанию**: работает от непривилегированного пользователя, фильтр seccomp, сервер раздаёт время только тем, кому явно разрешено (`allow`).
- **Без раздачи времени по сети** порт 123 можно не открывать вовсе (`port 0`).

| | chrony | ntpd (ntp.org) | ntpsec | systemd-timesyncd | OpenNTPD |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Клиент | ✅ | ✅ | ✅ | ✅ (только SNTP) | ✅ |
| Сервер для LAN | ✅ | ✅ | ✅ | ❌ | ✅ |
| NTS | ✅ | ❌ | ✅ | ❌ | ❌ |
| Аппаратные метки, PTP/PHC | ✅ | частично | частично | ❌ | ❌ |
| Быстрый старт, нестабильная сеть | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ |
| Работает с OpenRC | ✅ | ✅ | ✅ | ❌ (часть systemd) | ✅ |
| Развивается | ✅ | ❌ (2024) | ✅ | ✅ | медленно |

---

## 3. Установка

### Gentoo (OpenRC) — с переходом с ntp

```bash
# 1. Убрать старый ntp
emerge --ask --deselect net-misc/ntp           # из @world
rc-update del ntpd default 2>/dev/null; rc-update del ntp-client default 2>/dev/null
rc-service ntpd stop 2>/dev/null

# 2. Поставить chrony
emerge --ask net-misc/chrony

# 3. Удалить ntp
emerge --ask --depclean net-misc/ntp

# 4. Запустить
rc-update add chronyd default
rc-service chronyd start
chronyc tracking
```

| USE-флаг | Зачем | По умолчанию |
| :--- | :--- | :---: |
| `nts` | Network Time Security (через `net-libs/gnutls`) | ✅ |
| `cmdmon` | управление через `chronyc` | ✅ |
| `caps` | работа от пользователя `ntp` с минимумом прав (libcap) | ✅ |
| `seccomp` | фильтр системных вызовов | ✅ |
| `nettle` / `nss` / `libtomcrypt` | криптобиблиотека для ключей и NTS | `nettle` |
| `sechash` | хэши кроме MD5 для симметричных ключей | ✅ |
| `phc`, `pps`, `refclock`, `rtc` | эталонные часы: PTP-часы, PPS-сигнал GPS, RTC | ✅ |
| `readline` | история и редактирование в `chronyc` | ✅ |
| `samba` | подпись времени для клиентов Active Directory (Samba) | — |

Особенности Gentoo:
- конфигурация — **`/etc/chrony/chrony.conf`** (плюс ссылка `/etc/chrony.conf` для совместимости); по умолчанию — пул `2.gentoo.pool.ntp.org` (единственная зона Gentoo-пула с IPv6);
- параметры запуска — **`/etc/conf.d/chronyd`**: `ARGS=" -u ntp -F 2"` (`-F 2` — базовый уровень seccomp-фильтра; при проблемах можно `-F 1` или `-F -1`, см. `man chronyd`);
- если в конфиге есть `rtcfile`, init-скрипт добавит `-s` (взять время из RTC при старте), если `dumponexit` — `-r` (подхватить сохранённую статистику).

### Debian / Ubuntu

```bash
sudo apt install chrony        # сам удалит systemd-timesyncd, ntp/ntpsec конфликтуют
systemctl status chrony        # служба называется chrony (не chronyd)
```

Конфигурация — `/etc/chrony/chrony.conf`, а свои источники удобно класть в **`/etc/chrony/sources.d/*.sources`** и настройки в `/etc/chrony/conf.d/*.conf` (подхватываются `sourcedir`/`confdir`); после правки источников — `chronyc reload sources`. В Debian 12+ пакет `ntp` — уже лишь переходной на `ntpsec`.

### Arch

```bash
sudo pacman -S chrony
sudo systemctl disable --now systemd-timesyncd   # два демона времени одновременно — плохо
sudo systemctl enable --now chronyd
```

Конфигурация — `/etc/chrony.conf`. Есть `chrony-wait.service` — если службам нужно дождаться точного времени на загрузке.

### Entware (ASUS RT-AX56U)

```bash
opkg install chrony-nts        # или chrony — без NTS, без gnutls (~300 КБ)
# конфиг: /opt/etc/chrony/chrony.conf (из примеров /opt/etc/chrony/chrony.conf.example*)
/opt/etc/init.d/S06chronyd start
```

На роутере время **уже синхронизирует прошивка** ASUS (её NTP-клиент, а в Asuswrt-Merlin — и NTP-сервер для LAN). Chrony из Entware имеет смысл, только если нужен NTS или полноценный NTP-сервер для домашней сети; тогда встроенный сервер прошивки нужно выключить, чтобы не было двух служб на порту 123. Для простой синхронизации самого роутера Entware не нужен.

---

## 4. Конфигурация `chrony.conf`

### Минимальный клиент (рабочая станция, VPS)

```conf
# Источники: пул из нескольких серверов; iburst — быстрая первая синхронизация
pool 2.gentoo.pool.ntp.org iburst      # Debian: 2.debian.pool.ntp.org; везде подойдёт pool.ntp.org или региональный пул

# Запоминать уход частоты часов между перезапусками
driftfile /var/lib/chrony/drift

# При расхождении больше 1 с — шагнуть сразу (первые 3 обновления), иначе плавно подгонять
makestep 1.0 3

# Раз в 11 минут копировать системное время в аппаратные часы (RTC)
rtcsync

# Таблица дополнительных секунд из tzdata
leapsectz right/UTC

logdir /var/log/chrony
```

| Директива | Смысл |
| :--- | :--- |
| `server <хост> iburst` | конкретный сервер |
| `pool <имя> iburst maxsources 4` | имя пула → несколько серверов (по умолчанию до 4) |
| `minsources 2` | менять часы, только когда согласны хотя бы 2 источника |
| `makestep <порог> <сколько>` | когда можно **шагнуть** временем, а не плавно подгонять. `makestep 1 -1` — шагать всегда при расхождении > 1 с (удобно для ВМ после паузы и миграции) |
| `maxupdateskew`, `maxdistance` | отбраковка нестабильных источников |
| `rtcsync` | ядро само периодически пишет время в RTC |
| `driftfile` | файл с вычисленной ошибкой частоты |
| `dumpdir` + `dumponexit` | сохранять статистику источников между перезапусками |
| `sourcedir` / `confdir` | подключать фрагменты из каталогов |

**Плавная подгонка vs шаг.** По умолчанию chrony меняет время **плавно** (ускоряет или замедляет часы, до 83 мс в секунду), чтобы время в программах не прыгало назад. Шаг (`makestep`) нужен, только когда часы сбиты сильно.

### NTS — защищённое время

```conf
server time.cloudflare.com iburst nts
server nts.netnod.se iburst nts
server ptbtime1.ptb.de iburst nts
ntsdumpdir /var/lib/chrony            # кэш ключей NTS — быстрый старт после перезагрузки
```

Проверка: `chronyc -N authdata` — для NTS-источников колонка `Mode` = `NTS`, `KeyID`/`Cook` не нули. NTS использует TCP 4460 для обмена ключами и UDP 123 для времени. Важно: NTS проверяет TLS-сертификат, а для этого часы должны быть хотя бы примерно верны — при сильно сбитых часах первый запуск может не пройти (на этот случай есть опция `nocerttimecheck`).

### Сервер времени для локальной сети

```conf
pool 2.gentoo.pool.ntp.org iburst
allow 192.168.0.0/16                  # кому разрешено спрашивать время (по умолчанию — никому)
# allow                               # без аргумента — всем (не делайте этого на машине с публичным IP)
local stratum 10 orphan               # продолжать раздавать время, если интернет пропал
ratelimit interval 1 burst 16         # защита от флуда запросами
```

Клиенты в LAN указывают этот сервер: `server <адрес-сервера> iburst`. В фаерволе — UDP 123 только из локальной сети.

### Только клиент, без открытых портов

```conf
port 0          # не открывать порт сервера NTP (123)
cmdport 0       # не слушать UDP для chronyc; chronyc работает через Unix-сокет
```

### Виртуальная машина: точное время от хоста (KVM)

На KVM-гостях есть виртуальные PTP-часы хоста — модуль ядра `ptp_kvm` создаёт `/dev/ptp0` (опция ядра `CONFIG_PTP_1588_CLOCK_KVM`):

```bash
modprobe ptp_kvm && ls /dev/ptp*
```

```conf
refclock PHC /dev/ptp0 poll 2 dpoll -2 offset 0 stratum 2
pool 2.gentoo.pool.ntp.org iburst     # сетевые источники как резерв и проверка
makestep 1 -1
```

Так гость берёт время прямо у гипервизора без сети. Работает, только если хост сам синхронизирован и провайдер не отключил эту возможность; на «чужом» VPS это стоит проверить `chronyc sources`.

### Другие эталонные часы

```conf
refclock SHM 0 refid GPS precision 1e-1 offset 0.2 delay 0.2   # грубое время от gpsd
refclock PPS /dev/pps0 lock GPS refid PPS                     # точный секундный импульс GPS
refclock PHC /dev/ptp0 tai                                    # PTP-часы сетевой карты
hwtimestamp *                                                 # аппаратные метки на всех интерфейсах
```

---

## 5. `chronyc` — мониторинг и управление

```bash
chronyc tracking          # главное: смещение, частота, stratum, источник
chronyc sources -v        # источники и их состояние (с расшифровкой колонок)
chronyc sourcestats -v    # статистика по каждому источнику
chronyc activity          # сколько источников онлайн
chronyc -N authdata       # NTS/ключи по источникам
chronyc clients           # кто спрашивает время (если работает сервером)
chronyc serverstats       # счётчики запросов сервера
chronyc ntpdata           # подробности последнего NTP-обмена

chronyc makestep          # шагнуть временем прямо сейчас (root)
chronyc burst 4/4         # быстро опросить источники
chronyc offline / online  # отметить источники (ноутбук без сети)
chronyc reload sources    # перечитать sourcedir
chronyc waitsync 30 0.01  # ждать синхронизации (для скриптов)
```

Как читать `chronyc sources`:

```
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^* time.example.org              2   6   377    34   +215us[ +301us] +/-   12ms
^+ ntp2.example.org              2   6   377    35   -1083us[-997us] +/-   25ms
^- ntp3.example.org              3   6   377    33   +4123us[+4209us] +/-   48ms
```

| Знак | Значение |
| :---: | :--- |
| `^` / `#` | сетевой сервер / эталонные часы |
| `*` | **выбранный** источник |
| `+` | хороший, участвует в усреднении |
| `-` | исправный, но не используется |
| `?` | связь потеряна или мало данных |
| `x` | «лжец» — расходится с остальными |
| `~` | слишком нестабильный |

`Reach 377` (восьмеричное) — последние 8 опросов успешны. `tracking` → `System time` — насколько часы сейчас отличаются от правильного времени; `Leap status: Normal` — всё в порядке.

### Разовая синхронизация вместо `ntpdate`

```bash
chronyd -q 'server pool.ntp.org iburst'   # установить время и выйти (демон должен быть остановлен)
chronyd -Q 'server pool.ntp.org iburst'   # только показать смещение, ничего не меняя
```

---

## 6. Частые проблемы

| Симптом | Причина и решение |
| :--- | :--- |
| `chronyc: 506 Cannot talk to daemon` | `chronyd` не запущен, либо `chronyc` запущен не от root/не из группы с доступом к сокету |
| Все источники `?` | закрыт исходящий UDP 123 или нет DNS — проверить фаервол и `resolv.conf` |
| Время не догоняет после долгого простоя ВМ | нужен `makestep 1 -1` или `chronyc makestep` |
| На Arch/Debian два демона дерутся за часы | отключить `systemd-timesyncd` (Debian при установке chrony убирает его сам) |
| NTS не поднимается | закрыт TCP 4460 или часы так сбиты, что сертификат «ещё/уже недействителен» — сначала `chronyd -q` без NTS |
| На Gentoo демон падает на старте после обновления ядра или glibc | проблема seccomp-фильтра: временно `-F -1` в `/etc/conf.d/chronyd` и баг-репорт |
| Часы ВМ «уплывают», хотя chrony запущен | слишком редкие опросы при нестабильной частоте — добавить `refclock PHC /dev/ptp0` (KVM) или `maxpoll 6` |

## 🔗 Ссылки

- Проект и документация: https://chrony-project.org/ · [chrony.conf](https://chrony-project.org/doc/4.9/chrony.conf.html) · [chronyc](https://chrony-project.org/doc/4.9/chronyc.html)
- Сравнение с ntpd и другими: https://chrony-project.org/comparison.html
- Gentoo Wiki: https://wiki.gentoo.org/wiki/Chrony · https://wiki.gentoo.org/wiki/Network_Time_Protocol
- ArchWiki: https://wiki.archlinux.org/title/Chrony
- Удаление `net-misc/ntp` в Gentoo: https://bugs.gentoo.org/962880
- Публичные NTS-серверы: https://github.com/jauderho/nts-servers

#Network #NTP #chrony #Linux #Gentoo #OpenRC
