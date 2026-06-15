---
создал заметку: 2026-06-14T05:30:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - Шпаргалка
  - Версионирование
Источник:
  - https://git-scm.com/docs
  - https://git-scm.com/book/ru/v2
---

# 🗺️ Git — карта команд (шпаргалка)

Сводный указатель по всем заметкам серии Git: команда → что делает → ссылка на подробный разбор. Сгруппировано по этапам работы. Это «оглавление» для быстрого прыжка; детали, опции и подводные камни — внутри каждой заметки.

## 🧭 Ментальная модель: три зоны + удалёнка

```text
рабочее дерево  ──add──►  индекс (staging)  ──commit──►  репозиторий  ──push──►  сервер (origin)
   файлы                  «что уйдёт»                  история          ◄──fetch/pull──
```

Почти все команды двигают данные между этими зонами. Удерживая модель в голове, легко понять, «куда» и «откуда» работает любая команда.

## ⚙️ Настройка и создание

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git config` | идентичность, опции, алиасы (3 уровня) | [config](config.md) |
| `git init` | создать новый репозиторий | [init](init.md) |
| `git clone` | скопировать существующий с сервера | [clone](clone.md) |
| `.gitignore` | какие файлы не отслеживать | [.gitignore](gitignore.md) |

## 🔄 Базовый ежедневный цикл

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git status` | что изменено/проиндексировано | [status](status.md) |
| `git add` | проиндексировать (staging) | [add](add.md) |
| `git diff` | посмотреть изменения (дерево/индекс/коммиты) | [diff](diff.md) |
| `git commit` | зафиксировать снимок | [commit](commit.md) |
| `git log` | история коммитов | [log](log.md) |
| `git show` | детали одного коммита/объекта | [show](show.md) |

## ↩️ Отмена и восстановление

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git restore` | вернуть файл / снять из индекса | [restore](restore.md) |
| `git reset` | сдвинуть ветку, снять коммиты (soft/mixed/hard) | [reset](reset.md) |
| `git revert` | отменить коммит **новым** коммитом (безопасно для push) | [revert](revert.md) |
| `git stash` | временно спрятать правки | [stash](stash.md) |
| `git clean` | удалить неотслеживаемый мусор | [clean](clean.md) |
| `git reflog` | журнал HEAD — **восстановить** потерянное | [reflog](reflog.md) |

## 🌿 Ветки и интеграция

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git branch` | список/создание/удаление веток | [branch](branch.md) |
| `git switch` | переключение веток | [switch](switch.md) |
| `git merge` | слить ветку в текущую | [merge](merge.md) |
| `git rebase` | перенести коммиты, линейная история | [rebase](rebase.md) |
| `git cherry-pick` | скопировать отдельный коммит | [cherry-pick](cherry-pick.md) |
| `git tag` | метки версий (релизы) | [tag](tag.md) |

## 🌐 Работа с удалёнкой

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git remote` | управление ссылками на сервера | [remote](remote.md) |
| `git fetch` | забрать с сервера (без слияния) | [fetch](fetch.md) |
| `git pull` | fetch + merge/rebase | [pull](pull.md) |
| `git push` | отправить коммиты на сервер | [push](push.md) |

## 🗂️ Файлы: перемещение и удаление

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git mv` | переместить/переименовать | [mv](mv.md) |
| `git rm` | удалить отслеживаемый файл (`--cached` — перестать отслеживать) | [rm](rm.md) |

## 🔍 Инспекция и отладка

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git blame` | кто/когда ввёл строку | [blame](blame.md) |
| `git bisect` | двоичный поиск коммита с багом | [bisect](bisect.md) |
| `git log -L` / `git show` | история строк / детали коммита | [log](log.md) · [show](show.md) |

## 🧩 Большие проекты

| Команда | Зачем | Заметка |
| :--- | :--- | :--- |
| `git submodule` | вложенные репозитории (зависимости) | [submodule](submodule.md) |

## ⚡ Типичные рецепты

```bash
# Старт нового проекта
git init -b main && git add -A && git commit -m "Первый коммит"
git remote add origin <url> && git push -u origin main

# Ежедневно: обновиться → поработать → отправить
git pull --rebase --autostash
# ...правки...
git add -A && git commit -m "..." && git push

# Завести ветку под задачу и вернуть в main
git switch -c feature
# ...коммиты...
git switch main && git merge feature

# Срочно переключиться, не теряя правок
git stash && git switch hotfix
# ...починил...
git switch feature && git stash pop

# Откатить опубликованный коммит
git revert <hash> && git push

# «Всё сломал» — вернуться к серверу
git fetch origin && git reset --hard origin/main
```

## 🛟 «Спасательные» команды (когда паника)

| Ситуация | Что делать |
| :--- | :--- |
| снёс коммиты `reset --hard`/`rebase` | [`git reflog`](reflog.md) → `git reset --hard <hash>` |
| незавершённый merge/rebase/cherry-pick | `--abort` (см. [merge](merge.md)/[rebase](rebase.md)/[cherry-pick](cherry-pick.md)) |
| `push` отклонён (`fetch first`) | [`git pull --rebase`](pull.md) → `git push` |
| ищу, какой коммит сломал | [`git bisect`](bisect.md) |
| случайно закоммитил секрет | [`git rm --cached`](rm.md) + [.gitignore](gitignore.md) + ротация секрета |

## 🔗 Ссылки

- Полная документация: [git-scm.com/docs](https://git-scm.com/docs)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)

#Git #VCS #Шпаргалка #Версионирование
