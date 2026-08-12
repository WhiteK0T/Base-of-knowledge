---
создал заметку: 2026-06-19T15:15:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Workflow
  - Loops
  - Changelog
  - Релизы
Источник:
  - https://loops.elorm.xyz/loops/changelog-sync-after-ship
---

# 📝🔁 Changelog Sync After Ship — петля обновления чейнджлога

Петля из каталога [Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md): после релиза («ship») агент следит, чтобы в **`CHANGELOG.md`** были записи под пользовательские изменения — разбирает свежие коммиты и пишет аккуратные записи в формате **Keep a Changelog** под `[Unreleased]`.

## ⚙️ Параметры

| Параметр | Значение |
| :--- | :--- |
| Триггер | ручной (после релиза) |
| Check-команда (между итерациями) | `git log -5 --oneline` |
| Полная сверка коммитов | `git log $(git describe --tags --abbrev=0 2>/dev/null \|\| echo HEAD~20)..HEAD --oneline` |
| Макс. итераций | **3** |
| Условие выхода | changelog покрывает все видимые пользователю изменения |
| Читает / пишет | читает `CHANGELOG.md` + историю git; пишет в `CHANGELOG.md` (секции `[Unreleased]`: Added / Changed / Fixed) |
| Совместимость | Claude Code, Cursor, Codex, любой кодинг-агент |

## 📋 Kickoff-промпт (вставить агенту как есть)

```text
Start the "Changelog Sync After Ship" loop. Goal: CHANGELOG.md has accurate
[Unreleased] entries for this ship. Max iterations: 3. Between iterations run:
git log -5 --oneline. Exit when: changelog covers all user-visible changes.
Step 1: Review recent commits, write Keep-a-Changelog entries for user-visible
changes, and verify completeness.
```

**По-русски, что он делает:** (1) просмотреть последние коммиты; (2) написать записи **Keep a Changelog** для того, что видит пользователь (Added/Changed/Fixed под `[Unreleased]`); (3) проверить полноту. Выход — когда все пользовательские изменения отражены (макс. 3 круга).

## 🚀 Как запустить

- **Claude Code:** вставь промпт сразу после релиза/мерджа. Самоуправляемая `/loop`-задача (см. [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)).
- Нужен файл **`CHANGELOG.md`** в репозитории (формат [Keep a Changelog](https://keepachangelog.com/)).

> [!note] «User-visible» — ключевой фильтр
> В changelog идут изменения, **заметные пользователю** (фичи, фиксы, ломающие изменения), а не каждый рефакторинг/CI-правка. Петля сама отсеивает «внутреннее» — но проверь, что важное не потерялось и наоборот.

## 🛡️ Anti-gaming (встроенные предохранители)

Запрещено подгонять check-команду/критерий выхода ради формального завершения и пропускать сверку полноты. При неоднозначности — доложить, а не выдумывать записи.

## 💡 Когда использовать

- В конце потока релиза, обычно после [Docs Sync After Edits](Docs%20Sync%20After%20Edits%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D1%81%D0%B8%D0%BD%D1%85%D1%80%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8.md): доки → changelog.
- Удобно с **Conventional Commits**: из аккуратных сообщений коммитов записи собираются почти автоматически.
- Ограничение: завязана на `CHANGELOG.md` и git-историю; если чейнджлога нет — сначала заведи файл.

## 🔗 Ссылки

- Страница петли: [loops.elorm.xyz/loops/changelog-sync-after-ship](https://loops.elorm.xyz/loops/changelog-sync-after-ship)
- Формат: [keepachangelog.com](https://keepachangelog.com/)
- Связанные: [Каталог петель Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md) · [Docs Sync After Edits](Docs%20Sync%20After%20Edits%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D1%81%D0%B8%D0%BD%D1%85%D1%80%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8.md) · [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

#AI #Claude_Code #Workflow #Loops #Changelog #Релизы
