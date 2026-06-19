---
создал заметку: 2026-06-16T13:00:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - LocalLLM
  - llama_cpp
  - GGUF
  - OpenSource
Источник:
  - https://github.com/ggml-org/llama.cpp
---

# 🦙 llama.cpp — движок локального инференса GGUF

**llama.cpp** ([ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)) — низкоуровневый движок для запуска LLM **локально** на CPU и/или GPU. Написан на C/C++ (библиотека `ggml`), без Python-зависимостей, минимум накладных расходов. Это **фундамент**, на котором построены [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md) и [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md) — если нужен максимальный контроль и минимальный оверхед, работают прямо с ним.

> [!info] GGUF — «родной» формат
> llama.cpp использует формат **GGUF** (единый файл: веса + метаданные + токенизатор) с квантизацией (Q2…Q8, а также f16). Именно в GGUF раздают модели вроде [Gemma 4 12B Coder](../Model/Gemma%204%2012B%20Coder%20%E2%80%94%20локальный%20файнтюн%20на%20ризонинге%20Fable%205%20%28GGUF%29.md). Конвертация HF→GGUF — скриптом `convert_hf_to_gguf.py`, квантизация — `llama-quantize`.

## 🧰 Основные бинарники

| Бинарник | Назначение |
| :--- | :--- |
| **`llama-cli`** | интерактивный чат / запуск промпта из консоли |
| **`llama-server`** | HTTP-сервер с **OpenAI-совместимым API** (порт по умолчанию **8080**) |
| **`llama-bench`** | бенчмарк скорости (tok/s) под разные параметры |
| **`llama-quantize`** | квантизация GGUF (f16 → Q4_K_M и т.п.) |
| **`llama-perplexity`** | замер качества (perplexity) на тексте |
| `convert_hf_to_gguf.py` | конвертация моделей Hugging Face → GGUF |

## 🖥️ Бэкенды (ускорители)

CPU (по умолчанию), **CUDA** (NVIDIA), **HIP/ROCm** (AMD), **Vulkan** (любой GPU), **Metal** (Apple Silicon), **SYCL** (Intel GPU), OpenCL (Adreno), плюс BLAS/MUSA/CANN и др. Бэкенд выбирается **флагом на этапе сборки** (`-DGGML_CUDA=ON`, `-DGGML_VULKAN=ON`, `-DGGML_HIPBLAS=ON`).

## 📦 Установка

### Gentoo

В основном дереве Portage пакета нет. Варианты:

```bash
# Оверлей GURU
eselect repository enable guru && emaint sync -r guru
emerge --ask llama-cpp

# Либо сборка из исходников (надёжный путь, см. ниже)
```

### Debian / Ubuntu

Официального пакета нет — собираем из исходников или берём готовый релиз с GitHub:

```bash
sudo apt install -y build-essential cmake libcurl4-openssl-dev git
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build -DGGML_CUDA=ON     # без NVIDIA — убери флаг (будет CPU)
cmake --build build -j --config Release
# бинарники появятся в build/bin/
```

### Arch

В официальных репозиториях **нет** — только AUR:

```bash
yay -S llama.cpp                  # CPU
# варианты под GPU:
yay -S llama.cpp-cuda             # NVIDIA
yay -S llama.cpp-vulkan           # любой GPU через Vulkan
```

### Entware (ASUS RT-AX56U, armv7, 512 МБ RAM)

> [!warning] Технически можно, практически — только крошечные модели
> llama.cpp **компилируется** под ARM, но 512 МБ RAM на роутере хватит лишь на модели **0.5B–1.5B** в сильной квантизации (Q4) и при крошечном контексте. 7B+ не запустить. Для роутера это скорее эксперимент; серьёзный инференс — на десктопе/сервере, а на роутер ставить разве что лёгкий прокси к нему.
> ```bash
> opkg install gcc make cmake git-http
> git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
> cmake -B build -DGGML_NATIVE=OFF && cmake --build build -j2
> ```

## 🚀 Использование

```bash
# Интерактивный чат; модель скачается с Hugging Face по -hf (или укажи путь к .gguf)
llama-cli -hf yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF:Q4_K_M

# Запуск локальной модели по пути
llama-cli -m ./models/model-Q4_K_M.gguf -p "Напиши быструю сортировку на Python"

# OpenAI-совместимый сервер на :8080
llama-server -m ./models/model-Q4_K_M.gguf --ctx-size 8192 --port 8080 \
  -ngl 999          # выгрузить все слои на GPU (если собран с CUDA/Vulkan)
```

Проверка сервера (тот же формат, что у OpenAI):

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"привет"}]}'
```

> [!tip] Ключевые флаги
> `-ngl N` — сколько слоёв на GPU (999 = все; 0 = чистый CPU). `--ctx-size` / `-c` — размер контекста (больше → больше RAM на KV-кэш). `-t N` — число потоков CPU. `--host 0.0.0.0` — слушать по сети (осторожно: открывает доступ извне).

## 🔌 Подключение к инструментам

`llama-server` даёт `/v1/chat/completions` — его можно прокинуть в общий стек через [LiteLLM](../ProxyLLM/LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md) и дёргать из агентов / [Claude Code](../Claude%20Code%20%E2%80%94%20гайд.md)-совместимых клиентов.

## ⚖️ llama.cpp vs Ollama vs LM Studio

| | llama.cpp | [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md) | [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md) |
| :--- | :--- | :--- | :--- |
| Уровень | низкий, ручной | удобная обёртка/CLI | десктоп-GUI |
| Контроль | **максимальный** | средний | минимальный |
| Под капотом | — | llama.cpp | llama.cpp / MLX |
| Кому | хочу всё настроить сам | «поставил и работает» | визуально, мышкой |

## 💡 Когда выбирать

- Нужен **максимальный контроль** над флагами, квантизацией, оффлоадом на GPU.
- Минимум зависимостей (один бинарник), сервер/embedded, скрипты, CI.
- Хочешь **сам квантизовать** модель из HF (`convert_hf_to_gguf.py` + `llama-quantize`).
- Если хочется «просто запустить» — проще [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md).

## 🔗 Ссылки

- Репозиторий: [github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
- Связанные: [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md) · [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md) · [Gemma 4 12B Coder (GGUF)](../Model/Gemma%204%2012B%20Coder%20%E2%80%94%20локальный%20файнтюн%20на%20ризонинге%20Fable%205%20%28GGUF%29.md) · [LiteLLM — шлюз к LLM](../ProxyLLM/LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md)

#AI #LLM #LocalLLM #llama_cpp #GGUF #OpenSource
