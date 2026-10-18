---
создал заметку: 2026-10-18T23:30:00
author: WhiteK0T
tags:
  - Forgejo
  - Git
  - Трекеры
  - CI_CD
  - SelfHosted
  - Claude_Code
Источник:
  - https://forgejo.org/releases/
  - https://forgejo.org/2026-10-release-v17-0/
  - https://forgejo.org/docs/latest/admin/installation/binary/
  - https://forgejo.org/docs/next/admin/actions/installation/binary/
  - https://forgejo.org/docs/next/admin/actions/registration/
  - https://forgejo.org/2024-12-gitea-compatibility
---

# 🦊 Forgejo — свой Git-хостинг с задачами, досками и Actions

**Forgejo** — self-hosted платформа для Git, по ощущениям как GitHub: репозитории, pull request'ы, задачи (issues), доски проектов, вики, реестр пакетов и CI **Forgejo Actions** с синтаксисом GitHub Actions. Это один бинарник на Go, ему хватает 512 МБ памяти — поэтому Forgejo хорошо подходит для маленькой VPS.

- Появился в 2022 году как форк [Gitea](Gitea%20%E2%80%94%20%D0%BB%D1%91%D0%B3%D0%BA%D0%B8%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md).
- С 2024 года развивается **отдельно** от Gitea (hard fork).
- Проектом управляет сообщество под крылом некоммерческой Codeberg e.V. — на Forgejo работает [Codeberg.org](https://codeberg.org).
- Лицензия **GPL-3.0+**.

Сравнение с другими трекерами — в [общей заметке](../Trackers/%D0%A2%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D1%8B%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%94%20%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%28%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%8B%20%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%2C%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%2C%20self-hosted%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%29.md).

---

## 1. Версии и поддержка (на 18.10.2026)

| Ветка | Последний выпуск | Поддержка до | Когда брать |
| :--- | :--- | :--- | :--- |
| **v17.0** (stable) | 17.0.0 — 15.10.2026 | 28.01.2027 | нужны новые функции |
| **v16.0** (stable) | 16.0.6 | **29.10.2026** — заканчивается | только переход на 17 или 15 |
| **v15.0 LTS** | 15.0.10 | **15.07.2027** | сервер «поставил и забыл» |

Обычные ветки поддерживаются примерно три месяца, LTS — около года. Для своей VPS разумно брать **LTS** и раз в год переходить на следующую.

**Что нового в v17:**
- кнопка «Donate» из `FUNDING.yml`;
- автодополнение `#` (задачи и PR) и `!` (только PR) в комментариях;
- приглашения в организацию по почте;
- переработанный LFS;
- новые методы API для Actions: перезапуск, логи в NDJSON;
- сводки задач (job summary) через `$FORGEJO_STEP_SUMMARY`, нужен раннер 13.2+;
- миграция из Bitbucket Data Center.

> [!warning] Ломающие изменения v17
> - Абсолютные ссылки в отрисованных документах (README и т. п.) теперь считаются от корня репозитория, а не инстанса.
> - Вебхуки «action run» заменены событиями workflow run. Старые вебхуки придётся перенастроить вручную.

---

## 2. Что внутри для работы с задачами

| Возможность | Как устроено |
| :--- | :--- |
| **Задачи (issues)** | Markdown, упоминания `@user`, ссылки `#123`, вложения, реакции, закрепление (pin), блокировка обсуждения |
| **Метки** | обычные и **scoped** (`kind/bug`, `priority/high`): метки с одним префиксом взаимоисключающие. Наборы меток для организации |
| **Вехи (milestones)** | срок, процент закрытых задач |
| **Проекты** | **канбан-доски** на уровне репозитория, пользователя или организации; колонки, карточки задач и PR |
| **Зависимости** | «блокирует / заблокировано» между задачами; закрыть задачу с открытыми блокерами нельзя |
| **Учёт времени** | таймер или ручной ввод, оценка (estimate), отчёт по затраченному времени |
| **Шаблоны** | `.forgejo/issue_template/*.md` или `*.yaml` (формы с полями), то же для PR. Читаются и пути `.gitea/` и `.github/` |
| **Закрытие из коммита** | `Fixes #12`, `Closes #12`, `Resolves #12` в коммите или описании PR. `Ref #12` — только ссылка |
| **Поиск** | фильтры по метке, вехе, проекту, автору и исполнителю; встроенный поиск или внешний индекс (Bleve, Elasticsearch, Meilisearch) |

Отдельного языка запросов, как JQL в Jira, нет — Forgejo закрывает задачи небольшой команды, а не корпоративный портфель проектов.

---

## 3. Установка

### Gentoo (OpenRC) — оверлей GURU

Forgejo есть только в **GURU**: на 18.10.2026 там 15.0.7, 15.0.9 (LTS), 16.0.3 и 16.0.5, все под `~amd64`. Ebuild ставит службы OpenRC и systemd и использует того же пользователя `git`, что и Gitea. Поэтому пакет **блокирует `www-apps/gitea`** — на одной машине стоит что-то одно.

```bash
emerge --ask app-eselect/eselect-repository
eselect repository enable guru
emaint sync -r guru

# LTS-ветка: разрешить ~amd64 только для 15.x
echo "=www-apps/forgejo-15* ~amd64" >> /etc/portage/package.accept_keywords/forgejo
emerge --ask www-apps/forgejo            # USE: +acct pam sqlite pie

rc-update add forgejo default
rc-service forgejo start
```

Конфиг службы — `/etc/conf.d/forgejo`, конфиг приложения — `/etc/forgejo/app.ini`, данные — `/var/lib/forgejo`.

### Arch

```bash
sudo pacman -S forgejo                   # extra, 16.0.6 на 18.10.2026
sudo systemctl enable --now forgejo
```

Конфиг — `/etc/forgejo/app.ini`. Там же есть `forgejo-runner` (13.2.0) и консольный клиент `forgejo-cli` (команда `fj`).

### Debian / Ubuntu — официальный бинарник

Пакета сервера в Debian нет, есть только клиент `forgejo-cli`. Ставим бинарник:

```bash
VER=15.0.10                              # LTS; или 17.0.0
wget -O forgejo https://codeberg.org/forgejo/forgejo/releases/download/v$VER/forgejo-$VER-linux-amd64
wget -O forgejo.asc https://codeberg.org/forgejo/forgejo/releases/download/v$VER/forgejo-$VER-linux-amd64.asc
gpg --keyserver keys.openpgp.org --recv EB114F5E6C0DC2BCDD183550A4B61A2DC5923710
gpg --verify forgejo.asc forgejo

sudo install -m 755 forgejo /usr/local/bin/forgejo
sudo apt install git git-lfs

sudo adduser --system --shell /bin/bash --gecos 'Git Version Control' \
  --group --disabled-password --home /home/git git
sudo mkdir /var/lib/forgejo /etc/forgejo
sudo chown git:git /var/lib/forgejo && sudo chmod 750 /var/lib/forgejo
sudo chown root:git /etc/forgejo && sudo chmod 770 /etc/forgejo

sudo wget -O /etc/systemd/system/forgejo.service \
  https://codeberg.org/forgejo/forgejo/raw/branch/forgejo/contrib/systemd/forgejo.service
sudo systemctl daemon-reload
sudo systemctl enable --now forgejo
```

Для PostgreSQL или MariaDB раскомментируйте строки `Wants=` и `After=` в unit-файле.

Ключ подписи — тот, что указан на странице загрузки Forgejo. Перед установкой сверьте отпечаток.

### Docker — на любой системе

```yaml
# docker-compose.yml
services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:15      # LTS; или :17
    restart: unless-stopped
    environment:
      - USER_UID=1000
      - USER_GID=1000
    volumes:
      - ./data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "127.0.0.1:3000:3000"   # веб — только через обратный прокси
      - "2222:22"               # SSH для git
```

### Первый запуск

1. Откройте `http://localhost:3000/` — появится мастер установки. Выберите базу данных:
   - **SQLite** — для себя и пары человек;
   - **PostgreSQL** — если пользователей больше.
2. Укажите `ROOT_URL` (`https://git.example.com/`) и создайте администратора.
3. Закройте конфиг от записи:
   ```bash
   chmod 750 /etc/forgejo && chmod 640 /etc/forgejo/app.ini
   ```
4. Минимальные правки в `app.ini`:

```ini
[server]
ROOT_URL = https://git.example.com/
SSH_DOMAIN = git.example.com
HTTP_ADDR = 127.0.0.1

[service]
DISABLE_REGISTRATION = true       ; чужие не регистрируются
REQUIRE_SIGNIN_VIEW = false       ; true — закрыть всё от анонимов

[actions]
ENABLED = true                    ; включено по умолчанию
```

### Entware (роутер)

Пакетов Forgejo и Gitea в Entware **нет** — ни для armv7, ни для aarch64. А 512 МБ памяти RT-AX56U — это нижняя граница даже для одного Forgejo. Роутер лучше использовать как простое Git-хранилище:

```sh
opkg install git git-http
git init --bare /opt/git/project.git      # доступ: ssh://admin@router/opt/git/project.git
```

Задачи и CI в таком случае держите на VPS.

---

## 4. Forgejo Actions — CI

Workflow лежат в `.forgejo/workflows/*.yml`, файлы из `.github/workflows/` тоже читаются. Синтаксис — как у GitHub Actions.

```yaml
# .forgejo/workflows/ci.yml
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: docker            # метка вашего раннера
    container:
      image: node:22-bookworm
    steps:
      - uses: https://code.forgejo.org/actions/checkout@v4
      - run: npm ci && npm test
      - run: echo "### Тесты прошли ✅" >> "$FORGEJO_STEP_SUMMARY"
```

Короткая форма `uses: actions/checkout@v4` берёт действие с инстанса по умолчанию — `DEFAULT_ACTIONS_URL` в `[actions]`, обычно `https://data.forgejo.org`. С полным URL понятнее, откуда берётся код.

### Раннер `forgejo-runner`

Раннер ставится **отдельно** — лучше на другую машину или в изолированный контейнер: он исполняет код из репозиториев.

| Система | Установка |
| :--- | :--- |
| **Gentoo** | GURU: `emerge --ask dev-util/forgejo-runner` (12.13.2, 13.2.0) |
| **Arch** | `pacman -S forgejo-runner` |
| **Debian** | бинарник (ниже) |

```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
V=$(curl -s https://data.forgejo.org/api/v1/repos/forgejo/runner/releases/latest | jq -r .name | cut -c2-)
wget -O forgejo-runner https://code.forgejo.org/forgejo/runner/releases/download/v$V/forgejo-runner-$V-linux-$ARCH
sudo install forgejo-runner /usr/local/bin/
sudo useradd --create-home runner && sudo usermod -aG docker runner
```

**Регистрация (новый способ):**

1. Откройте страницу раннеров:
   - для всего инстанса — `/admin/actions/runners`;
   - для организации — `/org/<org>/settings/actions/runners`;
   - для репозитория — `/<owner>/<repo>/settings/actions/runners`.
2. Нажмите **Create new runner** — появятся UUID и токен.
3. Впишите их в конфиг раннера:

```yaml
# config.yml (forgejo-runner generate-config > config.yml)
server:
  connections:
    forgejo:
      url: https://git.example.com/
      uuid: <UUID>
      token: <TOKEN>
runner:
  labels:
    - "docker:docker://node:22-bookworm"
```

```bash
forgejo-runner -c config.yml daemon
```

**Регистрация без браузера** — прямо на машине с Forgejo:

```bash
forgejo forgejo-cli actions register --name vps-runner --scope myorg \
  --secret $(openssl rand -hex 20)
```

Команда выведет UUID. Секрет и будет токеном. Старая команда `forgejo-runner register` объявлена устаревшей.

> [!warning] Безопасность раннера
> - Метка `host` запускает задачи прямо на хосте, без изоляции. Используйте её только для своих доверенных репозиториев.
> - Docker-сокет у раннера фактически даёт root на машине. Держите раннер отдельно от Forgejo.

---

## 5. Переезд с Gitea и с GitHub

- **С Gitea «на месте»** (подменить бинарник на той же базе) возможно только с **Gitea до 1.22** включительно и только в **Forgejo до v10.0**. Дальше обновляться уже внутри Forgejo. Начиная с Gitea 1.23 базы несовместимы.
- **С Gitea 1.23+**, GitHub, GitLab, Bitbucket, Gogs переносите через **New Migration**: репозитории, задачи, PR, метки, вехи, релизы и вики. Нужен токен источника.
- **Зеркало** — pull-зеркало чужого репозитория или push-зеркало на GitHub (**Settings → Repository → Mirror**).

---

## 6. Forgejo и Claude

Официального MCP-сервера у Forgejo нет. Варианты:

1. **Сторонний MCP-сервер** для Forgejo — их несколько на Codeberg и GitHub. Перед подключением прочитайте код и выдайте токен с минимальными правами.
2. **Gitea MCP** (`gitea-mcp`) может работать с Forgejo частично, пока их API во многом совпадает. Совместимость никто не гарантирует, так что проверяйте на тестовом репозитории.
3. **Консольный клиент `fj`** (`forgejo-cli`, есть в Arch и Debian) плюс `curl` к REST API (`/api/v1`, Swagger на `/api/swagger`). Claude Code вызывает их из Bash, как `gh` у GitHub:

```bash
curl -s -H "Authorization: token $FORGEJO_TOKEN" \
  "https://git.example.com/api/v1/repos/me/app/issues?state=open&labels=bug" | jq '.[].title'
```

Агент в CI: workflow Forgejo Actions запускает `claude -p "…"` с секретом `ANTHROPIC_API_KEY` в репозитории. Схема та же, что в [заметке 06 серии Jira](../Trackers/Jira/06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md), только без `claude-code-action`: это действие написано под GitHub.

---

## 7. Резервные копии

```bash
# на Gentoo/Arch/Debian (служба под пользователем git)
sudo -u git forgejo dump -c /etc/forgejo/app.ini -f /backup/forgejo-$(date +%F).zip
```

В архив попадают:
- база данных;
- репозитории;
- `app.ini` с секретами `SECRET_KEY`, `INTERNAL_TOKEN` и `JWT_SECRET`.

Без этих секретов не восстановятся двухфакторная аутентификация и токены — храните архив зашифрованным.

---

## 8. Forgejo или Gitea

| | **Forgejo** | **Gitea** |
| :--- | :--- | :--- |
| Кто развивает | сообщество, Codeberg e.V. | Gitea Ltd (компания) и сообщество |
| Лицензия | GPL-3.0+ | MIT |
| LTS | да, около года | нет, обычные ветки |
| Федерация (ForgeFed) | в разработке | нет |
| Официальный MCP | нет | **есть** (`gitea-mcp`) |
| Пакет Gentoo | только GURU | основное дерево, стабильный `amd64` |
| Пакет Arch | `forgejo` | `gitea` |

Если важны открытая модель управления и LTS — **Forgejo**. Если нужны официальный MCP для Claude и пакет из основного дерева Gentoo — **Gitea**.

## 🔗 Ссылки

- [Forgejo](https://forgejo.org) · [выпуски и сроки поддержки](https://forgejo.org/releases/) · [документация](https://forgejo.org/docs/latest/)
- [Установка из бинарника](https://forgejo.org/docs/latest/admin/installation/binary/) · [раннер](https://forgejo.org/docs/next/admin/actions/installation/binary/) · [регистрация раннера](https://forgejo.org/docs/next/admin/actions/registration/)
- [Совместимость с Gitea (Gitea 1.22 — последняя для прямого перехода)](https://forgejo.org/2024-12-gitea-compatibility)

#Forgejo #Git #Трекеры #CI_CD #SelfHosted #Claude_Code
