---
создал заметку: 2026-06-13T19:40:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - fetch
  - Удалённый_репозиторий
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-fetch
  - https://git-scm.com/book/ru/v2
---

# 🌿 git fetch — забрать изменения с сервера

`git fetch` скачивает коммиты, ветки и теги с [удалённого репозитория](remote.md) и обновляет **remote-tracking ветки** (`origin/main` и т.п.), **не трогая** твои локальные ветки и рабочее дерево. Это «безопасный» способ узнать, что появилось на сервере, ничего не сливая.

> [!info] fetch ≠ pull
> `git fetch` только **скачивает** и обновляет `origin/*`. Он **не сливает** изменения в твою ветку и не меняет файлы. [`git pull`](pull.md) = `fetch` + автоматический `merge` (или `rebase`). Поэтому `fetch` безопасен: посмотреть, потом решить, как интегрировать.

## 🧬 Что обновляет fetch

```text
сервер (origin)  ──git fetch──►  remote-tracking ветки    локальные ветки
   main                            origin/main      (не меняются!)  main
   feature                         origin/feature                   feature
```

`git fetch` двигает только `origin/*` — снимок состояния сервера. Твоя `main` остаётся на месте, пока ты явно не сольёшь `origin/main` ([merge](pull.md)/rebase) или не сделаешь [pull](pull.md).

## 📝 Базовое использование

```bash
git fetch                        # забрать со всех remote текущей ветки (обычно origin)
git fetch origin                 # явно с origin
git fetch origin main            # только ветку main
git fetch --all                  # со всех настроенных remotes
git fetch --tags                 # забрать и теги
```

После `fetch` сравни своё с сервером:

```bash
git log HEAD..origin/main        # какие коммиты есть на сервере, но нет у меня
git diff HEAD origin/main        # построчная разница
git status                       # покажет "behind N" если сервер ушёл вперёд
```

## ⚙️ Полезные опции

| Опция | Описание |
| :--- | :--- |
| **`--all`** | забрать со всех remotes |
| **`-p` / `--prune`** | удалить локальные `origin/*`, которых уже нет на сервере |
| **`--tags`** | скачать все теги |
| **`--dry-run`** | показать, что было бы скачано, не скачивая |
| **`-v` / `--verbose`** | подробный вывод |
| **`--depth <n>`** | поверхностный fetch (последние `n` коммитов) — для больших реп |
| **`--unshallow`** | дотянуть полную историю у shallow-клона |

> [!tip] Привычка: fetch перед работой
> `git fetch` в начале дня (или `git fetch --prune`) показывает актуальное состояние сервера без риска что-то сломать. Решение «сливать/перебазировать» принимаешь уже осознанно — см. [pull](pull.md).

## 🧹 Чистка устаревших веток

```bash
git fetch --prune                # убрать ссылки на удалённые ветки, которых уже нет
git fetch --prune --tags         # заодно подчистить теги
```

Без `--prune` ветки, удалённые на сервере, продолжают «висеть» в `git branch -r`.

## 🩺 Частые вопросы

- **Сделал fetch, а файлы не изменились** — так и должно быть: `fetch` обновляет только `origin/*`. Чтобы применить — `git merge origin/main`, `git rebase origin/main` или сразу [`git pull`](pull.md).
- **«behind N» в status** — сервер впереди; забери и слей (`pull`) или перебазируйся.
- **`origin/feature` остался после удаления на сервере** — `git fetch --prune`.
- **Огромный репозиторий долго тянется** — `git fetch --depth=1` (shallow), позже `--unshallow`.

## 💎 Резюме

- `git fetch` — безопасно скачать состояние сервера в `origin/*`, ничего не сливая.
- Сравнить: `git log HEAD..origin/main`, `git diff HEAD origin/main`.
- Применить потом: `merge`/`rebase`/[`pull`](pull.md).
- Чистка: `git fetch --prune`; теги: `--tags`.

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-fetch](https://git-scm.com/docs/git-fetch)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git remote](remote.md) · [git pull](pull.md) · [git push](push.md)

#Git #VCS #fetch #Удалённый_репозиторий #Версионирование
