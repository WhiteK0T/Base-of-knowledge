---
создал заметку: 2026-09-09T00:30:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Claude_Code
  - Диаграммы
  - Дизайн
  - SVG
Источник:
  - https://t.me/bugnotfeature/26995
  - https://github.com/cathrynlavery/diagram-design
  - https://cathrynlavery.github.io/diagram-design/
---

# 📐 Diagram Design — 39 типов диаграмм для ИИ-агентов

Разбор [поста «Не баг, а фича» от 12.08.2026](https://t.me/bugnotfeature/26995) про скилл **Diagram Design** — [`cathrynlavery/diagram-design`](https://github.com/cathrynlavery/diagram-design).

Редкий случай: пост скорее **недооценивает** проект, чем раздувает. Всё перечисленное в нём правда, но за рамками осталось примерно вдвое больше. Проверено 09.09.2026 по репозиторию, с подсчётом токенов через `tiktoken` (`o200k_base`).

> [!info] Факты
> | | |
> | :--- | :--- |
> | Репозиторий | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design), создан 16.04.2026 |
> | Звёзд / форков | **34 400** · 2 187 |
> | Лицензия | **MIT** |
> | Версия скилла | 2.6 (манифесты плагина — 2.6.17) |
> | Активность | коммиты **ежедневно**, последний 07.09.2026 |
> | Контрибьюторов | 15+ (автор — 75 коммитов, дальше 16, 8, 5…) |
> | Автор | Cathryn Lavery, основательница BestSelf.co |
> | Объём | 216 файлов, **2,86 МБ**; 39 справок по типам + 4 примитива |

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :--- | :--- |
| «Скилл для Claude Code» | ⚠️ Не только | Claude Code, **Codex, Factory Droid, Claude Cowork, Pi, Kiro, OpenCode** — семь хостов |
| «От графиков и блок-схем до таймлайнов» | ✅ И сильно больше | **39 типов**: Sankey, Wardley map, fishbone, Gantt, ER, UML class, swimlane, treemap, radar, kanban, user journey, org chart… |
| «Полный контроль над генерацией» | ✅ Верно | Правится `references/style-guide.md`, есть именованные профили в `~/.diagram-design/profiles/` |
| «ИИ-агент **заранее** изучит проект и подберёт цвета и шрифты» | ⚠️ Механизм другой | Это не автомат: ты явно говоришь «onboard diagram-design to https://твойсайт», агент **скачивает главную страницу** и вытаскивает палитру и шрифты. Изучается **сайт**, а не проект |
| «HTML-файл, легко интегрировать куда угодно» | ⚠️ С оговоркой | Один самодостаточный `.html`, но по признанию README — *«no network requests beyond Google Fonts»*: шрифты подтягиваются из сети при открытии |
| Про цену в токенах | ❌ Умолчание | 206 токенов постоянно, ~10 000 при срабатывании |
| Про экспорт в SVG и PNG | ❌ Умолчание | Кроме HTML есть `svg` и `png` (в том числе @2 под слайды) |
| Про импорт из draw.io и Mermaid | ❌ Умолчание | Умеет перерисовывать `.drawio`, `.drawio.png/.svg` и `.mmd` |
| Про доступность | ❌ Умолчание | Автопроверка контраста WCAG AA, `role="img"`, `aria-labelledby`, `prefers-reduced-motion` |

## 🔢 Цена в токенах — здесь она честная

Стандартная для этого хранилища проверка. Замер `tiktoken`, кодировка `o200k_base`:

| Что | Токенов | Когда попадает в контекст |
| :--- | ---: | :--- |
| Frontmatter `SKILL.md` | **206** | **Всегда**, пока скилл установлен |
| └ из них строка `description` | 185 | |
| Тело `SKILL.md` | **10 005** | Только когда запрос совпал |
| Одна справка по типу | ~2–8 тыс. | Только та, что нужна |

Для сравнения — [nodumbmode](nodumbmode%20%28%D0%A5%D0%B0%D0%BD%D1%83%D0%BC%D0%B0%D1%82%D0%BE%D1%80%D0%B8%29%20%E2%80%94%206%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D1%82%D1%83%D0%BF%D0%BD%D1%8F%D0%BA%D0%B0%C2%BB%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%BD%D0%B5%204%2C%20%D1%87%D1%83%D0%B6%D0%BE%D0%B9%20%D0%BD%D0%B8%D0%BA%20%D0%B2%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B5%2C%20%D1%86%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%D1%85%29.md) держит в фоне 798 токенов, [Taste Skill](Taste%20Skill%20%28Leonxlnx%29%20%E2%80%94%2013%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D0%98%D0%98-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B2%D0%BE%20%D1%84%D1%80%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D0%B4%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2022k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%2C%20%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0%2C%20%D0%B2%D1%8B%D0%B4%D1%83%D0%BC%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%29.md) — 22 тысячи суммарно. Здесь 2,86 МБ материалов при 206 токенах фонового расхода: архитектура «прогрессивной загрузки» реально работает, а не заявлена на словах.

> [!tip] Почему так вышло
> Постоянно грузится только `name` + `description`. Описание раздуто до 185 токенов именно потому, что перечисляет все 39 типов — это плата за то, чтобы агент понимал, когда скилл уместен, не читая тело. Разумный размен.

## 🎨 Почему диаграммы не выглядят «сгенерированными»

Дизайн-система описана в README одним абзацем, и правила в ней жёсткие:

- **один акцентный цвет**, 1–2 фокусных элемента на диаграмму;
- три семейства шрифтов: Instrument Serif (заголовок и курсивные выноски), Geist (подписи узлов), Geist Mono (технические подписи — порты, URL, типы полей, а не «просто для айтишного вида»);
- **волосяные рамки 1px, никаких теней**, радиус скругления максимум 10px;
- **все координаты, ширины и отступы делятся на 4** — автор прямо называет это тем, что удерживает диаграммы от ощущения ИИ-генерации.

Тот же подход, что в [epstein.md](../Prompts/epstein.md%20%28Shipper%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B3%D0%B0%D0%BD%D1%82%D1%81%D0%BA%D0%B8%D0%B9%20.md-%D1%84%D0%B0%D0%B9%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%ABAI-%D1%81%D0%BB%D0%BE%D0%BF%D0%B0%C2%BB%20%D0%B2%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B5%20%28%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D1%82%D0%B5%D0%BD%D0%B8%2C%20%D1%8D%D0%BC%D0%BE%D0%B4%D0%B7%D0%B8%2C%20~350%20%D0%98%D0%98-%D1%81%D0%BB%D0%BE%D0%B2%29.md) и [Taste Skill](Taste%20Skill%20%28Leonxlnx%29%20%E2%80%94%2013%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D0%98%D0%98-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B2%D0%BE%20%D1%84%D1%80%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D0%B4%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2022k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%2C%20%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0%2C%20%D0%B2%D1%8B%D0%B4%D1%83%D0%BC%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%29.md): не «сделай красиво», а список запретов.

Плюс набор из **87 монохромных иконок** (Tabler Icons, MIT + Simple Icons, CC0) через `currentColor` — наследуют твою палитру.

## 🖌️ Брендирование: как это работает на самом деле

Пост говорит, что агент «заранее изучит проект». Реальный сценарий из README:

```
Ты:     "onboard diagram-design to https://yoursite.com"
Агент:  → скачивает главную страницу
        → извлекает доминирующую палитру и стек шрифтов
        → раскладывает по семантическим ролям: paper, ink, muted, accent, link
        → показывает предлагаемый diff
        → пишет токены в references/style-guide.md
Ты:     "yes, apply it"
```

| Что берётся с сайта | Во что превращается |
| :--- | :--- |
| фон `<body>` | `paper` — фон диаграммы |
| основной цвет текста | `ink` |
| вторичный текст | `muted` |
| самый частый брендовый цвет (CTA, ссылки) | `accent` — фокусный акцент |
| шрифт `<h1>` / `<body>` / `<code>` | заголовочный / подписи узлов / технические подписи |

Хорошая деталь: перед записью проверяется **контраст WCAG AA** для `ink` на `paper` при размерах 9–12px, и если цвет с сайта не проходит — предлагается поправка с объяснением. Ещё одна: **первый запуск в новом проекте не даёт молча выдать диаграмму в дефолтном стиле** — скилл останавливается и спрашивает, запустить онбординг, вставить токены руками или согласиться на умолчания.

Для нескольких клиентов — профили: `.diagram-design` с `profile: <slug>` в корне проекта, сами профили в `~/.diagram-design/profiles/`. Они переживают обновления скилла, в отличие от правок в `style-guide.md`.

## ⚠️ Три оговорки, которых нет в посте

> [!warning] 1. «Самодостаточный HTML» — с оговоркой про шрифты
> В `references/output-spec.md` формат `html` описан как self-contained, но с пометкой **live fonts**, а критерий приёмки в README звучит так: *«opens double-clicked, offline, with no network requests **beyond Google Fonts**»*. То есть при открытии файл ходит на `fonts.googleapis.com`. Для корпоративного контура, air-gapped-сети или просто из соображений приватности это стоит учитывать: либо вшивать шрифты в файл руками, либо экспортировать в `png`.

> [!warning] 2. Автообновление в Claude Code выключено по умолчанию
> README прямо предупреждает: Claude Code отключает автообновление для сторонних marketplace. После установки нужно зайти в `/plugin` → **Marketplaces** → **diagram-design** → **Enable auto-update**, иначе останешься на версии установки. Учитывая, что коммиты идут ежедневно, это заметно.

> [!note] 3. «No Mermaid slop» — но Mermaid импортируется
> Формулировка из описания репозитория задиристая, а на деле скилл **умеет читать** `.mmd` и перерисовывать их своим стилем (`references/import-mermaid.md`, скрипт `mermaid_extract.py` на 48 КБ). Позиция не «Mermaid — зло», а «Mermaid как формат исходника годится, как способ отрисовки — нет». То же для `.drawio`.

## 🧭 Когда скилл НЕ нужен

Отдельный раздел в README, и он честный — сам отговаривает от использования:

- **быстрые unicode-схемы** для твитов и вывода в терминал → другой скилл;
- **списки чего угодно** → таблица или буллеты;
- **сравнения «было/стало»** → таблица;
- **«диаграмма» из одной фигуры** → просто напиши предложение.

> *«Перед тем как рисовать, спроси: узнает ли читатель из этого больше, чем из хорошо написанного абзаца? Если нет — не рисуй.»*

Стоит помнить и про встроенные возможности: **Claude Code рендерит Mermaid в артефактах нативно**, без всяких библиотек, и для страниц-артефактов есть свой встроенный навык диаграмм. Diagram Design решает другую задачу — **отдельный `.html`/`.svg`/`.png` файл**, который кладут в презентацию, README или письмо.

## 💻 Установка

Скилл — это файлы для ИИ-агента, а не программа, поэтому ОС роли не играет: работает всюду, где работает сам агент (Linux, macOS, Windows). Для роутера с Entware неприменимо — там нет ни одного из этих хостов.

```text
# Claude Code
/plugin marketplace add cathrynlavery/diagram-design
/plugin install diagram-design@diagram-design
# затем /plugin → Marketplaces → diagram-design → Enable auto-update
```

```bash
# Codex
codex plugin marketplace add cathrynlavery/diagram-design
codex plugin add diagram-design@diagram-design

# Factory Droid
droid plugin marketplace add https://github.com/cathrynlavery/diagram-design
droid plugin install diagram-design@diagram-design --scope user

# Pi
pi install https://github.com/cathrynlavery/diagram-design
```

**Kiro** — импорт по URL подкаталога `.../tree/main/skills/diagram-design`. **OpenCode** — копия или симлинк `skills/diagram-design/` в `~/.config/opencode/skills/`.

Если планируешь править стиль руками — ставь из клона, иначе обновления затрут `style-guide.md`:

```bash
git clone https://github.com/cathrynlavery/diagram-design.git ~/code/diagram-design
ln -s ~/code/diagram-design/skills/diagram-design ~/.claude/skills/diagram-design
```

Проверка результата — в комплекте есть самопроверка:

```bash
python3 skills/diagram-design/scripts/self_check.py <файл.html>   # должно напечатать OK
```

Установка чистая: ник в командах — `cathrynlavery`, тот же, что у владельца репозитория. Это стоит проверять всегда: в [nodumbmode](nodumbmode%20%28%D0%A5%D0%B0%D0%BD%D1%83%D0%BC%D0%B0%D1%82%D0%BE%D1%80%D0%B8%29%20%E2%80%94%206%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D1%82%D1%83%D0%BF%D0%BD%D1%8F%D0%BA%D0%B0%C2%BB%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%BD%D0%B5%204%2C%20%D1%87%D1%83%D0%B6%D0%BE%D0%B9%20%D0%BD%D0%B8%D0%BA%20%D0%B2%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B5%2C%20%D1%86%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%D1%85%29.md) в команде установки стоял чужой аккаунт.

## 💡 Итог

Из всех скиллов, разобранных в этом хранилище, этот — самый аккуратно сделанный: реальная прогрессивная загрузка (206 токенов в фоне против 2,86 МБ материалов), доступность не для галочки, отдельный раздел «когда меня не надо», ежедневные коммиты и живое сообщество. MIT, ник в установке чистый.

Три вещи, о которых стоит помнить: **шрифты тянутся из Google** при открытии готового файла, **автообновление в Claude Code надо включить руками**, а онбординг под бренд читает **сайт**, а не проект — и делает это, только когда его об этом попросят.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/26995](https://t.me/bugnotfeature/26995) (12.08.2026)
- Проект: [GitHub](https://github.com/cathrynlavery/diagram-design) · [галерея всех типов](https://cathrynlavery.github.io/diagram-design/) · [SKILL.md](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/SKILL.md) · [cookbook](https://github.com/cathrynlavery/diagram-design/blob/main/docs/cookbook.md)
- Иконки: [Tabler Icons](https://tabler.io/icons) (MIT) · [Simple Icons](https://simpleicons.org) (CC0)
- Связанные: [nodumbmode — 6 скиллов против «тупняка»](nodumbmode%20%28%D0%A5%D0%B0%D0%BD%D1%83%D0%BC%D0%B0%D1%82%D0%BE%D1%80%D0%B8%29%20%E2%80%94%206%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D1%82%D1%83%D0%BF%D0%BD%D1%8F%D0%BA%D0%B0%C2%BB%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%BD%D0%B5%204%2C%20%D1%87%D1%83%D0%B6%D0%BE%D0%B9%20%D0%BD%D0%B8%D0%BA%20%D0%B2%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B5%2C%20%D1%86%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%D1%85%29.md) · [Taste Skill — против ИИ-шаблонности](Taste%20Skill%20%28Leonxlnx%29%20%E2%80%94%2013%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D0%98%D0%98-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B2%D0%BE%20%D1%84%D1%80%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D0%B4%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2022k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%2C%20%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0%2C%20%D0%B2%D1%8B%D0%B4%D1%83%D0%BC%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%29.md) · [agent-skills — реестр скиллов](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md) · [epstein.md — против AI-слопа в дизайне](../Prompts/epstein.md%20%28Shipper%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B3%D0%B0%D0%BD%D1%82%D1%81%D0%BA%D0%B8%D0%B9%20.md-%D1%84%D0%B0%D0%B9%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%ABAI-%D1%81%D0%BB%D0%BE%D0%BF%D0%B0%C2%BB%20%D0%B2%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B5%20%28%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D1%82%D0%B5%D0%BD%D0%B8%2C%20%D1%8D%D0%BC%D0%BE%D0%B4%D0%B7%D0%B8%2C%20~350%20%D0%98%D0%98-%D1%81%D0%BB%D0%BE%D0%B2%29.md) · [checklist.design — чек-листы UI/UX](../../Design/checklist.design%20%28George%20Hatzis%29%20%E2%80%94%20100%2B%20%D1%87%D0%B5%D0%BA-%D0%BB%D0%B8%D1%81%D1%82%D0%BE%D0%B2%20UI-UX%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%20%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D0%BE%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%2C%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%20%D0%BB%D0%B8%2C%20%D0%B7%D0%B0%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%2C%20%D0%BE%D1%84%D0%BB%D0%B0%D0%B9%D0%BD-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%29.md)

#AI #Skills #Claude_Code #Диаграммы #Дизайн #SVG
