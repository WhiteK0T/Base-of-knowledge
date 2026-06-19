---
создал заметку: 2026-06-16T13:10:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - LocalLLM
  - Ollama
  - GGUF
  - OpenSource
Источник:
  - https://ollama.com
  - https://github.com/ollama/ollama
---

# 🐑 Ollama — менеджер и сервер локальных LLM

**Ollama** ([ollama.com](https://ollama.com)) — удобная обёртка над [llama.cpp](llama.cpp%20%E2%80%94%20движок%20локального%20инференса%20GGUF.md), которая превращает запуск локальных моделей в «`ollama run` — и работает». Берёт на себя **скачивание, хранение, квантизацию по умолчанию и запуск фонового сервера** с OpenAI-совместимым API. Золотая середина между ручным llama.cpp и GUI [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md).

> [!info] Что даёт поверх llama.cpp
> Реестр моделей (`ollama pull gemma`), управление версиями/тегами, авто-выбор кванта под железо, фоновый демон (`ollama serve`), `Modelfile` для кастомизации (системный промпт, параметры), горячая выгрузка/загрузка моделей из памяти.

## 📦 Установка

### Gentoo

```bash
# Оверлей GURU
eselect repository enable guru && emaint sync -r guru
emerge --ask app-misc/ollama
rc-update add ollama default && rc-service ollama start   # OpenRC
```

### Debian / Ubuntu

```bash
curl -fsSL https://ollama.com/install.sh | sh   # ставит бинарь + systemd-юнит
systemctl enable --now ollama
```

### Arch

В официальном **extra** (несколько вариантов под ускоритель):

```bash
sudo pacman -S ollama          # CPU
sudo pacman -S ollama-cuda     # NVIDIA
sudo pacman -S ollama-rocm     # AMD
sudo pacman -S ollama-vulkan   # любой GPU через Vulkan
sudo systemctl enable --now ollama
```

### Entware (ASUS RT-AX56U)

> [!warning] На роутер не ставим
> Ollama — Go-бинарник, тянет за собой раннеры llama.cpp; под armv7 с **512 МБ RAM** это непрактично (нет лёгкого пакета в opkg, и память не позволит держать даже мелкую модель + демон). Правильный паттерн: Ollama крутится на **десктопе/сервере**, а к нему обращаются по сети (см. `OLLAMA_HOST` ниже).

## 🚀 Использование

```bash
ollama run gemma3              # скачать (если нет) и начать чат
ollama pull qwen3:8b           # только скачать
ollama list                    # что установлено
ollama ps                      # что сейчас в памяти
ollama rm qwen3:8b             # удалить
ollama show gemma3             # параметры модели
```

### Запуск GGUF с Hugging Face напрямую

```bash
ollama run hf.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF:Q4_K_M
```

### Modelfile (своя конфигурация)

```dockerfile
FROM gemma3
PARAMETER temperature 0.2
PARAMETER num_ctx 8192
SYSTEM "Ты лаконичный ассистент по Python."
```

```bash
ollama create my-coder -f Modelfile && ollama run my-coder
```

## 🔌 API (OpenAI-совместимый)

Демон слушает **`127.0.0.1:11434`**. Есть и нативный, и OpenAI-совместимый эндпоинт:

```bash
# нативный
curl http://localhost:11434/api/generate -d '{"model":"gemma3","prompt":"привет"}'

# OpenAI-совместимый — /v1/chat/completions
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma3","messages":[{"role":"user","content":"привет"}]}'
```

> [!tip] Доступ по сети и переменные
> `OLLAMA_HOST=0.0.0.0:11434` — слушать на всех интерфейсах (тогда с других машин: `OLLAMA_HOST=http://server-ip:11434 ollama run ...`). `OLLAMA_MODELS` — каталог хранения моделей (удобно вынести на большой диск/USB). `OLLAMA_KEEP_ALIVE` — сколько держать модель в RAM после запроса.

Через [LiteLLM](../ProxyLLM/LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md) Ollama легко включается в общий стек агентов / [Claude Code](../Claude%20Code%20%E2%80%94%20гайд.md)-совместимых клиентов.

## ⚠️ На что обратить внимание

> [!warning] Квант по умолчанию и доступ извне
> По умолчанию `ollama run <model>` тянет квант **примерно Q4** — для качества можно указать тег явно (`:q6_K`, `:q8_0`) или взять GGUF с HF. И помни: открыв `OLLAMA_HOST=0.0.0.0`, ты выставляешь модель в сеть **без аутентификации** — только в доверенной сети или за реверс-прокси с авторизацией.

## 💡 Когда выбирать

- Хочешь «**поставил и работает**», но из консоли/скриптов, с фоновым сервером.
- Нужен простой реестр моделей и быстрый OpenAI-эндпоинт для агентов.
- Нужен полный контроль над флагами/квантизацией → [llama.cpp](llama.cpp%20%E2%80%94%20движок%20локального%20инференса%20GGUF.md). Нужен GUI → [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md).

## 🔗 Ссылки

- Сайт: [ollama.com](https://ollama.com) · репозиторий: [github.com/ollama/ollama](https://github.com/ollama/ollama) · реестр моделей: [ollama.com/library](https://ollama.com/library)
- Связанные: [llama.cpp](llama.cpp%20%E2%80%94%20движок%20локального%20инференса%20GGUF.md) · [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md) · [Gemma 4 12B Coder (GGUF)](../Model/Gemma%204%2012B%20Coder%20%E2%80%94%20локальный%20файнтюн%20на%20ризонинге%20Fable%205%20%28GGUF%29.md) · [LiteLLM — шлюз к LLM](../ProxyLLM/LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md)

#AI #LLM #LocalLLM #Ollama #GGUF #OpenSource
