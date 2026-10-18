---
создал заметку: 2026-10-18T19:40:00
author: WhiteK0T
tags:
  - Claude_Code
  - CI_CD
  - GitHub_Actions
  - GitLab
  - Bitbucket
  - MCP
  - Skills
  - Jira
Источник:
  - https://code.claude.com/docs/en/plugins
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/headless
  - https://github.com/modelcontextprotocol/inspector
---

# 🧪 CI/CD для проектов про Claude — скиллы, плагины, MCP-серверы

Как проверять и выпускать **свои** проекты для экосистемы Claude автоматически: скиллы, плагины Claude Code, маркетплейсы плагинов, MCP-серверы и приложения на Claude API — и как связать это с Jira.

Часть серии — [карта серии](00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md). Связанные: [skill-creator — тестирование скиллов](../../AI/Skills/skill-creator%20%28Anthropic%29%20%E2%80%94%20%D0%BE%D1%84%D0%B8%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%20%D0%B4%D0%BB%D1%8F%20%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%B8%20%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%28eval%2C%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%2C%20%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20description%29%2C%20%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%81%D0%BE%20skill-forge.md).

---

## 1. Что проверять у какого проекта

| Проект | Структура | Быстрые проверки (на каждый PR) | Дорогие проверки (по расписанию / перед релизом) |
| :--- | :--- | :--- | :--- |
| **Скилл** | папка с `SKILL.md` (frontmatter `name`, `description`) + файлы | `claude plugin validate <папка> --strict`, линтер Markdown, проверка скриптов (`shellcheck`, `ruff`) | `claude plugin eval` — сработает ли скилл и хорошо ли делает работу |
| **Плагин Claude Code** | `.claude-plugin/plugin.json` + `skills/`, `commands/`, `agents/`, `hooks/` | то же + тесты скриптов хуков | `claude plugin eval`, `claude plugin details` (сколько токенов «весит») |
| **Маркетплейс плагинов** | `.claude-plugin/marketplace.json` + плагины | `claude plugin validate .` (манифест маркетплейса и все плагины) | — |
| **MCP-сервер** (Node/Python) | обычный проект | юнит-тесты, линтер, **MCP Inspector CLI**: сервер стартует и отдаёт список инструментов | интеграционные тесты, сценарии с реальным Claude |
| **Приложение на Claude API / Agent SDK** | обычный проект | юнит-тесты **с замоканным API** (без затрат) | eval-набор с реальной моделью, контроль стоимости |

---

## 2. Инструменты Claude Code для CI

Проверено на Claude Code **2.1.302**: подкоманды `claude plugin` появились недавно, на старых версиях их может не быть.

| Команда | Зачем | Нужен ключ Claude |
| :--- | :--- | :---: |
| `claude plugin validate <путь>` | проверка `plugin.json` / `marketplace.json`, скиллов, агентов, команд | нет |
| `claude plugin validate <путь> --strict` | **предупреждения тоже ошибка** (код выхода 1): нет `version`, `description`, `author`, у скилла нет `description` | нет |
| `claude plugin validate <путь> --json` | отчёт в JSON для разбора в пайплайне | нет |
| `claude plugin eval <путь>` | прогон eval-кейсов (`evals/**/case.yaml` или `prompt.md` + `graders/*.md`), сравнение «с плагином / без плагина» | **да** |
| `claude plugin eval … --trust-plugin --json results.json --max-cost-usd 2` | для CI: без интерактивного подтверждения, результат в файл, жёсткий потолок расходов (выход 2 при превышении) | **да** |
| `claude plugin details <имя>` | состав плагина и сколько токенов он добавит в контекст | нет |
| `claude plugin tag [путь] --push` | git-тег `<имя>--v<версия>` с проверкой, что версия в `plugin.json` и маркетплейсе совпадает | нет |
| `claude -p "…"` | headless-режим: любой сценарий с моделью (ревью, генерация, проверки) | **да** |

Пример вывода `--strict` на плагине без поля `author`:

```
⚠ Found 1 warning:
  ❯ author: No author information provided. Consider adding author details for plugin attribution
✘ Validation failed (--strict treats warnings as errors)
```

> [!warning] eval запускает код плагина
> `claude plugin eval` загружает плагин и выполняет его на раннере от имени CI. В CI это нормально для **своих** плагинов; чужие PR из форков на eval не пускайте (нет доступа к секретам — и хорошо).

---

## 3. GitHub Actions: репозиторий плагина

`.github/workflows/plugin.yml`:

```yaml
name: Plugin CI
on:
  pull_request:
  push:
    branches: [main]
    tags: ['*--v*']           # теги вида myplugin--v1.2.0
  schedule:
    - cron: '0 3 * * 1'       # eval раз в неделю
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Установить Claude Code
        run: |
          curl -fsSL https://claude.ai/install.sh | bash
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - name: Проверить манифест, скиллы, агентов, команды
        run: claude plugin validate . --strict
      - name: Скрипты хуков
        run: |
          sudo apt-get install -y shellcheck
          find . -name '*.sh' -print0 | xargs -0 -r shellcheck

  eval:
    # дорого: только по расписанию, вручную и на релизных тегах
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch' || startsWith(github.ref, 'refs/tags/')
    needs: validate
    runs-on: ubuntu-latest
    timeout-minutes: 45
    steps:
      - uses: actions/checkout@v4
      - run: |
          curl -fsSL https://claude.ai/install.sh | bash
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - name: Eval
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: claude plugin eval . --trust-plugin --json eval-results.json --max-cost-usd 3
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: eval-results
          path: eval-results.json

  release:
    if: startsWith(github.ref, 'refs/tags/')
    needs: [validate, eval]
    runs-on: ubuntu-latest
    environment: production       # деплой виден в Jira (заметка 05)
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: gh release create "$GITHUB_REF_NAME" --generate-notes
        env:
          GH_TOKEN: ${{ github.token }}
```

Выпуск версии: поднять `version` в `plugin.json` → `claude plugin tag --push` → пайплайн проверит, прогонит eval и создаст релиз.

## 4. MCP-сервер: smoke-тест через Inspector

```yaml
  mcp-smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm ci && npm run build && npm test
      - name: Сервер стартует и отдаёт инструменты
        run: |
          npx -y @modelcontextprotocol/inspector --cli node build/index.js --method tools/list > tools.json
          jq -e '.tools | length > 0' tools.json
      - name: Вызов инструмента
        run: npx -y @modelcontextprotocol/inspector --cli node build/index.js --method tools/call --tool-name ping --tool-arg text=hello
```

Для Python-сервера — `uv run pytest` и тот же Inspector с командой `uv run server.py`.

## 5. GitLab CI и Bitbucket Pipelines

```yaml
# .gitlab-ci.yml
validate:
  image: node:24-alpine3.21
  before_script:
    - apk add --no-cache bash curl git
    - curl -fsSL https://claude.ai/install.sh | bash
    - export PATH="$HOME/.local/bin:$PATH"
  script:
    - claude plugin validate . --strict

eval:
  extends: validate
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" || $CI_COMMIT_TAG
  script:
    - claude plugin eval . --trust-plugin --json eval-results.json --max-cost-usd 3   # ANTHROPIC_API_KEY — masked variable
  artifacts:
    paths: [eval-results.json]
    when: always
```

```yaml
# bitbucket-pipelines.yml
image: node:24
pipelines:
  default:
    - step:
        name: Validate
        script:
          - curl -fsSL https://claude.ai/install.sh | bash
          - export PATH="$HOME/.local/bin:$PATH"
          - claude plugin validate . --strict
  custom:
    eval:
      - step:
          name: Eval
          script:
            - curl -fsSL https://claude.ai/install.sh | bash
            - export PATH="$HOME/.local/bin:$PATH"
            - claude plugin eval . --trust-plugin --json eval-results.json --max-cost-usd 3
          artifacts: [eval-results.json]
```

## 6. Приложения на Claude API: тесты без затрат и с ними

- **Юнит-тесты** — с подменой клиента (`unittest.mock`, `respx`/`nock` для HTTP) — на каждый PR, бесплатно.
- **Eval-набор** — фиксированные входы и критерии ответа (строгие проверки + оценка моделью) — по расписанию, с **отдельным API-ключом с лимитом расходов** в консоли Anthropic.
- **Модель — в переменной окружения**, а не в коде: смена модели — это отдельный PR, который прогоняет eval.
- В Jira: задача «Обновить модель на …» → PR → eval в CI → результат комментарием в задачу через `acli` ([заметка 06](06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md)).

## 7. Связь с Jira

| Что | Как |
| :--- | :--- |
| Задачи на развитие плагинов | отдельный проект Jira (`CLP`) или компонент на каждый плагин |
| Версии | релиз Jira `myplugin 1.2.0` ↔ тег `myplugin--v1.2.0`; в задачах — Fix version |
| Деплой | job `release` с `environment: production` → в задачах релиза виден деплой |
| Результаты eval | `acli jira workitem comment-create --key …` с итоговым баллом или ссылкой на артефакт |
| Регрессия качества | eval упал → правило автоматизации по входящему вебхуку создаёт баг ([заметка 04](04%20%E2%80%94%20Jira%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%28%D1%82%D1%80%D0%B8%D0%B3%D0%B3%D0%B5%D1%80%D1%8B%2C%20%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F%2C%20%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D1%8F%2C%20smart%20values%2C%20%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B8%29.md)) |

## 🔗 Ссылки

- Claude Code: [плагины](https://code.claude.com/docs/en/plugins), [скиллы](https://code.claude.com/docs/en/skills), [headless](https://code.claude.com/docs/en/headless), [GitHub Actions](https://code.claude.com/docs/en/github-actions), [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)
- MCP Inspector: https://github.com/modelcontextprotocol/inspector
- Дальше: [08 — шпаргалка](08%20%E2%80%94%20Jira%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%28%D0%B3%D0%BE%D1%80%D1%8F%D1%87%D0%B8%D0%B5%20%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D1%88%D0%B8%2C%20JQL%2C%20smart%20commits%2C%20acli%29.md)

#Claude_Code #CI_CD #GitHub_Actions #GitLab #Bitbucket #MCP #Skills #Jira
