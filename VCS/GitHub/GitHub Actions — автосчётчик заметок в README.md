---
создал заметку: 2026-06-08T17:00:00
author: WhiteK0T
tags:
  - GitHub
  - GitHub_Actions
  - CI_CD
  - Автоматизация
Источник:
  - https://docs.github.com/actions
---

# GitHub Actions — автосчётчик заметок в README

Бейдж «Заметок-NN» в [README](../../README.md) раньше правился руками и легко расходился с реальностью. Этот **workflow** при каждом push пересчитывает число `.md`-заметок и сам обновляет цифру в бейдже отдельным коммитом бота.

GitHub автоматически подхватывает любой `*.yml` из каталога `.github/workflows/` как workflow — отдельной кнопки «включить» не нужно.

## 📜 Скрипт целиком

Файл `.github/workflows/note-count.yml`:

```yaml
name: Update note count

# Пересчитывает число заметок и обновляет бейдж в README при каждом push,
# затрагивающем markdown-файлы.
on:
  push:
    branches: [master]
    paths:
      - '**.md'
      - '.github/workflows/note-count.yml'

# Нужно право записи, чтобы запушить обновлённый README обратно.
permissions:
  contents: write

jobs:
  update-count:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Count notes and update badge
        run: |
          # Тематические заметки = все .md, кроме служебных папок и мета-файлов.
          COUNT=$(find . -name '*.md' \
            -not -path './.obsidian/*' \
            -not -path './Templates/*' \
            -not -path './Cache/*' \
            -not -path './.github/*' \
            -not -name 'README.md' \
            -not -name 'CLAUDE.md' \
            -not -name 'Obsidian Base Settings.md' \
            | wc -l | tr -d ' ')
          echo "Найдено заметок: $COUNT"
          # Подменяем число в бейдже вида ...badge/Заметок-NN-success
          sed -i -E "s/(badge\/Заметок-)[0-9]+(-success)/\1${COUNT}\2/" README.md

      - name: Commit if changed
        run: |
          if git diff --quiet README.md; then
            echo "Число не изменилось — коммит не нужен."
            exit 0
          fi
          git config user.name  "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git commit -m "chore: update note count badge [skip ci]"
          git push
```

## 🧩 Как это работает по блокам

### 1. Когда запускается — `on:`

Триггер — `push` в `master`, но **только** если в коммите менялись `.md` (или сам workflow). Фильтр `paths` экономит минуты Actions: правки картинок/конфигов его не дёргают. Число заметок меняется лишь при добавлении/удалении `.md` — то есть это ровно нужный момент.

### 2. Права — `permissions:`

По умолчанию у workflow доступ только на чтение. Раз он коммитит README обратно — нужно явно дать `contents: write`. Пуш идёт встроенным `GITHUB_TOKEN` (выдаётся каждому запуску автоматически, создавать секрет не надо).

### 3. Шаги — `steps:`

- **`actions/checkout@v5`** — клонирует репозиторий в раннер (чистая Ubuntu-виртуалка), иначе файлов там нет. Версия `v5` работает на Node.js 24; более старая `v4` крутится на Node.js 20, который GitHub выводит из эксплуатации (форс на Node 24 с 16 июня 2026, удаление Node 20 — с 16 сентября 2026).
- **Подсчёт + замена.** `find` собирает все `.md`, кроме служебных папок (`.obsidian`, `Templates`, `Cache`, `.github`) и мета-файлов (`README.md`, `CLAUDE.md`, `Obsidian Base Settings.md`). `sed` находит в URL бейджа кусок `Заметок-NN-success` и подменяет только число.
- **Коммит, только если изменилось.** `git diff --quiet README.md` истинно, когда правок нет → выходим без пустого коммита. Иначе коммитит бот `github-actions[bot]`.

## ♾️ Почему нет бесконечного цикла

Два предохранителя:

1. **`[skip ci]`** в сообщении коммита — GitHub пропускает запуск Actions для таких коммитов.
2. Даже без этого: пуши, сделанные `GITHUB_TOKEN`, **по дизайну не триггерят** новые workflow. А если бы и стриггерили — на втором прогоне число то же, diff пустой, коммита нет.

## ⚠️ Подводные камни

- **UTF-8 в `sed`.** Метка бейджа — кириллица (`Заметок`), `sed` матчит её побайтово, число ловится через ASCII `[0-9]+` — работает на стандартном `ubuntu-latest`.
- **Логика подсчёта живёт в двух местах.** Если меняешь правила (новая служебная папка) — поправь `find` и здесь, и при ручной сверке.
- **Только цифра динамическая.** Сам бейдж остаётся статичным [shields.io](https://shields.io); подменяется лишь число в его URL. Альтернатива — полностью динамический endpoint-бейдж, но для счётчика это избыточно.
- **Каталог в README не обновляется.** Workflow трогает только число; список заметок по-прежнему правится вручную (автогенерация рискует затереть ручные описания).

#GitHub #GitHub_Actions #CI_CD #Автоматизация
