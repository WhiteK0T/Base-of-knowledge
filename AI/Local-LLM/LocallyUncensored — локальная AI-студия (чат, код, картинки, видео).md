---
создал заметку: 2026-06-16T17:00:00
author: WhiteK0T
tags:
  - AI
  - LocalLLM
  - LocallyUncensored
  - Abliteration
  - SelfHosted
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/25814
  - https://locallyuncensored.com/
  - https://github.com/PurpleDoubleD/locally-uncensored
---

# 🎛️ LocallyUncensored — локальная AI-студия (чат, код, картинки, видео)

**LocallyUncensored** ([locallyuncensored.com](https://locallyuncensored.com/), [github](https://github.com/PurpleDoubleD/locally-uncensored)) — десктопное приложение (Tauri/Rust), которое в одном окне собирает **локальный AI-стек**: чат, кодинг-агент, генерацию картинок и видео, RAG, голос (STT/TTS) и удалённый доступ. Само по себе **не модель и не движок** — это **фронтенд-оркестратор** поверх готовых бэкендов ([Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md), [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md), [llama.cpp](llama.cpp%20%E2%80%94%20движок%20локального%20инференса%20GGUF.md), vLLM, ComfyUI и др.). Лицензия **AGPL-3.0**, бесплатно.

> [!warning] Отделяем факты от рекламы поста
> Исходный пост приукрашивает. Сверка с сайтом/репозиторием:
> | Заявление из новости | Реально |
> | :--- | :--- |
> | «80+ моделей» | на витрине ~20 пресетов; моделей много только потому, что качаются **по запросу** через менеджер |
> | «Интеграция с Claude Code» | **не подтверждено** — ни на сайте, ни в README такого нет; есть свой «coding agent» с инструментами + MCP |
> | «Без цензуры» | это **abliterated-модели** (снятые safety-фильтры), а не магия — см. ниже |
> | «Удобный чат-интерфейс» | да, GUI-студия (Tauri), это правда |

## 🧬 Что это по фактам

| Параметр | Значение |
| :--- | :--- |
| Тип | десктоп-приложение (Tauri v2, Rust), **оркестратор** локальных бэкендов |
| Возможности | чат, кодинг-агент (+MCP), генерация **изображений и видео** (ComfyUI), RAG, vision, STT/TTS, remote-доступ |
| Локальные бэкенды | Ollama, LM Studio, vLLM, llama.cpp, KoboldCpp, LocalAI, Jan, GPT4All и др. |
| Облачные (опц.) | OpenAI, Anthropic, OpenRouter, Groq, DeepSeek, Mistral… (по API-ключам) |
| Лицензия | **AGPL-3.0**, бесплатно, без аккаунта |
| Платформы | **Windows 10/11** (основная), Linux — сборка из исходников; **macOS пока нет** |
| Требования | мин. **8 ГБ RAM**; GPU обязателен для картинок/видео |
| Активность | ~690★, версия v2.5.4 (15.06.2026) |

## 🔓 Что значит «uncensored» (abliteration)

«Без цензуры» здесь = по умолчанию подгружаются **abliterated-модели** — у них хирургически подавлен «вектор отказа», поэтому они почти не отказываются отвечать. Это та же техника, что в заметке [Heretic](../Heretic%20%E2%80%94%20снятие%20safety-ограничений%20с%20открытых%20LLM%20%28abliteration%29.md). Плюс — нет фильтрации на генерации изображений/видео.

> [!danger] Ответственность целиком на тебе
> Снятые предохранители не делают незаконное законным. Генерация противоправного контента (CSAM, дипфейки без согласия, инструкции для реального вреда) **нелегальна независимо от инструмента** и ведёт к реальной ответственности. Abliteration также **снижает качество** на «пограничных» запросах (модель честнее, но и охотнее галлюцинирует/выдаёт опасные неточности). Для рабочих задач это инструмент «на свой страх и риск», не для прод-сервиса.

## 📦 Установка

### Windows (основной путь)

Скачать `.exe`/`.msi` из [Releases](https://github.com/PurpleDoubleD/locally-uncensored/releases) и запустить. На первом старте **мастер** проверяет железо (GPU/VRAM), рекомендует модели по классам VRAM (≤10 ГБ / 10–16 ГБ / >16 ГБ) и предлагает доставить недостающие бэкенды (Ollama, ComfyUI) в один клик.

### Linux (Gentoo / Debian-Ubuntu / Arch) — сборка из исходников

Готовых пакетов нет: собираем Tauri-приложение (нужны **Rust**, **Node.js** и системные зависимости Tauri — `webkit2gtk`, `libappindicator` и т.п.).

```bash
git clone https://github.com/PurpleDoubleD/locally-uncensored
cd locally-uncensored
npm install
npm run tauri build      # бинарь; для отладки в браузере — npm run dev
```

Зависимости Tauri по дистрибутивам:

```bash
# Debian/Ubuntu
sudo apt install libwebkit2gtk-4.1-dev build-essential curl libssl-dev libayatana-appindicator3-dev librsvg2-dev
# Arch
sudo pacman -S webkit2gtk-4.1 base-devel curl openssl appmenu-gtk-module libappindicator-gtk3 librsvg
# Gentoo
emerge --ask net-libs/webkit-gtk dev-lang/rust nodejs
```

> [!note] macOS и роутер
> **macOS** официально пока не поддерживается. На **Entware/RT-AX56U** неприменимо: это тяжёлая GPU-студия с десктопным GUI — генерация картинок/видео требует видеокарты, роутеру тут делать нечего.

## ⚙️ Под капотом

LocallyUncensored сам ничего не считает — он **подключается к локальным движкам**. Текст обычно идёт через [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md) (или другой выбранный бэкенд), картинки/видео — через **ComfyUI**. Если у тебя уже стоят [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md)/[LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md), приложение их подхватит. По сути это удобная «оболочка-агрегатор» над тем, что описано в соседних заметках.

## 💡 Стоит ли смотреть

- **Да**, если хочется **единый GUI** на весь локальный AI-зоопарк (чат + код + картинки + видео) без ручной склейки бэкендов, и ты на Windows с нормальным GPU.
- **Скептически** к «80+ моделей» и «интеграции с Claude Code» — это маркетинг; реальная ценность в **оркестрации** существующих движков.
- **Осторожно** с «uncensored»: это abliteration со всеми её минусами (качество, безопасность) и юридическими рисками на тебе.
- Если нужен **контроль/headless/сервер** — бери движки напрямую: [llama.cpp](llama.cpp%20%E2%80%94%20движок%20локального%20инференса%20GGUF.md) / [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md), а UI — [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md).

## 🔗 Ссылки

- Сайт: [locallyuncensored.com](https://locallyuncensored.com/) · репозиторий: [github.com/PurpleDoubleD/locally-uncensored](https://github.com/PurpleDoubleD/locally-uncensored)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/25814)
- Связанные: [Heretic — abliteration](../Heretic%20%E2%80%94%20снятие%20safety-ограничений%20с%20открытых%20LLM%20%28abliteration%29.md) · [Ollama](Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md) · [LM Studio](LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md) · [llama.cpp](llama.cpp%20%E2%80%94%20движок%20локального%20инференса%20GGUF.md) · [Gemma 4 12B Coder (GGUF)](../Model/Gemma%204%2012B%20Coder%20%E2%80%94%20локальный%20файнтюн%20на%20ризонинге%20Fable%205%20%28GGUF%29.md)

#AI #LocalLLM #LocallyUncensored #Abliteration #SelfHosted #Инструменты
