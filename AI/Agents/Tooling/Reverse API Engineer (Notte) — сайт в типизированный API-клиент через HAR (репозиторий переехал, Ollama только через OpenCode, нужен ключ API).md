---
создал заметку: 2026-09-09T18:00:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Парсинг
  - API
  - Playwright
  - Python
Источник:
  - https://t.me/bugnotfeature/27203
  - https://github.com/nottelabs/reverse-api-engineer
  - https://reverseapi.dev
---

# 🔁 Reverse API Engineer — сайт в типизированный API-клиент

Разбор [поста «Не баг, а фича» от 20.08.2026](https://t.me/bugnotfeature/27203). Инструмент настоящий, перечисленные возможности подтвердились почти дословно. Но пост не назвал ни одного условия запуска, а одну строчку в списке агентов поставил не на своё место.

Проверено 09.09.2026 по репозиторию, README, PyPI и сайту проекта.

> [!info] Факты
> | | |
> | :--- | :--- |
> | Репозиторий | **`nottelabs/reverse-api-engineer`** — ссылка из поста ведёт на старый адрес `kalil0321/…` и работает через редирект |
> | Владелец | **Notte** — верифицированная организация, *«Building the browser infrastructure layer for AI agents»*, [notte.cc](https://www.notte.cc/) |
> | Звёзд / форков | **1 137** · 100 |
> | Лицензия / язык | **MIT** · Python |
> | Создан / обновлён | 23.12.2025 / 30.08.2026 |
> | Пакет | `reverse-api-engineer` **0.13.1** на PyPI, Python **≥3.11**, 33 версии |
> | Сайт | [reverseapi.dev](https://reverseapi.dev) — лендинг CLI, платного облака нет |

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| Два режима: Manual и Agent | ✅ Верно | Уточнение: **Agent — режим по умолчанию**, а Manual требует доп-установки `[manual]` и `playwright install chromium` |
| Клиенты на 9 языках | ✅ Точно совпало | `python`, `javascript`, `typescript`, `go`, `java`, `csharp`, `php`, `ruby`, `c` |
| Агенты: Claude, OpenCode, Cursor, GitHub Copilot, **Ollama** | ⚠️ Ollama не в том ряду | SDK всего **четыре**: `claude` (по умолчанию), `opencode`, `cursor`, `copilot`. **Ollama — провайдер внутри OpenCode**, а не отдельный SDK |
| «Превратит ЛЮБОЙ сайт» | ⚠️ Не любой | Caveat из README: *«Sites with aggressive bot detection may block capture or require manual interaction»* |
| Про ключ API | ❌ Умолчание | README прямо: *«Requires Python 3.11+ and an **API key** for agent mode»* |
| Про проверку сгенерированного кода | ❌ Умолчание | Caveat авторов: *«Generated code runs locally via Claude Code, so **review before executing**»* |
| Ссылка на репозиторий | ⚠️ Устарела | Проект переехал в организацию `nottelabs` |

## ⚙️ Как это устроено

Механика простая и честная — никакой магии «ИИ понял сайт»:

1. Даёшь сайт и цель словами («забрать все вакансии Apple»).
2. Браузер идёт по сайту — сам или под управлением агента.
3. **Весь сетевой трафик пишется в HAR-файл.**
4. Модель читает HAR и пишет по нему типизированный клиент на выбранном языке.

То есть инструмент автоматизирует ровно то, что раньше делали руками: открыть DevTools, найти нужные запросы, скопировать cURL и склеить из этого клиент. Ключевой артефакт — **HAR**, а модель работает уже с ним, а не «с сайтом».

```bash
uv tool install reverse-api-engineer          # обычная установка
uv tool install "reverse-api-engineer[manual]" && playwright install chromium   # для ручного режима

reverse-api-engineer
> fetch all apple jobs from their careers page
# → ./scripts/apple_jobs_api/ (api_client.py, README.md, example_usage.py)
```

Agent-режим захватывает трафик через запускаемые из `npx` браузерные MCP-серверы (Playwright или Chrome DevTools) либо через Vercel `agent-browser` CLI — отдельных Python-зависимостей не требует.

## 🔌 Про модели: где деньги, а где бесплатно

Настройки лежат в `~/.reverse-api/config.json`, правятся через `/settings`. По умолчанию:

| Параметр | Значение по умолчанию |
| :--- | :--- |
| `sdk` | `claude` |
| `claude_code_model` / `collector_model` | `claude-sonnet-4-6` |
| `output_language` | `python` |
| `opencode_model` | `big-pickle` |

Варианты по стоимости:

- **Claude** (по умолчанию) — Sonnet 4.6, Opus 4.6 или Haiku 4.5. Нужен ключ, платишь за токены. Команда `/history` показывает прошлые прогоны **со стоимостью** — то есть расход отслеживается явно.
- **OpenCode** — RAE поднимет сервер сам через `npx`, глобальная установка не нужна. Свежие конфигурации по умолчанию берут **бесплатную** модель `opencode/big-pickle`, а в `/settings` бесплатные варианты помечены.
- **Ollama через OpenCode** — полностью локальный путь. RAE поднимет демон, если он установлен, и покажет **только те модели, что уже стоят**, с поддержкой tool calling и контекстом от 64k. Отдельно оговорено: модели **не скачиваются молча**.

> [!tip] Если не хочешь платить
> Рабочая связка — `sdk: opencode` с бесплатной моделью либо Ollama на своих весах. Требование к локальной модели жёсткое: **tool calling и контекст от 64 тысяч**, иначе она в списке не появится. Что под это подходит — смотри в [LLMs-local](../../Local-LLM/LLMs-local%20%E2%80%94%20awesome-%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%B2%D1%81%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0%20%D0%98%D0%98%20%28%D0%B4%D0%B2%D0%B8%D0%B6%D0%BA%D0%B8%2C%20UI%2C%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20RAG%2C%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%BE%2C%20%D0%B3%D0%B0%D0%B9%D0%B4%D1%8B%29.md).

Автозапуск OpenCode требует **Node.js 20+**. Отключается через `RAE_OPENCODE_AUTO_START=0` и `RAE_OLLAMA_AUTO_START=0`.

## ⚠️ Чего пост не сказал

**Нужен ключ API.** Для режима по умолчанию — обязательно. Бесплатно только если сознательно переключиться на OpenCode или Ollama.

**Сгенерированный код надо читать.** Прямая цитата из Caveats: *«Generated code runs locally via Claude Code, so review before executing»*. На сайте проекта шаг **Review** вообще вынесен в схему работы наравне с Browse, Capture и Generate.

**Сайты с защитой от ботов сломают захват.** Второй caveat авторов. Для чего-нибудь за Cloudflare или с поведенческой антибот-защитой ручной режим станет обязательным, а может не сработать вовсе.

**C требует POSIX-тулчейна.** Из документации: нужен `cc` и заголовки libcurl — то есть macOS/Linux либо WSL/MSYS2 на Windows. Для остальных восьми языков ограничений нет.

> [!caution] Правовая сторона, коротко
> Приватный API сайта — не публичный интерфейс. Его использование почти всегда противоречит пользовательскому соглашению, а нагрузка на неанонсированные эндпоинты легко тянет на злоупотребление. Инструмент нейтрален, но перед тем как строить что-то на сгенерированном клиенте, стоит посмотреть ToS сайта и наличие официального API. Похожая оговорка разбиралась в заметке про [Lightpanda](Lightpanda%20%E2%80%94%20headless-%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%20%D0%BD%D0%B0%20Zig%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B8%20%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%D0%BE%D0%B2%2C%20AGPL%2C%20robots.txt%2C%20%D1%87%D0%B5%D0%B3%D0%BE%20%D0%BD%D0%B5%D1%82%29.md).

## 💻 На твоих системах

Обычный Python-пакет, ставится в пользовательское окружение.

| Система | Что нужно |
| :--- | :--- |
| **Gentoo** (основная) | Python 3.11+ есть (у тебя 3.14), `emerge dev-python/uv`, затем `uv tool install reverse-api-engineer`. Для agent-режима нужен `net-libs/nodejs` (20+) под `npx`. Ручной режим — доп-экстра плюс `playwright install chromium` |
| **Debian / Ubuntu** | Системный pip заблокирован (PEP 668): `pipx install reverse-api-engineer` либо `uv tool install`. Node.js из NodeSource |
| **Arch** | `pacman -S uv nodejs`, дальше `uv tool install reverse-api-engineer` |
| **Entware / RT-AX56U** | ❌ Неприменимо — нужен браузер и Playwright |

## 💡 Итог

- Инструмент рабочий, MIT, за ним стоит **верифицированная компания** Notte, которая делает браузерную инфраструктуру для агентов. Это не однодневка, в отличие от [ScraperAI](ScraperAI%20%E2%80%94%20%D0%98%D0%98-%D0%BF%D0%B0%D1%80%D1%81%D0%B5%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2%20%D0%BF%D0%BE%20%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B7%D0%B0%D0%B1%D1%80%D0%BE%D1%88%D0%B5%D0%BD%20%D1%81%202024%2C%20pip%20%D0%BD%D0%B5%20%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%81%D1%8F%2C%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20OpenAI%29.md), который в базе уже разобран как заброшенный.
- Список возможностей в посте **совпал почти дословно** — редкий случай. Девять языков перечислены точно.
- Единственная фактическая неточность: **Ollama не самостоятельный SDK**, а провайдер внутри OpenCode.
- Умолчано главное для практики: **нужен ключ API**, **код надо ревьюить перед запуском**, **сайты с антиботом не поддадутся**, а ссылка ведёт на переехавший репозиторий.
- Подход честный: не «ИИ понимает сайт», а «пишем HAR и генерируем клиент по реальным запросам». Это воспроизводимо и проверяемо руками.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/27203](https://t.me/bugnotfeature/27203) (20.08.2026)
- Проект: [GitHub (актуальный адрес)](https://github.com/nottelabs/reverse-api-engineer) · [reverseapi.dev](https://reverseapi.dev) · [PyPI](https://pypi.org/project/reverse-api-engineer/)
- Компания: [Notte](https://www.notte.cc/) · [notte — их основной проект](https://github.com/nottelabs/notte)
- Связанные: [ScraperAI — как выглядит заброшенный аналог](ScraperAI%20%E2%80%94%20%D0%98%D0%98-%D0%BF%D0%B0%D1%80%D1%81%D0%B5%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2%20%D0%BF%D0%BE%20%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B7%D0%B0%D0%B1%D1%80%D0%BE%D1%88%D0%B5%D0%BD%20%D1%81%202024%2C%20pip%20%D0%BD%D0%B5%20%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%81%D1%8F%2C%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20OpenAI%29.md) · [Lightpanda — headless-браузер для парсинга](Lightpanda%20%E2%80%94%20headless-%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%20%D0%BD%D0%B0%20Zig%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B8%20%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%D0%BE%D0%B2%2C%20AGPL%2C%20robots.txt%2C%20%D1%87%D0%B5%D0%B3%D0%BE%20%D0%BD%D0%B5%D1%82%29.md) · [Cua Driver — computer use для агентов](Cua%20Driver%20%E2%80%94%20%D1%84%D0%BE%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D0%B5%D1%80%20%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28computer%20use%2C%20MCP%29.md) · [MCP — серверы Model Context Protocol](MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md)

#AI #Агенты #Парсинг #API #Playwright #Python
