---
создал заметку: 2026-06-19T15:05:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Workflow
  - Loops
  - CodeReview
  - PR
Источник:
  - https://loops.elorm.xyz/loops/pr-self-review
---

# 🔍🔁 PR Self-Review — петля самостоятельного ревью diff

Петля из каталога [Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md): агент сам ревьюит **свой собственный diff как старший ревьюер** — ищет баги, краевые случаи, плохие имена, недостающие тесты — чинит найденное и проходит так **три круга**, прежде чем выносить PR на чужое ревью. Цель — снять очевидные замечания заранее.

## ⚙️ Параметры

| Параметр | Значение |
| :--- | :--- |
| Триггер | ручной |
| Check-команда (между итерациями) | `git diff main...HEAD` |
| Макс. итераций | **3** |
| Условие выхода | три прохода завершены, критичных замечаний нет |
| Файлы | не требуются (prompt-only); опц. `download` → `.cursor/loops/pr-self-review/` |
| Совместимость | Claude Code, Cursor, Codex |

## 📋 Kickoff-промпт (вставить агенту как есть)

```text
Start the "PR Self-Review" loop. Goal: three clean self-review passes on the
current diff. Max iterations: 3. Between iterations run: git diff main...HEAD.
Exit when: three passes complete with no critical findings.
Step 1: Review the diff like a senior reviewer. Fix findings, then re-review.
```

**По-русски, что он делает на каждом круге:** (1) посмотреть `git diff main...HEAD`, разобрать как строгий ревьюер — баги, edge-cases, нейминг, нет ли пропущенных тестов; (2) починить замечания **с минимальным охватом** (highest-severity первыми); (3) переревью — убедиться, что прошлые находки закрыты. Выход — когда 3 круга прошли без критики.

## 🚀 Как запустить

- **Claude Code:** вставь промпт после того, как реализовал ветку, но **до** запроса чужого ревью / открытия PR. По духу — самоуправляемая `/loop`-задача (см. [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)).
- Работает на **любом git-репозитории** (в т.ч. на этом vault'е — diff правок заметок тоже можно так прогнать).

> [!tip] Подгони базовую ветку
> `main...HEAD` сравнивает текущую ветку с `main`. Если основная ветка другая — поменяй на `master...HEAD` (как в этом репозитории) или нужную базу.

## 🛡️ Anti-gaming (встроенные предохранители)

Нельзя менять check-команду или критерий выхода ради «успеха», нельзя пропускать/отключать проверки. Если после нескольких итераций затык — **остановиться и доложить** блокеры, а не имитировать чистый проход.

## 💡 Когда использовать

- Перед открытием PR / запросом ревью — чтобы прийти к ревьюеру с уже вычищенным diff.
- Хорошо комбинируется с петлями «до зелёного» (тесты/CI) и с [Docs Sync After Edits](Docs%20Sync%20After%20Edits%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D1%81%D0%B8%D0%BD%D1%85%D1%80%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8.md) — сначала довести код и доки, потом self-review.
- Три прохода — это про дисциплину, а не магию: на больших diff'ах смотри, чтобы агент не «замыливал» крупные проблемы ради формального закрытия кругов.

## 🔗 Ссылки

- Страница петли: [loops.elorm.xyz/loops/pr-self-review](https://loops.elorm.xyz/loops/pr-self-review)
- Связанные: [Каталог петель Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md) · [Autoloop TDD](Autoloop%20TDD%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20TDD%20%28red-green-refactor%29.md) · [Docs Sync After Edits](Docs%20Sync%20After%20Edits%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D1%81%D0%B8%D0%BD%D1%85%D1%80%D0%BE%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8.md) · [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

#AI #Claude_Code #Workflow #Loops #CodeReview #PR
