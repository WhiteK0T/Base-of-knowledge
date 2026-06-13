---
создал заметку: 2026-06-13T16:00:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - status
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-status
  - https://git-scm.com/book/ru/v2
---

# 🌿 git status — состояние рабочего дерева

`git status` показывает, **в каком состоянии репозиторий прямо сейчас**: что изменено, что проиндексировано (staging), что не отслеживается, и насколько ветка опережает/отстаёт от удалённой. Это «приборная панель» Git — самая частая команда в работе.

## 🧬 Что именно показывает status

`git status` разносит файлы по трём зонам (см. [`git add`](add.md)):

| Зона в выводе | Что значит | Как туда попало |
| :--- | :--- | :--- |
| **Changes to be committed** | проиндексировано — **уйдёт** в коммит | `git add` |
| **Changes not staged for commit** | отслеживается, изменено, **но не** в индексе | правка без `git add` |
| **Untracked files** | Git про файл **не знает** | новый файл |

Плюс служебная строка вверху: на какой ветке (`On branch master`), отношение к удалённой (`Your branch is up to date` / `ahead` / `behind`), идёт ли merge/rebase.

> [!info] status ничего не меняет
> Команда **только читает** состояние — выполнять её можно сколько угодно и в любой момент, она безопасна. Это первое, что стоит делать перед `add`/`commit`/`pull`.

## 📝 Базовое использование

```bash
git status
```

Типичный вывод:

```text
On branch master
Your branch is ahead of 'origin/master' by 1 commit.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   VCS/Git/add.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        VCS/Git/status.md
```

Git прямо в выводе **подсказывает команды** — `git add`, `git restore --staged`, `git restore` — для каждого раздела.

## ⚙️ Основные опции и флаги

| Опция | Описание | Пример |
| :--- | :--- | :--- |
| **`-s` / `--short`** | Компактный вывод (по строке на файл, двухбуквенные коды). | `git status -s` |
| **`-b` / `--branch`** | Показать строку ветки даже в коротком режиме. | `git status -sb` |
| **`--show-stash`** | Показать, есть ли записи в stash. | `git status --show-stash` |
| **`-u` / `--untracked-files[=mode]`** | Детализация untracked: `no` / `normal` / `all` (показать файлы внутри новых каталогов). | `git status -uall` |
| **`--ignored`** | Показать также **игнорируемые** (`.gitignore`) файлы. | `git status --ignored` |
| **`-v` / `--verbose`** | Показать **diff** проиндексированных изменений. `-vv` — ещё и не проиндексированных. | `git status -v` |
| **`--porcelain`** | Стабильный машиночитаемый формат (для скриптов). | `git status --porcelain` |

## 🔠 Короткий формат — `git status -s`

```bash
git status -sb
```

```text
## master...origin/master [ahead 1]
M  README.md
 M VCS/Git/add.md
?? VCS/Git/status.md
```

Каждая строка — **два столбца статуса**: левый = **индекс (staging)**, правый = **рабочее дерево**.

| Код | Значение |
| :--- | :--- |
| **`M`** | modified (изменён) |
| **`A`** | added (новый, добавлен в индекс) |
| **`D`** | deleted (удалён) |
| **`R`** | renamed (переименован) |
| **`C`** | copied |
| **`U`** | unmerged (конфликт слияния) |
| **`??`** | untracked (не отслеживается) |
| **`!!`** | ignored (при `--ignored`) |

> [!tip] Как читать два столбца
> - `M ` (M + пробел) — изменение **в индексе**, рабочее дерево чисто → файл застейджен полностью.
> - ` M` (пробел + M) — изменение **только в рабочем дереве**, не добавлено.
> - `MM` — застейджена одна правка, а поверх неё файл изменён **ещё раз** (новые правки не в индексе).
> - `??` — новый файл, Git его не отслеживает.

## 🔀 Состояние веток и операций

Верхняя строка отражает связь с **upstream** (удалённой веткой):

- **`up to date`** — совпадает с `origin`.
- **`ahead N`** — у тебя на `N` коммитов больше → пора `git push`.
- **`behind N`** — сервер впереди на `N` → пора `git pull`.
- **`diverged`** — и опередил, и отстал → нужен `pull --rebase` или merge.

Во время незавершённых операций status подскажет состояние: `You have unmerged paths` (конфликт merge), `interactive rebase in progress`, `You are currently cherry-picking` — с подсказками `--continue` / `--abort`.

## 🩺 Частые вопросы

- **«Untracked files» при `git status -s` показывает каталог, а не файлы** — по умолчанию режим `normal`; чтобы развернуть содержимое новых каталогов: `git status -uall`.
- **Файла нет в выводе, хотя он создан** — он попадает под `.gitignore`. Проверить: `git status --ignored` или `git check-ignore -v <файл>`.
- **`modified`, хотя «ничего не менял»** — часто это права доступа (`chmod`) или перевод строк (CRLF/LF). Глянуть точную разницу: `git diff <файл>`.
- **Нужен статус в скрипте** — парси `git status --porcelain` (стабильный формат), а не человекочитаемый вывод.

## 💎 Резюме

- Полная картина: `git status`; компактно: `git status -sb`.
- Левый столбец короткого вывода = индекс, правый = рабочее дерево.
- `ahead`/`behind` подсказывают `push`/`pull`.
- Untracked внутри каталогов: `-uall`; игнорируемые: `--ignored`; для скриптов: `--porcelain`.
- Git сам печатает команды-подсказки (`add`, `restore`, `restore --staged`).

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-status](https://git-scm.com/docs/git-status)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git add — индексация](add.md) · [git commit — фиксация](commit.md)

#Git #VCS #status #Версионирование
