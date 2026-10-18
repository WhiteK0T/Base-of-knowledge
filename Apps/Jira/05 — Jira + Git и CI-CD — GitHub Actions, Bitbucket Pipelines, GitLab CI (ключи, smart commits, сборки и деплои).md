---
создал заметку: 2026-10-18T19:00:00
author: WhiteK0T
tags:
  - Jira
  - Atlassian
  - CI_CD
  - GitHub_Actions
  - GitLab
  - Bitbucket
  - Git
Источник:
  - https://support.atlassian.com/jira-cloud-administration/docs/integrate-jira-software-with-github/
  - https://support.atlassian.com/jira-cloud-administration/docs/link-github-workflows-and-deployments-to-jira-issues/
  - https://support.atlassian.com/jira-software-cloud/docs/process-issues-with-smart-commits/
  - https://support.atlassian.com/bitbucket-cloud/docs/set-up-and-monitor-deployments/
  - https://docs.gitlab.com/integration/jira/development_panel/
  - https://developer.atlassian.com/cloud/acli/reference/commands/
---

# 🔗 Jira + Git и CI/CD — GitHub Actions, Bitbucket Pipelines, GitLab CI

Как связать Jira с репозиториями и пайплайнами, чтобы в каждой задаче было видно ветки, коммиты, PR, **сборки и деплои**, а задачи сами двигались по статусам.

Часть серии — [карта серии](00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md). Связанные: [GitHub Actions в базе](../../VCS/GitHub/GitHub%20Actions%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D1%87%D1%91%D1%82%D1%87%D0%B8%D0%BA%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BE%D0%BA%20%D0%B2%20README.md), [карта команд Git](../../VCS/Git/Git%20%E2%80%94%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%20%28%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%29.md).

---

## 1. Главный принцип: ключ задачи везде

Jira связывает код с задачей **только по ключу** (`WEB-42`) — в имени ветки, сообщении коммита или заголовке PR/MR:

| Где | Пример |
| :--- | :--- |
| Ветка | `WEB-42-password-check` или `feature/WEB-42-password-check` |
| Коммит | `WEB-42 Добавить проверку длины пароля` |
| PR / MR | `WEB-42: проверка длины пароля` |

После этого в задаче появляется блок **Development**: ветки, коммиты, PR со статусом, **Builds** (зелёные/красные сборки), **Deployments** (куда выкатили), а на карточке доски — значки сборки и деплоя. Ключ должен быть **заглавными буквами**, `web-42` не распознается.

### Подставлять ключ автоматически: git-хук

`.git/hooks/prepare-commit-msg` (или общий для всех репозиториев через `git config --global core.hooksPath ~/.githooks`):

```sh
#!/bin/sh
# Берёт ключ Jira из имени ветки и добавляет в начало сообщения, если ключа там ещё нет
case "$2" in merge|squash) exit 0 ;; esac          # не трогать merge- и squash-сообщения
branch=$(git symbolic-ref --short HEAD 2>/dev/null) || exit 0
key=$(printf '%s' "$branch" | grep -oE '[A-Z][A-Z0-9]+-[0-9]+' | head -n1)
[ -n "$key" ] || exit 0
if ! grep -q "$key" "$1"; then
  sed -i.bak "1s/^/$key /" "$1" && rm -f "$1.bak"
fi
```

`chmod +x` — и коммиты в ветке `WEB-42-…` сами получат префикс `WEB-42`.

### Создать ветку из задачи

В задаче: **Development → Create branch** — Jira предложит имя с ключом и откроет GitHub/GitLab/Bitbucket. Из консоли — просто `git switch -c WEB-42-password-check`.

---

## 2. Smart commits — управлять задачей из коммита

```
WEB-42 #comment Исправил проверку пустого пароля #time 1h 30m #in-review
```

| Команда | Действие |
| :--- | :--- |
| `#comment текст` | комментарий в задаче |
| `#time 1w 2d 4h 30m [текст]` | списать время |
| `#<переход>` | выполнить переход workflow: имя перехода в нижнем регистре, пробелы → дефисы (`#done`, `#in-progress`, `#in-review`) |

Условия: smart commits включены в настройках интеграции; **почта автора коммита совпадает с почтой пользователя Jira** (`git config user.email`), у него есть права на переход; переход доступен из текущего статуса. Поддерживаются интеграциями Bitbucket и GitHub for Atlassian; в GitLab — проверьте настройку в приложении GitLab for Jira Cloud.

> [!tip] Smart commits или автоматизация
> Smart commits — ручное управление из коммитов. Надёжнее двигать статусы **правилами автоматизации** по событиям «PR создан/смёржен» ([заметка 04](04%20%E2%80%94%20Jira%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%28%D1%82%D1%80%D0%B8%D0%B3%D0%B3%D0%B5%D1%80%D1%8B%2C%20%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F%2C%20%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F%2C%20smart%20values%2C%20%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B8%29.md)): не зависит от дисциплины коммитов.

---

## 3. GitHub + GitHub Actions

### Подключение

1. Jira → **Apps → Explore more apps** → **GitHub for Atlassian** (бывш. GitHub for Jira) → Install. Или из Jira: **Settings → Products → Development tools / Toolchain**.
2. **Connect GitHub organization** → выбрать организацию или личный аккаунт → установить GitHub App на нужные репозитории.
3. Приложение подтянет историю (**backfill**) — старые коммиты с ключами тоже свяжутся.

### Сборки

Ничего настраивать не нужно: запуски **GitHub Actions** для веток, коммитов и PR с ключом задачи появляются в задаче как **Builds**.

### Деплои

Jira показывает **deployments** из GitHub — их создаёт сам GitHub, если job объявляет **`environment:`**. Тип окружения Jira угадывает по имени (`prod*` → production, `stag*` → staging, `test*` → testing, `dev*` → development). Свои имена — через файл **`.jira/config.yml`** в основной ветке:

```yaml
deployments:
  environmentMapping:
    development: ["dev*", "local"]
    testing: ["test*", "ci"]
    staging: ["stage*", "preview-*"]
    production: ["prod*", "vps-*"]
```

После появления файла автоугадывание отключается — перечислите все свои окружения (до 10 шаблонов на тип).

### Пример пайплайна: `.github/workflows/ci.yml`

```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  # PR без ключа Jira в заголовке — красный
  jira-key:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - name: Заголовок PR содержит ключ задачи
        env:
          TITLE: ${{ github.event.pull_request.title }}
        run: |
          echo "$TITLE" | grep -qE '[A-Z][A-Z0-9]+-[0-9]+' || { echo "::error::Добавьте ключ Jira (WEB-123) в заголовок PR"; exit 1; }

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test            # ваша сборка и тесты

  deploy-staging:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    environment: staging          # ← это и попадёт в Jira как деплой
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production       # в настройках репо можно включить ручное подтверждение
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh production
```

Деплой свяжется со всеми задачами, ключи которых встречаются в коммитах, попавших в этот выкат.

> [!note] Старые actions от Atlassian
> `atlassian/gajira-login`, `gajira-transition` и другие **больше не поддерживаются** (Node 16). Для действий с задачами из CI используйте официальный **`acli`** (раздел 6) или REST API.

---

## 4. Bitbucket + Bitbucket Pipelines

Самая «родная» связка: Bitbucket и Jira — один вендор.

### Подключение

Jira → **Settings → Products → Development tools** (или при создании проекта) → **Connect Bitbucket** → выбрать workspace. Ветки, коммиты, PR и сборки Pipelines с ключами задач появятся в Development.

### Пример `bitbucket-pipelines.yml`

```yaml
image: node:22

pipelines:
  pull-requests:
    '**':
      - step:
          name: Test
          caches: [node]
          script:
            - npm ci
            - npm test

  branches:
    main:
      - step:
          name: Test
          caches: [node]
          script:
            - npm ci
            - npm test
      - step:
          name: Deploy to staging
          deployment: staging          # ← ключевое слово: Jira покажет деплой
          script:
            - ./deploy.sh staging
      - step:
          name: Deploy to production
          deployment: production
          trigger: manual              # ручное подтверждение
          script:
            - ./deploy.sh production
```

Окружения (`test`, `staging`, `production` и свои) настраиваются в **Repository settings → Deployments**; их переменные и секреты — там же. Бесплатный тариф Bitbucket даёт ограниченное число минут сборки в месяц.

---

## 5. GitLab + GitLab CI

### Подключение

Два варианта:

| | **GitLab for Jira Cloud** (приложение) | **Jira issue integration** (в GitLab) |
| :--- | :--- | :--- |
| Что даёт | Development-панель в Jira: ветки, коммиты, MR, **сборки и деплои** в реальном времени | ссылки на задачи Jira в GitLab, комментарии в Jira о коммитах, закрытие задач ключевыми словами |
| Где ставить | Atlassian Marketplace → GitLab for Jira Cloud → привязать группу GitLab | GitLab → проект → **Settings → Integrations → Jira** |

Для CI/CD нужен первый — он передаёт **сборки и деплои**. Работает с GitLab.com и self-managed GitLab.

### Пример `.gitlab-ci.yml`

```yaml
stages: [test, deploy]

test:
  stage: test
  image: python:3.13
  script:
    - pip install -r requirements.txt
    - pytest

deploy_staging:
  stage: deploy
  script: ./deploy.sh staging
  environment:
    name: staging
    deployment_tier: staging        # тип окружения для Jira: development/testing/staging/production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy_production:
  stage: deploy
  script: ./deploy.sh production
  environment:
    name: vps-main
    deployment_tier: production     # имя любое — тип задаёт deployment_tier
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

Интеграция ищет ключи задач в имени ветки и сообщениях коммитов при каждом запуске пайплайна. Если деплои не видны в Jira — проверьте, что пайплайн шёл на ветке с ключом и что тип окружения распознан.

---

## 6. Jira из пайплайна: `acli` и REST API

Иногда нужно из CI **написать в задачу** или **перевести её**: «выкачено на staging», «e2e-тесты упали».

### Официальный Atlassian CLI (`acli`)

```bash
# Установка в раннер (Linux amd64)
curl -fsSLo /usr/local/bin/acli https://acli.atlassian.com/linux/latest/acli_linux_amd64/acli
chmod +x /usr/local/bin/acli

# Вход по API-токену (секреты CI: JIRA_SITE, JIRA_EMAIL, JIRA_API_TOKEN)
echo "$JIRA_API_TOKEN" | acli jira auth login --site "$JIRA_SITE" --email "$JIRA_EMAIL" --token

# Ключи задач из коммитов этого выката
KEYS=$(git log --format=%s "$PREV_SHA..$CURRENT_SHA" | grep -oE '[A-Z][A-Z0-9]+-[0-9]+' | sort -u | paste -sd,)

# Комментарий и переход
acli jira workitem comment-create --key "$KEYS" --body "Выкачено на staging: $CI_PIPELINE_URL"
acli jira workitem transition --key "$KEYS" --status "Ready for QA" --yes
```

Подкоманды комментариев между версиями `acli` менялись (`comment` / `comment-create`) — сверяйтесь с `acli jira workitem --help` на своей версии.

### REST API напрямую

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://$JIRA_SITE/rest/api/3/issue/WEB-42/comment" \
  -d '{"body":{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"Выкачено на staging"}]}]}}'
```

API v3 принимает текст в формате **ADF** (Atlassian Document Format) — отсюда вложенный JSON.

### Секреты

| Где | Куда класть |
| :--- | :--- |
| GitHub Actions | Settings → Secrets and variables → Actions (`JIRA_API_TOKEN`, …) |
| Bitbucket Pipelines | Repository settings → Repository variables (Secured) |
| GitLab CI | Settings → CI/CD → Variables (Masked, Protected) |

API-токен Jira — от **отдельного пользователя-бота** с доступом только к нужным проектам; у токенов теперь ограниченный срок жизни — поставьте напоминание о продлении.

---

## 7. Запуск пайплайна из Jira

Правило автоматизации → **Send web request** ([заметка 04](04%20%E2%80%94%20Jira%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%28%D1%82%D1%80%D0%B8%D0%B3%D0%B3%D0%B5%D1%80%D1%8B%2C%20%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F%2C%20%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F%2C%20smart%20values%2C%20%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B8%29.md)):

| CI | Запрос | Принимающая сторона |
| :--- | :--- | :--- |
| **GitHub Actions** | `POST https://api.github.com/repos/OWNER/REPO/actions/workflows/<файл>.yml/dispatches`, тело `{"ref":"main","inputs":{"issue_key":"{{issue.key}}"}}`, заголовок `Authorization: Bearer <PAT>` | `on: workflow_dispatch: inputs: issue_key: …` |
| **Bitbucket Pipelines** | `POST https://api.bitbucket.org/2.0/repositories/<workspace>/<repo>/pipelines/`, тело `{"target":{"ref_type":"branch","type":"pipeline_ref_target","ref_name":"main","selector":{"type":"custom","pattern":"from-jira"}},"variables":[{"key":"ISSUE_KEY","value":"{{issue.key}}"}]}`, токен доступа репозитория | `pipelines: custom: from-jira: …` |
| **GitLab CI** | `POST https://gitlab.com/api/v4/projects/<id>/trigger/pipeline` с полями `token=<trigger token>`, `ref=main`, `variables[ISSUE_KEY]={{issue.key}}` | `rules: - if: $CI_PIPELINE_SOURCE == "trigger"` |

Типичные сценарии: «задача переведена в Ready to deploy → запустить деплой», «метка `claude` → агент делает задачу» ([заметка 06](06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md)).

---

## 8. Если не работает

| Симптом | Причина |
| :--- | :--- |
| В задаче нет коммитов | ключ в нижнем регистре или с опечаткой; интеграция не установлена на этот репозиторий; не прошёл backfill |
| Smart commit не сработал | почта коммита ≠ почта в Jira; нет такого перехода из текущего статуса; smart commits выключены |
| Сборки есть, деплоев нет | GitHub: job без `environment:`; GitLab: нет `environment`/`deployment_tier` или пайплайн не на ветке с ключом; Bitbucket: шаг без `deployment:` |
| Окружение «Undefined» | имя не распознано — `.jira/config.yml` (GitHub) или `deployment_tier` (GitLab) |
| `acli` 401 | истёк API-токен или неверный `--site` (нужно `имя.atlassian.net`, без `https://`) |

## 🔗 Ссылки

- GitHub: [подключение](https://support.atlassian.com/jira-cloud-administration/docs/integrate-jira-software-with-github/), [сборки и деплои](https://support.atlassian.com/jira-cloud-administration/docs/link-github-workflows-and-deployments-to-jira-issues/)
- [Smart commits](https://support.atlassian.com/jira-software-cloud/docs/process-issues-with-smart-commits/)
- Bitbucket: [деплои в Pipelines](https://support.atlassian.com/bitbucket-cloud/docs/set-up-and-monitor-deployments/)
- GitLab: [Jira development panel](https://docs.gitlab.com/integration/jira/development_panel/)
- [Atlassian CLI](https://developer.atlassian.com/cloud/acli/reference/commands/)

#Jira #Atlassian #CI_CD #GitHub_Actions #GitLab #Bitbucket #Git
