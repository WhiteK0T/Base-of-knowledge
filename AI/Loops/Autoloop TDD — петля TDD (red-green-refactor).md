---
создал заметку: 2026-06-19T15:00:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Workflow
  - Loops
  - TDD
  - Тесты
Источник:
  - https://loops.elorm.xyz/loops/autoloop-tdd
---

# 🧪🔁 Autoloop TDD — петля TDD (red → green → refactor)

Петля из каталога [Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md): агент реализует поведение **через тесты-первыми** — пишет падающий тест, добавляет минимум кода, рефакторит и повторяет, пока вся цель не покрыта тестами и сьют не зелёный. Сам себя «пейсит» (self-pace) до условия выхода.

## ⚙️ Параметры

| Параметр | Значение |
| :--- | :--- |
| Триггер | ручной (только промпт) |
| Check-команда (между итерациями) | `npm test` |
| Макс. итераций | **12** |
| Условие выхода | целевое поведение покрыто и все тесты зелёные |
| Файлы | при «download»-режиме кладёт README+kickoff в `.cursor/loops/autoloop-tdd/`; в режиме «только промпт» файлы не нужны |
| Совместимость | Claude Code, Cursor (`/loop`), Codex, любой кодинг-агент (вставкой промпта) |

## 📋 Kickoff-промпт (вставить агенту как есть)

```text
Start the "Autoloop TDD" loop. Goal: implement the target behavior test-first
with a green suite. Max iterations: 12. Between iterations run: npm test.
Exit when: target behavior is covered and all tests pass.
Step 1: Write a failing test for the next behavior, implement the minimum code
to pass, refactor, and repeat. Self-pace this loop. After each iteration, run the
check command, read the output, and only continue if the exit condition is not met.
```

**По-русски, что он делает:** на каждой итерации — (1) написать **падающий** тест на следующее поведение → (2) минимальный код, чтобы он позеленел → (3) рефакторинг при зелёном сьюте → прогнать `npm test`, прочитать вывод и продолжать, только пока условие выхода не достигнуто (максимум 12 кругов).

## 🚀 Как запустить

- **Claude Code:** вставь kickoff-промпт в чат; по сути это самоуправляемая задача в духе `/loop` — «делай и проверяй, пока не выполнится условие выхода» (см. [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)). Дай агенту право запускать тест-команду.
- **Cursor / Codex:** поддерживается `/loop` или просто вставка промпта.

## 🛡️ Anti-gaming (встроенные предохранители)

Петля запрещает агенту «жульничать» ради зелёного: **не менять check-команду**, не пропускать/отключать тесты, не ослаблять ассерты, не имитировать ложный успех. Если застрял после нескольких итераций — остановиться и доложить, а не подгонять.

## 💡 Когда использовать и как адаптировать

- Берёт там, где есть **чёткое проверяемое поведение** и тест-раннер. Идеально для нового модуля/функции с понятными кейсами.
- **`npm test` — это про JS/Node.** Под другой стек поменяй check-команду в промпте: `pytest -q` (Python), `go test ./...` (Go), `cargo test` (Rust), `mvn -q test` (Java) и т.п.
- Не для разовых правок «на один тест» — выигрыш на **итеративной** разработке поведения.
- Для этого Obsidian-репозитория **неприменима** (нет кода/тестов) — заметка как переиспользуемый рецепт под кодовые проекты.

## 🔗 Ссылки

- Страница петли: [loops.elorm.xyz/loops/autoloop-tdd](https://loops.elorm.xyz/loops/autoloop-tdd)
- Связанные: [Каталог петель Loops!](Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md) · [PR Self-Review (петля ревью diff)](PR%20Self-Review%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20diff.md) · [Claude Code — гайд](../Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

#AI #Claude_Code #Workflow #Loops #TDD #Тесты
