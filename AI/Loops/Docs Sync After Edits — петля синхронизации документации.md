---
создал заметку: 2026-06-19T15:10:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Workflow
  - Loops
  - Документация
Источник:
  - https://loops.elorm.xyz/loops/docs-sync-after-edits
---

# 📄🔁 Docs Sync After Edits — петля синхронизации документации

Петля из каталога [Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md): после правок кода агент **подтягивает документацию под изменения** — README, API-референс, инлайн-комментарии — находит устаревшие места по diff'у и приводит их в соответствие, проверяя точность.

## ⚙️ Параметры

| Параметр | Значение |
| :--- | :--- |
| Триггер | ручной |
| Check-команда (между итерациями) | `git diff main...HEAD --name-only` |
| Макс. итераций | **3** |
| Условие выхода | все затронутые доки обновлены и проверены |
| Читает / пишет | читает README, `docs/`, комментарии в коде; пишет обновления туда же |
| Совместимость | Claude Code, Cursor (`/loop`), Codex, любой кодинг-агент |

## 📋 Kickoff-промпт (вставить агенту как есть)

```text
Start the "Docs Sync After Edits" loop. Goal: documentation matches the current
code changes. Max iterations: 3. Between iterations run:
git diff main...HEAD --name-only. Exit when: all affected docs are updated and
verified. Step 1: Review the diff, find stale docs, update them, and verify accuracy.
```

**По-русски, что он делает:** (1) посмотреть, какие файлы изменены (`git diff main...HEAD --name-only`); (2) найти **устаревшие** упоминания в доках, связанные с этими изменениями; (3) обновить документацию под текущий код; (4) сверить точность с diff'ом. Выход — когда все затронутые доки приведены в порядок (макс. 3 круга).

## 🚀 Как запустить

- **Claude Code:** вставь промпт **после** того, как закончил правки кода, но перед коммитом/PR. Самоуправляемая `/loop`-задача (см. [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)).
- Применимо к **любому** репозиторию, где код и доки живут вместе.

> [!tip] Для этого Obsidian-vault'а тоже работает
> Здесь «документация» — это README со списком заметок: после добавления/переноса заметок такая петля может находить расхождения между файлами и ссылками в README. Не забудь сменить базовую ветку на `master...HEAD`.

## 🛡️ Anti-gaming (встроенные предохранители)

Hardened-петля: запрещено менять check-команду/критерий ради формального закрытия, пропускать проверку «точности». Если непонятно, как должна выглядеть дока — лучше доложить, чем выдумать.

## 💡 Когда использовать

- После изменений API/поведения/CLI — чтобы README и референс не «отставали» от кода.
- В связке: [PR Self-Review](PR%20Self-Review%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20diff.md) (вычистить код) → **Docs Sync** (подтянуть доки) → [Changelog Sync After Ship](Changelog%20Sync%20After%20Ship%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D1%87%D0%B5%D0%B9%D0%BD%D0%B4%D0%B6%D0%BB%D0%BE%D0%B3%D0%B0.md) (после релиза).
- Ограничение: петля синхронизирует доки **под уже сделанные** правки, а не пишет документацию с нуля.

## 🔗 Ссылки

- Страница петли: [loops.elorm.xyz/loops/docs-sync-after-edits](https://loops.elorm.xyz/loops/docs-sync-after-edits)
- Связанные: [Каталог петель Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md) · [Changelog Sync After Ship](Changelog%20Sync%20After%20Ship%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D1%87%D0%B5%D0%B9%D0%BD%D0%B4%D0%B6%D0%BB%D0%BE%D0%B3%D0%B0.md) · [PR Self-Review](PR%20Self-Review%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20diff.md) · [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

#AI #Claude_Code #Workflow #Loops #Документация
