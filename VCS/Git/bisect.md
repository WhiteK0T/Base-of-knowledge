---
создал заметку: 2026-06-14T04:30:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - bisect
  - Отладка
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-bisect
  - https://git-scm.com/book/ru/v2
---

# 🌿 git bisect — двоичный поиск «плохого» коммита

`git bisect` находит коммит, который **внёс баг**, методом двоичного поиска: ты указываешь заведомо «хороший» и «плохой» коммиты, а Git раз за разом переключает тебя на середину диапазона и спрашивает, есть ли баг. За `log₂(N)` шагов он сужает тысячи коммитов до одного виновного.

## 🧬 Идея

Баг где-то между «работало» (`good`) и «сломалось» (`bad`). Git делит диапазон пополам, ты проверяешь середину → отвечаешь `good`/`bad` → Git делит оставшуюся половину, и так далее. **1000 коммитов → ~10 проверок.**

```text
good ────────────────●──────────────── bad
                 проверяем середину →
        good ──────●────── bad   (баг во второй половине)
                ...сужаем до одного коммита
```

## 📝 Базовый цикл

```bash
git bisect start                 # начать сессию
git bisect bad                   # текущий коммит — СЛОМАН
git bisect good <old-commit>     # вот этот старый — РАБОТАЛ

# Git переключает на середину. Проверяешь (собираешь/тестируешь) и отвечаешь:
git bisect good                  # на этом коммите бага НЕТ
git bisect bad                   # на этом коммите баг ЕСТЬ
# ... повторяешь, пока Git не назовёт виновный коммит ...

git bisect reset                 # ВАЖНО: завершить и вернуться на исходную ветку
```

В конце Git печатает: `<hash> is the first bad commit` — с автором, датой и сообщением.

> [!warning] Не забудь `git bisect reset`
> Во время bisect ты в **detached HEAD** (Git прыгает по коммитам). `git bisect reset` обязателен в конце — он возвращает на ветку, где ты был. Без него останешься «висеть» на случайном коммите.

## ⚙️ Подкоманды и опции

| Команда | Описание |
| :--- | :--- |
| **`git bisect start [<bad> <good>]`** | начать (можно сразу задать границы) |
| **`git bisect bad [<commit>]`** | пометить коммит как сломанный |
| **`git bisect good [<commit>]`** | пометить как рабочий |
| **`git bisect skip`** | пропустить коммит, который нельзя проверить (не собирается) |
| **`git bisect reset [<commit>]`** | завершить сессию, вернуться (по умолчанию — на исходную ветку) |
| **`git bisect log`** | показать ход текущего поиска |
| **`git bisect replay <файл>`** | повторить поиск из сохранённого лога |
| **`git bisect run <скрипт>`** | **автоматический** bisect (см. ниже) |
| **`git bisect terms`** | переименовать `good/bad` (напр. `old/new` для не-багов) |

## 🤖 Автоматизация — `git bisect run`

Если баг ловится скриптом/тестом, Git пройдёт весь поиск **сам**:

```bash
git bisect start HEAD <old-good>
git bisect run ./test.sh
git bisect reset
```

Правило кода выхода скрипта: **0 = good**, **1–124 (кроме 125) = bad**, **125 = skip** (не удалось проверить).

```bash
# пример: баг = падение конкретного теста
git bisect run pytest tests/test_parser.py::test_edgecase
# или одной командой
git bisect run sh -c 'make && ./app --check'
```

> [!tip] `bisect run` — суперсила
> С воспроизводимым тестом `git bisect run` находит регрессию **без ручного участия**: соберёт и проверит каждый шаг сам. Главное — чтобы скрипт возвращал правильный код выхода (0 — норма, 1 — баг).

## ⚡ Частые сценарии

```bash
# знаю, что в v1.2 работало, в HEAD сломано
git bisect start HEAD v1.2
git bisect run ./repro.sh
git bisect reset

# коммит не собирается — пропустить
git bisect skip
```

## 🩺 Частые вопросы

- **Коммит не собирается/не проверяется** — `git bisect skip` (Git выберет соседний).
- **Запутался, хочу заново** — `git bisect reset` и начать сначала; ход виден в `git bisect log`.
- **Остался в detached HEAD** — это нормально во время bisect; `git bisect reset` вернёт на ветку.
- **«Регрессия» не бага, а фичи** — переименуй термины: `git bisect start --term-old=works --term-new=broken` или `git bisect terms`.
- **Нужно повторить тот же поиск** — `git bisect log > bisect.log`, потом `git bisect replay bisect.log`.

## 💎 Резюме

- `git bisect` — двоичный поиск коммита-виновника за `log₂(N)` шагов.
- Цикл: `start` → `bad` → `good <old>` → отвечать `good`/`bad` → `reset`.
- Не проверяется коммит — `skip`; всегда заверши `reset` (выйти из detached HEAD).
- Автоматизация: `git bisect run <скрипт>` (0=good, 1=bad, 125=skip).

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-bisect](https://git-scm.com/docs/git-bisect)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git log — найти коммиты](log.md) · [git show — осмотреть коммит](show.md) · [git switch — detached HEAD](switch.md) · [git revert — откатить виновника](revert.md)

#Git #VCS #bisect #Отладка #Версионирование
