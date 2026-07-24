---
создал заметку: 2026-07-24T19:20:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Дизайн
  - Frontend
  - Анимации
  - ClaudeCode
  - Ресурсы
Источник:
  - https://t.me/bugnotfeature/26516
  - https://github.com/emilkowalski/skills
  - https://emilkowal.ski/skill
---

# 🍎 apple-design — 17 принципов Apple-дизайна интерфейсов (с кодом)

**apple-design** — скилл из репозитория [emilkowalski/skills](https://github.com/emilkowalski/skills) («Skills for Design Engineers», MIT, **~20k★**). Автор — **Emil Kowalski**, известный design-инженер (создатель [Sonner](https://github.com/emilkowalski/sonner)/[Vaul](https://github.com/emilkowalski/vaul), автор курса по анимациям). Скилл — один файл [`SKILL.md`](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md), где **17 принципов** «живого» интерфейса Apple разобраны и **переложены на веб** (CSS, Pointer Events, `requestAnimationFrame`, spring-библиотеки вроде Motion/Framer Motion) — к каждому есть **пример кода**. Ставится в [Claude Code](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)/агента как обычный Agent Skill.

> [!info] Отделяем факты от рекламы поста
> | Заявление поста | Реально |
> | :--- | :--- |
> | «собрали ВСЕ паттерны и принципы дизайна с WWDC» | это дистилляция **в основном одного доклада** — *Designing Fluid Interfaces* (WWDC 2018) — плюс материалы/типографика/основы. Не «весь WWDC», а концентрат про **плавную жестовую моторику** интерфейса |
> | «17 принципов, к каждому пример кода» | ✅ ровно **17 разделов** (Response, Direct manipulation, Interruptibility, Springs, Momentum, Rubber-banding, Materials, Typography, Reduced motion…) с CSS/JS-сниппетами |
> | «делаем дизайны как профи в один клик» | ⚠️ это **справочник-знание для агента**, а не «кнопка красоты». Он повышает качество моушена/интеракций в коде, но думать про UX всё равно тебе |
> | «ставится за один клик, без ограничений» | ✅ бесплатно (MIT), это markdown-скилл: ставишь или просто копируешь `SKILL.md` |

> [!tip] Про что он на самом деле (важно для ожиданий)
> Ядро — **fluid motion и жесты для веба**: анимировать от текущего значения, наследовать скорость пальца, проецировать инерцию, ловить и разворачивать анимацию на лету (interruptibility), пружины вместо CSS-transition для gesture-driven UI, rubber-banding на границах. Это **фронтенд/React-моушен**, а не графдизайн и не нативный iOS. Идеально для web/React design-инженера, слабо применимо к «просто картинкам».

## 🧩 Что внутри (17 разделов)

Response (убить задержку) · Direct manipulation (1:1-трекинг, `setPointerCapture`) · **Interruptibility** (главный принцип — прерываемость) · Behavior over animation (springs) · Velocity handoff · Momentum projection · Spatial consistency · Hinting · Rubber-banding · Gesture «feel»-чеклист · Frame-level smoothness · Materials & depth (полупрозрачность/иерархия) · Multimodal feedback (motion+sound+haptics) · **Reduced motion & a11y** · Typography (optical sizing, tracking, leading) · Design foundations (8 принципов) · Process. В конце — Quick Reference.

## 📦 Это часть набора из 7 скиллов

В репозитории [emilkowalski/skills](https://github.com/emilkowalski/skills) кроме apple-design есть: `animation-vocabulary`, `emil-design-eng`, `find-animation-opportunities`, `improve-animations`, `pick-ui-library`, `review-animations` — почти всё про **анимации и UI-инженерию**. apple-design — самый «фундаментальный» из них.

## ✅ Почему честно хвалить

- Автор **реально из индустрии** (Sonner/Vaul — популярные UI-компоненты), а не безымянный «топ-10 листикл».
- Это **дистилляция легендарного доклада Apple** в конкретные веб-практики с кодом — редкий случай, когда «принципы» сразу применимы.
- Открыто и бесплатно (MIT); можно читать как статью, даже не ставя как скилл.

## 🖥️ Применимость на системах владельца

Платформонезависимо — это markdown-знание для ИИ-агента:

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ ставишь скилл в Claude Code/агента при вёрстке фронтенда с анимациями; либо читаешь `SKILL.md` как гайд |
| **Entware / RT-AX56U** | ➖ неактуально: разработка/рендер идут на десктопе, роутер ни при чём |

## 🔗 Связанные заметки

- Обратная сторона дизайна — **убрать** слоп: [epstein.md — гигантский .md против «AI-слопа» в дизайне](../Prompts/epstein.md%20%28Shipper%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B3%D0%B0%D0%BD%D1%82%D1%81%D0%BA%D0%B8%D0%B9%20.md-%D1%84%D0%B0%D0%B9%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%ABAI-%D1%81%D0%BB%D0%BE%D0%BF%D0%B0%C2%BB%20%D0%B2%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B5%20%28%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D1%82%D0%B5%D0%BD%D0%B8%2C%20%D1%8D%D0%BC%D0%BE%D0%B4%D0%B7%D0%B8%2C%20~350%20%D0%98%D0%98-%D1%81%D0%BB%D0%BE%D0%B2%29.md)
- Дизайн-системы для агентов: [Open Design — альтернатива Claude Design](../Open%20Design%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%B0%20Claude%20Design%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%2B%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%29.md)
- Где берут и ставят скиллы: [agent-skills — реестр скиллов + CLI](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/emilkowalski/skills](https://github.com/emilkowalski/skills) · Сам скилл: [apple-design/SKILL.md](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md) · Сайт автора: [emilkowal.ski/skill](https://emilkowal.ski/skill)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26516)

#AI #Skills #Дизайн #Frontend #Анимации #ClaudeCode #Ресурсы
