---
создал заметку: 2026-10-18T18:30:00
author: WhiteK0T
tags:
  - Jira
  - Atlassian
  - JQL
  - Обучение
Источник:
  - https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/
  - https://support.atlassian.com/jira-software-cloud/docs/jql-functions/
  - https://support.atlassian.com/jira-software-cloud/docs/jql-operators/
  - https://support.atlassian.com/jira-software-cloud/docs/jql-fields/
---

# 🔎 Jira — JQL и фильтры

**JQL** (Jira Query Language) — язык запросов к задачам, похожий на `WHERE` из SQL. На нём работают поиск, фильтры, доски, гаджеты дашбордов, автоматизация, `acli` и REST API — поэтому JQL окупается быстрее всего остального в Jira.

Где писать: **Filters → Search work items** (или `/` → поиск) → переключить в **JQL**. Редактор подсказывает поля, операторы и значения (`Ctrl+Space`).

Часть серии — [карта серии](00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md).

---

## 1. Синтаксис

```
поле оператор значение [AND|OR поле оператор значение …] [ORDER BY поле [ASC|DESC]]
```

```sql
project = WEB AND status = "In Progress" AND assignee = currentUser() ORDER BY priority DESC
```

- Значения с пробелами — в кавычках: `status = "In Review"`.
- Регистр ключевых слов не важен; `NOT`, скобки — как обычно.
- `issue` и `issuetype` в JQL работают по-прежнему, хотя интерфейс говорит «work item» и «work type».

## 2. Операторы

| Оператор | Пример |
| :--- | :--- |
| `=` `!=` | `status = Done` |
| `>` `>=` `<` `<=` | `created >= -7d`, `"Story Points" > 3` |
| `IN` `NOT IN` | `status IN ("To Do", "In Progress")` |
| `~` `!~` (содержит текст) | `summary ~ "логин"`, `text ~ "NullPointerException"` |
| `IS EMPTY` `IS NOT EMPTY` | `assignee IS EMPTY`, `"Story Points" IS EMPTY` |
| `WAS` `WAS NOT` `WAS IN` | `status WAS "In Review"` — был когда-либо |
| `CHANGED` | `status CHANGED FROM "In Progress" TO Done DURING (startOfWeek(), now())` |

У `WAS` и `CHANGED` есть уточнения: `BY пользователь`, `BEFORE`, `AFTER`, `ON`, `DURING (с, по)`.

## 3. Основные поля

| Поле | Примеры |
| :--- | :--- |
| `project` | `project = WEB`, `project IN (WEB, BOT)` |
| `issuetype` / `type` | `type = Bug`, `type IN (Story, Task)` |
| `status`, `statusCategory` | `statusCategory != Done` — все незакрытые, как бы ни назывались статусы |
| `resolution` | `resolution = Unresolved` |
| `assignee`, `reporter` | `assignee = currentUser()`, `reporter = "Иван Петров"` |
| `priority` | `priority IN (Highest, High)` |
| `labels` | `labels = claude`, `labels IS EMPTY` |
| `component`, `fixVersion` | `fixVersion = "1.4.0"`, `fixVersion IN unreleasedVersions()` |
| `parent` | `parent = WEB-10` — все дети эпика или задачи |
| `sprint` | `sprint IN openSprints()` |
| `created`, `updated`, `resolved`, `due` | `updated >= -1d`, `due < now()` |
| `text`, `summary`, `description`, `comment` | полнотекстовый поиск |
| `development` (разработка) | `development[pullrequests].open > 0`, `development[commits].all = 0` — нужна интеграция с репозиторием (заметка 05) |

**Даты:** относительные `-1d`, `-2w`, `-4h`, `1d` (через день); абсолютные `"2026-10-01"`, `"2026-10-01 14:00"`.

## 4. Функции

| Функция | Что возвращает |
| :--- | :--- |
| `currentUser()` | вы |
| `membersOf("group")` | участники группы |
| `now()` | сейчас |
| `startOfDay()`, `endOfDay()`, `startOfWeek()`, `startOfMonth()`, `startOfYear()` и `endOf…` | границы периода; со сдвигом: `startOfWeek(-1)` — прошлая неделя |
| `openSprints()`, `closedSprints()`, `futureSprints()` | спринты |
| `unreleasedVersions()`, `releasedVersions()`, `latestReleasedVersion(WEB)` | версии |
| `linkedIssues("WEB-10")`, `linkedIssues("WEB-10", "blocks")` | связанные задачи |
| `issueHistory()` | недавно просмотренные вами |
| `watchedIssues()`, `votedIssues()` | наблюдаемые и с вашим голосом |
| `updatedBy(user, "-1w")` | изменённые пользователем за период |

## 5. Готовые запросы

```sql
-- Мои открытые задачи, свежие сверху
assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC

-- Что я закрыл на этой неделе (для отчёта)
assignee = currentUser() AND status CHANGED TO Done DURING (startOfWeek(), now())

-- Незакрытые баги проекта по приоритету
project = WEB AND type = Bug AND resolution = Unresolved ORDER BY priority DESC, created ASC

-- Задачи без исполнителя в текущем спринте
sprint IN openSprints() AND assignee IS EMPTY

-- Просроченные
due < now() AND statusCategory != Done

-- Застряли: в работе дольше недели
status = "In Progress" AND status CHANGED TO "In Progress" BEFORE -7d

-- Без оценки в бэклоге
project = WEB AND sprint IS EMPTY AND "Story Points" IS EMPTY AND statusCategory = "To Do"

-- Все задачи эпика WEB-10 (прямые дети)
parent = WEB-10

-- Подзадачи конкретных задач
parent IN (WEB-11, WEB-12)

-- В работе, но нет ни одного коммита (взяли и забыли)
status = "In Progress" AND development[commits].all = 0

-- Есть открытый PR, а задача не в Review
development[pullrequests].open > 0 AND status != "In Review"

-- Задачи для ИИ-агента (заметка 06)
labels = claude AND statusCategory = "To Do" ORDER BY priority DESC

-- Изменилось за сутки во всех моих проектах
project IN (WEB, BOT, INFRA) AND updated >= -1d ORDER BY updated DESC
```

## 6. Фильтры

- Написать запрос → **Save as** → имя. Сохранённый фильтр — это и источник доски, и гаджет дашборда, и условие автоматизации.
- **Подписка** (Filter → Subscribe): присылать результаты на почту по расписанию — например, каждое утро «Мои открытые задачи».
- **Доступ**: кому виден фильтр (только мне, проекту, всем).
- Ссылка на поиск: `https://имя.atlassian.net/issues/?jql=<URL-encoded JQL>` — можно класть в README и чаты.
- Экспорт результатов: **Export → CSV / Excel**.
- Из консоли: `acli jira workitem search --jql "…" --csv` ([заметка 06](06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md)).

## 7. Дашборды

**Dashboards → Create dashboard** → **Add gadget**. Полезный набор для своих проектов:

| Гаджет | Фильтр |
| :--- | :--- |
| **Filter results** «Мои в работе» | `assignee = currentUser() AND statusCategory = "In Progress"` |
| **Pie chart** по статусам | `project = WEB AND statusCategory != Done` |
| **Created vs. resolved** | `project = WEB` за 30 дней — растёт ли бэклог |
| **Filter results** «Сломанное» | `type = Bug AND priority IN (Highest, High) AND resolution = Unresolved` |
| **Activity stream** | что происходит в проектах |

## 8. Частые ошибки

| Ошибка | Решение |
| :--- | :--- |
| `The value 'In Review' does not exist for the field 'status'` | такого статуса нет в этом проекте — проверьте точное имя или используйте `statusCategory` |
| Поиск по тексту не находит часть слова | `~` ищет по словам и их формам; для части слова — `summary ~ "логин*"` |
| Своё поле не находится | в JQL его имя в кавычках: `"Story Points"`; или по ID: `cf[10016]` |
| Пустой результат с `sprint = "Sprint 5"` | имена спринтов повторяются между досками — используйте `openSprints()` или ID спринта |

## 🔗 Дальше

- [04 — автоматизация](04%20%E2%80%94%20Jira%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%28%D1%82%D1%80%D0%B8%D0%B3%D0%B3%D0%B5%D1%80%D1%8B%2C%20%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F%2C%20%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F%2C%20smart%20values%2C%20%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B8%29.md)
- Документация: [JQL](https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/), [функции](https://support.atlassian.com/jira-software-cloud/docs/jql-functions/), [операторы](https://support.atlassian.com/jira-software-cloud/docs/jql-operators/), [поля](https://support.atlassian.com/jira-software-cloud/docs/jql-fields/)

#Jira #Atlassian #JQL #Обучение
