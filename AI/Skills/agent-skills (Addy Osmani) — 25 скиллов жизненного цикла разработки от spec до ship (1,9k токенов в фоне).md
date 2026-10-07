---
создал заметку: 2026-10-07T12:00:00
author: WhiteK0T
tags:
  - Скиллы
  - ИИ-агенты
  - Claude_Code
  - Codex
  - Cursor
  - Инженерные_практики
  - TDD
Источник:
  - https://github.com/addyosmani/agent-skills
  - https://skills.addy.ie
---

# agent-skills (Addy Osmani) — 25 скиллов жизненного цикла разработки

> [!info] Что это
> Набор из **25 скиллов** (`SKILL.md`), **9 слэш-команд**, **4 персон-ревьюеров** и **7 чек-листов**, которые заставляют ИИ-агента кода работать как старший инженер: сначала спецификация, потом план, код маленькими срезами с тестами, ревью, и только затем выпуск. Автор — **Addy Osmani**, лицензия **MIT**, сайт [skills.addy.ie](https://skills.addy.ie).
>
> Идея из README: агент по умолчанию идёт кратчайшим путём (пропускает спеки, тесты, безопасность), а скиллы навязывают дисциплину, которой придерживаются сильные инженеры.

> [!warning] Не путать
> В хранилище уже есть заметка [agent-skills — реестр проверенных скиллов](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md) — это **другой** проект (`tech-leads-club/agent-skills`, реестр с проверкой безопасности). Здесь — `addyosmani/agent-skills`, набор процессов разработки.

---

## 1. Цифры (замерено на клоне и через API, 2026-10-07)

| Параметр | Значение |
| :--- | :--- |
| Репозиторий создан | 2026-02-15, последний пуш 2026-10-03 |
| Звёзды / форки | **102 672** / **10 757** |
| Открытых issue + PR | 135 (счётчик GitHub считает их вместе) |
| Версия плагина | **0.6.12** (`plugin.json`), теги `0.6.x` |
| Авторы | Addy Osmani; среди основных соавторов по коммитам — Federico Bartoli и Joan León |
| Скиллов / команд / персон / чек-листов | 25 / 9 / 4 / 7 |
| Eval-кейсов | 25 файлов в `evals/cases/` (по одному на скилл) |

### Цена в токенах (tiktoken `o200k_base`)

| Что | Токены |
| :--- | ---: |
| Фронтматтеры всех 25 скиллов (то, что агент держит постоянно) | **1 890** |
| Все 25 `SKILL.md` целиком | 75 693 |
| Скиллы вместе с подфайлами (`references/`, `scripts/`) | 90 879 |
| 4 персоны (`agents/`) | 5 518 |
| 7 чек-листов (`references/`) | 15 708 |
| 9 команд (`.claude/commands/`) | 3 861 |

Вывод: **в фоне проект стоит ~1,9k токенов** — это дёшево (для сравнения, [claude-skills (alirezarezvani)](claude-skills%20%28alirezarezvani%29%20%E2%80%94%20374%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%B0%20%C2%AB%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%C2%BB%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2036k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D1%81%D0%B0%D0%BC%20%D0%BD%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D0%B5%D1%82%29.md) держит ~36k). Тело скилла (2–5k токенов, у `code-review-and-quality` 4,5k) подгружается только когда он сработал. Самые тяжёлые с подфайлами: `idea-refine` (8,6k), `constraint-driven-development` (7,9k), `security-and-hardening` (7,0k), `performance-optimization` (6,2k).

---

## 2. Жизненный цикл

```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
 /spec   /plan  /build   /test   /review  /ship
```

Каждая команда включает нужные скиллы. Ещё есть `/constraints` (зафиксировать стандарты качества один раз), `/code-simplify` и `/webperf` (аудит веб-производительности).

### Все 25 скиллов

**Мета (1)**

| Скилл | Зачем |
| :--- | :--- |
| `using-agent-skills` | Маршрутизатор: дерево «какая задача → какой скилл» и 6 правил поведения (раздел 4) |

**Define и Plan (5)**

| Скилл | Зачем |
| :--- | :--- |
| `interview-me` | Пошаговое интервью, пока понимание задачи не дойдёт до высокой уверенности; для расплывчатых запросов |
| `idea-refine` | Расходящееся → сходящееся мышление: из сырой идеи в конкретное предложение |
| `spec-driven-development` | PRD до кода: цели, команды, структура, стиль, тесты, границы |
| `constraint-driven-development` | Интервью о стандартах качества → `CONSTRAINTS.md`, проверки по стоимости, перехват пропуска тестов |
| `planning-and-task-breakdown` | Спецификация → малые проверяемые задачи с критериями приёмки и порядком зависимостей |

**Build (7)**

| Скилл | Зачем |
| :--- | :--- |
| `incremental-implementation` | Тонкие вертикальные срезы: реализация → тест → проверка → коммит |
| `test-driven-development` | Red-Green-Refactor, «пирамида» тестов 80/15/5, Prove-It для багов, DAMP против DRY, Beyoncé Rule |
| `context-engineering` | Какой контекст и когда подавать агенту (rules-файлы, MCP) |
| `source-driven-development` | Каждое решение по фреймворку — со ссылкой на официальную документацию |
| `doubt-driven-development` | Состязательная проверка со «свежим» контекстом: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP |
| `frontend-ui-engineering` | Компоненты, дизайн-системы, состояние, доступность WCAG 2.1 AA |
| `api-and-interface-design` | Contract-first, закон Хайрама, One-Version Rule, семантика ошибок |

**Verify (2)**

| Скилл | Зачем |
| :--- | :--- |
| `browser-testing-with-devtools` | Chrome DevTools MCP: DOM, консоль, сеть, трассировки |
| `debugging-and-error-recovery` | Пять шагов: воспроизвести → локализовать → свести к минимуму → исправить → защитить тестом |

**Review (4)**

| Скилл | Зачем |
| :--- | :--- |
| `code-review-and-quality` | Ревью по пяти осям (корректность, читаемость, архитектура, безопасность, производительность), метки Nit/Optional/FYI, ~100 строк на изменение |
| `code-simplification` | Chesterton's Fence, упрощение без смены поведения |
| `security-and-hardening` | OWASP Top 10, аутентификация, секреты, трёхуровневые границы |
| `performance-optimization` | Сначала измерить: Core Web Vitals, профилирование, анализ бандла |

**Ship (6)**

| Скилл | Зачем |
| :--- | :--- |
| `git-workflow-and-versioning` | Trunk-based, атомарные коммиты, коммит как точка сохранения |
| `ci-cd-and-automation` | Shift Left, фича-флаги, качественные пайплайны |
| `deprecation-and-migration` | «Код — это обязательство», обязательное и рекомендательное устаревание, миграции |
| `documentation-and-adrs` | Architecture Decision Records, документация «зачем», а не «что» |
| `observability-and-instrumentation` | Структурные логи, метрики RED, трассировка OpenTelemetry |
| `shipping-and-launch` | Предрелизный чек-лист, жизненный цикл флагов, поэтапный выкат, откат |

---

## 3. Команды и персоны

| Команда | Что делает |
| :--- | :--- |
| `/spec` | Спецификация (`SPEC.md`) до кода |
| `/plan` | План мелких задач (`tasks/plan.md`) |
| `/build` | Одна задача: тест (RED) → код (GREEN) → регрессия → сборка → коммит → стоп |
| `/build auto` | Весь план за один утверждённый проход: **один** человеческий барьер, дальше задача за задачей |
| `/test`, `/constraints`, `/review`, `/webperf`, `/code-simplify` | Соответствующие этапы |
| `/ship` | Веер: параллельно запускает персоны и сводит отчёты в **go/no-go** с планом отката |

Что стоит знать про `/build auto` (по тексту команды):
- требует спецификацию по известному пути (`SPEC.md`, `docs/SPEC.md` или `spec/`); README за спецификацию не считается — иначе остановится и отправит на `/spec`;
- до старта проверяет чистоту `git status`, чтобы автокоммиты не захватили чужие правки;
- согласие должно быть однозначным («approve», «go»); «выглядит разумно» не засчитывается;
- по коммиту на задачу, `git add -A` не используется; на авторизации, платежах, деструктивных миграциях и всём, что нельзя откатить `git revert`, **останавливается** и просит подтверждения.

`/ship` пропускает веер, только если одновременно: ≤2 файлов, дифф <50 строк и нет auth/платежей/доступа к данным/конфигов. Свои `code-reviewer`/`security-auditor`/`test-engineer` в `.claude/agents/` имеют приоритет над плагинными.

**Персоны (`agents/`):** `code-reviewer` (staff-инженер, пять осей), `test-engineer` (стратегия тестов, Prove-It), `security-auditor` (уязвимости, threat modeling), `web-performance-auditor` (Core Web Vitals, режимы Quick/Deep). Правило из `orchestration-patterns.md`: персоны **не вызывают** друг друга — оркестрирует команда.

**Чек-листы (`references/`):** definition-of-done, testing-patterns, security-checklist, performance-checklist, accessibility-checklist, observability-checklist, orchestration-patterns.

---

## 4. Как устроено и почему работает

- **Процесс, а не проза.** Скилл — шаги, контрольные точки и критерии выхода, а не справочник.
- **Таблица «Common Rationalizations».** В каждом скилле — отговорки агента («тесты потом») и контраргументы, плюс «Red Flags».
- **Проверка обязательна.** Работа не закончена без доказательств: прогон тестов, вывод сборки, данные рантайма. «Выглядит верно» не считается.
- **Постепенное раскрытие.** `SKILL.md` — точка входа, остальное грузится по необходимости.
- **Фронтматтер = триггер.** По `skill-anatomy.md` описание начинается с того, *что* делает скилл, и содержит «Use when…»; процесс в описание **нельзя** класть (агент прочтёт пересказ вместо скилла). Лимит 1024 символа, разрешены только поля спецификации [agentskills.io](https://agentskills.io).

Шесть сквозных правил из мета-скилла:
1. **Озвучивать допущения** (`ASSUMPTIONS I'M MAKING` → «поправьте, иначе иду дальше»).
2. **Останавливаться при путанице**, а не угадывать.
3. **Возражать**, когда подход плох (угодничество — ошибка).
4. **Простота**: 1000 строк там, где хватило бы 100, — провал.
5. **Дисциплина объёма**: не трогать то, о чём не просили.
6. **Проверять**, а не предполагать; общая планка — `definition-of-done.md`.

Идеи заимствованы из книги *Software Engineering at Google* (Hyrum's Law, Beyoncé Rule, Chesterton's Fence, trunk-based, Shift Left).

---

## 5. Хуки (необязательные)

Каталог `hooks/`. **Плагином не подключаются** — включаются вручную в `.claude/settings.json`.

| Хук | Что делает |
| :--- | :--- |
| `session-start.sh` | Подкладывает мета-скилл в начало сессии (нужен `jq`). Нужен только там, где у хоста нет собственной маршрутизации скиллов; в Claude Code и Codex получился бы второй роутер поверх родного |
| `sdd-cache-pre.sh` / `sdd-cache-post.sh` | Кэш для `WebFetch` в `source-driven-development`: хранит страницы на диске, но **перепроверяет у сервера** (`If-None-Match`/`If-Modified-Since`), отдаёт из кэша только при `304` |
| `simplify-ignore.sh` | Блоки между `simplify-ignore-start/end` скрываются от модели при чтении и возвращаются при записи — защита перф-критичного кода от `/code-simplify` |

---

## 6. Установка

> [!note] Требования
> Универсальный путь и Gemini/Codex-установка — через Node.js. Gentoo: `emerge net-libs/nodejs`. Debian/Ubuntu: `apt install nodejs npm`. Arch: `pacman -S nodejs npm`. Entware: сам проект не нужен — скиллы это обычные `.md`-файлы, при желании копируйте каталог `skills/` вручную.

**Claude Code** (рекомендуется; одинаково на Gentoo/Debian/Arch):
```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```
Если SSH не работает — `/plugin marketplace add https://github.com/addyosmani/agent-skills.git`. Локально: `claude --plugin-dir /путь/к/agent-skills`.

**Универсально** (70+ агентов, [vercel-labs/skills](https://github.com/vercel-labs/skills)):
```bash
npx skills add addyosmani/agent-skills --list                             # посмотреть
npx skills add addyosmani/agent-skills --skill test-driven-development    # один скилл
```

**Другие хосты** (по `docs/*-setup.md`):

| Хост | Как |
| :--- | :--- |
| Codex | `codex plugin marketplace add addyosmani/agent-skills`, затем `codex plugin add agent-skills@agent-skills`; вызов `@spec-driven-development` |
| Gemini CLI | `gemini skills install https://github.com/addyosmani/agent-skills.git --path skills` |
| Cursor | синхронизировать `skills/` в `.cursor/skills/`, правила — в `.cursor/rules/*.mdc` (не вставлять скиллы целиком в rules) |
| OpenCode | копировать в `.opencode/skills/` или `~/.config/opencode/skills/` + `AGENTS.md` |
| Kiro | `.kiro/skills/` |
| Command Code | `cmd skills add addyosmani/agent-skills [--global]` |
| Copilot / Windsurf | персоны из `agents/` и тексты скиллов — в `.github/copilot-instructions.md` / правила Windsurf |
| Antigravity | `agy plugin install https://github.com/addyosmani/agent-skills.git`; обёртки команд не находятся, вызывать скиллы напрямую |

---

## 7. Сравнение и ограничения

В `docs/comparison.md` автор сравнивает проект с **Superpowers** (obra) и скиллами **Matt Pocock**. Итог его же таблицы:
- **agent-skills** — весь жизненный цикл, человек на каждом этапе, evals в репозитории;
- **Superpowers** — длинные автономные прогоны с субагентами и git-worktree;
- **Pocock** — острый ежедневный цикл, сильнее всего в выяснении требований («grill me»).

Единственный внешний бенчмарк, на который ссылается автор, — [эксперимент Om Mishra](https://www.linkedin.com/pulse/superpowers-vs-agent-skills-faster-shipping-safer-reasoning-om-mishra-dzakf/) (одна задача: ~8 мин против ~12, 7 проверок против 5, токены примерно равны). Сам автор называет это не бенчмарком, а иллюстрацией.

> [!warning] Что проверить самому
> - **Сравнение написано автором проекта** — честное по духу, но не независимое.
> - **Нет доказательства, что скиллы улучшают результат.** Три уровня evals проверяют структуру, маршрутизацию по описаниям и трассу выполнения, но не качество итогового кода. Файл `evals/skill-impact.md` — лишь журнал отклонённых правок. Пользу замерьте A/B-тестом, например через [skillcheck](skillcheck%20%28sx4im%29%20%E2%80%94%20A-B-%D1%82%D0%B5%D1%81%D1%82%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%28SKILL.md%2C%20AGENTS.md%2C%20CLAUDE.md%29%20%D1%81%D0%BE%20%D1%81%D0%BB%D0%B5%D0%BF%D0%BE%D0%B9%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%D0%B9%20%D0%B8%20bootstrap-CI%2C%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B3%D0%B4%D0%B5%20%D0%BE%D0%BD%D0%B0%20%D0%B2%D1%80%D1%91%D1%82.md).
> - **Тяжёлый процесс для мелочей.** Для правки в пару строк весь цикл избыточен; автор сам даёт «короткую дорогу» (`/test` + `/review`).
> - **Примеры в основном про веб/TypeScript** (Core Web Vitals, DevTools MCP). Ядро (TDD, ревью, git, ADR) от языка не зависит, а `test-driven-development` прямо требует сначала выяснить стек и команды проекта; но веб-скиллы для системной разработки (C, ядро, пакеты Gentoo) бесполезны.
> - **Автономный режим коммитит сам** — запускайте `/build auto` в отдельной ветке.

---

## 8. С чего начать

1. Поставьте плагин (раздел 6) и посмотрите, сколько реально занимает фон: `/context` в Claude Code.
2. На существующем проекте — путь «brownfield» из `docs/adoption-guide.md`: начать с `/review`, добавить `/test`, потом расширять; на новом — сразу `/spec` → `/plan` → `/build`.
3. Если нужны не все 25 — ставьте точечно (`--skill ...`): для обычной работы хватает `spec-driven-development`, `test-driven-development`, `code-review-and-quality`, `debugging-and-error-recovery`, `git-workflow-and-versioning`.
4. Правила проекта держите в `CLAUDE.md`/`AGENTS.md` (что туда класть — см. `context-engineering`).

## Ссылки

- Репозиторий: https://github.com/addyosmani/agent-skills
- Сайт: https://skills.addy.ie
- Формат скилла: https://github.com/addyosmani/agent-skills/blob/main/docs/skill-anatomy.md
- Руководство по внедрению: https://github.com/addyosmani/agent-skills/blob/main/docs/adoption-guide.md
- Сравнение с аналогами: https://github.com/addyosmani/agent-skills/blob/main/docs/comparison.md
- Спецификация формата скиллов: https://agentskills.io
- CLI `npx skills`: https://github.com/vercel-labs/skills
- Книга *Software Engineering at Google*: https://abseil.io/resources/swe-book

#Скиллы #ИИ_агенты #Claude_Code #Codex #Cursor #Инженерные_практики #TDD
