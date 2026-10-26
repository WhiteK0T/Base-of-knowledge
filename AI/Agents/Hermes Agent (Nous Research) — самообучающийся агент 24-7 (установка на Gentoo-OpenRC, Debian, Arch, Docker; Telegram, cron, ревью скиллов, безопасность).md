---
создал заметку: 2026-10-27T04:20:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Hermes
  - NousResearch
  - Harness
  - Telegram
  - Безопасность
  - Gentoo
  - OpenRC
  - Docker
Источник:
  - https://github.com/NousResearch/hermes-agent
  - https://hermes-agent.nousresearch.com/docs/getting-started/installation
  - https://hermes-agent.nousresearch.com/docs/getting-started/platform-support
  - https://hermes-agent.nousresearch.com/docs/user-guide/security
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
  - https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
  - https://hermes-agent.nousresearch.com/docs/integrations/providers
  - https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup
---

# ☤ Hermes Agent (Nous Research) — самообучающийся агент 24/7

**Hermes Agent** ([NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent), MIT, ~257 тыс. звёзд) — опенсорсный агент, который живёт постоянно: сидит в Telegram и других мессенджерах, выполняет задачи по расписанию, копит память и **сам пишет себе скиллы**. В терминах заметки [«ИИ-агент vs харнесс»](../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md) это **Agentic OS**: харнесс с инструментами и субагентами, поверх которого добавлен слой «операционной системы».

Сведения сверены с документацией, которая лежит в самом репозитории (коммит `c714c42` от 26.10.2026). Hermes на живой системе я не ставил: установщик меняет домашний каталог и тянет свои Python, Node и Chromium. Init-скрипт OpenRC ниже проверен только на синтаксис (`sh -n`, shellcheck).

Каталоги экосистемы — в заметках [awesome-hermes-agent](../Skills/awesome-hermes-agent%20%280xNyk%29%20%E2%80%94%20%D0%BD%D0%B5%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D1%8B%D0%B9%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20Hermes%20Agent%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%2C%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%2C%20%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C%29%2C%20%D1%81%20%D0%BC%D0%B5%D1%82%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B7%D1%80%D0%B5%D0%BB%D0%BE%D1%81%D1%82%D0%B8.md) и [Skills Hub](../Skills/Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md).

## 🧭 Что умеет

| Возможность | Как устроено |
| :--- | :--- |
| Интерфейсы | терминал (`hermes`, TUI), десктоп-приложение, **шлюз** в Telegram, Discord, Slack, WhatsApp, Signal, Matrix, почту и ещё два десятка платформ |
| Модели | 40+ провайдеров: Anthropic, OpenAI и подписка ChatGPT (Codex), OpenRouter, Nous Portal, локальные Ollama и llama.cpp через custom endpoint |
| Расписание | встроенный cron: `/cron add "every 2h" "…"` или обычной фразой «каждое утро в 9…». Задачи выполняет **шлюз**, он тикает раз в 60 секунд |
| Память | долговременная память, полнотекстовый поиск по прошлым сессиям, модель пользователя (Honcho) |
| Самообучение | после нетривиальной задачи агент сохраняет скилл (`skill_manage`), а **куратор** чистит устаревшие |
| Где выполняются команды | `local`, `ssh`, `docker`, `modal`, `daytona`, `vercel_sandbox` (плюс Singularity плагином) |
| Расширения | MCP-серверы, плагины, субагенты, импорт настроек из OpenClaw, Claude Code, Codex, Cursor |

## 🖥️ Где работает — и что это значит для наших систем

Официальная матрица поддержки:

- **Tier 1:** Linux и WSL2 на x86_64/aarch64 через `install.sh`, Docker-образ, macOS на Apple Silicon, Windows 10/11. Про Linux сказано: «тестируем на свежей Ubuntu; дистрибутив с glibc, systemd и FHS скорее всего подойдёт».
- **Tier 2** (по мере сил): Nix, Android/Termux на aarch64.
- **Не поддерживаются:** установка из **AUR**, через `pip`/`uv tool install`, через `brew`, Termux не на aarch64.

Рантайм — **только Python 3.14**: установщик сам ставит закреплённые версии Python, Node.js, ripgrep и FFmpeg через свой пакетный менеджер PM. От системы нужны лишь git, curl, tar и утилиты SHA-256.

| Система | Как ставить | Нюансы |
| :--- | :--- | :--- |
| **Gentoo** (OpenRC) | `install.sh` от обычного пользователя | glibc есть, а systemd нет: `hermes gateway install` не поможет, нужна служба OpenRC (ниже). `libatomic.so.1` для их Node.js поставляет `sys-devel/gcc` |
| **Debian / Ubuntu** | `install.sh` | Tier 1, «родная» среда. На минимальных образах установщик сам ставит `libatomic1` через sudo |
| **Arch** | `install.sh`, **не AUR** | AUR официально не поддерживается; `gcc-libs` (libatomic) обычно уже стоит |
| **Docker** (любая система) | `nousresearch/hermes-agent` | Tier 1; обновление — новым образом, `hermes update` в контейнере не работает |
| **Entware** (RT-AX56U) | ❌ | 32-битный armv7 не поддерживается, а Python 3.14 + Node + браузер не влезут в 512 МБ ОЗУ. Hermes ставится на ПК или VPS, роутеру остаётся роль сети |

## 📥 Установка

<details><summary>Linux: install.sh (Gentoo, Debian/Ubuntu, Arch)</summary>

Скрипт из интернета лучше скачать и прочитать, а не сразу отдавать в `bash`:

```sh
curl -fsSL https://hermes-agent.nousresearch.com/install.sh -o install.sh
less install.sh
bash install.sh --skip-browser      # без Chromium: на сервере он обычно не нужен
source ~/.bashrc
hermes doctor
```

Что делает установщик: клонирует исходники в `~/.hermes/hermes-agent/`, кладёт обёртку `~/.local/bin/hermes`, данные хранит в `~/.hermes/`. По умолчанию он также ставит Chromium (Chrome for Testing) и драйвер computer-use. Отключаются они флагами `--skip-browser` и `--skip-computer-use`, и Hermes запоминает этот выбор при обновлениях. `--non-interactive` пропускает шаги, требующие ввода.

Зависимости, если их нет:

| Gentoo | Debian / Ubuntu | Arch |
| :--- | :--- | :--- |
| `emerge --ask dev-vcs/git net-misc/curl` (tar и coreutils в @system) | `apt install git curl tar coreutils` | `pacman -S git curl tar coreutils` |

Ставить **от отдельного пользователя**, не от root. В чеклисте самой документации: «никогда не запускайте шлюз от root».

</details>

<details><summary>Docker</summary>

```sh
mkdir -p ~/.hermes
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup    # мастер настройки один раз
docker run -d --name hermes --restart unless-stopped \
  -v ~/.hermes:/opt/data -p 8642:8642 nousresearch/hermes-agent gateway run
```

Порт 8642 нужен только для дашборда и OpenAI-совместимого API шлюза. Для одного Telegram его можно не публиковать. Внутри образа шлюзом управляет s6-overlay и перезапускает его при падении.

</details>

## 🔌 Подключение модели

Мастер — `hermes setup` (всё сразу) или `hermes model` (только модель). Ключи лежат в `~/.hermes/.env`, настройки — в `~/.hermes/config.yaml`; отдельные значения можно менять через `hermes config set КЛЮЧ ЗНАЧЕНИЕ`.

| Провайдер | Как подключить | Оплата |
| :--- | :--- | :--- |
| **Ollama / llama.cpp** | custom endpoint `http://localhost:11434/v1` (пример ниже) | бесплатно, своё железо |
| **Claude** | `ANTHROPIC_API_KEY` в `.env` и `provider: anthropic` | за токены по API |
| **Claude по подписке** | `hermes model` → Anthropic OAuth | **только Max с докупленным extra usage**; на Pro не работает, базовый лимит Max не тратится |
| **ChatGPT / Codex** | `hermes model` → ChatGPT or Codex Subscription (device code) | по подписке; как расходуются лимиты Codex, документация не говорит |
| **OpenRouter** | `OPENROUTER_API_KEY` | за токены |
| **Nous Portal** | `hermes setup --portal` | подписка Nous: 300+ моделей и инструменты (поиск, картинки, TTS) |

Почему подписка Claude работает лишь так, разобрано в [основной заметке](../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md) (вопрос 5). Ещё Hermes умеет подхватывать логин Claude Code с этой машины. Если это не нужно, задайте `auth.adopt_external_logins: false`.

<details><summary>Локальная модель через Ollama</summary>

Hermes нужно **не меньше 64 000 токенов контекста**, а у Ollama окно по умолчанию гораздо меньше. Делаем вариант модели с большим окном (документация советует `gemma4:31b` как лучшую локальную модель с вызовом инструментов; ей нужно 24+ ГБ памяти):

```sh
ollama pull gemma4:31b
cat > Modelfile <<'EOF'
FROM gemma4:31b
PARAMETER num_ctx 64000
EOF
ollama create gemma4-64k -f Modelfile
```

`~/.hermes/config.yaml`:

```yaml
model:
  default: "gemma4-64k"
  provider: "custom"
  base_url: "http://localhost:11434/v1"
```

Для медленного CPU-инференса — `HERMES_API_TIMEOUT=1800` в `~/.hermes/.env`. Модель без поддержки tools сможет только болтать: агентом она не станет. Подробнее про сам сервер — в заметке [Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md).

</details>

## 💬 Telegram-бот

1. В [@BotFather](https://t.me/BotFather): `/newbot`, имя, username на `bot` → токен.
2. Свой **числовой** id — у [@userinfobot](https://t.me/userinfobot).
3. `hermes gateway setup` (мастер) или вручную в `~/.hermes/.env`:

```sh
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_ALLOWED_USERS=123456789
```

4. Запуск: `hermes gateway` (на переднем плане). Как сделать из этого службу — ниже.

Доступ по умолчанию **закрыт**: без списков разрешённых пользователей шлюз отказывает всем и пишет об этом в лог. Есть и коды сопряжения: незнакомому пользователю бот выдаёт код, а владелец подтверждает его командой `hermes pairing approve telegram <код>`. `GATEWAY_ALLOW_ALL_USERS=true` открывает бота всем; документация прямо запрещает так делать в продакшене. Для групп нужно отключить privacy mode бота в BotFather (Bot Settings → Group Privacy) или сделать бота админом.

## ⚙️ Шлюз как служба

Шлюз нужен не только мессенджерам: **задачи cron выполняются только при запущенном шлюзе**. Если он не работает, задачи пропускаются с записью в лог.

<details><summary>systemd (Debian/Ubuntu, Arch)</summary>

```sh
hermes gateway install                 # пользовательская служба
sudo loginctl enable-linger "$USER"    # стартовать при загрузке без входа в систему
hermes gateway status
```

Для VPS документация советует именно пользовательскую службу с linger: тогда `hermes update` перезапускает шлюз без sudo. Есть и системная служба, `sudo hermes gateway install --system`. После обновления используйте `hermes gateway restart`, а не голый `systemctl restart`: так шлюз сначала доделает начатые ответы.

</details>

<details><summary>OpenRC (Gentoo) — свой init-скрипт</summary>

`/etc/init.d/hermes-gateway` (сделать исполняемым — `chmod +x`):

```sh
#!/sbin/openrc-run
# Шлюз Hermes Agent (мессенджеры + планировщик cron) под OpenRC.
# Штатный «hermes gateway install» создаёт только службы systemd/launchd.
# Настройки — /etc/conf.d/hermes-gateway.

description="Hermes Agent messaging gateway"
supervisor=supervise-daemon
: "${HERMES_USER:=hermes}"
user_home=$(getent passwd "${HERMES_USER}" | cut -d: -f6)
command="${user_home}/.local/bin/hermes"
command_args="gateway run"
command_user="${HERMES_USER}"
directory="${user_home}"
output_log="/var/log/hermes-gateway.log"
error_log="/var/log/hermes-gateway.log"
respawn_delay=15
respawn_max=0

depend() {
	need net
	after dns
}

start_pre() {
	if [ ! -x "${command}" ]; then
		eerror "Нет ${command}: установите Hermes install.sh от пользователя ${HERMES_USER}"
		return 1
	fi
	checkpath -f -o "${HERMES_USER}" -m 0640 /var/log/hermes-gateway.log
	# HOME supervise-daemon выставит сам по command_user; HERMES_HOME — только если задан
	if [ -n "${HERMES_HOME}" ]; then
		supervise_daemon_args="--env HERMES_HOME=${HERMES_HOME}"
	fi
}
```

`/etc/conf.d/hermes-gateway`:

```sh
# Настройки шлюза Hermes Agent (/etc/init.d/hermes-gateway)

# пользователь, от которого запускался install.sh (не root!)
HERMES_USER="hermes"

# каталог данных, если не стандартный ~/.hermes этого пользователя
#HERMES_HOME="/home/hermes/.hermes"
```

```sh
rc-update add hermes-gateway default
rc-service hermes-gateway start
tail -f /var/log/hermes-gateway.log
```

Проверено только на синтаксис (`sh -n`, shellcheck). Стиль тот же, что у службы `jenkins-agent` на нашем VPS: supervise-daemon сам перезапускает процесс при падении, а `$HOME` по `command_user` выставляет тоже сам. После `hermes update` перезапускайте службу через `rc-service hermes-gateway restart`.

</details>

## ⏰ Задачи по расписанию

```text
/cron add "every 2h" "Проверь, отвечают ли сайты из списка, и напиши, если что-то лежит"
/cron add "in 30m" "Напомни проверить сборку"
```

То же из терминала — `hermes cron create "every 2h" "…"`, состояние — `hermes cron status`. Можно и обычной фразой: «Каждое утро в 9 собирай новости по ИИ и присылай в Telegram». Задача может подключать скиллы (`--skill`) и выполняться на своей модели (`cron.model` или отдельно для задачи).

Ограничения по безопасности: задача cron не может создавать новые задачи, а опасную команду в ней по умолчанию **блокирует** `approvals.cron_mode: deny`. Подтвердить её некому.

## 🧠 Самообучение под контролем

Как это работает и почему без контроля опасно, разобрано в [основной заметке](../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md) (вопрос 2). Коротко: скилл агент пишет сам, решив, что задача удалась, а **подтверждение записи по умолчанию выключено**. Рычаги:

| Что | Как |
| :--- | :--- |
| Ревью каждой записи скилла | `skills.write_approval: true` (или `/skills approval on` на ходу). Записи ждут в `~/.hermes/pending/skills/`, разбираются командами `/skills pending`, `/skills diff <id>`, `/skills approve <id>` и `/skills reject <id>` |
| Чистка | **куратор** раз в 7 дней (если агент простаивает больше 2 часов): скилл без использования 14 дней становится `stale`, через 30 дней уходит в `~/.hermes/skills/.archive/`. Слияние похожих скиллов моделью выключено по умолчанию (`curator.consolidate`). Посмотреть план без изменений — `hermes curator run --dry-run` |
| Защита ценного | закреплённые (pinned) скиллы не трогают ни куратор, ни сам агент; скиллы, на которые ссылается задача cron, куратор не архивирует |
| Откат | держать `~/.hermes/skills/` в git и смотреть diff, как код |

## 🛡️ Безопасность

У Hermes несколько уровней защиты, и все они настраиваются:

- **Опасные команды.** `approvals.mode`: `smart` (по умолчанию — риск оценивает вспомогательная модель), `manual` (всегда спрашивать) или `off` (= `--yolo`, без вопросов). Ниже всех режимов лежит неотключаемый **hardline-блоклист**. Свои запреты задаются в `approvals.deny` glob-шаблонами; они действуют даже в YOLO и в контейнере.
- **Запись файлов.** В системные файлы и хранилища учётных данных (ключи в `~/.ssh`, секреты самого Hermes вроде `~/.hermes/.env`) агент не пишет никогда. `HERMES_WRITE_SAFE_ROOT` ограничивает запись одним каталогом.
- **Изоляция команд.** Бэкенд `terminal.backend: docker` запускает каждую команду в контейнере: `--cap-drop ALL`, `no-new-privileges`, лимит процессов, `/tmp` ограниченного размера. Проверку опасных команд Hermes при этом **пропускает**: границей считается контейнер. Переменные окружения пробрасываются в контейнер только по явному списку `docker_forward_env`.
- **Отдельная машина.** `terminal.backend: ssh`: шлюз с токенами мессенджеров остаётся на одной машине, а команды выполняются на другой.
- **Инъекции через файлы проекта** (`AGENTS.md`, `.cursorrules`): Hermes сканирует их на prompt injection.

<details><summary>Пример «осторожного» config.yaml для шлюза на VPS</summary>

```yaml
model:
  provider: "anthropic"            # ключ ANTHROPIC_API_KEY — в ~/.hermes/.env (chmod 600)
  default: "claude-sonnet-5-5"

terminal:
  backend: docker                  # команды агента — в контейнере
  docker_forward_env: []           # никаких секретов внутрь контейнера
  container_cpu: 1
  container_memory: 2048
  container_persistent: true

approvals:
  mode: manual                     # спрашивать про каждую опасную команду
  cron_mode: deny
  deny:
    - "git push --force*"
    - "*curl*|*sh*"

skills:
  write_approval: true             # скиллы — только после ревью

auth:
  adopt_external_logins: false     # не подхватывать логин Claude Code / Codex CLI

curator:
  consolidate: false
```

Ключи взяты из документации: `model.*`, `terminal.*` и `approvals.*` — из страницы Security, `skills.write_approval` — из Configuration, `auth.adopt_external_logins` — из Providers. Модель указана для примера; подойдёт любая.

</details>

Остальное из чеклиста документации: явные списки пользователей вместо allow-all, `chmod 600 ~/.hermes/.env`, `terminal.cwd` не на чувствительном каталоге, логи в `~/.hermes/logs/`, регулярный `hermes update`.

## 🔄 Обновление и удаление

```sh
hermes update                          # канал stable: только релизы
hermes update --set-channel main       # следовать за каждым коммитом main (и обратно — stable)
hermes uninstall --dry-run             # сначала посмотреть, что удалится
hermes uninstall                       # код; настройки и данные по умолчанию остаются
hermes uninstall --full                # вместе с данными
```

## 💡 Итог

- Hermes — харнесс с «надстройкой ОС»: мессенджеры, cron, память, самописные скиллы, изоляция в Docker или по SSH. Для ассистента 24/7 это одно из самых полных опенсорсных решений.
- На **Gentoo** ставится обычным `install.sh`, но службу шлюза для OpenRC придётся написать самому (пример выше). **Debian/Ubuntu** — родная среда, на **Arch** — тот же `install.sh` (не AUR), на **роутере** Hermes не работает.
- Перед тем как пускать в мессенджер: список разрешённых пользователей, `terminal.backend: docker`, `approvals.mode: manual` и `skills.write_approval: true`.
- С Claude — через API-ключ. По подписке работает только Max с докупленным extra usage.

## 🔗 Ссылки

- Проект: [GitHub](https://github.com/NousResearch/hermes-agent) · [документация](https://hermes-agent.nousresearch.com/docs/) · [установка](https://hermes-agent.nousresearch.com/docs/getting-started/installation) · [платформы](https://hermes-agent.nousresearch.com/docs/getting-started/platform-support)
- Разделы: [безопасность](https://hermes-agent.nousresearch.com/docs/user-guide/security) · [скиллы](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) · [куратор](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator) · [cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) · [Telegram](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram) · [провайдеры](https://hermes-agent.nousresearch.com/docs/integrations/providers) · [Ollama](https://hermes-agent.nousresearch.com/docs/guides/local-ollama-setup)
- В хранилище: [ИИ-агент vs харнесс](../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md) · [awesome-hermes-agent](../Skills/awesome-hermes-agent%20%280xNyk%29%20%E2%80%94%20%D0%BD%D0%B5%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D1%8B%D0%B9%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20Hermes%20Agent%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%2C%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%2C%20%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C%29%2C%20%D1%81%20%D0%BC%D0%B5%D1%82%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B7%D1%80%D0%B5%D0%BB%D0%BE%D1%81%D1%82%D0%B8.md) · [awesome-hermes-skills](../Skills/awesome-hermes-skills%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20Hermes%20Agent%20%28Nous%20Research%29%2C%20%D0%BA%D1%80%D0%BE%D1%81%D1%81-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%20%D1%81%20Claude%20Code-Cursor-Windsurf.md) · [Skills Hub](../Skills/Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md) · [Moltworker (OpenClaw)](Tooling/Moltworker%20%28Cloudflare%29%20%E2%80%94%20%D0%B4%D0%B5%D0%BF%D0%BB%D0%BE%D0%B9%20%D0%98%D0%98-%D0%B0%D1%81%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BD%D1%82%D0%B0%20OpenClaw%20%28ex-Moltbot%29%20%D0%BD%D0%B0%20Cloudflare%20Workers%2C%20%D1%84%D0%B0%D0%BA%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%AB%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%20%D0%B8%20%D1%81%D1%82%D0%B0%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D0%BE%C2%BB.md) · [Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) · [Сводная таблица AI-агентов](%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%29.md)

#AI #Агенты #Hermes #NousResearch #Harness #Telegram #Безопасность #Gentoo #OpenRC #Docker
