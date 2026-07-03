---
создал заметку: 2026-07-03T15:00:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Промпты
  - Anthropic
  - Reference
Источник:
  - https://t.me/bugnotfeature/26224
  - https://code.claude.com/docs/en/prompt-library
---

# 📚 Prompt library — готовые промпты для Claude Code (официальная, Anthropic)

[**Prompt library**](https://code.claude.com/docs/en/prompt-library) — страница в официальной документации Anthropic с **копипаст-промптами именно для [Claude Code](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)** (агентного CLI), разложенными по **фазам разработки** (discover → build → ship) и **ролям** (разработчик, PM, дизайн, безопасность). Каждая карточка — готовый промпт со слотами-подстановками (`{path}`, `{behavior}` и т.п.) и ссылкой на **гайд-первоисточник**, откуда паттерн взят. Примеры: «дай обзор архитектуры этого кодбейса», «объясни, что делает `{path}` и как через него идут данные», «что сломается, если удалить `{target}`», «пройди по истории коммитов `{path}` и summary как он эволюционировал».

> [!info] Что внутри
> - **Категории:** Onboard/Understand (разобраться в незнакомом коде), сборка фич, отладка, ревью и безопасность, автоматизация рутины.
> - **Источники карточек:** это выжимка из уже существующих материалов Anthropic — [Common workflows](https://code.claude.com/docs/en/common-workflows), [Best practices](https://www.anthropic.com/engineering/claude-code-best-practices), «How Anthropic teams use Claude Code» (в т.ч. кейсы legal / marketing / cybersecurity) и гайда по масштабированию агентного кодинга.
> - **Формат:** промпт + слоты + тег фазы/роли + линк «откуда». Можно фильтровать по задаче и роли.

## 🧪 Факты против хайпа

> [!note] Это не «новый релиз», а собранная в одну страницу документация
> Пост подал это как «Anthropic **выкатили** библиотеку». На деле промпты **не новые** — это **курированная страница доков**, компилирующая паттерны из давно опубликованных гайдов Anthropic (workflows, best practices, кейсы команд). Ценность не в «свежести», а в том, что собрано в одном месте, отсортировано по фазам/ролям и снабжено ссылками на первоисточник. Как «стартовый набор, если не знаешь, с чего начать» — отлично; как «секретные новые промпты» — нет.

> [!caution] «БЕСПЛАТНЫЙ» — это просто документация; платно тут само использование Claude Code
> Все доки Anthropic бесплатны — акцент на «БЕСПЛАТНО» вводит в заблуждение. Промпты — это текст, который ты **вставляешь в Claude Code**; денег стоит **сам Claude Code** (подписка Claude или оплата API-токенов), а не список промптов. Библиотека полезна, только если у тебя уже есть где их запускать.

> [!warning] Это библиотека для Claude Code (кодинг), а не общая «библиотека промптов для Claude»
> Легко перепутать: у Anthropic **две разные** библиотеки.
> - **Эта** ([code.claude.com/.../prompt-library](https://code.claude.com/docs/en/prompt-library)) — под **Claude Code**, про работу с кодбейсом: онбординг, отладка, ревью, security-анализ изменений.
> - **Другая** ([общая Prompt Library](https://docs.anthropic.com/en/prompt-library) в доках API/Console) — ~60 промптов под **широкие задачи** (тексты, аналитика, роли-ассистенты), не про кодинг.
> Пост назвал её «библиотека промптов для Claude» — но ссылка ведёт именно на **кодинговую** (Claude Code). Если нужен общий копирайтинг/аналитика — смотри вторую.

> [!tip] Security-анализ здесь — это встроенная команда, а не просто промпт
> В разделе про безопасность фигурирует разбор изменений «на эксплуатируемые уязвимости». В Claude Code это оформлено как **встроенная slash-команда `/security-review`** (и есть GitHub Action), а не только копипаст-текст — то есть запускается штатно из сессии. Аналогично ревью кода — `/code-review`. Библиотека показывает, *как формулировать*, а часть сценариев уже зашита командами.

## 💻 Как это ложится на твои системы

Промпты — это просто текст; «применимость» = **там, где запущен Claude Code**. Сам Claude Code ставится через `npm i -g @anthropic-ai/claude-code` (нужен Node.js) и работает в терминале/IDE.

| Система | Применимость |
| :--- | :--- |
| **Gentoo** (основная) | ✅ Claude Code через npm (`net-libs/nodejs` + `npm i -g @anthropic-ai/claude-code`) → промпты из библиотеки вставляешь как есть |
| **Debian / Ubuntu** | ✅ Так же — Node.js + npm-установка Claude Code |
| **Arch** | ✅ Так же (`pacman -S nodejs npm`), затем Claude Code |
| **Entware / RT-AX56U** | **N/A** — Claude Code (Node-CLI, агентная работа с кодбейсом) на роутере с 512 МБ RAM не запускают; промпты негде применять |

## 💡 Кому полезно

- **Пользователям Claude Code** (в т.ч. тебе в этом репо): готовые формулировки под онбординг в чужой код, отладку, ревью и security-разбор — быстрый старт, когда «не знаю, что попросить».
- **Не** источник «тайных» промптов и **не** про общий копирайтинг — это кодинговые паттерны из гайдов Anthropic, собранные в одну шпаргалку.

## 🔗 Ссылки

- Библиотека: [code.claude.com/docs/en/prompt-library](https://code.claude.com/docs/en/prompt-library)
- Первоисточники: [Common workflows](https://code.claude.com/docs/en/common-workflows) · [Best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- Общая (не-кодинговая) [Prompt Library](https://docs.anthropic.com/en/prompt-library) в доках API
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26224)
- Связанные: [Claude Code — гайд](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [Claude Code — шпаргалка команд](Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) · [How to AI (сборник гайдов по Claude)](How%20to%20AI%20%28Ruben%20Hassid%29%20%E2%80%94%20%D1%81%D0%B1%D0%BE%D1%80%D0%BD%D0%B8%D0%BA%20%D0%B3%D0%B0%D0%B9%D0%B4%D0%BE%D0%B2%20%D0%BF%D0%BE%20Claude.md)

#AI #Claude_Code #Промпты #Anthropic #Reference
