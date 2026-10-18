---
создал заметку: 2026-10-19T00:40:00
author: WhiteK0T
tags:
  - YouTrack
  - Трекеры
  - SelfHosted
  - MCP
  - Claude_Code
Источник:
  - https://www.jetbrains.com/youtrack/
  - https://www.jetbrains.com/help/youtrack/cloud/2026.1/switching-subscription-plans.html
  - https://www.jetbrains.com/help/youtrack/cloud/search-and-command-attributes.html
  - https://www.jetbrains.com/help/youtrack/cloud/commands.html
  - https://www.jetbrains.com/help/youtrack/cloud/integrate-with-version-control.html
  - https://www.jetbrains.com/help/youtrack/cloud/apply-commands-in-vcs-commits.html
  - https://www.jetbrains.com/help/youtrack/server/youtrack-docker-installation.html
  - https://www.jetbrains.com/help/youtrack/server/model-context-protocol-server.html
---

# 🎯 YouTrack — трекер задач JetBrains

**YouTrack** — трекер задач и проектов от JetBrains. Есть облачная версия (**Cloud**) и сервер для своей установки (**Server**). Чем он выделяется:

- **язык запросов** с автодополнением — по смыслу как JQL;
- **команды**: меняешь сразу много полей одной строкой, в том числе из коммита;
- доски **Scrum и Kanban**, диаграмма Gantt, учёт времени;
- база знаний (**Articles**), **Helpdesk** для внешних заявок;
- **workflow на JavaScript** — правила и автоматизация.

Лицензия проприетарная. **До 10 пользователей бесплатно** и в облаке, и на своём сервере. Текущая версия — **2026.2**, сборка Docker `2026.2.19580` от 09.10.2026.

Сравнение с другими трекерами — в [общей заметке](%D0%A2%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D1%8B%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%94%20%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%28%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%8B%20%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%2C%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%2C%20self-hosted%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%29.md).

---

## 1. Лицензии и цены

| | Что известно точно (документация JetBrains) |
| :--- | :--- |
| **Бесплатно** | до **10 пользователей и 3 агентов Helpdesk**, без срока. Гостевой аккаунт считается пользователем: чтобы приватные проекты работали на 10 человек, гостя нужно заблокировать |
| **Платно** | помесячно или за год, **за пользователя**. Объём хранилища растёт вместе с числом пользователей. Можно превысить оплаченное число до 150% — доплата в конце периода |
| **Старые фиксированные планы** | с 01.10.2025 не продлеваются, нужен переход на оплату за пользователя |

Страница цен JetBrains отдаёт цифры только в браузере. Сторонние обзоры называют для облака около **$3–4 за пользователя в месяц** при 11 и более пользователях, но эти данные расходятся. Точную цену смотрите на [jetbrains.com/youtrack/buy](https://www.jetbrains.com/youtrack/buy/) при покупке.

> [!warning] Доступность из России
> JetBrains с 2022 года не продаёт продукты в РФ. Бесплатный Server на 10 человек ставится без покупки, но регистрацию в облаке и получение лицензии проверьте на своём аккаунте.

---

## 2. Понятия

| Понятие | Что это |
| :--- | :--- |
| **Project** | проект с ключом (`APP`) → задачи `APP-1`, `APP-2` |
| **Issue** | задача. Поля зависят от проекта: State, Priority, Type, Assignee, Subsystem, Fix versions, Estimation, Spent time |
| **Custom fields** | свои поля любого типа (перечисление, пользователь, версия, дата, период, число), общие для проектов или свои |
| **Tags** | личные или общие метки, по ним же — **сохранённые поиски** |
| **Agile board** | доска Scrum со спринтами или Kanban с WIP-лимитами; колонки — значения любого поля |
| **Links** | связи `subtask of` / `parent for`, `depends on`, `duplicates`, `relates to` + свои типы |
| **Articles** | база знаний с вложенностью, ссылками на задачи и совместным редактированием |
| **Helpdesk** | проекты для заявок извне: почта, онлайн-форма, SLA. Агенты считаются отдельно от пользователей |
| **Workflows** | правила на JavaScript: on-change, on-schedule, state machine, action-команды |
| **Gantt** | план работ с зависимостями |

---

## 3. Язык запросов — шпаргалка

Поиск строится из пар `атрибут: значение` с автодополнением. Разные атрибуты соединяются через **И**, несколько значений одного атрибута — через **ИЛИ**.

```text
project: APP #Unresolved for: me
in: APP State: {In Progress}, Review sort by: updated desc
#Unresolved has: -comments sort by: created asc
(in: APP #Critical or in: API #Major) and for: me
Priority: Critical, Major updated: {minus 2h} .. *
created: {minus 7d} .. Today tag: regression
has: -Assignee #Unresolved                 # никому не назначено
summary: логин -State: Fixed
```

| Синтаксис | Значение |
| :--- | :--- |
| `project:` / `in:` | проект |
| `for:` / `assigned to:` | исполнитель, `me` — вы |
| `#Unresolved`, `#Resolved` | нерешённые и решённые |
| `#Critical`, `#bug` | одиночное значение любого поля или тега |
| `has: X` / `has: -X` | поле заполнено или пусто (`has: -comments` — без комментариев) |
| `reporter:`, `commenter:`, `summary:`, `description:`, `comments:`, `links:` | автор, комментатор, поиск по тексту, связи |
| `created:`, `updated:`, `resolved date:` | даты |
| `-значение` | исключить |
| `{ }` | значение с пробелами: `{In Progress}` |
| `..` | диапазон: `2026-10-01 .. 2026-10-18` |
| `*`, `?` | маски: любые символы или один символ |
| `sort by: поле asc/desc` | сортировка |

**Даты:**
- конкретные — `2026-10-18`, `2026-10`;
- слова — `Today`, `Yesterday`, `{This week}`, `{Last month}`, `Monday`;
- сдвиги — `{minus 7d}`, `{plus 5d}`, `{minus 1y 6M}`. Единицы `y M w d h`, минуты не поддерживаются.

---

## 4. Команды

Команда — строка вида «поле значение», применяется к одной или сразу ко многим выделенным задачам. Окно команд открывается **Ctrl + Alt + J**, применить — **Ctrl + Enter**.

| Команда | Что делает |
| :--- | :--- |
| `for me` | назначить на себя |
| `for me state in progress` | назначить на себя и перевести в работу |
| `state fixed` | статус Fixed |
| `priority major` | приоритет |
| `type Bug tag regression` | тип и тег одной строкой |
| `remove tag regression` | снять тег |
| `remove Fix versions 2025.3` | убрать одно значение из многозначного поля |
| `duplicates APP-240` | связь «дубликат» (обратная ставится сама) |
| `project API` | перенести задачи в другой проект |

### Команды из коммитов

После подключения репозитория (раздел 6) в сообщении коммита пишут `#` или `^`, ключ задачи и команду:

```bash
git commit -m "Починил таймаут сессии #APP-345 Fixed"
git commit -m "Рефакторинг (#APP-12 #APP-13) state Review"   # одна команда для двух задач
git commit -m "Ссылка без команды: APP-345"                 # просто привяжет коммит
```

Как это работает:
- Команды выполняются только от участников группы **Committers** из настроек интеграции. Автора коммита YouTrack ищет по e-mail, затем по имени в VCS.
- **Команды в заголовке и описании PR игнорируются** — пишите их в коммитах.
- Ключ задачи в имени ветки тоже привязывает её к задаче, если это включено в настройках. Команды из имени ветки не выполняются.

---

## 5. Установка YouTrack Server

Официально — **Docker-образ** `jetbrains/youtrack:<сборка>`, в нём всё, включая базу и Java. Пакет AUR устарел, в Gentoo, Debian и Arch пакетов нет. На **Entware** не ставится: нужен Docker и не меньше нескольких гигабайт памяти. Минимум по памяти документация не называет — на практике заложите **4 ГБ** и больше для команды.

### Docker на всех трёх системах

| Система | Команды |
| :--- | :--- |
| **Gentoo** (OpenRC) | `emerge --ask app-containers/docker` → `rc-update add docker default && rc-service docker start` |
| **Debian / Ubuntu** | `sudo apt install docker.io` → `sudo systemctl enable --now docker` |
| **Arch** | `sudo pacman -S docker` → `sudo systemctl enable --now docker` |

### Запуск

```bash
sudo mkdir -p -m 750 /opt/youtrack/{data,conf,logs,backups}
sudo chown -R 13001:13001 /opt/youtrack          # UID пользователя в образе

docker run -d --name youtrack --restart unless-stopped \
  -v /opt/youtrack/data:/opt/youtrack/data \
  -v /opt/youtrack/conf:/opt/youtrack/conf \
  -v /opt/youtrack/logs:/opt/youtrack/logs \
  -v /opt/youtrack/backups:/opt/youtrack/backups \
  -p 127.0.0.1:8080:8080 \
  jetbrains/youtrack:2026.2.19580

docker logs youtrack | grep wizard_token       # одноразовая ссылка на мастер настройки
```

1. Откройте ссылку из лога.
2. Нажмите **Set up**.
3. Укажите **Base URL** — внешний адрес за прокси, например `https://youtrack.example.com`.
4. Задайте пароль администратора.
5. Выберите бесплатную лицензию.

Порт в Base URL должен совпадать с портом, по которому YouTrack доступен снаружи.

**Обновление:** сделайте резервную копию (**Administration → Database Backup**, файлы появятся в `/opt/youtrack/backups`), остановите и удалите контейнер, запустите новую сборку с теми же каталогами. Данные остаются в каталогах хоста.

> [!tip] Обратный прокси
> Порт `8080` держите на `127.0.0.1`, наружу — через nginx или Caddy с HTTPS. Для WebSocket (живые обновления) прокси должен пропускать заголовки `Upgrade` и `Connection`.

---

## 6. Связь с Git и CI

**Прямые интеграции:** GitHub, GitLab, Bitbucket, Azure Repos. Свои серверы тоже подключаются: GitHub Enterprise, GitLab CE/EE, Bitbucket Server, **Gitea**, Gogs.

Как подключить: **проект → Settings → VCS Integrations → New integration**. Дальше:
1. Выберите сервис и репозиторий.
2. Укажите группу Committers.
3. Если нужно, включите привязку по имени ветки.

После этого в задаче появляется вкладка **VCS changes**: коммиты, ветки, PR и их статусы.

**Из CI** — через REST API с постоянным токеном (**Profile → Account Security → New token**, scope YouTrack):

```bash
YT=https://youtrack.example.com
# найти задачи
curl -s -H "Authorization: Bearer $YT_TOKEN" \
  "$YT/api/issues?query=project:%20APP%20%23Unresolved&fields=idReadable,summary" | jq
# применить команду к задаче (как в окне команд)
curl -s -X POST -H "Authorization: Bearer $YT_TOKEN" -H "Content-Type: application/json" \
  "$YT/api/commands" \
  -d '{"query":"state Fixed","issues":[{"idReadable":"APP-345"}],"comment":"Выкачено в prod"}'
```

Шаг деплоя в GitHub Actions или GitLab CI может так закрывать задачи из коммитов релиза. Ключи берите `git log --format=%s | grep -oE '[A-Z]+-[0-9]+'`.

---

## 7. YouTrack и Claude — встроенный MCP

MCP-сервер **встроен** в сам YouTrack, ставить ничего не нужно. Адрес — `<Base URL>/mcp`.

```bash
# постоянный токен (scope YouTrack)
claude mcp add --header "Authorization: Bearer <token>" --transport http youtrack https://youtrack.example.com/mcp
```

**Вход по OAuth** удобнее. Администратор включает CIMD в **Administration → Access Management → OAuth Clients**; если клиент CIMD не поддерживает, создаётся OAuth-клиент вручную. Динамическая регистрация клиентов (DCR) не поддерживается.

**Инструменты:**

| Группа | Инструменты |
| :--- | :--- |
| Задачи | `search_issues` (язык запросов из раздела 3), `get_issue`, `create_issue`, `create_draft_issue`, `update_issue`, `change_issue_assignee`, `add_issue_comment`, `get_issue_comments`, `link_issues`, `manage_issue_tags`, `get_saved_issue_searches`, `get_issue_fields_schema` |
| База знаний | `search_articles`, `get_article`, `create_article`, `update_article` |
| Проекты и люди | `find_projects`, `get_project`, `find_user`, `get_current_user`, `find_user_groups`, `get_user_group_members` |
| Время | `log_work` |

**Ограничения:**
- Агент видит только то, что доступно пользователю токена. Администратор может дополнительно скрыть проекты от ИИ.
- Если YouTrack доступен только во внутренней сети или по VPN, облачный Claude.ai до него не дойдёт — используйте Claude Code локально.
- В Claude.ai YouTrack Server добавляется как **custom connector**: проверенный коннектор адреса своих серверов не принимает.
- Инструменты меняют данные, поэтому подтверждайте вызовы вручную, а для агента в CI заведите отдельного пользователя с минимальными правами.

Пример запроса агенту: «найди `project: APP #Unresolved for: me sort by: Priority`, по самой важной задаче прочитай связанные статьи базы знаний, предложи план и запиши 30 минут работы через `log_work`».

## 🔗 Ссылки

- [YouTrack](https://www.jetbrains.com/youtrack/) · [цены](https://www.jetbrains.com/youtrack/buy/) · [тарифные планы (документация)](https://www.jetbrains.com/help/youtrack/cloud/2026.1/switching-subscription-plans.html)
- [Язык запросов](https://www.jetbrains.com/help/youtrack/cloud/search-and-command-attributes.html) · [команды](https://www.jetbrains.com/help/youtrack/cloud/commands.html) · [команды в коммитах](https://www.jetbrains.com/help/youtrack/cloud/apply-commands-in-vcs-commits.html) · [интеграции с VCS](https://www.jetbrains.com/help/youtrack/cloud/integrate-with-version-control.html)
- [Установка в Docker](https://www.jetbrains.com/help/youtrack/server/youtrack-docker-installation.html) · [MCP-сервер](https://www.jetbrains.com/help/youtrack/server/model-context-protocol-server.html)

#YouTrack #Трекеры #SelfHosted #MCP #Claude_Code
