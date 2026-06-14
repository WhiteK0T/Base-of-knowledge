---
создал заметку: 2026-06-13T20:00:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - pull
  - Удалённый_репозиторий
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-pull
  - https://git-scm.com/book/ru/v2
---

# 🌿 git pull — забрать и влить изменения

`git pull` = [`git fetch`](fetch.md) + интеграция в **текущую** ветку. То есть скачать коммиты с [сервера](remote.md) и сразу слить их в свою ветку — `merge` (по умолчанию) или `rebase`. Это самая частая команда «обновиться».

```text
git pull  =  git fetch  +  git merge origin/<ветка>
git pull --rebase  =  git fetch  +  git rebase origin/<ветка>
```

> [!info] pull меняет твою ветку и файлы
> В отличие от безопасного [`fetch`](fetch.md), `pull` **двигает локальную ветку и обновляет рабочее дерево**. Если есть конфликты — их придётся разрешать. Поэтому полезно перед pull иметь чистое дерево (или `--autostash`).

## 🔀 merge против rebase при pull

| Режим | Что делает | История |
| :--- | :--- | :--- |
| **`git pull`** (merge, по умолчанию) | вливает `origin/main` merge-коммитом | ветвистая, с merge-коммитами |
| **`git pull --rebase`** | перематывает твои локальные коммиты **поверх** свежих серверных | линейная, чистая |

```bash
git pull                         # merge-стратегия
git pull --rebase                # rebase-стратегия (линейная история)
git pull --ff-only               # только fast-forward, иначе отказать
```

> [!tip] Рекомендуемый режим — `--rebase --autostash`
> ```bash
> git pull --rebase --autostash
> ```
> `--rebase` даёт линейную историю без «мусорных» merge-коммитов, `--autostash` временно прячет незакоммиченные правки и возвращает их после. Удобно закрепить глобально:
> ```bash
> git config --global pull.rebase true
> git config --global rebase.autoStash true
> ```

## ⚙️ Полезные опции

| Опция | Описание |
| :--- | :--- |
| **`--rebase` / `-r`** | перебазировать вместо merge |
| **`--no-rebase`** | принудительно merge (если в конфиге включён rebase) |
| **`--ff-only`** | только fast-forward; при расхождении — отказать (безопасно) |
| **`--autostash`** | спрятать/вернуть локальные правки вокруг pull |
| **`--no-commit`** | слить, но не создавать merge-коммит автоматически |
| **`--prune`** | заодно подчистить устаревшие `origin/*` |
| **`-v` / `--verbose`** | подробный вывод |

## ⚔️ Конфликты при pull

Если твои и серверные правки задели одни строки — будет конфликт:

```text
CONFLICT (content): Merge conflict in file.txt
```

Разрешение:

```bash
# 1. открыть файлы с маркерами <<<<<<< ======= >>>>>>>, выбрать нужное
git status                       # покажет "Unmerged paths"
# 2. отредактировать, убрать маркеры
git add file.txt                 # пометить как разрешённый
# 3. завершить:
git merge --continue             # (или git commit) для merge-режима
git rebase --continue            # для --rebase
# отменить и вернуться как было:
git merge --abort                # или git rebase --abort
```

> [!warning] Конфликт ≠ поломка
> Конфликт — нормальная ситуация, Git просто не знает, чью версию взять. Дерево не испорчено: можно разрулить вручную либо `--abort` и вернуться в исходное состояние. Маркеры `<<<<<<<`/`=======`/`>>>>>>>` показывают «твоё»/«их».

## 🩺 Частые вопросы

- **`fetch` или `pull`?** — `fetch` если хочешь сперва посмотреть; `pull` если готов сразу влить.
- **«Your local changes would be overwritten by merge»** — незакоммиченные правки мешают: закоммить, `git stash` или `git pull --autostash`.
- **Не хочу merge-коммиты** — `git pull --rebase` (или `pull.rebase=true` глобально).
- **«divergent branches» / pull требует выбрать стратегию** — новые Git просят явно: задай `git config pull.rebase true|false` или используй флаг `--rebase`/`--no-rebase`.
- **Запутался в конфликте** — `git merge --abort` / `git rebase --abort` вернёт всё назад.

## 💎 Резюме

- `git pull` = `fetch` + `merge`; `git pull --rebase` = `fetch` + `rebase` (линейная история).
- Рекомендуется: `git pull --rebase --autostash` (можно закрепить в конфиге).
- Только перемотка без merge-коммитов: `--ff-only`.
- Конфликты: правишь → `git add` → `--continue`; передумал → `--abort`.
- Хочешь сперва посмотреть, не сливая → [`git fetch`](fetch.md).

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-pull](https://git-scm.com/docs/git-pull)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git fetch](fetch.md) · [git push](push.md) · [git remote](remote.md)

#Git #VCS #pull #Удалённый_репозиторий #Версионирование
