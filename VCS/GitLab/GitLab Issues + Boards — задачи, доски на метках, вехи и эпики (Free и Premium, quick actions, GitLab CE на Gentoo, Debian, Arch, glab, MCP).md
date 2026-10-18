---
создал заметку: 2026-10-19T02:10:00
author: WhiteK0T
tags:
  - GitLab
  - Трекеры
  - CI_CD
  - SelfHosted
  - MCP
  - Claude_Code
Источник:
  - https://about.gitlab.com/pricing/
  - https://docs.gitlab.com/user/project/issue_board/
  - https://docs.gitlab.com/user/project/issues/managing_issues/
  - https://docs.gitlab.com/user/project/labels/
  - https://docs.gitlab.com/user/project/quick_actions/
  - https://docs.gitlab.com/install/requirements/
  - https://docs.gitlab.com/user/model_context_protocol/mcp_server/
---

# 🦊 GitLab Issues + Boards — задачи и доски рядом с кодом и CI

В GitLab трекер встроен в ту же платформу, что Git и **GitLab CI**. В него входят:

- **задачи** (issues) и подзадачи-**tasks**;
- **метки**, **вехи**, учёт времени;
- **доски** (issue boards), где колонки — это метки;
- **быстрые команды** (quick actions) прямо в комментариях;
- на платных планах — **эпики**, **итерации**, веса, свои поля и статусы.

GitLab можно поставить у себя бесплатно — **GitLab CE**. Сравнение с другими трекерами — в [общей заметке](../Trackers/%D0%A2%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D1%8B%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%94%20%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%28%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%8B%20%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%2C%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%2C%20self-hosted%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%29.md). Связка GitLab CI с Jira — в [заметке 05 серии Jira](../Trackers/Jira/05%20%E2%80%94%20Jira%20%2B%20Git%20%D0%B8%20CI-CD%20%E2%80%94%20GitHub%20Actions%2C%20Bitbucket%20Pipelines%2C%20GitLab%20CI%20%28%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%2C%20smart%20commits%2C%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%BF%D0%BB%D0%BE%D0%B8%29.md).

---

## 1. Что есть бесплатно, а что — с Premium

На gitlab.com план **Free** — это до **5 пользователей** в группе верхнего уровня и **400 минут** CI в месяц. **Premium** стоит **$29** за пользователя в месяц при оплате за год. В своём **GitLab CE** доступно то же, что на Free, но без лимита пользователей и минут.

| Возможность | Free / CE | Premium | Ultimate |
| :--- | :---: | :---: | :---: |
| Задачи, метки, вехи, комментарии, шаблоны | ✅ | ✅ | ✅ |
| **Tasks** (дочерние задачи) | ✅ | ✅ | ✅ |
| Связи `relates to` | ✅ | ✅ | ✅ |
| Связи `blocks` / `is blocked by` | — | ✅ | ✅ |
| **Учёт времени** (`/estimate`, `/spend`) | ✅ | ✅ | ✅ |
| Доски проекта — **несколько** | ✅ | ✅ | ✅ |
| Доски группы | **одна** | несколько | несколько |
| Колонки по исполнителю, вехе, итерации, статусу; лимиты WIP; дорожки по эпикам | — | ✅ | ✅ |
| **Scoped-метки** (`priority::high`) | — | ✅ | ✅ |
| Несколько исполнителей | — | ✅ | ✅ |
| **Веса задач** | — | ✅ | ✅ |
| **Эпики**, дорожная карта | — | ✅ | ✅ (+ многоуровневые) |
| **Итерации** (спринты) | — | ✅ | ✅ |
| Burndown и burnup по вехам | — | ✅ | ✅ |
| **Свои поля** и **свои статусы** | — | ✅ | ✅ |
| OKR, health status | — | — | ✅ |

> [!tip] Как жить на Free
> Без итераций и эпиков спринт можно вести **вехой** (`%Sprint-42` со сроком), эпик — **родительской задачей с tasks**. Статусы заменяют обычные метки `workflow-todo`, `workflow-doing`, `workflow-review` и доска на них.

---

## 2. Задачи

### Ссылки в Markdown

| Синтаксис | Что это |
| :--- | :--- |
| `#123` | задача этого проекта |
| `group/project#123` | задача другого проекта |
| `!45` | merge request |
| `~bug`, `~"needs review"` | метка |
| `%v2.0` | веха |
| `&7` | эпик (Premium) |
| `@user` | пользователь |

### Быстрые команды (quick actions)

Пишутся отдельной строкой в описании или комментарии и выполняются при сохранении:

```text
/assign @me
/label ~bug ~"priority::high"
/unlabel ~needs-triage
/milestone %v2.0
/due 2026-10-25
/estimate 3h
/spend 1h30m
/relate #120
/duplicate #98
/copy_metadata #100
/move group/other-project
/weight 3                 # Premium
/epic &7                  # Premium
/iteration *iteration:"Sprint 42"   # Premium
/close
```

### Закрытие из коммита и MR

Ключевые слова — `Close`, `Fix`, `Resolve`, `Implement` во всех формах (`Closes`, `Fixed`, `Resolving`…), а за ними ссылка `#123`, `group/project#123` или полный URL.

```bash
git commit -m "Починил таймаут сессии

Closes #123"
```

- Задача закрывается, когда коммит попадает в **ветку по умолчанию** — пушем или влитием MR.
- В описании MR можно перечислить несколько задач: `Fixes #12, #13`.
- Отключить автозакрытие: **Settings → Repository → Branch defaults → Auto-close referenced issues on default branch**.

### Шаблоны

Шаблоны задач лежат в `.gitlab/issue_templates/*.md`, шаблоны MR — в `.gitlab/merge_request_templates/*.md`. Внутри шаблона можно использовать quick actions: шаблон «Баг» сам ставит `/label ~bug` и `/assign @lead`.

---

## 3. Доски

**Plan → Issue boards** в проекте или группе.

- **Колонка — это метка.** В колонке видны все открытые задачи с этой меткой.
- Есть ещё колонки **Open** (задачи без меток из других колонок) и **Closed**.
- **Перетащили карточку** в другую колонку — у задачи снялась старая метка и поставилась новая.
- Перетащили в **Closed** — задача закрылась, в **Open** — открылась снова.
- Задача с несколькими «колоночными» метками видна в нескольких колонках, поэтому делайте колонки на **взаимоисключающих** метках.

**Процесс на Free:**
1. Метки `workflow-todo`, `workflow-doing`, `workflow-review` (на Premium — scoped `workflow::todo` и т. д.: их нельзя повесить две сразу).
2. Доска: колонки по этим трём меткам + Closed.
3. Вторая доска проекта, например «Баги»: та же раскладка, но фильтр в строке поиска `~bug`. Сохранять фильтр в настройках доски можно только на Premium.
4. Шаблон задачи с `/label ~workflow-todo`.

---

## 4. GitLab CE у себя

**Требования:** база — 16 ГБ памяти и 8 vCPU; при нехватке памяти GitLab работает **от 8 ГБ**. База данных — только PostgreSQL (GitLab 19.x — PostgreSQL 17–18), она уже входит в пакет. Своп документация советует отключить. Для VPS на 1–2 ГБ GitLab не подходит — берите [Forgejo](../Forgejo-Gitea/Forgejo%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md) или [Gitea](../Forgejo-Gitea/Gitea%20%E2%80%94%20%D0%BB%D1%91%D0%B3%D0%BA%D0%B8%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md).

| Система | Как ставить |
| :--- | :--- |
| **Debian / Ubuntu** | официальный пакет (Linux package, бывший Omnibus) — самый простой и поддерживаемый путь |
| **Gentoo** | пакета GitLab в дереве **нет** → Docker |
| **Arch** | `pacman -S gitlab` (extra, 19.5.0) — сборка из исходников, PostgreSQL, Redis, Gitaly и nginx настраиваются вручную по ArchWiki. Проще Docker |
| **Entware** | не подходит по памяти |

### Debian / Ubuntu

```bash
sudo apt install -y curl openssh-server ca-certificates perl postfix
curl -fsSL https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
sudo EXTERNAL_URL="https://gitlab.example.com" apt install gitlab-ce

sudo cat /etc/gitlab/initial_root_password      # пароль root, файл удаляется через 24 часа
sudo gitlab-ctl reconfigure                       # после правки /etc/gitlab/gitlab.rb
sudo gitlab-ctl status
```

Прочитайте скрипт перед `| sudo bash` — он добавляет репозиторий `packages.gitlab.com` и ключ.

### Docker (Gentoo, Arch, любая система)

```yaml
# docker-compose.yml
services:
  gitlab:
    image: gitlab/gitlab-ce:19.5.0-ce.0
    restart: always
    hostname: gitlab.example.com
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com'
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
        puma['worker_processes'] = 2          # экономия памяти
        prometheus_monitoring['enable'] = false
    ports:
      - "127.0.0.1:8929:443"
      - "2224:22"
    volumes:
      - ./config:/etc/gitlab
      - ./logs:/var/log/gitlab
      - ./data:/var/opt/gitlab
    shm_size: "256m"
```

```bash
docker compose up -d
docker compose exec gitlab cat /etc/gitlab/initial_root_password
docker compose exec gitlab gitlab-backup create     # резервная копия (плюс сохраните ./config)
```

### GitLab Runner

| Система | Установка |
| :--- | :--- |
| **Gentoo** | `emerge --ask dev-util/gitlab-runner` (18.8.0, stable amd64) → `rc-update add gitlab-runner default` |
| **Arch** | `sudo pacman -S gitlab-runner` (19.5.0) → `sudo systemctl enable --now gitlab-runner` |
| **Debian** | репозиторий `packages.gitlab.com/runner/gitlab-runner` (`script.deb.sh`) → `apt install gitlab-runner` |

```bash
# токен: Settings → CI/CD → Runners → New project runner
sudo gitlab-runner register --non-interactive \
  --url https://gitlab.example.com --token glrt-XXXX \
  --executor docker --docker-image alpine:latest
```

Версия раннера может отставать от сервера на одну-две минорные версии — это нормально.

---

## 5. `glab` и автоматизация из CI

| Система | Установка `glab` |
| :--- | :--- |
| **Arch** | `pacman -S glab` (1.123.0) |
| **Debian 13** | `apt install glab` (1.53 — старый, часть команд может отличаться) |
| **Gentoo** | пакета нет → бинарник из [выпусков glab](https://gitlab.com/gitlab-org/cli/-/releases) |

```bash
glab auth login --hostname gitlab.example.com
glab issue list --assignee=@me --label=bug
glab issue create -t "Логин падает на Safari" -d "Шаги: …" -l bug -m v2.0 -a @me
glab issue note 123 -m "Воспроизвёл на 2.0.1"
glab issue close 123
glab issue board view                    # доска в терминале
glab mr create --fill --related-issue 123
```

### Задача о падении pipeline

```yaml
# .gitlab-ci.yml
stages: [test, report]

test:
  stage: test
  image: node:22
  script: [npm ci, npm test]

report-failure:
  stage: report
  image: registry.gitlab.com/gitlab-org/cli:latest
  when: on_failure
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - glab auth login --hostname "$CI_SERVER_HOST" --token "$GITLAB_ISSUES_TOKEN"
    - glab issue create -R "$CI_PROJECT_PATH" -l ci-failure
        -t "Pipeline упал на $CI_DEFAULT_BRANCH ($CI_COMMIT_SHORT_SHA)"
        -d "Pipeline: $CI_PIPELINE_URL"
```

`CI_JOB_TOKEN` задачи создавать не может. Для этого нужна маскированная переменная `GITLAB_ISSUES_TOKEN` с токеном проекта: роль Reporter, scope `api`.

---

## 6. GitLab и Claude — встроенный MCP

MCP-сервер встроен в сам GitLab: адрес `https://<gitlab>/api/v4/mcp`. Он **общедоступен с GitLab 19.5** на всех планах, включая Free, и для gitlab.com, и для своего сервера.

```bash
claude mcp add -s user --transport http GitLab https://gitlab.com/api/v4/mcp
# свой сервер: https://gitlab.example.com/api/v4/mcp
# затем в сессии: /mcp → GitLab → подтвердить в браузере
```

**Что нужно заранее:**
- **Разрешить MCP.** На gitlab.com — в группе верхнего уровня, на своём сервере — для всего инстанса (в Admin).
- **Подходящий токен.** OAuth со scope `mcp` (так работает вход через `/mcp`) или **fine-grained PAT** с ресурсом MCP tool и правом Execute. **Старые PAT, токены проекта и группы отклоняются** с ошибкой 403, даже со scope `api`.

**Наборы инструментов** задаются заголовком `X-Gitlab-Enabled-Mcp-Server-Toolsets`:
- по умолчанию — `core`, `merge_requests`, `work_items`, `repository`, `ci`;
- по запросу — `wikis`, `code_security`, `orbit`;
- если доступна платформа агентов GitLab Duo — ещё `duo_agent_platform`.

Если сервер раньше добавлялся без `-s user`, локальная запись перекрывает пользовательскую. Проверьте `claude mcp list` и удалите лишнюю: `claude mcp remove GitLab -s local`.

### Агент в GitLab CI

Официальная инструкция — [Claude Code GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd). Интеграция в **бете**, поддерживает её GitLab.

Схема: ручной запуск pipeline, событие MR или комментарий с `@claude` → job с `claude -p` → ветка и MR с `Closes #N` → после влития задача закрывается сама.

Минимальный job из документации:

```yaml
stages: [ai]

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  timeout: 30m
  before_script:
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
    - export PATH="$HOME/.local/bin:$PATH"
  script:
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Review this MR and implement the requested changes'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --max-turns 30
```

**Упоминание `@claude` из коробки не работает.** Нужен свой обработчик: вебхук проекта на «Comments» вызывает trigger API pipeline с переменными `AI_FLOW_INPUT` (текст запроса) и `AI_FLOW_CONTEXT`.

Нужна маскированная переменная `ANTHROPIC_API_KEY`. Для комментариев и MR хватает `CI_JOB_TOKEN`, иначе — токен проекта со scope `api` в переменной `GITLAB_ACCESS_TOKEN`. Как устроить всю цепочку «задача → агент → MR», подробно разобрано в [заметке 06 серии Jira](../Trackers/Jira/06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md).

> [!warning] Prompt injection
> Агент читает текст задач, а его может написать кто угодно. Документация GitLab тоже предупреждает об этом. Давайте токену минимальные права, не запускайте агента на задачах от чужих людей автоматически и проверяйте каждый MR.

## 🔗 Ссылки

- [Тарифы](https://about.gitlab.com/pricing/) · [доски](https://docs.gitlab.com/user/project/issue_board/) · [управление задачами и автозакрытие](https://docs.gitlab.com/user/project/issues/managing_issues/) · [quick actions](https://docs.gitlab.com/user/project/quick_actions/) · [метки](https://docs.gitlab.com/user/project/labels/)
- [Требования к серверу](https://docs.gitlab.com/install/requirements/) · [установка Linux package](https://about.gitlab.com/install/) · [Docker](https://docs.gitlab.com/install/docker/) · [GitLab Runner](https://docs.gitlab.com/runner/install/)
- [MCP-сервер GitLab](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) · [glab](https://gitlab.com/gitlab-org/cli) · [Claude Code в GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)

#GitLab #Трекеры #CI_CD #SelfHosted #MCP #Claude_Code
