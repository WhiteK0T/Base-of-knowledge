---
создал заметку: 2026-06-09T12:00:00
author: WhiteK0T
tags:
  - LiteLLM
  - LLM
  - Proxy
  - Gateway
  - AI
Источник:
  - https://www.litellm.ai/
  - https://github.com/BerriAI/litellm
  - https://docs.litellm.ai/
---

# 🔀 LiteLLM — единый шлюз (proxy) к 100+ LLM

[**LiteLLM**](https://github.com/BerriAI/litellm) (BerriAI, лицензия **MIT**, ~49.7k★) — open-source **AI-шлюз (LLM Gateway)**, который даёт доступ к **100+ провайдерам LLM** (OpenAI, Anthropic, Azure, Bedrock, Gemini, а также локальным — Ollama, **LM Studio**, vLLM) через **единый OpenAI-совместимый API**. Любой запрос приводится к формату OpenAI, поэтому клиенту не нужно знать, какой провайдер стоит за моделью.

Поставляется в двух видах:

| Форма | Что это | Когда |
| :--- | :--- | :--- |
| **Python SDK** (`pip install litellm`) | библиотека `litellm.completion(...)` прямо в коде | один скрипт/приложение |
| **Proxy Server / Gateway** (Docker) | отдельный сервис с `config.yaml`, слушает порт `4000` | команда/несколько клиентов, общий учёт и ключи |

## ✨ Зачем нужен (proxy)

- **Единая точка входа.** Один URL и формат OpenAI на все модели — меняешь бэкенд, не трогая клиентов.
- **Виртуальные ключи** (`virtual keys`) — выдаёшь ключи пользователям/командам, не светя реальные API-ключи провайдеров.
- **Учёт расходов и бюджеты** (spend tracking) с привязкой к ключу/юзеру/команде; лимиты **RPM/TPM**.
- **Надёжность:** балансировка нагрузки, ретраи, **fallback** между провайдерами при сбоях.
- **Observability:** логирование в Langfuse, MLflow, Arize Phoenix, Langsmith, OpenTelemetry.
- **Guardrails**, а в Enterprise — SSO/JWT/Audit Logs.

Среди пользователей OSS: Stripe, Netflix, Google ADK. Заявленная производительность proxy — `8ms P95 @ 1k RPS`.

## 🎛️ Подмена имён моделей (ключевой приём)

Главная фишка `config.yaml` — поле `model_name` это **публичный псевдоним**, который видит клиент, а `litellm_params.model` — реальный бэкенд. Это позволяет, например, **подсунуть локальную модель из LM Studio под именем `claude-haiku-4-5`** — и любой клиент, который умеет ходить в Claude/OpenAI-совместимый эндпоинт (Claude Code, IDE-плагины и т.п.), будет работать с локальной моделью, думая, что это облако.

> [!note] Префикс провайдера
> `model: lm_studio/<id-модели-в-LM-Studio>` — префикс `lm_studio/` говорит LiteLLM, как формировать запрос; `api_base` указывает на локальный сервер LM Studio (`/v1`). Для запроса из Docker-контейнера к хосту используется `host.docker.internal`.

> [!tip] `drop_params: true`
> Молча **выкидывает параметры, которые локальная модель не поддерживает** (вместо ошибки 400). Полезно, когда клиент шлёт OpenAI-специфичные поля, а LM Studio-модель их не понимает.

## ⚙️ Мой конфиг (`litellm-config.yaml`)

Два псевдонима: `claude-haiku-4-5` и `glm-5-turbo` — оба ведут на локальные модели в LM Studio. Закомментированный блок — запасной маппинг `glm-5-turbo` на другую модель.

```yaml
model_list:
  - model_name: claude-haiku-4-5
    litellm_params:
      model: lm_studio/google/gemma-4-26b-a4b
      api_base: http://host.docker.internal:1234/v1
      api_key: "sk-lm-wlADPi3J:HB7T1Lde9OZmcy2z0RmN"

#  - model_name: glm-5-turbo
#    litellm_params:
#      model: lm_studio/google/gemma-4-26b-a4b
#      api_base: http://host.docker.internal:1234/v1
#      api_key: "sk-lm-wlADPi3J:HB7T1Lde9OZmcy2z0RmN"
#      drop_params: true

  - model_name: glm-5-turbo
    litellm_params:
      model: lm_studio/qwen/qwen3.6-27b
      api_base: http://host.docker.internal:1234/v1
      api_key: "sk-lm-wlADPi3J:HB7T1Lde9OZmcy2z0RmN"
      drop_params: true
```

> [!warning] Ключи в конфиге
> В примере `api_key` — это токен **локального LM Studio**, не платный облачный ключ. Но в общем случае держи реальные ключи провайдеров вне репозитория (env-переменные `os.environ/...` или `.env`), а наружу выдавай виртуальные ключи LiteLLM.

## 🚀 Скрипт запуска (`run-litellm-proxy.sh`)

Поднимает proxy в Docker, монтирует конфиг только на чтение, публикует порт **только на localhost** (`127.0.0.1:4000`) и прокидывает `host.docker.internal` на адрес docker-моста, чтобы из контейнера достучаться до LM Studio на хосте.

```bash
#!/bin/bash

docker run -d \
  --name litellm-proxy \
  -v "/root/proxy/litellm-config.yaml:/app/config.yaml:ro" \
  -p 127.0.0.1:4000:4000 \
  --add-host=host.docker.internal:172.17.0.1 \
  ghcr.io/berriai/litellm:latest \
  --config /app/config.yaml
```

Разбор флагов:

| Флаг | Зачем |
| :--- | :--- |
| `-d` | запуск в фоне (detached) |
| `--name litellm-proxy` | имя контейнера |
| `-v ...:/app/config.yaml:ro` | монтируем конфиг внутрь, **read-only** |
| `-p 127.0.0.1:4000:4000` | порт наружу только на localhost (не торчит в сеть) |
| `--add-host=host.docker.internal:172.17.0.1` | алиас на хост (стандартный адрес docker0-моста) для доступа к LM Studio |
| `ghcr.io/berriai/litellm:latest` | официальный образ |
| `--config /app/config.yaml` | путь к смонтированному конфигу |

### Проверка и обслуживание

```bash
docker logs -f litellm-proxy          # смотреть логи
curl http://127.0.0.1:4000/v1/models  # список доступных моделей
docker restart litellm-proxy          # после правки конфига
docker rm -f litellm-proxy            # снести контейнер
```

## 🔌 Как обращаться

После старта эндпоинт OpenAI-совместимый — `http://127.0.0.1:4000`. Запрашиваешь модель по её псевдониму (`model_name`):

```bash
curl http://127.0.0.1:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-haiku-4-5",
    "messages": [{"role": "user", "content": "Привет!"}]
  }'
```

## 🔗 См. также

- [MCP — серверы Model Context Protocol](MCP%20%E2%80%94%20серверы%20Model%20Context%20Protocol.md)
- [Сводная таблица AI-агентов для программирования (июнь 2026)](Сводная%20таблица%20AI-агентов%20для%20программирования%20%28июнь%202026%29.md)
- [Claude Code — гайд](Claude%20Code%20%E2%80%94%20гайд.md)

#LiteLLM #LLM #Proxy #Gateway #AI
