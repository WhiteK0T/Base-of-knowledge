---
создал заметку: 2026-10-18T16:00:00
author: WhiteK0T
tags:
  - Network
  - NTP
  - ntpsec
  - Linux
  - Gentoo
  - OpenRC
Источник:
  - https://www.ntpsec.org/
  - https://docs.ntpsec.org/latest/ntpsec.html
  - https://docs.ntpsec.org/latest/NTS-QuickStart.html
  - https://gitlab.com/NTPsec/ntpsec
  - https://wiki.gentoo.org/wiki/Network_Time_Protocol
  - https://bugs.gentoo.org/962880
---

# 🛡️ ntpsec — защищённый форк классического ntpd

**NTPsec** — форк эталонного NTP из ntp.org («NTP Classic»), начатый в 2015 году ради безопасности. Из исходного кода выброшено **более 74%**: устаревшие платформы, небезопасные режимы, лишние утилиты. Новый код в критичном ядре — менее 5%. При этом формат `ntp.conf`, протокол и утилита `ntpq` остались почти теми же, так что ntpsec — **прямая замена старого ntpd** с минимальными правками конфигов.

| | |
| :--- | :--- |
| Лицензия | свободная, смешанная: в основном BSD-2-Clause и NTP License (список — каталог `LICENSES/`) |
| Последний выпуск | **1.2.5** (30.07.2026); 1.2.4 — 18.04.2025 |
| Стек | C (демон `ntpd`) + Python (клиентские утилиты), сборка через waf, OpenSSL |
| В дистрибутивах | Gentoo: 1.2.5 (amd64 стабильная), Debian 13: 1.2.3, Debian sid: 1.2.5, Arch: только AUR, Entware: нет |
| Сайт и репозиторий | https://www.ntpsec.org/ · https://gitlab.com/NTPsec/ntpsec |

---

## 1. Контекст: почему встал вопрос замены `net-misc/ntp`

С 06.10.2026 Gentoo маскирует `net-misc/ntp` и **удаляет его 04.01.2027** (bug #962880): пакет остался без мейнтейнера, а ntp.org не выпускал новых версий с 4.2.8p18 (2024). Подробно — в заметке [chrony](chrony%20%E2%80%94%20%D1%81%D0%B8%D0%BD%D1%85%D1%80%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B8%20%28NTP-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%2C%20NTS%2C%20PTP-PHC%2C%20chronyc%29%2C%20%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B0%20ntp%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20Entware.md). В маске Gentoo предлагает две замены — **chrony** и **ntpsec**. Debian пошёл тем же путём ещё раньше: с Debian 12 пакет `ntp` — лишь переходной на `ntpsec`.

### chrony или ntpsec

| | **ntpsec** | **chrony** |
| :--- | :--- | :--- |
| Кому ближе | тем, у кого **годами настроенный `ntp.conf`**, скрипты на `ntpq -p`, мониторинг ntpd | новые установки, ноутбуки, VPS |
| Конфигурация | формат ntp.org (`server`, `pool`, `restrict`, `driftfile`…) | свой `chrony.conf` |
| NTS | ✅ клиент и сервер | ✅ клиент и сервер |
| Эталонные часы | **богатый набор драйверов** (GPS NMEA, gpsd, PPS, Trimble, Spectracom, JJY, HP GPS, модемные службы NIST/PTB…) | PPS, PHC/PTP, SHM, gpsd, RTC |
| PTP-часы ВМ (`ptp_kvm`), аппаратные метки | ❌ | ✅ |
| Быстрый старт, сон, нестабильная сеть | ⚠️ как у классического ntpd | ✅ лучше |
| Анализ и графики | **`ntpviz`**, `ntpmon`, подробная статистика | `chronyc`, логи |
| Зависимости | Python + OpenSSL | C, без Python |

**Коротко:** для «просто точного времени» на рабочей машине или VPS проще и лучше chrony. ntpsec выбирают, когда важна **совместимость с классическим ntpd** (конфиги, `ntpq`, мониторинг), нужен **серьёзный сервер времени** со статистикой и графиками или **экзотический драйвер эталонных часов**.

---

## 2. Что изменилось по сравнению с классическим ntpd

### Убрано ради безопасности

| Что | Почему |
| :--- | :--- |
| **`ntpdc`** и протокол Mode 7 | постоянный источник уязвимостей; функции перенесены в `ntpq` |
| **Autokey** (RFC 5906) | несовместим и уязвим; замена — **NTS** |
| **broadcast / multicast / anycast** | невозможно защитить |
| **режим `peer`** | слово `peer` в `ntp.conf` теперь просто синоним `server` |
| **interleave mode** | был с ошибкой и причиной минимум двух CVE |
| **`ntpdate`** | заменён обёрткой над `ntpdig` (опции `-e` и `-p` не поддерживаются) |
| `ntpsnmpd`, `trap`, `saveconfig`, `ntpdsim` | недоделанное или опасное |
| много устаревших драйверов эталонных часов | меньше кода — меньше атак |
| отключение аутентификации для удалённой настройки через `ntpq` | больше нельзя выключить |

### Переименовано

| NTP Classic | ntpsec |
| :--- | :--- |
| `sntp` | **`ntpdig`** |
| `ntp-keygen` | `ntpkeygen` |
| `ntp-wait` | `ntpwait` |
| `update-leap` | `ntpleapfetch` |
| `tickadj` | часть **`ntpfrob`** |
| `/dev/palisadeN`, `/dev/actsN` | `/dev/trimbleN`, `/dev/modemN` |

Также: метки времени в логах — в формате ISO 8601; часы в статистике называются по имени драйвера, а не «магическими» адресами `127.127.t.u`; `--help` теперь `-h`. Часть изменений можно вернуть сборкой с `--enable-classic-mode`.

### Добавлено

- **NTS** — защищённое время (RFC 8915) и как клиент, и как сервер.
- **Минимизация данных клиента** — по черновику IETF, чтобы клиента нельзя было «опознать» по полям пакета.
- **`ntpmon`** — монитор в реальном времени (как `top` для NTP).
- **`ntpviz`** — графики смещения, джиттера, температуры и т.д. из статистики ntpd (HTML и картинки, с 1.2.5 — `.webp`).
- **`ntploggps`, `ntplogtemp`** — запись данных GPS и температуры для анализа.
- Наносекундная точность внутри, фиксы выбора источников, унаследованные от Classic.
- 1.2.5: `pool <имя> nts`, отдельный журнал `ntskelog`, сильный генератор случайных чисел, исправления CVE-2026-18321 (драйвер Zyfer) и ряда ошибок NTS.

---

## 3. Установка

### Gentoo (OpenRC) — с переходом с ntp

```bash
# 1. Убрать старый ntp (ntpsec его блокирует — вместе не ставятся)
rc-service ntpd stop 2>/dev/null; rc-update del ntpd default 2>/dev/null; rc-update del ntp-client default 2>/dev/null
emerge --ask --deselect net-misc/ntp
emerge --ask --depclean net-misc/ntp

# 2. Поставить ntpsec
emerge --ask net-misc/ntpsec

# 3. Запустить — служба называется ntp (не ntpd!)
rc-update add ntp default
rc-service ntp start
ntpq -p
```

| USE-флаг | Зачем |
| :--- | :--- |
| драйверы часов: `gpsd`, `nmea`, `pps`, `shm`, `trimble`, `spectracom`, `jjy`, `hpgps`, `oncore`, `zyfer`, `arbiter`, `truetime`, `generic`, `modem`, `local` | какие драйверы эталонных часов собрать; **по умолчанию не включены** — для синхронизации по сети не нужны |
| `nist` | службы времени NIST/USNO/PTB по модему (требует `local`) |
| `seccomp` | фильтр системных вызовов |
| `early` | сбрасывать права root как можно раньше |
| `samba` | подпись времени для клиентов Active Directory (MS-SNTP) |
| `smear` | «размазывание» дополнительной секунды (экспериментально) |
| `ntpviz` | графики (тянет зависимости для построения) |
| `doc`, `heat`, `libbsd`, `debug` | документация, скрипты нагрева CPU для стабилизации частоты, libbsd, отладка |

Файлы на Gentoo:

| Путь | Что |
| :--- | :--- |
| `/etc/ntp.conf` | главный конфиг (по умолчанию — 4 зоны `gentoo.pool.ntp.org` и `restrict`) |
| `/etc/ntp.d/` | готовые фрагменты для `includefile` (см. ниже) |
| `/etc/conf.d/ntp` | `NTPD_OPTS="-g -u ntp:ntp"`: `-g` разрешает большой первый шаг времени, `-u` — работа от пользователя `ntp` |
| `/var/lib/ntp/ntp.drift` | файл дрейфа частоты |
| `/var/log/ntpstats/` | статистика для `ntpviz` |

Если на машине уже работает **chrony** — две службы времени одновременно запускать нельзя: остановите одну (`rc-service chronyd stop && rc-update del chronyd default`).

### Debian / Ubuntu

```bash
sudo apt install ntpsec              # служба ntpsec.service, конфиг /etc/ntpsec/ntp.conf
sudo apt install ntpsec-ntpdate      # если нужна обёртка ntpdate
systemctl status ntpsec
```

Пакет конфликтует с `chrony` и `systemd-timesyncd`. В Debian 13 — версия 1.2.3 (без исправлений 1.2.5), свежая — в sid.

### Arch

Только в **AUR**: `yay -S ntpsec` (или `paru`). Перед запуском — `sudo systemctl disable --now systemd-timesyncd`, затем включить службу из пакета (имя — `systemctl list-unit-files | grep -i ntp`). Пакет `ntp` (классический) в Arch пока в `extra`, но перспектива у него та же, что и в Gentoo.

### Entware

Пакета **нет**. На роутере время синхронизирует прошивка; если нужен NTS или свой сервер для LAN — `chrony-nts` из Entware (см. заметку про chrony).

---

## 4. Конфигурация `ntp.conf`

### Клиент

```conf
pool 2.gentoo.pool.ntp.org iburst
tos maxclock 5                         # сколько серверов брать из пула

driftfile /var/lib/ntp/ntp.drift
leapfile /usr/share/zoneinfo/leap-seconds.list   # таблица дополнительных секунд

# Никто снаружи не может настраивать или опрашивать демон
restrict default kod limited nomodify noquery
restrict -6 default kod limited nomodify noquery
restrict 127.0.0.1
restrict -6 ::1
```

| Директива | Смысл |
| :--- | :--- |
| `server <хост> iburst` / `pool <имя> iburst` | источник / пул; `iburst` — быстрая первая синхронизация |
| `prefer`, `noselect` | предпочесть источник / только наблюдать |
| `minpoll`, `maxpoll` | интервал опроса (степени двойки, секунды) |
| `restrict` | доступ: `kod` (просьба притормозить), `limited` (ограничение частоты), `nomodify` (без настройки), `noquery` (без запросов `ntpq`), `nopeer` |
| `tos maxclock`, `tos minsane` | сколько источников держать и сколько должны согласиться |
| `includefile` | подключить фрагмент |
| `statistics`, `filegen`, `statsdir` | сбор статистики для `ntpviz` |

### Готовые фрагменты из `/etc/ntp.d/`

```conf
includefile /etc/ntp.d/use-pool                    # pool pool.ntp.org iburst + tos maxclock 5
includefile /etc/ntp.d/use-no-remote-configuration # restrict: обычная защита
includefile /etc/ntp.d/use-minimal-logging         # только driftfile
# includefile /etc/ntp.d/use-performance-logging   # loopstats/peerstats/clockstats для ntpviz
# includefile /etc/ntp.d/use-gpsd-json             # GPS через gpsd (JSON)
# includefile /etc/ntp.d/use-gpsd-shm              # GPS + PPS через разделяемую память gpsd
```

### NTS — защищённое время (клиент)

```conf
server time.cloudflare.com iburst nts
server nts.netnod.se iburst nts
server ptbtime1.ptb.de iburst nts
pool   ntppool.example nts        # с 1.2.5 — nts и для pool (если пул поддерживает NTS)
```

Проверка — в логе должна быть строка вида `NTSc: Got 7 cookies, length 100, aead=15` и `NTS-KE req … OK`, а в `ntpq -p` сервер достижим. NTS-KE идёт по **TCP 4460**, время — по UDP 123.

### Сервер времени для LAN

```conf
pool 2.gentoo.pool.ntp.org iburst
driftfile /var/lib/ntp/ntp.drift

restrict default kod limited nomodify noquery nopeer
restrict 192.168.0.0 mask 255.255.0.0 kod limited nomodify noquery   # клиенты LAN
restrict 127.0.0.1
restrict -6 ::1
```

### NTS-сервер

```conf
nts enable
nts key  /etc/letsencrypt/live/ntp.example.com/privkey.pem
nts cert /etc/letsencrypt/live/ntp.example.com/fullchain.pem
nts cookie /var/lib/ntp/nts-keys      # ключи для cookies переживают перезапуск
```

Нужен действующий TLS-сертификат на имя сервера (подойдёт Let's Encrypt), открытый **TCP 4460** и UDP 123. Пользователь `ntp` должен иметь право читать ключ.

---

## 5. Утилиты

```bash
ntpq -p                 # источники (как раньше)
ntpq -c rv              # системные переменные: смещение, stratum, leap
ntpq -c sysinfo         # сводка, включая root distance
ntpq -c mrulist         # кто обращался к серверу
ntpmon                  # монитор в реальном времени (q — выход)
ntpdig pool.ntp.org     # разовый запрос смещения (бывший sntp); ничего не меняет
ntpdig -s pool.ntp.org  # подправить часы плавно (slew, root); -S — шагом (step)
ntpwait -v              # дождаться синхронизации (для скриптов загрузки)
ntpleapfetch            # обновить таблицу дополнительных секунд
ntpfrob -A              # показать переменную ядра tick (бывший tickadj)
ntpviz -o /var/www/html/ntp   # HTML-отчёт с графиками по /var/log/ntpstats
```

Как читать `ntpq -p`:

```
     remote                       refid      st t when poll reach   delay   offset   jitter
=========================================================================================
*time.example.org                .GPS.        1 u   34   64  377   9.812   +0.215    0.081
+ntp2.example.org                10.0.0.1     2 u   35   64  377  12.004   -1.083    0.244
-ntp3.example.org                192.0.2.5    2 u   33   64  377  31.200   +4.123    1.920
```

`*` — выбранный источник, `+` — участвует в усреднении, `-` — отброшен, `x` — «лжец»; `reach 377` — 8 успешных опросов подряд; `offset` и `jitter` — в миллисекундах.

---

## 6. Частые проблемы

| Симптом | Решение |
| :--- | :--- |
| `emerge` не ставит ntpsec: блокировка | сначала удалить `net-misc/ntp` (и `openntpd`) — пакеты взаимоисключающие |
| На Gentoo «служба ntpd не найдена» | у ntpsec служба называется **`ntp`**, конфиг — `/etc/conf.d/ntp` |
| После обновления Python `ntpq`/`ntpmon` не запускаются | утилиты на Python: пересобрать `emerge -1 net-misc/ntpsec` после смены `PYTHON_TARGETS` |
| Скрипты используют `ntpdc` | переписать на `ntpq` (`ntpdc` удалён) |
| Конфиг с `broadcast`, `manycastclient`, `crypto`/`autokey` | эти режимы удалены — заменить на `server`/`pool` и NTS |
| NTS не поднимается | закрыт TCP 4460, нет корневых сертификатов (`app-misc/ca-certificates`) или часы сбиты так, что TLS-сертификат «недействителен» |
| ntpd «не синхронизирован» долго после старта | нормально для первых минут; добавить `iburst`, проверить `-g` в `NTPD_OPTS` |

## 🔗 Ссылки

- Сайт: https://www.ntpsec.org/ · документация: https://docs.ntpsec.org/latest/
- Отличия от NTP Classic: https://docs.ntpsec.org/latest/ntpsec.html
- NTS Quick Start: https://docs.ntpsec.org/latest/NTS-QuickStart.html
- Исходники и новости: https://gitlab.com/NTPsec/ntpsec (файл `NEWS.adoc`)
- Удаление `net-misc/ntp` в Gentoo: https://bugs.gentoo.org/962880
- Публичные NTS-серверы: https://github.com/jauderho/nts-servers

Связанная заметка: [chrony — синхронизация времени](chrony%20%E2%80%94%20%D1%81%D0%B8%D0%BD%D1%85%D1%80%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%B8%20%28NTP-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%2C%20NTS%2C%20PTP-PHC%2C%20chronyc%29%2C%20%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B0%20ntp%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20Entware.md).

#Network #NTP #ntpsec #Linux #Gentoo #OpenRC
