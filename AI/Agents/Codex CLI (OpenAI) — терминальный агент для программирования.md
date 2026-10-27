---
создал заметку: 2026-10-27T20:30:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Codex
  - OpenAI
  - CLI
Источник:
  - https://github.com/openai/codex
  - https://learn.chatgpt.com/docs/codex/cli
  - https://learn.chatgpt.com/docs/developer-commands?surface=cli
  - https://learn.chatgpt.com/docs/agent-approvals-security
  - https://learn.chatgpt.com/docs/config-file/config-reference
  - https://learn.chatgpt.com/docs/non-interactive-mode
  - https://learn.chatgpt.com/docs/pricing
---

# 🤖 Codex CLI (OpenAI) — терминальный агент для программирования

**Codex CLI** — открытый агент для программирования от OpenAI, который работает в терминале на вашей машине. Он читает репозиторий, правит файлы, запускает команды и тесты и ведёт задачу по шагам. Команды выполняются в песочнице ОС, а одобрения настраиваются отдельно.

CLI написан на Rust и распространяется под Apache-2.0. Работает с моделями GPT-6, а войти можно через подписку ChatGPT или по API-ключу.

Сверено 27.10.2026 по репозиторию [openai/codex](https://github.com/openai/codex) (релиз `rust-v0.164.0` от 23.10.2026) и документации на learn.chatgpt.com. Старые ссылки `developers.openai.com/codex/...` ведут туда же. Флаги и клавиши сверены по исходникам `codex-rs`.

> [!info] Коротко
> | | |
> | :--- | :--- |
> | Репозиторий | [openai/codex](https://github.com/openai/codex) — ★131k, **Apache-2.0**, Rust (`codex-rs`) |
> | Версия | **0.164.0** (23.10.2026); в npm уже есть альфы 0.166 |
> | Платформы | macOS 12+, Linux x86_64/arm64, Windows (нативно в PowerShell или через WSL2) |
> | Требования | ОЗУ от 4 ГБ (рекомендуется 8), Git 2.23+ по желанию; на Linux — `bubblewrap` для песочницы |
> | Вход | аккаунт ChatGPT (Plus, Pro, Business, Edu, Enterprise; Free и Go — ограниченно) или API-ключ |
> | Модели | GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna; локальные — через Ollama и LM Studio |
> | Конфиг | `~/.codex/config.toml`, инструкции — `AGENTS.md` |

## 🧭 Где CLI в семействе Codex

Под именем Codex у OpenAI несколько продуктов, и у них общие вход, конфиг и история:

| Продукт | Что это | Как открыть из CLI |
| :--- | :--- | :--- |
| **Codex CLI** | агент в терминале (эта заметка) | `codex` |
| **IDE-расширение** | то же в VS Code, Cursor, Windsurf; делит с CLI `~/.codex` | `/ide` подтягивает открытые файлы и выделение |
| **Десктоп-приложение ChatGPT** | Codex и ChatGPT Work в одном окне (macOS, Windows) | `codex app`, в сессии — `/app` |
| **Codex Cloud** | задачи в облачных контейнерах OpenAI, ревью PR на GitHub | `codex cloud`, `codex apply` |

## 💻 Установка

Официальный путь — установщик или npm-пакет. В дистрибутивах есть и нативные пакеты:

| Система | Как поставить |
| :--- | :--- |
| **Gentoo** (основная) | В основном дереве нет, есть в оверлее `gentoo-zh`: `dev-util/codex-bin` (готовый бинарник) или `dev-util/codex` (сборка из исходников), оба `~amd64 ~arm64`, тянут `sys-apps/bubblewrap`. Либо npm: `emerge --ask net-libs/nodejs`, затем `npm i -g @openai/codex` |
| **Debian / Ubuntu** | `sudo apt install bubblewrap`, затем официальный установщик `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` или `npm i -g @openai/codex` (Node 16+) |
| **Arch** | `sudo pacman -S openai-codex bubblewrap` — пакет в `extra`, версия 0.164.0; в AUR есть ещё `openai-codex-bin` |
| **Entware / RT-AX56U** | ❌ сборок под armv7 нет (только x86_64 и aarch64), а минимум ОЗУ — 4 ГБ. Запускать на ПК или VPS |

<details><summary>Gentoo: оверлей gentoo-zh и ключевые слова</summary>

```bash
# один раз: подключить оверлей (eselect-repository)
eselect repository enable gentoo-zh
emaint sync -r gentoo-zh

echo "dev-util/codex-bin ~amd64" >> /etc/portage/package.accept_keywords/codex
emerge --ask dev-util/codex-bin

codex --version
```

</details>

Обновление:
- установщиком — запустить ту же команду ещё раз;
- через npm — `npm i -g @openai/codex`;
- самообновление — `codex update`, если установка его поддерживает;
- в дистрибутиве — пакетным менеджером.

Шелл-автодополнение: `eval "$(codex completion bash)"` (есть `zsh`, `fish`, `powershell`).

**Песочница на Linux.** Codex берёт первый `bwrap` из `PATH`. Если его нет, используется встроенный помощник, которому нужны непривилегированные user namespaces, а при старте выводится предупреждение. На Ubuntu 24.04 может понадобиться AppArmor-профиль `bwrap-userns-restrict` из пакета `apparmor-profiles`; на 25.04 он уже в комплекте. В Docker-контейнере песочница может не работать, если хост запрещает namespaces или seccomp.

## 🔑 Вход и тарифы

| Способ | Команда | Когда |
| :--- | :--- | :--- |
| Через ChatGPT | `codex login` — открывает браузер | обычный случай: расход идёт из лимитов подписки |
| Device code | `codex login --device-auth` | сервер без браузера (бета; включается в настройках безопасности ChatGPT) |
| Проброс порта | `ssh -L 1455:localhost:1455 user@host`, затем `codex login` на сервере | если device code недоступен |
| API-ключ | `printenv OPENAI_API_KEY \| codex login --with-api-key` | CI и скрипты; оплата по тарифам API |
| Проверка | `codex login status` (код `0` — вход есть), `codex logout` | |

Учётные данные хранятся в `~/.codex/auth.json` или в системном хранилище ключей. Управляет этим ключ `cli_auth_credentials_store`: `file`, `keyring`, `auto` или `ephemeral`. **`auth.json` — это пароль**: его нельзя коммитить и пересылать.

**Что даёт подписка ChatGPT** (OpenAI публикует оценки лимитов, а не жёсткие квоты):

| План | Цена | Codex |
| :--- | :--- | :--- |
| Free / Go | $0 / $8 | лёгкие задачи на GPT-6 Luna, в десктоп-приложении, раскатывается постепенно |
| Plus | $20 | веб, CLI, IDE, iOS; за 5 часов примерно 15–160 сообщений GPT-6.1 Sol, 35–285 Terra, 5–45 Astra, 350–3000 Luna |
| Pro | $100 / $200 / $500 | всё из Plus с бо́льшими лимитами, сейчас без пятичасового окна; Ultrafast — на плане за $500 |
| Business | $20 за место (годовая оплата) или $25 помесячно | лимиты как у Plus на место, можно докупать кредиты |
| Enterprise / Edu | по договору | гибкие кредиты, политики администратора |

Режим **Fast** расходует лимит в 2,5 раза быстрее, **Ultrafast** — в 8 раз.

С API-ключом действует обычный прайс API. Облачные функции при этом недоступны: Codex Cloud, ревью PR на GitHub, интеграция со Slack.

## 🧠 Модели и reasoning

| Модель | Для чего |
| :--- | :--- |
| `gpt-6-astra` | самая сильная: сложная работа с кодом, приложениями и исследованиями |
| `gpt-6.1-sol` | почти уровень Astra дешевле; основная на платных планах, хороша для долгих задач |
| `gpt-6.1-terra` | быстрая и экономная: тексты, картинки, computer use (нужен CLI 0.159+) |
| `gpt-6-luna` | узкие повторяющиеся задачи, большие объёмы |

Как управлять моделью:
- **выбор:** `codex -m gpt-6.1-sol`, в сессии — `/model`, в конфиге — `model = "..."`. Список, который видит ваш аккаунт, — `codex debug models`;
- **reasoning:** `model_reasoning_effort` — `low`, `medium`, `high`, `xhigh`, `max`, `ultra` (набор зависит от модели). В TUI уровень меняют `Shift+↑`/`Shift+↓` или `Alt+.`/`Alt+,`;
- **отдельно для планирования:** `plan_mode_reasoning_effort` действует только в plan-режиме;
- **Ultra** — не просто уровень: Codex раскладывает задачу на субагентов;
- **Fast:** `/fast` переключает быстрый тариф модели, если модель его предлагает.

Локальные модели подключаются флагом `--oss` (`--local-provider ollama|lmstudio`). Свой провайдер описывается в `[model_providers.<id>]`. Ограничение: Codex говорит только по протоколу **Responses API** (`wire_api = "responses"` — единственное значение), так что шлюз с одним Chat Completions напрямую не подойдёт.

> [!warning] Мониторинг безопасности у GPT-6 Astra
> Codex асинхронно следит за поведением модели и может остановить задачу, если заметит небезопасные действия. В CLI такая задача завершается, продолжить её нельзя. Мониторинг не заменяет песочницу и проверку результата.

## 🛡️ Песочница и одобрения

Безопасность держится на двух независимых настройках.

**Песочница** (`--sandbox`, `-s`, `sandbox_mode`) — что команды могут технически:

| Режим | Что можно |
| :--- | :--- |
| `read-only` | только чтение |
| `workspace-write` | запись в рабочий каталог и временные каталоги; **сеть выключена** |
| `danger-full-access` | всё, без песочницы |

**Одобрения** (`--ask-for-approval`, `-a`, `approval_policy`) — когда Codex спрашивает:
- `on-request` — модель сама решает, когда спросить: выход за песочницу, сеть, запись вне рабочего каталога;
- `never` — не спрашивать; ошибки сразу возвращаются модели;
- `{ granular = { ... } }` — выборочно по категориям запросов.

Режим `untrusted` убран — с ним Codex может не запуститься. Флага `--full-auto` тоже больше нет.

**Готовые сочетания** — переключаются командой `/permissions`:

| Пресет | Флаги | Что получается |
| :--- | :--- | :--- |
| **Auto** (по умолчанию в git-репозитории) | `--sandbox workspace-write -a on-request` | читает, правит и запускает в рабочем каталоге; за его пределами и для сети — спрашивает |
| **Read Only** (по умолчанию вне git) | `--sandbox read-only -a on-request` | только смотреть и планировать |
| **Approve for me** | `--approve-for-me` | как Auto, но запросы сначала оценивает агент-ревьюер (`approvals_reviewer = "auto_review"`): опасное отклоняет, отказ можно перезапустить через `/approve` |
| **CI, только чтение** | `--sandbox read-only -a never` | ничего не спрашивает и ничего не меняет |
| **Полный доступ** | `--dangerously-bypass-approvals-and-sandbox` (`--yolo`) | ни песочницы, ни вопросов — только в одноразовой ВМ или контейнере |

Ещё несколько правил песочницы:
- **Защищённые пути.** Даже в `workspace-write` каталоги `.git`, `.agents`, `.codex` и `.aws` внутри рабочего каталога доступны только на чтение.
- **Дополнительные каталоги** — `--add-dir DIR`. Это безопаснее, чем сразу открывать `danger-full-access`.
- **Сеть** в `workspace-write` включается так: `[sandbox_workspace_write] network_access = true`. Ограничить направления можно экспериментальной функцией `network_proxy` со списком доменов (allowlist).
- **Реализация по ОС:** Seatbelt на macOS, `bwrap` + seccomp на Linux, MXC или restricted token на Windows. Проверить, как команда поведёт себя в песочнице, — `codex sandbox linux <команда>`.
- **Правила** (`~/.codex/rules/*.rules`, экспериментально) решают, какие команды можно запускать вне песочницы. Например, `prefix_rule(pattern=["gh","pr","view"], decision="prompt")`. Когда вы разрешаете команду в TUI, правило дописывается в `~/.codex/rules/default.rules`. Проверить правило заранее — `codex execpolicy check`.

## 📝 AGENTS.md, конфиг и память

**`AGENTS.md`** — инструкции проекта, аналог `CLAUDE.md`. Codex собирает их при старте:
1. глобальный `~/.codex/AGENTS.override.md` или `AGENTS.md` — берётся первый непустой;
2. затем по пути от корня репозитория до текущего каталога: в каждом каталоге `AGENTS.override.md` или `AGENTS.md`;
3. файлы склеиваются сверху вниз, ближние к рабочему каталогу идут последними и потому важнее.

Лимит на всё — `project_doc_max_bytes` (32 КиБ по умолчанию). `/init` создаёт заготовку. Если в проекте уже есть `CLAUDE.md`, можно не дублировать его: `project_doc_fallback_filenames = ["CLAUDE.md"]` — Codex прочитает его там, где нет `AGENTS.md`.

**Конфиг** (`config.toml`), по убыванию приоритета:
1. флаги и `-c ключ=значение`;
2. `.codex/config.toml` проекта — только для доверенных проектов;
3. профиль `--profile name` — файл `~/.codex/name.config.toml`;
4. `~/.codex/config.toml`;
5. облачные настройки рабочего пространства;
6. `/etc/codex/config.toml`;
7. встроенные значения.

Флаг `--strict-config` падает на неизвестных ключах. `/debug-config` показывает, какой слой что задал.

<details><summary>Пример ~/.codex/config.toml</summary>

```toml
model = "gpt-6.1-sol"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"                         # cached | indexed | live | disabled
project_doc_fallback_filenames = ["CLAUDE.md"]

[sandbox_workspace_write]
network_access = false

[tui]
vim_mode_default = false
status_line = ["model-with-reasoning", "context-remaining", "git-branch"]

[mcp_servers.docs]                            # то же делает: codex mcp add docs -- npx -y …
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/home/me/docs"]

[features]
memories = true                               # экспериментально, по умолчанию выключено
```

</details>

Состав `status_line` удобнее собрать через `/statusline`: команда сама запишет его в конфиг.

**Веб-поиск** по умолчанию включён в режиме `cached` — ответы берутся из индекса OpenAI, а не из живой сети. `--search` или `web_search = "live"` дают свежие страницы. Помните, что веб — путь для prompt injection.

**Память** (`features.memories`, экспериментально) — локальное хранилище фактов из прошлых сессий; управляется командой `/memories`. Обязательные правила всё равно держите в `AGENTS.md`.

## 🧩 Skills, плагины, MCP, хуки, субагенты

- **Skills** — каталог со `SKILL.md` (`name` и `description` обязательны). Где Codex их ищет:
  - `.agents/skills` — от текущего каталога вверх до корня репозитория;
  - `~/.agents/skills` — личные;
  - `/etc/codex/skills` — общие для машины.

  Вызов — `$имя-скилла` в промпте или `/skills`. Встроенные помощники — `$skill-creator` и `$skill-installer`. Custom prompts устарели, их заменили скиллы.
- **Плагины** — пакеты скиллов, приложений и MCP из маркетплейсов: `codex plugin add <плагин>@<маркетплейс>`, `codex plugin list`, в сессии — `/plugins`.
- **MCP:**
  - локальный stdio-сервер — `codex mcp add <имя> -- <команда> [аргументы]`;
  - HTTP-сервер — `codex mcp add <имя> --url <URL>` (`--bearer-token-env-var`, `codex mcp login` для OAuth);
  - в сессии — `/mcp` (с `verbose` — подробности).

  Сам Codex MCP-сервером больше не бывает: `codex mcp-server` удалён, вместо него — `codex app-server`.
- **Хуки** — `~/.codex/hooks.json` или `.codex/hooks.json`, либо `[hooks]` в конфиге. События:
  - `SessionStart`, `SubagentStart`;
  - `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`;
  - `PreCompact`, `PostCompact`, `SubagentStop`, `Stop`.

  Новый или изменённый хук не запустится, пока вы не доверите ему в `/hooks`: доверие привязано к хешу определения.
- **Субагенты.** Встроенные — `default`, `worker` (реализация) и `explorer` (чтение кода). Свои описываются TOML-файлами в `~/.codex/agents/` или `.codex/agents/` с полями `name`, `description` и `developer_instructions`. Codex запускает субагентов по прямой просьбе или по инструкции в проекте или скилле; `/subagents` переключает между их потоками.

## 🔁 Сессии и параллельная работа

Сессии сохраняются, к ним можно вернуться:
- `codex resume` — выбор из списка; `--last` — последняя в этом каталоге; `--all` — по всем каталогам;
- `codex fork` — копия сессии;
- `codex archive` / `unarchive` / `delete` — скрыть, вернуть или удалить сессию.

Внутри сессии:
- `/fork` — копия текущего диалога;
- `/side` (`/btw`) — эфемерная побочная беседа;
- `Esc Esc` на пустой строке — отредактировать прошлое сообщение и ответвиться от него.

Пока Codex работает:
- `Enter` добавляет указание в текущий ход;
- `Tab` ставит сообщение или команду в очередь на следующий ход;
- `/goal <цель>` задаёт цель, к которой Codex идёт ход за ходом.

Параллельная работа:
- `--worktree` и `/worktree` создают управляемый git worktree, чтобы чаты не мешали друг другу;
- `codex agents` открывает центр управления сессиями на общем фоновом сервере (`/daemon`);
- `codex queue --thread <ID> --message "..."` отправляет сообщение в уже идущую сессию.

## ⚙️ Автоматизация: `codex exec`

`codex exec` (короткая форма — `codex e`) запускает задачу без интерфейса:
- **вывод:** прогресс идёт в stderr, в stdout — только финальный ответ, поэтому результат удобно перенаправлять;
- **права:** по умолчанию песочница **read-only**. Права выдаются явно: `--sandbox workspace-write`, при необходимости `--add-dir`;
- **stdin:** если передан и промпт-аргумент, и данные в stdin, то промпт — это инструкция, а stdin — контекст: `git diff | codex exec "..."`;
- **JSON:** `--json` превращает stdout в поток событий JSONL (`thread.started`, `turn.completed` с расходом токенов, `item.*` с командами и правками);
- **результат в файл:** `-o файл` сохраняет финальное сообщение, `--output-schema schema.json` требует ответ строго по JSON Schema;
- **без следов:** `--ephemeral` не пишет сессию на диск, `--ignore-user-config` не читает `config.toml`, `--ignore-rules` — `.rules`;
- **вне репозитория:** нужен `--skip-git-repo-check`;
- **продолжение:** `codex exec resume --last "дальше"` или по ID; `codex exec fork <ID>`.

Ревью кода без интерфейса: `codex review --uncommitted`, `--base main` или `--commit <sha>`. Модель для ревью задаётся ключом `review_model`.

**Ключ в CI.** Задайте `CODEX_API_KEY=... codex exec ...` только для самого вызова. Не кладите его в переменные всего job, где запускается код из репозитория. Для GitHub есть готовое действие `openai/codex-action@v1`.

### Codex из своего кода

Пример: передать `git diff` в Codex и получить найденные проблемы. Codex работает только на чтение (`--sandbox read-only`) и не сохраняет сессию (`--ephemeral`). Запуск — `git diff | <программа>`. Все версии проверены на подставном `codex`: аргументы, stdin, код ошибки, вход на 400 КБ без зависаний.

<details><summary>☕ Java 11+ — CodexReview.java (только стандартная библиотека)</summary>

```sh
git diff | java CodexReview.java
```

```java
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

public class CodexReview {
    static final String PROMPT =
        "Найди ошибки в этом диффе. Ответь списком: файл, строка, проблема.";

    public static void main(String[] args) throws Exception {
        byte[] diff = System.in.readAllBytes();               // git diff из stdin
        Process p = new ProcessBuilder(List.of(
                "codex", "exec", "--sandbox", "read-only", "--ephemeral", PROMPT))
            .redirectError(ProcessBuilder.Redirect.INHERIT)   // прогресс Codex идёт в stderr
            .start();

        // stdout читаем параллельно, иначе таймаут ниже не сработает
        CompletableFuture<String> answer = CompletableFuture.supplyAsync(() -> read(p.getInputStream()));
        try (OutputStream in = p.getOutputStream()) {
            in.write(diff);                                   // дифф уходит как контекст
        }
        if (!p.waitFor(10, TimeUnit.MINUTES)) {
            p.destroyForcibly();
            throw new IllegalStateException("codex exec: таймаут");
        }
        if (p.exitValue() != 0) {
            throw new IllegalStateException("codex exec завершился с кодом " + p.exitValue());
        }
        System.out.print(answer.get());                       // в stdout — только финальный ответ
    }

    static String read(InputStream s) {
        try {
            return new String(s.readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
```

</details>

<details><summary>🐍 Python 3.8+ — codex_review.py</summary>

```sh
git diff | python3 codex_review.py
```

```python
import subprocess
import sys

PROMPT = "Найди ошибки в этом диффе. Ответь списком: файл, строка, проблема."

diff = sys.stdin.read()  # git diff из stdin
result = subprocess.run(
    ["codex", "exec", "--sandbox", "read-only", "--ephemeral", PROMPT],
    input=diff,                # дифф уходит как контекст
    stdout=subprocess.PIPE,    # в stdout — только финальный ответ
    text=True,                 # stderr не перехватываем: там прогресс Codex
    timeout=600,
)
if result.returncode != 0:
    sys.exit(f"codex exec завершился с кодом {result.returncode}")
print(result.stdout, end="")
```

</details>

<details><summary>🟨 JavaScript (Node.js 18+) — codex_review.mjs</summary>

```sh
git diff | node codex_review.mjs
```

```javascript
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";

const PROMPT = "Найди ошибки в этом диффе. Ответь списком: файл, строка, проблема.";

const diff = readFileSync(0, "utf8"); // git diff из stdin
try {
  const answer = execFileSync(
    "codex",
    ["exec", "--sandbox", "read-only", "--ephemeral", PROMPT],
    {
      input: diff,                       // дифф уходит как контекст
      stdio: ["pipe", "pipe", "inherit"], // stderr — прогресс Codex
      encoding: "utf8",
      timeout: 10 * 60 * 1000,
    },
  );
  process.stdout.write(answer);         // в stdout — только финальный ответ
} catch (err) {
  console.error(`codex exec: ${err.status ?? err.message}`);
  process.exit(1);
}
```

</details>

<details><summary>🐹 Go 1.21+ — main.go</summary>

```sh
go mod init codexreview && go build -o review . && git diff | ./review
```

```go
package main

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"time"
)

const prompt = "Найди ошибки в этом диффе. Ответь списком: файл, строка, проблема."

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Minute)
	defer cancel()

	cmd := exec.CommandContext(ctx, "codex", "exec", "--sandbox", "read-only", "--ephemeral", prompt)
	cmd.Stdin = os.Stdin   // git diff из stdin уходит как контекст
	cmd.Stderr = os.Stderr // прогресс Codex
	answer, err := cmd.Output()
	if err != nil {
		fmt.Fprintln(os.Stderr, "codex exec:", err)
		os.Exit(1)
	}
	fmt.Print(string(answer)) // в stdout — только финальный ответ
}
```

</details>

<details><summary>🦀 Rust (stable) — main.rs, без внешних крейтов</summary>

```sh
rustc -O -o review main.rs && git diff | ./review
```

В стандартной библиотеке нет таймаута на процесс. Если он нужен — крейт `wait-timeout` или `tokio::process`.

```rust
use std::io::{self, Read, Write};
use std::process::{Command, Stdio};

const PROMPT: &str = "Найди ошибки в этом диффе. Ответь списком: файл, строка, проблема.";

fn main() -> io::Result<()> {
    let mut diff = Vec::new();
    io::stdin().read_to_end(&mut diff)?; // git diff из stdin

    let mut child = Command::new("codex")
        .args(["exec", "--sandbox", "read-only", "--ephemeral", PROMPT])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped()) // в stdout — только финальный ответ
        .stderr(Stdio::inherit()) // прогресс Codex
        .spawn()?;

    // пишем в отдельном потоке, чтобы не упереться в буфер пайпа
    let mut stdin = child.stdin.take().expect("stdin");
    let writer = std::thread::spawn(move || stdin.write_all(&diff));
    let out = child.wait_with_output()?;
    writer.join().expect("writer")?;

    if !out.status.success() {
        eprintln!("codex exec завершился: {}", out.status);
        std::process::exit(1);
    }
    io::stdout().write_all(&out.stdout)
}
```

</details>

<details><summary>🐚 Bash — codex-review.sh</summary>

```bash
#!/usr/bin/env bash
set -euo pipefail
prompt="Найди ошибки в этом диффе. Ответь списком: файл, строка, проблема."

# дифф уходит через stdin, прогресс — в stderr, в stdout — только ответ
git diff | timeout 10m codex exec --sandbox read-only --ephemeral "$prompt"
```

</details>

Для более плотной интеграции есть SDK:
- **TypeScript** — `npm i @openai/codex-sdk` (Node 18+): потоки, продолжение и возобновление сессий;
- **Python** — `pip install openai-codex` (Python 3.10+): управляет локальным `codex app-server` по JSON-RPC.

## 🔄 Если вы пришли из Claude Code

| Claude Code | Codex CLI |
| :--- | :--- |
| `CLAUDE.md` | `AGENTS.md` (или `project_doc_fallback_filenames = ["CLAUDE.md"]`) |
| `~/.claude/settings.json`, `.claude/settings.json` | `~/.codex/config.toml`, `.codex/config.toml` (TOML вместо JSON) |
| режимы прав (`Shift+Tab`) | песочница + политика одобрений, пресеты в `/permissions` |
| `.claude/skills/<n>/SKILL.md` | `.agents/skills/<n>/SKILL.md`, вызов `$n` |
| `.claude/agents/*.md` | `.codex/agents/*.toml` |
| `claude -p "..."` | `codex exec "..."` |
| `claude -c` / `claude -r` | `codex resume --last` / `codex resume <ID>` |
| `/compact`, `/clear`, `/model`, `/init`, `/mcp`, `/review` | те же команды |
| `/btw` | `/side` (алиас `/btw`) |

Перенести настройки, проекты и до 50 чатов за последние 30 дней из Claude Code или Cursor — команда `/import` в локальной сессии Codex. Исходная настройка при этом не меняется.

## 💡 Итог

- Открытый (Apache-2.0) агент на Rust с настоящей песочницей ОС: по умолчанию сеть выключена, запись ограничена рабочим каталогом, а `.git` защищён даже там.
- Работает от подписки ChatGPT (с Plus за $20) или от API-ключа; на Linux нужен `bubblewrap`. Для Gentoo есть пакеты в `gentoo-zh`, для Arch — в `extra`.
- Хорошо встраивается в скрипты: `codex exec` пишет в stdout только ответ, умеет JSONL и JSON Schema, по умолчанию работает только на чтение.
- Кто знаком с Claude Code, освоится быстро: те же идеи (инструкции проекта, скиллы, субагенты, хуки, MCP) под другими именами, а `/import` переносит настройки.

## 🔗 Ссылки

- Репозиторий: [openai/codex](https://github.com/openai/codex) · [релизы](https://github.com/openai/codex/releases) · [npm `@openai/codex`](https://www.npmjs.com/package/@openai/codex)
- Документация: [Codex CLI](https://learn.chatgpt.com/docs/codex/cli) · [команды и флаги](https://learn.chatgpt.com/docs/developer-commands?surface=cli) · [песочница и одобрения](https://learn.chatgpt.com/docs/agent-approvals-security) · [конфиг](https://learn.chatgpt.com/docs/config-file/config-reference) · [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [`codex exec`](https://learn.chatgpt.com/docs/non-interactive-mode) · [тарифы](https://learn.chatgpt.com/docs/pricing) · [всё одним файлом](https://learn.chatgpt.com/docs/codex-manual.md)
- В хранилище: [Сводная таблица AI-агентов](%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%29.md) · [Claude Code — гайд](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [MCP — серверы Model Context Protocol](Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) · [CodexPro — MCP-мост между ChatGPT и локальным репо](Tooling/CodexPro%20%E2%80%94%20MCP-%D0%BC%D0%BE%D1%81%D1%82%20%D0%BC%D0%B5%D0%B6%D0%B4%D1%83%20ChatGPT%20Developer%20Mode%20%D0%B8%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%BC%20%D1%80%D0%B5%D0%BF%D0%BE.md) · [abtop — мониторинг сессий Claude Code, Codex, OpenCode](Tooling/abtop%20%E2%80%94%20htop%20%D0%B4%D0%BB%D1%8F%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B9%20Claude%20Code-Codex-OpenCode%29.md) · [Свой харнесс на Claude API](Tooling/%D0%A1%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%20Claude%20API%20%E2%80%94%20Messages%20API%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28SDK%20%D0%B4%D0%BB%D1%8F%20Java%2C%20Python%2C%20JS%2C%20Go%3B%20%D1%81%D1%8B%D1%80%D0%BE%D0%B9%20HTTP%20%D0%B2%20Rust%20%D0%B8%20Bash%3B%20thinking%2C%20%D0%BE%D1%82%D0%BA%D0%B0%D0%B7%D1%8B%2C%20fallbacks%29.md)

#AI #Агенты #Codex #OpenAI #CLI
