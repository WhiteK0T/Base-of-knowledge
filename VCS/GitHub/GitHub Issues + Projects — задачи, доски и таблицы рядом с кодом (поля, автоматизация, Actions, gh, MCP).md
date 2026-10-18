---
создал заметку: 2026-10-19T01:40:00
author: WhiteK0T
tags:
  - GitHub
  - Трекеры
  - GitHub_Actions
  - CI_CD
  - MCP
  - Claude_Code
Источник:
  - https://github.com/pricing
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations
  - https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests
  - https://cli.github.com/manual/gh_project
  - https://cli.github.com/manual/gh_issue_create
  - https://github.com/github/github-mcp-server
---

# 🐙 GitHub Issues + Projects — задачи рядом с кодом

На GitHub трекер встроен прямо в хостинг кода:

- **Issues** — задачи в репозитории: метки, вехи, исполнители, типы, подзадачи, зависимости;
- **Projects** — доски, таблицы и дорожные карты поверх задач и PR из любых репозиториев владельца, со своими полями и автоматизацией;
- **Actions** — CI, который двигает карточки, создаёт задачи и запускает агентов.

Всё это есть **на бесплатном плане**. Сравнение с отдельными трекерами — в [общей заметке](../Trackers/%D0%A2%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D1%8B%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%94%20%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%28%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%8B%20%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%2C%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%2C%20self-hosted%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%29.md). Про Actions для этого хранилища — [автосчётчик заметок](GitHub%20Actions%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D1%87%D1%91%D1%82%D1%87%D0%B8%D0%BA%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BE%D0%BA%20%D0%B2%20README.md) и [автоматизация релизов](%D0%90%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D0%BE%D0%B2%20%E2%80%94%20release-please%20%D0%B8%20semantic-release%20%28Conventional%20Commits%2C%20SemVer%2C%20Changelog%29.md).

---

## 1. Тарифы (на 18.10.2026)

| | **Free** | **Team** | **Enterprise** |
| :--- | :--- | :--- | :--- |
| Цена | $0 | **$4** за пользователя в месяц (первые 12 месяцев) | от **$21** (первые 12 месяцев) |
| Issues, Projects, вехи | ✅ | ✅ | ✅ |
| Минуты Actions (приватные репо) | 2 000 | 3 000 | 50 000 |
| Packages | 500 МБ | 2 ГБ | 50 ГБ |
| Несколько исполнителей задачи | только публичные репо | ✅ | ✅ |
| Защита веток (rulesets) | только публичные репо | ✅ | ✅ |
| Автодобавление в Project (auto-add) | **1** правило | 5 (и на Pro) | 20 |

Для публичных репозиториев минуты Actions и Packages бесплатны на всех планах. Цену Team и Enterprise после первых 12 месяцев страница не называет.

---

## 2. Issues

| Возможность | Как устроено |
| :--- | :--- |
| **Метки** | на уровне репозитория; набор по умолчанию: `bug`, `enhancement`, `documentation`, `good first issue`… |
| **Вехи** | срок и процент закрытых задач — удобно под релиз |
| **Типы задач** | на уровне **организации**: по умолчанию `Task`, `Bug`, `Feature`, всего до 25 своих. В личных репозиториях типов нет |
| **Подзадачи (sub-issues)** | до **100** у одной задачи, вложенность до **8** уровней, прогресс виден у родителя |
| **Зависимости** | **Relationships → Blocked by / Blocking**. Заблокированные задачи помечаются значком на досках и в списке |
| **Шаблоны** | `.github/ISSUE_TEMPLATE/*.md` или `*.yml` (формы с полями), `config.yml` — отключить пустые задачи, добавить ссылки |
| **Закрытие из PR** | `Fixes #12`, `Closes #12`, `Resolves #12` (и формы fix/fixed, close/closed, resolve/resolved) в описании PR или коммите. Срабатывает при влитии в **ветку по умолчанию** |
| **Другой репозиторий** | `Fixes owner/repo#12` |
| **Причина закрытия** | `completed` или `not planned` |
| **Связь с PR** | **Development** в боковой панели: создать ветку из задачи или привязать PR |

### Поиск

```text
is:issue is:open assignee:@me
is:open type:"Bug" label:"priority: high"
label:"bug","wip"                         # bug ИЛИ wip
label:"bug" label:"wip"                   # bug И wip
no:assignee no:milestone is:open
(type:"Bug" AND assignee:alice) OR (type:"Feature" AND assignee:bob)
is:closed reason:"not planned"
is:open linked:pr                         # есть связанный PR
is:open field.priority:high               # поле из Project
sort:created-asc
```

Скобки вкладываются до 5 уровней. Пробел между условиями означает AND.

---

## 3. Projects

Project принадлежит **пользователю или организации**, а не репозиторию. В него можно положить задачи и PR из разных репозиториев и черновики (draft issues).

### Раскладки и представления

| Раскладка | Для чего |
| :--- | :--- |
| **Table** | плотная таблица, массовое редактирование, группировка и срезы (slice) по полю |
| **Board** | канбан по любому полю с одним значением (обычно Status), лимиты колонок |
| **Roadmap** | временная шкала по полям-датам или итерациям |

Каждое представление сохраняет фильтр, сортировку, группировку и видимые поля. Фильтры в Projects пишутся на том же языке поиска: `assignee:@me status:"In progress" -label:blocked`.

### Поля

До **50 полей** на проект, встроенные и свои вместе.

| Тип | Пример |
| :--- | :--- |
| Text | заметка |
| Number | оценка, story points |
| Date | срок, дата релиза |
| **Single select** | Status, Priority, Size |
| **Iteration** | спринт: длина, перерывы между итерациями |

Встроенные поля — Assignees, Labels, Milestone, Repository, Linked pull requests, Reviewers, Parent issue, Sub-issues progress.

### Встроенная автоматизация

Меню проекта **⋯ → Workflows**:

| Workflow | По умолчанию |
| :--- | :--- |
| Item added to project | Status = Todo |
| Item closed | Status = **Done** (включено) |
| Pull request merged | Status = **Done** (включено) |
| Pull request closed | Status = Done (включено) |
| Item reopened | вернуть статус |
| **Auto-add to project** | добавлять задачи и PR репозитория по фильтру: `is:issue label:bug -label:wontfix` |
| **Auto-archive items** | архивировать, например `is:closed updated:<@today-14d` |

В фильтре auto-add поддерживаются `is:` (open, closed, merged, draft, issue, pr), `label:`, `reason:`, `assignee:`, `no:`. Отрицание `-` работает со всеми, кроме `no:`.

**Ещё в Projects:**
- **Insights** — графики по полям (burn-up, распределение по статусам);
- **Status updates** — «On track» или «At risk», даты и текст;
- **шаблоны проектов** для организации.

### Как устроить свой процесс

1. Создайте Project (**Your profile → Projects → New project**) из шаблона **Team planning** или **Kanban**.
2. Поле **Status**: `Backlog`, `Todo`, `In progress`, `In review`, `Done`.
3. Добавьте поля **Priority** (single select), **Size** (single select или number) и **Iteration** на 2 недели.
4. Включите **Auto-add** для основного репозитория: `is:issue,pr is:open`.
5. Включите **Auto-archive**: `is:closed updated:<@today-30d`.
6. Сделайте представления: «Доска» (board по Status), «Мой спринт» (`assignee:@me iteration:@current`), «Дорожная карта» (roadmap по Iteration).

---

## 4. `gh` — работа из терминала

| Система | Установка |
| :--- | :--- |
| **Gentoo** | `emerge --ask dev-util/github-cli` (2.102.0) |
| **Arch** | `sudo pacman -S github-cli` (2.102.0) |
| **Debian / Ubuntu** | в Debian 13 пакет `gh` версии 2.46 — **старый**, в нём нет `--type`, `--parent` и `--blocked-by`. Лучше официальный репозиторий (ниже) |
| **Entware** | пакета нет. В выпусках gh есть статический бинарник `linux_armv6` — он работает на armv7 роутера |

```bash
# Debian / Ubuntu — официальный репозиторий GitHub CLI
sudo mkdir -p -m 755 /etc/apt/keyrings
wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg >/dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh
```

```bash
gh auth login
gh auth refresh -s project        # для команд gh project нужен scope project

# задачи
gh issue list --search 'is:open no:assignee label:"bug" sort:created-asc'
gh issue create -t "Логин падает на Safari" -b "Шаги: …" -l bug --type Bug -a @me \
  -m "v2.0" -p "Roadmap"
gh issue create -t "Сверстать форму" --parent 41          # подзадача
gh issue create -t "Миграция БД" --blocking 57            # блокирует задачу 57
gh issue edit 57 --add-blocked-by 60
gh issue view 57 --json title,state,blockedBy,blocking
gh issue develop 57 --checkout                            # ветка, привязанная к задаче
gh issue close 57 --reason "not planned"

# проекты
gh project list --owner @me
gh project field-list 1 --owner @me
gh project item-add 1 --owner @me --url https://github.com/me/app/issues/57
gh project item-list 1 --owner @me --format json | jq '.items[] | {title, status}'
gh project item-edit --project-id <PVT_…> --id <PVTI_…> \
  --field-id <PVTSSF_…> --single-select-option-id <id-опции>
```

Идентификаторы полей и опций берите из `gh project field-list 1 --owner @me --format json`.

---

## 5. Actions + Issues: автоматизация

### Класть новые задачи в Project другого владельца

Встроенный auto-add работает только в пределах владельца проекта и ограничен одним правилом на Free. Action `actions/add-to-project` обходит оба ограничения:

```yaml
# .github/workflows/add-to-project.yml
on:
  issues:
    types: [opened, labeled]
jobs:
  add:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v1.0.2
        with:
          project-url: https://github.com/users/me/projects/1
          github-token: ${{ secrets.PROJECT_PAT }}   # PAT со scope project
          labeled: bug, feature
          label-operator: OR
```

### Задача о падении сборки

```yaml
on:
  workflow_run:
    workflows: [CI]
    types: [completed]
permissions:
  issues: write
jobs:
  report:
    if: github.event.workflow_run.conclusion == 'failure' && github.event.workflow_run.head_branch == 'main'
    runs-on: ubuntu-latest
    steps:
      - run: |
          gh issue create -R "$GITHUB_REPOSITORY" -l ci-failure \
            -t "CI упал на main: ${{ github.event.workflow_run.head_sha }}" \
            -b "Прогон: ${{ github.event.workflow_run.html_url }}"
        env:
          GH_TOKEN: ${{ github.token }}
```

Встроенного `GITHUB_TOKEN` хватает для задач своего репозитория. Для Projects пользователя или организации нужен **PAT** или **GitHub App** со scope `project`.

---

## 6. GitHub и Claude

### MCP-сервер GitHub (официальный)

```bash
# удалённый, по PAT (Claude Code 2.1.1+)
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp/x/issues","headers":{"Authorization":"Bearer '"$GITHUB_PAT"'"}}'

# локальный в Docker
claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_PAT \
  -e GITHUB_TOOLSETS=issues,projects,pull_requests,labels \
  -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN -e GITHUB_TOOLSETS ghcr.io/github/github-mcp-server
```

| Как сузить | Пример |
| :--- | :--- |
| Только нужный набор инструментов (toolset) | URL `…/mcp/x/issues`, `…/mcp/x/projects` или заголовок `X-MCP-Toolsets: issues,projects` |
| Только чтение | добавить `/readonly`: `…/mcp/x/issues/readonly`, или заголовок `X-MCP-Readonly: true`, или `--read-only` локально |
| Права токена | fine-grained PAT только на нужные репозитории с правом Issues: read/write. Projects организации — право Projects в fine-grained PAT; для проектов пользователя нужен classic PAT со scope `project` |

Наборы по умолчанию — `context`, `repos`, `issues`, `pull_requests`, `users`. **`projects` по умолчанию выключен** — добавьте его, если агент должен двигать карточки.

### Агент в CI — `claude-code-action`

Задача с меткой `claude` → агент делает ветку и PR с `Fixes #N` → после влития задача закрывается, а Project сам ставит Status = Done.

```yaml
# .github/workflows/claude-issue.yml
on:
  issues:
    types: [labeled]
permissions:
  contents: write
  pull-requests: write
  issues: write
jobs:
  claude:
    if: github.event.label.name == 'claude'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Реши задачу #${{ github.event.issue.number }}: ${{ github.event.issue.title }}.
            Создай ветку, внеси правки, прогони тесты и открой PR с "Fixes #${{ github.event.issue.number }}".
```

Кроме того, `@claude` в комментарии к задаче или PR запускает агента, если установлено приложение Claude (`/install-github-app` в Claude Code). Подробно — в [заметке 06 серии Jira](../Trackers/Jira/06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md) и [заметке 07](../Trackers/Jira/07%20%E2%80%94%20CI-CD%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%20%D0%BF%D1%80%D0%BE%20Claude%20%E2%80%94%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%2C%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%D1%8B%2C%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20%28validate%2C%20eval%2C%20%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D1%8B%29.md) про CI для проектов о Claude.

> [!warning] Кто может запустить агента
> Метку `claude` ставят только участники с правом записи, но текст задачи может написать кто угодно — это prompt injection. В публичном репозитории не давайте агенту секретов, кроме ключа API, и проверяйте каждый PR.

---

## 7. Когда GitHub Issues + Projects мало

| Нужно | Куда смотреть |
| :--- | :--- |
| Сложные workflow с переходами и правами, отчёты для менеджмента | [Jira](../Trackers/Jira/00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md), [YouTrack](../Trackers/YouTrack%20%E2%80%94%20%D1%82%D1%80%D0%B5%D0%BA%D0%B5%D1%80%20JetBrains%20%28%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D1%8B%20%D0%B8%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B8%2C%20workflow%20%D0%BD%D0%B0%20JS%2C%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%20%D0%B4%D0%BE%2010%20%D1%87%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA%2C%20Docker%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D0%B2%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20MCP%29.md) |
| Удобный продуктовый трекер с циклами | [Linear](../Trackers/Linear%20%E2%80%94%20%D0%B1%D1%8B%D1%81%D1%82%D1%80%D1%8B%D0%B9%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%87%D0%BD%D1%8B%D0%B9%20%D1%82%D1%80%D0%B5%D0%BA%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%20%28%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%2C%20%D1%86%D0%B8%D0%BA%D0%BB%D1%8B%2C%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D1%8B%2C%20GitHub%20%D0%B8%20GitLab%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D0%BE%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%29.md), [Plane](../Trackers/Plane%20%E2%80%94%20open-source%20%D1%82%D1%80%D0%B5%D0%BA%D0%B5%D1%80%20%D0%B2%20%D1%81%D1%82%D0%B8%D0%BB%D0%B5%20Linear%20%D0%B8%20Jira%20%28%D1%86%D0%B8%D0%BA%D0%BB%D1%8B%2C%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D0%B8%2C%20Intake%3B%20CE%20%D0%BD%D0%B0%20Docker%20%D0%B4%D0%BB%D1%8F%20Gentoo%2C%20Debian%2C%20Arch%3B%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%29.md) |
| То же самое, но у себя на сервере | [Forgejo](../Forgejo-Gitea/Forgejo%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md), [Gitea](../Forgejo-Gitea/Gitea%20%E2%80%94%20%D0%BB%D1%91%D0%B3%D0%BA%D0%B8%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md) |

## 🔗 Ссылки

- [Тарифы](https://github.com/pricing) · [о Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects) · [встроенная автоматизация](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations) · [auto-add](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically)
- [Подзадачи](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues) · [зависимости](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies) · [типы задач](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization) · [поиск](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests)
- [gh project](https://cli.github.com/manual/gh_project) · [gh issue create](https://cli.github.com/manual/gh_issue_create) · [GitHub MCP Server](https://github.com/github/github-mcp-server) · [claude-code-action](https://github.com/anthropics/claude-code-action)

#GitHub #Трекеры #GitHub_Actions #CI_CD #MCP #Claude_Code
