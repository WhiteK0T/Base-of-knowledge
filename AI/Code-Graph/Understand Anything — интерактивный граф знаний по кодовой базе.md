---
создал заметку: 2026-06-17T18:40:00
author: WhiteK0T
tags:
  - AI
  - Программирование
  - АнализКода
  - UnderstandAnything
  - ClaudeCode
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/25895
  - https://github.com/Egonex-AI/Understand-Anything
  - https://understand-anything.com/
---

# 🗺️ Understand Anything — интерактивный граф знаний по кодовой базе

**Understand Anything** ([github.com/Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)) — открытый инструмент, который превращает **любую кодовую базу в интерактивный граф знаний**: сканирует проект, строит карту файлов, функций, классов и зависимостей и даёт **дашборд**, где по коду можно кликать, искать, задавать вопросы и смотреть, что сломает правка. Это **плагин поверх AI-агента** (нативно — [Claude Code](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md); также Cursor, VS Code+Copilot, Gemini CLI, Codex и др.), а не отдельная программа. MIT, ~63k★, v2.7.3 (май 2026), TypeScript.

> [!warning] Отделяем факты от рекламы поста
> Пост обещает «превратит любую программу в наглядную карту в один клик». Сверка с репозиторием:
> | Заявление | Реально |
> | :--- | :--- |
> | «само построит карту» | строит **твой LLM** через агент-хост (Claude Code/Cursor…) — нужен настроенный AI-агент и расходуются токены |
> | «понимает любой код» | структуру даёт детерминированный **Tree-sitter**, смыслы — LLM (может ошибаться/выдумывать на больших проектах) |
> | «отдельная имба» | это **плагин/слой** над агентом, не standalone-приложение и не [MCP](../Agents/Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md)-сервер |
> | поддержка русского | да, контент можно генерить на русском (`--language ru`) |

## 🧬 Как работает

Гибрид «статика + LLM»: факты берутся разбором, объяснения — моделью.

- **Tree-sitter** — детерминированный парсинг: импорты/экспорты, определения, наследование (точные структурные факты, без галлюцинаций).
- **LLM-агенты** — пояснения простым языком, выделение архитектурных слоёв и бизнес-доменов.
- **Конвейер из 6 воркеров**: сканер проекта → анализатор файлов → анализатор архитектуры → построитель «туров» → ревьюер графа → анализатор доменов.

Результат сохраняется локально в `.understand-anything/knowledge-graph.json` и открывается как **интерактивный дашборд** (каждый файл/функция/класс — кликабельный узел).

## ✨ Что умеет

- **Структурный граф** с нечётким и семантическим поиском по узлам.
- **Domain view** — визуализация бизнес-доменов; **слои** (API / Service / Data / UI / Utility).
- **Гайд-туры** по архитектуре в порядке зависимостей (быстро войти в новый проект).
- **Diff impact analysis** — что зацепит правка ещё **до** её внесения (ripple-эффект).
- Вопрос-ответ по коду, wiki-документация, подсказки по 12 языковым концептам (дженерики, замыкания, декораторы…).

## 🔌 С чем работает

| Хост | Как подключается |
| :--- | :--- |
| **Claude Code** | нативный плагин (через marketplace) |
| **Cursor** | авто-обнаружение (`.cursor-plugin/plugin.json`) |
| **VS Code + Copilot** | авто-обнаружение (Copilot v1.108+) |
| **Прочие** | Codex, OpenCode, OpenClaw, Gemini CLI, Pi Agent, Hermes, Cline, Kimi CLI, Trae, Kiro, Antigravity и др. |

## 📦 Установка

Нужен **уже настроенный AI-агент** (например [Claude Code](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)) и Node.js-окружение. Сам плагин ставится одинаково на всех десктоп-дистрибутивах владельца.

```bash
# Внутри Claude Code — через маркетплейс плагинов:
/plugin marketplace add Egonex-AI/Understand-Anything
/plugin install understand-anything
```

```bash
# Универсальный установщик (macOS / Linux):
curl -fsSL https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/main/install.sh | bash
```

```powershell
# Windows (PowerShell):
iwr -useb https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/main/install.ps1 | iex
```

Скрипт клонирует репозиторий в `~/.understand-anything/repo` и делает симлинки под выбранный хост. Контент на русском — флагом `--language ru` (язык диалога тул определяет на первом запуске).

| Система | Как ставить |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | `install.sh` (`curl \| bash`) **или** плагин-команды Claude Code; нужен `nodejs`/`npm` |
| **Entware / RT-AX56U** | **неприменимо** — десктоп-dev-инструмент над AI-агентом, на роутере не запускают |

> [!caution] `curl … | bash` / `iwr | iex` — посмотри, что исполняешь
> Установка одной строкой запускает скачанный скрипт. Доверяешь источнику (репо на 63k★) — ок; иначе сперва глянь `install.sh`/`install.ps1` или ставь через плагин-команды агента.

## 💡 Когда полезно

- **Быстро войти в незнакомый/большой проект** — увидеть структуру, слои, домены и «туры» вместо ручного блуждания по файлам.
- **Оценить риск правки** заранее (diff impact) — что потянет за собой изменение.
- Уже работаешь в [Claude Code](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)/Cursor — это удобная надстройка; помни, что граф строит **твоя модель** (токены) и смысловые подписи стоит перепроверять.
- Не нужен ещё один AI-агент — это **дополнение** к нему; полный список агентов — в [сводной таблице](../Agents/%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md).

## 🔗 Ссылки

- Репозиторий: [github.com/Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) · сайт: [understand-anything.com](https://understand-anything.com/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/25895)
- Связанные: [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [MCP — серверы Model Context Protocol](../Agents/Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) · [Сводная таблица AI-агентов](../Agents/%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md) · [MiMo Code (Xiaomi)](../Agents/MiMo%20Code%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%B4%D0%BB%D1%8F%20%D0%BA%D0%BE%D0%B4%D0%B0%20%D1%81%20%D0%B4%D0%BE%D0%BB%D0%B3%D0%BE%D0%B9%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%D1%8E%20%28Xiaomi%29.md)

#AI #Программирование #АнализКода #UnderstandAnything #ClaudeCode #Инструменты
