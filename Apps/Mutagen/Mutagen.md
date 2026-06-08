---
создал заметку: 2026-06-08T18:00:00
author: WhiteK0T
tags:
  - Mutagen
  - Синхронизация
  - SSH
  - DevTools
Источник:
  - https://mutagen.io/documentation/introduction
  - https://github.com/mutagen-io/mutagen
---

# 🔄 Mutagen — синхронизация файлов и проброс портов

**Mutagen** — инструмент для **двусторонней синхронизации файлов** и **проброса сетевых портов** в реальном времени поверх **SSH** (а также Docker, k8s). Главный сценарий: код редактируется локально в любимой IDE, а Mutagen мгновенно отражает изменения на удалённом сервере (где идёт сборка/запуск) — и наоборот.

> [!info] Где ставить
> Mutagen ставится **только на локальную машину** (Mac/Windows/Linux). На сервер ничего ставить не нужно — Mutagen сам доставляет туда агента по SSH. Все команды выполняются локально.

## 📦 Установка и настройка по ОС

- 🪟 [Установка и настройка Mutagen — Windows](Установка%20и%20настройка%20Mutagen%20%E2%80%94%20Windows.md)
- 🐧 [Установка и настройка Mutagen — Linux](Установка%20и%20настройка%20Mutagen%20%E2%80%94%20Linux.md)
- 🍎 [Установка и настройка Mutagen — macOS](Установка%20и%20настройка%20Mutagen%20%E2%80%94%20macOS.md)

## ⚡ Краткий справочник команд

### Демон

| Команда | Что делает |
| :--- | :--- |
| `mutagen daemon start` | запустить демон (работает в фоне, следит за изменениями) |
| `mutagen daemon stop` | остановить демон |
| `mutagen daemon register` | автозапуск демона при входе в систему (один раз) |

### Синхронизация (`sync`)

| Команда | Что делает |
| :--- | :--- |
| `mutagen sync create <alpha> <beta>` | создать сессию синхронизации |
| `mutagen sync list [-l]` | список сессий (`-l` — подробно) |
| `mutagen sync monitor` | следить за статусом в реальном времени |
| `mutagen sync flush` | принудительный цикл синхронизации сейчас |
| `mutagen sync pause` / `resume` | пауза / возобновление |
| `mutagen sync reset` | сброс при конфликте/ошибке |
| `mutagen sync terminate` | удалить сессию |

**Endpoint** (`alpha`/`beta`) — это локальный путь или `[user@]host:path` (хост берётся из `~/.ssh/config`). Пример:

```bash
mutagen sync create --name=my-project \
  ~/Projects/my-project \
  my-server:/home/user/projects/my-project
```

### Проброс портов (`forward`)

| Команда | Что делает |
| :--- | :--- |
| `mutagen forward create tcp:localhost:8080 my-server:tcp:localhost:80` | туннель порта |
| `mutagen forward list` / `terminate` | список / удалить |

> **sync vs forward:** `sync` синхронизирует **файлы** между двумя точками; `forward` пробрасывает **сетевой порт** (TCP/Unix-сокет) между ними. Это независимые подсистемы.

### Проект (`project`) — через `mutagen.yml`

Если в текущей папке лежит `mutagen.yml`, можно поднять сразу все описанные в нём сессии:

| Команда | Что делает |
| :--- | :--- |
| `mutagen project start` | запустить все сессии из `mutagen.yml` |
| `mutagen project terminate` | завершить проект |
| `mutagen project list` / `flush` | список / принудительный flush |

## 🗂️ Рабочий конфиг (`mutagen.yml`)

Проектный файл описывает дефолты и именованные сессии. Запускается командой `mutagen project start` из папки с файлом.

```yaml
sync:
  defaults:
    # Двусторонняя синхронизация. При конфликте приоритет у локальных изменений (alpha)
    mode: "two-way-resolved"
    # Исключения
    ignore:
      vcs: true            # игнорировать каталоги VCS (.git и т.п.)
      paths:
        - "target/"
        - "build/"
        - ".gradle/"
        - "*.class"
        - "*.jar"
        - "*.war"
        - ".idea/"
        - "*.iml"
        - ".vscode/"
        - "*.log"
        - "hs_err_pid*.log"
        - "replay_pid*.log"
        - "node_modules/"
        - ".mutagen.yml"

  fictionbook-sync:
    alpha: "/home/sam/dev/java/FictionBook/"     # локальная папка
    beta: "claude:/home/claude/FictionBook/"     # удалённая (host из ~/.ssh/config)
    flushOnCreate: true                          # сразу синхронизировать при создании
    configurationBeta:
      permissions:
        defaultFileMode: 0644
        defaultDirectoryMode: 0755
```

**Разбор:**
- `mode: two-way-resolved` — двусторонняя синхронизация; при конфликте «побеждает» сторона `alpha` (локальная), без ручного разбора.
- `ignore.vcs: true` + `ignore.paths` — не синхронизировать VCS-каталоги, артефакты сборки (Java/Gradle/Maven), IDE-файлы, `node_modules`, логи.
- `fictionbook-sync` — именованная сессия: `alpha` (локально) ↔ `beta` (удалённо `claude:...`).
- `flushOnCreate: true` — выполнить полную синхронизацию сразу при создании сессии.
- `configurationBeta.permissions` — задать права на файлы/папки **только на стороне beta** (сервере).

#Mutagen #Синхронизация #SSH #DevTools
