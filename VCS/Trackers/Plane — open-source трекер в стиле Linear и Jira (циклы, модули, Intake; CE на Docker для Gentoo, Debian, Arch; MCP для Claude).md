---
создал заметку: 2026-10-19T00:10:00
author: WhiteK0T
tags:
  - Plane
  - Трекеры
  - SelfHosted
  - MCP
  - Claude_Code
Источник:
  - https://plane.so/pricing
  - https://developers.plane.so/self-hosting/methods/docker-compose
  - https://developers.plane.so/self-hosting/editions-and-versions
  - https://docs.plane.so/core-concepts/issues/states
  - https://docs.plane.so/integrations/github
  - https://github.com/makeplane/plane
  - https://github.com/makeplane/plane-mcp-server
---

# ✈️ Plane — open-source трекер в стиле Linear и Jira

**Plane** — трекер задач для команд разработки. По интерфейсу похож на Linear, по модели — на Jira: проекты, задачи (work items), спринты (**циклы**), группы задач (**модули**), представления, страницы-документы и входящие заявки (**Intake**).

- Можно пользоваться облаком [plane.so](https://plane.so) или поставить у себя.
- Исходники — [makeplane/plane](https://github.com/makeplane/plane): около 61 тыс. звёзд, лицензия **AGPL-3.0**.
- Стабильный выпуск — **v1.4.2** (23.08.2026), в работе 1.4.3-rc1.

Сравнение с другими трекерами — в [общей заметке](%D0%A2%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D1%8B%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%94%20%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%28%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%8B%20%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%2C%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%2C%20self-hosted%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%29.md).

---

## 1. Понятия

| Понятие | Что это | Аналог в Jira |
| :--- | :--- | :--- |
| **Workspace** | организация, адрес `app.plane.so/<slug>` | сайт |
| **Project** | проект с идентификатором (`WEB`) → задачи `WEB-1`, `WEB-2` | проект |
| **Work item** | задача: состояние, приоритет, исполнители, метки, оценка, сроки, подзадачи, связи | issue |
| **State** | статус внутри одной из 5 групп (ниже) | статус |
| **Cycle** | ограниченный по времени отрезок с burndown — спринт | sprint |
| **Module** | группа задач под фичу или релиз, со своим прогрессом и ответственным | epic / fix version |
| **View** | сохранённый фильтр с раскладкой (список, доска, календарь, таблица, Gantt) | фильтр |
| **Page** | документ внутри проекта (спецификации, заметки) со ссылками на задачи | страница Confluence |
| **Intake** | входящие заявки: попадают в состояние Triage, дальше их принимают или отклоняют | Service Management (упрощённо) |
| **Estimates** | оценки в очках, категориях (S/M/L) или времени | story points |

### Группы состояний

Состояния можно переименовывать и добавлять, но каждое относится к одной из пяти групп. По группам считаются прогресс циклов и модулей и аналитика.

| Группа | Состояние по умолчанию | Смысл |
| :--- | :--- | :--- |
| Backlog | Backlog | ещё не приоритизировано; новые задачи попадают сюда |
| Unstarted | Todo | запланировано |
| Started | In Progress | в работе |
| Completed | Done | **единственная группа, которая считается «сделано»** |
| Cancelled | Cancelled | неактуально |

Добавьте своё состояние «Review» в группу Started и «Deployed» в Completed — и доска повторит ваш процесс без настройки workflow.

---

## 2. Тарифы и редакции (на 18.10.2026)

| План | Цена (год / месяц) | Пользователи | Что добавляется |
| :--- | :--- | :--- | :--- |
| **Free** | $0 | до **12** | проекты, задачи, циклы, модули, все раскладки, Intake внутри приложения, оценки, страницы проекта |
| **Pro** | **$6** / $8 | без ограничения | типы задач, свои поля (на уровне проекта), вики, учёт времени, дашборды, инициативы, teamspaces, **интеграции (GitHub, GitLab, Slack)**, SAML/OIDC, 500 ИИ-кредитов на место |
| **Business** | **$13** / $15 | без ограничения | шаблоны проектов, повторяющиеся задачи, Intake через формы и почту, вложенные страницы, один workflow с правилами, дашборды шире, 1 000 ИИ-кредитов |
| **Enterprise Grid** | по запросу (отмечен «coming soon») | — | несколько workflow с согласованием, поля на уровне workspace, LDAP, аудит |

Цены — за пользователя в месяц.

### Self-hosted: две редакции

| | **Community Edition (CE)** | **Commercial Edition** |
| :--- | :--- | :--- |
| Лицензия | AGPL-3.0, открытый код | закрытый код |
| Возможности | как облачный **Free** | как облако, все планы |
| Пользователи | без лимита | Free — 12 мест на workspace, дальше платные |
| Установка | `setup.sh` (ниже) | `prime.plane.so` |

> [!important] Что это значит на практике
> - **В CE нет того, что в облаке начинается с Pro:** интеграций с GitHub и GitLab, учёта времени, вики, своих полей и типов задач.
> - Чтобы купить платный план для своего сервера, сначала нужно перейти на Commercial Edition.
> - Если нужна связь задач с PR бесплатно, а Plane не обязателен, присмотритесь к [Gitea](../Forgejo-Gitea/Gitea%20%E2%80%94%20%D0%BB%D1%91%D0%B3%D0%BA%D0%B8%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md) или [Forgejo](../Forgejo-Gitea/Forgejo%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md): там задачи и код в одном месте.

---

## 3. Установка Community Edition

Plane — это несколько сервисов (веб, API на Django, воркеры, PostgreSQL, Redis, RabbitMQ, MinIO), поэтому ставится он **только через Docker Compose**. Нативных пакетов нет ни в одном дистрибутиве.

**Требования:** 2 ядра и 4 ГБ памяти, для работы команды — 8 ГБ.

### Шаг 1. Docker

| Система | Команды |
| :--- | :--- |
| **Gentoo** (OpenRC) | `emerge --ask app-containers/docker app-containers/docker-compose` → `rc-update add docker default && rc-service docker start` |
| **Debian / Ubuntu** | `sudo apt install docker.io docker-compose` (или репозиторий Docker) → `sudo systemctl enable --now docker` |
| **Arch** | `sudo pacman -S docker docker-compose` → `sudo systemctl enable --now docker` |

На **Entware** Plane не встанет: нет Docker, а 512 МБ памяти роутера мало.

### Шаг 2. Plane

```bash
mkdir plane-selfhost && cd plane-selfhost
curl -fsSL -o setup.sh https://github.com/makeplane/plane/releases/latest/download/setup.sh
chmod +x setup.sh
./setup.sh            # 1 — Install, затем 8 — Exit
```

Появится каталог `plane-app/` с `docker-compose.yaml` и `plane.env`. Поправьте `plane.env`:

```ini
LISTEN_HTTP_PORT=8080                      # по умолчанию 80
LISTEN_HTTPS_PORT=8443                     # по умолчанию 443
WEB_URL=https://plane.example.com
CORS_ALLOWED_ORIGINS=https://plane.example.com
```

```bash
./setup.sh            # 2 — Start
```

Меню `setup.sh`:

| Пункт | Действие |
| :--- | :--- |
| 1 | установить |
| 2 | запустить |
| 3 | остановить (перед правкой `plane.env`) |
| 4 | перезапустить |
| 5 | **обновить** |
| 6 | логи |
| 7 | **резервная копия** |
| 8 | выход |

Откройте `WEB_URL` и создайте учётную запись администратора инстанса (адрес `/god-mode`): там настраиваются почта SMTP, способы входа (Google, GitHub, GitLab OAuth) и ключи ИИ.

> [!warning] Наружу — через обратный прокси
> Если на сервере уже есть nginx или Caddy, переведите Plane на свободные порты (как выше) и проксируйте домен с HTTPS на `127.0.0.1:8080`. Делайте копию пунктом 7 и перед каждым обновлением.

---

## 4. Рабочий процесс — с чего начать

1. **Workspace → Create project.** Укажите идентификатор (`APP`), включите нужные функции проекта: Cycles, Modules, Views, Pages, Intake.
2. **Settings → States.** Добавьте свои статусы в нужные группы, например Review в Started.
3. **Settings → Labels.** Метки `bug`, `feature`, `tech-debt`.
4. **Settings → Estimates.** Выберите очки (1, 2, 3, 5, 8) или размеры.
5. **Cycles → New cycle** на две недели. Перетаскивайте задачи из бэклога, смотрите burndown.
6. **Modules** — под крупные фичи («Авторизация», «Релиз 2.0»).
7. **Views** — сохранённые фильтры: «мои задачи в текущем цикле», «баги с высоким приоритетом».

**Горячие клавиши:**

| Клавиша | Действие |
| :--- | :--- |
| `C` | новая задача |
| `Ctrl/Cmd + K` | палитра команд |
| `Q` | новый цикл |
| `M` | новый модуль |
| `D` | новая страница |
| `Shift + ?` | список всех клавиш |

### Связь с Git

Интеграции GitHub и GitLab доступны с плана **Pro** — в облаке или в Commercial Edition. Что они умеют:

- **Синхронизация задач.** Задача GitHub с меткой `plane` попадает в Plane, задача Plane с меткой `github` — в GitHub. Синхронизируются заголовок, описание, статус, исполнители, метки и комментарии; двусторонне — только в режиме bidirectional.
- **PR со ссылкой на задачу.** Если в заголовке или описании PR стоит `[APP-12]` в квадратных скобках, задача двигается по статусам: черновик → открыт → ревью → одобрен → влит или закрыт (что какому статусу соответствует, настраивает админ). Без скобок (`APP-12`) PR просто ссылается на задачу.

В CE этого нет. Обходной путь — свой шаг в CI, который через REST API Plane двигает задачу по ключу из имени ветки (пример ниже).

---

## 5. API и автоматизация из CI

Ключ API: **Profile settings → Personal Access Tokens** или **Workspace Settings → API tokens**. Передаётся в заголовке `X-API-Key`.

```bash
# облако: https://api.plane.so ; свой сервер: https://plane.example.com
PLANE=https://plane.example.com
curl -s -H "X-API-Key: $PLANE_API_KEY" \
  "$PLANE/api/v1/workspaces/my-team/projects/" | jq '.results[] | {id, identifier, name}'
```

Полный список методов — в [документации API](https://developers.plane.so/api-reference/introduction). Задачи в новых версиях API называются `work-items`.

---

## 6. Plane и Claude — официальный MCP

| Вариант | Адрес / команда | Вход |
| :--- | :--- | :--- |
| Облако, OAuth | `claude mcp add --transport http plane https://mcp.plane.so/http/mcp` → `/mcp` | браузер |
| Облако, токен | `https://mcp.plane.so/http/api-key/mcp` + заголовки `Authorization: Bearer <PAT>` и `X-Workspace-slug: <slug>` | PAT |
| **Свой сервер** (stdio) | `uvx plane-mcp-server stdio` (Python 3.10+, пакет 0.3.4) | `PLANE_API_KEY`, `PLANE_WORKSPACE_SLUG`, `PLANE_BASE_URL` |

Для self-hosted:

```bash
claude mcp add --transport stdio --scope user plane \
  --env PLANE_API_KEY=<ключ> \
  --env PLANE_WORKSPACE_SLUG=my-team \
  --env PLANE_BASE_URL=https://plane.example.com \
  -- uvx plane-mcp-server stdio
```

Как устроен сервер:
- **30 инструментов** — по одному на ресурс Plane (`workitem`, `cycle`, `module`, `page`…), **207 операций**. Нужную операцию выбирают параметром `action`: `workitem(action="create", …)`.
- В поиске и списках работает **PQL** — язык запросов Plane. Синтаксис агент получает инструментом `get_pql_reference`.
- Endpoint SSE (`/sse`) устарел — используйте HTTP.

Пример запроса агенту: «возьми задачи текущего цикла APP со статусом Todo и меткой bug, по каждой предложи план исправления и оставь его комментарием».

## 🔗 Ссылки

- [Plane](https://plane.so) · [тарифы](https://plane.so/pricing) · [GitHub](https://github.com/makeplane/plane) · [чейнджлог](https://plane.so/changelog)
- [Self-hosting: Docker Compose](https://developers.plane.so/self-hosting/methods/docker-compose) · [редакции CE и Commercial](https://developers.plane.so/self-hosting/editions-and-versions)
- [Состояния](https://docs.plane.so/core-concepts/issues/states) · [интеграция с GitHub](https://docs.plane.so/integrations/github) · [MCP-сервер](https://github.com/makeplane/plane-mcp-server)

#Plane #Трекеры #SelfHosted #MCP #Claude_Code
