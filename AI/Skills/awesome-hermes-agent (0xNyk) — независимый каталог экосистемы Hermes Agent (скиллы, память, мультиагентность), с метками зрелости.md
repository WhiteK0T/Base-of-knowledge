---
создал заметку: 2026-07-24T20:00:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Hermes
  - NousResearch
  - Каталог
  - AwesomeList
  - Ресурсы
Источник:
  - https://t.me/bugnotfeature/26527
  - https://github.com/0xNyk/awesome-hermes-agent
  - https://www.nyk.dev/oss/awesome-hermes-agent
---

# 🗂️ awesome-hermes-agent — независимый каталог экосистемы Hermes Agent

**awesome-hermes-agent** ([github.com/0xNyk/awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent)) — курируемый **awesome-list не только скиллов, а всей экосистемы** вокруг **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** (самообучающийся опенсорс-агент от **Nous Research**): скиллы и плагины, **провайдеры памяти**, инструменты, **мультиагентные системы**, интеграции/мосты, «поверхности» (GUI/дашборды), гайды. Автор — 0xNyk; список **подчёркнуто независимый** (не официальный проект Nous). **CC BY 4.0, ~4960★**, обновляется.

> [!info] Это НЕ тот же список, что «271 скилл» из прошлого поста
> Пост сваливает в кучу два разных репозитория:
> - **«271 скилл»** — это [awesome-hermes-skills (ZeroPointRepo)](awesome-hermes-skills%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20Hermes%20Agent%20%28Nous%20Research%29%2C%20%D0%BA%D1%80%D0%BE%D1%81%D1%81-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%20%D1%81%20Claude%20Code-Cursor-Windsurf.md) — каталог **именно скиллов** (и с коммерческим уклоном, см. ту заметку).
> - **«ультимативный список»** (этот) — **0xNyk/awesome-hermes-agent** — шире по охвату и **независимый**. Это два разных каталога, а не один.

> [!info] Сверка поста с репозиторием
> | Заявление поста | Реально |
> | :--- | :--- |
> | «мультиагентные системы, провайдеры памяти, наборы скиллов» | ✅ так и есть — разделы Memory Providers, Multi-Agent, Skills & Plugins, Tools, Integrations & Bridges, Detection & Media Forensics |
> | «каждый проект: готовый / экспериментальный / бета» | ✅ у каждой записи **метка зрелости**: `production` (стабильно), `beta` (работает, но допиливается), `experimental` (ранняя стадия) — но это **редакторская оценка**, перепроверяй проект перед тем, как на него закладываться |
> | «список ЛУЧШИХ / ультимативный» | это **хороший независимый обзор**, но «лучший/ультимативный» — оценочно; полезен **только если работаешь с Hermes** |

> [!tip] Чем этот список приятно выделяется
> Помимо охвата — **вменяемое отношение к безопасности**: отдельный раздел *«Check the trust boundary»* напоминает перед включением community-скилла/плагина/MCP/крон-задачи проверить, **кто его триггерит, какие инструменты и доступы он получает, где выполняются команды и как его остановить**. Для «списка ссылок» это редкая и правильная культура. И лицензия **CC BY 4.0** — контент можно переиспользовать с указанием авторства.

## 🗺️ Разделы каталога

- **Official Resources** — офиц. доки/квикстарт Hermes.
- **Skills & Plugins** — community-скиллы, плагины, экосистема agentskills.io, реестры/поиск скиллов.
- **Memory Providers** — бэкенды долгой памяти для агента.
- **Tools & Utilities** (+ Deployment) — утилиты и деплой.
- **Integrations & Bridges** — мосты к другим системам.
- **Detection & Media Forensics** — распознавание/форензика медиа.
- **Multi-Agent** — оркестрация нескольких агентов, «поверхности» (GUI вроде hermes-workspace, дашборды вроде mission-control).
- Секция **«Where do I start?»** — маршрут «с нуля»: запустить Hermes → добавить скиллы → добавить surface.

## 🔁 awesome-hermes-agent vs awesome-hermes-skills

| | **awesome-hermes-agent** (0xNyk) | **[awesome-hermes-skills](awesome-hermes-skills%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20Hermes%20Agent%20%28Nous%20Research%29%2C%20%D0%BA%D1%80%D0%BE%D1%81%D1%81-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%20%D1%81%20Claude%20Code-Cursor-Windsurf.md)** (ZeroPointRepo) |
| :--- | :--- | :--- |
| Охват | **вся экосистема** (память, мультиагент, мосты, tools, surfaces) | в основном **скиллы** (built-in/optional/community) |
| Независимость | подчёркнуто независимый, homepage — личный nyk.dev | коммерческий уклон (homepage transcriptapi.com) |
| Метки | зрелость production/beta/experimental + раздел про безопасность | счётчики скиллов, «skill of the week» |
| Лицензия | **CC BY 4.0** (контент) | MIT |

Не конкуренты насмерть, а **два взгляда**: широкий независимый обзор экосистемы vs плотный каталог скиллов.

## 🖥️ Применимость на системах владельца

Это **список ссылок** (markdown) — платформонезависим; полезен, **только если реально гоняешь Hermes**:

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ ставишь Hermes на десктоп и берёшь из каталога скиллы/память/мосты; читать список можно откуда угодно |
| **Entware / RT-AX56U** | ⚠️ сам агент на роутере не гоняют (нужен LLM-бэкенд/окружение) — Hermes ставь на десктоп/VPS, список читай откуда удобно |

## 🔗 Связанные заметки

- Родственный каталог (скиллы, коммерческий уклон): [awesome-hermes-skills (ZeroPointRepo)](awesome-hermes-skills%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20Hermes%20Agent%20%28Nous%20Research%29%2C%20%D0%BA%D1%80%D0%BE%D1%81%D1%81-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%20%D1%81%20Claude%20Code-Cursor-Windsurf.md)
- Скиллы под других агентов: [agent-skills — реестр скиллов + CLI](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/0xNyk/awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent) · Сайт: [nyk.dev/oss](https://www.nyk.dev/oss/awesome-hermes-agent) · Агент: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26527) · Про «271 скилл»: [@bugnotfeature/26483](https://t.me/bugnotfeature/26483)

#AI #Skills #Hermes #NousResearch #Каталог #AwesomeList #Ресурсы
