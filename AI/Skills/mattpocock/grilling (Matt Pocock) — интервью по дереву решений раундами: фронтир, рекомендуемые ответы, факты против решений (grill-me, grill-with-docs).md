---
создал заметку: 2026-10-20T10:50:00
author: WhiteK0T
tags:
  - Скиллы
  - ИИ-агенты
  - Claude_Code
  - Промпты
  - Требования
Источник:
  - https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
  - https://github.com/mattpocock/skills/blob/main/docs/productivity/grilling.md
  - https://github.com/mattpocock/skills/blob/main/docs/productivity/grill-me.md
  - https://github.com/mattpocock/skills/blob/main/docs/engineering/grill-with-docs.md
  - https://github.com/mattpocock/skills/tree/main/.out-of-scope
---

# grilling (Matt Pocock) — интервью по дереву решений

> [!info] Что это
> **`grilling`** — скилл-«примитив» из [набора Matt Pocock](skills%20%28Matt%20Pocock%29%20%E2%80%94%2038%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BD%D0%B0%D1%81%D1%82%D0%BE%D1%8F%D1%89%D0%B8%D1%85%20%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%BE%D0%B2%3A%20grilling%2C%20%D0%B3%D0%BB%D0%BE%D1%81%D1%81%D0%B0%D1%80%D0%B8%D0%B9%20%D0%B8%20ADR%2C%20to-spec%20%D0%B8%20to-tickets%2C%20tdd%2C%20code-review%20%28~0%2C6k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%29.md): агент **безжалостно допрашивает** вас о плане, решении или идее, пока у вас не появится **общее понимание**, — и только потом что-то делает. На нём стоят самые популярные скиллы автора `/grill-me` и `/grill-with-docs`, а также `triage`, `wayfinder` и `improve-codebase-architecture`.
>
> Проблема, которую он решает: *«No-one knows exactly what they want»* (The Pragmatic Programmer). Агент делает не то не потому, что глуп, а потому, что вы не договорились.

**Размер:** 328 слов, ~430 токенов (на 20.10.2026). Его можно прочитать целиком за минуту — ниже он полностью.

## 1. Текст скилла

```markdown
---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user
  wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a
**design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are
already settled: the questions you can ask _now_ without guessing at answers you haven't
heard yet. Ask the whole frontier in one round: number each question and give your
recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including
multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - ...

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward
and unblock questions that depended on them. Recompute the frontier and ask the next round.
A question whose answer depends on another question still open in this round belongs to a
_later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from
the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the
user for anything you could look up yourself. Don't block on it: a running exploration is
an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to
report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them
and wait.

The session is done when the frontier is empty: every branch of the design tree visited,
nothing left silently assumed. Do not act on it until the user confirms you have reached a
shared understanding.
```

## 2. Как это работает

Три понятия:

| Понятие | Смысл |
| :--- | :--- |
| **Дерево решений** (design tree) | модель предмета: каждое решение тянет за собой зависимые |
| **Фронтир** (frontier) | все решения, чьи предпосылки уже приняты, — только их и можно спрашивать сейчас |
| **Раунд** (round) | весь фронтир, заданный целиком и целиком отвеченный |

- **Ни по одному вопросу, ни всё сразу.** Раунд — это весь фронтир, но вопрос, зависящий от ещё открытого вопроса этого же раунда, уходит в следующий. По словам документации, 13 вопросов обычно укладываются примерно в 3 раунда, а не в 13.
- **Формат раунда фиксирован:** номер и заголовок после `❓`, тело вопроса, рекомендуемый ответ отдельной строкой после `➡️`. Отвечать можно по номерам: «1 да, 2 второй вариант, 3 нет, потому что…».
- **«Да» = принять рекомендацию.** С октября 2026 вопрос формулируется так, чтобы «да» означало согласие с рекомендацией агента.
- **Факты — дело агента, решения — ваше.** Если вопросу нужен факт из окружения (файлы, инструменты), агент сам отправляет субагента выяснить и **не ждёт**: ждут только вопросы, которые от этого факта зависят. Решения агент обязан отдать вам и ждать ответа. Агент, который сам отвечает на свои вопросы-решения, **ломает скилл**.
- **Ворота подтверждения.** Сессия заканчивается, когда фронтир пуст, но **действовать нельзя**, пока вы не подтвердите общее понимание.

Пример одного раунда:

```
❓ **Q1** - **Хранилище**: держим состояние игры в памяти сервера или в SQLite?
Варианты: (а) память — проще, теряется при рестарте; (б) SQLite — переживает рестарт.

➡️ Память: игры короткие, рестарт сервера редкий. Берём память?

---

❓ **Q2** - **Кто клиент CLI**: живые игроки или скрипты для проверки сервера?

➡️ Скрипты: CLI нужен, чтобы гонять сервер без браузера. Так и есть?
```

## 3. Семейство скиллов

| Скилл | Кто вызывает | Что добавляет к `grilling` |
| :--- | :--- | :--- |
| **`grilling`** | агент сам (единственный в семье, кого модель может вызвать) или `/grilling` | чистое интервью — механизм |
| **`/grill-me`** | только человек | ничего: одна строка «Call the Skill tool with "grilling"». **Без состояния**: не пишет файлов, годится для чего угодно — бизнес-решение, текст, «что делать дальше» |
| **`/grill-with-docs`** | только человек | + `domain-modeling`: **пишет в репозиторий** — термины сразу в `GLOSSARY.md`, трудные решения в ADR (`docs/adr/`) |
| `triage` | человек | грилинг входящего issue, если его надо доработать (после проверки, что баг воспроизводится) |
| `wayfinder` | человек | грилинг внутри тикетов-решений большой многосессионной карты; сначала — «назвать пункт назначения» |
| `improve-codebase-architecture` | человек | грилинг по выбранной возможности «углубить» модуль: ограничения, зависимости, форма модуля, что переживут тесты |

> `grill-me` и `grill-with-docs` — однострочные обёртки. Установили только их — **ничего не работает**: нужен `grilling` (а для `grill-with-docs` ещё и `domain-modeling`). Ставьте набор целиком или вместе с примитивами.

### Что оставляет grill-with-docs

| Что решено | Куда попадает |
| :--- | :--- |
| Термин проекта | `GLOSSARY.md` — **сразу**, как только устоялся |
| Решение, которое **одновременно** трудно отменить, неочевидно без контекста и является настоящим компромиссом | ADR в `docs/adr/` |
| Всё остальное | **только разговор** |

Третья строка — главная ловушка: большинство решений не проходит три условия ADR, а глоссарий — не спецификация. Поэтому **не очищайте контекст**: передайте этот же разговор в `/to-spec` и потом перечитайте спеку против своих ответов. Сессия, давшая только чище глоссарий и ноль ADR, работает правильно.

## 4. Как пользоваться хорошо (из документации автора)

- **Начинать в свежем разговоре** с сырой идеи — расплывчатость не повод ждать, сессия существует, чтобы её убрать.
- **Plan mode выключить:** он торопит агента выдать план, а нужно, чтобы он продолжал спрашивать.
- **Это разговор, а не допрос.** Главный провал — **пассивность**: «согласен, согласен, согласен» на сорок вопросов, и на выходе план агента, которому вы кивали. Спорьте, говорите, когда уходит рамка, отвечайте «не знаю» всерьёз.
- **«Неграбильные» вопросы** — «одна длинная форма или три страницы?», «как это должно ощущаться?» — разговором не решить. Остановитесь, сделайте `/prototype`, посмотрите и ответьте одной строкой.
- **Считать раунды, а не вопросы.** 46 вопросов в 4 раундах — обычная сессия. 200 вопросов — значит, рамка слишком широка: сначала разбить работу, потом грилить куски. Очень длинная сессия уезжает в «глупую зону» переполненного контекста.
- **Модель — лучшая из доступных.** Грилинг опирается на знание модели о том, как ломаются системы; реализацию можно отдать модели дешевле.
- **Признаки, что работает:** вы с чем-то не согласились; поздние раунды строятся на ранних ответах; вы пришли туда, куда не ожидали; каждый выбор сможете объяснить тому, кого не было.

## 5. Настройки через свой CLAUDE.md / AGENTS.md

Скилл нейтрален к агенту, поэтому личные предпочтения — строкой в своём файле инструкций, а не правкой скилла:

```text
When grilling, ask one question at a time.          # вернуть по одному вопросу
When grilling, ask via AskUserQuestion.             # спрашивать через UI вопросов Claude Code
Do not implement anything without my explicit go.   # если модель пропускает ворота подтверждения
```

- **По одному вопросу** — поддерживаемый вариант, а не обходной путь: так удобнее тем, кто читает медленно, работает на втором языке или лучше фокусируется последовательно.
- **`AskUserQuestion` автор сознательно не встроил** (`.out-of-scope/native-question-tool.md`): у каждого агента свой инструмент вопросов или никакого, а структурированные «пикеры» толкают модель к вопросам с готовыми вариантами — противоположность открытым вопросам грилинга. Пять отклонённых запросов на эту тему.
- **Лимита на число вопросов нет и не будет** (`question-limits.md`, поводом был issue «Codex just asked me 200 questions»): кому-то нужно 3 вопроса, кому-то 50. Управление — обычными словами: «закругляйся», «подведи итог».

## 6. Известные проблемы

| Симптом | Причина и что делать |
| :--- | :--- |
| Всё спросил разом, без рекомендаций, про `GLOSSARY.md` ни слова | обёртка не подгрузила `grilling` (и `domain-modeling`) — модель импровизирует. Самая частая жалоба; спросите агента прямо, какие скиллы он загрузил |
| Хорошее интервью, но файлы не появились | загрузился `grilling`, но не `domain-modeling`; или `grill-with-docs` запущен внутри чужого оркестратора — известный незакрытый баг. Проверить рабочий каталог |
| Кончились вопросы — и начал строить | модель проскочила ворота подтверждения (чаще на слабых и «быстрых» моделях) — строка в `CLAUDE.md` из раздела 5 |
| Сам ответил на свои вопросы | баг прогона; чаще, когда грилинг вызван другим скиллом (`wayfinder`, `triage`). По той же причине нет асинхронного режима: сессия без ответов человека — мнение агента, а не ваше |
| Рекомендация спорит с формулировкой вопроса | «да» тогда означает отказ от рекомендации — ответьте на рекомендацию и скажите об этом |
| Два вопроса в одном раунде всё-таки зависели друг от друга | фронтир выбирается суждением модели, а не вычисляется из графа. Скажите об этом — ветка откроется в следующем раунде |

## 7. Как скилл менялся

| Дата | Изменение |
| :--- | :--- |
| 2026-04 | первые `grill-me` и `grill-with-docs`; вопросы шли по одному |
| 2026-06-12 | вынесен общий примитив `grilling`, `grill-with-docs` = `grilling` + `domain-modeling` |
| 2026-07-03 | ворота подтверждения («не действуй, пока пользователь не подтвердит») |
| 2026-07-06 | «перестать грилить самого себя» (в паре с `wayfinder`) |
| 2026-07-31 | **раунды по фронтиру** и фиксированный формат с `❓`/`➡️`; отдельный скилл `batch-grill-me` влит обратно в `grilling` |
| 2026-08-20 | разделитель `---` между вопросами раунда |
| 2026-10-07 | вопросы формулируются так, чтобы «да» принимало рекомендацию |

## 8. Установка отдельно

```bash
# только примитив и обёртка (через vercel-labs/skills, нужен Node.js)
npx skills@latest add mattpocock/skills --skill grilling
npx skills@latest add mattpocock/skills --skill grill-me
# с документами — ещё два
npx skills@latest add mattpocock/skills --skill domain-modeling
npx skills@latest add mattpocock/skills --skill grill-with-docs
```

В Claude Code проще поставить весь плагин: `claude plugin install mattpocock-skills@claude-plugins-official` — команды будут `/mattpocock-skills:grill-me` и т. п.

**Без установки:** скопировать текст из раздела 1 в `~/.claude/skills/grilling/SKILL.md` (Claude Code) — это обычный Markdown, работает одинаково на Gentoo, Debian и Arch. Даже одна фраза в промпте — *«interview me relentlessly until we reach a shared understanding»* — уже даёт неплохое интервью; скилл добавляет к ней раунды, рекомендации, поиск фактов самим агентом и ворота подтверждения (сравнение — в [конспекте ролика Swag](../../../Education/Youtube/Swag/%D0%A1%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%E2%80%94%20%D1%82%D1%80%D0%B8%20%D0%BF%D0%BE%D0%B4%D1%85%D0%BE%D0%B4%D0%B0%3A%20Matt%20Pocock%2C%20Addy%20Osmani%2C%20pstack%20%28%D0%BA%D0%BE%D0%BD%D1%81%D0%BF%D0%B5%D0%BA%D1%82%20Swag%3A%20grill-me%2C%20%D0%B6%D0%B8%D0%B7%D0%BD%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%2C%20poteto-mode%2C%20unslop%29.md)).

> Аналоги у других авторов: `interview-me` и `idea-refine` у [Addy Osmani](../addyosmani/agent-skills%20%28Addy%20Osmani%29%20%E2%80%94%2025%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B6%D0%B8%D0%B7%D0%BD%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%86%D0%B8%D0%BA%D0%BB%D0%B0%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%20%D0%BE%D1%82%20spec%20%D0%B4%D0%BE%20ship%20%281%2C9k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%29.md) (по одному вопросу до ~95 % уверенности); в [pstack](../pstack/pstack%20%28poteto%2C%20Cursor%29%20%E2%80%94%2056%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%3A%20poteto-mode%20%D1%81%2023%20%D0%BF%D0%BB%D0%B5%D0%B9%D0%B1%D1%83%D0%BA%D0%B0%D0%BC%D0%B8%2C%2024%20%D0%BF%D1%80%D0%B8%D0%BD%D1%86%D0%B8%D0%BF%D0%B0%2C%20interrogate%2C%20unslop%3B%20Cursor%20%D0%B8%20Claude%20Code%20%28~0%2C1k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%29.md) — наоборот, принцип «never block on the human».

## Ссылки

- Скилл: https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
- Документация: [grilling](https://github.com/mattpocock/skills/blob/main/docs/productivity/grilling.md) · [grill-me](https://github.com/mattpocock/skills/blob/main/docs/productivity/grill-me.md) · [grill-with-docs](https://github.com/mattpocock/skills/blob/main/docs/engineering/grill-with-docs.md)
- Отклонённые идеи: [native-question-tool](https://github.com/mattpocock/skills/blob/main/.out-of-scope/native-question-tool.md) · [question-limits](https://github.com/mattpocock/skills/blob/main/.out-of-scope/question-limits.md)

#Скиллы #ИИ_агенты #Claude_Code #Промпты #Требования
