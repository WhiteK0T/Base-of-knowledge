---
создал заметку: 2026-11-08T11:25:00
author: WhiteK0T
tags:
  - AI
  - ClaudeCode
  - Плагин
  - Хуки
  - Настройки
  - claude-code-templates
Источник:
  - https://t.me/bugnotfeature/28599
  - https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/mods/productivity/ultra-config
  - https://www.aitmpl.com/mods
  - https://www.npmjs.com/package/claude-code-templates
  - https://code.claude.com/docs/en/plugins/mods/overview
  - https://code.claude.com/docs/en/settings-reference.md
  - https://code.claude.com/docs/en/permissions.md
  - https://code.claude.com/docs/en/model-config.md
---

# Ultra Config — пять профилей настроек Claude Code в одной панели

**Ultra Config** — мод для Claude Code из каталога [claude-code-templates](https://github.com/davila7/claude-code-templates) ([aitmpl.com](https://www.aitmpl.com/mods), ~33 тыс. звёзд). Мод — это плагин, поведение которого написано функциями-хуками на TypeScript. Он работает внутри Claude Code и умеет рисовать интерфейс.

Ultra Config добавляет команду `/ultra-config`. Она открывает боковую панель с пятью профилями: у каждого видно, что именно изменится, есть кнопка *Activate* и откат. Заметка по посту [«Не баг, а фича»](https://t.me/bugnotfeature/28599) от 24 октября 2026 года, сверена с исходниками мода и с документацией Claude Code.

| | |
| :--- | :--- |
| Версия мода | 0.2.1 (в каталоге на 8 ноября 2026), MIT |
| Нужно | Claude Code **2.1.287+** — в нём моды включены по умолчанию |
| Установщик | npm-пакет `claude-code-templates` 1.32.2 (MIT, ~5 тыс. загрузок в неделю) |
| Куда ставится | `.claude/skills/ultra-config/` **текущего каталога**; Claude Code подхватывает его как `ultra-config@skills-dir`, когда папке доверяют |
| Куда пишет | строки меню `/config` — через API движка, как будто их поменяли руками; остальное — в `~/.claude/settings.json`, перед этим копия в `settings.json.ultra-config.bak` |

## 1. Установка

Нужен Node.js с `npx`:

| Система | Команда |
| :--- | :--- |
| Gentoo | `emerge --ask net-libs/nodejs` (с USE `npm`, он включён по умолчанию) |
| Debian / Ubuntu | `sudo apt install nodejs npm` |
| Arch | `sudo pacman -S nodejs npm` |
| Entware | неприменимо: Claude Code на роутере не запускают |

```bash
cd ~/my-project
CCT_NO_TRACKING=true npx claude-code-templates@latest --mod productivity/ultra-config
claude            # согласиться доверять папке, затем /ultra-config
```

- **Мод ставится в проект.** Он ложится в `./.claude/skills/ultra-config/` каталога, из которого запущена команда. Другой каталог задаётся через `-d <каталог>`.
- **Версия не закреплена.** Установщик скачивает файлы мода с ветки `main` на GitHub в момент установки. Это код, который выполняется внутри Claude Code и читает и пишет файлы настроек, так что перед первым запуском его стоит просмотреть: `hooks/profiles.ts` и `hooks/register.tsx`, около 900 строк.
- **Аналитика.** Установщик отправляет на `aitmpl.com` тип и имя компонента, относительный путь установки и версию CLI. Отключается переменной `CCT_NO_TRACKING=true` или `CCT_NO_ANALYTICS=true`.
- Подключить мод на одну сессию: `claude --plugin-dir .claude/skills/ultra-config`.

## 2. Что меняет каждый профиль

По `hooks/profiles.ts`. Строки `/config` пишутся как из меню, остальные ключи — в `~/.claude/settings.json`.

| Профиль | Что ставит |
| :--- | :--- |
| **Token saver** | модель `sonnet`; усилие `low`; субагенты на `haiku` (`env.CLAUDE_CODE_SUBAGENT_MODEL`); быстрый режим выключен — он тарифицируется дороже; стиль ответов `Concise`; без подсказок следующего промпта и без recap, потому что каждое — лишний вызов модели; автосжатие контекста включено; маленькие мультиагентные workflow, без запуска по ключевому слову; ответы MCP урезаны до 10 000 токенов (`env.MAX_MCP_OUTPUT_TOKENS`, по умолчанию 25 000) |
| **Fast flow** | модель `sonnet`; усилие `medium`; режим разрешений `acceptEdits` — правки файлов без вопросов; стиль `Concise`; подсказки промпта по Tab; длительность хода и прогресс во вкладке терминала; workflow среднего размера |
| **Max quality** | самая сильная доступная модель (`best`); усилие `xhigh`; субагенты снова на той модели, которую просят (переменная удаляется); стиль по умолчанию; workflow включены, большие, слово `ultracode` их запускает; чекпоинты для отката правок; автосжатие |
| **Guarded** | ручной режим (`default`) — каждая правка и команда спрашивают; план не выполняется сам; запрет режима `bypassPermissions` (`permissions.disableBypassPermissionsMode`); правила deny `Read(./.env)`, `Read(./.env.*)`, `Read(./secrets/**)`, `Read(~/.ssh/**)`, `Read(~/.aws/**)`; чекпоинты; подробный вывод вызовов инструментов; без workflow по ключевому слову |
| **Autopilot** | режим `auto` — безопасные действия одобряет классификатор; план выполняется без остановок; усилие `high`; workflow включены; recap к возвращению; push-уведомления, когда Claude сочтёт нужным и когда ждёт ответа; автосжатие |

Перед активацией панель показывает каждую строку: было, станет и почему. Строки, запрещённые политикой организации или неизвестные этой версии Claude Code, помечаются и пропускаются.

### Уточнения к посту

- **«Max quality — максимальный уровень усилий».** Профиль ставит `xhigh`, а выше есть ещё `max`. У Fable 5.x, Opus/Sonnet/Haiku 5.5, Opus 5 и Opus 4.7–4.8 уровни идут `low`–`xhigh`–`max`. На моделях без `xhigh` (Opus 4.6, Sonnet 4.6) Claude Code опускает его до `high`.
- **«Guarded — защита от обхода лимитов».** Речь о запрете режима `bypassPermissions`, то есть обхода разрешений; лимиты тут ни при чём. Правила `Read(...)` закрывают встроенные файловые инструменты: Read, по возможности Grep и Glob, `@`-упоминания. Команду `cat .env` через shell они не блокируют, но в ручном режиме её всё равно придётся подтвердить.
- **«Autopilot — push-уведомления».** Уведомления приходят на телефон через [Remote Control](https://code.claude.com/docs/en/remote-control.md#mobile-push-notifications), в локальной сессии — пока он подключён. Режим `auto` с версии 2.1.283 и так стартовый для терминала и VS Code. Если он недоступен сессии, Claude Code запускается в ручном режиме.
- **Усилие сохраняется для конкретной модели.** С версии 2.1.251 оно хранится в `modelSettings.<модель>.effortLevel`. Мод записывает его при следующем сообщении, когда становится известна модель.

## 3. Профили складываются, а не заменяют друг друга

- **Эффект глобальный.** Мод установлен в проект, но пишет в пользовательские настройки. Включённый профиль действует во всех проектах и сессиях.
- **Каждый профиль меняет только свои ключи.** Переключение не возвращает остальное к исходному. Пример: Token saver → Fast flow. Субагенты останутся на `haiku`, лимит MCP — 10 000, recap — выключен: Fast flow этих ключей не касается. После Guarded правила deny и запрет `bypassPermissions` остаются при любом следующем профиле.
- **Перед переключением лучше откатить предыдущий профиль.** Панель показывает, какая доля профиля уже действует.

```text
/ultra-config                   открыть панель
/ultra-config <профиль>         открыть профиль: saver, flow, quality, guarded, autopilot
/ultra-config apply <профиль>   включить без панели
/ultra-config undo              откатить последнее включение (история — 20 шагов)
/ultra-config close             закрыть панель
```

- `undo` возвращает и строки `/config`, и ключи `settings.json` — даже те, что вы поменяли с тех пор.
- Копия `~/.claude/settings.json.ultra-config.bak` одна и перезаписывается при каждом включении.
- Удаление мода — это удаление каталога `.claude/skills/ultra-config/`. Настройки, которые он поменял, при этом останутся, поэтому сначала `undo`.

## 4. То же без мода: профили через `--settings`

Штатный флаг `--settings` загружает дополнительный файл настроек **только на эту сессию**, поверх обычных `settings.json`. Ключи, которых в файле нет, берутся как обычно. Профили получаются без правки глобальных настроек и без стороннего кода:

`~/.claude/profiles/saver.json`:

```json
{
  "model": "sonnet",
  "outputStyle": "Concise",
  "env": {
    "CLAUDE_CODE_SUBAGENT_MODEL": "haiku",
    "MAX_MCP_OUTPUT_TOKENS": "10000"
  }
}
```

`~/.claude/profiles/guarded.json`:

```json
{
  "permissions": {
    "defaultMode": "default",
    "disableBypassPermissionsMode": "disable",
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)", "Read(~/.ssh/**)", "Read(~/.aws/**)"]
  }
}
```

```bash
alias claude-saver='claude --settings ~/.claude/profiles/saver.json --effort low'
alias claude-flow='claude --model sonnet --effort medium --permission-mode acceptEdits'
alias claude-max='claude --effort xhigh'
alias claude-guarded='claude --settings ~/.claude/profiles/guarded.json'
```

Разница с модом:
- у мода — панель с наглядным «было → станет», переключение посреди сессии и откат;
- у алиасов — профиль живёт ровно одну сессию и ничего не оставляет в `~/.claude/settings.json`.

## Связанные заметки

- [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) — настройки, режимы разрешений, плагины
- [Claude Code — шпаргалка команд](../Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) — `/model`, `/effort`, `/config` и флаги запуска
- [Claude Code — кэш промптов](../Claude%20Code%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D0%BE%D0%B2%20%28TTL%205%20%D0%BC%D0%B8%D0%BD%D1%83%D1%82%20%D0%B8%201%20%D1%87%D0%B0%D1%81%2C%20subagentPromptCacheTtl%2C%20%D1%87%D1%82%D0%BE%20%D1%81%D0%B1%D1%80%D0%B0%D1%81%D1%8B%D0%B2%D0%B0%D0%B5%D1%82%20%D0%BA%D1%8D%D1%88%29.md) — ещё один рычаг экономии токенов, кроме смены модели
- [Portal и Shunt (Spotify) — плагины Claude Code для экономии токенов](Portal%20%D0%B8%20Shunt%20%28Spotify%29%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%D1%8B%20Claude%20Code%20%D0%B4%D0%BB%D1%8F%20%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D0%B8%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%2890%25%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B4%D0%B0%2C%20%D0%BD%D0%BE%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20Spotify%20Portal%2C%20%D0%B0%20Gemini%20%D1%82%D0%B0%D0%BC%20%D0%BD%D0%B5%D1%82%29.md)
- [workout-gate — плагин Claude Code на хуках](workout-gate%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20Claude%20Code%2C%20%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D1%83%D1%8E%D1%89%D0%B8%D0%B9%20%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%20%D0%B4%D0%BE%20%D0%BE%D1%82%D0%B6%D0%B8%D0%BC%D0%B0%D0%BD%D0%B8%D0%B9%20%28%D0%B2%D0%B5%D0%B1%D0%BA%D0%B0%29.md) — другой пример того, что умеют хуки

## 🔗 Ссылки

- Пост: https://t.me/bugnotfeature/28599
- Исходники мода: https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/mods/productivity/ultra-config
- Каталог модов: https://www.aitmpl.com/mods
- npm `claude-code-templates`: https://www.npmjs.com/package/claude-code-templates
- Моды в Claude Code: https://code.claude.com/docs/en/plugins/mods/overview
- Справочник настроек: https://code.claude.com/docs/en/settings-reference.md
- Правила разрешений: https://code.claude.com/docs/en/permissions.md
- Уровни усилия: https://code.claude.com/docs/en/model-config.md

#AI #ClaudeCode #Плагин #Хуки #Настройки #claude-code-templates
