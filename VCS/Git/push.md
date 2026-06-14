---
создал заметку: 2026-06-13T19:50:00
author: WhiteK0T
tags:
  - Git
  - VCS
  - push
  - Удалённый_репозиторий
  - Версионирование
Источник:
  - https://git-scm.com/docs/git-push
  - https://git-scm.com/book/ru/v2
---

# 🌿 git push — отправить коммиты на сервер

`git push` отправляет твои локальные коммиты в [удалённый репозиторий](remote.md), обновляя там ветку. Это «обратная» к [`fetch`](fetch.md) операция: публикуешь свою работу, чтобы её увидели другие (или просто сохранил на GitHub).

## 📝 Базовое использование

```bash
git push                         # отправить текущую ветку в её upstream
git push origin main             # явно: ветку main на remote origin
git push -u origin feature       # отправить и ЗАПОМНИТЬ upstream (первый push ветки)
git push --all                   # все локальные ветки
git push --tags                  # отправить теги
```

> [!info] Первый push новой ветки
> У новой локальной ветки ещё нет upstream — `git push` без аргументов не знает, куда слать. Поэтому первый раз: `git push -u origin <ветка>` (`-u` = `--set-upstream`). Дальше достаточно `git push`/`git pull` без аргументов.

## ⚙️ Основные опции

| Опция | Описание |
| :--- | :--- |
| **`-u` / `--set-upstream`** | привязать локальную ветку к удалённой (запомнить связь) |
| **`--all`** | отправить все ветки |
| **`--tags`** | отправить теги (по умолчанию push их не шлёт) |
| **`--force` / `-f`** | перезаписать удалённую ветку (**опасно**) |
| **`--force-with-lease`** | «безопасный force»: перезапишет, только если на сервере не появилось нового |
| **`--delete` / `-d`** | удалить ветку/тег на сервере |
| **`--dry-run`** | показать, что было бы отправлено, не отправляя |
| **`--prune`** | удалить на сервере ветки, которых нет локально (по refspec) |
| **`-o` / `--push-option`** | передать опцию на сервер (напр. GitLab `ci.skip`) |

## 💥 force-push — осторожно

`git push --force` **перезаписывает** удалённую ветку твоей версией, **затирая** чужие коммиты, которых у тебя нет. Нужен после `rebase`/`amend` (переписанная история не совпадает с сервером).

```bash
git push --force-with-lease      # ПРЕДПОЧТИТЕЛЬНО: откажет, если сервер ушёл вперёд
git push --force                 # грубо: перезапишет в любом случае
```

> [!danger] Всегда предпочитай `--force-with-lease`
> Обычный `--force` затрёт коммиты, которые кто-то запушил, пока ты переписывал историю. `--force-with-lease` проверяет, что удалённая ветка осталась там, где ты её видел в последний `fetch` — иначе отказывает. На общих ветках (`main`) force-push вообще избегай.

## 🌿 Удаление и теги

```bash
git push origin --delete feature     # удалить ветку на сервере
git push origin --delete v1.0        # удалить тег на сервере
git push origin v1.0                 # отправить один тег
git push --tags                      # отправить все теги
git push --follow-tags               # коммиты + связанные аннотированные теги
```

## 🚫 Когда push отклоняется

```text
! [rejected]        main -> main (fetch first)
error: failed to push some refs ...
```

Это значит: на сервере есть коммиты, которых у тебя нет (кто-то запушил раньше). Push отклонён, чтобы не потерять их. Решение:

```bash
git pull --rebase                # забрать и перебазировать свои поверх
git push                         # теперь пройдёт
```

> [!warning] Не «лечи» reject через --force
> Соблазн сделать `git push --force` после reject — затрёт чужую работу. Правильно — сначала [`git pull`](pull.md) (лучше `--rebase`), разрулить, потом обычный push.

## 🩺 Частые вопросы

- **«fatal: The current branch has no upstream»** — первый push: `git push -u origin <ветка>`.
- **«failed to push (fetch first)»** — сервер впереди: `git pull --rebase`, затем `git push`.
- **Теги не появились на сервере** — `git push` их не шлёт; нужен `git push --tags` / `--follow-tags`.
- **После rebase push не проходит** — история переписана: `git push --force-with-lease` (на своей ветке).
- **Случайно запушил секрет** — простого «отозвать» нет: ротация секрета + чистка истории (`git filter-repo`); считай его скомпрометированным.

## 💎 Резюме

- Первый раз: `git push -u origin <ветка>`; дальше — `git push`.
- Отклонили (fetch first) → `git pull --rebase` → `git push`.
- После rebase/amend → `git push --force-with-lease` (не `--force`).
- Теги отдельно: `--tags`/`--follow-tags`; удалить ветку на сервере: `--delete`.

## 🔗 Ссылки

- Официальная документация: [git-scm.com/docs/git-push](https://git-scm.com/docs/git-push)
- Книга Pro Git (рус.): [git-scm.com/book/ru/v2](https://git-scm.com/book/ru/v2)
- Связанные: [git pull](pull.md) · [git fetch](fetch.md) · [git remote](remote.md)

#Git #VCS #push #Удалённый_репозиторий #Версионирование
