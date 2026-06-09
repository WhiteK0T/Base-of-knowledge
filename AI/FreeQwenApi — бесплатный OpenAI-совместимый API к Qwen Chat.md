---
создал заметку: 2026-06-09T14:00:00
author: WhiteK0T
tags:
  - FreeQwenApi
  - Qwen
  - LLM
  - API
  - Proxy
  - AI
Источник:
  - https://github.com/y13sint/FreeQwenApi
---

# 🆓 FreeQwenApi — бесплатный OpenAI-совместимый API к Qwen Chat

[**FreeQwenApi**](https://github.com/y13sint/FreeQwenApi) — локальный **browser-based proxy**, который превращает обычный веб-аккаунт **Qwen Chat** (chat.qwen.ai) в локальный **OpenAI-совместимый API** на `http://localhost:3264/api`. Позволяет дёргать модели Qwen **без официального API-ключа DashScope/Alibaba** — из любого инструмента, который умеет в OpenAI-формат (LiteLLM, Open WebUI, Claude Code, свои скрипты).

> [!warning] Это не локальная модель и не официальный API
> Проект **автоматизирует браузер** (Chromium): ты логинишься в Qwen Chat, сессия сохраняется, а запросы проксируются на серверы Qwen под твоим аккаунтом. Отсюда вытекает:
> - **Нарушение ToS.** Автоматизация веб-аккаунта почти наверняка противоречит условиям использования Qwen Chat — аккаунт могут заблокировать. Используй на свой риск и только со своим аккаунтом.
> - **Не для продакшена.** Это «серое» reverse-engineering-решение, может сломаться при любом изменении на стороне Qwen.
> - **Секреты.** Токены сессии лежат в `session/` — **не коммить и не публикуй их**.
> - Лицензия в README явно не указана — проверь репозиторий перед использованием в своих проектах.

> [!note] Репозиторий — форк
> Это форк (в README клон-URL и водяной знак указывают на `ForgetMeAI` / `t.me/forgetmeai`). В ответах может присутствовать водяной знак `watermark: t.me/forgetmeai`.

## ⚙️ Как работает

1. `npm run auth` открывает браузер → ты логинишься в Qwen Chat.
2. Проект сохраняет токены сессии в `session/tokens.json` (и по аккаунтам в `session/accounts/*/token.txt`).
3. Поднимается локальный сервер на порту **3264**, который принимает запросы в формате OpenAI и форвардит их в Qwen, поддерживая авторизованную веб-сессию.
4. При нескольких аккаунтах — **автоматическая round-robin ротация** при упоре в лимиты.

## 🚀 Установка и запуск

Нужен **Node.js** (и Chrome/Chromium для авторизации).

```bash
git clone https://github.com/y13sint/FreeQwenApi
cd FreeQwenApi
npm install
npm run auth            # вход в Qwen Chat через браузер
npm run models:sync     # синхронизировать список моделей
SKIP_ACCOUNT_MENU=true npm start
```

Дополнительно:

```bash
npm run smoke           # smoke-тест
docker compose up --build -d   # запуск в Docker
```

Управление аккаунтами через флаги к `npm run auth`:

| Флаг | Действие |
| :--- | :--- |
| `--add` | добавить аккаунт |
| `--list` | список аккаунтов и их статусов (`OK` / `WAIT` / `INVALID`) |
| `--relogin` | перелогиниться (токен протух) |
| `--remove` | удалить аккаунт |

## 🤖 Модели

| Модель | Назначение |
| :--- | :--- |
| `qwen3.7-max` | обычный чат / агенты (по умолчанию) |
| `qwen3.7-plus` | быстрее и легче |
| `qwen3-coder-plus` | кодинг |
| `qwen3-vl-plus` | изображения/видео через Qwen Chat |
| `qwen3.6-plus` | ещё одна доступная модель |

## 🔌 Основные endpoints

| Метод | Путь | Назначение |
| :--- | :--- | :--- |
| `POST` | `/api/chat/completions` | чат (OpenAI-совместимый, поддержка `stream`) |
| `POST` | `/api/images/generations` | генерация изображений |
| `POST` | `/api/videos/generations` | генерация видео (с поллингом задачи) |
| `GET` | `/api/tasks/status/:taskId` | статус асинхронной задачи |
| `GET` | `/api/models` | список моделей |
| `GET` | `/api/health` · `/api/status` | здоровье / детальный статус |
| `GET` | `/api/images/status` · `/api/videos/status` | статус генерации |

### Примеры запросов

**Чат:**

```bash
curl http://localhost:3264/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.7-max",
    "messages": [
      {"role": "user", "content": "Ответь коротко: что такое FreeQwenApi?"}
    ],
    "stream": false
  }'
```

**Изображение:**

```bash
curl http://localhost:3264/api/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Кинематографичный робот в неоновом Токио, стиль sci-fi poster",
    "model": "qwen3-vl-plus",
    "size": "16:9"
  }'
```

**Видео (с ожиданием результата):**

```bash
curl http://localhost:3264/api/videos/generations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Камера медленно приближается к футуристическому городу ночью",
    "model": "qwen3-vl-plus",
    "size": "16:9",
    "wait": true
  }'
```

## 🧩 Интеграции

**LiteLLM / Claude Code** (см. [LiteLLM](LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md) — тот же приём с подменой `model_name`):

```yaml
model_list:
  - model_name: qwen3.7-max
    litellm_params:
      model: openai/qwen3.7-max
      api_base: http://localhost:3264/api
      api_key: dummy-key
```

**Open WebUI:** Base URL `http://localhost:3264/api`, API Key `dummy-key`, модель `qwen3.7-max` (в Docker — `http://host.docker.internal:3264/api`).

**Hermes Agent:**

```yaml
custom_providers:
  - name: qwen-free
    base_url: http://localhost:3264/api
    model: qwen3.7-max
    api_key: dummy-key
```

> API-ключ здесь любой (`dummy-key`) — авторизация идёт через сохранённую сессию Qwen, а не через ключ.

## 🔧 Ключевые переменные окружения (`.env.example`)

| Переменная | Дефолт | Назначение |
| :--- | :--- | :--- |
| `PORT` | `3264` | порт сервера |
| `HOST` | `0.0.0.0` | хост |
| `DEFAULT_MODEL` | `qwen3.7-max` | модель по умолчанию |
| `SKIP_ACCOUNT_MENU` | `false` | пропустить меню выбора аккаунта при старте |
| `NON_INTERACTIVE` | `false` | полностью неинтерактивный режим |
| `QWEN_RATELIMIT_HOURS` | `24` | срок блокировки токена при лимите |
| `MAX_RETRY_COUNT` | `3` | число повторов |
| `MAX_FILE_SIZE` | `10485760` | макс. размер файла (байт, 10 МБ) |
| `PAGE_POOL_SIZE` | `3` | пул вкладок браузера |
| `TASK_POLL_MAX_ATTEMPTS` / `TASK_POLL_INTERVAL` | `90` / `2000` | поллинг задач (попытки / интервал, мс) |
| `CHROME_PATH` | пусто | путь к Chrome/Chromium |
| `SESSION_DIR` / `UPLOADS_DIR` / `LOGS_DIR` | `session` / `uploads` / `logs` | каталоги |
| `LOG_LEVEL` | `info` | уровень логов |
| `QWEN_BASE_URL` | `https://chat.qwen.ai` | базовый URL Qwen |
| `DASHSCOPE_API_KEY` | пусто | ключ DashScope (опционально) |

Полный список таймаутов (`PAGE_TIMEOUT`, `AUTH_TIMEOUT`, `NAVIGATION_TIMEOUT` и т.д.) — в `.env.example`.

## 🔗 См. также

- [LiteLLM — единый шлюз (proxy) к 100+ LLM](LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md) — можно поставить перед FreeQwenApi для учёта/ротации
- [MCP — серверы Model Context Protocol](MCP%20%E2%80%94%20серверы%20Model%20Context%20Protocol.md)
- [Сводная таблица AI-агентов для программирования (июнь 2026)](Сводная%20таблица%20AI-агентов%20для%20программирования%20%28июнь%202026%29.md)

#FreeQwenApi #Qwen #LLM #API #Proxy #AI
