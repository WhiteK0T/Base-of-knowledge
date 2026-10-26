---
создал заметку: 2026-10-27T06:40:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Harness
  - Claude
  - Anthropic
  - Java
  - Python
  - JavaScript
  - Go
  - Rust
  - Bash
Источник:
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
  - https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback
  - https://github.com/anthropics/anthropic-sdk-java
  - https://github.com/anthropics/anthropic-sdk-python
  - https://github.com/anthropics/anthropic-sdk-typescript
  - https://github.com/anthropics/anthropic-sdk-go
  - https://code.claude.com/docs/en/legal-and-compliance
---

# 🟠 Свой харнесс на Claude API — Messages API на 6 языках

Продолжение раздела «Если модель — Claude» из заметки [«ИИ-агент vs харнесс»](../../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md). Там харнесс говорит на OpenAI-совместимом диалекте (Ollama, DeepSeek, OpenRouter). Здесь **тот же харнесс** — те же три инструмента, песочница, подтверждение записи, `AGENTS.md`, обрезка вывода, — но на **Anthropic Messages API**:

- **Java, Python, JavaScript, Go** — через официальные SDK (`anthropic-java` 3.3.0, `anthropic` 2.3.0, `@anthropic-ai/sdk` 1.3.0, `anthropic-sdk-go` v2.3.0);
- **Rust и Bash** — сырым HTTP: официального SDK для Rust нет, а у Bash есть curl.

Все версии проверены на тестовом сервере, который изображает Messages API. С настоящим API код не запускался: для этого нужен ключ и деньги на счету.

> [!warning] Только API-ключ
> Свой харнесс работает с Claude **по API-ключу** из [Claude Console](https://platform.claude.com/), с оплатой за токены. Вход подпиской Pro/Max в сторонних приложениях условия Anthropic запрещают. Разбор — в вопросе 5 [основной заметки](../../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md).

## 🔀 Что меняется по сравнению с OpenAI-совместимым харнессом

| | OpenAI-совместимый харнесс | Этот харнесс |
| :--- | :--- | :--- |
| Эндпоинт | `/v1/chat/completions` | `/v1/messages` (в SDK — бета-ветка `client.beta.messages`, она нужна для `fallbacks`) |
| Авторизация | `Authorization: Bearer` | SDK с версией API `2026-10-21` шлют ключ как `Authorization: Bearer`; curl — как `x-api-key` + `anthropic-version: 2026-10-21` |
| Системный промпт | сообщение `role: system` | поле `system` |
| Инструменты | `{"type": "function", "function": {…, "parameters"}}` | `{name, description, input_schema}` |
| Вызов | `tool_calls[]`, аргументы — строка с JSON | блок `tool_use` в `content`, `input` — уже объект (битого JSON не бывает) |
| Результаты | по сообщению `role: tool` на вызов | **все** `tool_result` одного шага — **одним** сообщением `role: user`; ошибка — `is_error: true` |
| Признак конца | нет `tool_calls` | `stop_reason` ≠ `tool_use`; отдельно обрабатываются `refusal` и `max_tokens` |

## 🧠 Четыре вещи, которых не было в первом харнессе

1. **Ответ модели — в историю целиком.** Claude Opus 5.5 думает всегда. В ответе приходят блоки `thinking` (по умолчанию с пустым текстом, но с **подписью**), и их нужно вернуть в следующем запросе **без изменений**. Харнесс должен быть «append-only»: правка или удаление старых ходов ломает проверку этих блоков. Поэтому история только дописывается: Python и JS кладут `response.content` как есть, Java и Go — `response.toParam()` / `resp.ToParam()`, Rust и Bash — сырой JSON `content`.
2. **Глубина рассуждений — через `effort`.** Бюджета токенов на размышления (`budget_tokens`) у новых моделей больше нет, вместо него `output_config.effort`: `low`, `medium`, `high`, `xhigh`, `max`. У Opus 5.5 по умолчанию `medium`, и в коде он задан явно (переменная `HARNESS_EFFORT`).
3. **Отказы.** Классификаторы безопасности могут отклонить запрос. Это обычный HTTP 200 с `stop_reason: "refusal"` и `stop_details.category` (`cyber`, `bio`…). Харнесс печатает категорию и **откатывает ход** (задача и всё после неё из истории убираются), чтобы следующий запрос не начинался с пустого ответа.
4. **Страховка `fallbacks: "default"`.** С бета-заголовком `server-side-fallback-2026-07-01` API при отказе сам повторяет запрос на модели, которую Anthropic рекомендует для этой категории (для Claude Opus 5, например, отказ категории `cyber` уходит на Claude Opus 4.8). Повтор происходит внутри того же вызова, и харнессу ничего делать не нужно. Если отказала и запасная модель, приходит обычный `refusal`.

Переменные окружения названы `HARNESS_MODEL` и `HARNESS_EFFORT`, а не `CLAUDE_*`: префикс `CLAUDE_` занят самим Claude Code. Например, внутри его сессий уже задан `CLAUDE_EFFORT`, и харнесс, запущенный оттуда, молча подхватил бы чужое значение. На этом споткнулся первый же тест.

## 🔧 Настройка

| Переменная | По умолчанию | Смысл |
| :--- | :--- | :--- |
| `ANTHROPIC_API_KEY` | — (обязательна) | ключ из Claude Console |
| `ANTHROPIC_BASE_URL` | `https://api.anthropic.com` | адрес API (для прокси или тестового сервера) |
| `HARNESS_MODEL` | `claude-opus-5-5` | модель |
| `HARNESS_EFFORT` | `medium` | глубина рассуждений |
| `WORKDIR`, `AUTO_APPROVE` | `.`, — | как в базовом харнессе |

Модели и цены по справочнику Anthropic на 06.10.2026 (за 1 млн токенов, вход / выход):

| Модель | ID | Цена | Когда брать |
| :--- | :--- | :--- | :--- |
| Claude Opus 5.5 | `claude-opus-5-5` | $4 / $20 | по умолчанию: кодинг, агентные задачи |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | $2 / $10 | быстрее и дешевле, повседневная работа |
| Claude Haiku 5.5 | `claude-haiku-5-5` | $0,10 / $0,50 | простые и массовые задачи; **серверного fallback нет**, параметр `fallbacks` для неё убирают |
| Claude Fable 5.1 | `claude-fable-5-1` | $10 / $50 | самые сложные задачи |

Цены меняются; актуальные — на [странице цен](https://platform.claude.com/docs/en/about-claude/pricing). `max_tokens` здесь 16 000, без потоковой передачи. Для длинных ответов нужен стриминг (в SDK — `.stream()` и `get_final_message()` / `finalMessage()`), иначе можно упереться в таймаут HTTP.

## 💻 Код

<details><summary>☕ Java 21+ — ClaudeHarness.java (anthropic-java 3.3.0)</summary>

`pom.xml` — только чтобы Maven скачал SDK со всеми зависимостями (29 jar) в `lib/`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>local</groupId>
  <artifactId>claude-harness</artifactId>
  <version>1</version>
  <dependencies>
    <dependency>
      <groupId>com.anthropic</groupId>
      <artifactId>anthropic-java</artifactId>
      <version>3.3.0</version>
    </dependency>
  </dependencies>
</project>
```

```sh
mvn -q dependency:copy-dependencies -DoutputDirectory=lib
java -cp 'lib/*' ClaudeHarness.java
```

Аргументы вызова SDK сам разбирает в `record Args(String path, String content)` через `call.input(Args.class)`. Для отправки на `client.beta().messages()` есть готовый `.fallbacksDefault()`.

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.beta.messages.BetaContentBlockParam;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaMessageParam;
import com.anthropic.models.beta.messages.BetaOutputConfig;
import com.anthropic.models.beta.messages.BetaStopReason;
import com.anthropic.models.beta.messages.BetaTool;
import com.anthropic.models.beta.messages.BetaToolResultBlockParam;
import com.anthropic.models.beta.messages.BetaToolUseBlock;
import com.anthropic.models.beta.messages.MessageCreateParams;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

/** Харнесс на Claude API (SDK anthropic-java): те же инструменты и цикл, но формат Messages API. */
public class ClaudeHarness {
    static final String MODEL = env("HARNESS_MODEL", "claude-opus-5-5");
    static final String EFFORT = env("HARNESS_EFFORT", "medium");  // low | medium | high | xhigh | max
    static final Path ROOT = Path.of(env("WORKDIR", ".")).toAbsolutePath().normalize();
    static final boolean AUTO_APPROVE = "1".equals(System.getenv("AUTO_APPROVE"));
    static final int MAX_STEPS = 20;       // предохранитель от бесконечного цикла
    static final int MAX_OUTPUT = 10_000;  // сколько символов результата отдаём модели

    static final AnthropicClient CLIENT = AnthropicOkHttpClient.fromEnv();  // ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL
    static final BufferedReader IN = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));

    static final List<BetaTool> TOOLS = List.of(
            tool("list_files", "List files and directories at a path relative to the working directory.", "path"),
            tool("read_file", "Read a text file.", "path"),
            tool("write_file", "Create or overwrite a text file; parent directories are created.", "path", "content"));

    /** Аргументы инструментов: SDK сам разбирает input вызова в этот record. */
    record Args(String path, String content) {}

    record Result(String text, boolean isError) {}

    static BetaTool tool(String name, String description, String... params) {
        BetaTool.InputSchema.Properties.Builder properties = BetaTool.InputSchema.Properties.builder();
        for (String p : params) properties.putAdditionalProperty(p, JsonValue.from(Map.of("type", "string")));
        return BetaTool.builder().name(name).description(description)
                .inputSchema(BetaTool.InputSchema.builder().properties(properties.build()).required(List.of(params)).build())
                .build();
    }

    static String env(String name, String def) {
        String value = System.getenv(name);
        return value == null || value.isEmpty() ? def : value;
    }

    static String systemPrompt() throws Exception {
        String text = "You are a coding agent. Work only through the tools; paths are relative to the working directory. "
                + "When the task is done, answer with a short summary.";
        Path memory = ROOT.resolve("AGENTS.md");  // память проекта, как AGENTS.md / CLAUDE.md
        if (Files.isRegularFile(memory)) {
            text += "\n\nProject instructions (AGENTS.md):\n" + Files.readString(memory);
        }
        return text;
    }

    static Path safePath(String p) {  // песочница: никаких выходов за ROOT
        Path full = ROOT.resolve(Objects.requireNonNull(p, "missing argument path")).normalize();
        if (!full.startsWith(ROOT)) throw new SecurityException("path outside workdir");
        return full;
    }

    static String ask(String prompt) throws Exception {
        System.out.print(prompt);
        System.out.flush();
        String line = IN.readLine();
        return line == null ? null : line.strip();
    }

    static boolean approve(String action) throws Exception {
        return AUTO_APPROVE || "y".equalsIgnoreCase(ask("  Разрешить " + action + "? [y/N] "));
    }

    /** Ошибку видит модель (is_error), харнесс не падает. */
    static Result runTool(BetaToolUseBlock call) {
        try {
            Args args = call.input(Args.class);
            switch (call.name()) {
                case "list_files" -> {
                    try (var entries = Files.list(safePath(args.path()))) {
                        return new Result(entries.map(e -> e.getFileName() + (Files.isDirectory(e) ? "/" : ""))
                                .sorted().collect(Collectors.joining("\n")), false);
                    }
                }
                case "read_file" -> {
                    return new Result(Files.readString(safePath(args.path())), false);
                }
                case "write_file" -> {
                    Path file = safePath(args.path());
                    String content = Objects.requireNonNull(args.content(), "missing argument content");
                    if (!approve("write_file " + args.path())) return new Result("user denied the write", true);
                    Files.createDirectories(file.getParent());
                    Files.writeString(file, content);
                    return new Result("ok: wrote " + content.length() + " chars to " + args.path(), false);
                }
                default -> {
                    return new Result("unknown tool " + call.name(), true);
                }
            }
        } catch (Exception e) {
            return new Result(e.toString(), true);
        }
    }

    static String truncate(String text) {
        if (text.length() <= MAX_OUTPUT) return text;
        return text.substring(0, MAX_OUTPUT) + "\n[...truncated " + (text.length() - MAX_OUTPUT) + " chars]";
    }

    public static void main(String[] argv) throws Exception {
        String system = systemPrompt();
        List<BetaMessageParam> messages = new ArrayList<>();
        System.out.printf("Харнесс: %s (effort %s), папка %s. Пустая строка — выход.%n", MODEL, EFFORT, ROOT);
        String task;
        while ((task = ask("> ")) != null && !task.isEmpty()) {
            int turnStart = messages.size();
            messages.add(BetaMessageParam.ofUser(task));
            int step = 1;
            for (; step <= MAX_STEPS; step++) {  // агентный цикл
                MessageCreateParams.Builder params = MessageCreateParams.builder()
                        .model(MODEL).maxTokens(16000L).system(system).messages(messages)
                        .outputConfig(BetaOutputConfig.builder().effort(BetaOutputConfig.Effort.of(EFFORT)).build())
                        // при отказе модели API сам повторит запрос на рекомендованной запасной
                        .addBeta("server-side-fallback-2026-07-01").fallbacksDefault();
                TOOLS.forEach(params::addTool);
                BetaMessage response = CLIENT.beta().messages().create(params.build());
                Optional<BetaStopReason> stop = response.stopReason();
                if (stop.equals(Optional.of(BetaStopReason.REFUSAL))) {
                    String details = response.stopDetails()
                            .map(d -> d.category().map(Object::toString).orElse("—") + "): " + d.explanation().orElse(""))
                            .orElse("—)");
                    System.out.println("Модель отказалась (категория: " + details);
                    messages.subList(turnStart, messages.size()).clear();  // отказанный ход в историю не попадает
                    break;
                }
                messages.add(response.toParam());  // ответ — целиком: thinking с подписью, текст, tool_use
                List<BetaToolUseBlock> calls = response.content().stream().flatMap(b -> b.toolUse().stream()).toList();
                if (!stop.equals(Optional.of(BetaStopReason.TOOL_USE)) || calls.isEmpty()) {
                    System.out.println(response.content().stream().flatMap(b -> b.text().stream())
                            .map(t -> t.text()).collect(Collectors.joining()));
                    if (stop.equals(Optional.of(BetaStopReason.MAX_TOKENS))) System.out.println("(ответ обрезан по max_tokens)");
                    break;
                }
                List<BetaContentBlockParam> results = new ArrayList<>();
                for (BetaToolUseBlock call : calls) {
                    System.err.printf("  [шаг %d] %s %s%n", step, call.name(), call._input());
                    Result result = runTool(call);
                    results.add(BetaContentBlockParam.ofToolResult(BetaToolResultBlockParam.builder()
                            .toolUseId(call.id()).content(truncate(result.text())).isError(result.isError()).build()));
                }
                messages.add(BetaMessageParam.ofUserOfContentBlockParams(results));  // все результаты — одним сообщением
            }
            if (step > MAX_STEPS) System.out.println("Остановлено: больше " + MAX_STEPS + " шагов.");
        }
    }
}
```

</details>

<details><summary>🐍 Python 3.10+ — claude_harness.py (anthropic 2.3.0)</summary>

```sh
python3 -m venv .venv && .venv/bin/pip install anthropic
.venv/bin/python claude_harness.py
```

```python
#!/usr/bin/env python3
"""Харнесс на Claude API (SDK anthropic): те же инструменты и цикл, но формат Messages API."""
import json
import os
import sys
from pathlib import Path

import anthropic

MODEL = os.environ.get("HARNESS_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("HARNESS_EFFORT", "medium")  # low | medium | high | xhigh | max
ROOT = Path(os.environ.get("WORKDIR", ".")).resolve()
AUTO_APPROVE = os.environ.get("AUTO_APPROVE") == "1"
MAX_STEPS = 20       # предохранитель от бесконечного цикла
MAX_OUTPUT = 10_000  # сколько символов результата отдаём модели

TOOLS = [
    {"name": "list_files",
     "description": "List files and directories at a path relative to the working directory.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "read_file",
     "description": "Read a text file.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "write_file",
     "description": "Create or overwrite a text file; parent directories are created.",
     "input_schema": {"type": "object",
                      "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                      "required": ["path", "content"]}},
]

client = anthropic.Anthropic()  # ключ и адрес — из ANTHROPIC_API_KEY и ANTHROPIC_BASE_URL


def system_prompt():
    text = ("You are a coding agent. Work only through the tools; paths are relative to the working directory. "
            "When the task is done, answer with a short summary.")
    memory = ROOT / "AGENTS.md"  # память проекта, как AGENTS.md / CLAUDE.md
    if memory.is_file():
        text += "\n\nProject instructions (AGENTS.md):\n" + memory.read_text(encoding="utf-8")
    return text


def safe_path(p):  # песочница: никаких выходов за ROOT
    full = (ROOT / p).resolve()
    if not full.is_relative_to(ROOT):
        raise PermissionError("path outside workdir")
    return full


def approve(action):
    return AUTO_APPROVE or input(f"  Разрешить {action}? [y/N] ").strip().lower() == "y"


def run_tool(name, args):
    """Возвращает (текст, is_error): ошибку видит модель, харнесс не падает."""
    try:
        if name == "list_files":
            return "\n".join(sorted(e.name + ("/" if e.is_dir() else "") for e in safe_path(args["path"]).iterdir())), False
        if name == "read_file":
            return safe_path(args["path"]).read_text(encoding="utf-8"), False
        if name == "write_file":
            file = safe_path(args["path"])
            if not approve(f"write_file {args['path']}"):
                return "user denied the write", True
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(args["content"], encoding="utf-8")
            return f"ok: wrote {len(args['content'])} chars to {args['path']}", False
        return f"unknown tool {name}", True
    except Exception as e:
        return repr(e), True


def truncate(text):
    if len(text) <= MAX_OUTPUT:
        return text
    return text[:MAX_OUTPUT] + f"\n[...truncated {len(text) - MAX_OUTPUT} chars]"


def main():
    system = system_prompt()
    messages = []
    print(f"Харнесс: {MODEL} (effort {EFFORT}), папка {ROOT}. Пустая строка — выход.")
    while True:
        try:
            task = input("> ").strip()
        except EOFError:
            break
        if not task:
            break
        turn_start = len(messages)
        messages.append({"role": "user", "content": task})
        for step in range(1, MAX_STEPS + 1):  # агентный цикл
            response = client.beta.messages.create(
                model=MODEL, max_tokens=16000, system=system, tools=TOOLS, messages=messages,
                output_config={"effort": EFFORT},
                # при отказе модели API сам повторит запрос на рекомендованной запасной
                betas=["server-side-fallback-2026-07-01"], fallbacks="default",
            )
            if response.stop_reason == "refusal":
                details = response.stop_details
                print(f"Модель отказалась (категория: {details.category if details else '—'}): "
                      f"{details.explanation if details else ''}")
                del messages[turn_start:]  # отказанный ход в историю не попадает
                break
            # ответ — в историю целиком: thinking-блоки с подписью, текст, tool_use
            messages.append({"role": "assistant", "content": response.content})
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            if response.stop_reason != "tool_use" or not tool_uses:
                print("".join(b.text for b in response.content if b.type == "text"))
                if response.stop_reason == "max_tokens":
                    print("(ответ обрезан по max_tokens)")
                break
            results = []
            for block in tool_uses:
                print(f"  [шаг {step}] {block.name} {json.dumps(block.input, ensure_ascii=False)}", file=sys.stderr)
                text, is_error = run_tool(block.name, block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": truncate(text), "is_error": is_error})
            messages.append({"role": "user", "content": results})  # все результаты шага — одним сообщением
        else:
            print(f"Остановлено: больше {MAX_STEPS} шагов.")


if __name__ == "__main__":
    main()
```

</details>

<details><summary>🟨 JavaScript (Node.js 20+) — claude-harness.mjs (@anthropic-ai/sdk 1.3.0)</summary>

```sh
npm i @anthropic-ai/sdk     # в папке со скриптом
node claude-harness.mjs
```

```javascript
#!/usr/bin/env node
// Харнесс на Claude API (SDK @anthropic-ai/sdk): те же инструменты и цикл, но формат Messages API.
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import Anthropic from "@anthropic-ai/sdk";

const MODEL = process.env.HARNESS_MODEL || "claude-opus-5-5";
const EFFORT = process.env.HARNESS_EFFORT || "medium";  // low | medium | high | xhigh | max
const ROOT = path.resolve(process.env.WORKDIR || ".");
const AUTO_APPROVE = process.env.AUTO_APPROVE === "1";
const MAX_STEPS = 20;       // предохранитель от бесконечного цикла
const MAX_OUTPUT = 10_000;  // сколько символов результата отдаём модели

const tool = (name, description, params) => ({
  name, description,
  input_schema: {
    type: "object",
    properties: Object.fromEntries(params.map((p) => [p, {type: "string"}])),
    required: params,
  },
});
const TOOLS = [
  tool("list_files", "List files and directories at a path relative to the working directory.", ["path"]),
  tool("read_file", "Read a text file.", ["path"]),
  tool("write_file", "Create or overwrite a text file; parent directories are created.", ["path", "content"]),
];

const client = new Anthropic();  // ключ и адрес — из ANTHROPIC_API_KEY и ANTHROPIC_BASE_URL

const lines = readline.createInterface({input: process.stdin})[Symbol.asyncIterator]();
async function ask(prompt) {
  process.stdout.write(prompt);
  const {value, done} = await lines.next();
  return done ? null : value.trim();
}

function systemPrompt() {
  let text = "You are a coding agent. Work only through the tools; paths are relative to the working directory. " +
    "When the task is done, answer with a short summary.";
  const memory = path.join(ROOT, "AGENTS.md");  // память проекта, как AGENTS.md / CLAUDE.md
  if (fs.existsSync(memory)) text += "\n\nProject instructions (AGENTS.md):\n" + fs.readFileSync(memory, "utf8");
  return text;
}

function safePath(p) {  // песочница: никаких выходов за ROOT
  const full = path.resolve(ROOT, String(p));
  if (full !== ROOT && !full.startsWith(ROOT + path.sep)) throw new Error("path outside workdir");
  return full;
}

const approve = async (action) =>
  AUTO_APPROVE || (await ask(`  Разрешить ${action}? [y/N] `))?.toLowerCase() === "y";

// Возвращает [текст, isError]: ошибку видит модель, харнесс не падает.
async function runTool(name, args) {
  try {
    switch (name) {
      case "list_files":
        return [fs.readdirSync(safePath(args.path), {withFileTypes: true})
          .map((e) => e.name + (e.isDirectory() ? "/" : "")).sort().join("\n"), false];
      case "read_file":
        return [fs.readFileSync(safePath(args.path), "utf8"), false];
      case "write_file": {
        const file = safePath(args.path);
        if (!(await approve(`write_file ${args.path}`))) return ["user denied the write", true];
        fs.mkdirSync(path.dirname(file), {recursive: true});
        fs.writeFileSync(file, args.content);
        return [`ok: wrote ${args.content.length} chars to ${args.path}`, false];
      }
      default:
        return [`unknown tool ${name}`, true];
    }
  } catch (e) {
    return [e.message, true];
  }
}

const truncate = (text) => text.length <= MAX_OUTPUT ? text
  : text.slice(0, MAX_OUTPUT) + `\n[...truncated ${text.length - MAX_OUTPUT} chars]`;

const system = systemPrompt();
const messages = [];
console.log(`Харнесс: ${MODEL} (effort ${EFFORT}), папка ${ROOT}. Пустая строка — выход.`);
for (let task; (task = await ask("> "));) {
  const turnStart = messages.length;
  messages.push({role: "user", content: task});
  let step = 1;
  for (; step <= MAX_STEPS; step++) {  // агентный цикл
    const response = await client.beta.messages.create({
      model: MODEL, max_tokens: 16000, system, tools: TOOLS, messages,
      output_config: {effort: EFFORT},
      // при отказе модели API сам повторит запрос на рекомендованной запасной
      betas: ["server-side-fallback-2026-07-01"], fallbacks: "default",
    });
    if (response.stop_reason === "refusal") {
      const d = response.stop_details;
      console.log(`Модель отказалась (категория: ${d?.category ?? "—"}): ${d?.explanation ?? ""}`);
      messages.splice(turnStart);  // отказанный ход в историю не попадает
      break;
    }
    // ответ — в историю целиком: thinking-блоки с подписью, текст, tool_use
    messages.push({role: "assistant", content: response.content});
    const toolUses = response.content.filter((b) => b.type === "tool_use");
    if (response.stop_reason !== "tool_use" || toolUses.length === 0) {
      console.log(response.content.filter((b) => b.type === "text").map((b) => b.text).join(""));
      if (response.stop_reason === "max_tokens") console.log("(ответ обрезан по max_tokens)");
      break;
    }
    const results = [];
    for (const block of toolUses) {
      console.error(`  [шаг ${step}] ${block.name} ${JSON.stringify(block.input)}`);
      const [text, isError] = await runTool(block.name, block.input);
      results.push({type: "tool_result", tool_use_id: block.id, content: truncate(text), is_error: isError});
    }
    messages.push({role: "user", content: results});  // все результаты шага — одним сообщением
  }
  if (step > MAX_STEPS) console.log(`Остановлено: больше ${MAX_STEPS} шагов.`);
}
process.exit(0);
```

</details>

<details><summary>🐹 Go 1.25+ — main.go (anthropic-sdk-go v2.3.0)</summary>

```sh
go mod init claudeharness && go get github.com/anthropics/anthropic-sdk-go/v2
go run .
```

`fallbacks: "default"` в Go — вариант объединения: `BetaFallbacksParamUnion{OfDefault: constant.ValueOf[constant.Default]()}`. Аргументы вызова — сырой JSON из `b.JSON.Input.Raw()`.

```go
// Харнесс на Claude API (SDK anthropic-sdk-go): те же инструменты и цикл, но формат Messages API.
package main

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"unicode/utf8"

	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/shared/constant"
)

const (
	maxSteps  = 20     // предохранитель от бесконечного цикла
	maxOutput = 10_000 // сколько символов результата отдаём модели
)

var (
	model       = env("HARNESS_MODEL", "claude-opus-5-5")
	effort      = env("HARNESS_EFFORT", "medium") // low | medium | high | xhigh | max
	root, _     = filepath.Abs(env("WORKDIR", "."))
	autoApprove = os.Getenv("AUTO_APPROVE") == "1"
	stdin       = bufio.NewScanner(os.Stdin)
	client      = anthropic.NewClient() // ключ и адрес — из ANTHROPIC_API_KEY и ANTHROPIC_BASE_URL
)

var tools = []anthropic.BetaToolUnionParam{
	tool("list_files", "List files and directories at a path relative to the working directory.", "path"),
	tool("read_file", "Read a text file.", "path"),
	tool("write_file", "Create or overwrite a text file; parent directories are created.", "path", "content"),
}

func tool(name, description string, params ...string) anthropic.BetaToolUnionParam {
	props := map[string]any{}
	for _, p := range params {
		props[p] = map[string]string{"type": "string"}
	}
	return anthropic.BetaToolUnionParam{OfTool: &anthropic.BetaToolParam{
		Name:        name,
		Description: anthropic.String(description),
		InputSchema: anthropic.BetaToolInputSchemaParam{Properties: props, Required: params},
	}}
}

func env(name, def string) string {
	if v := os.Getenv(name); v != "" {
		return v
	}
	return def
}

func systemPrompt() string {
	text := "You are a coding agent. Work only through the tools; paths are relative to the working directory. " +
		"When the task is done, answer with a short summary."
	if b, err := os.ReadFile(filepath.Join(root, "AGENTS.md")); err == nil { // память проекта, как AGENTS.md / CLAUDE.md
		text += "\n\nProject instructions (AGENTS.md):\n" + string(b)
	}
	return text
}

func safePath(p string) (string, error) { // песочница: никаких выходов за root
	full := filepath.Join(root, p)
	if full != root && !strings.HasPrefix(full, root+string(filepath.Separator)) {
		return "", errors.New("path outside workdir")
	}
	return full, nil
}

func ask(prompt string) (string, bool) {
	fmt.Print(prompt)
	if !stdin.Scan() {
		return "", false
	}
	return strings.TrimSpace(stdin.Text()), true
}

func approve(action string) bool {
	if autoApprove {
		return true
	}
	answer, _ := ask("  Разрешить " + action + "? [y/N] ")
	return strings.EqualFold(answer, "y")
}

// runTool возвращает ошибку текстом: модель увидит её как is_error, харнесс не падает.
func runTool(name, rawInput string) (string, error) {
	var args struct {
		Path    *string `json:"path"`
		Content *string `json:"content"`
	}
	if err := json.Unmarshal([]byte(rawInput), &args); err != nil {
		return "", err
	}
	if args.Path == nil {
		return "", errors.New("missing argument path")
	}
	path, err := safePath(*args.Path)
	if err != nil {
		return "", err
	}
	switch name {
	case "list_files":
		entries, err := os.ReadDir(path)
		if err != nil {
			return "", err
		}
		names := make([]string, 0, len(entries))
		for _, e := range entries {
			if e.IsDir() {
				names = append(names, e.Name()+"/")
			} else {
				names = append(names, e.Name())
			}
		}
		return strings.Join(names, "\n"), nil
	case "read_file":
		b, err := os.ReadFile(path)
		return string(b), err
	case "write_file":
		if args.Content == nil {
			return "", errors.New("missing argument content")
		}
		if !approve("write_file " + *args.Path) {
			return "", errors.New("user denied the write")
		}
		if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
			return "", err
		}
		if err := os.WriteFile(path, []byte(*args.Content), 0o644); err != nil {
			return "", err
		}
		return fmt.Sprintf("ok: wrote %d chars to %s", utf8.RuneCountInString(*args.Content), *args.Path), nil
	}
	return "", fmt.Errorf("unknown tool %s", name)
}

func truncate(text string) string {
	runes := []rune(text)
	if len(runes) <= maxOutput {
		return text
	}
	return string(runes[:maxOutput]) + fmt.Sprintf("\n[...truncated %d chars]", len(runes)-maxOutput)
}

func main() {
	system := []anthropic.BetaTextBlockParam{{Text: systemPrompt()}}
	var messages []anthropic.BetaMessageParam
	fmt.Printf("Харнесс: %s (effort %s), папка %s. Пустая строка — выход.\n", model, effort, root)
	for {
		task, ok := ask("> ")
		if !ok || task == "" {
			return
		}
		turnStart := len(messages)
		messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(task)))
		step := 1
		for ; step <= maxSteps; step++ { // агентный цикл
			resp, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
				Model: model, MaxTokens: 16000, System: system, Tools: tools, Messages: messages,
				OutputConfig: anthropic.BetaOutputConfigParam{Effort: anthropic.BetaOutputConfigEffort(effort)},
				// при отказе модели API сам повторит запрос на рекомендованной запасной
				Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_07_01},
				Fallbacks: anthropic.BetaFallbacksParamUnion{OfDefault: constant.ValueOf[constant.Default]()},
			})
			if err != nil {
				fmt.Fprintln(os.Stderr, "ошибка:", err)
				os.Exit(1)
			}
			if resp.StopReason == anthropic.BetaStopReasonRefusal {
				fmt.Printf("Модель отказалась (категория: %s): %s\n", resp.StopDetails.Category, resp.StopDetails.Explanation)
				messages = messages[:turnStart] // отказанный ход в историю не попадает
				break
			}
			messages = append(messages, resp.ToParam()) // ответ — целиком: thinking с подписью, текст, tool_use
			var text strings.Builder
			var results []anthropic.BetaContentBlockParamUnion
			for _, block := range resp.Content {
				switch b := block.AsAny().(type) {
				case anthropic.BetaTextBlock:
					text.WriteString(b.Text)
				case anthropic.BetaToolUseBlock:
					raw := b.JSON.Input.Raw()
					fmt.Fprintf(os.Stderr, "  [шаг %d] %s %s\n", step, b.Name, raw)
					result, err := runTool(b.Name, raw)
					if err != nil {
						result = err.Error()
					}
					results = append(results, anthropic.NewBetaToolResultBlock(b.ID, truncate(result), err != nil))
				}
			}
			if resp.StopReason != anthropic.BetaStopReasonToolUse || len(results) == 0 {
				fmt.Println(text.String())
				if resp.StopReason == anthropic.BetaStopReasonMaxTokens {
					fmt.Println("(ответ обрезан по max_tokens)")
				}
				break
			}
			messages = append(messages, anthropic.NewBetaUserMessage(results...)) // все результаты — одним сообщением
		}
		if step > maxSteps {
			fmt.Printf("Остановлено: больше %d шагов.\n", maxSteps)
		}
	}
}
```

</details>

<details><summary>🦀 Rust 1.88+ — Cargo.toml + src/main.rs (сырой HTTP, ureq 3)</summary>

```toml
[package]
name = "claude-harness"
version = "0.1.0"
edition = "2024"

[dependencies]
serde_json = "1"
ureq = { version = "3", features = ["json"] }
```

```sh
cargo run --release
```

Чтобы при ошибке API (400, 429…) увидеть текст ошибки, а не только код, запрос отправляется с `http_status_as_error(false)`.

```rust
// Харнесс на Claude API через сырой HTTP (официального SDK для Rust нет): формат Messages API.
use serde_json::{Value, json};
use std::error::Error;
use std::io::{self, BufRead, StdinLock, Write};
use std::path::{Component, Path, PathBuf};
use std::{env, fs};

const MAX_STEPS: usize = 20; // предохранитель от бесконечного цикла
const MAX_OUTPUT: usize = 10_000; // сколько символов результата отдаём модели

struct Harness {
    base_url: String,
    api_key: String,
    model: String,
    effort: String, // low | medium | high | xhigh | max
    root: PathBuf,
    auto_approve: bool,
    stdin: io::Lines<StdinLock<'static>>,
}

fn var(name: &str, default: &str) -> String {
    env::var(name)
        .ok()
        .filter(|v| !v.is_empty())
        .unwrap_or_else(|| default.to_string())
}

fn truncate(text: String) -> String {
    let len = text.chars().count();
    if len <= MAX_OUTPUT {
        return text;
    }
    let head: String = text.chars().take(MAX_OUTPUT).collect();
    format!("{head}\n[...truncated {} chars]", len - MAX_OUTPUT)
}

fn tools() -> Value {
    json!([
        {"name": "list_files",
         "description": "List files and directories at a path relative to the working directory.",
         "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
        {"name": "read_file",
         "description": "Read a text file.",
         "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
        {"name": "write_file",
         "description": "Create or overwrite a text file; parent directories are created.",
         "input_schema": {"type": "object",
                          "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                          "required": ["path", "content"]}}
    ])
}

impl Harness {
    fn system_prompt(&self) -> String {
        let mut text = String::from(
            "You are a coding agent. Work only through the tools; paths are relative to the working directory. \
             When the task is done, answer with a short summary.",
        );
        // память проекта, как AGENTS.md / CLAUDE.md
        if let Ok(memory) = fs::read_to_string(self.root.join("AGENTS.md")) {
            text += "\n\nProject instructions (AGENTS.md):\n";
            text += &memory;
        }
        text
    }

    fn safe_path(&self, p: &str) -> Result<PathBuf, String> {
        // песочница: только относительные пути без «..»
        let rel = Path::new(p);
        if rel
            .components()
            .any(|c| !matches!(c, Component::Normal(_) | Component::CurDir))
        {
            return Err("path outside workdir".into());
        }
        Ok(self.root.join(rel))
    }

    fn ask(&mut self, prompt: &str) -> Option<String> {
        print!("{prompt}");
        io::stdout().flush().ok();
        self.stdin.next()?.ok().map(|line| line.trim().to_string())
    }

    fn approve(&mut self, action: &str) -> bool {
        self.auto_approve
            || self
                .ask(&format!("  Разрешить {action}? [y/N] "))
                .is_some_and(|a| a.eq_ignore_ascii_case("y"))
    }

    /// Err — текст ошибки: модель увидит его как is_error, харнесс не падает.
    fn run_tool(&mut self, name: &str, args: &Value) -> Result<String, String> {
        let arg = |key: &str| {
            args[key]
                .as_str()
                .map(str::to_string)
                .ok_or(format!("missing argument {key}"))
        };
        match name {
            "list_files" => {
                let mut names: Vec<String> = fs::read_dir(self.safe_path(&arg("path")?)?)
                    .map_err(|e| e.to_string())?
                    .filter_map(Result::ok)
                    .map(|e| {
                        let name = e.file_name().to_string_lossy().into_owned();
                        if e.path().is_dir() { name + "/" } else { name }
                    })
                    .collect();
                names.sort();
                Ok(names.join("\n"))
            }
            "read_file" => {
                fs::read_to_string(self.safe_path(&arg("path")?)?).map_err(|e| e.to_string())
            }
            "write_file" => {
                let (path, content) = (arg("path")?, arg("content")?);
                let file = self.safe_path(&path)?;
                if !self.approve(&format!("write_file {path}")) {
                    return Err("user denied the write".into());
                }
                if let Some(dir) = file.parent() {
                    fs::create_dir_all(dir).map_err(|e| e.to_string())?;
                }
                fs::write(&file, &content).map_err(|e| e.to_string())?;
                Ok(format!(
                    "ok: wrote {} chars to {path}",
                    content.chars().count()
                ))
            }
            _ => Err(format!("unknown tool {name}")),
        }
    }

    fn create(&self, system: &str, messages: &[Value]) -> Result<Value, Box<dyn Error>> {
        let body = json!({
            "model": self.model, "max_tokens": 16000, "system": system, "tools": tools(), "messages": messages,
            "output_config": {"effort": self.effort},
            "fallbacks": "default", // при отказе модели API сам повторит запрос на рекомендованной запасной
        });
        let mut resp = ureq::post(format!("{}/v1/messages", self.base_url))
            .config()
            .http_status_as_error(false)
            .build()
            .header("x-api-key", &self.api_key)
            .header("anthropic-version", "2026-10-21")
            .header("anthropic-beta", "server-side-fallback-2026-07-01")
            .send_json(body)?;
        let status = resp.status();
        let reply: Value = resp.body_mut().read_json()?;
        if !status.is_success() {
            return Err(format!("HTTP {status}: {}", reply["error"]["message"]).into());
        }
        Ok(reply)
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let api_key = env::var("ANTHROPIC_API_KEY").map_err(|_| "set ANTHROPIC_API_KEY")?;
    let mut h = Harness {
        base_url: var("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
        api_key,
        model: var("HARNESS_MODEL", "claude-opus-5-5"),
        effort: var("HARNESS_EFFORT", "medium"),
        root: fs::canonicalize(var("WORKDIR", "."))?,
        auto_approve: env::var("AUTO_APPROVE").as_deref() == Ok("1"),
        stdin: io::stdin().lock().lines(),
    };
    let system = h.system_prompt();
    let mut messages: Vec<Value> = Vec::new();
    println!(
        "Харнесс: {} (effort {}), папка {}. Пустая строка — выход.",
        h.model,
        h.effort,
        h.root.display()
    );
    while let Some(task) = h.ask("> ").filter(|t| !t.is_empty()) {
        let turn_start = messages.len();
        messages.push(json!({"role": "user", "content": task}));
        let mut finished = false;
        for step in 1..=MAX_STEPS {
            // агентный цикл
            let resp = h.create(&system, &messages)?;
            let stop = resp["stop_reason"].as_str().unwrap_or("");
            if stop == "refusal" {
                let d = &resp["stop_details"];
                println!(
                    "Модель отказалась (категория: {}): {}",
                    d["category"].as_str().unwrap_or("—"),
                    d["explanation"].as_str().unwrap_or("")
                );
                messages.truncate(turn_start); // отказанный ход в историю не попадает
                finished = true;
                break;
            }
            // ответ — в историю целиком: thinking с подписью, текст, tool_use
            messages.push(json!({"role": "assistant", "content": resp["content"]}));
            let blocks = resp["content"].as_array().cloned().unwrap_or_default();
            let calls: Vec<&Value> = blocks.iter().filter(|b| b["type"] == "tool_use").collect();
            if stop != "tool_use" || calls.is_empty() {
                let text: String = blocks
                    .iter()
                    .filter(|b| b["type"] == "text")
                    .filter_map(|b| b["text"].as_str())
                    .collect();
                println!("{text}");
                if stop == "max_tokens" {
                    println!("(ответ обрезан по max_tokens)");
                }
                finished = true;
                break;
            }
            let mut results = Vec::new();
            for call in calls {
                let name = call["name"].as_str().unwrap_or("");
                eprintln!("  [шаг {step}] {name} {}", call["input"]);
                let (text, is_error) = match h.run_tool(name, &call["input"]) {
                    Ok(text) => (text, false),
                    Err(e) => (e, true),
                };
                results.push(json!({"type": "tool_result", "tool_use_id": call["id"],
                                    "content": truncate(text), "is_error": is_error}));
            }
            messages.push(json!({"role": "user", "content": results})); // все результаты — одним сообщением
        }
        if !finished {
            println!("Остановлено: больше {MAX_STEPS} шагов.");
        }
    }
    Ok(())
}
```

</details>

<details><summary>🐚 Bash 4+ — claude-harness.sh (curl + jq 1.6+)</summary>

```sh
bash claude-harness.sh
```

Результаты одного шага копятся в файле JSON Lines и уходят одним сообщением (`jq -s`). Системный промпт передаётся в jq через `--rawfile`, а не аргументом: `AGENTS.md` может быть длинным.

```bash
#!/usr/bin/env bash
# Харнесс на Claude API через curl + jq: формат Messages API. Нужны bash 4+, curl, jq 1.6+.
set -uo pipefail
: "${ANTHROPIC_API_KEY:?set ANTHROPIC_API_KEY}"

BASE_URL=${ANTHROPIC_BASE_URL:-https://api.anthropic.com}
MODEL=${HARNESS_MODEL:-claude-opus-5-5}
EFFORT=${HARNESS_EFFORT:-medium}  # low | medium | high | xhigh | max
ROOT=$(cd "${WORKDIR:-.}" && pwd -P) || exit 1
MAX_STEPS=20      # предохранитель от бесконечного цикла
MAX_OUTPUT=10000  # сколько символов результата отдаём модели

TOOLS='[
 {"name": "list_files",
  "description": "List files and directories at a path relative to the working directory.",
  "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
 {"name": "read_file",
  "description": "Read a text file.",
  "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
 {"name": "write_file",
  "description": "Create or overwrite a text file; parent directories are created.",
  "input_schema": {"type": "object",
                   "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                   "required": ["path", "content"]}}]'

WORK=$(mktemp -d) && trap 'rm -rf "$WORK"' EXIT
HIST=$WORK/history.json REQ=$WORK/request.json OUT=$WORK/tool.out RESULTS=$WORK/results.jsonl
echo '[]' >"$HIST"
{
  printf '%s' "You are a coding agent. Work only through the tools; paths are relative to the working directory. "
  printf '%s' "When the task is done, answer with a short summary."
  if [[ -f $ROOT/AGENTS.md ]]; then  # память проекта, как AGENTS.md / CLAUDE.md
    printf '\n\nProject instructions (AGENTS.md):\n'
    cat "$ROOT/AGENTS.md"
  fi
} >"$WORK/system.txt"

push() {  # добавить сообщение (JSON со stdin) в историю
  jq --slurpfile m /dev/stdin '. + $m' "$HIST" >"$HIST.new" && mv "$HIST.new" "$HIST"
}

safe_path() {  # песочница: только относительные пути без «..»
  [[ $1 == /* || /$1/ == */../* ]] && return 1
  printf '%s/%s' "$ROOT" "$1"
}

run_tool() {  # $1 — имя, $2 — input (JSON-объект); текст результата — в $OUT; код 1 — ошибка (is_error)
  local name=$1 input=$2 path file ans=""
  case $name in
    list_files | read_file | write_file) ;;
    *) echo "unknown tool $name" >"$OUT"; return 1 ;;
  esac
  path=$(jq -er '.path | strings' <<<"$input") || { echo "missing argument path" >"$OUT"; return 1; }
  file=$(safe_path "$path") || { echo "path outside workdir" >"$OUT"; return 1; }
  case $name in
    list_files)
      ls -Ap -- "$file" >"$OUT" 2>/dev/null || { echo "cannot list $path" >"$OUT"; return 1; } ;;
    read_file)
      [[ -f $file ]] || { echo "no such file $path" >"$OUT"; return 1; }
      cat -- "$file" >"$OUT" ;;
    write_file)
      jq -e '.content | strings' <<<"$input" >/dev/null || { echo "missing argument content" >"$OUT"; return 1; }
      if [[ ${AUTO_APPROVE:-} != 1 ]]; then
        read -r -p "  Разрешить write_file $path? [y/N] " ans
        [[ ${ans,,} == y ]] || { echo "user denied the write" >"$OUT"; return 1; }
      fi
      if ! mkdir -p -- "$(dirname -- "$file")" || ! jq -j '.content' <<<"$input" >"$file"; then
        echo "cannot write $path" >"$OUT"
        return 1
      fi
      echo "ok: wrote $(jq '.content | length' <<<"$input") chars to $path" >"$OUT" ;;
  esac
}

create() {  # отправить историю, напечатать ответ модели (JSON)
  jq -n --slurpfile m "$HIST" --argjson tools "$TOOLS" --rawfile system "$WORK/system.txt" \
    --arg model "$MODEL" --arg effort "$EFFORT" \
    '{model: $model, max_tokens: 16000, system: $system, tools: $tools, messages: $m[0],
      output_config: {effort: $effort},
      fallbacks: "default"}' >"$REQ"  # при отказе модели API сам повторит запрос на запасной
  curl -sS --fail-with-body "$BASE_URL/v1/messages" \
    -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: server-side-fallback-2026-07-01" -H "content-type: application/json" \
    --data-binary @"$REQ"
}

echo "Харнесс: $MODEL (effort $EFFORT), папка $ROOT. Пустая строка — выход."
while IFS= read -r -p "> " task && [[ -n $task ]]; do
  turn_start=$(jq length "$HIST")
  jq -n --arg t "$task" '{role: "user", content: $t}' | push
  for ((step = 1; step <= MAX_STEPS; step++)); do  # агентный цикл
    resp=$(create) || { echo "ошибка запроса к API: $resp" >&2; exit 1; }
    stop=$(jq -r '.stop_reason' <<<"$resp")
    if [[ $stop == refusal ]]; then
      jq -r '"Модель отказалась (категория: \(.stop_details.category // "—")): \(.stop_details.explanation // "")"' <<<"$resp"
      jq --argjson n "$turn_start" '.[:$n]' "$HIST" >"$HIST.new" && mv "$HIST.new" "$HIST"  # ход откатывается
      break
    fi
    jq -c '{role: "assistant", content: .content}' <<<"$resp" | push  # целиком: thinking с подписью, tool_use
    if [[ $stop != tool_use || $(jq '[.content[] | select(.type == "tool_use")] | length' <<<"$resp") == 0 ]]; then
      jq -r '[.content[] | select(.type == "text") | .text] | join("")' <<<"$resp"
      if [[ $stop == max_tokens ]]; then echo "(ответ обрезан по max_tokens)"; fi
      break
    fi
    : >"$RESULTS"
    while IFS= read -r call <&3; do  # вызовы — из fd 3, stdin свободен для подтверждений
      name=$(jq -r '.name' <<<"$call")
      input=$(jq -c '.input' <<<"$call")
      echo "  [шаг $step] $name $input" >&2
      if run_tool "$name" "$input"; then is_error=false; else is_error=true; fi
      jq -n --arg id "$(jq -r '.id' <<<"$call")" --rawfile r "$OUT" --argjson max "$MAX_OUTPUT" --argjson err "$is_error" \
        '{type: "tool_result", tool_use_id: $id, is_error: $err,
          content: ($r | if length > $max then .[:$max] + "\n[...truncated \(length - $max) chars]" else . end)}' >>"$RESULTS"
    done 3< <(jq -c '.content[] | select(.type == "tool_use")' <<<"$resp")
    jq -s '{role: "user", content: .}' "$RESULTS" | push  # все результаты шага — одним сообщением
  done
  if ((step > MAX_STEPS)); then echo "Остановлено: больше $MAX_STEPS шагов."; fi
done
```

</details>

## 🧰 Без ручного цикла

Ручной цикл здесь нужен, чтобы видеть устройство харнесса. В работе его обычно не пишут:

| Что | Где | Что даёт |
| :--- | :--- | :--- |
| **Tool Runner** (бета) | Python `client.beta.messages.tool_runner` + `@beta_tool`, TS `client.beta.messages.toolRunner`, Java `client.beta().messages().toolRunner(...)`, Go `client.Beta.Messages.NewToolRunner(...)` | SDK сам крутит цикл над вашими функциями. Подтверждения и логирование остаются: решение принимается внутри функции инструмента или перед её запуском |
| **Claude Agent SDK** | Python, TypeScript | харнесс Claude Code целиком в виде библиотеки: Read/Edit/Bash, хуки, субагенты, сессии |
| **Managed Agents** (бета) | API Anthropic | харнесс и песочницу держит Anthropic, вы присылаете задачи и результаты своих инструментов |

## ✅ Как проверено

Тестовый сервер изображает `/v1/messages` и проверяет каждый запрос:

- есть ключ (`x-api-key` или `Authorization: Bearer`), `anthropic-version` и бета-заголовок `server-side-fallback-2026-07-01`;
- в теле `model: claude-opus-5-5` (по умолчанию), `fallbacks: "default"`, `output_config.effort: medium`, `max_tokens`, системный промпт с текстом из `AGENTS.md`, три инструмента с `input_schema`;
- **блок `thinking` с подписью** из первого ответа возвращается во втором запросе без изменений;
- четыре вызова первого шага (список файлов, `../secret.txt`, несуществующий инструмент, вызов без `path`) возвращаются **одним** сообщением, последние три — с `is_error: true`;
- дальше запись с подтверждением, обрезка файла на 30 000 символов, чтение обратно и финальный ответ.

Каждая версия прошла три прогона: с `AUTO_APPROVE=1`, с ответом `y` и сценарий **отказа** (`stop_reason: refusal`, категория `cyber`: харнесс должен напечатать её и спокойно ждать следующую задачу). Итого 6 × 3 = **18 прогонов**, все прошли. Для Rust и Bash отдельно проверено, что ответ API 400 показывает текст ошибки. Окружение: JDK 25 (`--release 21`), Python 3.14, Node 26, Go 1.27, Rust 1.98 (clippy без замечаний), bash 5.3 + jq 1.8 (shellcheck без замечаний).

<details><summary>🧪 Тестовый сервер mock_claude.py</summary>

Запуск: `python3 mock_claude.py 8765 agent ./work result.json` (или `refusal`), затем харнесс с `ANTHROPIC_BASE_URL=http://127.0.0.1:8765 ANTHROPIC_API_KEY=test-key WORKDIR=./work`. В `./work` должны лежать `AGENTS.md` со строкой `ALWAYS-ANSWER-IN-RUSSIAN` и `big.log` на 30 000 символов.

```python
#!/usr/bin/env python3
"""Тестовый сервер, изображающий Anthropic Messages API (/v1/messages) по сценарию.

Запуск: mock_claude.py PORT SCENARIO WORKDIR RESULT_JSON   (SCENARIO: agent | refusal)
"""
import json, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT, SCENARIO, WORKDIR, RESULT = int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
state = {"fails": [], "steps": []}


def check(cond, msg):
    if not cond:
        state["fails"].append(msg)


def tool_use(cid, name, args):
    return {"type": "tool_use", "id": cid, "name": name, "input": args}


def text_of(content):  # content результата — строка или список текстовых блоков
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content or [])


def results(msg):
    out = {}
    for b in msg.get("content", []) if isinstance(msg.get("content"), list) else []:
        if b.get("type") == "tool_result":
            out[b["tool_use_id"]] = (text_of(b.get("content")), bool(b.get("is_error")))
    return out


def reply(content, stop, details=None):
    return {"id": f"msg_{len(state['steps'])}", "type": "message", "role": "assistant", "model": "claude-opus-5-5",
            "content": content, "stop_reason": stop, "stop_sequence": None, "stop_details": details,
            "usage": {"input_tokens": 100, "output_tokens": 20}}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        check(self.path.split("?")[0] == "/v1/messages", f"path {self.path}")
        # SDK с версией API 2026-10-21 шлют ключ как Authorization: Bearer, curl-примеры — как x-api-key
        check(self.headers.get("x-api-key") == "test-key" or self.headers.get("authorization") == "Bearer test-key",
              "no API key")
        check(bool(self.headers.get("anthropic-version")), "no anthropic-version header")
        check("server-side-fallback-2026-07-01" in (self.headers.get("anthropic-beta") or ""),
              f"anthropic-beta {self.headers.get('anthropic-beta')}")
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        check(body.get("model") == "claude-opus-5-5", f"model {body.get('model')}")
        check(body.get("fallbacks") == "default", f"fallbacks {body.get('fallbacks')}")
        check((body.get("output_config") or {}).get("effort") == "medium", f"output_config {body.get('output_config')}")
        check(body.get("max_tokens", 0) >= 1000, f"max_tokens {body.get('max_tokens')}")
        check("ALWAYS-ANSWER-IN-RUSSIAN" in text_of(body.get("system")), "AGENTS.md not in system")
        names = sorted(t["name"] for t in body.get("tools", []))
        check(names == ["list_files", "read_file", "write_file"], f"tools {names}")
        check(all(t.get("input_schema", {}).get("type") == "object" for t in body.get("tools", [])), "input_schema")
        msgs = body["messages"]
        k = sum(1 for m in msgs if m["role"] == "assistant")
        state["steps"].append(k)
        if SCENARIO == "refusal":
            out = reply([], "refusal", {"type": "refusal", "category": "cyber",
                                        "explanation": "Запрос похож на разработку вредоноса."})
        elif k == 0:
            out = reply([{"type": "thinking", "thinking": "", "signature": "sig-1"},
                         {"type": "text", "text": "Смотрю, что в папке."},
                         tool_use("c1", "list_files", {"path": "."}),
                         tool_use("c2", "read_file", {"path": "../secret.txt"}),
                         tool_use("c3", "delete_all", {}),
                         tool_use("c4", "read_file", {})], "tool_use")
        elif k == 1:
            prev = msgs[-2]["content"]
            check(isinstance(prev, list) and prev[0].get("type") == "thinking" and prev[0].get("signature") == "sig-1",
                  f"thinking block not echoed back unchanged: {str(prev)[:200]}")
            check([b.get("id") for b in prev if b.get("type") == "tool_use"] == ["c1", "c2", "c3", "c4"], "tool_use ids")
            r = results(msgs[-1])
            check(list(r) == ["c1", "c2", "c3", "c4"], f"tool_results must come in one user message: {list(r)}")
            c1 = r.get("c1", ("", True))
            check("AGENTS.md" in c1[0] and "big.log" in c1[0] and not c1[1], f"c1 {c1}")
            for cid in ("c2", "c3", "c4"):
                check(r.get(cid, ("", False))[1], f"{cid} must have is_error: {r.get(cid)}")
            out = reply([tool_use("c5", "write_file", {"path": "bot/main.py", "content": "print('привет')\n"}),
                         tool_use("c6", "read_file", {"path": "big.log"})], "tool_use")
        elif k == 2:
            p = os.path.join(WORKDIR, "bot", "main.py")
            check(os.path.exists(p) and open(p, encoding="utf-8").read() == "print('привет')\n", "c5 file")
            r = results(msgs[-1])
            check(r.get("c5", ("", True))[0].startswith("ok"), f"c5 {r.get('c5')}")
            big = r.get("c6", ("", True))[0]
            check(10000 <= len(big) <= 10100 and "truncated" in big, f"c6 len={len(big)}")
            out = reply([tool_use("c7", "read_file", {"path": "bot/main.py"})], "tool_use")
        elif k == 3:
            r = results(msgs[-1])
            check(r.get("c7", ("", True)) == ("print('привет')\n", False), f"c7 {r.get('c7')}")
            out = reply([{"type": "text", "text": "Готово: бот создан в bot/main.py."}], "end_turn")
        else:
            check(False, f"unexpected step {k}")
            out = reply([{"type": "text", "text": "?"}], "end_turn")
        data = json.dumps(out, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        json.dump(state, open(RESULT, "w"), ensure_ascii=False)


HTTPServer(("127.0.0.1", PORT), H).serve_forever()
```

</details>

## 🖥️ По системам

| | Gentoo | Debian / Ubuntu | Arch | Entware (RT-AX56U) |
| :--- | :--- | :--- | :--- | :--- |
| **Java 21+ + Maven** | `emerge dev-java/openjdk:21 dev-java/maven-bin` | `apt install openjdk-21-jdk maven` | `pacman -S jdk21-openjdk maven` | ❌ |
| **Python 3.10+** | есть; SDK — в venv | `apt install python3-venv` | `pacman -S python` | SDK тянет нативный `pydantic-core` — на armv7 не проверялось |
| **Node.js 20+** | `emerge net-libs/nodejs` | Debian 13 — 20.x; Ubuntu 24.04 — 18.x, нужен NodeSource или nvm | `pacman -S nodejs npm` | ❌ в Entware Node 18, SDK требует 20+ |
| **Go 1.25+** | `emerge dev-lang/go` | в Debian 13 — 1.24, нужен архив с [go.dev](https://go.dev/dl/); в Ubuntu проверьте `go version` | `pacman -S go` | собрать на ПК: `GOOS=linux GOARCH=arm GOARM=7 CGO_ENABLED=0 go build -ldflags="-s -w"` |
| **Rust 1.88+** | `emerge dev-lang/rust` | через rustup | `pacman -S rust` | кросс-сборка, не проверялась |
| **Bash + curl + jq** | `emerge app-misc/jq` | `apt install curl jq` | `pacman -S curl jq` | ✅ `opkg install bash curl jq` |

На роутере проще всего Bash-версия: ей нужны только curl и jq, а Claude API доступен по HTTPS напрямую.

## 🔗 Ссылки

- Документация Anthropic: [tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · [отказы и fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback) · [цены](https://platform.claude.com/docs/en/about-claude/pricing) · [правила аутентификации Claude Code](https://code.claude.com/docs/en/legal-and-compliance)
- SDK: [Java](https://github.com/anthropics/anthropic-sdk-java) · [Python](https://github.com/anthropics/anthropic-sdk-python) · [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript) · [Go](https://github.com/anthropics/anthropic-sdk-go)
- В хранилище: [ИИ-агент vs харнесс (OpenAI-совместимая версия и разбор подписок)](../../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md) · [Prompt injection в ИИ-агентах](../../../Security/Prompt%20injection%20%D0%B2%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%B0%D1%85%20%E2%80%94%20%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0%20%D0%B2%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%D0%B5%2C%20%D0%B0%20%D0%BD%D0%B5%20%D0%B2%20%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D0%B5%20%28taint-%D0%BE%D1%82%D1%81%D0%BB%D0%B5%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20%D1%81%D0%BC%D0%B5%D1%80%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D1%82%D1%80%D0%B8%D0%B0%D0%B4%D0%B0%2C%20%D0%BF%D0%BE%D0%B4%D1%82%D0%B2%D0%B5%D1%80%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F%3B%20%D0%BA%D0%BE%D0%B4%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%29.md) · [RLM на практике](RLM%20%D0%BD%D0%B0%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B5%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20Recursive%20Language%20Model%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%20%D0%B2%20REPL%2C%20%D1%80%D0%B5%D0%BA%D1%83%D1%80%D1%81%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20llm_query%3B%20exec%2C%20vm%2C%20JShell%2C%20yaegi%2C%20Rhai%2C%20bash%3B%20%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D0%B0%29.md) · [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [Claude Code — кэш промптов](../Claude%20Code%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D0%BE%D0%B2%20%28TTL%205%20%D0%BC%D0%B8%D0%BD%D1%83%D1%82%20%D0%B8%201%20%D1%87%D0%B0%D1%81%2C%20subagentPromptCacheTtl%2C%20%D1%87%D1%82%D0%BE%20%D1%81%D0%B1%D1%80%D0%B0%D1%81%D1%8B%D0%B2%D0%B0%D0%B5%D1%82%20%D0%BA%D1%8D%D1%88%29.md) · [Daily brief на Managed Agents](../../Automations/Daily%20brief%20%28Anthropic%29%20%E2%80%94%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%BF%D0%BE%20%D1%80%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D1%8E%20%D0%BD%D0%B0%20Claude%20Managed%20Agents%20%28Slack%20%D0%B8%20GitHub%2C%20%D0%B7%D0%B0%D0%BA%D0%BB%D0%B0%D0%B4%D0%BA%D0%B8%2C%20%D0%B6%D1%83%D1%80%D0%BD%D0%B0%D0%BB%20%D0%BE%D1%82%D1%87%D1%91%D1%82%D0%BE%D0%B2%2C%20%D0%B1%D1%8E%D0%B4%D0%B6%D0%B5%D1%82%20%D0%BD%D0%B0%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%29.md)

#AI #Агенты #Harness #Claude #Anthropic #Java #Python #JavaScript #Go #Rust #Bash
