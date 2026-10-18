---
создал заметку: 2026-10-18T19:50:00
author: WhiteK0T
tags:
  - Jira
  - Atlassian
  - JQL
  - Шпаргалка
Источник:
  - https://support.atlassian.com/jira-software-cloud/docs/use-keyboard-shortcuts/
  - https://support.atlassian.com/jira-software-cloud/docs/process-issues-with-smart-commits/
  - https://developer.atlassian.com/cloud/acli/reference/commands/
---

# 📋 Jira — шпаргалка

Всё самое частое из [серии](00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md) на одной странице.

## Горячие клавиши (Jira Cloud)

| Клавиши | Действие |
| :--- | :--- |
| `?` | список всех горячих клавиш |
| `c` | создать задачу |
| `/` | поиск |
| `g` затем `d` | перейти на дашборд |
| `g` затем `a` | доска (agile board) |
| `g` затем `i` | поиск задач |
| `j` / `k` | следующая / предыдущая задача в списке |
| `o` или `Enter` | открыть выбранную задачу |
| `e` | редактировать задачу |
| `a` | назначить |
| `i` | назначить на себя |
| `m` | комментарий |
| `l` | метки |
| `.` | меню действий (переход, клонирование, перемещение) |
| `Ctrl+Enter` | сохранить комментарий / форму |
| `1`, `2`, `3` (на доске) | бэклог / активный спринт / отчёты |

Набор клавиш Atlassian иногда меняет — актуальный список всегда по `?`.

## Частые JQL

```sql
assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC   -- мои открытые
assignee = currentUser() AND status CHANGED TO Done DURING (startOfWeek(), now())   -- закрыл на неделе
project = WEB AND type = Bug AND resolution = Unresolved ORDER BY priority DESC     -- открытые баги
sprint IN openSprints() AND assignee IS EMPTY                                        -- ничьи в спринте
due < now() AND statusCategory != Done                                               -- просроченные
status = "In Progress" AND updated < -7d                                             -- зависшие
development[pullrequests].open > 0 AND status != "In Review"                         -- PR есть, статус не тот
labels = claude AND statusCategory = "To Do"                                         -- очередь агенту
text ~ "timeout" AND created >= -30d                                                 -- поиск по тексту
```

Операторы: `= != > < IN NOT IN ~ !~ IS EMPTY WAS CHANGED`; даты: `-1d -2w startOfWeek() now()`. Подробно — [заметка 03](03%20%E2%80%94%20Jira%20%E2%80%94%20JQL%20%D0%B8%20%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D1%8B%20%28%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D0%BE%D0%B2%2C%20%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B8%2C%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%29.md).

## Ключи в Git

```bash
git switch -c WEB-42-password-check              # ветка с ключом
git commit -m "WEB-42 Добавить проверку пароля"   # коммит с ключом
gh pr create --title "WEB-42: проверка пароля"    # PR с ключом
```

## Smart commits

```
WEB-42 #comment Текст комментария
WEB-42 #time 1h 30m Чем занимался
WEB-42 #in-review                                  ← имя перехода, пробелы → дефисы
WEB-42 #comment Готово #time 2h #done              ← можно комбинировать
```

Работают, если почта коммита = почта в Jira и переход доступен из текущего статуса.

## acli

```bash
acli jira auth login --web
acli jira workitem search --jql "assignee = currentUser() AND statusCategory != Done"
acli jira workitem search --jql "project = WEB" --fields "key,summary,status" --csv
acli jira workitem view WEB-42
acli jira workitem view WEB-42 --web                       # открыть в браузере
acli jira workitem create --project WEB --type Bug --summary "Падает вход" --description "…"
acli jira workitem transition --key "WEB-42,WEB-43" --status "Done" --yes
acli jira workitem comment-create --key WEB-42 --body "Выкачено на staging"
acli jira workitem --help                                   # всё остальное
```

## MCP для Claude Code

```bash
claude mcp add --transport http --scope user atlassian https://mcp.atlassian.com/v2/mcp
# затем в сессии: /mcp → atlassian → Authenticate
```

## Деплой виден в Jira, если…

| CI | Нужно |
| :--- | :--- |
| GitHub Actions | job с `environment: staging/production`; свои имена — `.jira/config.yml` |
| Bitbucket Pipelines | шаг с `deployment: staging/production` |
| GitLab CI | `environment:` + `deployment_tier: production` |

## Тарифы Jira Cloud Free

10 пользователей · 2 ГБ вложений · 100 запусков автоматизации в месяц (правила одного проекта) · без ролей и аудита.

#Jira #Atlassian #JQL #Шпаргалка
