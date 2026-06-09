---
создал заметку: 2026-06-09T15:00:00
author: WhiteK0T
tags:
  - FreeDeepseekAPI
  - DeepSeek
  - LLM
  - API
  - Proxy
  - AI
Источник:
  - https://github.com/ForgetMeAI/FreeDeepseekAPI
---

# 🐳 FreeDeepseekAPI — бесплатный OpenAI-совместимый API к DeepSeek

[**FreeDeepseekAPI**](https://github.com/ForgetMeAI/FreeDeepseekAPI) — локальный **browser-based proxy**, превращающий веб-аккаунт **DeepSeek Web Chat** (chat.deepseek.com) в локальный **OpenAI- и Anthropic-совместимый API** на `http://localhost:9655`. Позволяет дёргать модели DeepSeek **без официального API-ключа**, из любого инструмента под OpenAI/Anthropic-формат (LiteLLM, Open WebUI, **Claude Code**, OpenAI SDK).

Идейный «брат» проекта [FreeQwenApi](FreeQwenApi%20%E2%80%94%20бесплатный%20OpenAI-совместимый%20API%20к%20Qwen%20Chat.md) от того же автора (**ForgetMeAI**), но для DeepSeek и с более широким набором совместимых API.

> [!warning] Это не локальная модель и не официальный API
> Проект **автоматизирует браузер** (Chromium): ты логинишься в DeepSeek Chat, сессия сохраняется, запросы проксируются на серверы DeepSeek под твоим аккаунтом.
> - **Нарушение ToS.** Автоматизация веб-аккаунта почти наверняка противоречит условиям DeepSeek — аккаунт могут заблокировать. На свой риск и только со своим аккаунтом.
> - **Экспериментально.** Зависит от внутреннего веб-API DeepSeek; ломается при изменениях на их стороне.
> - **Секреты.** Креды лежат в `deepseek-auth.json` (нужны `token`, `cookie`, `wasmUrl`); на Unix права `0600`. **Не коммить и не публикуй.**

> [!note] Репозиторий
> `ForgetMeAI/FreeDeepseekAPI` — **самостоятельный проект** (не форк), создан в июне 2026, ~104★. Лицензия — **MIT** (файл `LICENSE` есть). Поддержка/анонсы — Telegram-канал `t.me/forgetmeai`.

## ✨ Чем отличается от FreeQwenApi

- **Три совместимых API сразу:** OpenAI (`/v1/chat/completions`), **Anthropic Messages** (`/v1/messages`) и **OpenAI Responses** (`/v1/responses`).
- **Reasoning** — модель-ризонер отдаёт отдельное поле `reasoning_content`.
- **Tool calling** в трёх форматах (OpenAI / Anthropic / Responses).
- **Sticky-сессии** по агенту (`x-agent-session`/`user`) — переиспользуют цепочку чата DeepSeek, с авто-восстановлением.
- **Zero-dependencies** (нет npm-зависимостей), нужен **Node.js 18+**.

## ⚙️ Как работает

1. `npm run auth` открывает браузер → вход в DeepSeek Chat в отдельном профиле Chrome.
2. Креды сохраняются в `deepseek-auth.json`.
3. Локальный сервер на порту **9655** принимает запросы в формате OpenAI/Anthropic и форвардит их в веб-API DeepSeek.
4. При нескольких аккаунтах — **round-robin ротация** с cooldown по аккаунту при лимитах (`429/401/403`).

## 🚀 Установка и запуск

Нужен **Node.js 18+** и Chrome/Chromium.

```bash
git clone https://github.com/ForgetMeAI/FreeDeepseekAPI.git
cd FreeDeepseekAPI
npm run auth     # вход в DeepSeek Chat через браузер
npm start        # запуск прокси на :9655
```

Доп. режимы и диагностика:

```bash
NON_INTERACTIVE=1 npm start   # без меню (VPS/CI)
npm run doctor                # диагностика
npm run test                  # тесты
```

## 🤖 Модели

| Алиас | Reasoning | Web Search |
| :--- | :---: | :---: |
| `deepseek-chat` | — | — |
| `deepseek-reasoner` | ✓ | — |
| `deepseek-chat-search` | — | ✓ |
| `deepseek-reasoner-search` | ✓ | ✓ |
| `deepseek-expert` | — | — |
| `deepseek-v4-pro` | ✓ | — |

## 🔌 Endpoints

| Метод | Путь | Назначение |
| :--- | :--- | :--- |
| `GET` | `/health` | статус сервера |
| `GET` | `/v1/models` | список алиасов моделей |
| `GET` | `/v1/model-capabilities` | полная карта моделей/возможностей |
| `POST` | `/v1/chat/completions` | чат (OpenAI-совместимый, stream/SSE) |
| `POST` | `/v1/messages` | shim под **Anthropic Messages API** |
| `POST` | `/v1/responses` | shim под **OpenAI Responses API** |
| `GET` | `/v1/sessions` | активные сессии |
| `POST` | `/reset-session?agent=<id>` | сброс сессии агента |

### Примеры запросов

**Чат:**

```json
POST /v1/chat/completions
{
  "model": "deepseek-chat",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}
```

**С рассуждением** (ответ содержит `reasoning_content` рядом с `content`):

```json
POST /v1/chat/completions
{
  "model": "deepseek-reasoner",
  "messages": [{"role": "user", "content": "Why is sky blue?"}],
  "stream": false
}
```

## 🧩 Интеграции

**Claude Code** (через Anthropic-shim — переменная окружения):

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:9655"
```

**Open WebUI:** Base URL `http://localhost:9655/v1` (в Docker — `http://host.docker.internal:9655/v1`).

**LiteLLM** (см. [LiteLLM](LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md)) — как обычный OpenAI-совместимый провайдер:

```yaml
model_list:
  - model_name: deepseek-reasoner
    litellm_params:
      model: openai/deepseek-reasoner
      api_base: http://localhost:9655/v1
      api_key: dummy-key
```

## 🔧 Ключевые переменные окружения

| Переменная | Назначение |
| :--- | :--- |
| `CHROME_PATH` | путь к Chrome/Chromium |
| `DEEPSEEK_AUTH_DIR` | каталог с несколькими auth-файлами (пул аккаунтов) |
| `DEEPSEEK_AUTH_PATH` | пути к auth-файлам через запятую |
| `DEEPSEEK_ACCOUNT_COOLDOWN_MS` | длительность cooldown аккаунта при лимите |
| `NON_INTERACTIVE=1` | без интерактивных меню (headless/CI) |
| `SKIP_ACCOUNT_MENU=1` | пропустить меню выбора аккаунта |

## 🔗 См. также

- [FreeQwenApi — бесплатный OpenAI-совместимый API к Qwen Chat](FreeQwenApi%20%E2%80%94%20бесплатный%20OpenAI-совместимый%20API%20к%20Qwen%20Chat.md) — аналог от того же автора, для Qwen
- [LiteLLM — единый шлюз (proxy) к 100+ LLM](LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md)
- [Сводная таблица AI-агентов для программирования (июнь 2026)](Сводная%20таблица%20AI-агентов%20для%20программирования%20%28июнь%202026%29.md)

#FreeDeepseekAPI #DeepSeek #LLM #API #Proxy #AI
