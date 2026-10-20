---
создал заметку: 2026-10-20T09:43:00
author: WhiteK0T
tags:
  - Education
  - Youtube
  - AI
  - Skills
  - Claude_Code
  - Cursor
Источник:
  - https://www.youtube.com/watch?v=C_uGcUJtGjw
  - https://www.youtube.com/@javaswag
  - https://github.com/mattpocock/skills
  - https://github.com/addyosmani/agent-skills
  - https://github.com/cursor/plugins/tree/main/pstack
---

# 🧰 Скиллы для ИИ-агентов — три подхода: Matt Pocock, Addy Osmani, pstack (Swag)

Конспект ролика [«Если ты не используешь скиллы в 2026 — ты в меньшинстве. Разбираю, как собрать свой набор»](https://www.youtube.com/watch?v=C_uGcUJtGjw) канала [**Swag**](https://www.youtube.com/@javaswag) (11.10.2026, ~22 минуты). Видео расшифровано whisper, таблицы и цифры сверены со слайдами, звёзды и установка — с GitHub на 20.10.2026.

**Повод:** в прошлом выпуске о трендах 2026 года вывод был «скиллы используют все». Автор признаётся, что сам пользуется ими минимально, и сравнивает три популярных набора, чтобы понять, **как собрать свой** — для себя, команды или организации.

**Главная мысль:** три сильных инженера пишут скиллы **по-разному** — и это три готовых шаблона дизайна собственного набора.

## Три репозитория

| | Matt Pocock | Addy Osmani | pstack (poteto) |
| :--- | :--- | :--- | :--- |
| Кто | автор курсов по TypeScript (Total TypeScript, AI Hero) | Director of Engineering в Google (Chrome; Lighthouse) | Lauren (poteto) — инженер Cursor и xAI, команда React Compiler; ранее Meta и Netflix. В X: «2000 PR за прошлый месяц» |
| Репозиторий | [mattpocock/skills](https://github.com/mattpocock/skills) | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | [cursor/plugins → pstack](https://github.com/cursor/plugins/tree/main/pstack) |
| Звёзды | ~298k | ~109k | ~13k — **у всего** монорепозитория `cursor/plugins` |
| Состав | 38 скиллов: engineering, productivity, WIP, misc | 25 скиллов, 4 персоны, 9 команд | 51 скилл, 23 playbook'а, 2 агента |
| Размер скилла | **~20–2 000 слов** — короткие | **~1 300–3 500 слов** — развёрнутые | принципы по 130–400 слов; главный режим ~3 000 |
| С чего начать | `/setup-matt-pocock-skills`, затем `ask-matt` | `/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship` | `/setup-pstack`, затем `/poteto-mode` |
| Где работает | Claude Code, Codex, Copilot, Gemini, `npx skills` | Claude Code, Codex, Gemini, OpenCode, `npx skills` (70+ агентов) | плагин Cursor, рассчитан на несколько моделей; **ставится и в Claude Code** (см. ниже) |
| Дополнительно | глоссарий, scope policy, журнал отклонённых идей | hooks, reference checklists, evals | гайд из 10 глав, бот Benny для Slack |

> Звёзды на слайде (284k / 104k / 10,7k на 10.10.2026) за десять дней выросли; число скиллов меняется ещё быстрее — автор и сам оговаривается, что «завтра это может быть неправдой».

## Три подхода к дизайну скиллов

| Набор инструментов — **Matt Pocock** | Жизненный цикл — **Addy Osmani** | Один главный режим — **pstack** |
| :--- | :--- | :--- |
| `grill-me`, `to-spec`, `to-tickets`, `tdd`, `prototype`, `triage`, `wayfinder`, `diagnosing-bugs`, `handoff`, `teach` | `/spec` → `/plan` → `/build` → `/test` → `/review` → `/ship` | `poteto-mode` в центре; вокруг `tdd`, `arena`, `swarm`, `why`, `how`, `recall`, `reflect`, `unslop` |
| Маленькие независимые части: берёшь нужную, комбинируешь, форкаешь то, что оставляешь | Этапы по порядку; каждая команда включает нужные скиллы своего этапа | Вызываешь один режим — он сам выбирает playbook и вызывает остальные скиллы |

- **Matt — скиллы как tools.** Нужна операция grill — вызвал grill; нужны тикеты — `to-tickets`. Можно и цепочкой, но каждый скилл самостоятелен.
- **Addy — жизненный цикл.** Сначала спека, потом план, потом можно прогнать автономно. Скиллы заточены друг под друга: «не вызывай после grill-me сразу диагностику багов, потому что захотелось».
- **pstack — «картофельный режим».** Входишь в `poteto-mode`, пишешь задачу — дальше он решает сам. Скиллы здесь больше похожи на **принципы**, которые агент подбирает автоматически.
- Установка у всех — **скиллом же**: команда setup. «По моде 2026 года» и для своей CLI-утилиты стоит написать скилл, который её установит.

## Matt Pocock — «маленькие, легко адаптируемые и composable»

Подробно про набор: [skills (Matt Pocock)](../../../AI/Skills/mattpocock/skills%20%28Matt%20Pocock%29%20%E2%80%94%2038%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BD%D0%B0%D1%81%D1%82%D0%BE%D1%8F%D1%89%D0%B8%D1%85%20%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%BE%D0%B2%3A%20grilling%2C%20%D0%B3%D0%BB%D0%BE%D1%81%D1%81%D0%B0%D1%80%D0%B8%D0%B9%20%D0%B8%20ADR%2C%20to-spec%20%D0%B8%20to-tickets%2C%20tdd%2C%20code-review%20%28~0%2C6k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%29.md).


- **Главное:** планирование через ваш issue tracker — `grill-me`, затем `to-spec`, `to-tickets` и реализация. `wayfinder` планирует работу больше одной сессии, `triage` переводит issues между метками в заданном порядке.
- **Трекер расширяемый:** по умолчанию задачи пишутся в Markdown-файл, но можно сказать «залей в GitHub».
- **Чем выделяется — язык инженерного дизайна:** `codebase-design` (deep modules), `domain-modeling` (**глоссарий и ADR**), `improve-codebase-architecture`. Есть и задачи вне кода: `teach`, writing, `handoff`.
  - **Глоссарий** фиксирует, что значит каждый термин спецификации («что такое tracker и где он»).
  - **ADR** (Architectural Decision Record) — документ с принятыми архитектурными решениями; вариант `grill-me with docs` создаёт ADR на каждую спеку.
  - Ощущение, что Matt просто взял любимые практики — DDD, ADR, глоссарий — и упаковал их.
- **Компромисс — строгий отбор:** новые скиллы от контрибьюторов не принимаются, issue должен описывать сбой из реальной сессии. Под себя — **через форк**: форкнул, удалил ненужное.

### grill-me — главный совет ролика

Суть скилла — первая фраза: *«interview the user relentlessly until we reach a shared understanding»* — допрашивай пользователя, пока не придёте к общему пониманию. Дальше — техника: разложить решения в дерево (design tree) и идти по нему раундами.

Демо на проекте «Морской бой» (Java 25, сервер + браузерный фронтенд, WebSocket/SSE), задача «хочу CLI», Claude Code в plan mode:

| Просто фраза «interview me relentlessly…» без скилла | `grill-me` |
| :--- | :--- |
| Для чего CLI? → для терминала. Кто будет пользоваться? → реальные игроки. Играть против браузерных игроков? → только CLI | сначала **сам собирает факты** из кода (главный класс, сервер, SSE, GET/POST) — правило «не спрашивай факты, которые можно найти самому» |
| — | спрашивает **«зачем?»** (и сам предлагает ответ: scriptable way to exercise the server) |
| про язык и зависимости не спросил | спрашивает **язык и зависимости** («а вдруг я хочу CLI на Rust?») |

Вывод: даже голая фраза даёт неплохое интервью, но короткие ёмкие дополнения `grill-me` заставляют копать глубже.

## Addy Osmani — «production-grade engineering skills для AI coding agents»

- **Главное:** каждый этап delivery — spec, plan, разработка маленькими шагами, TDD, review, security, performance, observability, CI/CD, deprecation и launch.
- **Чем выделяется:** единственный из трёх с **evals** (test cases, fixtures и отчёт, что меняет каждый скилл). Плюс constraint-driven, doubt-driven и source-driven development.
- **Компромисс:** длинные чек-листы-гайды по 1 300–3 500 слов — подробно, но **занимает много контекста**. Дополняются 4 персонами и 7 reference checklists.
- **Только для спеки — три пути:** `interview-me` (вопросы по одному, пока не будет ~95 % уверенности, — аналог grill-me), `idea-refine` (обсудить сырую идею), `spec-driven-development` (PRD до кода). Затем — `planning-and-task-breakdown`.
- `planning-and-task-breakdown` читается как объяснение джуниору: задачи маленькие, проверяемые, с явными критериями приёмки, каждая — на одну сессию. «Хорошая разбивка — разница между агентом, который работает надёжно, и агентом, который производит месиво». Внутри — шаблон задачи (acceptance criteria, verification, dependencies, files), размеры XS–XL (L и больше — дробить) и вертикальные срезы вместо горизонтальных.
- Впечатление автора: «**вся голова Эдди выгружена в скиллы**» — раньше для этого понадобилась бы книга. И магии нет: дотошно записанные приёмочные критерии, верификация, зависимости.

Подробно про набор: [agent-skills (Addy Osmani)](../../../AI/Skills/addyosmani/agent-skills%20%28Addy%20Osmani%29%20%E2%80%94%2025%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B6%D0%B8%D0%B7%D0%BD%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%86%D0%B8%D0%BA%D0%BB%D0%B0%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%20%D0%BE%D1%82%20spec%20%D0%B4%D0%BE%20ship%20%281%2C9k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%29.md).

## pstack — принципы и один режим

- **Принципы** (`principle-*`): короткие правила хорошей фичи и системы — как ООП-принципы, только для инженерной работы агента. Пример — `principle-fix-root-causes`: *при отладке не чини симптомы; проследи каждую проблему до корня и исправь там*. И объяснение **почему**: фиксы симптомов накапливаются, каждый обход усложняет систему, а настоящий баг остаётся; поиск корня медленнее вначале, но в сумме сокращает отладку.
- **`unslop`** — любимый скилл автора: убирает из текста «ИИ-шаблоны», сохраняя смысл и тон. В списке паттернов — highlighting, ensuring, reflecting, showcasing, fostering, жаргон и абстрактные метафоры (substrate, wedge, vector…). По словам автора, unslop — способ «немного избавиться от ИИ-психоза».
- **`bro`** — пересказать последнее сообщение простым человеческим языком, без жаргона.
- **«Never block on the human»** — агент никогда не останавливается, чтобы спросить человека, а ищет решение сам. Автор связывает это с фабрикой агентов, работающей без участия автора, и бесплатными токенами Cursor.

## Одни темы — разные подходы

| Тема | Matt Pocock | Addy Osmani | pstack |
| :--- | :--- | :--- | :--- |
| TDD | `tdd`: red-green-refactor, ~570 слов | `test-driven-development`, ~2 400 слов | `tdd` — только по запросу или при очевидном repro |
| Отладка | `diagnosing-bugs`, пошаговый цикл | `debugging-and-error-recovery` | bug-fix playbook + `fix-root-causes` |
| Ревью | `code-review`: стандарты и спека, в параллельных субагентах | `code-review-and-quality`, проверка по пяти осям | `interrogate`: adversarial review несколькими моделями |
| Планирование | `to-spec`, затем `to-tickets` в вашем трекере | spec-driven, затем task breakdown | architect, figure-it-out, multi-phase plan |
| Вопросы пользователю | `grill-me`, grilling | `interview-me`, `idea-refine` | **избегает**: «never block on the human» |

«Всё то же самое, просто упаковано по-другому».

## Какой выбрать

| Matt Pocock — если вы | Addy Osmani — если вы | pstack — если вы |
| :--- | :--- | :--- |
| хотите маленькие скиллы, которые форкаете и держите у себя | хотите покрыть каждый этап | работаете в Cursor |
| планируете работу через issues и тикеты | нужны письменные quality gates для команды | запускаете агентов параллельно или на ночь |
| цените продуманный дизайн модулей | любите slash-команды по этапам | хотите доказательств, что каждая задача работает |
| переключаетесь между агентами | хотите evals, доказывающие пользу скиллов | готовы принять одно сильное мнение |

**Выбор автора:**

- `grill-me` (или `grill-me with docs`) — **«стопудово»**; если брать один скилл — этот;
- `to-spec` и `to-tickets` от Matt — по желанию: результат лучше и быстрее его собственных спек и тикетов; при хорошо «прогретой» сессии иногда достаточно сохранить Markdown-файл;
- **проверки от Addy** — в конце скиллов вроде `incremental-implementation` есть верификация: каждый инкремент протестирован и закоммичен, сборка чистая. Модель иногда галлюцинирует, что сделала работу, — проверка ловит это. **У Matt такого нет**, поэтому автор скрестил бы скиллы Matt с верификацией Addy;
- `unslop` от pstack.

Если не знаете, с чего начать, — начните с мелочей, например с одной строки из grill-me в обычном промпте.

## Поправки и уточнения (на 20.10.2026)

- **pstack работает не только в Cursor.** README прямо описывает установку в Claude Code: `/plugin marketplace add cursor/plugins`, `/plugin install pstack@cursor-plugins`. Команды получают префикс (`/pstack:poteto-mode`), модели выбираются через `/pstack:setup-pstack`, а шаги с функциями только Cursor (Bugbot, Automations) пропускаются. По умолчанию режим делит работу между моделями: код — Grok, самые сложные изменения, тексты и суждения — Opus 5.5.
- **Вклад:** в pstack PR приветствуются («fork it. improve it. make it yours. PRs are welcome!»); строгий отбор — это про репозиторий Matt.
- **Установка Matt в Claude Code** — плагином, который обновляется сам: `claude plugin install mattpocock-skills@claude-plugins-official`; альтернатива — `skills.sh`, который копирует редактируемые файлы в проект (ставить что-то одно, иначе каждый скилл будет дважды).
- **Addy:** `npx skills add addyosmani/agent-skills` (Claude Code, Cursor, Codex, Copilot, Cline и другие).

## Призыв автора

Делиться опытом: как вы пользуетесь скиллами, где их храните, как передаёте друг другу в команде и организации — «это полезнее, чем говорить, что ИИ нас всех погубит».

## 🔗 Ссылки

- Видео: https://www.youtube.com/watch?v=C_uGcUJtGjw
- Канал Swag: https://www.youtube.com/@javaswag
- Matt Pocock — skills: https://github.com/mattpocock/skills
- Addy Osmani — agent-skills: https://github.com/addyosmani/agent-skills
- pstack (Cursor plugins): https://github.com/cursor/plugins/tree/main/pstack

#Education #Youtube #AI #Skills #Claude_Code #Cursor
