---
создал заметку: 2026-06-14T01:00:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - config
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/book/ru/v2
---

# 🌿 git config — настройки Git

`git config` читает и пишет настройки Git: имя/почту автора, поведение команд, алиасы, инструменты слияния. Настройки хранятся в обычных текстовых INI-файлах на **трёх уровнях** (system → global → local), где более узкий уровень переопределяет более широкий.

## 🧬 Три уровня настроек

| Уровень | Флаг | Файл | Область |
| :--- | :--- | :--- | :--- |
| **system** | `--system` | `/etc/gitconfig` | для всех пользователей машины |
| **global** | `--global` | `~/.gitconfig` (или `~/.config/git/config`) | для всех репозиториев пользователя |
| **local** | `--local` | `.git/config` | только **текущий** репозиторий |

> [!info] Приоритет: local > global > system
> Чем «уже» уровень, тем выше приоритет. `local` (репозиторий) перекрывает `global` (пользователь), а тот — `system`. Без флага `git config` пишет в **local** (если ты внутри репозитория). Узнать, откуда взялось значение: `git config --show-origin <ключ>`.

## 📝 Базовое использование

```bash
git config user.name "WhiteK0T"          # записать (по умолчанию в local)
git config --global user.email "you@x"   # записать в global
git config user.name                     # прочитать значение
git config --list                        # все настройки
git config --list --show-origin          # + из какого файла каждая
git config --unset user.name             # удалить ключ
git config --edit                        # открыть конфиг в редакторе
```

## 👤 Идентичность — самое важное

Без имени и почты Git не даст коммитить («Please tell me who you are»):

```bash
git config --global user.name "WhiteK0T"
git config --global user.email "you@example.com"
```

> [!tip] Разная личность для разных проектов
> Глобально задаёшь основную личность, а в конкретном репозитории переопределяешь **локально** (без `--global`): `git config user.email "work@company.com"`. Так рабочие и личные коммиты идут под разными адресами. Проверить, что применится здесь: `git config user.email`.

## ⚙️ Частые настройки

```bash
# редактор для сообщений коммитов
git config --global core.editor "nvim"

# имя ветки по умолчанию при git init
git config --global init.defaultBranch main

# поведение git pull (линейная история — см. заметку про pull)
git config --global pull.rebase true
git config --global rebase.autoStash true

# автоматически проставлять upstream при первом push
git config --global push.autoSetupRemote true

# цветной вывод (обычно уже включено)
git config --global color.ui auto

# глобальный .gitignore (мусор ОС/IDE)
git config --global core.excludesFile ~/.gitignore_global

# окончания строк (Linux/macOS — input; Windows — true)
git config --global core.autocrlf input
```

## 🔗 Алиасы — сокращения команд

`git config alias.<имя> "<команда>"` создаёт короткие команды:

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
```

Теперь `git st`, `git lg`, `git unstage <файл>` и т.п. Алиас с `!` запускает шелл-команду:

```bash
git config --global alias.visual '!gitk'
```

## 🔧 Формат файла

Конфиг — это обычный INI, можно править руками (`git config --edit` или редактором):

```ini
[user]
    name = WhiteK0T
    email = you@example.com
[init]
    defaultBranch = main
[alias]
    lg = log --oneline --graph --decorate --all
[pull]
    rebase = true
```

> [!note] Ключ = секция.имя
> `git config user.name` соответствует секции `[user]`, ключу `name`. Точка разделяет секцию и параметр. Для под-секций: `[remote "origin"]` → ключ `remote.origin.url`.

## 🩺 Частые вопросы

- **«Please tell me who you are»** — не задана идентичность: `git config --global user.name/user.email`.
- **Откуда взялось значение** — `git config --show-origin <ключ>` (покажет файл и уровень).
- **Локально или глобально?** — `--global` для своей машины в целом; без флага (local) — только этот репозиторий (перекрывает global).
- **Случайно записал не на тот уровень** — перезапиши с нужным флагом или `git config --unset` и задай заново; либо правь файл напрямую (`--edit`).
- **Нужны разные имена/почты на проект** — задавай локально в каждом репозитории; глобально оставь основную.

## 💎 Резюме

- Уровни: `--system` < `--global` < `--local` (приоритет растёт; по умолчанию пишет в local).
- Обязательное: `git config --global user.name` и `user.email`.
- Полезное: `init.defaultBranch main`, `pull.rebase true`, `push.autoSetupRemote true`, `core.excludesFile`.
- Алиасы: `git config --global alias.lg "log --oneline --graph --all"`.
- Откуда значение: `git config --show-origin`; править руками: `git config --edit`.

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-config](https://git-scm.com/docs/git-config)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git init — defaultBranch](init.md) · [git pull — pull.rebase](pull.md) · [.gitignore — core.excludesFile](gitignore.md) · [git log — алиас lg](log.md)

#Git #VCS #config #Версионирование
