---
создал заметку: 2026-06-13T19:30:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - remote
  - Удалённый_репозиторий
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-remote
  - https://git-scm.com/book/ru/v2
---

# 🌿 git remote — удалённые репозитории

`git remote` управляет **именованными ссылками на удалённые репозитории** (GitHub, GitLab, свой сервер). «Remote» — это короткое имя (обычно `origin`) для URL, чтобы не писать его каждый раз в [`fetch`](fetch.md)/[`push`](push.md)/[`pull`](pull.md).

## 🧬 Что такое remote

Remote — это **закладка**: имя + URL. У одного репозитория может быть несколько remotes (напр. `origin` — свой форк, `upstream` — оригинальный проект).

| Имя | Смысл (по соглашению) |
| :--- | :--- |
| **`origin`** | основной удалённый репозиторий (откуда клонировали) |
| **`upstream`** | оригинал, от которого сделан форк (для синхронизации) |

> [!info] origin — это просто имя
> `origin` не магия, а имя по умолчанию, которое `git clone` даёт источнику. Его можно переименовать или иметь несколько remotes с любыми именами.

## 📝 Базовое использование

```bash
git remote                       # список имён remotes
git remote -v                    # + их URL (fetch и push отдельно)
git remote add <имя> <url>       # добавить remote
git remote remove <имя>          # удалить
git remote rename <старое> <новое>
git remote show <имя>            # подробности (ветки, tracking, URL)
```

Типичный `git remote -v`:

```text
origin    git@github.com:WhiteK0T/Base-of-knowledge.git (fetch)
origin    git@github.com:WhiteK0T/Base-of-knowledge.git (push)
```

## ⚙️ Основные подкоманды

| Команда | Описание |
| :--- | :--- |
| **`git remote -v`** | список remotes с URL (fetch/push) |
| **`git remote add <имя> <url>`** | добавить новый remote |
| **`git remote remove <имя>`** (`rm`) | удалить remote |
| **`git remote rename <ст> <нов>`** | переименовать |
| **`git remote show <имя>`** | детально: ветки, что отслеживается, что устарело |
| **`git remote set-url <имя> <url>`** | сменить URL (напр. HTTPS → SSH) |
| **`git remote get-url <имя>`** | вывести текущий URL |
| **`git remote prune <имя>`** | удалить локальные ссылки на ветки, которых уже нет на сервере |

## 🔗 SSH против HTTPS

URL remote задаёт протокол доступа:

| Протокол | URL | Аутентификация |
| :--- | :--- | :--- |
| **SSH** | `git@github.com:User/repo.git` | по SSH-ключу (без ввода пароля) |
| **HTTPS** | `https://github.com/User/repo.git` | логин + токен (PAT) |

```bash
# переключить origin с HTTPS на SSH
git remote set-url origin git@github.com:WhiteK0T/Base-of-knowledge.git
```

> [!tip] SSH удобнее для частых push
> С SSH-ключом не нужно каждый раз вводить токен. См. заметки по [SSH-ключам](../../Network/SSH/SSH-Ключи.md). Проверить, что remote на SSH: `git remote -v` (URL начинается с `git@`).

## 🍴 Сценарий форка — origin + upstream

При работе с форком держат два remotes: свой (`origin`) и оригинал (`upstream`):

```bash
git remote add upstream git@github.com:original/project.git
git fetch upstream                       # забрать обновления оригинала
git merge upstream/main                  # влить их в свою ветку
git remote -v                            # проверить оба
```

## 🧹 Чистка устаревших ссылок

После удаления веток на сервере локальные `remotes/origin/*` остаются «висеть»:

```bash
git remote prune origin          # удалить устаревшие remote-tracking ветки
git remote prune origin --dry-run   # показать, что удалится
git fetch --prune                # то же самое заодно с fetch
```

## 🩺 Частые вопросы

- **«fatal: No configured push destination»** — нет remote: `git remote add origin <url>`.
- **Сменить аккаунт/протокол** — `git remote set-url origin <новый-url>` (не нужно удалять и добавлять заново).
- **`git branch -r` показывает удалённые ветки, которых уже нет** — `git remote prune origin` или `git fetch --prune`.
- **Где хранится** — в `.git/config` (секции `[remote "origin"]`). Можно править руками, но лучше через `git remote`.

## 💎 Резюме

- Посмотреть: `git remote -v`; детально: `git remote show origin`.
- Добавить/сменить URL: `git remote add` / `git remote set-url`.
- Форк: `origin` (свой) + `upstream` (оригинал).
- Почистить мёртвые ветки: `git remote prune origin` / `git fetch --prune`.
- Remote — это имя для URL; дальше им оперируют [`fetch`](fetch.md), [`push`](push.md), [`pull`](pull.md).

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-remote](https://git-scm.com/docs/git-remote)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git fetch](fetch.md) · [git push](push.md) · [git pull](pull.md)

#Git #VCS #remote #Удалённый_репозиторий #Версионирование
