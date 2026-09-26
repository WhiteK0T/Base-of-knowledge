---
создал заметку: 2026-09-27T02:04:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Claude_Code
Источник:
  - https://t.me/bugnotfeature/28076
  - https://github.com/alirezarezvani/claude-skills
---

# claude-skills (alirezarezvani) — «команда разработчиков» из 350+ скиллов

Пост «Не баг, а фича» (26.09.2026) обещает: *«Превращаем Claude в целую КОМАНДУ разработчиков — на GitHub собрали 350 скиллов… Claude станет кодером, тестировщиком, безопасником, менеджером и даже начнёт САМ продвигать ваш проект»*, плюс «работают в Claude Code, OpenCode, Antigravity, Hermes, WindSurf и других».

Я клонировал репозиторий (коммит `19392f7`, 26.08.2026), пересчитал `SKILL.md`, прогнал `name`+`description` через `tiktoken` (`o200k_base`) и прочитал README, `INSTALLATION.md`, `STORE.md` и `marketplace.json`.

**Коротко:** проект живой, популярный и под MIT, но сам запутался в своих цифрах. Скиллов **374 уникальных**, а если ставить всё — это **~36 000 токенов постоянно в контексте** (18 % окна на 200k). «Сам продвигает проект» — неправда: маркетинговые скиллы прямо пишут, что ничего не публикуют и не отправляют.

---

## Что это на самом деле

| Параметр | Значение |
| :--- | :--- |
| Репозиторий | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) |
| Лицензия | MIT (© 2025 Alireza Rezvani) |
| Звёзд / форков | ~26 500 / ~3 700 (в README до сих пор написано «5,200+ stars») |
| Создан / последний push | 2025-10-19 / 2026-08-30 |
| Коммитов | 1 499, из них 212 за последний месяц — активно развивается |
| `SKILL.md` в основных папках | 388, **уникальных имён — 374** (9 скиллов лежат дважды: отдельным плагином и внутри домена) |
| `SKILL.md` всего в дереве | 846 — остальное зеркала `.gemini/`, `.codex/`, `.vibe/`, `.hermes/` (симлинки) |
| Python-скриптов | ~745, только stdlib (без `pip install`) |
| Плагинов в marketplace | 99 |
| Размер без `.git` | 52 МБ |

### Сколько же скиллов — сам репозиторий не знает

| Где | Цифра |
| :--- | ---: |
| Пост | 350 |
| Раздел «Multi-Tool Support» README | 345 |
| Описание репозитория на GitHub | 380 |
| Заголовок и бейдж README | 388 |
| Реально уникальных `name` | **374** |

Цифра в посте — просто одна из устаревших версий README. Счётчики Python-скриптов (706 и 727 в двух соседних абзацах) тоже расходятся, а часть команд установки из README ссылается на несуществующие плагины (см. «Установка») — README не успевает за коммитами.

---

## Проверка заявлений поста

| Заявление | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «350 скиллов» | ⚠️ | 374 уникальных. Порядок верный, цифра — из старой версии README |
| «Кодер» | ✅ | `engineering` (88) + `engineering-team` (53): архитектура, фронт/бэк, Docker, Terraform, Helm, K8s-операторы, SLO, `karpathy-coder` и т.д. |
| «Тестировщик» | ✅ | `playwright-pro` (9 скиллов, 3 агента), `api-test-suite-builder`, QA-скиллы |
| «Безопасник» | ✅/⚠️ | Есть `security-pen-testing`, `skill-security-auditor`, `security-guidance` (PreToolUse-хук на 12 антипаттернов). Это чек-листы и простые сканеры, не замена SAST/пентестеру |
| «Менеджер» | ✅ | `product-team` (17), `project-management` (9), плюс целый «C-suite» из 40+22 скиллов-персон (CFO, CMO, CTO…) |
| «Начнёт САМ продвигать проект» | ❌ | 49+7 маркетинговых скиллов **генерируют** тексты, лендинги, SEO-аудиты. LinkedIn-пакет прямо пишет: *«Nothing is automated and nothing is sent. No credentials, no API, no scraping.»* Публиковать будете вы |
| «Закрыть все моменты разработки» | ⚠️ | Широко, но это методички + скрипты-анализаторы. Скиллы не оркестрируют полный цикл сами; есть `agenthub`, `workflow-builder`, но их надо собирать руками |
| «Claude Code, OpenCode, Antigravity, Hermes, WindSurf» | ✅ с оговоркой | Нативно — Claude Code, Codex, Gemini CLI. Hermes и Mistral Vibe — «BYO-sync»: нужен локальный скрипт синка. OpenCode/Windsurf/Antigravity/Cursor/Aider — через конвертер `scripts/convert.sh` |

---

## Цена в токенах — главное, что стоит знать

Claude Code держит в контексте постоянно `name` + `description` каждого установленного скилла; тело грузится по срабатыванию.

| Что | Токенов |
| :--- | ---: |
| `name`+`description` всех 374 уникальных | **36 449** — ~18 % окна на 200k, ещё до первого сообщения |
| Все тела скиллов | 742 273 (грузятся по требованию) |
| В среднем на скилл | 97 / 1 985 (описание / тело) |

По доменам (постоянный расход, если ставить домен целиком):

| Папка / плагин | Скиллов | Токенов в фоне |
| :--- | ---: | ---: |
| `engineering` (`engineering-advanced-skills`) | 88 | 7 004 |
| `marketing-skill` (`marketing-skills`) | 49 | 5 085 |
| `engineering-team` (`engineering-skills`) | 53 | 3 894 |
| `c-level-advisor` (`c-level-skills`) | 40 | 3 338 |
| `ra-qm-team` | 17 | 1 806 |
| `product-team` | 17 | 1 471 |
| `project-management` (`pm-skills`) | 9 | 1 046 |
| `finance` | 5 | 528 |

Самые дорогие описания: `litreview` 252, `agent-launcher-orchestrator` 242, `stock-analysis` 231. Самые тяжёлые тела: `stock-analysis` 7 279, `terraform-patterns` 5 253, `regulatory-affairs-head` 4 432.

Для сравнения: [rampstack-skills](rampstack-skills%20%E2%80%94%20103%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%B0%20%C2%AB%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%C2%BB%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2014%20163%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D0%BD%D0%B5%D0%B9%D1%80%D0%BE-CEO%20%D0%BD%D0%B5%D1%82%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%B8%20%D0%B2%D0%BD%D0%B5%20%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D0%B0%29.md) — 103 скилла и 14 163 токена в фоне. Здесь в 2,5 раза больше. **Ставить «всё сразу» нельзя**, это прямо противоречит идее «команды» — половину окна съест штатное расписание.

---

## На что обратить внимание

- **Часть бесплатных MIT-скиллов продаётся.** `STORE.md` описывает бандлы на Stan Store / Gumroad: «Indie Hacker Pack — $49» (`saas-scaffolder`, `stripe-integration-expert`…), «Engineering Lead Pack — $49», «AI Builder Pack — $39». Все эти скиллы лежат в репозитории бесплатно — платить незачем.
- **Сетевые скрипты.** Из ~745 скриптов сеть трогают 18 (SEO/AEO-аудит страниц, sitemap, load-tester, поиск литературы, аудит зависимостей и т.п.). Телеметрии не нашёл, но перед запуском `scripts/*.py` чужого скилла — читайте.
- **`youtube-full`** — порт [youtube-skills (ZeroPointRepo)](youtube-skills%20%28ZeroPointRepo%29%20%E2%80%94%20%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%D0%B3%D0%BE%20TranscriptAPI%2C%20%D0%B0%20%D0%BD%D0%B5%20%C2%AB%D0%B7%D1%80%D0%B5%D0%BD%D0%B8%D0%B5%C2%BB%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%B0%20%28100%20%D0%BA%D1%80%D0%B5%D0%B4%D0%B8%D1%82%D0%BE%D0%B2%20%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%2C%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%20%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D0%BE%D0%B2%29.md), то есть клиент платного TranscriptAPI (100 бесплатных кредитов разово). Инструкции про обход скрытия секретов из оригинала в этой адаптации нет.
- **`skillopt-sleep`** читает ваши прошлые сессии Claude Code и «переигрывает» задачи **за ваш API-бюджет**, чтобы переписать `CLAUDE.md`/`SKILL.md`. Мощно, но это и расход денег, и доступ ко всей истории — включать осознанно.
- **Установщик OpenClaw** — `bash <(curl -s …/openclaw-install.sh)`: классический «пайп в bash», сначала скачайте и прочитайте.
- **Windows:** зеркала — симлинки; без `git clone -c core.symlinks=true` вместо скиллов получите однострочные файлы-указатели.

---

## Установка

Скилл — это Markdown + (иногда) Python-скрипты, поэтому дистрибутив почти не важен: нужен сам агент, `git` и `python3` для скриптов.

### Способ 1. Плагинами Claude Code — по доменам (рекомендуется)

```
/plugin marketplace add alirezarezvani/claude-skills

/plugin install engineering-skills@claude-code-skills     # ~3,9k токенов
/plugin install pw@claude-code-skills                     # Playwright-тесты (в README ошибочно playwright-pro)
```

⚠️ README предлагает `/plugin install playwright-pro@…`, `skill-security-auditor@…` и `content-creator@…` — **таких плагинов в `marketplace.json` нет**, команды упадут. Playwright называется `pw`, а `skill-security-auditor` приезжает только в составе `engineering-advanced-skills` (или копируйте папку вручную, способ 2).

Правило: ставьте 1–2 домена под текущую задачу, после установки проверьте расход через `/context`.

### Способ 2. Вручную — только нужные

```bash
git clone --depth 1 https://github.com/alirezarezvani/claude-skills
mkdir -p ~/.claude/skills
cp -r claude-skills/engineering-team/skills/{senior-backend,stripe-integration-expert} ~/.claude/skills/
```

### Другие агенты

```bash
./scripts/convert.sh --tool all                       # сконвертировать под все форматы
./scripts/install.sh --tool opencode --target .       # windsurf / cursor / aider / kilocode / augment
./scripts/install.sh --tool antigravity               # ~/.gemini/antigravity/skills/
python3 scripts/sync-hermes-skills.py --verbose       # Hermes Agent → ~/.hermes/skills/
./scripts/codex-install.sh                            # Codex
./scripts/gemini-install.sh                           # Gemini CLI
```

### Зависимости по системам

| Система | Команда |
| :--- | :--- |
| **Gentoo** | `emerge --ask dev-vcs/git dev-lang/python` (Python обычно уже стоит как системный) |
| **Debian / Ubuntu** | `sudo apt install git python3` |
| **Arch** | `sudo pacman -S git python` |
| **Entware (RT-AX56U)** | `opkg install git python3` — пакеты есть, но смысла мало: сам Claude Code на роутере не живёт, а 52 МБ скиллов на 256 МБ флеша — мусор. Максимум — держать клон на USB-диске как зеркало |

---

## Итог

| Кому | Стоит ли |
| :--- | :--- |
| Хочет «команду разработчиков» одной кнопкой | **Нет.** Это библиотека методичек, а не автономная команда; продвигать проект она не будет |
| Ищет готовые скиллы под конкретную задачу (Terraform, Playwright, SEO-аудит, PRD из кода) | **Да.** Выбирайте точечно, по одному-два домена |
| Хочет поставить все 374 | **Нет.** ~36k токенов в фоне навсегда |
| Собирается купить бандл в Gumroad | **Нет.** Те же скиллы бесплатно под MIT |
| Пишет свои скиллы | **Да** — `SKILL-AUTHORING-STANDARD.md`, `write-a-skill`, `skill-security-auditor` полезны как образец |

Сам репозиторий лучше поста: он честно документирует ограничения (BYO-sync для Hermes, «nothing is sent» у маркетинга). Пост добавил от себя «сам продвигает» и взял цифру 350 из устаревшего README.

---

## Связанное

- [rampstack-skills](rampstack-skills%20%E2%80%94%20103%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%B0%20%C2%AB%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%C2%BB%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2014%20163%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D0%BD%D0%B5%D0%B9%D1%80%D0%BE-CEO%20%D0%BD%D0%B5%D1%82%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%B8%20%D0%B2%D0%BD%D0%B5%20%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D0%B0%29.md) — похожий «вместо команды» сборник, 103 скилла
- [Skills Hub (Hermes Agent, Nous Research)](Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md)
- [skillcheck (sx4im)](skillcheck%20%28sx4im%29%20%E2%80%94%20A-B-%D1%82%D0%B5%D1%81%D1%82%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%28SKILL.md%2C%20AGENTS.md%2C%20CLAUDE.md%29%20%D1%81%D0%BE%20%D1%81%D0%BB%D0%B5%D0%BF%D0%BE%D0%B9%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%D0%B9%20%D0%B8%20bootstrap-CI%2C%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B3%D0%B4%D0%B5%20%D0%BE%D0%BD%D0%B0%20%D0%B2%D1%80%D1%91%D1%82.md) — как проверить, помогает ли скилл вообще
- [youtube-skills (ZeroPointRepo)](youtube-skills%20%28ZeroPointRepo%29%20%E2%80%94%20%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%D0%B3%D0%BE%20TranscriptAPI%2C%20%D0%B0%20%D0%BD%D0%B5%20%C2%AB%D0%B7%D1%80%D0%B5%D0%BD%D0%B8%D0%B5%C2%BB%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%B0%20%28100%20%D0%BA%D1%80%D0%B5%D0%B4%D0%B8%D1%82%D0%BE%D0%B2%20%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%2C%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%20%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D0%BE%D0%B2%29.md) — оригинал `youtube-full`
- [Claude Code — шпаргалка команд](../Agents/Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) — `/plugin`, `/context`
- [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

#AI #Skills #Claude_Code
