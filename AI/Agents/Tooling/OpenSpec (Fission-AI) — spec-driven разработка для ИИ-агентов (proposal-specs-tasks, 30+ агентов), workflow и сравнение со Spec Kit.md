---
создал заметку: 2026-09-14T23:10:00
author: WhiteK0T
tags:
  - AI
  - Agents
  - SpecDriven
  - Workflow
  - ClaudeCode
  - OpenSource
  - Инструменты
Источник:
  - https://github.com/Fission-AI/OpenSpec
---

# 📐 OpenSpec — spec-driven разработка для ИИ-агентов

**OpenSpec** ([github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec), автор **Fission-AI**, **MIT**, TypeScript, ~68k★, активен) — лёгкий фреймворк **spec-driven development (SDD)**: заставляет ИИ-агента сперва **согласовать спецификацию в Markdown**, а уже потом писать код. Идея — убрать «агент нафантазировал не то»: сначала proposal + требования + план задач, ревью человеком, затем реализация по чеклисту. Ставится как CLI и подключается к **30+ ИИ-ассистентам** (Claude Code, Cursor, Copilot, Windsurf, Amazon Q, CodeRabbit и др.) через слэш-команды.

> [!info] Зачем это (проблема, которую решает)
> «Vibe-coding» вслепую ломается на нетривиальных задачах: агент теряет контекст, переписывает не то, дублирует. OpenSpec вводит **артефакт-контракт** между тобой и агентом: спецификация версионируется в репо, агент реализует **ровно** согласованное, а не своё представление. Особо полезно на **brownfield** (существующий код), не только на новых проектах.

## 🔄 Workflow (4 фазы)

| Фаза | Команда | Что происходит |
| :--- | :--- | :--- |
| **Explore** | `/opsx:explore` | обсуждаешь варианты с агентом до коммита к решению |
| **Propose** | `/opsx:propose <идея>` | агент создаёт папку изменения: `proposal.md`, `specs/`, `design.md`, `tasks.md` |
| **Apply** | `/opsx:apply` | агент реализует задачи по чеклисту из `tasks.md` |
| **Archive** | `/opsx:archive` | завершённое изменение уходит в архив, `specs/` обновляются |

Синтаксис вызова зависит от агента: `/opsx:propose`, `/opsx-propose`, `@opsx-propose`, `$openspec-propose`.

## 🗂️ Структура (что генерится)

```
openspec/
  changes/
    <имя-изменения>/
      proposal.md   # зачем и рамки (rationale + scope)
      specs/        # требования с конкретными сценариями (обычный Markdown)
      design.md     # технический подход
      tasks.md      # чеклист реализации
  ...               # после archive — актуальные specs проекта
```
Ключевое: **specs — это простой Markdown со сценариями**, не DSL. Ревьюишь как обычный текст, держишь в git.

## 📦 Установка

Нужен **Node.js 20.19.0+**:
```bash
npm install -g @fission-ai/openspec@latest
cd your-project
openspec init            # инициализация + инструкции для агента
openspec update          # обновить инструкции агента (после апдейтов)
```
> [!tip] Быстрый старт «руками агента»
> В README есть setup-промпт: вставляешь его в кодинг-агент — он сам ставит CLI, гоняет `openspec init` и проверяет результат.

**CLI-команды:** `init`, `update`, `list`, `show`, `validate` (проверить спеки), `archive`. `validate` полезен в CI — ловит расхождения спеки и реализации.

## ⚖️ OpenSpec vs [Spec Kit](Spec%20Kit%20%28GitHub%29%20%E2%80%94%20%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B4%D0%BE%20%D0%BA%D0%BE%D0%B4%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D0%B4%D0%B0%D0%B2%D0%BD%D0%BE%20%D1%81%20%D0%BF%D1%80%D0%B5%D1%84%D0%B8%D0%BA%D1%81%D0%BE%D0%BC%20speckit%2C%20%D0%B8%D1%85%2010%20%D0%B0%20%D0%BD%D0%B5%206%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%2040%29.md) (GitHub)

| | **OpenSpec** | **Spec Kit (GitHub)** |
| :--- | :--- | :--- |
| Философия | fluid, iterative, лёгкий | thorough, но тяжеловесный |
| Фазовые ворота | мягкие, итеративные | жёсткие phase-gates |
| Стек | Node/TypeScript | Python + много Markdown |
| Позиционирование | brownfield + greenfield, от личных проектов до enterprise | больше про строгий процесс |

Сам README OpenSpec про Spec Kit: *«Thorough but heavyweight… OpenSpec is lighter and lets you iterate freely»*. То есть выбор — **строгий процесс (Spec Kit)** против **гибких итераций (OpenSpec)**.

## ⚠️ Нюансы

> [!caution] На что обратить внимание
> - **Телеметрия включена по умолчанию** (анонимно: имена команд + версия). Отключить: `openspec config set telemetry.enabled false` или переменной окружения.
> - **Дисциплина важнее тула:** пользы ноль, если писать спеки формально и не ревьюить. Ценность — в честном `proposal`/`tasks`, а не в самом факте установки.
> - **Stores (Beta):** кросс-репо планирование через отдельный planning-репозиторий (общие спеки на команду/несколько репо) — пока бета.
> - **Токены:** фаза proposal/specs тратит контекст агента; на больших изменениях это заметные токены (= деньги на платных моделях).

## 🖥️ Применимость на системах владельца

Это Node-CLI + Markdown, платформонезависимо:

| Система | Как |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | `npm i -g @fission-ai/openspec` (нужен Node ≥20.19); подключаешь к своему кодинг-агенту (Claude Code и др.) |
| **Entware / RT-AX56U** | ➖ неактуально: разработка идёт на десктопе, где стоит агент; роутер ни при чём |

## 🔗 Связанные заметки

- Прямой конкурент (строгий процесс): [Spec Kit (GitHub)](Spec%20Kit%20%28GitHub%29%20%E2%80%94%20%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B4%D0%BE%20%D0%BA%D0%BE%D0%B4%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D0%B4%D0%B0%D0%B2%D0%BD%D0%BE%20%D1%81%20%D0%BF%D1%80%D0%B5%D1%84%D0%B8%D0%BA%D1%81%D0%BE%D0%BC%20speckit%2C%20%D0%B8%D1%85%2010%20%D0%B0%20%D0%BD%D0%B5%206%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%2040%29.md)
- Агент, к которому это цепляется: [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

## 🔗 Ссылки

- Репозиторий: [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) (MIT, TypeScript) · пакет: `@fission-ai/openspec`

#AI #Agents #SpecDriven #Workflow #ClaudeCode #OpenSource #Инструменты
