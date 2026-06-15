---
создал заметку: 2026-06-15T12:00:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Ponytail
  - Агенты
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/25819
  - https://github.com/DietrichGebert/ponytail
---

# 🐴 Ponytail — скилл против «графомании» AI-агентов в коде

**Ponytail** — плагин/набор правил для AI-агентов кодинга, который заставляет их писать **минимальный прагматичный код** вместо «простыней». Идея — поведение «лениво-гениального сеньора»: вместо 500 строк агент пишет 5, не жертвуя безопасностью, валидацией и доступностью. Лицензия **MIT**.

## 🧬 Как работает

Перед генерацией кода агент прогоняет запрос через **иерархию решений** (по сути усиленный YAGNI):

1. Это вообще нужно? → не делать (YAGNI).
2. Есть в **стандартной библиотеке**? → использовать её.
3. Есть **нативная** возможность платформы? → использовать её.
4. Уже стоит как **зависимость**? → использовать её.
5. Можно **в одну строку**? → одна строка.
6. Только потом — минимальная рабочая реализация.

> [!info] Что НЕ урезается
> Безопасность, валидация и доступность (a11y) сокращению **не подлежат** — режется только лишний объём/over-engineering, а не качество.

## 📊 Заявленные метрики

Бенчмарки на трёх моделях (Haiku, Sonnet, Opus):

| Показатель | Эффект |
| :--- | :--- |
| Объём кода | **−80…94 %** |
| Стоимость задачи | **−47…77 %** |
| Скорость | **в 3–6× быстрее** |

> [!note] Это цифры авторов
> Метрики — из README проекта, не независимый аудит. Порядок величин правдоподобен (меньше токенов на вывод → дешевле и быстрее), но проверяй на своих задачах.

## 🎚️ Режимы интенсивности

Уровень «агрессивности» сокращения переключается командой `/ponytail`:

| Режим | Смысл |
| :--- | :--- |
| `lite` | мягкое сокращение |
| `full` | по умолчанию |
| `ultra` | максимально жёсткая минимизация |
| `off` | выключить |

Глобально режим задаётся переменной `PONYTAIL_DEFAULT_MODE` (`lite`/`full`/`ultra`/`off`).

## 🧰 Команды

| Команда | Действие |
| :--- | :--- |
| `/ponytail [lite\|full\|ultra\|off]` | задать уровень |
| `/ponytail-review` | проверить текущий diff на over-engineering |
| `/ponytail-audit` | аудит всего репозитория |
| `/ponytail-debt` | собрать отложенные `ponytail:`-сокращения в реестр |
| `/ponytail-help` | краткая справка |

## 📦 Установка

### Claude Code (основной кейс)

```bash
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

См. также заметки [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20гайд.md) и [Claude Code — шпаргалка команд](../Claude%20Code%20%E2%80%94%20шпаргалка%20команд.md).

### Другие агенты

```bash
# Codex
codex plugin marketplace add DietrichGebert/ponytail

# GitHub Copilot CLI
copilot plugin marketplace add DietrichGebert/ponytail
copilot plugin install ponytail@ponytail

# Gemini / Antigravity CLI
gemini extensions install https://github.com/DietrichGebert/ponytail
```

```json
// OpenCode — в opencode.json
{ "plugin": ["./.opencode/plugins/ponytail.mjs"] }
```

Режим «только правила» (ruleset) поддерживают также **Cursor, Windsurf, Cline, Kiro, Aider** — без плагина, через подключение правил.

## ⚙️ Конфигурация

Опциональный конфиг:

| ОС | Путь |
| :--- | :--- |
| **Linux/macOS** (Gentoo тоже) | `~/.config/ponytail/config.json` |
| **Windows** | `%APPDATA%\ponytail\config.json` |

Или просто переменная окружения `PONYTAIL_DEFAULT_MODE`.

## 💡 Когда полезно

- Агент склонен «раздувать» решения, плодить абстракции и бойлерплейт.
- Хочется **дешевле/быстрее** прогонять рутинные задачи (меньше выходных токенов).
- Нужен быстрый аудит уже сгенерированного кода на over-engineering (`/ponytail-review`, `/ponytail-audit`).

> [!warning] Не серебряная пуля
> Жёсткие режимы (`ultra`) могут сокращать там, где явность была бы уместнее (читаемость, расширяемость). Для прод-кода разумнее `full` + ручной review, а `ultra` — для черновиков/прототипов.

## 🔗 Ссылки

- Репозиторий: [github.com/DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/25819)
- Связанные: [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20гайд.md) · [Claude Code — шпаргалка команд](../Claude%20Code%20%E2%80%94%20шпаргалка%20команд.md) · [MCP — серверы Model Context Protocol](../MCP%20%E2%80%94%20серверы%20Model%20Context%20Protocol.md)

#AI #Claude_Code #Ponytail #Агенты #Инструменты
