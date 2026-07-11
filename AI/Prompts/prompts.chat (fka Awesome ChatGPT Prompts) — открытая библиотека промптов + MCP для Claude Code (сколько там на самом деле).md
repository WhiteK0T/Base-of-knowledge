---
создал заметку: 2026-07-10T22:00:00
author: WhiteK0T
tags:
  - Prompt
  - LLM
  - ClaudeCode
  - MCP
  - OpenSource
Источник:
  - https://t.me/bugnotfeature/26348
  - https://github.com/f/prompts.chat
  - https://prompts.chat/
---

# 📚 prompts.chat (fka Awesome ChatGPT Prompts) — открытая библиотека промптов + MCP для Claude Code

[**prompts.chat**](https://prompts.chat/) ([f/prompts.chat](https://github.com/f/prompts.chat), автор **Fatih Kadir Akın / fka**) — бывший легендарный *Awesome ChatGPT Prompts*, теперь сайт-библиотека промптов с интеграцией в инструменты. Открытая, мультимодельная (ChatGPT, Claude, Gemini, Llama, Mistral). Лицензия двойная: **MIT** на код + **CC0 1.0** на сами промпты (можно брать и переделывать без ограничений).

> [!warning] «165 000 промптов» — это НЕ количество промптов
> Пост перепутал: **165 000+ — это звёзды на GitHub**, а не число запросов. Я скачал `prompts.csv` и посчитал: реально в библиотеке **~2008 промптов** (на 10.07.2026). Отличная, но **курируемая** коллекция на пару тысяч — а не «имба на 165 тысяч». Ошибка примерно в **80 раз**.

## 🧩 Что внутри

- **~2008 промптов** в `prompts.csv` со столбцами: `act` (роль/название), `prompt` (текст), `for_devs` (флаг «для разработчиков»), `type`, `contributor`.
- Классика «Act as …»: *Linux Terminal, English Translator, JavaScript Console, Excel Sheet, Job Interviewer* и т.д.
- Разделение на **dev / не-dev** (`for_devs`) и категории; на сайте — поиск и просмотр.
- Форматы: **сайт** [prompts.chat/prompts](https://prompts.chat/prompts), **`prompts.csv`**, **`PROMPTS.md`**, датасет на **Hugging Face**.
- Бонусы: интерактивный «*The Interactive Book of Prompting*» и «*Prompting for Kids*».

## 🔌 Интеграция с Claude Code (MCP)

Главная «фича» из поста — дёргать промпты по клику прямо из [Claude Code](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) через **MCP-сервер**:

- **Быстро:** `npx prompts.chat` (локальный MCP-сервер).
- **Удалённый MCP:** подключить эндпоинт `https://prompts.chat/api/mcp`.
- **Через маркетплейс плагинов** Claude Code.

После подключения промпты библиотеки становятся доступны агенту как инструменты/ресурсы — выбрал и применил, не копипастя вручную.

## 🏠 Своя приватная библиотека

Проект можно **self-host**: развернуть свою копию с приватными промптами, собственным брендингом/темой и аутентификацией — удобно для команды/организации, когда промпты не хочется держать в публичном облаке.

## ⚠️ Нюансы

> [!note] Community-контент → качество разное
> Это **краудсорс**: промпты присылает сообщество, качество и актуальность **варьируются**. Часть — родом из эпохи раннего ChatGPT и под современные модели (Claude Opus 4.8, GPT-5.5) может быть избыточной или устаревшей. Бери как **отправную точку** и адаптируй под свою модель/задачу. Зато **CC0** — использовать и править можно свободно.

## 🖥️ По системам

Веб-ресурс + датасет + MCP-сервер на Node — **ОС-агностично**. MCP работает в Claude Code на любом десктопе (Gentoo/Debian/Arch), нужен `node`/`npx`. На роутере **RT-AX56U** смысла нет (это не инференс, а библиотека промптов для десктопного агента). CSV/MD можно просто скачать и грепать локально где угодно.

## 🔗 Ссылки

- Сайт: [prompts.chat](https://prompts.chat/) · Репозиторий: [github.com/f/prompts.chat](https://github.com/f/prompts.chat) (MIT + CC0) · MCP: `npx prompts.chat` / `https://prompts.chat/api/mcp`
- Источник новости: [@bugnotfeature/26348](https://t.me/bugnotfeature/26348)
- Связанные: [Prompt library для Claude Code (официальная библиотека Anthropic)](Prompt%20library%20%D0%B4%D0%BB%D1%8F%20Claude%20Code%20%E2%80%94%20%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%BA%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82-%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D1%8B%20%28%D0%BE%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B0%20Anthropic%29.md) — официальный (кураторский) аналог против этого community-каталога

#Prompt #LLM #ClaudeCode #MCP #OpenSource
