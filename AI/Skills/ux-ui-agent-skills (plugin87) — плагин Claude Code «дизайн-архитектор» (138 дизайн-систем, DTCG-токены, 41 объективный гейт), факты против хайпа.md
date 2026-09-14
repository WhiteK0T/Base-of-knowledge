---
создал заметку: 2026-09-14T14:40:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Дизайн
  - Frontend
  - ClaudeCode
  - Ресурсы
Источник:
  - https://t.me/bugnotfeature/27794
  - https://github.com/plugin87/ux-ui-agent-skills
  - https://plugin87.github.io/ux-ui-agent-skills/
---

# 🎨 ux-ui-agent-skills — плагин Claude Code «дизайн-архитектор»

**ux-ui-agent-skills** ([github.com/plugin87/ux-ui-agent-skills](https://github.com/plugin87/ux-ui-agent-skills), MIT, v2.10.0, ~1.3k★) — **не «библиотека дизайна для любого ИИ», а плагин/кит для [Claude Code](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)**: чистый **слой знаний и инструкций** (без своего рантайма и зависимостей), который превращает агента в «сеньор-дизайн-архитектора». Внутри — **138 брендовых дизайн-систем**, DTCG-токены, 50+ спецификаций компонентов, **19 запускаемых скиллов**, 5 команд и агент `design-critic`. Автор — **Thientan Soparat** ([@plugin87](https://github.com/plugin87)).

> [!warning] Отделяем факты от рекламы поста
> | Заявление поста | Реально |
> | :--- | :--- |
> | «библиотека для ИИ-агентов, делают красивые интерфейсы» | активируется **через Claude Code** (`/plugin` или `npx … init` + автозагрузка `CLAUDE.md`). Есть `.claude/rules/`, команды, агент — это **экосистема Claude Code**, а не «любой агент». В другой агент — только копированием файлов вручную |
> | «138 профессиональных дизайн-систем» | ✅ подтверждено (в `/design-systems`); плюс 50+ компонентов, токены в **DTCG**-формате, адаптеры под React/Next/Vue/Svelte/Angular/SwiftUI и др. |
> | «дизайн-архитектор с 15+ лет опыта» | это **цитата из README самого автора**, маркетинг. По факту — справочник-знание + проверки, а не «кнопка красоты»: за UX-решения всё равно отвечаешь ты |
> | «ставится, работает из коробки» | ✅ бесплатно (MIT, но **с указанием авторства**); pure-markdown/JS-слой без build-инструментов |
> | «14/14 на независимой оценке» (cold-start evals в `/evals`) | цифры **самоотчёт автора**, не сторонний аудит — принимать со скидкой |

> [!tip] Что здесь реально ценно (честно хвалить)
> Главное отличие от обычных промпт-паков — **41 объективный гейт качества** (`node scripts/accuracy_report.mjs`), которые **валят сборку вместо «успеха на словах»**: контраст WCAG на **реальных headless-рендерах** в светлой и тёмной теме, размер целей (2.5.8), фокус/клавиатура, адаптив на **280/320/414px**, RTL, `prefers-reduced-motion`, **ноль хардкод-значений и эмодзи**. Плюс **anti-slop доктрина** (запрет indigo→purple градиентов, эмодзи-иконок, слабого контраста) и агент `/critique`, который рендерит на нескольких брейкпоинтах, кликает по контролам и даёт **аргументированный** фидбек. Это ближе к инженерии дизайн-систем, чем к «сделай красиво».

## 🧩 Что внутри (структура репо)

- `/tokens` — DTCG-токены (цвет, типографика, отступы, тени, границы, моушн).
- `/components` — 50+ компонентов от атомов до шаблонов, с полными состояниями.
- `/design-systems` — **138** брендовых систем (layout- и editorial-паттерны).
- `/frameworks` — адаптеры генерации кода: React, Next.js, Vue, Svelte, Angular, SwiftUI, Jetpack Compose, Flutter, vanilla CSS…
- `/accessibility` — гайдлайны WCAG 2.2 AA/AAA.
- `/.claude/rules/` — «доктрина дизайна» (принудительные правила).
- `/evals` — результаты cold-start прогонов; `/tests` — **41 объективный гейт**.

## ⌨️ Команды и скиллы

`/design-component` · `/data-dashboard` · `/gate` · `/critique` · `/grill-me` · `/ship` · `/scaffold-project` — плюс 19 скиллов и агент `design-critic`.

## 📦 Установка

```bash
# Как плагин Claude Code (рекомендуется — без копирования файлов в репо):
/plugin marketplace add plugin87/ux-ui-agent-skills
/plugin install ux-ui-agent-skills@ux-ui-agent-skills
#   → 19 скиллов, 5 команд, агент design-critic

# Как npm-кит (кладёт файлы локально, CLAUDE.md автозагрузится в Claude Code):
npx ux-ui-agent-skills init
npx ux-ui-agent-skills demo

# Прогнать все проверки качества:
node scripts/accuracy_report.mjs
```

Живое демо без установки: [plugin87.github.io/ux-ui-agent-skills](https://plugin87.github.io/ux-ui-agent-skills/) (26 отрендеренных страниц).

## 🖥️ Применимость на системах владельца

Платформонезависимо — это markdown/JS-слой знаний для ИИ-агента, «движок» и рендер идут на десктопе:

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ ставишь плагином в Claude Code при фронтенд-работе; для гейтов нужен Node (headless-рендер контраста/адаптива) |
| **Entware / RT-AX56U** | ➖ неактуально: разработка и рендер на десктопе, роутер ни при чём |

## 🔗 Связанные заметки

- Прямой сосед по теме: [Open Design — опенсорсная альтернатива Claude Design](../Open%20Design%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%B0%20Claude%20Design%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%2B%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%29.md) (там движок — любой агент из PATH; здесь — заточка под Claude Code)
- Принципы «живого» дизайна: [apple-design (Emil Kowalski)](apple-design%20%28Emil%20Kowalski%29%20%E2%80%94%2017%20%D0%BF%D1%80%D0%B8%D0%BD%D1%86%D0%B8%D0%BF%D0%BE%D0%B2%20Apple-%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B0%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81%D0%BE%D0%B2%20%D1%81%20%D0%BA%D0%BE%D0%B4%D0%BE%D0%BC%20%28WWDC%20Designing%20Fluid%20Interfaces%29.md)
- Против шаблонности во фронтенде: [Taste Skill (Leonxlnx)](Taste%20Skill%20%28Leonxlnx%29%20%E2%80%94%2013%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D0%98%D0%98-%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B2%D0%BE%20%D1%84%D1%80%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D0%B4%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2022k%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%2C%20%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D0%B0%2C%20%D0%B2%D1%8B%D0%B4%D1%83%D0%BC%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%B8%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%29.md) · анти-слоп: [epstein.md (Shipper)](../Prompts/epstein.md%20%28Shipper%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B3%D0%B0%D0%BD%D1%82%D1%81%D0%BA%D0%B8%D0%B9%20.md-%D1%84%D0%B0%D0%B9%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%ABAI-%D1%81%D0%BB%D0%BE%D0%BF%D0%B0%C2%BB%20%D0%B2%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B5%20%28%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D1%82%D0%B5%D0%BD%D0%B8%2C%20%D1%8D%D0%BC%D0%BE%D0%B4%D0%B7%D0%B8%2C%20~350%20%D0%98%D0%98-%D1%81%D0%BB%D0%BE%D0%B2%29.md)
- Где берут и ставят скиллы: [agent-skills — реестр скиллов + CLI](agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/plugin87/ux-ui-agent-skills](https://github.com/plugin87/ux-ui-agent-skills) · Демо: [plugin87.github.io/ux-ui-agent-skills](https://plugin87.github.io/ux-ui-agent-skills/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/27794)

#AI #Skills #Дизайн #Frontend #ClaudeCode #Ресурсы
