---
создал заметку: 2026-07-24T17:00:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - CLI
  - Kimi
  - MoonshotAI
  - Кодинг
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/26503
  - https://github.com/MoonshotAI/kimi-code
  - https://moonshotai.github.io/kimi-code/
---

# 🌙 Kimi Code CLI (MoonshotAI) — терминальный ИИ-агент кода

**Kimi Code CLI** ([github.com/MoonshotAI/kimi-code](https://github.com/MoonshotAI/kimi-code)) — терминальный ИИ-агент для кода от китайской **Moonshot AI**: читает и правит код, гоняет shell-команды, ищет файлы, тянет веб-страницы и сам планирует шаги. Ставится одной командой (single-binary, **Node.js для установки не нужен**), «из коробки» работает с моделями **Kimi** (актуальная — **Kimi K3**, 2.8T MoE, 1M контекст, вышла 16.07.2026), но может быть настроен и на **другие совместимые провайдеры**. MIT, TypeScript, ~4900★, активная разработка.

> [!warning] «Похоронили Claude Code» — это заголовок ради кликов
> Пост подаёт Kimi как «убийцу Claude Code» с «фишками, которых нет в Claude Code». По факту **бо́льшая часть этих фишек в [Claude Code](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) уже есть**, а сам Kimi Code CLI **сделан по образу и подобию Claude Code** (те же `/login`, `/mcp-config`, субагенты, ACP, hooks). Сверка «фишек»:
> | «Есть у Kimi, нет у Claude Code» (пост) | Реально |
> | :--- | :--- |
> | «скинуть скрин экрана как ввод» | у Kimi упор на **видео-ввод** (можно бросить запись экрана/демо-клип). Но **Claude Code тоже принимает изображения/скриншоты** — «чего нет у CC» тут неверно; отличие — именно видео |
> | «`/mcp-config` в диалоге без ручного JSON» | ✅ у Kimi это есть. Но и в Claude Code MCP настраивается командами (`claude mcp add …`), не только руками |
> | «встроенные субагенты coder/explore/plan в изолированном контексте» | ✅ есть у Kimi. **Субагенты есть и в Claude Code** (Task/кастомные агенты в изолированном контексте) |
> | «ACP → Zed/JetBrains» | ✅ честное отличие: Kimi «из коробки» говорит по [Agent Client Protocol](https://agentclientprotocol.com/) (`kimi acp`). У Claude Code своя интеграция с IDE |
>
> Итого: **реальные отличия** — видео-ввод, single-binary без Node, ACP «из коробки» и, главное, **дешёвые модели Kimi**. «Похороны Claude Code» — маркетинг.

> [!caution] «БЕСПЛАТНО» — только сам CLI, не модель
> Код CLI открыт (**MIT**) — да. Но «мозги» — это **облачные модели Moonshot**: при `/login` выбираешь **Kimi Code OAuth** (тариф kimi.com) **или API-ключ Moonshot Open Platform**. Серьёзный агентский прогон K3 стоит денег (**API ~$3 / $15 за 1M вход/выход токенов**, $0.30 за кэш-вход); бесплатный лимит если и есть — небольшой. Плюс это **китайский облачный сервис**: код и промпты уходят на серверы Moonshot — учитывай приватность/комплаенс (как и с [GLM](GLM%205.2%20%E2%80%94%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%B0%D1%8F%20%D0%BA%D0%B8%D1%82%D0%B0%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20LLM%20%28Z.ai%2C%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3%29.md)).

> [!note] Какой репозиторий актуален
> Старый [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) (Python) **сворачивается** и «перетекает» в **kimi-code** (TypeScript) — это и есть «Kimi Code CLI». Ставь именно его; установка `kimi-code` автоматически переносит конфиг и сессии старого `kimi-cli`.

## 🧩 Что реально умеет (по README)

- **Video input** — бросаешь запись экрана/демо-клип, агент «смотрит» то, что сложно описать словами (референс-клип → LUT, длинное видео → короткое, запись экрана → рабочий код).
- **AI-native MCP** — `/mcp-config`: добавить/править/авторизовать MCP-серверы **разговором**, без ручного JSON (плюс `kimi mcp add/list/remove` в старом CLI).
- **Субагенты** `coder` / `explore` / `plan` — параллельная работа в **изолированных контекстах**, основной диалог остаётся чистым.
- **Lifecycle hooks** — локальные команды в ключевых точках: гейтить рискованные вызовы, аудит, десктоп-уведомления, своя автоматизация.
- **ACP** — управлять сессией прямо из **Zed / JetBrains** (`kimi acp`).
- **TUI + shell-режим**, marketplace скиллов/MCP/датасорсов с указанием уровня доверия.

## 🛠️ Установка

```sh
# macOS / Linux (официальный скрипт; Node.js не требуется):
curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash
# Windows (PowerShell) — нужен Git for Windows (Git Bash):
# irm https://code.kimi.com/kimi-code/install.ps1 | iex

kimi --version     # проверка
cd твой-проект && kimi
# внутри: /login → Kimi Code OAuth или API-ключ Moonshot
```

> [!tip] Скрипт из поста немного другой
> В посте команда `curl -LsSf https://code.kimi.com/install.sh | bash` — она ведёт на **старый** `kimi-cli`. Для актуального Kimi Code CLI бери путь **`/kimi-code/install.sh`** из официального README (выше).

> [!caution] `curl | bash` — на свой риск
> Любой `curl … | bash` исполняет удалённый скрипт немедленно. Ставь только с официального `code.kimi.com`, при желании — сперва скачай скрипт и просмотри его.

## 🖥️ Применимость на системах владельца

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ single-binary ставится скриптом; нужен только доступ к моделям Moonshot (или свой совместимый провайдер) |
| **Entware / RT-AX56U** | ❌ практически неактуально: официальный бинарь под armv7-роутер не рассчитан, а сама модель всё равно облачная. Гоняй с десктопа |

## 🔗 Связанные заметки

- Другой терминальный агент от китайского вендора: [MiMo Code — терминальный AI-агент (Xiaomi)](MiMo%20Code%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%B4%D0%BB%D1%8F%20%D0%BA%D0%BE%D0%B4%D0%B0%20%D1%81%20%D0%B4%D0%BE%D0%BB%D0%B3%D0%BE%D0%B9%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%D1%8E%20%28Xiaomi%29.md)
- Эталон, с которым сравнивают: [Claude Code — гайд](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · Переключение провайдеров: [CCS (Claude Code Switch)](ProxyLLM/CCS%20%28Claude%20Code%20Switch%29%20%E2%80%94%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BA%D0%BB%D1%8E%D1%87%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D0%B8%20%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20Claude%20Code.md)
- Обзор рынка: [Сводная таблица AI-агентов для программирования](%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B8%D1%8E%D0%BD%D1%8C%202026%29.md) · Китайская LLM рядом: [GLM 5.2 (Z.ai)](GLM%205.2%20%E2%80%94%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%B0%D1%8F%20%D0%BA%D0%B8%D1%82%D0%B0%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20LLM%20%28Z.ai%2C%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/MoonshotAI/kimi-code](https://github.com/MoonshotAI/kimi-code) · Документация: [moonshotai.github.io/kimi-code](https://moonshotai.github.io/kimi-code/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26503)

#AI #Агенты #CLI #Kimi #MoonshotAI #Кодинг #Инструменты
