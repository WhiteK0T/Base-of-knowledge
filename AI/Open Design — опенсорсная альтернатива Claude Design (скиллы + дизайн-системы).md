---
создал заметку: 2026-06-17T20:40:00
author: WhiteK0T
tags:
  - AI
  - Дизайн
  - OpenDesign
  - ClaudeCode
  - MCP
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/25906
  - https://github.com/nexu-io/open-design
  - https://open-design.ai/
---

# 🎨 Open Design — опенсорсная альтернатива Claude Design (скиллы + дизайн-системы)

**Open Design** ([github.com/nexu-io/open-design](https://github.com/nexu-io/open-design), [open-design.ai](https://open-design.ai/)) — local-first **опенсорсная альтернатива Claude Design**: генерирует сайты, мобильные интерфейсы, презентации, картинки и видео в фирменных стилях по описанию. Ключевая идея — **сам инструмент не содержит ИИ-агента**: «движком» выступают уже установленные у тебя кодинг-агенты ([Claude Code](Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md), Codex, Cursor, Gemini, Copilot, Kimi и др.), а Open Design даёт им **скиллы, дизайн-системы и плагины**. Apache-2.0, зрелый проект (v0.11.0, 17.06.2026, >2300 коммитов), TypeScript.

> [!warning] Отделяем факты от рекламы поста
> | Заявление поста | Реально |
> | :--- | :--- |
> | «юзаем Claude Design бесплатно / клон» | это **независимая** альтернатива (Apache-2.0), **не форк/клон** продукта Anthropic; «тот же артефакт-first подход, без лок-ина» |
> | «бесплатно» | бесплатен **сам тул**; генерацию делает **твой агент** (Claude Code/Codex…) — это его токены/подписка |
> | «132 скилла и 150 дизайн-систем» | числа **гуляют по версиям** (README заявляет 259+/142+, пост — 132/150) — маркетинговые счётчики; порядок верный: **сотни скиллов, ~150 брендстайлов** |
> | «цепляет 16 ИИ-агентов автоматически» | подхватывает агентов **из PATH** (заявлено 17–22 CLI); своей «интеллектуальности» у него нет — это слой поверх агента |

## 🧬 Как работает (artifact-first)

- **Агент-движок из PATH**: Open Design не несёт свою LLM — берёт Claude Code / Codex / Cursor / Gemini / Copilot / Kimi / OpenCode и т.д., переключаются «в один клик».
- **`DESIGN.md`** — схема бренда из 9 секций (палитра, типографика, отступы, моушн, голос, анти-паттерны). В репозитории — **~150 готовых систем** (Apple, Notion, Linear, Stripe, Vercel, Airbnb, Tesla, Anthropic, Figma, Supabase…).
- **Artifact-first цикл**: агент выдаёт артефакт → к нему привязаны плагин/скилл/`DESIGN.md` → результат стримится в **песочницу (sandboxed iframe)**, правится прямо там или через чат.
- **Реальный HTML/CSS** на выходе — его можно дальше «достраивать кодом» в Cursor/Codex/Claude Code или экспортнуть.
- **MCP-сервер** (stdio): любой MCP-совместимый агент из другого репо может читать файлы проектов Open Design как структурированный API.

## 📤 Что генерит и экспорт

- Прототипы **web / mobile / desktop**, **слайды/презентации**, дашборды, **картинки и видео**, моушн (HyperFrames).
- Экспорт: **HTML / PDF / PPTX / MP4**; HTML можно закинуть прямо в проект и продолжать как код.

## 📦 Установка

Нужен **Node ~24** и **pnpm 10.33.x** (для CLI/из исходников).

```bash
# Десктоп-приложение (проще всего): скачать с open-design.ai (macOS/Windows), zero-config

# CLI + интеграция с конкретным агентом:
curl -fsSL https://open-design.ai/install.sh | sh -s <agent>
#   <agent> = claude | codex | cursor | copilot | openclaw | antigravity | gemini

# Из исходников:
git clone https://github.com/nexu-io/open-design.git && cd open-design
corepack enable && pnpm install
pnpm tools-dev run web

# Docker:
docker compose up -d        # затем http://localhost:7456
```

| Система | Как ставить |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | `nodejs` (~24) + `pnpm`, затем `install.sh <agent>` **или** из исходников / **Docker** (`docker compose up -d`) |
| **macOS / Windows** | десктоп-приложение с сайта (zero-config) |
| **Entware / RT-AX56U** | **неприменимо** — тяжёлая генерация дизайна + нужен кодинг-агент; не для роутера |

> [!caution] `curl … | bash` и нужен реальный агент
> Установщик одной строкой исполняет скачанный скрипт — доверяешь репо (Apache-2.0, активный), ок; иначе глянь `install.sh` или ставь из исходников/Docker. И помни: без установленного агента (Claude Code/Codex…) генерировать **нечем** — Open Design сам по себе не рисует.

## 💡 Когда полезно

- Уже пользуешься [Claude Code](Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)/Cursor/Codex и хочешь **быстрые брендовые макеты** (лендинги, слайды, прототипы) с экспортом в HTML/PPTX без вендор-лока.
- Нужны **готовые дизайн-системы** известных брендов как стартовая точка.
- **Не** ждёт чудес «бесплатности»: счёт идёт по твоему агенту/модели; и для серьёзной вёрстки результат всё равно дорабатывается руками.
- Для генерации **целого сайта в код** — смежно с [AI Website Cloner](Agents/AI%20Website%20Cloner%20%E2%80%94%20%D0%BA%D0%BB%D0%BE%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2%20%D0%B2%20Next.js%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2.md).

## 🔗 Ссылки

- Репозиторий: [github.com/nexu-io/open-design](https://github.com/nexu-io/open-design) · сайт: [open-design.ai](https://open-design.ai/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/25906)
- Связанные: [Claude Code — гайд](Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [MCP — серверы Model Context Protocol](Agents/Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) · [Сводная таблица AI-агентов](Agents/%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md) · [AI Website Cloner](Agents/AI%20Website%20Cloner%20%E2%80%94%20%D0%BA%D0%BB%D0%BE%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2%20%D0%B2%20Next.js%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2.md)

#AI #Дизайн #OpenDesign #ClaudeCode #MCP #Инструменты
