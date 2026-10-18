---
создал заметку: 2026-10-18T18:40:00
author: WhiteK0T
tags:
  - Jira
  - Atlassian
  - Автоматизация
  - CI_CD
  - Обучение
Источник:
  - https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/
  - https://support.atlassian.com/cloud-automation/docs/jira-automation-actions/
  - https://support.atlassian.com/cloud-automation/docs/what-are-smart-values/
  - https://support.atlassian.com/cloud-automation/docs/how-is-my-usage-calculated/
  - https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event
---

# ⚙️ Jira — автоматизация

**Jira Automation** — встроенный конструктор правил «**когда** (триггер) → **если** (условия) → **сделать** (действия)», без кода. Им закрывают рутину: двигают задачи по статусам по событиям из Git и CI, назначают исполнителей, пишут комментарии, создают задачи по расписанию и **вызывают внешние системы** — например, запускают workflow GitHub Actions с ИИ-агентом.

Где: **Project settings → Automation** (правила проекта) или **Settings → System → Automation** (глобальные, с тарифа Standard). Есть готовая **библиотека шаблонов** — с неё удобно начинать.

Часть серии — [карта серии](00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md).

---

## 1. Из чего состоит правило

```
Триггер ──▶ Условие(я) ──▶ Действие(я)
              │
              └─▶ Ветвление (для связанных задач / подзадач / JQL) ──▶ действия
```

### Триггеры

| Группа | Примеры |
| :--- | :--- |
| Задачи | **Work item created**, **Work item transitioned** (смена статуса), **Field value changed**, Work item commented, Work item assigned |
| Время | **Scheduled** — по расписанию (cron или «каждый день в 9:00»), можно с JQL: «для всех задач, найденных запросом» |
| Вручную | **Manual trigger** — кнопка в меню задачи «Automation» |
| Внешние | **Incoming webhook** — правило запускается HTTP-запросом извне (из CI, скрипта) |
| **DevOps** (нужна интеграция, заметка 05) | **Branch created**, **Commit created**, **Pull request created / merged / declined**, **Build successful / failed / status changed**, **Deployment successful / failed** |
| Спринты и релизы | Sprint started/completed, Version released |

### Условия

- **JQL condition** — задача подходит под запрос (`labels = claude AND type = Task`);
- **Work item fields condition** — поле равно/не равно/пусто;
- **If / else** — разветвить логику;
- **User condition** — кто инициатор (не реагировать на действия бота);
- **Related work items condition** — например, «все подзадачи закрыты».

### Действия

| Действие | Пример |
| :--- | :--- |
| **Transition work item** | перевести в «In Review» |
| **Edit / Assign** | поставить метку, исполнителя, приоритет |
| **Comment** | написать комментарий (в том числе внутренний) |
| **Create work item / subtasks** | завести баг, создать чек-лист подзадач |
| **Send email**, **Send Slack / Teams message** | уведомить |
| **Send web request** | HTTP-запрос куда угодно: GitHub API, Telegram-бот, свой сервер |
| **Lookup work items** | найти задачи по JQL и использовать результат в следующих шагах |
| **Log action** | написать в журнал правила (отладка) |

---

## 2. Smart values — переменные в правилах

В поля действий подставляются значения в двойных фигурных скобках:

| Smart value | Что даёт |
| :--- | :--- |
| `{{issue.key}}`, `{{issue.summary}}` | ключ и заголовок задачи |
| `{{issue.description}}` | описание |
| `{{issue.status.name}}`, `{{issue.issueType.name}}` | статус, тип |
| `{{issue.assignee.displayName}}`, `{{issue.reporter.emailAddress}}` | люди |
| `{{issue.labels}}`, `{{issue.priority.name}}` | метки, приоритет |
| `{{issue.url}}` | ссылка на задачу |
| `{{initiator.displayName}}` | кто запустил правило |
| `{{now.format("yyyy-MM-dd")}}`, `{{now.plusDays(3)}}` | даты |
| `{{pullRequest.title}}`, `{{pullRequest.url}}`, `{{pullRequest.sourceBranch}}` | в DevOps-триггерах по PR |
| `{{build.name}}`, `{{build.url}}`, `{{deployment.environment.name}}` | в триггерах сборок и деплоев |
| `{{webhookData}}` | тело входящего вебхука |
| `{{lookupIssues}}` | результат Lookup work items |

Функции: `{{issue.summary.toLowerCase()}}`, `{{issue.summary.substring(0, 50)}}`, `{{issue.description.jsonEncode}}` (для вставки в JSON), условия `{{#if(issue.assignee)}}…{{/}}`. Для отладки — действие **Log action** с нужным значением и вкладка **Audit log**.

---

## 3. Готовые правила для разработки с CI

Нужна подключённая интеграция с GitHub/GitLab/Bitbucket — [заметка 05](05%20%E2%80%94%20Jira%20%2B%20Git%20%D0%B8%20CI-CD%20%E2%80%94%20GitHub%20Actions%2C%20Bitbucket%20Pipelines%2C%20GitLab%20CI%20%28%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%2C%20smart%20commits%2C%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%BF%D0%BB%D0%BE%D0%B8%29.md).

| # | Когда | Если | Сделать |
| :---: | :--- | :--- | :--- |
| 1 | **Branch created** | статус = To Do | перевести в **In Progress**, назначить на `{{initiator}}` |
| 2 | **Pull request created** | — | перевести в **In Review**, комментарий «PR: `{{pullRequest.url}}`» |
| 3 | **Pull request merged** | — | перевести в **Done** |
| 4 | **Pull request declined** | — | вернуть в **In Progress** |
| 5 | **Build failed** | ветка = `main` | метка `ci-broken`, комментарий со ссылкой `{{build.url}}` |
| 6 | **Deployment successful** | окружение = production | перевести в **Released** / заполнить Fix version |
| 7 | **Work item transitioned** в Done | тип = Subtask, все соседние подзадачи закрыты | закрыть родителя |
| 8 | **Scheduled**, каждый понедельник | JQL `status = "In Progress" AND updated < -7d` | комментарий «Задача висит неделю — актуальна?» |

Похожие правила 1–4 есть в библиотеке шаблонов: **Automation → Templates → DevOps**.

---

## 4. Вызов внешних систем: `Send web request`

### Запустить workflow GitHub Actions из Jira

Например, при добавлении метки `claude` запустить агента, который сделает задачу ([заметка 06](06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md)).

| Поле | Значение |
| :--- | :--- |
| Триггер | **Field value changed** → Labels |
| Условие | JQL `labels = claude AND statusCategory = "To Do"` |
| URL | `https://api.github.com/repos/OWNER/REPO/actions/workflows/claude-jira.yml/dispatches` |
| Method | `POST` |
| Headers | `Authorization: Bearer <fine-grained PAT>`, `Accept: application/vnd.github+json`, `X-GitHub-Api-Version: 2022-11-28` |
| Body | см. ниже |

```json
{
  "ref": "main",
  "inputs": {
    "issue_key": "{{issue.key}}",
    "summary": "{{issue.summary.jsonEncode}}"
  }
}
```

**Токен GitHub** — fine-grained PAT, ограниченный **одним репозиторием** и правом **Actions: Read and write**. В Jira его видят все, кто может редактировать правило, — не используйте токен с широкими правами. Заголовки с секретами в правиле можно пометить как скрытые.

Аналогично: Bitbucket Pipelines — `POST https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}/pipelines/`, GitLab — `POST https://gitlab.com/api/v4/projects/{id}/trigger/pipeline` с trigger-токеном (примеры — в заметке 05).

### Принять событие извне: `Incoming webhook`

Триггер **Incoming webhook** даёт URL и секрет (заголовок `X-Automation-Webhook-Token`). Из CI:

```bash
curl -X POST "$JIRA_AUTOMATION_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -H "X-Automation-Webhook-Token: $JIRA_AUTOMATION_WEBHOOK_TOKEN" \
  -d '{"issues": ["WEB-42"], "data": {"result": "e2e-tests passed", "url": "'"$CI_JOB_URL"'"}}'
```

В правиле: `{{webhookData.data.result}}`, а задачи из массива `issues` попадут в контекст правила.

---

## 5. Лимиты и экономия

| Тариф | Запусков правил в месяц |
| :--- | :--- |
| **Free** | **100**, только правила одного проекта |
| Standard | ~1 700 |
| Premium | значительно больше (по пользователям) |
| Enterprise | без ограничений |

- Считаются запуски, в которых правило **выполнило действия**; если условия не прошли, запуск обычно не засчитывается — поэтому ставьте **условия как можно раньше**.
- DevOps-триггеры на коммиты срабатывают часто — на Free предпочитайте **PR created/merged** вместо **Commit created**.
- Текущий расход: **Automation → Usage**.
- Точные цифры Atlassian меняет — сверяйтесь со страницей тарифов.

## 6. Отладка и безопасность

- **Audit log** правила: что сработало, какие задачи, ошибки (например, «Transition not available» — нет такого перехода из текущего статуса).
- **Actor** правила (от чьего имени): по умолчанию «Automation for Jira»; чтобы правило не зациклилось, в триггерах на изменение задач включите **«не реагировать на действия этого правила»** (опция Allow rule trigger выключена).
- Правило с `Send web request` хранит секреты — давайте права на редактирование автоматизации только тем, кому доверяете.

## 🔗 Дальше

- [05 — Jira + Git и CI/CD](05%20%E2%80%94%20Jira%20%2B%20Git%20%D0%B8%20CI-CD%20%E2%80%94%20GitHub%20Actions%2C%20Bitbucket%20Pipelines%2C%20GitLab%20CI%20%28%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%2C%20smart%20commits%2C%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%BF%D0%BB%D0%BE%D0%B8%29.md)
- Документация: [триггеры](https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/), [действия](https://support.atlassian.com/cloud-automation/docs/jira-automation-actions/), [smart values](https://support.atlassian.com/cloud-automation/docs/what-are-smart-values/), [учёт запусков](https://support.atlassian.com/cloud-automation/docs/how-is-my-usage-calculated/)
- GitHub API: [workflow dispatch](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)

#Jira #Atlassian #Автоматизация #CI_CD #Обучение
