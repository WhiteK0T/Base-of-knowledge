---
создал заметку: 2026-10-19T00:05:00
author: WhiteK0T
tags:
  - Jenkins
  - CI_CD
  - DevOps
  - SelfHosted
  - Java
  - Docker
  - MCP
  - Claude_Code
Источник:
  - https://www.jenkins.io/doc/
  - https://www.jenkins.io/changelog/
  - https://www.jenkins.io/changelog-stable/
  - https://www.jenkins.io/doc/book/platform-information/support-policy-java/
  - https://www.jenkins.io/doc/book/installing/linux/
  - https://www.jenkins.io/doc/book/installing/docker/
  - https://www.jenkins.io/doc/book/pipeline/syntax/
  - https://www.jenkins.io/security/advisories/
  - https://www.jenkins.io/security/advisory/2026-09-02/
  - https://plugins.jenkins.io/mcp-server/
  - https://plugins.jenkins.io/configuration-as-code/
  - https://github.com/jenkinsci/docker-agents/blob/master/README_inbound-agent.md
  - https://packages.gentoo.org/packages/dev-util/jenkins-bin
  - https://archlinux.org/packages/extra/any/jenkins/
---

# 🤵 Jenkins — self-hosted CI/CD сервер

**Jenkins** — свободный (MIT) сервер автоматизации на Java: собирает, тестирует и выкладывает код по событию в Git, по расписанию или по кнопке. В отличие от GitHub Actions, GitLab CI и Forgejo/Gitea Actions он **не привязан к Git-хостингу**: один Jenkins может обслуживать репозитории на GitHub, GitLab и своём Forgejo сразу. Всё, что сверх ядра, — плагины (их тысячи).

> Данные сверены с jenkins.io, Docker Hub и репозиториями Gentoo/Arch на 19.10.2026.

## Когда Jenkins, а когда встроенный CI

| | Jenkins | GitHub Actions / GitLab CI / Forgejo Actions |
| :--- | :--- | :--- |
| Где живёт | отдельный сервер (свой) | внутри Git-хостинга |
| Конфигурация | `Jenkinsfile` (Groovy DSL) в репозитории + настройки сервера | YAML в репозитории |
| Расширения | плагины ядра (ставятся на сервер) | готовые actions / шаблоны |
| Несколько хостингов сразу | ✅ | ❌ (каждый свой) |
| Поддержка | сам: обновления ядра и плагинов, бэкапы, Java | хостинг делает за вас |
| Ресурсы | от ~1 ГБ RAM на контроллер, Java | раннер — лёгкий бинарник |

Jenkins выбирают, когда нужны сложные цепочки сборок, сборка на своём железе (в т.ч. Windows, macOS, ARM), несколько Git-хостингов или уже есть парк задач. Для одного проекта на GitHub/Forgejo встроенные Actions обычно проще — см. [Forgejo](../Forgejo-Gitea/Forgejo%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Git-%D1%85%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20%D1%81%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B0%D0%BC%D0%B8%2C%20%D0%B4%D0%BE%D1%81%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B8%20Actions%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch%2C%20%D1%80%D0%B0%D0%BD%D0%BD%D0%B5%D1%80%2C%20MCP%29.md) и [GitHub Actions](../GitHub/GitHub%20Actions%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D1%87%D1%91%D1%82%D1%87%D0%B8%D0%BA%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BE%D0%BA%20%D0%B2%20README.md).

## Версии и Java (октябрь 2026)

Две линии выпусков:

- **Weekly** — каждую неделю, сейчас **2.586** (12.10.2026);
- **LTS** — раз в ~12 недель новая база + точечные обновления, сейчас **2.580.1** (30.09.2026). Для своего сервера берите LTS.

| Java | Поддержка в Jenkins | Конец поддержки |
| :--- | :--- | :--- |
| **21** | с LTS 2.479.1 | сентябрь 2027 |
| **25** | с LTS 2.541.1 | сентябрь 2029 |
| 17 | последняя LTS 2.541.3, с 2.555.1 — не запускается | — |

Что важно в свежих выпусках:

- **2.580.1 LTS** перестал встраивать несколько плагинов (SSH server, JavaMail API, Instance Identity и др.), `jenkins.war` похудел на 20+ МБ. Если что-то из них нужно — поставьте из менеджера плагинов после обновления. Плюс CLI принимает ключи ECDSA и Ed25519, появились правила сложности паролей.
- **2.568.3 LTS / 2.580 weekly** закрывают 13 уязвимостей ядра из [бюллетеня 02.09.2026](https://www.jenkins.io/security/advisory/2026-09-02/) (8 высокой важности: десериализация, XSS в просмотре системного лога, фиксация сессии, утечка CSRF-токена). Всё, что старше, — обновлять.
- **2.584 weekly** убрал поддержку агентов (Remoting / `agent.jar`) старше августа 2024 — старые агенты надо обновить.

## Основные понятия

| Понятие | Что это |
| :--- | :--- |
| **Controller** (раньше master) | сервер с веб-интерфейсом, хранит настройки и историю, раздаёт работу |
| **Agent** (node) | машина или контейнер, где реально идут сборки; подключается по SSH или сам (inbound, TCP/WebSocket) |
| **Executor** | слот для одной сборки на агенте; на контроллере ставьте **0** — собирать на нём небезопасно |
| **Job / Item** | задача: Freestyle (кнопки в UI), **Pipeline** (`Jenkinsfile`), **Multibranch Pipeline** (по задаче на каждую ветку и PR), **Organization Folder** (все репозитории организации) |
| **Build** | один запуск задачи: лог, артефакты, результаты тестов |
| **Credentials** | хранилище секретов (пароли, токены, SSH-ключи, файлы); в пайплайне подставляются по ID |
| **Plugins** | всё сверх ядра: Git, Pipeline, Docker, интеграции с хостингами |
| **`JENKINS_HOME`** | вся «память» сервера: настройки, задачи, история, плагины, секреты. Бэкапить именно её |

## Установка

### Gentoo (OpenRC)

Пакет `dev-util/jenkins-bin` — готовый `jenkins.war` из официального LTS-репозитория:

| Версия | Слот | amd64 | arm64 |
| :--- | :--- | :--- | :--- |
| 2.541.3 | lts | стабильная | стабильная |
| **2.568.3** | lts | **стабильная** | `~arm64` |
| 2.555.1 | lts | `~amd64` | `~arm64` |
| 2.561 | 0 (weekly) | `~amd64` | `~arm64` |

Самой свежей LTS 2.580.1 в дереве пока нет; 2.568.3 уже содержит исправления от 02.09.2026.

```bash
# Java 21 (или 25): ebuild разрешает и 17, но Jenkins 2.555+ на ней не стартует
sudo emerge --ask dev-java/openjdk-bin:21          # или dev-java/openjdk:21
sudo eselect java-vm list
sudo eselect java-vm set system openjdk-bin-21

sudo emerge --ask dev-util/jenkins-bin:lts
```

Файлы:

- WAR — `/opt/jenkins/jenkins.war`;
- **`JENKINS_HOME` — `/var/lib/jenkins/home`** (не `/var/lib/jenkins`, как в Debian);
- лог — `/var/log/jenkins/jenkins.log`;
- настройки службы — `/etc/conf.d/jenkins`.

Слушать только localhost (наружу — через nginx, см. ниже):

```bash
# /etc/conf.d/jenkins
JENKINS_PORT="8080"
JENKINS_ARGS="--httpListenAddress=127.0.0.1"
JENKINS_JAVA_OPTIONS="-Djava.awt.headless=true -Xmx1g"
```

```bash
sudo rc-update add jenkins default
sudo rc-service jenkins start
sudo cat /var/lib/jenkins/home/secrets/initialAdminPassword
```

Init-скрипт берёт Java из `java-config --jre-home`, то есть системную VM из `eselect java-vm`. Если Jenkins падает сразу после старта — первым делом проверьте, что там не Java 17.

### Debian / Ubuntu (systemd)

В репозиториях Debian Jenkins нет — ставим из официального `pkg.jenkins.io`. Ветка `debian-stable` — это LTS. Ключ подписи с 2026 года новый: `jenkins.io-2026.key`.

```bash
# сначала Java, иначе служба не найдёт её
sudo apt update
sudo apt install fontconfig openjdk-21-jre

sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins
```

Если `openjdk-21-jre` в вашем релизе нет (старые Ubuntu/Debian) — возьмите Temurin из репозитория Adoptium или запускайте Jenkins в Docker.

Настройки — через `systemctl edit jenkins` (файл `/etc/default/jenkins` больше не используется):

```ini
[Service]
Environment="JENKINS_LISTEN_ADDRESS=127.0.0.1"
Environment="JENKINS_PORT=8080"
Environment="JAVA_OPTS=-Djava.awt.headless=true -Xmx1g"
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

`JENKINS_HOME` — `/var/lib/jenkins`.

### Arch (systemd)

Пакет `jenkins` в `extra` собирается из исходников и идёт **по weekly-линии** (сейчас 2.586), LTS в официальных репозиториях нет. Хотите LTS — Docker.

```bash
sudo pacman -S jenkins          # потребует Java 25 (java-runtime=25)
```

Особенности пакета (`/etc/conf.d/jenkins`):

- порт по умолчанию **8090**, а не 8080;
- Java 25: `JAVA=/usr/lib/jvm/java-25-openjdk/bin/java`;
- память ограничена: `JAVA_ARGS=-Xmx512m` — для пары плагинов мало, поднимите до `-Xmx1g`;
- `JENKINS_HOME=/var/lib/jenkins`.

```bash
# /etc/conf.d/jenkins
JAVA_ARGS=-Xmx1g
JENKINS_OPTS=--httpListenAddress=127.0.0.1
```

```bash
sudo systemctl enable --now jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Docker (любой дистрибутив)

Официальный образ `jenkins/jenkins`. Теги: `lts` = `lts-jdk21` (2.580.1), есть `lts-jdk25`, `latest` — weekly. Архитектуры: amd64, arm64, ppc64le, s390x, riscv64 (**armv7 нет**).

```yaml
# docker-compose.yml
services:
  jenkins:
    image: jenkins/jenkins:lts-jdk21
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"     # веб, только localhost
      - "127.0.0.1:50000:50000"   # TCP для inbound-агентов (не нужен, если агенты по WebSocket)
    volumes:
      - jenkins_home:/var/jenkins_home
volumes:
  jenkins_home:
```

```bash
docker compose up -d
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Docker на хостах: Gentoo — `app-containers/docker` + `app-containers/docker-compose`, `rc-update add docker default`; Debian — `docker.io` + `docker-compose` (или репозиторий Docker); Arch — `docker docker-compose`. Подробнее — [Linux/Containers](../../Linux/Containers/).

> Не пробрасывайте `/var/run/docker.sock` в контейнер контроллера ради «Docker внутри Jenkins»: это root на хосте для любого, кто может править `Jenkinsfile`. Сборки в контейнерах запускайте на **агенте** с Docker.

### Entware (ASUS RT-AX56U)

Ни Jenkins, ни Java в Entware для armv7 нет, образов Jenkins под armv7 тоже нет — роутер не годится ни как контроллер, ни как агент. Зато роутер может быть **целью деплоя**: пайплайн по SSH копирует на него конфиги или скрипты (пример ниже, плагин SSH Agent).

## Первый запуск

1. Открыть `http://localhost:8080` (или туннель `ssh -L 8080:127.0.0.1:8080 vps` с ноутбука).
2. Ввести `initialAdminPassword`.
3. **Install suggested plugins** (Git, Pipeline, Credentials и т.д.) или выбрать вручную.
4. Создать администратора, указать **Jenkins URL** (тот, по которому к нему ходят снаружи — от него зависят ссылки и вебхуки).
5. *Manage Jenkins → Nodes → Built-In Node → Number of executors = 0*, сборки — только на агентах.
6. *Manage Jenkins → Security*: «Matrix-based security» или «Role-based» (плагин Role Strategy), регистрацию пользователей выключить. В 2.586 Jenkins сам предупреждает, если всем вошедшим выдан полный доступ.

### nginx перед Jenkins

```nginx
server {
    listen 443 ssl http2;
    server_name ci.example.org;
    # ssl_certificate ... (certbot / acme.sh)

    location / {
        proxy_pass         http://127.0.0.1:8080;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;     # WebSocket для агентов и CLI
        proxy_set_header   Connection "upgrade";
        proxy_request_buffering off;
        proxy_buffering    off;                       # живой лог сборки
        client_max_body_size 100m;                    # загрузка плагинов и артефактов
    }
}
```

nginx: Gentoo `www-servers/nginx`, Debian `nginx`, Arch `nginx`.

## Агенты

### SSH-агент (Linux-машина)

Контроллер сам заходит на агент по SSH и запускает `agent.jar`. На агенте нужны только Java 21+ и пользователь:

```bash
# на агенте
sudo useradd -m -s /bin/bash jenkins     # Gentoo/Debian/Arch одинаково
# Java: Gentoo openjdk-bin:21, Debian openjdk-21-jre-headless, Arch jre21-openjdk-headless
sudo -u jenkins mkdir -p ~jenkins/.ssh   # сюда публичный ключ контроллера
```

В Jenkins: плагин **SSH Build Agents** → *Nodes → New node → Launch agents via SSH*, учётка — SSH-ключ из Credentials, *Host Key Verification Strategy* — «Known hosts file» (не «Non verifying»).

### Inbound-агент в Docker (WebSocket)

Агент сам подключается к контроллеру — удобно, если агент за NAT. С WebSocket хватает одного HTTPS-порта, 50000 открывать не нужно.

В Jenkins: *Nodes → New node → Permanent Agent*, *Launch method: Launch agent by connecting it to the controller*, галка **Use WebSocket**. На странице агента появится секрет.

```bash
docker run -d --init --name jenkins-agent --restart unless-stopped \
  -e JENKINS_URL=https://ci.example.org \
  -e JENKINS_SECRET=<секрет со страницы агента> \
  -e JENKINS_AGENT_NAME=docker-agent-1 \
  -e JENKINS_AGENT_WORKDIR=/home/jenkins/agent \
  -e JENKINS_WEB_SOCKET=true \
  jenkins/inbound-agent:latest-jdk21
```

### Агенты «на лету»

Плагины **Docker** и **Kubernetes** поднимают агент-контейнер под каждую сборку и удаляют после. Для домашнего сервера достаточно одного постоянного агента с Docker и `agent { docker { ... } }` в пайплайне (ниже).

## Pipeline: `Jenkinsfile`

Пайплайн хранится в корне репозитория как `Jenkinsfile`. Два синтаксиса: **Declarative** (структурированный, рекомендуемый) и **Scripted** (чистый Groovy, `node { ... }`). Ниже — declarative.

```groovy
pipeline {
    agent { label 'linux' }                 // на каком агенте

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
    }

    environment {
        APP = 'myapp'
    }

    parameters {
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Выложить после сборки')
    }

    triggers {
        cron('H 3 * * *')                   // H — «размазать» время по задачам
    }

    stages {
        stage('Build') {
            agent {
                docker { image 'maven:3-eclipse-temurin-21'; reuseNode true }   // плагин Docker Pipeline
            }
            steps {
                sh 'mvn -B -DskipTests package'
            }
        }

        stage('Test') {
            parallel {
                stage('Unit') {
                    steps { sh 'mvn -B test' }
                    post { always { junit '**/target/surefire-reports/*.xml' } }
                }
                stage('Lint') {
                    steps { sh './scripts/lint.sh' }
                }
            }
        }

        stage('Deploy') {
            when {
                allOf { branch 'master'; expression { params.DEPLOY } }
            }
            steps {
                withCredentials([string(credentialsId: 'deploy-token', variable: 'TOKEN')]) {
                    sh 'curl -fsS -H "Authorization: Bearer $TOKEN" https://deploy.example.org/hook'   // одинарные кавычки: секрет не попадёт в Groovy-строку
                }
            }
        }
    }

    post {
        success { archiveArtifacts artifacts: 'target/*.jar', fingerprint: true }
        failure { echo "Сборка ${env.BUILD_NUMBER} упала: ${env.BUILD_URL}" }
        cleanup { cleanWs() }               // плагин Workspace Cleanup
    }
}
```

Полезное:

- **`when`**: `branch`, `changeRequest()` (это PR), `tag 'v*'`, `changeset 'docs/**'`, `environment`, `expression`.
- **`input`** — ручное подтверждение перед шагом (например, перед продом).
- **`stash` / `unstash`** — передать файлы между стадиями на разных агентах.
- **Shared Libraries** — общий Groovy-код для многих репозиториев (`@Library('my-lib') _`).
- **Replay** в интерфейсе сборки — перезапустить с изменённым `Jenkinsfile`, не коммитя.
- Генератор шагов: *Pipeline Syntax* на странице задачи (`/job/<имя>/pipeline-syntax/`).
- Проверить синтаксис без запуска: `curl -X POST -u user:token -F "jenkinsfile=<Jenkinsfile" https://ci.example.org/pipeline-model-converter/validate`.

### Деплой на роутер по SSH

```groovy
stage('Deploy to router') {
    steps {
        sshagent(credentials: ['router-ssh']) {          // плагин SSH Agent
            sh '''
                scp -o StrictHostKeyChecking=yes conf/*.conf admin@router:/opt/etc/myapp/
                ssh admin@router /opt/etc/init.d/S99myapp restart
            '''
        }
    }
}
```

`router` — имя из `~/.ssh/config` и `known_hosts` на агенте.

## Связка с Git-хостингами

Обычная схема — **Multibranch Pipeline** (или Organization Folder): Jenkins сам находит ветки и PR с `Jenkinsfile`, а хостинг сообщает о пушах вебхуком и показывает статус сборки у коммита.

| Хостинг | Плагин | Вебхук |
| :--- | :--- | :--- |
| GitHub | **GitHub Branch Source** (лучше через GitHub App, а не токен) | `https://<jenkins>/github-webhook/` |
| GitLab | **GitLab Branch Source** | плагин может создать хуки сам |
| Gitea / Forgejo | **Gitea** (Forgejo совместим по API, плагин с ним обычно работает) | галка «manage hooks» — плагин создаёт хуки сам |
| Любой Git | **Git** + опрос (`pollSCM`) или Generic Webhook Trigger | — |

Для приватных репозиториев — учётка в Credentials (токен или SSH-ключ). Если Jenkins за NAT и вебхуки до него не доходят — используйте `pollSCM('H/5 * * * *')` или поднимите туннель.

## Configuration as Code (JCasC)

Плагин **Configuration as Code** описывает настройки сервера YAML-файлом — сервер можно поднять заново из Git, а не кликать.

```yaml
# /var/lib/jenkins/casc.yaml  (Gentoo: /var/lib/jenkins/home/casc.yaml)
jenkins:
  systemMessage: "CI — настроен через JCasC"
  numExecutors: 0
  securityRealm:
    local:
      allowsSignup: false
      users:
        - id: admin
          password: "${JENKINS_ADMIN_PASSWORD}"   # из переменной окружения, не в Git
  authorizationStrategy:
    loggedInUsersCanDoAnything:
      allowAnonymousRead: false
unclassified:
  location:
    url: https://ci.example.org/
```

Путь задаётся переменной `CASC_JENKINS_CONFIG` (по умолчанию `$JENKINS_HOME/jenkins.yaml`). Текущую конфигурацию можно выгрузить: *Manage Jenkins → Configuration as Code → View/Download*. Для командной работы `loggedInUsersCanDoAnything` замените на матрицу прав (плагин Matrix Authorization).

Плагины для образа — списком:

```dockerfile
FROM jenkins/jenkins:lts-jdk21
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
COPY casc.yaml /var/jenkins_home/casc.yaml
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc.yaml \
    JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
```

```text
# plugins.txt
configuration-as-code
workflow-aggregator
git
github-branch-source
docker-workflow
ssh-agent
credentials-binding
matrix-auth
mcp-server
```

## CLI и REST API

API-токен: *профиль пользователя → Security → API Token → Add new token*. С токеном CSRF-crumb для запросов не нужен.

```bash
JENKINS=https://ci.example.org
AUTH=user:11a1b2c3...              # имя:API-токен

# запустить сборку (с параметрами)
curl -fsS -X POST -u "$AUTH" "$JENKINS/job/myapp/job/master/build"
curl -fsS -X POST -u "$AUTH" "$JENKINS/job/myapp/buildWithParameters?DEPLOY=true"

# статус последней сборки и лог
curl -fsS -u "$AUTH" "$JENKINS/job/myapp/lastBuild/api/json?tree=result,number,url"
curl -fsS -u "$AUTH" "$JENKINS/job/myapp/lastBuild/consoleText"

# CLI-клиент (jar скачивается с самого сервера)
curl -fsSO "$JENKINS/jnlpJars/jenkins-cli.jar"
java -jar jenkins-cli.jar -s "$JENKINS" -auth "$AUTH" -webSocket who-am-i
java -jar jenkins-cli.jar -s "$JENKINS" -auth "$AUTH" -webSocket list-plugins
java -jar jenkins-cli.jar -s "$JENKINS" -auth "$AUTH" -webSocket safe-restart
```

В пути задачи Multibranch каждая ветка — вложенная задача: `/job/<репо>/job/<ветка>/`.

## MCP для Claude Code

Официальный плагин **MCP Server** (`mcp-server`, версия 0.211, требует Jenkins 2.541.3+) превращает Jenkins в MCP-сервер. Отдельно ничего ставить не нужно — после установки плагина появляются адреса:

- `<jenkins>/mcp-server/mcp` — Streamable HTTP (рекомендуется);
- `<jenkins>/mcp-server/sse` — SSE;
- `<jenkins>/mcp-server/stateless`.

Инструменты:

- задачи — `getJob`, `getJobs`, `triggerBuild`, `getQueueItem`;
- сборки — `getBuild`, `getBuildLog`, `searchBuildLog`, `rebuildBuild`, `replayBuild`, `getTestResults` и др.;
- SCM — `getJobScm`, `getBuildChangeSets`, `findJobsWithScmUrl`;
- сервер — `whoAmI`, `getStatus`, `getSystemLog`.

Авторизация — Basic: `base64("пользователь:API-токен")`.

```bash
printf 'claude-bot:11a1b2c3...' | base64 -w0
```

```json
{
  "mcpServers": {
    "jenkins": {
      "type": "http",
      "url": "https://ci.example.org/mcp-server/mcp",
      "headers": {
        "Authorization": "Basic ${JENKINS_MCP_AUTH}"
      }
    }
  }
}
```

Это `.mcp.json` в проекте; `${JENKINS_MCP_AUTH}` Claude Code подставит из окружения, так что токен не попадёт в Git. То же одной командой:

```bash
claude mcp add --transport http jenkins https://ci.example.org/mcp-server/mcp \
  --header "Authorization: Basic $JENKINS_MCP_AUTH"
```

Права MCP = права пользователя. Заведите для Claude отдельного пользователя: *Overall/Read*, *Job/Read*, *Job/Build* на нужные папки — и он сможет читать логи упавших сборок и перезапускать их, но не менять настройки сервера. Если Jenkins доступен только на localhost VPS, а Claude Code работает там же, используйте `http://127.0.0.1:8080/mcp-server/mcp`.

## Безопасность и обслуживание

- **Обновления.** Бюллетени безопасности выходят ~раз в 2–4 недели, чаще всего — по плагинам. Подписка: [jenkins.io/security/advisories](https://www.jenkins.io/security/advisories/) (есть RSS). *Manage Jenkins* сам показывает предупреждения об уязвимых плагинах.
- **Меньше плагинов — меньше дыр.** Ставьте только нужные, неиспользуемые удаляйте.
- **Не выставляйте Jenkins в интернет без нужды.** Только localhost + SSH-туннель или VPN; если нужны вебхуки — nginx с HTTPS, регистрация выключена, анонимам — ничего.
- **`Jenkinsfile` = код на ваших агентах.** Кто может пушить в репозиторий, тот выполняет команды на агенте. Сборки PR из форков — только после одобрения (в Branch Source: «Trust» = только участники).
- **Секреты** — только в Credentials и через `withCredentials`, в лог они маскируются. Не делайте `echo $TOKEN` и не подставляйте секрет в Groovy-строку в двойных кавычках.
- **Script Console** (`/script`) — полный доступ к серверу, только для админов.
- **Бэкап** — `JENKINS_HOME` целиком (особенно `secrets/` и `credentials.xml` — без `secrets/master.key` пароли не расшифровать). Можно без `workspace/` и кеша. Пример: `tar --exclude=workspace -czf jenkins-$(date +%F).tgz -C /var/lib jenkins` (на Gentoo дома лежит в `/var/lib/jenkins/home`). Плагин ThinBackup делает это по расписанию.
- **Диск** — ограничивайте историю (`buildDiscarder`), чистите workspace (`cleanWs()`).

## Частые проблемы

| Симптом | Причина и решение |
| :--- | :--- |
| `failed to find a valid Java installation` / служба сразу падает | Нет Java 21/25 или выбрана 17. Debian: ставить `openjdk-21-jre` до Jenkins; Gentoo: `eselect java-vm set system openjdk-bin-21` |
| После обновления на 2.580.1 пропали функции | Плагины перестали быть встроенными — доставить из *Plugins → Available* |
| Агент не подключается после обновления ядра | Старый `agent.jar` (до августа 2024) — обновить образ агента / Remoting |
| Агенты по WebSocket отваливаются через nginx | Нет `Upgrade`/`Connection "upgrade"` и `proxy_http_version 1.1` |
| Ссылки в письмах и статусах ведут на `localhost` | Не задан *Jenkins URL* (*Manage Jenkins → System*) |
| На Arch Jenkins тормозит и падает с `OutOfMemoryError` | `-Xmx512m` по умолчанию — поднять в `/etc/conf.d/jenkins` |
| Arch: веб не открывается на 8080 | В пакете Arch порт 8090 |
| Вебхук не запускает сборку | Jenkins недоступен снаружи или неверный URL; смотреть *Recent Deliveries* на стороне хостинга, в крайнем случае `pollSCM` |

## Ссылки

- [jenkins.io](https://www.jenkins.io) · [документация](https://www.jenkins.io/doc/) · [синтаксис Pipeline](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Изменения weekly](https://www.jenkins.io/changelog/) · [изменения LTS](https://www.jenkins.io/changelog-stable/) · [поддержка Java](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
- [Установка на Linux](https://www.jenkins.io/doc/book/installing/linux/) · [в Docker](https://www.jenkins.io/doc/book/installing/docker/) · [inbound-agent](https://github.com/jenkinsci/docker-agents/blob/master/README_inbound-agent.md)
- [Бюллетени безопасности](https://www.jenkins.io/security/advisories/) · [плагины](https://plugins.jenkins.io) · [MCP Server](https://plugins.jenkins.io/mcp-server/) · [JCasC](https://plugins.jenkins.io/configuration-as-code/)
- Gentoo: [dev-util/jenkins-bin](https://packages.gentoo.org/packages/dev-util/jenkins-bin) · Arch: [jenkins](https://archlinux.org/packages/extra/any/jenkins/)

#Jenkins #CI_CD #DevOps #SelfHosted #Java #Docker #MCP #Claude_Code
