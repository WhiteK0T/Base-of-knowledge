---
создал заметку: 2026-06-16T13:20:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - LocalLLM
  - LM_Studio
  - GGUF
Источник:
  - https://lmstudio.ai
---

# 🖥️ LM Studio — десктоп-GUI для локальных LLM

**LM Studio** ([lmstudio.ai](https://lmstudio.ai)) — настольное приложение (GUI) для запуска локальных LLM «мышкой»: поиск и скачивание моделей из Hugging Face прямо в интерфейсе, чат, и встроенный **локальный сервер с OpenAI-совместимым API**. Под капотом — те же движки [llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) (GGUF) и MLX (на Apple Silicon). Самый простой вход для тех, кому не хочется в консоль.

> [!warning] Проприетарное, но бесплатное; десктоп x86_64
> LM Studio — **закрытое** приложение (бесплатно для личного использования; для коммерции — свои условия), в отличие от открытых [llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md)/[Ollama](Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md). Это **десктопный** продукт (Windows / macOS / Linux **x86_64**, Linux — AppImage). **GUI обязателен** для первичной настройки; чисто headless-сервер — не его сценарий (для сервера бери llama.cpp/Ollama).

## ✨ Что умеет

- **Поиск и загрузка** GGUF-моделей из Hugging Face во встроенном браузере (с подсказкой, какой квант влезет в твою память).
- **Чат** с моделью, пресеты параметров (температура, контекст, системный промпт).
- **Локальный сервер** — поднимает OpenAI-совместимый эндпоинт одним переключателем.
- **RAG** «из коробки»: подкинуть документы в чат.
- **`lms`** — CLI-утилита для управления из терминала (загрузка моделей, запуск сервера).

## 📦 Установка

### Linux (Gentoo / Debian-Ubuntu / Arch) — AppImage

Единый способ для всех десктоп-дистрибутивов — официальный **AppImage** с сайта (отдельного пакета в Portage/apt/pacman нет):

```bash
# скачать .AppImage с lmstudio.ai, затем:
chmod +x LM-Studio-*.AppImage
./LM-Studio-*.AppImage
```

> [!note] Зависимости AppImage
> Нужен FUSE для запуска AppImage (`sys-fs/fuse` на Gentoo, `libfuse2` на Debian/Ubuntu, `fuse2` на Arch). Требуется x86_64-десктоп с GUI; на сервере без графики смысла нет.

### Windows / macOS

Установщик с [lmstudio.ai](https://lmstudio.ai) (на Mac — нативная сборка с поддержкой **MLX** для Apple Silicon, заметно быстрее GGUF на этих чипах).

### Entware / роутер

> [!danger] Неприменимо
> LM Studio — графическое x86_64-приложение. На ASUS RT-AX56U (armv7, без GUI) **не запускается в принципе**. Для роутера это не вариант ни в каком виде.

## 🔌 Локальный сервер (OpenAI API)

В разделе **Developer / Local Server** включаешь сервер (по умолчанию порт **1234**):

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"local-model","messages":[{"role":"user","content":"привет"}]}'
```

Или через CLI:

```bash
lms server start            # поднять сервер
lms ls                      # список загруженных моделей
lms load <model>            # загрузить модель в память
```

Эндпоинт совместим с OpenAI → подключается через [LiteLLM](../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md) к агентам / [Claude Code](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)-совместимым клиентам.

## ⚖️ Сравнение

| | [llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) | [Ollama](Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) | LM Studio |
| :--- | :--- | :--- | :--- |
| Интерфейс | CLI/сервер | CLI/сервер | **GUI** + сервер |
| Лицензия | Open (MIT) | Open (MIT) | **проприетарное** (free) |
| Порог входа | высокий | низкий | **самый низкий** |
| Headless-сервер | да | да | не основной сценарий |
| Подбор кванта под RAM | вручную | авто | **визуально, с подсказкой** |

## 💡 Когда выбирать

- Хочешь **визуально** искать/пробовать модели, сравнивать кванты, не трогая консоль.
- Нужен быстрый локальный OpenAI-эндпоинт + чат + RAG в одном окне.
- На **Apple Silicon** — поддержка MLX даёт хорошую скорость.
- Для сервера/автоматизации/CI — лучше [llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) или [Ollama](Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) (открытые, headless, легче автоматизировать).

## 🔗 Ссылки

- Сайт: [lmstudio.ai](https://lmstudio.ai)
- Связанные: [llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) · [Ollama](Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) · [Gemma 4 12B Coder (GGUF)](../Model/Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md) · [LiteLLM — шлюз к LLM](../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md)

#AI #LLM #LocalLLM #LM_Studio #GGUF
