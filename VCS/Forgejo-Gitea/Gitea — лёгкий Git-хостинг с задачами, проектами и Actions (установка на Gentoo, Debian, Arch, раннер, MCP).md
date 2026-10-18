---
создал заметку: 2026-10-18T23:50:00
author: WhiteK0T
tags:
  - Gitea
  - Git
  - Трекеры
  - CI_CD
  - SelfHosted
  - MCP
  - Claude_Code
Источник:
  - https://blog.gitea.com/
  - https://blog.gitea.com/release-of-28.0.0/
  - https://blog.gitea.com/release-of-28.2.0/
  - https://docs.gitea.com/installation/install-from-binary
  - https://docs.gitea.com/installation/install-with-docker
  - https://docs.gitea.com/runner/installation/binary/
  - https://docs.gitea.com/runner/registration/
  - https://gitea.com/gitea/gitea-mcp
  - https://about.gitea.com/pricing
---

# 🍵 Gitea — лёгкий Git-хостинг с задачами, проектами и Actions

**Gitea** — self-hosted Git-платформа на Go: репозитории, PR, задачи, канбан-проекты, вики, реестр пакетов, CI **Gitea Actions** (синтаксис GitHub Actions). Один бинарник, работает от 512 МБ памяти, база — SQLite, PostgreSQL или MySQL. Лицензия **MIT**. Развивает компания Gitea Ltd вместе с сообществом.

У Gitea есть форк [Forgejo](Forgejo%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md). Сравнение с ним — в конце той заметки, сравнение со всеми трекерами — в [общей заметке](../Trackers/%D0%A2%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D1%8B%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%E2%80%94%20%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%28%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%8B%20%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%2C%20MCP%20%D0%B4%D0%BB%D1%8F%20Claude%2C%20self-hosted%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%29.md).

---

## 1. Версии (на 18.10.2026)

Осенью 2026 года Gitea **убрала префикс `1.` из номера**: после 1.27.3 (29.08.2026) вышла **28.0.0** (30.09.2026) — это бывшая «1.28». Дальше вышли 28.1.0 (06.10) и **28.2.0** (18.10).

> [!warning] Обновитесь до 28.2.0
> В 28.2.0 закрыто **12 CVE**, в том числе:
> - вход под чужим пользователем через SSH-сертификат;
> - привязка чужого OpenID к аккаунту;
> - дыры в проверке прав в веб-интерфейсе и API;
> - исчерпание памяти через API артефактов Actions.
>
> На 18.10.2026 в Gentoo есть только 1.27.3, в Arch — 28.1.0. Пока пакеты не обновились, сервер, доступный из интернета, лучше держать на официальном бинарнике или образе 28.2.0.

### Что нового в 28

- **Журнал аудита** событий безопасности с экспортом в JSONL. По умолчанию выключен.
- **Бот-аккаунты**: вход только по токену, без интерактивного логина.
- **HTTPS deploy-токены** для Git и LFS на уровне репозитория — аналог SSH deploy-ключей.
- **Вход под другим пользователем** для администратора — с баннером и записью в аудит.
- **Обязательное одобрение CODEOWNERS** в защите веток.
- **Очередь сборок Actions**, предпросмотр артефактов, API досок проектов.

> [!warning] Ломающие изменения 28 — проверить до обновления
> - Регистрация **выключена**, если явно не задано `[service] DISABLE_REGISTRATION = false`.
> - `[server] DOMAIN` **игнорируется** — нужен `ROOT_URL`.
> - Миграции и зеркала ходят через внутренний прокси со списками разрешённых и запрещённых адресов. Пресет `external` удалён.
> - Завершённые прогоны Actions удаляются через **400 дней**. Чтобы хранить их вечно, задайте `RUN_RETENTION_DAYS = 0`.
> - `if:` на уровне задачи вычисляется **до** раскрытия матрицы, `fail-fast` теперь соблюдается.
> - Нужен **Git ≥ 2.25.0**. Сборки для 32-битного x86 и варианты `gogit` больше не выпускаются, в именах файлов загрузки нет суффикса версии ОС.

---

## 2. Задачи и проекты

Возможности те же, что у Forgejo, — общая кодовая база до 2024 года:

| Возможность | Коротко |
| :--- | :--- |
| Задачи | Markdown, `@упоминания`, `#ссылки`, закрепление, вложения |
| **Scoped-метки** | `kind/bug`, `priority/high` — внутри одного префикса метка одна |
| Вехи | срок и прогресс |
| **Проекты** | канбан-доски для репозитория, пользователя или организации, с API (с версии 28) |
| Зависимости | «блокирует / заблокировано» |
| Учёт времени | таймер, оценка, отчёт |
| Шаблоны | `.gitea/ISSUE_TEMPLATE/` — Markdown или YAML-формы; читается и `.github/` |
| Закрытие из коммита | `Fixes #12`, `Closes #12`, `Resolves #12` |

Подробнее про каждую возможность — в [заметке по Forgejo, раздел 2](Forgejo%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md).

---

## 3. Установка

### Gentoo (OpenRC) — основное дерево

`www-apps/gitea` есть в основном дереве со **стабильным** `amd64`: на 18.10.2026 это 1.26.4 и 1.27.3. USE-флаги: `+acct gogit pam sqlite pie`.

```bash
echo "www-apps/gitea sqlite" >> /etc/portage/package.use/gitea   # если база SQLite
emerge --ask www-apps/gitea
rc-update add gitea default
rc-service gitea start
```

| Что | Где |
| :--- | :--- |
| Настройки службы | `/etc/conf.d/gitea` (`GITEA_CONF`, `GITEA_USER=git`, `GITEA_WORK_DIR=/var/lib/gitea`) |
| Конфиг | `/etc/gitea/app.ini` (владелец `root:git`, группе разрешена запись) |
| Данные | `/var/lib/gitea/data`, свои шаблоны — `/var/lib/gitea/custom` |

Консольный клиент **`tea`** — `emerge --ask dev-util/tea`. Раннер Gitea Actions в дереве Gentoo не найден — ставьте бинарник (раздел 4).

### Arch

```bash
sudo pacman -S gitea tea gitea-runner     # 28.1.0, 0.16.0, 5.1.1 — extra
sudo systemctl enable --now gitea
```

### Debian / Ubuntu — официальный бинарник

Пакета Gitea в Debian нет.

```bash
VER=28.2.0
wget -O gitea https://dl.gitea.com/gitea/$VER/gitea-$VER-linux-amd64
wget https://dl.gitea.com/gitea/$VER/gitea-$VER-linux-amd64.sha256
echo "$(cut -d' ' -f1 gitea-$VER-linux-amd64.sha256)  gitea" | sha256sum -c
sudo install -m 755 gitea /usr/local/bin/gitea

sudo adduser --system --shell /bin/bash --gecos 'Git Version Control' \
  --group --disabled-password --home /home/git git
sudo mkdir -p /var/lib/gitea/{custom,data,log}
sudo chown -R git:git /var/lib/gitea && sudo chmod -R 750 /var/lib/gitea
sudo mkdir /etc/gitea && sudo chown root:git /etc/gitea && sudo chmod 770 /etc/gitea
```

Unit-файл для systemd возьмите из документации ([Run as a Linux service](https://docs.gitea.com/installation/linux-service)) или из репозитория (`contrib/systemd/gitea.service`), затем:

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now gitea
```

После мастера установки закройте конфиг от записи: `chmod 750 /etc/gitea && chmod 640 /etc/gitea/app.ini`.

### Docker — на любой системе

```yaml
services:
  server:
    image: docker.gitea.com/gitea:28.2.0
    container_name: gitea
    restart: always
    environment:
      - USER_UID=1000
      - USER_GID=1000
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "127.0.0.1:3000:3000"
      - "222:22"
```

Для PostgreSQL задайте переменные `GITEA__database__DB_TYPE=postgres`, `GITEA__database__HOST=db:5432`, `…__NAME`, `…__USER`, `…__PASSWD` и добавьте сервис `postgres:18`.

> [!note] Образы
> Обычный и rootless-образы между собой несовместимы. Выберите один сразу.

### Entware

Gitea в репозитории Entware нет, а 512 МБ памяти RT-AX56U мало. Для роутера — `git` и bare-репозитории по SSH, как в [заметке по Forgejo](Forgejo%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md).

### Минимальный `app.ini`

```ini
[server]
ROOT_URL  = https://git.example.com/
HTTP_ADDR = 127.0.0.1
SSH_DOMAIN = git.example.com

[service]
DISABLE_REGISTRATION = true

[actions]
ENABLED = true                 ; по умолчанию включено с 1.21
;RUN_RETENTION_DAYS = 0        ; не удалять старые прогоны
```

---

## 4. Gitea Actions и раннер

Workflow лежат в `.gitea/workflows/*.yml`, `.github/workflows/` тоже читается.

```yaml
# .gitea/workflows/ci.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with: { go-version: stable }
      - run: go test ./...
```

Раннер теперь называется **Gitea Runner** (бинарник `gitea-runner`, бывший `act_runner`). Актуальная ветка — 5.x: 5.0.0 вышла 08.10.2026, в Arch — 5.1.1. Задачи раннер выполняет в Docker, **Podman официально не поддерживается**.

```bash
VERSION=5.1.1
curl -sSLO https://dl.gitea.com/gitea-runner/$VERSION/gitea-runner-$VERSION-linux-amd64
curl -sSLO https://dl.gitea.com/gitea-runner/$VERSION/gitea-runner-$VERSION-linux-amd64.sha256
sha256sum -c gitea-runner-$VERSION-linux-amd64.sha256
sudo install -m 0755 gitea-runner-$VERSION-linux-amd64 /usr/local/bin/gitea-runner

sudo useradd --system --home-dir /var/lib/gitea-runner --create-home gitea-runner
sudo install -d /etc/gitea-runner
sudo -u gitea-runner gitea-runner generate-config | sudo tee /etc/gitea-runner/config.yaml >/dev/null
cd /var/lib/gitea-runner
sudo -u gitea-runner gitea-runner -c /etc/gitea-runner/config.yaml register --no-interactive \
  --instance https://git.example.com --token-file /root/runner-token \
  --name vps-runner --labels "ubuntu-latest:docker://gitea/runner-images:ubuntu-latest"
```

Токен регистрации берётся в **Site Administration → Actions → Runners**, в настройках организации или в настройках репозитория. `--token-file` не оставляет токен в истории команд.

Регистрация создаёт файл `.runner` в рабочем каталоге — запускайте службу из того же каталога. Метки задаются в формате `имя:docker://образ`.

**Служба:**

- **systemd** (Debian, Arch) — unit из документации:
  ```ini
  ExecStart=/usr/local/bin/gitea-runner daemon --config /etc/gitea-runner/config.yaml
  WorkingDirectory=/var/lib/gitea-runner
  User=gitea-runner
  TimeoutStopSec=3h          # = runner.shutdown_timeout
  ```
- **OpenRC** (Gentoo) — простой init-скрипт:

```sh
#!/sbin/openrc-run
# /etc/init.d/gitea-runner
command=/usr/local/bin/gitea-runner
command_args="daemon --config /etc/gitea-runner/config.yaml"
command_user="gitea-runner:gitea-runner"
directory=/var/lib/gitea-runner
command_background=yes
pidfile=/run/gitea-runner.pid
depend() { need net; after docker; }
```

```bash
chmod +x /etc/init.d/gitea-runner && rc-update add gitea-runner default && rc-service gitea-runner start
```

Чтобы задачи могли запускать контейнеры, добавьте пользователя в группу `docker` (`usermod -aG docker gitea-runner`). Это права, равные root, поэтому раннер держите на отдельной машине или VM.

Запустить workflow локально, без сервера: `gitea-runner exec -W .gitea/workflows/ci.yml -j test`.

---

## 5. Gitea и Claude — официальный MCP

У Gitea есть **официальный MCP-сервер `gitea-mcp`** (v1.9.0 от 16.10.2026). Он умеет:
- задачи, PR, метки, вехи, проекты;
- учёт времени, вики, Actions;
- релизы, ветки, файлы, поиск, пакеты, уведомления.

**Локально (stdio), через Docker:**

```bash
claude mcp add --transport stdio --scope user gitea \
  --env GITEA_HOST=https://git.example.com \
  --env GITEA_ACCESS_TOKEN=<токен> \
  -- docker run --rm -i -e GITEA_HOST -e GITEA_ACCESS_TOKEN docker.gitea.com/gitea-mcp-server
```

**Как сервер по HTTP** (один на команду, адрес `/mcp`, проверка живости `/healthz`):

```bash
gitea-mcp -t http --port 8080 -H https://git.example.com -oauth -oauth-public-url https://mcp.git.example.com
claude mcp add --transport http gitea https://mcp.git.example.com/mcp
```

В режиме HTTP каждый клиент передаёт свой Bearer-токен. С `-oauth` вход идёт через OAuth 2.1 — так подключаются и веб-клиенты вроде Claude.ai.

**Ограничить агента:**

| Опция | Что делает |
| :--- | :--- |
| `-r` / `GITEA_READONLY=true` | скрыть все инструменты записи |
| `-S` / `GITEA_SCOPES` | оставить инструменты только нужных областей |
| `-O` / `GITEA_TOOLS` | перечислить конкретные инструменты |
| токен Gitea | выдать с минимальными правами (scopes `read:issue`, `write:issue` и т. п.) |

**Без MCP** — `tea`:

```bash
tea login add --name home --url https://git.example.com --token <токен>
tea issues list --state open --labels bug
tea issues create --title "Сломан логин" --description "…" --labels bug
tea pulls create --head feature/x --base main --title "…"
```

Агент в CI — тот же принцип, что в [заметке 06 серии Jira](../Trackers/Jira/06%20%E2%80%94%20Claude%20%2B%20Jira%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20Atlassian%2C%20acli%2C%20Claude%20Code%20%D0%B2%20CI%20%28%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%20%E2%86%92%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%E2%86%92%20PR%29.md): workflow Gitea Actions запускает `claude -p` с секретом `ANTHROPIC_API_KEY`, а `gitea-mcp` или `tea` дают доступ к задачам.

---

## 6. Резервные копии и обновление

```bash
sudo -u git gitea dump -c /etc/gitea/app.ini -f /backup/gitea-$(date +%F).zip
```

Как обновляться:
1. Сделать `dump`.
2. Прочитать раздел breaking changes в посте о выпуске.
3. Заменить бинарник или образ.
4. Перезапустить. Миграции базы применяются автоматически при старте.

Откатиться на старую версию с той же базой **нельзя** — только восстановиться из копии.

---

## 7. Платные варианты

| Вариант | Цена | Что добавляет |
| :--- | :--- | :--- |
| **Gitea** (open source) | бесплатно, MIT | всё описанное выше |
| **Gitea Enterprise** | от **$9.5** за пользователя в месяц, годовой контракт, 30 дней пробно *(на странице указано «$9.5$19*», точную цифру уточняйте у продаж)* | SAML SSO, автомасштабируемые раннеры в Kubernetes, приоритетные уведомления о уязвимостях, поддержка с SLA |
| **Gitea Cloud** | цена на странице не указана | управляемый Gitea |

## 🔗 Ссылки

- [Gitea](https://about.gitea.com) · [блог с выпусками](https://blog.gitea.com/) · [документация](https://docs.gitea.com)
- [Установка из бинарника](https://docs.gitea.com/installation/install-from-binary) · [Docker](https://docs.gitea.com/installation/install-with-docker) · [Gitea Runner](https://docs.gitea.com/runner/installation/binary/)
- [gitea-mcp](https://gitea.com/gitea/gitea-mcp) · [tea](https://gitea.com/gitea/tea)

#Gitea #Git #Трекеры #CI_CD #SelfHosted #MCP #Claude_Code
