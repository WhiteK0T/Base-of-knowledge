---
создал заметку: 2026-06-13T19:00:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - branch
  - Ветки
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-branch
  - https://git-scm.com/book/ru/v2
---

# 🌿 git branch — управление ветками

`git branch` создаёт, показывает, переименовывает и удаляет **ветки**. Сама по себе она **не переключает** на ветку (это [`git switch`](switch.md)) — она управляет их списком и свойствами.

## 🧬 Что такое ветка в Git

Ветка — это **лёгкий подвижный указатель** на коммит (по сути файл в `.git/refs/heads/` с одним хешем). Когда ты коммитишь, указатель **текущей** ветки сам сдвигается на новый коммит. `HEAD` — это указатель на «текущую ветку».

> [!info] Ветка ≈ стикер на коммите
> Создать ветку — почти бесплатно: Git просто пишет хеш в новый ref, ничего не копируя. Поэтому ветвление в Git дёшево и поощряется (feature-ветка под каждую задачу).

## 📝 Базовое использование

```bash
git branch                   # список локальных веток (текущая помечена *)
git branch -v                # + последний коммит каждой ветки
git branch <имя>             # создать ветку (НЕ переключаясь на неё)
git branch <имя> <старт>     # создать от коммита/ветки/тега
git branch -d <имя>          # удалить ветку (только слитую)
git branch -m <старое> <новое>   # переименовать
```

> [!note] branch создаёт, switch переключает
> `git branch feature` лишь **заводит** ветку, оставляя тебя на текущей. Чтобы создать **и сразу перейти** — `git switch -c feature` (или старое `git checkout -b feature`). `git branch` удобен, когда нужно поставить «метку» на коммит, не уходя с текущей ветки.

## ⚙️ Основные опции

| Опция | Описание | Пример |
| :--- | :--- | :--- |
| **(без аргументов)** | список локальных веток | `git branch` |
| **`-a` / `--all`** | все ветки: локальные + удалённые (`remotes/...`) | `git branch -a` |
| **`-r` / `--remotes`** | только удалённые отслеживаемые ветки | `git branch -r` |
| **`-v` / `-vv`** | + последний коммит; `-vv` — ещё и upstream + ahead/behind | `git branch -vv` |
| **`-d` / `--delete`** | удалить **слитую** ветку (безопасно) | `git branch -d feature` |
| **`-D`** | принудительно удалить (даже **не** слитую) | `git branch -D feature` |
| **`-m` / `--move`** | переименовать ветку | `git branch -m new-name` |
| **`-c` / `--copy`** | скопировать ветку (с её конфигом) | `git branch -c backup` |
| **`--merged` / `--no-merged`** | показать ветки, уже/ещё не слитые в текущую | `git branch --merged` |
| **`-u <upstream>` / `--set-upstream-to`** | привязать ветку к удалённой | `git branch -u origin/main` |
| **`--show-current`** | вывести имя текущей ветки (для скриптов) | `git branch --show-current` |
| **`-f` / `--force`** | переустановить существующую ветку на другой коммит | `git branch -f main HEAD~2` |

## 🌿 Создание и переименование

```bash
git branch feature                 # создать от текущего HEAD
git branch hotfix main             # создать от другой ветки/коммита
git branch -m old-name new-name    # переименовать конкретную
git branch -m new-name             # переименовать ТЕКУЩУЮ ветку
```

> [!tip] Переименовать master → main
> ```bash
> git branch -m master main          # локально
> git push -u origin main            # запушить новую
> git push origin --delete master    # удалить старую на сервере
> ```
> На GitHub ещё нужно сменить «ветку по умолчанию» в настройках репозитория.

## 🗑️ Удаление веток

```bash
git branch -d feature        # безопасно: откажет, если ветка НЕ слита
git branch -D feature        # принудительно (потеря несмёрженных коммитов!)
git push origin --delete feature   # удалить ветку на удалённом сервере
```

> [!warning] `-D` может потерять работу
> `git branch -d` бережёт: не даст удалить ветку с коммитами, которых нет в текущей. `git branch -D` удаляет **в любом случае** — несмёрженные коммиты станут недостижимы (искать потом в [`git reflog`](log.md)). Используй `-D` осознанно.

## 🔗 Связь с удалёнными ветками (tracking)

«Отслеживаемая» (upstream) ветка — это удалённая ветка, с которой локальная синхронизируется (`git pull`/`git push` без аргументов, отображение ahead/behind в [`git status`](status.md)).

```bash
git branch -vv                       # увидеть upstream и ahead/behind у всех веток
git branch -u origin/main            # привязать ТЕКУЩУЮ к origin/main
git branch --unset-upstream          # отвязать
```

> [!info] Локальные ≠ удалённые ветки
> `git branch` показывает **локальные** ветки. `git branch -r` — `remotes/origin/...` (снимок состояния сервера на момент последнего `git fetch`, не «вживую»). Полный список — `git branch -a`. Удалённые refs обновляются `git fetch`/`git remote prune`.

## 🧹 Чистка слитых веток

```bash
git branch --merged                  # какие ветки уже влиты в текущую (можно удалять)
git branch --merged | grep -v '\*\|main\|master' | xargs -r git branch -d
git fetch --prune                    # убрать локальные ссылки на удалённые ветки, которых уже нет
```

## 🩺 Частые вопросы

- **`branch` против `switch`** — `branch` управляет списком/свойствами веток; `switch` переключает текущую. Создать+перейти: `git switch -c`.
- **«error: branch not fully merged»** — `-d` защищает от потери коммитов; если точно не нужны — `-D`.
- **Не вижу удалённых веток** — сделай `git fetch`, затем `git branch -r`/`-a`.
- **Удалил ветку с нужными коммитами** — пока не сработал GC, найди хеш в `git reflog` и пересоздай: `git branch <имя> <hash>`.
- **Как зовут текущую ветку в скрипте** — `git branch --show-current` (или `git rev-parse --abbrev-ref HEAD`).

## 💎 Резюме

- Список: `git branch` (`-a` все, `-r` удалённые, `-vv` + upstream/ahead-behind).
- Создать: `git branch <имя>` (без перехода); создать и перейти: `git switch -c <имя>`.
- Переименовать: `git branch -m`; удалить: `-d` (безопасно) / `-D` (принудительно).
- Привязать к удалённой: `git branch -u origin/<имя>`; почистить: `git fetch --prune`.

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-branch](https://git-scm.com/docs/git-branch)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git switch — переключение веток](switch.md) · [git log / reflog](log.md) · [git status — состояние дерева](status.md)

#Git #VCS #branch #Ветки #Версионирование
