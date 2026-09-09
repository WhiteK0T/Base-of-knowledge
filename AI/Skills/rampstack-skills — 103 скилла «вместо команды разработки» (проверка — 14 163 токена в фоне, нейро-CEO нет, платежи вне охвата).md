---
создал заметку: 2026-09-09T00:00:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Claude_Code
  - SEO
Источник:
  - https://t.me/bugnotfeature/27249
  - https://github.com/rampstackco/claude-skills
  - https://rampstack.co
---

# rampstack-skills — 103 скилла «вместо команды разработки»

Сборник скиллов для Claude Code от компании RampStack. Пост подаёт его как замену команде фронтенд- и бэкенд-разработки, которая «создаёт проект, пока вы отдыхаете», и завершает работу «нейро-CEO» с вердиктом о продакшене.

Проверил репозиторий целиком: скачал, посчитал токены через `tiktoken` (`o200k_base`), разобрал состав по темам и прочитал `workflows/`. Число 103 — правда. Почти всё остальное из описания — нет.

**Главная цифра: 14 163 токена постоянно в контексте.** Это ~7,1 % окна на 200k, которые расходуются ещё до того, как вы напишете первое слово. Самый дорогой сборник скиллов из задокументированных в этой базе.

---

## Что это на самом деле

| Параметр | Значение |
| :--- | :--- |
| Репозиторий | [rampstackco/claude-skills](https://github.com/rampstackco/claude-skills) |
| Лицензия | MIT |
| Звёзд / форков | 830 / 117 |
| Создан | 2026-04-28 |
| Последний push | 2026-09-07 |
| Открытых issue | 2 |
| Сайт | `rampstack.co` (коммерческий) |
| Скиллов в `skills/` | **103** |
| Всего `SKILL.md` в дереве | 206 — это те же 103 плюс их копия в `dist/pi/.agents/skills/` (сборка под Pi) |

Собственное описание репозитория, без маркетинга поста:

> Stack-agnostic Claude Skills covering the full website lifecycle: brand, design, content, SEO, dev, ops, growth, and research

То есть авторы честно говорят «жизненный цикл **сайта**»: бренд, дизайн, контент, SEO, разработка, эксплуатация, рост, ресёрч. «Команда фронтенд- и бэкенд-разработки» — это уже добавка пересказчика.

---

## Проверка заявлений поста

| Заявление | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «103 скилла» | ✅ | Ровно 103 каталога в `skills/`. Единственная честная цифра поста |
| «Ставятся в один клик» | ✅ | `/plugin marketplace add rampstackco/claude-skills` + `/plugin install` — действительно две команды |
| «Заменит команду фронтенд- и бэкенд-разработки» | ❌ | Разработки и эксплуатации касаются ~14 скиллов из 103. Остальное — SEO, бренд, контент, продакт-менеджмент |
| «Дизайн, вёрстка, безопасность» | ⚠️ | Есть: `frontend-component-build`, `design-standards`, `security-baseline`, `accessibility-audit`. Но это методички, а не генераторы кода |
| «Подключение платежей» | ❌ | Ни одного скилла про платежи. Ближайший, `upgrade-flow-design`, **прямо исключает** это из охвата (цитата ниже) |
| «Учтено буквально ВСЁ» | ❌ | Дыры видны сразу: нет бэкенда, БД, API, аутентификации, деплоя как такового |
| «Работают в команде и создают проект, пока вы отдыхаете» | ❌ | Скиллы не оркестрируются между собой и не запускают друг друга. А `workflows/` построены вокруг **решения человека** (цитата ниже) |
| «Любой процесс настраиваемый» | ✅ | Обычные `SKILL.md` под MIT — правьте как угодно |
| «Финал — нейро-CEO: проверит работу и выдаст вердикт о продакшене» | ❌ | **Скилла CEO не существует.** Слово `CEO` встречается в репозитории 4 раза — и все в прозе чужих скиллов, как пример должности |

### Про платежи — цитата из самого репозитория

`skills/upgrade-flow-design/SKILL.md`, строка 35:

> Out of scope: cross-funnel architecture (covered by `funnel-flow-architecture`); pricing-page copy (covered by `landing-page-copy`); **the engineering implementation; specific Stripe/Chargebee/Recurly/Paddle billing-platform configurations** (those stay implementation-side).

Единственный скилл, вплотную подходящий к деньгам, явно выносит и саму инженерную реализацию, и настройку платёжных платформ за свои границы.

### Про «нейро-CEO»

Поиск по всем 103 скиллам и по `workflows/` даёт четыре вхождения слова `CEO`, и ни одно не является скиллом:

- `ux-research` — «CEO wants strategic implications» (как формулировать бриф под аудиторию);
- `ai-content-collaboration` — «a CEO, an expert, a journalist» (чья подпись под текстом);
- `feature-launch-playbook` — «Executive sponsor. Usually CEO at this size»;
- `long-form-content-frameworks` — пример плохой цитаты «Content is king, John Smith, CEO».

Ближе всего к «вердикту о продакшене» подходят `launch-runbook` и `feature-launch-playbook` — чек-листы запуска. Никакого агента-начальника, выносящего решение, в репозитории нет.

### Про «пока вы отдыхаете»

`workflows/AGREEMENT-LOG.md` описывает схему журнала согласий — и она построена ровно на обратном:

> The agreement log records what an engine proposed, what its guardrail said, **what a human decided**, and whether the two agreed.

Автономность здесь не выдаётся авансом, а **зарабатывается**: `workflows/autonomy-review.md` — «периодическая церемония» над этим журналом, где по проценту совпадений агента с человеком отдельные классы проверок получают право на авто-пропуск, а регрессии после мерджа это право отзывают. Это осмысленная инженерная позиция, но она прямо противоположна обещанию «создают проект, пока вы отдыхаете».

---

## Цена в токенах — главное, что стоит знать

Замер: `tiktoken`, кодировка `o200k_base`, локальная копия репозитория.

Claude Code держит в контексте постоянно только `name` + `description` каждого скилла, тело подгружается по срабатыванию. README это подтверждает: *«Skills load on demand: each contributes roughly its name and description until Claude needs it»*.

| Что | Токенов | Комментарий |
| :--- | ---: | :--- |
| `name` + `description` всех 103 | **14 163** | **всегда в контексте** — 7,1 % окна на 200k |
| Весь frontmatter всех 103 | 18 525 | если считать со служебными полями |
| Все тела скиллов | 310 643 | грузятся по требованию, целиком не влезут никогда |
| В среднем на скилл | 138 / 3016 | описание / тело |

Самые дорогие описания (постоянный расход): `integration-orchestrator` 206, `logo-design` 201, `experiment-design` 194, `editorial-qa` 190, `vertical-site-conventions` 190.

Самые тяжёлые тела (разовый расход при срабатывании): `experimentation-analytics` 7065, `experiment-design` 6124, `long-form-content-frameworks` 6052, `data-warehouse-experimentation` 5868, `feature-flagging` 5283.

### Сравнение с другими сборниками из этой базы

| Сборник | Скиллов | Постоянно в контексте |
| :--- | ---: | ---: |
| [Diagram Design](Diagram%20Design%20%28cathrynlavery%29%20%E2%80%94%2039%20%D1%82%D0%B8%D0%BF%D0%BE%D0%B2%20%D0%B4%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28206%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D1%88%D1%80%D0%B8%D1%84%D1%82%D1%8B%20%D0%B8%D0%B7%20Google%2C%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20Claude%20Code%29.md) | 1 | 206 |
| [nodumbmode](nodumbmode%20%28%D0%A5%D0%B0%D0%BD%D1%83%D0%BC%D0%B0%D1%82%D0%BE%D1%80%D0%B8%29%20%E2%80%94%206%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D1%82%D1%83%D0%BF%D0%BD%D1%8F%D0%BA%D0%B0%C2%BB%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%BD%D0%B5%204%2C%20%D1%87%D1%83%D0%B6%D0%BE%D0%B9%20%D0%BD%D0%B8%D0%BA%20%D0%B2%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B5%2C%20%D1%86%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%D1%85%29.md) | 6 | 798 |
| [Spec Kit](../Agents/Tooling/Spec%20Kit%20%28GitHub%29%20%E2%80%94%20%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B4%D0%BE%20%D0%BA%D0%BE%D0%B4%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D0%B4%D0%B0%D0%B2%D0%BD%D0%BE%20%D1%81%20%D0%BF%D1%80%D0%B5%D1%84%D0%B8%D0%BA%D1%81%D0%BE%D0%BC%20speckit%2C%20%D0%B8%D1%85%2010%20%D0%B0%20%D0%BD%D0%B5%206%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%2040%29.md) | 10 | 941 |
| **rampstack-skills** | **103** | **14 163** |

Порядок величины другой. За 14k токенов вы покупаете не «команду», а каталог, из которого в конкретной задаче сработают два-три пункта.

Для сравнения по разовому расходу: [Taste Skill](Taste%20Skill%20%28Leonxlnx%29%20%E2%80%94%2013%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D0%98%D0%98-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B2%D0%BE%20%D1%84%D1%80%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D0%B4%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2022k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%2C%20%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0%2C%20%D0%B2%D1%8B%D0%B4%D1%83%D0%BC%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%29.md) съедает 22k при срабатывании, но почти ничего в фоне. Здесь ровно наоборот: фон дорогой, а тела разумного размера.

---

## Что внутри на самом деле — состав по темам

| Тема | Скиллов |
| :--- | ---: |
| SEO | 15 |
| Контент и маркетинг | 16 |
| Бренд и дизайн | 14 |
| Разработка и эксплуатация | 14 |
| Прочее: UX-ресёрч, продакт-менеджмент, аналитика, эксперименты | 44 |
| **Всего** | **103** |

Разработки в этом сборнике меньше, чем одного только SEO. Полный список дев-скиллов, которые вообще можно назвать инженерными:

`frontend-component-build`, `code-review-web`, `qa-testing`, `security-baseline`, `performance-optimization`, `accessibility-audit`, `dependency-management`, `feature-flagging`, `incident-response`, `monitoring-and-alerting`, `backup-and-disaster-recovery`, `internationalization`, `documentation-strategy`, `cost-optimization`.

Это набор практик для веб-сайта, а не стек для приложения. Ни бэкенда, ни схемы БД, ни API, ни аутентификации.

---

## Установка

Скилл — это набор Markdown-файлов для агента, а не программа, поэтому дистрибутив роли не играет: работает везде, где работает сам Claude Code. Ниже — способы, а не платформы.

### Способ 1. Плагином (рекомендуется)

```
/plugin marketplace add rampstackco/claude-skills
/plugin install rampstack-skills@rampstack
```

### Способ 2. Подмножеством — на порядок дешевле

README сам пишет прямым текстом: **«You do not have to install all 103. Pick the categories that match your work.»** Авторы вынесли курируемые подборки в отдельные репозитории:

| Плагин | Репозиторий | Скиллов | Постоянно в контексте |
| :--- | :--- | ---: | ---: |
| `rampstack-starter` | `rampstackco/claude-skills-starter` | 14 | **1 865** (0,9 %) |
| `rampstack-seo` | `rampstackco/claude-skills-seo` | 12 | **1 678** (0,8 %) |
| `rampstack-pm` | `rampstackco/claude-skills-pm` | 12 | **1 640** (0,8 %) |

```
/plugin marketplace add rampstackco/plugins
/plugin install rampstack-starter@rampstack
```

Стартовый набор — это как раз почти весь дев-блок: `frontend-component-build`, `code-review-web`, `qa-testing`, `performance-optimization`, `accessibility-audit`, `design-standards`, плюс базовый SEO и контент. **За 1865 токенов вместо 14 163 вы получаете практически всю инженерную часть сборника.** Если ставить вообще, то так.

Оговорка: сами репозитории подборок совсем свежие и почти без внимания (`claude-skills-starter` — 2 звезды, `claude-skills-seo` — 5, `claude-skills-pm` — 4, все созданы в середине мая 2026). Лицензия MIT, содержимое — копия скиллов из основного репозитория.

### Способ 3. Вручную, файлами

```bash
git clone https://github.com/rampstackco/claude-skills
mkdir -p ~/.claude/skills
cp -r claude-skills/skills/* ~/.claude/skills/      # глобально, все 103

# или только нужные — правильный вариант
cp -r claude-skills/skills/{frontend-component-build,code-review-web,qa-testing} ~/.claude/skills/

# или в проект
mkdir -p .claude/skills && cp -r claude-skills/skills/* .claude/skills/
```

**Gentoo / Debian-Ubuntu / Arch:** разницы нет — нужен только сам Claude Code и `git` (`emerge dev-vcs/git` · `apt install git` · `pacman -S git`).

**Entware / ASUS RT-AX56U:** технически файлы положить можно (`git` в репозитории `armv7sf-k3.2` есть), но смысла ноль — Claude Code на роутере не живёт, а 103 каталога Markdown на 256 МБ флеша это просто мусор.

---

## Коммерческая часть

Репозиторий бесплатный и под MIT, но он же витрина для `rampstack.co`. Это видно по формулировкам в `workflows/`:

> The instance, its write path, the designation allowlist, and every promotion decision are **operated, not published**.

То есть схема журнала согласий опубликована, а работающий экземпляр, путь записи и логика принятия решений — нет. Это оговорено честно и открытым текстом, но означает, что часть описанной в `workflows/` методологии в открытой версии не воспроизводится.

Отдельно лежит `STARTER-KIT.md` — методичка о том, как строить собственную библиотеку рабочих процессов; она явным образом заявлена как пригодная к использованию без платных «движков» RampStack.

---

## Итог

| Кому | Стоит ли |
| :--- | :--- |
| Ищет замену команде разработки | **Нет.** Ни бэкенда, ни платежей, ни оркестрации, ни «нейро-CEO». Пост описывает другой продукт |
| Ведёт свой сайт / продукт и занимается SEO и контентом | **Да, это основная аудитория.** Ставьте `rampstack-seo` |
| Фронтендер, нужны чек-листы качества | **Осторожно да** — только `rampstack-starter`, 1865 токенов |
| Хочет поставить все 103 | **Нет.** 7,1 % окна навсегда ради каталога, из которого сработают единицы |
| Изучает, как устроены большие библиотеки скиллов | **Да** — `SKILL_AUTHORING.md`, `STARTER-KIT.md` и `workflows/` написаны неожиданно вдумчиво |

Сам репозиторий заметно лучше поста о нём. Это аккуратная, честно документированная библиотека методичек по жизненному циклу сайта с внятной позицией по автономности агентов. Пост же приписал ей бэкенд, платежи, автономную работу и несуществующего начальника — четыре заявления из девяти просто ложны, и ни одно из них не является преувеличением авторов: всё это добавлено пересказом.

---

## Связанное

- [Skills Hub (Hermes Agent, Nous Research)](Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md) — как считают скиллы в каталогах
- [skillcheck (sx4im)](skillcheck%20%28sx4im%29%20%E2%80%94%20A-B-%D1%82%D0%B5%D1%81%D1%82%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%28SKILL.md%2C%20AGENTS.md%2C%20CLAUDE.md%29%20%D1%81%D0%BE%20%D1%81%D0%BB%D0%B5%D0%BF%D0%BE%D0%B9%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%D0%B9%20%D0%B8%20bootstrap-CI%2C%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B3%D0%B4%D0%B5%20%D0%BE%D0%BD%D0%B0%20%D0%B2%D1%80%D1%91%D1%82.md) — чем проверить, помогает ли скилл вообще
- [Claude Code — шпаргалка команд](../Agents/Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) — `/plugin`, `/context` и остальное
- [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

#AI #Skills #Claude_Code #SEO
