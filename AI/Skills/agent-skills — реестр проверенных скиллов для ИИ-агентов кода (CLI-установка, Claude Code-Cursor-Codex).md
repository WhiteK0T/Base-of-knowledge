---
создал заметку: 2026-06-26T18:00:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Skills
  - Безопасность
  - Реестр
  - Ресурсы
Источник:
  - https://t.me/bugnotfeature/26075
  - https://github.com/tech-leads-club/agent-skills
---

# 📦 agent-skills — реестр проверенных скиллов для ИИ-агентов кода (CLI-установка)

[**agent-skills**](https://github.com/tech-leads-club/agent-skills) (tech-leads-club) — **реестр готовых скиллов** (`SKILL.md`) для ИИ-агентов кода с **CLI-установщиком**: одной командой подключаешь нужный скилл (Playwright-парсер, поиск уязвимостей, AWS-советник и т.д.) к [Claude Code](../Claude%20Code%20%E2%80%94%20гайд.md), Cursor, Codex, Copilot и ещё ~десятку агентов. Позиционируется как **«secure, validated»** — кураторская альтернатива случайным `SKILL.md` из интернета. CLI на TypeScript, ~**4700★**, обновляется (правки — сегодня).

> [!note] Что такое скилл и зачем реестр
> Скилл — это папка с `SKILL.md` (инструкции-промпт) + опционально `templates/` и `references/`; формат [Anthropic Agent Skills](https://www.anthropic.com/news/skills), который агент подхватывает, когда задача совпадает с описанием (механика — как у [Ponytail](Ponytail%20%E2%80%94%20скилл%20против%20%C2%ABграфомании%C2%BB%20AI-агентов%20в%20коде.md)). Проблема: скиллы расползаются по репозиториям, формат под каждый агент свой. agent-skills решает это **единым каталогом + CLI**, который раскладывает скилл в нужную папку конкретного агента (`~/.claude`, `~/.gemini`, проектные конфиги).

## 🚀 Как пользоваться (CLI)

```bash
# интерактивный мастер: выбрать скилл, агента, способ (copy/symlink), scope (global/project)
npx @tech-leads-club/agent-skills

# или по командам
npx @tech-leads-club/agent-skills list                 # список доступных скиллов
npx @tech-leads-club/agent-skills install -s playwright-skill   # поставить конкретный
npx @tech-leads-club/agent-skills update               # обновить установленные
npx @tech-leads-club/agent-skills remove               # удалить
```

Скилл ставится **глобально** (в домашние папки агента) или **на проект**; скачанное кэшируется в `~/.cache/agent-skills/` (работает офлайн).

## 🤖 Кого поддерживает (16+ агентов)

| Уровень | Агенты |
| :--- | :--- |
| **Популярные** | Claude Code, Cursor, Cline, GitHub Copilot, Windsurf |
| **Восходящие** | Antigravity, Aider, Gemini CLI, OpenAI Codex |
| **Enterprise** | Amazon Q, Augment, Sourcegraph Cody, Tabnine |

Примеры скиллов: **playwright-skill** (браузерная автоматизация/тесты), **security-best-practices** (поиск и отчёт по уязвимостям), **aws-advisor** (архитектура/безопасность AWS), **figma** (дизайн→код), **tlc-spec-driven** (планирование проекта по 4-фазному workflow).

## 🧪 Факты против хайпа (сверено с README)

> [!warning] «Все топовые SKILL.md в одном месте» — с оговорками
> - В посте упор на **безопасность**: «куча скиллов на GitHub с малварёй, а тут проверенные». Защита реальна, но это **best-effort, а не гарантия** (см. ниже).
> - Команда из поста `agent-skills install -s playwright-skill` верна по сути, но запускается через **`npx @tech-leads-club/agent-skills ...`** (или глобально установленный бинарь) — голого `agent-skills` в PATH сразу нет.
> - Точное число скиллов в README не зафиксировано — реестр «растущий», не статичные «5 штук».

> [!caution] «Validated» — что реально проверяют (и чего это не гарантирует)
> README заявляет: 100% open-source (без бинарей), **статический анализ в CI/CD**, скан каждого скилла **Snyk Agent Scan** перед публикацией, **ручная курация** промптов, защита самого CLI (санитизация, path-изоляция, защита от symlink-атак). Мотивация — тезис «13% скиллов на маркетплейсах содержат критические уязвимости».
> - Но скилл — это **инструкции, которые твой агент выполнит** (вызовет команды, прочитает/запишет файлы). Сканер ловит явные паттерны, а не злонамеренный промпт, замаскированный под полезный.
> - **Читай `SKILL.md` перед установкой** — особенно скиллы с доступом к shell/сети. Доверие к реестру ≠ слепое доверие каждому скиллу.
> - **Third-party-скиллы** проходят меньше контроля, чем «родные» от Tech Leads Club.

> [!info] Лицензии — разные внутри одного репо
> - **CLI/движок** — **MIT**.
> - **Скиллы Tech Leads Club** — **CC-BY-4.0** (нужна атрибуция).
> - **Сторонние скиллы** сохраняют свои лицензии (смотри в самом `SKILL.md`). На GitHub лицензия репо помечена как `NOASSERTION` именно из-за этой смеси — это норма, а не «без лицензии».

## 💻 Как это ложится на твои системы

| Система | Применимость |
| :--- | :--- |
| **Gentoo / Debian / Arch** (десктоп) | Основной путь. Нужен **Node.js/npm** (`nodejs` в Gentoo `net-libs/nodejs`, `nodejs npm` в Debian/Arch) для `npx`. Сам по себе скилл-движок кроссплатформенный; работает с твоим уже стоящим агентом (Claude Code/Cursor) |
| **Arch** (план с июня 2026) | как выше; node из repo |
| **Entware / RT-AX56U** | **N/A на практике** — node под Entware есть (`opkg install node`), но ИИ-агенты кода (Claude Code/Cursor) на роутере не работают; скиллам тут негде применяться |

## 💡 Кому полезно

- **Пользователям Claude Code/Cursor/Codex:** быстро ставить готовые проверенные скиллы вместо ручного копирования `SKILL.md` и адаптации под формат своего агента.
- **Командам:** единый источник скиллов + обновление по команде (меньше дрейфа между разработчиками).
- **Не** «магия, делающая агента умнее»: скилл — это структурированный промпт; качество зависит от самого скилла, и проверять его всё равно нужно.

## 🔗 Ссылки

- Репозиторий: [github.com/tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) · сайт-каталог [agent-skills.techleads.club](https://agent-skills.techleads.club/)
- Формат: [Anthropic Agent Skills](https://www.anthropic.com/news/skills)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26075)
- Связанные: [Ponytail (скилл Claude Code)](Ponytail%20%E2%80%94%20скилл%20против%20%C2%ABграфомании%C2%BB%20AI-агентов%20в%20коде.md) · [Awesome-Journal-Skills (скиллы под журналы)](Awesome-Journal-Skills%20%E2%80%94%20скиллы%20Claude%20Code%20под%20научные%20журналы.md) · [MCP — серверы Model Context Protocol](../MCP%20%E2%80%94%20серверы%20Model%20Context%20Protocol.md) · [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20гайд.md)

#AI #Claude_Code #Skills #Безопасность #Реестр #Ресурсы
