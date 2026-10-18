---
создал заметку: 2026-10-18T22:00:00
author: WhiteK0T
tags:
  - Трекеры
  - Jira
  - MCP
  - Claude_Code
  - SelfHosted
  - CI_CD
Источник:
  - https://github.com/pricing
  - https://about.gitlab.com/pricing/
  - https://linear.app/pricing
  - https://plane.so/pricing
  - https://www.openproject.org/pricing/
  - https://trello.com/pricing
  - https://asana.com/pricing
  - https://clickup.com/pricing
  - https://www.shortcut.com/pricing
  - https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/
  - https://www.yougile.com/prices
  - https://huly.io/pricing
  - https://yandex.ru/support/tracker/ru/user/mcp-server
  - https://docs.gitlab.com/user/model_context_protocol/mcp_server/
  - https://linear.app/docs/mcp
  - https://www.jetbrains.com/help/youtrack/server/model-context-protocol-server.html
---

# 🗃️ Трекеры задач — сравнение

Сравнение популярных трекеров по трём вопросам: **сколько стоит** (проверено по официальным страницам цен 18.10.2026), **можно ли подключить к Claude через MCP**, **можно ли поставить у себя** на Gentoo, Debian или Arch.

Подробная серия по Jira — в папке [`Jira/`](Jira/00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md).

> [!info] Как читать цены
> Цены — за пользователя в месяц, если не сказано иное; «год» — при оплате за год (обычно на 15–25% дешевле помесячной). Где официальная страница не отдаёт цифры без браузера, это помечено, а цифра взята из сторонних обзоров. Цены и лимиты меняются — перед покупкой сверяйтесь со страницей тарифов.

---

## 1. Облачные трекеры для разработки

| Трекер | Бесплатно | Платно | MCP для Claude | Связь с CI | Self-hosted |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Jira** | до **10** пользователей, 2 ГБ, 100 запусков автоматизации в месяц | Standard ≈ $7.91, Premium ≈ $14.54 *(сторонние обзоры)* | ✅ официальный, Atlassian MCP v2 (только Cloud) | GitHub, GitLab, Bitbucket — сборки и деплои в задаче | Data Center — сворачивается к 2029 |
| **Linear** | **без ограничения людей**, но 2 команды и **250 задач** | Basic **$10**, Business **$16** (год) | ✅ официальный | GitHub, GitLab | ❌ |
| **GitHub Issues + Projects** | ✅ безлимит репозиториев, **2 000** мин Actions | Team **$4** (первые 12 мес., дальше по прайсу), Enterprise от **$21** | ✅ официальный (GitHub MCP Server) | Actions — нативно | GitHub Enterprise Server (дорого) |
| **GitLab Issues + Boards** | **5** пользователей на группу, **400** мин CI | Premium **$29** (год), Ultimate — по запросу | ✅ официальный, общедоступен с GitLab 19.5, все тарифы | GitLab CI — нативно | ✅ GitLab CE (бесплатно) |
| **YouTrack** (JetBrains) | до **10** пользователей — и облако, и сервер | свыше 10 — по прайсу *(страница цен работает только в браузере)* | ✅ встроенный с версии 2025.3 | GitHub, GitLab, Bitbucket, IDE JetBrains | ✅ YouTrack Server (Docker) |
| **Azure DevOps Boards** | первые **5** пользователей, 1 параллельная сборка (1 800 мин) | **$6** за пользователя | ✅ официальный (`@azure-devops/mcp`, локальный) | Azure Pipelines — нативно, GitHub | Azure DevOps Server |
| **Shortcut** | ✅ бесплатный тариф | Team **$8.50**, Business **$12** (год) | ✅ официальный | GitHub, GitLab, Bitbucket | ❌ |

## 2. Общие таск-менеджеры

Хороши для личных и смешанных задач, слабее в связке с CI.

| Трекер | Бесплатно | Платно | MCP |
| :--- | :--- | :--- | :--- |
| **Trello** (Atlassian) | до **10** участников в рабочем пространстве | Standard **$5** ($6 помесячно), Premium **$10** ($12.50) | ⚠️ официального нет, только сторонние |
| **Asana** | Personal — **2** пользователя | Starter **$10.99**, Advanced **$24.99** (год) | ✅ официальный |
| **ClickUp** | Free Forever | Unlimited **$7** ($10), Business **$12** ($19) | ✅ официальный |

## 3. Российские

| Трекер | Бесплатно | Платно | MCP | Своя установка |
| :--- | :--- | :--- | :--- | :--- |
| **Яндекс Трекер** | с **01.07.2026** даже командам до 5 человек нужен тариф Яндекс 360 для бизнеса или платёжный аккаунт Yandex Cloud; бесплатно — только «Чтение» | в составе Яндекс 360, цена по расчёту | ✅ **официальный**: `https://mcp.tracker.yandex.net/mcp` | ❌ |
| **YouGile** | облако — первые **10** пользователей | облако **594 ₽** (год) / 990 ₽ (месяц); коробка **995 ₽** (год) | ⚠️ только сторонние | ✅ коробочная версия (платно) |
| **Kaiten** | не подтверждено | «Старт» ≈ **250 ₽** (210 ₽ при оплате за год) *(сторонний обзор, официальная страница не открылась)* | ⚠️ только сторонние | есть коробочная версия |

> [!warning] Доступность из России
> Atlassian с 2022 года не продаёт лицензии в РФ и, по сообщениям российских СМИ, блокирует часть аккаунтов. Официальных данных о доступе к бесплатному Jira Cloud из РФ нет. Перед тем как строить процесс на Jira, Linear, Asana и других зарубежных сервисах, проверьте регистрацию и работу аккаунта на своём адресе и способе оплаты.

---

## 4. Self-hosted: что можно поставить у себя

| Трекер | Лицензия | Стек | Память | **Gentoo** | **Debian** | **Arch** | MCP |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Plane** CE | AGPL-3.0 | Docker Compose (Python, Node, PostgreSQL, Redis) | 4 ГБ, лучше 8 | Docker | Docker | Docker | ✅ официальный (облако и self-hosted через `uvx`) |
| **OpenProject** | GPL-3.0 | Ruby on Rails, PostgreSQL | от 4 ГБ | Docker | **DEB-пакеты** для Debian 12 / Ubuntu 22.04, или Docker | Docker | ✅ официальный, но платное дополнение (Professional+) |
| **YouTrack Server** | проприетарная, бесплатно до 10 польз. | Java, всё в одном контейнере | от 4 ГБ | Docker | Docker | Docker (пакет AUR устарел) | ✅ встроенный |
| **GitLab CE** | MIT | Ruby, Go, PostgreSQL, много сервисов | от 8 ГБ | Docker | официальный DEB-репозиторий | Docker | ✅ встроенный |
| **Gitea** | MIT | один Go-бинарник, SQLite/PostgreSQL | от 512 МБ | **`www-apps/gitea`** (1.27.3) | бинарник или Docker | **`gitea`** (extra, 28.1.0) | ✅ официальный `gitea-mcp` |
| **Forgejo** | GPL-3.0 | форк Gitea, один бинарник | от 512 МБ | оверлей **GURU** (`www-apps/forgejo`) | бинарник или Docker | **`forgejo`** (extra, 16.0.6) | ⚠️ сторонние |
| **Redmine** | GPL-2.0 | Ruby on Rails | от 1 ГБ | **`www-apps/redmine`** (6.0.7, `~amd64`) | **`redmine`** (trixie 6.0.5) | **`redmine`** (extra, 7.0.2) | ⚠️ сторонние |
| **Taiga** | MPL-2.0 | Python/Django + Angular, Docker Compose | от 2–4 ГБ | Docker | Docker | Docker | ⚠️ сторонние |
| **Huly** | EPL-2.0 | много сервисов, Docker Compose | **8 ГБ** минимум, 16 рекомендуется | Docker | Docker | Docker | ⚠️ сторонние |
| **Vikunja** | AGPL-3.0 | один Go-бинарник | от 256 МБ | бинарник или Docker | бинарник или Docker | AUR `vikunja`, `vikunja-bin` | ⚠️ сторонние |
| **Kanboard** | MIT | PHP + SQLite | от 128 МБ | Docker или PHP вручную | только `sid` или Docker | AUR `kanboard` | ⚠️ сторонние |

Версии в пакетах — на 18.10.2026. Последние выпуски проектов: Plane 1.4.2, OpenProject 17.9.2, YouTrack 2026.2, Gitea 28.1.0, Forgejo 17.0.0, Vikunja 2.7.0, Kanboard 1.2.54.

> [!tip] Что тянет VPS
> На небольшой VPS (1–2 ГБ памяти) встанут **Gitea/Forgejo**, **Vikunja**, **Kanboard**, **Redmine**. **Plane**, **OpenProject**, **YouTrack**, **Taiga** хотят 4 ГБ и больше, **GitLab** и **Huly** — 8 ГБ и больше.

---

## 5. Установка

### Docker на всех трёх системах (нужен для большинства)

| Система | Команды |
| :--- | :--- |
| **Gentoo** (OpenRC) | `emerge --ask app-containers/docker app-containers/docker-compose` → `rc-update add docker default && rc-service docker start` |
| **Debian / Ubuntu** | `sudo apt install docker.io docker-compose` (или официальный репозиторий Docker) → `sudo systemctl enable --now docker` |
| **Arch** | `sudo pacman -S docker docker-compose` → `sudo systemctl enable --now docker` |

Подробнее — заметки в [`Linux/Containers/`](../../Linux/Containers).

### Plane (Community Edition)

```bash
mkdir plane-selfhost && cd plane-selfhost
curl -fsSL -o setup.sh https://github.com/makeplane/plane/releases/latest/download/setup.sh
chmod +x setup.sh
./setup.sh          # 1 — установить, затем 8 — выйти и отредактировать plane.env (адрес, порты)
./setup.sh          # 2 — запустить
```

`curl … prime.plane.so/install` — это установщик **коммерческой** редакции, для бесплатной используйте `setup.sh`.

### OpenProject

```bash
# Docker — всё в одном контейнере (любой дистрибутив)
docker run -d --name openproject -p 8080:80 \
  -e SECRET_KEY_BASE="$(openssl rand -hex 64)" \
  -e OPENPROJECT_HOST__NAME=pm.example.com \
  -e OPENPROJECT_HTTPS=true \
  -v openproject_pgdata:/var/openproject/pgdata \
  -v openproject_assets:/var/openproject/assets \
  openproject/openproject:17
```

`SECRET_KEY_BASE` должен быть одинаковым при каждом запуске — сохраните его. На **Debian 12** есть пакеты: ключ `https://packages.openproject.com/srv/deb/opf/openproject/gpg-key.gpg`, источник `https://packages.openproject.com/srv/opf/openproject/stable/17/installer/debian/12.list` → `apt install openproject` → `openproject configure`. Debian 13 в списке поддержки пакетов пока нет — на нём Docker.

### YouTrack Server

```bash
mkdir -p /opt/youtrack/{data,conf,logs,backups} && chown -R 13001:13001 /opt/youtrack
docker run -d --name youtrack -p 8080:8080 \
  -v /opt/youtrack/data:/opt/youtrack/data -v /opt/youtrack/conf:/opt/youtrack/conf \
  -v /opt/youtrack/logs:/opt/youtrack/logs -v /opt/youtrack/backups:/opt/youtrack/backups \
  jetbrains/youtrack:2026.2.19580
```

Дальше мастер настройки в браузере. Бесплатная лицензия — до 10 пользователей.

### Gitea / Forgejo — Git, задачи и CI в одном

| Система | Gitea | Forgejo |
| :--- | :--- | :--- |
| **Gentoo** | `emerge --ask www-apps/gitea` → `rc-update add gitea default` | `eselect repository enable guru && emaint sync -r guru` → `emerge --ask www-apps/forgejo` |
| **Debian** | бинарник с https://dl.gitea.com или `docker.gitea.com/gitea` | бинарник с https://codeberg.org/forgejo/forgejo/releases или `codeberg.org/forgejo/forgejo:17` |
| **Arch** | `pacman -S gitea` → `systemctl enable --now gitea` | `pacman -S forgejo` → `systemctl enable --now forgejo` |

У обоих есть **Actions** — CI с синтаксисом GitHub Actions (нужен отдельный раннер `act_runner` / `forgejo-runner`). Задачи, доски проектов, метки и вехи — встроены. Для маленькой VPS это самый лёгкий способ получить «GitHub у себя».

### Redmine

| Система | Команды |
| :--- | :--- |
| **Gentoo** | `echo "www-apps/redmine ~amd64" >> /etc/portage/package.accept_keywords/redmine` → `emerge --ask www-apps/redmine` (+ PostgreSQL или MariaDB, веб-сервер через Puma/Passenger) |
| **Debian** | `sudo apt install redmine redmine-pgsql` (или `redmine-mysql`) |
| **Arch** | `sudo pacman -S redmine` |

### Taiga, Huly, Vikunja, Kanboard — коротко

```bash
# Taiga
git clone https://github.com/taigaio/taiga-docker && cd taiga-docker
# отредактировать .env (адрес, секреты), затем
./launch-taiga.sh

# Huly (минимум 8 ГБ памяти)
git clone https://github.com/hcengineering/huly-selfhost && cd huly-selfhost
./setup.sh --quick          # затем http://localhost:8087

# Vikunja — один контейнер
docker run -d --name vikunja -p 3456:3456 -v vikunja_files:/app/vikunja/files -v vikunja_db:/db vikunja/vikunja

# Kanboard — один контейнер
docker run -d --name kanboard -p 8081:80 -v kanboard_data:/var/www/app/data kanboard/kanboard:latest
```

> [!warning] Наружу — только через обратный прокси с HTTPS
> Публикуйте трекер через nginx/Caddy с сертификатом, а порты приложений (`8080`, `3456`…) держите на `127.0.0.1`. Включите резервные копии базы и каталога вложений.

---

## 6. MCP для Claude Code — команды подключения

| Трекер | Команда | Вход |
| :--- | :--- | :--- |
| **Jira, Confluence** | `claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp` | `/mcp` → OAuth |
| **Linear** | `claude mcp add --transport http linear-server https://mcp.linear.app/mcp` | `/mcp` → OAuth |
| **GitHub** | `claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer '"$GITHUB_PAT"'"}}'` | PAT |
| **GitLab** (облако и свой) | `claude mcp add -s user --transport http GitLab https://gitlab.com/api/v4/mcp` | `/mcp` → OAuth (scope `mcp`) или fine-grained PAT; на своём GitLab заменить адрес |
| **YouTrack** | `claude mcp add --header "Authorization: Bearer <token>" --transport http youtrack https://youtrack.example.com/mcp` | OAuth или постоянный токен |
| **Plane** (облако) | `claude mcp add --transport http plane https://mcp.plane.so/http/mcp` | OAuth; для self-hosted — локальный сервер через `uvx` |
| **Gitea** | `claude mcp add --transport stdio --scope user gitea --env GITEA_HOST=https://git.example.com --env GITEA_ACCESS_TOKEN=… -- docker run --rm -i -e GITEA_HOST -e GITEA_ACCESS_TOKEN docker.gitea.com/gitea-mcp-server` | токен Gitea |
| **Яндекс Трекер** | добавить HTTP-сервер `https://mcp.tracker.yandex.net/mcp` | OAuth Яндекса, удаление и массовые изменения — с подтверждением |
| **Azure DevOps** | `claude mcp add ado -- npx -y @azure-devops/mcp <организация>` | вход Microsoft |

Все официальные серверы работают **от имени пользователя и с его правами**. Как связка «задача → агент → PR» устроена на примере Jira — [заметка 06 серии](Jira/06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md); для других трекеров схема та же.

---

## 7. Что выбрать

| Задача | Выбор |
| :--- | :--- |
| Научиться тому, что спрашивают на работе | **Jira** ([серия](Jira/00%20%E2%80%94%20Jira%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20Cloud%20%D0%B8%D0%BB%D0%B8%20Data%20Center%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D0%B8%D1%8F%20%D0%B8%20%D0%BA%D0%B0%D1%80%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B8%D0%B8.md)) |
| Свои проекты, CI на GitHub | **GitHub Issues + Projects** — бесплатно, задачи рядом с кодом и Actions |
| Свои проекты, CI на GitLab | **GitLab Issues + Boards** |
| Самый удобный облачный трекер для разработки | **Linear** (на Free — до 250 задач) |
| Всё у себя на маленькой VPS | **Forgejo** или **Gitea**: Git + задачи + CI в одном бинарнике |
| Полноценный трекер у себя | **Plane** (современный, похож на Linear/Jira) или **YouTrack** (до 10 человек бесплатно) |
| Классическое управление проектами (Gantt, учёт времени) у себя | **OpenProject** или **Redmine** |
| Данные в РФ, оплата в рублях | **Яндекс Трекер** (есть официальный MCP), **YouGile** (10 человек бесплатно) |
| Личные дела и простые доски | **Trello** или **Vikunja** у себя |

## 🔗 Ссылки

- Цены: [GitHub](https://github.com/pricing), [GitLab](https://about.gitlab.com/pricing/), [Linear](https://linear.app/pricing), [Plane](https://plane.so/pricing), [OpenProject](https://www.openproject.org/pricing/), [Trello](https://trello.com/pricing), [Asana](https://asana.com/pricing), [ClickUp](https://clickup.com/pricing), [Shortcut](https://www.shortcut.com/pricing), [Azure DevOps](https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/), [YouGile](https://www.yougile.com/prices), [Huly](https://huly.io/pricing), [Jira](https://www.atlassian.com/software/jira/pricing), [YouTrack](https://www.jetbrains.com/youtrack/buy/)
- MCP: [Atlassian](https://github.com/atlassian/atlassian-mcp-server), [Linear](https://linear.app/docs/mcp), [GitHub](https://github.com/github/github-mcp-server), [GitLab](https://docs.gitlab.com/user/model_context_protocol/mcp_server/), [YouTrack](https://www.jetbrains.com/help/youtrack/server/model-context-protocol-server.html), [Plane](https://github.com/makeplane/plane-mcp-server), [Gitea](https://gitea.com/gitea/gitea-mcp), [Яндекс Трекер](https://yandex.ru/support/tracker/ru/user/mcp-server), [Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/mcp-server/mcp-server-overview), [Asana](https://developers.asana.com/docs/using-asanas-mcp-server), [ClickUp](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server), [Shortcut](https://github.com/useshortcut/mcp-server-shortcut)
- Установка: [Plane](https://developers.plane.so/self-hosting/methods/docker-compose), [OpenProject Docker](https://www.openproject.org/docs/installation-and-operations/installation/docker/), [OpenProject пакеты](https://www.openproject.org/docs/installation-and-operations/installation/packaged/), [Huly](https://github.com/hcengineering/huly-selfhost), [Taiga](https://github.com/taigaio/taiga-docker)

#Трекеры #Jira #MCP #Claude_Code #SelfHosted #CI_CD
