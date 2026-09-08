---
создал заметку: 2026-09-09T04:00:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Агенты
  - Spec-Driven
  - GitHub
  - Python
Источник:
  - https://t.me/bugnotfeature/27048
  - https://github.com/github/spec-kit
  - https://github.github.io/spec-kit/
  - https://pypi.org/project/specify-cli/
---

# 📐 Spec Kit — спецификация до кода для ИИ-агентов

Разбор [поста «Не баг, а фича» от 13.08.2026](https://t.me/bugnotfeature/27048) про [`github/spec-kit`](https://github.com/github/spec-kit) — тулкит от GitHub, заставляющий агента сначала написать спецификацию, а уже потом кодить.

Проект хороший и настоящий, но **шесть команд из поста в таком виде не существуют уже месяца четыре**. Проверено 09.09.2026 по репозиторию и руками: ставил `specify-cli`, инициализировал проект, считал токены через `tiktoken`.

> [!info] Факты
> | | |
> | :--- | :--- |
> | Репозиторий | [github/spec-kit](https://github.com/github/spec-kit), создан **21.08.2025** |
> | Звёзд / форков | **134 138** · 12 070 |
> | Лицензия / язык | **MIT** · Python |
> | Версия | **v1.0.4** (02.09.2026), 1.0.0 вышла 21.08.2026 |
> | Открытых issue | 320 |
> | Активность | коммиты ежедневно, последний — 08.09.2026 |
> | Пакет | `specify-cli` на PyPI, требует **Python ≥3.11** (верхней границы нет) |

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «На Гитхаб **запустили**» | ❌ Проекту год | Создан 21.08.2025. Релиз 1.0.0 назывался *«Spec Kit Turns One»* и вышел 21.08.2026 — через неделю **после** поста |
| Команды `/constitution`, `/specify`, `/clarify`, `/plan`, `/tasks`, `/implement` | ❌ **Так они не работают** | Все команды с префиксом: `/speckit.constitution` и т. д. Префикс встречается в релизах уже с **апреля 2026** — за четыре месяца до поста |
| «Последовательность из 6 команд» | ❌ Их 10 | 7 основных + 3 опциональных |
| `/clarify` как обязательный третий шаг | ⚠️ Она опциональная | В документации `/speckit.clarify` — из блока «Optional», рекомендуется перед `/speckit.plan` |
| «Совместима с Claude Code, Cursor, Copilot, Codex, Gemini CLI и ещё 25 агентами» | ✅ Даже занижено | Насчитал руками **40 интеграций** через `specify integration list` |
| «Больше 95 тысяч звёзд и 8 тысяч форков» | ⚠️ Было верно, устарело | Сейчас **134 138** звёзд и 12 070 форков |
| «Код полностью открытый» | ✅ Верно | MIT |
| «Меньше багов, предсказуемее результат» | ⚠️ Обещание, не факт | Методология, а не гарантия; замеров эффективности проект не приводит |

## 🔤 Главная практическая проблема: имена команд

Если скопировать список из поста и ввести `/constitution` — агент не поймёт. Причём форм имён сейчас **три**, и зависят они от способа установки.

| Как поставил | Как называются команды |
| :--- | :--- |
| Обычные slash-команды (`--integration copilot` и большинство) | `/speckit.constitution` — через **точку** |
| Режим скиллов (Claude Code, `--integration claude`) | `/speckit-constitution` — через **дефис** |
| В посте | `/constitution` — **не существует** |

Проверил на своей машине. Вот что вывел `specify init` при установке под Claude Code:

```
3.1 /speckit-constitution - Establish project principles
3.2 /speckit-specify      - Create baseline specification
3.3 /speckit-plan         - Create implementation plan
3.4 /speckit-tasks        - Generate actionable tasks
3.5 /speckit-implement    - Execute implementation
3.6 /speckit-converge     - Assess the codebase and append remaining work as tasks
```

## 📋 Полный список команд

### Основные (7)

| Команда | Что делает |
| :--- | :--- |
| `speckit.constitution` | Принципы и стандарты проекта |
| `speckit.specify` | Что строим: требования и пользовательские истории |
| `speckit.plan` | Технический план под выбранный стек |
| `speckit.tasks` | Разбивка на выполнимые задачи |
| `speckit.taskstoissues` | **Превращает задачи в issue на GitHub** |
| `speckit.implement` | Выполнение по плану |
| `speckit.converge` | Сверяет кодовую базу со спекой и дописывает оставшееся в задачи |

### Опциональные (3)

| Команда | Что делает |
| :--- | :--- |
| `speckit.clarify` | Уточняющие вопросы по недосказанному (раньше называлась `quizme`) |
| `speckit.analyze` | Проверка согласованности между спекой, планом и задачами |
| `speckit.checklist` | Чек-листы качества требований — авторы называют это *«unit tests for English»* |

Последние четыре из этих десяти пост не упоминает вовсе, а `taskstoissues` и `converge` — как раз то, что отличает Spec Kit от «просто напиши мне ТЗ».

## 💰 Цена в токенах — замерил

Поставил под Claude Code и посчитал `tiktoken` (`o200k_base`):

| Что | Токенов |
| :--- | ---: |
| **Постоянно в контексте** (frontmatter 10 скиллов) | **941** |
| Тела всех скиллов суммарно (грузятся по одному) | 29 543 |
| Каркас проекта на диске | 380 КБ, из них скиллы 192 КБ |

Для сравнения из этой же базы: [Diagram Design](../../Skills/Diagram%20Design%20%28cathrynlavery%29%20%E2%80%94%2039%20%D1%82%D0%B8%D0%BF%D0%BE%D0%B2%20%D0%B4%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28206%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D1%88%D1%80%D0%B8%D1%84%D1%82%D1%8B%20%D0%B8%D0%B7%20Google%2C%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20Claude%20Code%29.md) — 206 токенов в фоне, [nodumbmode](../../Skills/nodumbmode%20%28%D0%A5%D0%B0%D0%BD%D1%83%D0%BC%D0%B0%D1%82%D0%BE%D1%80%D0%B8%29%20%E2%80%94%206%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D1%82%D1%83%D0%BF%D0%BD%D1%8F%D0%BA%D0%B0%C2%BB%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%BD%D0%B5%204%2C%20%D1%87%D1%83%D0%B6%D0%BE%D0%B9%20%D0%BD%D0%B8%D0%BA%20%D0%B2%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B5%2C%20%D1%86%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%D1%85%29.md) — 798. То есть 941 токен постоянного расхода — это заметно, но в пределах нормы для набора из десяти скиллов.

## 🛠️ Установка и первый запуск (проверено)

Ставится через `uv` (рекомендуемый способ) либо обычным pip из PyPI:

```bash
uv tool install specify-cli                 # из PyPI
# или зафиксировать релиз:
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.4

specify init my-project --integration claude
cd my-project
```

Полезные флаги, которые пригодятся в скриптах и на серверах без нормального терминала:

```bash
specify init my-project --non-interactive --ignore-agent-tools   # не зависнет на выборе агента
specify init --here --force --non-interactive --integration claude

specify check              # проверить, что нужные инструменты стоят
specify integration list   # все 40 интеграций и какая установлена
specify self check         # есть ли новая версия (ничего не меняет)
specify self upgrade       # обновиться на месте
```

Что появляется в проекте:

```
.claude/skills/speckit-{constitution,specify,plan,tasks,taskstoissues,
                        implement,converge,clarify,analyze,checklist}
.specify/memory/constitution.md
.specify/templates/{spec,plan,checklist,constitution}-template.md
.specify/integrations/, .specify/scripts/bash/
```

> [!tip] С Python здесь всё в порядке
> `specify-cli` требует `>=3.11` **без верхней границы** — на моём Python 3.14.7 встала актуальная 1.0.4 без плясок. Приятный контраст с [Soup](../../Local-LLM/Soup%20%E2%80%94%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20LLM%20%D0%B8%D0%B7%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%B3%D0%BE%20YAML%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20VRAM-%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%D0%B2%D0%B5%D1%80%D0%BD%D0%B0%2C%20%D0%BD%D0%BE%20%D0%BD%D0%B0%20Python%203.13%2B%20pip%20%D1%82%D0%B8%D1%85%D0%BE%20%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%20%D1%81%D1%82%D0%B0%D1%80%D1%83%D1%8E%200.72.4%29.md), который на 3.13+ молча ставит старую версию.

## 🧩 Чего в посте нет вовсе

Помимо четырёх пропущенных команд, за кадром остались три вещи покрупнее.

**Расширение `bug` — починка багов по тому же принципу.** Отдельный цикл «оценить → починить → протестировать», чтобы агент не прыгал от отчёта сразу к патчу:

```bash
specify extension add bug
# speckit-bug-assess "<отчёт>" slug=login-crash
# speckit-bug-fix   slug=login-crash
# speckit-bug-test  slug=login-crash
```

**Расширение `assess` — оценка идеи до того, как что-то писать.** Цикл «intake → research → define → shape → decide» с исходом **go / needs-clarification / kill**. Работает самостоятельно: если решение «go», результат передаётся в `speckit-specify`.

**Система расширений и пресетов** с приоритетами разрешения шаблонов:

| Приоритет | Что | Где лежит |
| ---: | :--- | :--- |
| 1 | Локальные переопределения проекта | `.specify/templates/overrides/` |
| 2 | Пресеты | `.specify/presets/templates/` |
| 3 | Расширения | `.specify/extensions/templates/` |
| 4 | Ядро Spec Kit | `.specify/templates/` |

Шаблоны разрешаются в момент выполнения сверху вниз — первое совпадение выигрывает. Есть каталог сообщества с готовыми расширениями и пресетами.

## 🤔 Трезво о самой идее

Spec-Driven Development — это дисциплина, а не магия. Что она реально даёт: агент не начинает писать код, пока не зафиксированы требования, план и разбивка, а `speckit.analyze` и `speckit.checklist` ловят противоречия между этими артефактами до того, как они станут кодом.

Чего она не даёт:

- **никаких замеров эффективности** проект не публикует — «меньше багов» из поста это обещание методологии, а не измеренный результат;
- **накладные расходы реальны**: шесть-десять шагов вместо одного промпта, 941 токен постоянно и тысячи на каждый вызов. Для правки в три строки это лишнее;
- **320 открытых issue** и релизы почти ежедневно — проект живой, но подвижный;
- версия 1.0.0 здесь, по признанию самих авторов, **не означает стабильности API**: в релизных заметках они прямо пишут, что старый смысл мажорной версии для них не работает, потому что подстроиться под ломающее изменение агент теперь может быстрее, чем человек прочитает миграционный гайд.

Практический вывод: Spec Kit оправдан на новой фиче или новом проекте, где непонимание задачи дорого обходится. На мелких правках он только замедлит.

## 💻 На твоих системах

Это Python-пакет и набор markdown-инструкций, поэтому от дистрибутива почти не зависит.

| Система | Установка |
| :--- | :--- |
| **Gentoo** (основная) | `emerge dev-python/uv` (или `pipx`), затем `uv tool install specify-cli`. Системный Python 3.14 подходит. Через Portage пакета нет и не нужно — это инструмент разработчика, ставится в пользовательское окружение |
| **Debian / Ubuntu** | Системный pip заблокирован (PEP 668), поэтому `sudo apt install pipx` и `pipx install specify-cli`, либо `uv tool install specify-cli` |
| **Arch** | `pacman -S uv`, дальше `uv tool install specify-cli` |
| **Entware / RT-AX56U** | ❌ Смысла нет: инструмент нужен там, где работает сам ИИ-агент, то есть на десктопе |

Отдельно: `git` в проекте нужен — Spec Kit создаёт ветки под фичи, хотя есть `.specify/feature.json` для работы вне стандартного gitflow.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/27048](https://t.me/bugnotfeature/27048) (13.08.2026)
- Проект: [GitHub](https://github.com/github/spec-kit) · [документация](https://github.github.io/spec-kit/) · [список интеграций](https://github.github.io/spec-kit/reference/integrations.html) · [`specify-cli` на PyPI](https://pypi.org/project/specify-cli/)
- Связанные: [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [Сводная таблица AI-агентов](../%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md) · [MCP — серверы Model Context Protocol](MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) · [Diagram Design — 39 типов диаграмм](../../Skills/Diagram%20Design%20%28cathrynlavery%29%20%E2%80%94%2039%20%D1%82%D0%B8%D0%BF%D0%BE%D0%B2%20%D0%B4%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28206%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D1%88%D1%80%D0%B8%D1%84%D1%82%D1%8B%20%D0%B8%D0%B7%20Google%2C%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20Claude%20Code%29.md) · [nodumbmode — скиллы против «тупняка» агента](../../Skills/nodumbmode%20%28%D0%A5%D0%B0%D0%BD%D1%83%D0%BC%D0%B0%D1%82%D0%BE%D1%80%D0%B8%29%20%E2%80%94%206%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D1%82%D1%83%D0%BF%D0%BD%D1%8F%D0%BA%D0%B0%C2%BB%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%BD%D0%B5%204%2C%20%D1%87%D1%83%D0%B6%D0%BE%D0%B9%20%D0%BD%D0%B8%D0%BA%20%D0%B2%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B5%2C%20%D1%86%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%D1%85%29.md)

#AI #Claude_Code #Агенты #Spec-Driven #GitHub #Python
