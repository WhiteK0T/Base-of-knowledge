---
создал заметку: 2026-07-23T14:40:00
author: WhiteK0T
tags:
  - AI
  - LocalLLM
  - AwesomeList
  - Каталог
  - Ollama
  - llama_cpp
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/26461
  - https://github.com/0xSojalSec/LLMs-local
---

# 📚 LLMs-local — awesome-каталог всего для локального запуска ИИ

**LLMs-local** ([github.com/0xSojalSec/LLMs-local](https://github.com/0xSojalSec/LLMs-local)) — **курируемый список (awesome-list)** ссылок на всё, что нужно, чтобы запускать нейросети **локально, на своём ПК**: движки инференса, оболочки, модели, ИИ-агенты, RAG, железо и гайды. Это не программа и не документация, а **навигатор-указатель** по экосистеме локальных LLM: один длинный README (~54 КБ) со ссылками, разбитыми по категориям. ~1000★, создан в декабре 2025, последнее обновление — июнь 2026.

> [!warning] Отделяем факты от рекламы поста
> Пост называет это «настоящей александрийской библиотекой» и обещает, что «больше ни один источник не нужен». По факту:
> | Заявление | Реально |
> | :--- | :--- |
> | «вся инфа по локальному ИИ тут» | это **список ссылок**, а не сами гайды/доки. Он приведёт к нужным репозиториям/статьям, но читать и разбираться — по первоисточникам |
> | «больше ничего не нужно» | awesome-list полезен как **карта/стартовая точка**, но не заменяет официальную документацию инструментов |
> | подборка всегда актуальна | зависит от **сопровождения**: в любых awesome-list со временем появляются мёртвые ссылки и устаревшие проекты — проверяй даты и звёзды |
> | это авторский труд | контент реальный и структурированный, но у аккаунта много агрегированных списков; **у репозитория нет лицензии** (формально «все права защищены») — это просто ссылки, не код для переиспользования |

## 🗂️ Что внутри (разделы каталога)

Категории README совпадают с тем, что перечислил пост:

- **Inference platforms** — [LM Studio](LM%20Studio%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF-GUI%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md), Jan, [LocalAI](https://github.com/mudler/LocalAI), ChatBox, lemonade.
- **Inference engines** — [Ollama](Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md), [llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md), vLLM, exo и др.
- **User Interfaces** — Open WebUI, Lobe Chat, ChatBox и прочие оболочки.
- **Large Language Models** — эксплореры/бенчмарки/лидерборды, провайдеры моделей и конкретные модели по назначению: general purpose, **coding**, multimodal, **image / audio**, прочее.
- **Tools** — модели-утилиты, **agent frameworks**, **[MCP](../MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md)** (Model Context Protocol), **RAG**, **coding agents** (альтернативы Cursor/Copilot), **computer use**, **browser automation**, memory management, тестирование/оценка/observability, research, **training & fine-tuning**.
- **Hardware** — калькуляторы RAM/VRAM, сборки ПК, советы по видеокартам.
- **Tutorials** — модели, prompt/context engineering, инференс, агенты, RAG и разное.
- **Communities** — где спрашивать.

## 🧭 Как использовать с пользой

- Как **точку входа**: нужно «чем запустить модель локально» — идёшь в Inference engines/platforms, а не гуглишь наугад.
- Как **чеклист областей**: увидеть, что помимо запуска есть RAG, память, агенты, computer use — и не пропустить целый пласт.
- **Не как истину в последней инстанции**: перешёл по ссылке → смотри звёзды, дату последнего коммита, лицензию и живость проекта сам.
- Многие пункты уже разобраны отдельными заметками в этом хранилище (ниже) — там факты уже сверены и адаптированы под системы владельца.

## 🖥️ Применимость на системах владельца

| Система | Применимо |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ — десктопы для локального инференса; каталог ведёт к [Ollama](Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)/[llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md)/[LM Studio](LM%20Studio%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF-GUI%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md). Раздел Hardware (VRAM/сборки) — прямо для подбора железа |
| **Entware / RT-AX56U** | ❌ — 512 МБ RAM и armv7 не тянут полноценные LLM; роутер годится максимум под лёгкие эмбеддинг/утилиты, но не под то, о чём этот каталог. Сам список читать можно откуда угодно |

## 🔗 Что из этого каталога уже есть отдельными заметками

- Движки/платформы: [Ollama — менеджер и сервер локальных LLM](Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) · [llama.cpp — движок инференса GGUF](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) · [LM Studio — десктоп-GUI](LM%20Studio%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF-GUI%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) · [MTP-ускорение в llama.cpp](MTP-%D1%83%D1%81%D0%BA%D0%BE%D1%80%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B2%20llama.cpp%20%28Qwen3.6%2027B%29%20%E2%80%94%20%D1%82%D1%8E%D0%BD%D0%B8%D0%BD%D0%B3%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20%28--fit%2C%20vLLM%2C%20%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D1%8B%29.md)
- Готовые студии: [LocallyUncensored — локальная AI-студия](LocallyUncensored%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20AI-%D1%81%D1%82%D1%83%D0%B4%D0%B8%D1%8F%20%28%D1%87%D0%B0%D1%82%2C%20%D0%BA%D0%BE%D0%B4%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%29.md)
- Инфраструктура: [MCP — серверы Model Context Protocol](../MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) · [Сводная таблица AI-агентов для программирования](../%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B8%D1%8E%D0%BD%D1%8C%202026%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/0xSojalSec/LLMs-local](https://github.com/0xSojalSec/LLMs-local)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26461)

#AI #LocalLLM #AwesomeList #Каталог #Ollama #Инструменты
