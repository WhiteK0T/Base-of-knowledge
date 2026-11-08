---
создал заметку: 2026-11-08T12:23:00
author: WhiteK0T
tags:
  - AI
  - ClaudeCode
  - Skills
  - Плагин
  - Каталог
  - claude-code-templates
Источник:
  - https://t.me/bugnotfeature/28709
  - https://aitmpl.com/
  - https://github.com/davila7/claude-code-templates
  - https://www.npmjs.com/package/claude-code-templates
---

# 🧰 Claude Code Templates (aitmpl.com) — каталог компонентов Claude Code

**[aitmpl.com](https://aitmpl.com/)** — сайт открытого каталога [claude-code-templates](https://github.com/davila7/claude-code-templates) (Daniel Avila, davila7). Собраны готовые компоненты для Claude Code — скиллы, агенты, команды, хуки, MCP-серверы, настройки, моды, циклы — с разбивкой по категориям и поиском. Ставятся они одной командой через `npx claude-code-templates`. Заметка по посту [«Не баг, а фича»](https://t.me/bugnotfeature/28709) от 29 октября 2026 года, сверена с репозиторием и сайтом.

| | |
| :--- | :--- |
| Лицензия | MIT (сам каталог; у заимствованных компонентов — лицензии их авторов) |
| Репозиторий | с июля 2025 года, ~33 тыс. звёзд, ~3,9 тыс. форков, ~460 открытых issue и PR |
| Установщик | npm `claude-code-templates` 1.32.2, ~5 тыс. загрузок в неделю |
| На сайте | разделы скиллов, агентов, команд, хуков, MCP, модов, плагинов, настроек, «trending»; плюс непрофильные `/jobs`, `/certifications`, `/supporters` |

## 1. Сколько чего

Подсчёт по репозиторию на 8 ноября 2026 года:

| Раздел | Сколько | Что это |
| :--- | ---: | :--- |
| Скиллы | 922 | `SKILL.md` по 32 категориям |
| Агенты | 421 | субагенты Claude Code (`.md`) |
| Команды | 348 | слэш-команды |
| MCP | 124 | конфиги MCP-серверов |
| Настройки | 80 | фрагменты `settings.json` |
| Хуки | 64 | хуки событий Claude Code |
| Моды | 50 | плагины с функциями-хуками на TypeScript, например [Ultra Config](Ultra%20Config%20%28claude-code-templates%29%20%E2%80%94%20%D0%BC%D0%BE%D0%B4%20Claude%20Code%20%D1%81%20%D0%BF%D1%8F%D1%82%D1%8C%D1%8E%20%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8F%D0%BC%D0%B8%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA%20%28%D1%87%D1%82%D0%BE%20%D0%BC%D0%B5%D0%BD%D1%8F%D0%B5%D1%82%20%D0%BA%D0%B0%D0%B6%D0%B4%D1%8B%D0%B9%2C%20%D0%BE%D1%82%D0%BA%D0%B0%D1%82%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20settings.json%29.md) |
| Циклы | 18 | сценарии долгой работы агента: «сборка — тест — исправление», ревью, ночные PR и т. п. |
| Песочницы | 3 | запуск в Docker, E2B, Cloudflare |
| Плагины | 2 | ссылки на чужие репозитории |

## 2. Что подтверждается в посте

- **Открытый код** — да, MIT, всё лежит на GitHub.
- **Разделы и поиск** — да: навыки, агенты, команды, хуки, MCP, плагины, циклы, настройки, моды.
- **«Огромная коллекция»** — да, больше 2 000 компонентов. Но это не значит, что все одного качества: каталог собирает и чужие компоненты, и сгенерированные агентами (раздел 3).

## 3. Откуда компоненты и как проверяются

- **Наполнение.** Каталог пополняют сообщество (PR из форков, их сливают вручную) и агенты мейнтейнера. PR агентов из веток самого репозитория сливаются автоматически, если прошла общая проверка и нет метки `needs-human`. Часть скиллов подтягивается из внешних репозиториев — для них есть отдельная проверка устаревания.
- **Проверка скиллов в PR** — сканером [SkillSpector от NVIDIA](../../../Security/SkillSpector%20%28NVIDIA%29%20%E2%80%94%20%D1%81%D0%BA%D0%B0%D0%BD%D0%B5%D1%80%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BE%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8%20%2871%20%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%2C%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B0%200%E2%80%93100%3B%20LLM-%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E%20%D1%88%D0%BB%D1%91%D1%82%20%D1%84%D0%B0%D0%B9%D0%BB%D1%8B%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D1%83%29.md), только статический анализ. PR блокируется, лишь если оценка изменённого скилла выше 50 **и** выросла по сравнению с `main`. Скилл, у которого высокая оценка уже была в `main`, можно править без блокировки за старые находки.
- **Еженедельный прогон всего каталога** только формирует отчёт и ничего не блокирует. На 5 ноября 2026 года он дал около **5 000 находок**: их пришлось убрать из code scanning GitHub, чтобы не тонули предупреждения о коде самого проекта. Результаты по каждому компоненту показываются на сайте значком SkillSpector.
- **Установщик:**
  - скачивает компоненты с ветки `main` в момент установки, без закрепления версии. Исключение — `--plugin`: плагины закреплены за проверенным коммитом;
  - отправляет на `aitmpl.com` аналитику: тип и имя компонента, путь установки, версию CLI. Отключается переменной `CCT_NO_TRACKING=true`.

## 4. Как пользоваться

Нужен Node.js с `npx`:

| Система | Команда |
| :--- | :--- |
| Gentoo | `emerge --ask net-libs/nodejs` |
| Debian / Ubuntu | `sudo apt install nodejs npm` |
| Arch | `sudo pacman -S nodejs npm` |

```bash
export CCT_NO_TRACKING=true
npx claude-code-templates@latest                                  # интерактивный выбор
npx claude-code-templates@latest --agent <категория/имя>          # один агент
npx claude-code-templates@latest --skill <категория/имя>
npx claude-code-templates@latest --command <категория/имя>
npx claude-code-templates@latest --hook <категория/имя>
npx claude-code-templates@latest --mcp <категория/имя>
npx claude-code-templates@latest --setting <категория/имя>
npx claude-code-templates@latest --mod <категория/имя>            # мод (плагин на функциях-хуках)
npx claude-code-templates@latest --loop <категория/имя>           # цикл вместе с компонентами, на которые он ссылается
npx claude-code-templates@latest --plugin <имя> --scope project   # плагин, закреплённый за проверенным коммитом
npx claude-code-templates@latest --agent <…> --dry-run            # показать, что будет скопировано
```

Другие каталоги задаёт `-d <каталог>`, несколько компонентов указываются через запятую. У CLI есть и посторонние функции: `--analytics` (локальная панель статистики сессий на `localhost:3333`), `--chats` (просмотр переписки с Claude Code в браузере), `--health-check`.

### Перед установкой

- **Посмотреть исходник.** На карточке сайта есть ссылка на GitHub. Особенно внимательно — хуки, MCP-конфиги и моды: они выполняют команды и код с вашими правами.
- **Посмотреть значок SkillSpector на карточке** или прогнать сканер самому: `skillspector scan <папка компонента> --no-llm`.
- **Ставить по одному компоненту и в проект**, а не пачкой и в `~/.claude/`. Каждый скилл и агент добавляет описание в фоновый контекст. Сотня компонентов «на всякий случай» — это тысячи токенов в каждом запросе и путаница в том, какой скилл сработает.
- **Не запускать `--prompt`** с чужими промптами: этот флаг сразу после установки выполняет переданный промпт в Claude Code.

## Связанные заметки

- [Ultra Config — мод из этого каталога](Ultra%20Config%20%28claude-code-templates%29%20%E2%80%94%20%D0%BC%D0%BE%D0%B4%20Claude%20Code%20%D1%81%20%D0%BF%D1%8F%D1%82%D1%8C%D1%8E%20%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D1%8F%D0%BC%D0%B8%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA%20%28%D1%87%D1%82%D0%BE%20%D0%BC%D0%B5%D0%BD%D1%8F%D0%B5%D1%82%20%D0%BA%D0%B0%D0%B6%D0%B4%D1%8B%D0%B9%2C%20%D0%BE%D1%82%D0%BA%D0%B0%D1%82%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20settings.json%29.md) — подробный разбор установщика и одного мода
- [SkillSpector (NVIDIA) — сканер скиллов до установки](../../../Security/SkillSpector%20%28NVIDIA%29%20%E2%80%94%20%D1%81%D0%BA%D0%B0%D0%BD%D0%B5%D1%80%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BE%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8%20%2871%20%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%2C%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B0%200%E2%80%93100%3B%20LLM-%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E%20%D1%88%D0%BB%D1%91%D1%82%20%D1%84%D0%B0%D0%B9%D0%BB%D1%8B%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D1%83%29.md) — тот же сканер, что работает в CI каталога
- [Skills Hub (Hermes Agent) — 90 700 скиллов в одном каталоге](../../Skills/Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md) — ещё больший каталог с теми же вопросами о происхождении
- [agent-skills — реестр проверенных скиллов](../../Skills/agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md) — меньше, но с ручной проверкой
- [claude-skills (alirezarezvani) — 374 скилла «вместо команды»](../../Skills/claude-skills%20%28alirezarezvani%29%20%E2%80%94%20374%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%B0%20%C2%AB%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%C2%BB%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2036k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D1%81%D0%B0%D0%BC%20%D0%BD%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D0%B5%D1%82%29.md) — что бывает, если поставить сотни скиллов сразу

## 🔗 Ссылки

- Пост: https://t.me/bugnotfeature/28709
- Сайт каталога: https://aitmpl.com/
- Репозиторий: https://github.com/davila7/claude-code-templates
- npm: https://www.npmjs.com/package/claude-code-templates

#AI #ClaudeCode #Skills #Плагин #Каталог #claude-code-templates
