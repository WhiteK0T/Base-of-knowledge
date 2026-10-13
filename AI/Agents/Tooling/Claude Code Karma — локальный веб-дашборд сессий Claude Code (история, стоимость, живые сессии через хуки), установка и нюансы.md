---
создал заметку: 2026-10-14T17:00:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Мониторинг
  - Hooks
  - SelfHosted
Источник:
  - https://t.me/open_source_friend/5905
  - https://github.com/JayantDevkar/claude-code-karma
---

# 📊 Claude Code Karma — локальный веб-дашборд сессий Claude Code

**[Claude Code Karma](https://github.com/JayantDevkar/claude-code-karma)** читает то, что Claude Code и так сохраняет в `~/.claude/` (JSONL-файлы сессий), и показывает это в браузере: сессии по проектам, ход каждой сессии по шагам, затраты и токены, инструменты, агенты, скиллы, хуки, плагины. С установленными хуками видны и **идущие прямо сейчас** сессии.

| | |
| :--- | :--- |
| Лицензия | **Apache-2.0** |
| Звёзды / форки | 332 · 36, проект с января 2026 |
| Активность | живой: последние коммиты 11–12.10.2026 (ускорение, исправление подсчёта стоимости) |
| Стек | FastAPI (Python 3.10+) на порту **8020** + SvelteKit (Node 18+) на порту **5180** |

Всё из поста подтверждается: работает локально, без аккаунтов и телеметрии. Внешних запросов в коде API нет. Индекс хранится в SQLite в `~/.claude_karma/metadata.db`.

---

## 1. Что показывает

- **Сессии**: поиск по названию и запросам, фильтр по проекту; идущие сейчас сессии — сверху с меткой статуса.
- **Страница сессии**: хронология всех запросов, вызовов инструментов, размышлений модели и ответов; вкладки **задачи**, **файлы** (кто, когда и каким инструментом читал или менял файл), **субагенты**, **скиллы**, **фоновые процессы**, **аналитика** (стоимость, токены, доля попаданий в кэш, распределение инструментов).
- **Проекты** — сгруппированы по git-репозиториям.
- **Общая аналитика**: токены, стоимость, тренды, доля кэша, по каким моделям и в какие часы вы работаете.
- **Инструменты и MCP, агенты, скиллы, хуки, плагины** — что установлено и как часто используется.
- **Привязка к задачам** Linear, Jira и GitHub Issues: вручную, командой `/link-ticket-to-session ABC-123` или автоматически по имени ветки. Karma только читает: в трекер ничего не пишет.
- Планы, палитра команд (`Ctrl+K`), кнопка «открыть терминал» с идущей сессией (macOS Terminal, iTerm2 и tmux).

---

## 2. Установка

Нужны Python 3.10+, Node.js 18+, npm и git:

| Система | Зависимости |
| :--- | :--- |
| **Gentoo** | `emerge --ask dev-lang/python net-libs/nodejs dev-vcs/git` (npm входит в `nodejs` с USE-флагом `npm`) |
| **Debian / Ubuntu** | `sudo apt install python3-venv python3-pip nodejs npm git` (если Node в репозитории старше 18 — из NodeSource) |
| **Arch** | `sudo pacman -S python nodejs npm git` |
| **Entware** | не подходит: дашборд должен стоять там же, где Claude Code и его `~/.claude/` |

Уровни установки:

| Уровень | Что добавляет |
| :--- | :--- |
| **1. Дашборд** | API + веб-интерфейс: просмотр истории |
| **2. Живые сессии** (рекомендуется) | хук `live_session_tracker.py`: статус сессий в реальном времени |
| **3. Названия сессий** | хук, который придумывает понятные названия: сначала из git, иначе через `claude -p --model haiku` |
| **4. Задачи** | скилл `link-ticket-to-session` и опциональный хук определения задачи по ветке |

### Уровень 1

```bash
git clone https://github.com/JayantDevkar/claude-code-karma.git
cd claude-code-karma

# API (терминал 1)
cd api
python3 -m venv venv && . venv/bin/activate
pip install -e ".[dev]" && pip install -r requirements.txt
uvicorn main:app --port 8020          # слушает 127.0.0.1

# веб-интерфейс (терминал 2)
cd ../frontend
npm install && npm run dev            # http://localhost:5180
```

Проверка: `curl http://localhost:8020/health` — в ответе `session_count` должно совпадать с числом ваших сессий.

### Уровень 2 — живые сессии

Скрипт хука кладётся в `~/.claude/hooks/` (симлинком или копией), а в `~/.claude/settings.json` регистрируется на события `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Notification`, `Stop`, `SubagentStart` и `SubagentStop`. Готовый JSON — в [SETUP.md](https://github.com/JayantDevkar/claude-code-karma/blob/main/SETUP.md) раздел Tier 2.

> [!warning] Хуки меняют ваш `settings.json`
> Перед правкой сделайте копию `~/.claude/settings.json`. Хуки запускаются на **каждый** вызов инструмента — если API Karma выключен, они должны быстро завершаться (в последних версиях исправлены таймауты хуков). Уровень 3 тратит лимиты вашей подписки: на каждую сессию без названия из git — один запрос к Haiku.

### Автозапуск

Готовый установщик ярлыка и автозапуска (`scripts/install_karma_app.py`) есть **только для macOS и Windows**. На Linux можно сделать пользовательскую службу, например для systemd (Debian, Arch):

```ini
# ~/.config/systemd/user/karma-api.service
[Unit]
Description=Claude Code Karma API
[Service]
WorkingDirectory=%h/claude-code-karma/api
ExecStart=%h/claude-code-karma/api/venv/bin/uvicorn main:app --port 8020
Restart=on-failure
[Install]
WantedBy=default.target
```

`systemctl --user enable --now karma-api`. Веб-интерфейс — так же, через собранную версию (`npm run build`, затем `node build` из `frontend/`). На Gentoo с OpenRC — скрипт в `/etc/init.d/` с `command_user` вашего пользователя. В автозапуске Karma занимает около 200–250 МБ памяти.

---

## 3. Важно: история хранится 30 дней

Claude Code по умолчанию **удаляет сессии старше 30 дней** из `~/.claude/projects/`, и вместе с ними они пропадают из Karma. Чтобы видеть историю дольше, увеличьте срок в `~/.claude/settings.json`:

```json
{
  "cleanupPeriodDays": 365
}
```

Это же значение можно поменять в настройках самого Karma. Учтите, что JSONL-файлы сессий занимают место и содержат всё, что было в сессиях, включая содержимое файлов и вывод команд.

---

## 4. Чем отличается от соседей

| | **Karma** | [**abtop**](abtop%20%E2%80%94%20htop%20%D0%B4%D0%BB%D1%8F%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B9%20Claude%20Code-Codex-OpenCode%29.md) | `/usage` в Claude Code |
| :--- | :--- | :--- | :--- |
| Где | веб-интерфейс | терминал | внутри сессии |
| История | все сохранённые сессии, разбор по шагам | только текущие | текущий расход и лимиты |
| Агенты | только Claude Code | Claude Code, Codex, OpenCode | — |
| Установка | Python + Node, хуки | один бинарник | встроено |

Karma — когда нужно разобрать прошлые сессии и посмотреть, куда ушли токены и деньги. abtop — быстро глянуть, что делают агенты прямо сейчас.

## 🔗 Ссылки

- Репозиторий: https://github.com/JayantDevkar/claude-code-karma
- Пошаговая установка: https://github.com/JayantDevkar/claude-code-karma/blob/main/SETUP.md
- Исходный пост: https://t.me/open_source_friend/5905

Связанные заметки: [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md), [Claude Code — кэш промптов](../Claude%20Code%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D0%BE%D0%B2%20%28TTL%205%20%D0%BC%D0%B8%D0%BD%D1%83%D1%82%20%D0%B8%201%20%D1%87%D0%B0%D1%81%2C%20subagentPromptCacheTtl%2C%20%D1%87%D1%82%D0%BE%20%D1%81%D0%B1%D1%80%D0%B0%D1%81%D1%8B%D0%B2%D0%B0%D0%B5%D1%82%20%D0%BA%D1%8D%D1%88%29.md).

#AI #Claude_Code #Мониторинг #Hooks #SelfHosted
