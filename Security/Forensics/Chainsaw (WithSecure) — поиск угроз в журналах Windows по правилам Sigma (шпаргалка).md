---
создал заметку: 2026-10-28T00:23:00
author: WhiteK0T
tags:
  - Security
  - Forensics
  - DFIR
  - BlueTeam
  - Windows
  - EVTX
  - Sigma
  - Шпаргалка
Источник:
  - https://t.me/+3X56uL4A-UM3Njgy
  - https://github.com/WithSecureOpenSource/chainsaw
  - https://github.com/WithSecureOpenSource/chainsaw/releases/tag/v2.17.1
  - https://github.com/SigmaHQ/sigma
---

# 🪚 Chainsaw — поиск угроз в журналах Windows по правилам Sigma (шпаргалка)

**Chainsaw** ([github.com/WithSecureOpenSource/chainsaw](https://github.com/WithSecureOpenSource/chainsaw), бывший `WithSecureLabs/chainsaw` — старые ссылки перенаправляются) — консольная утилита команды WithSecure Countercept для быстрого разбора артефактов Windows **без SIEM**. Она прогоняет журналы событий (EVTX) через правила **Sigma** и собственные правила Chainsaw, ищет по строкам, регуляркам и полям событий, разбирает MFT, кусты реестра, SRUM и shimcache. Написана на Rust, лицензия **GPL-3.0**.

На 28.10.2026: версия **v2.17.1** (14.10.2026), ~3,7 тыс. звёзд, проект живой — в октябре добавили модификаторы Sigma `i` и `windash`.

Основа — пост из канала [CodeGuard: PySec Edition](https://t.me/+3X56uL4A-UM3Njgy). Команды ниже сверены с определениями ключей в `src/main.rs` v2.17.1 и с README, состав релиза — по архиву `chainsaw_all_platforms+rules+examples.zip`.

## 📦 Что скачать

Бинарник действительно один и без установки, но для `hunt` ему нужны ещё три вещи: **правила Chainsaw**, **mapping-файл** для Sigma и сами **правила Sigma**.

| Архив релиза | Размер | Что внутри |
| :--- | :--- | :--- |
| `chainsaw_x86_64-unknown-linux-gnu.tar.gz` (и сборки для aarch64 Linux, macOS, Windows) | ~3,5 МБ | только бинарник (Linux x86_64 — glibc ≥ 2.34) |
| `chainsaw_all_platforms+rules.zip` | ~39 МБ | бинарники всех платформ + `rules/` + `mappings/` + копия Sigma |
| `chainsaw_all_platforms+rules+examples.zip` | ~51 МБ | то же + **EVTX-ATTACK-SAMPLES** (66 МБ журналов с атаками — потренироваться) |

- `rules/` — правила Chainsaw: 78 для EVTX (очистка журналов, перебор паролей, RDP, создание служб, срабатывания антивирусов…) и 53 для MFT (следы mimikatz, LaZagne, AnyDesk, сканеров сети…).
- `mappings/sigma-event-logs-all.yml` — какие поля журналов подставлять в правила Sigma. Без него Sigma не запускается.
- `sigma/` в архиве — снимок SigmaHQ (2420 правил для Windows). Свежие правила: `git clone --depth 1 https://github.com/SigmaHQ/sigma.git`.

> [!warning] Антивирус может ругаться
> README предупреждает: EDR/антивирус часто помечает архив как вредоносный — в примерах журналов и правилах Sigma есть строки вроде `mimikatz`, а часть движков срабатывает на сам бинарник. Разбирай **копии журналов на машине аналитика**, а не на поражённом хосте.

## 🚀 Команды из поста — рабочие версии

```bash
# 1. Охота по Sigma с результатом в JSON
chainsaw hunt evtx_files/ -s sigma/rules/ --mapping mappings/sigma-event-logs-all.yml --json -o results.json

# 2. Только правила уровня critical
chainsaw hunt evtx_files/ -s sigma/rules/ --mapping mappings/sigma-event-logs-all.yml --level critical

# 3. Поиск по Event ID (здесь — успешные входы 4624)
chainsaw search -t 'Event.System.EventID: =4624' evtx_files/
```

- **`--sigma` требует `--mapping`** — без mapping-файла Chainsaw не запустится, это прописано в определении ключа.
- **`--output` задаёт только файл**, формат — `--json`, `--jsonl`, `--csv` или `--log`. Без них в `results.json` попадёт обычная текстовая таблица.
- **Ключа `--event-id` нет.** Поля событий ищут tau-выражениями `-t 'Поле: значение'` (синтаксис — ниже).
- **`--level` отбирает правила, а не события.** Несколько уровней — повтором: `--level critical --level high`. Уровень — оценка автора правила, а не вердикт: например, в правилах Chainsaw уровнем `critical` помечен любой вход по RDP (4624, LogonType 10).
- **Сортировки по критичности нет.** Вывод сгруппирован по группам правил (`Group: Antivirus`, `Log Tampering`, `Sigma`…), внутри группы строки идут по времени. Уровень, автора и статус правила в таблице показывает `--metadata`.
- **Форматы входа:** EVTX/EVT, XML, JSON/JSONL, `$MFT`, кусты реестра (`.hve`), ESE-базы (SRUM, `.dat`/`.edb`). **Дампы памяти Chainsaw не разбирает** — это задача Volatility.
- **«2 ГБ за 3 минуты»** — замер автора поста. Время зависит от числа правил, диска и CPU. Сократить его можно, сузив окно (`--from`/`--to`), набор правил (`--level`, `--status stable`) или включив `--preprocess` (бета).

## 🎯 hunt — охота по правилам

```bash
# Sigma + правила Chainsaw, таблица в терминал
chainsaw hunt evtx_files/ -s sigma/rules/ --mapping mappings/sigma-event-logs-all.yml -r rules/

# только правила Chainsaw: без -s/-r первый аргумент — каталог правил
chainsaw hunt rules/ evtx_files/

# high + critical, в JSON
chainsaw hunt evtx_files/ -s sigma/rules/ --mapping mappings/sigma-event-logs-all.yml -r rules/ \
  --level critical --level high --json -o hits.json

# CSV: -o — каталог, внутри по файлу на группу правил
chainsaw hunt evtx_files/ -s sigma/rules/ --mapping mappings/sigma-event-logs-all.yml -r rules/ --csv -o results/

# окно инцидента, время — в своём поясе
chainsaw hunt evtx_files/ -s sigma/rules/ --mapping mappings/sigma-event-logs-all.yml \
  --from 2026-10-20T00:00:00 --to 2026-10-21T00:00:00 --timezone Europe/Moscow

# MFT по правилам Chainsaw для MFT
chainsaw hunt rules/mft/ ./\$MFT
```

| Ключ | Что делает |
| :--- | :--- |
| `-s, --sigma` + `-m, --mapping` | правила Sigma и mapping к ним — только вместе |
| `-r, --rule` | правила Chainsaw (можно повторять) |
| `--level`, `--status`, `--kind` | какие правила загружать: `critical/high/medium/low/info`, `stable/experimental`, `chainsaw/sigma` |
| `--from`, `--to` | окно по времени, формат `YYYY-MM-DDTHH:MM:SS` |
| `--json`, `--jsonl`, `--csv`, `--log` | формат; `-o` — файл, для `--csv` — каталог |
| `--jsonl -c` | `--cache-to-disk`: результаты копятся на диске, меньше RAM на больших наборах |
| `--full`, `--column-width N`, `--metadata` | таблица: значения целиком, ширина колонок, сведения о правиле |
| `--local`, `--timezone <пояс>` | время в местном или указанном поясе (по умолчанию UTC). С `--timezone` в этом же поясе понимаются и границы `--from`/`--to` |
| `--extension evtx`, `--skip-errors` | брать только эти файлы; не падать на битом файле |
| `--no-banner`, `--num-threads N`, `-v` | общие ключи — пишутся **до** подкоманды: `chainsaw --no-banner hunt …` |

Часть правил Sigma Chainsaw не загружает (неподдерживаемые модификаторы, источники журналов, которых нет в mapping) — в начале вывода видно `Loaded N detection rules (M not loaded)`. Проверить набор заранее: `chainsaw lint sigma/rules/ --kind sigma`.

## 🔎 search — поиск по строкам и полям

```bash
chainsaw search mimikatz -i evtx_files/                         # строка, без учёта регистра
chainsaw search -e 'DC[0-9]\.corp\.local' evtx_files/           # регулярное выражение
chainsaw search -t 'Event.System.EventID: =4624' evtx_files/    # поле события

# входы по RDP: несколько -t — это «И»
chainsaw search -t 'Event.System.EventID: =4624' -t 'Event.EventData.LogonType: =10' evtx_files/

# неудачные входы или вход с явными учётными данными: --match-any — «ИЛИ»
chainsaw search --match-any -t 'Event.System.EventID: =4625' -t 'Event.System.EventID: =4648' evtx_files/

# окно по времени: для search нужен --timestamp
chainsaw search -t 'Event.System.EventID: =4104' --timestamp 'Event.System.TimeCreated' \
  --from 2026-10-20T00:00:00 --to 2026-10-21T00:00:00 --json -o ps.json evtx_files/
```

Значение в `-t` (между ключом и значением — двоеточие **и пробел**):

| Запись | Значит |
| :--- | :--- |
| `=4624`, `>5`, `>=`, `<`, `<=` | сравнение чисел |
| `admin` | точное совпадение |
| `admin*`, `*.exe`, `*mimikatz*` | начинается с / заканчивается на / содержит |
| `?regex` | регулярное выражение |
| `i` в начале: `i*mimikatz*` | без учёта регистра |
| `int(Поле)`, `str(Поле)`, `not(Поле)` в ключе | привести тип поля / отрицание |

### Event ID, с которых начинают разбор

| ID | Журнал | Событие |
| :--- | :--- | :--- |
| 4624 / 4625 | Security | успешный / неудачный вход (`LogonType`: 2 — локальный, 3 — сетевой, 10 — RDP) |
| 4648 | Security | вход с явно указанными учётными данными (`runas`, боковое перемещение) |
| 4672 | Security | вход с особыми привилегиями (админ) |
| 4688 | Security | создание процесса (если включён аудит) |
| 4698 | Security | создание запланированной задачи |
| 4720 / 4732 | Security | создан пользователь / добавлен в локальную группу |
| 1102 | Security | журнал безопасности очищен |
| 7045 | System | установлена служба |
| 4104 | PowerShell/Operational | Script Block — текст выполненного PowerShell |
| 1 / 3 / 11 / 13 | Sysmon/Operational | процесс / сетевое соединение / создание файла / запись в реестр |

## 🧰 analyse, dump, lint

```bash
chainsaw analyse evtx evtx_files/            # сводка: сколько событий по каналам и Event ID
chainsaw analyse gaps evtx_files/            # дыры в EventRecordID и долгие паузы — следы выборочного удаления записей без 1102
chainsaw analyse shimcache ./SYSTEM --amcache ./Amcache.hve --tspair \
  --regexfile analysis/shimcache_patterns.txt -o timeline.csv   # таймлайн запусков из shimcache + amcache
chainsaw analyse srum --software ./SOFTWARE ./SRUDB.dat -o srum.json   # SRUM: активность приложений и их сетевой трафик
chainsaw dump ./SOFTWARE.hve --json -o software.json                   # MFT / реестр / ESE → JSON
chainsaw lint rules/ --kind chainsaw         # проверить, что правила загружаются
```

`analysis/shimcache_patterns.txt` лежит в репозитории (в архивы релиза каталог `analysis/` не входит; пакет Kali ставит его в `/usr/share/chainsaw/`). `analyse evtx` и `analyse gaps` появились в 2026 году — в старых сборках их нет.

## 🪟 Где взять журналы на Windows

Журналы лежат в `C:\Windows\System32\winevt\Logs\`. Работающие журналы надёжнее выгрузить штатным `wevtutil` (консоль администратора):

```bat
mkdir C:\IR
wevtutil epl Security C:\IR\Security.evtx
wevtutil epl System C:\IR\System.evtx
wevtutil epl Microsoft-Windows-PowerShell/Operational C:\IR\PowerShell.evtx
wevtutil epl Microsoft-Windows-Sysmon/Operational C:\IR\Sysmon.evtx
```

Каталог `C:\IR` переносят на машину аналитика и разбирают там.

## 💻 Установка на твоих системах

| Система | Как поставить |
| :--- | :--- |
| **Gentoo** | ebuild'а нет ни в основном дереве, ни в `gentoo-zh`, в GURU тоже не нашёл. Варианты: бинарник из релиза (`~/.local/bin` или `/usr/local/bin`, правила и mapping — рядом) или сборка из исходников: `git clone --branch v2.17.1 https://github.com/WithSecureOpenSource/chainsaw.git && cd chainsaw && cargo build --release --locked` (нужен `dev-lang/rust` или `dev-lang/rust-bin`), бинарник — `target/release/chainsaw` |
| **Debian / Ubuntu** | в репозиториях нет; бинарник из релиза работает на Debian 12+ и Ubuntu 22.04+ (glibc ≥ 2.34), на более старых — сборка из исходников со свежим Rust (rustup). **Kali:** `sudo apt install chainsaw` (2.16.0; правила и mapping — в `/usr/share/chainsaw/`, Sigma клонировать отдельно) |
| **Arch** | ⚠️ пакет **`chainsaw` в AUR — другой проект** (Kyverno, тесты Kubernetes). Нужный — в репозитории **BlackArch** (`pacman -S chainsaw` после подключения BlackArch, 2.17.1, только бинарник), либо релиз / `cargo` как выше |
| **Entware / RT-AX56U** | пакета нет, сборки под armv7 тоже нет. Журналы Windows разбирают на ПК, роутер для этого не нужен |
| **Windows** | `chainsaw_x86_64-pc-windows-msvc.zip` из релиза; добавь каталог в исключения антивируса на машине аналитика |
| **Nix** | `nix-shell -p chainsaw` |

> [!caution] `cargo install chainsaw` ставит не то
> Крейт `chainsaw` на crates.io — посторонняя утилита для филогенетических деревьев (newick). Chainsaw от WithSecure на crates.io не публикуется — только из git или релиза.

## 🔗 Ссылки

- Репозиторий: [WithSecureOpenSource/chainsaw](https://github.com/WithSecureOpenSource/chainsaw) · [релизы](https://github.com/WithSecureOpenSource/chainsaw/releases)
- Правила: [SigmaHQ/sigma](https://github.com/SigmaHQ/sigma) · движок выражений [tau-engine](https://github.com/WithSecureLabs/tau-engine)
- Учебные журналы: [EVTX-ATTACK-SAMPLES](https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES)
- Пост: канал [CodeGuard: PySec Edition](https://t.me/+3X56uL4A-UM3Njgy)
- Связанные: [Linux-команды для ИБ — шпаргалка](Linux-%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%91%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%28%D0%B0%D1%83%D0%B4%D0%B8%D1%82%2C%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%D0%BD%D1%86%D0%B8%D0%B4%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%2C%20%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%20%D0%BF%D0%B5%D1%80%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8%29.md) · [tcpdump — захват трафика и фильтры для разбора инцидента](../../Linux/Commands/tcpdump.md)

#Security #Forensics #DFIR #BlueTeam #Windows #EVTX #Sigma #Шпаргалка
