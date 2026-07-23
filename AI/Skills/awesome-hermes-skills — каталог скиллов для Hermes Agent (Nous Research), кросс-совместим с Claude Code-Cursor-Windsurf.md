---
создал заметку: 2026-07-23T15:50:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Hermes
  - NousResearch
  - Каталог
  - ClaudeCode
  - Ресурсы
Источник:
  - https://t.me/bugnotfeature/26483
  - https://github.com/ZeroPointRepo/awesome-hermes-skills
---

# 🧰 awesome-hermes-skills — каталог скиллов для Hermes Agent

**awesome-hermes-skills** ([github.com/ZeroPointRepo/awesome-hermes-skills](https://github.com/ZeroPointRepo/awesome-hermes-skills)) — курируемый **awesome-list готовых к установке скиллов** для **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** (самообучающийся ИИ-агент от **Nous Research**). Собирает встроенные скиллы, опциональный каталог и проверенные community-скиллы в один список с командами установки. Скиллы **кросс-совместимы** с [Claude Code](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md), OpenClaw, Cursor и Windsurf (общий формат `SKILL.md`). MIT.

> [!warning] Отделяем факты от рекламы поста
> Пост называет это «ультимативным паком» и «имбой, кроме которой не нужно НИЧЕГО». Сверка с репозиторием:
> | Заявление поста | Реально (на момент заметки) |
> | :--- | :--- |
> | «271 скилл: 81 встроенный + 101 + 85» | в репо сейчас **258**: **72 встроенных** + **101 опциональный** + **85 community**. Цифры с постом слегка разошлись (встроенных 72, не 81) — **список живой, счётчики меняются**, сверяйся с бейджем в README |
> | «кроме этого не нужно ничего» | это каталог **под один агент — Hermes**. Полезно, но не «всё на свете»; для других агентов есть свои реестры (ниже) |
> | «работает с Claude Code, Cursor, Windsurf» | да — скиллы в формате `SKILL.md` переносимы, но **заточены под Hermes** (его установщик `hermes skills install …`) |
> | «бесплатно» | сам список — да (MIT). Но см. коммерческий нюанс ниже |

> [!caution] Коммерческий уклон — не весь список «нейтральный»
> Домашняя страница репозитория — **transcriptapi.com**, а рубрика «Skill of the Week» продвигает `youtube-skills` мейнтейнера, завязанный на **платный TranscriptAPI** (есть бесплатный лимит, дальше — деньги). Сам каталог открытый, но **часть «витринных» скиллов ведёт на платный сервис владельца** — это подборка с интересом, а не независимый обзор. Оценивай каждый скилл отдельно.

## 🤖 Что такое Hermes Agent (контекст)

**Hermes** от [Nous Research](https://nousresearch.com) позиционируется как агент с **реальной петлёй самообучения**: он **пишет собственные скиллы из твоих рабочих процессов**, ищет по своим прошлым диалогам и запускается где угодно — от **$5 VPS** и ноутбука до GPU-кластера. Идея репозитория: «агент силён настолько, насколько хороши его скиллы» — поэтому готовый каталог экономит время на старте.

## 🗂️ Как устроен каталог

- **Built-in (72)** — скиллы, что идут с Hermes из коробки.
- **Optional (101)** — опциональный каталог, который можно доустановить.
- **Community (85)** — сторонние скиллы/плагины/тулзы, отобранные «по качеству».
- Установка — одной командой, напр.:
  ```bash
  hermes skills install skills-sh/ZeroPointRepo/youtube-skills/skills/youtube-full
  ```
- Разбито по темам (data science, автоматизация, работа с медиа и т.д.), есть раздел «с чего начать».

> [!note] Что такое скилл (общий формат)
> Скилл — папка с `SKILL.md` (инструкции-промпт) + опц. `templates/`/`references/`; агент подхватывает его, когда задача совпадает с описанием — та же механика [Anthropic Agent Skills](https://www.anthropic.com/news/skills), что у [Ponytail](Ponytail%20%E2%80%94%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D0%B3%D1%80%D0%B0%D1%84%D0%BE%D0%BC%D0%B0%D0%BD%D0%B8%D0%B8%C2%BB%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B5.md). Именно поэтому эти скиллы переносимы между Hermes, Claude Code, Cursor и Windsurf.

## 🔁 Чем отличается от [agent-skills](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md)

| | **awesome-hermes-skills** | **[agent-skills](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md)** (tech-leads-club) |
| :--- | :--- | :--- |
| Фокус | скиллы **под Hermes** (Nous Research) | скиллы под **много агентов** (Claude Code, Cursor, Codex, Copilot…) |
| Формат | awesome-list + `hermes skills install` | **реестр + собственный CLI-установщик** |
| Позиционирование | максимум скиллов для одного агента | «secure, validated» кураторский набор |
| Нюанс | коммерческий уклон (TranscriptAPI) | нейтральнее, упор на безопасность |

Не конкуренты, а разные точки входа: **Hermes-центричный** список vs **мультиагентный** реестр.

## 🖥️ Применимость на системах владельца

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ ставишь Hermes (или используешь скиллы в [Claude Code](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)/Cursor/Windsurf); каталог — источник готовых `SKILL.md` |
| **Entware / RT-AX56U** | ⚠️ сам агент на роутере не гоняют (нужен LLM-бэкенд/Python-окружение). Hermes «запускается на $5 VPS» — вот туда и ставь, а список читай откуда угодно |

## 💡 Вывод

- Полезный **стартовый каталог**, если работаешь с **Hermes**; для других агентов бери переносимые `SKILL.md` выборочно.
- ~332★ — нишевый, но живой список (обновляется); «имба, кроме которой ничего не нужно» — маркетинг поста.
- Помни про **коммерческий уклон** и **расхождение цифр** — смотри на актуальный README, а не на пост.

## 🔗 Ссылки

- Репозиторий: [github.com/ZeroPointRepo/awesome-hermes-skills](https://github.com/ZeroPointRepo/awesome-hermes-skills) · Агент: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26483)
- Связанные: [agent-skills — реестр скиллов + CLI](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md) · [Ponytail — скилл против «графомании»](Ponytail%20%E2%80%94%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D0%B3%D1%80%D0%B0%D1%84%D0%BE%D0%BC%D0%B0%D0%BD%D0%B8%D0%B8%C2%BB%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B5.md) · [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [Сводная таблица AI-агентов](../%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B8%D1%8E%D0%BD%D1%8C%202026%29.md)

#AI #Skills #Hermes #NousResearch #Каталог #ClaudeCode #Ресурсы
