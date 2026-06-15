---
создал заметку: 2026-06-13T22:00:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - clone
  - Удалённый_репозиторий
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-clone
  - https://git-scm.com/book/ru/v2
---

# 🌿 git clone — клонировать репозиторий

`git clone` создаёт **локальную копию** удалённого репозитория: скачивает всю историю, создаёт рабочее дерево и сразу настраивает [remote](remote.md) `origin` с привязкой веток. Это стартовая команда, с которой обычно начинается работа над чужим/своим проектом с сервера.

## 🧬 Что делает clone

Одной командой:

1. создаёт каталог и инициализирует в нём `.git`;
2. скачивает **всю историю** (все коммиты, ветки, теги);
3. заводит remote с именем **`origin`**, указывающий на источник;
4. создаёт remote-tracking ветки `origin/*`;
5. переключается (checkout) на ветку по умолчанию (`main`/`master`).

> [!info] clone = init + remote add + fetch + checkout
> По сути `git clone` — это удобная обёртка: создать репозиторий, добавить `origin`, забрать всё ([fetch](fetch.md)) и развернуть рабочее дерево. Поэтому после clone сразу можно работать — ничего донастраивать не нужно.

## 📝 Базовое использование

```bash
git clone <url>                      # в каталог по имени репозитория
git clone <url> my-dir               # в указанный каталог
git clone git@github.com:User/repo.git        # по SSH
git clone https://github.com/User/repo.git    # по HTTPS
```

URL определяет протокол — см. [SSH против HTTPS](remote.md):

| Протокол | URL | Аутентификация |
| :--- | :--- | :--- |
| **SSH** | `git@github.com:User/repo.git` | по SSH-ключу |
| **HTTPS** | `https://github.com/User/repo.git` | логин + токен (PAT) |

## ⚙️ Полезные опции

| Опция | Описание |
| :--- | :--- |
| **`-b <ветка>` / `--branch`** | checkout указанной ветки (или тега) вместо дефолтной |
| **`--depth <n>`** | **поверхностный** клон: только последние `n` коммитов (быстро, легко) |
| **`--single-branch`** | забрать только одну ветку, а не все |
| **`--no-checkout` / `-n`** | склонировать без разворачивания рабочего дерева |
| **`--bare`** | «голый» репозиторий без рабочего дерева (для серверов/зеркал) |
| **`--mirror`** | полное зеркало всех refs (для бэкапа/миграции) |
| **`--recurse-submodules`** | сразу склонировать и подмодули |
| **`-o <имя>` / `--origin`** | назвать remote не `origin`, а иначе |
| **`-j <n>` / `--jobs`** | параллельные потоки (с подмодулями) |
| **`--filter=blob:none`** | partial clone: без содержимого блобов (подтянет по требованию) |

## ⚡ Частые сценарии

### Быстрый поверхностный клон (CI, большой репозиторий)

```bash
git clone --depth 1 <url>            # только последний коммит
git clone --depth 1 --single-branch -b main <url>
```

Экономит трафик/время, когда история не нужна (сборка, разовый просмотр). Позже можно дотянуть полную историю: `git fetch --unshallow`.

### Клон конкретной ветки

```bash
git clone -b develop <url>           # сразу на ветке develop
```

### Клон с подмодулями

```bash
git clone --recurse-submodules <url>
# если забыл — уже после клона:
git submodule update --init --recursive
```

### Зеркало для бэкапа/переезда

```bash
git clone --mirror <url> repo-backup.git    # все refs, bare
```

> [!tip] bare против mirror
> `--bare` — голый репозиторий без рабочего дерева (нельзя редактировать файлы, только хранить/отдавать). `--mirror` — то же, но зеркалит **все** refs (ветки, теги, заметки) и настраивает push-обновление всех ссылок: удобно для миграции репозитория на другой сервер.

## 🩺 Частые вопросы

- **«Permission denied (publickey)»** — SSH-ключ не настроен/не добавлен на GitHub; склонируй по HTTPS или настрой [SSH-ключи](../../Network/SSH/SSH-Ключи.md).
- **Очень долго/много весит** — `git clone --depth 1` (shallow), при необходимости `git fetch --unshallow` позже.
- **Подмодули пустые** — клонировал без `--recurse-submodules`: `git submodule update --init --recursive`.
- **Хочу склонировать в текущий (непустой) каталог** — clone требует пустой/новый каталог; вариант: клонировать рядом и перенести `.git`, либо `git init` + `git remote add` + `git pull`.
- **Куда указывает origin** — `git remote -v` (см. [remote](remote.md)); сменить — `git remote set-url`.

## 💎 Резюме

- `git clone <url> [каталог]` — полная копия + настроенный `origin` + готовое рабочее дерево.
- Быстро/легко: `--depth 1 --single-branch`; позже — `git fetch --unshallow`.
- Конкретная ветка: `-b <ветка>`; подмодули: `--recurse-submodules`.
- Зеркало/бэкап: `--mirror`; сервер без рабочего дерева: `--bare`.
- После clone сразу работают [fetch](fetch.md)/[pull](pull.md)/[push](push.md).

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-clone](https://git-scm.com/docs/git-clone)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git remote](remote.md) · [git fetch](fetch.md) · [git pull](pull.md) · [git push](push.md)

#Git #VCS #clone #Удалённый_репозиторий #Версионирование
