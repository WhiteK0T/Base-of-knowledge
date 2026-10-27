---
создал заметку: 2026-09-09T10:30:00
обновлено: 2026-10-27T19:30:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - DeepSeek
  - Плагины
  - Безопасность
  - TypeScript
Источник:
  - https://t.me/bugnotfeature/27114
  - https://github.com/deepseek-ai/deepseek-harness
  - https://deepseek-harness.github.io/deepseek-harness/
  - https://github.com/cordiverse/cordis
  - https://arxiv.org/abs/2608.25512
---

# 🔌 DeepSeek Harness (dsh) — агентская среда «всё есть плагин»

**DeepSeek Harness** (`dsh`) — открытая агентская среда (harness) от DeepSeek AI. В ней всё — плагин: инструменты агента, адаптеры моделей, сессии, скиллы, песочницы, планировщик и сам интерфейс подключаются модулями на фреймворке [Cordis](https://github.com/cordiverse/cordis). Работать с ней можно через веб-интерфейс, терминал, ACP/SDK или в headless-режиме. Модели — DeepSeek по ключу API, сторонние провайдеры или любой OpenAI/Anthropic-совместимый эндпоинт. Статус — **developer preview**.

Заметка по [посту «Не баг, а фича» от 17.08.2026](https://t.me/bugnotfeature/27114). Данные сверены 27.10.2026 по GitHub API, npm и документации проекта (первая версия заметки — 09.09.2026).

> [!info] Коротко
> | | |
> | :--- | :--- |
> | Репозиторий | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness), создан **13.08.2026** |
> | Звёзд / форков | **263 506** · 31 868 |
> | Лицензия / язык | **MIT** · TypeScript |
> | npm | [`@deepseek-ai/dsh`](https://www.npmjs.com/package/@deepseek-ai/dsh): `latest` — **0.2.1-rc.2**, `next` — 0.2.1-rc.4 (26.10.2026); 38 версий, стабильной пока нет |
> | Релизы на GitHub | с 17.10.2026, пререлизы `dsh-v0.2.1-rc.1` … `rc.3` |
> | Ядро | Cordis — копия в `vendor/` под именем `@deepseek-ai/cordis` (апстрим [cordiverse/cordis](https://github.com/cordiverse/cordis), 9 428★) |
> | Node.js | **≥ 24.9**; для сборки из исходников — pnpm |
> | Обратная связь | issues отключены; [Discussions](https://github.com/deepseek-ai/deepseek-harness/discussions) и Discord |

## 🧩 Как устроено

Среда — это набор пакетов `@deepseek-ai/dsh-*`, а пакет CLI собирает их вместе. По его зависимостям видно, из чего состоит агент «из коробки»:

| Группа | Пакеты (примеры) |
| :--- | :--- |
| Инструменты | `dsh-tool-bash`, `dsh-tool-pwsh`, `dsh-tool-fs`, `dsh-tool-web`, `dsh-tool-todo`, `dsh-tool-jobs`, `dsh-tool-skill` |
| Режимы и поведение | `dsh-plan-mode`, `dsh-goal`, `dsh-persona`, `dsh-agent-preset`, `dsh-schedule` |
| Интеграции | `dsh-mcp-client`, `dsh-http-proxy`, `dsh-token-meter` |
| Интерфейсы | `dsh-web-app`, `dsh-terminal`, `dsh-headless`, `dsh-acp-app`, `dsh-sdk-app` |
| Изоляция и окружение | `dsh-pwsh-sandbox`, `dsh-fs-local`, `dsh-jobs-local` |

Встроенные модули устроены так же, как сторонние, поэтому любой из них можно отключить или заменить своим.

**Профиль** — каталог `$DSH_HOME/profiles/<имя>/`. В нём лежат `package.json` со списком подключённых бандлов и `cordis.patch.yml` — пользовательский слой настроек поверх них. Плагин `dsh-hmr` следит за этими файлами и пересобирает дерево плагинов на лету; без него изменения применяются после перезапуска.

### Cordis

[Cordis](https://github.com/cordiverse/cordis) («Meta-Framework of Spatiotemporal Composability») — фреймворк плагинов с жизненным циклом, сервисами, событиями и детерминированной очисткой. Плагин можно загрузить, выгрузить или перезагрузить на ходу, и всё, что он создал, уберётся вместе с ним.

- Проект существует с 2022 года в организации `cordiverse`. Основной автор — **Shigma** (569 коммитов), сейчас в его профиле GitHub указано `@deepseek-ai`.
- Модель описана в статье [*A Programming Paradigm for Spatiotemporal Composability*](https://arxiv.org/abs/2608.25512) (arXiv, 26.08.2026; Yifan Shi, Wei Zhang, Tianyi Cui). Tianyi Cui (`@deepseek-ai`) — главный контрибьютор самого Harness, около 7 тыс. коммитов.
- Harness не тянет Cordis из npm, а держит его исходники в [`vendor/`](https://github.com/deepseek-ai/deepseek-harness/blob/master/vendor/README.md) под скоупом `@deepseek-ai` — по словам авторов, «чтобы полностью владеть слоем фреймворка»: проверять, патчить, закреплять версии. Все отличия от апстрима перечислены там же — сейчас это 21 правка (жизненный цикл, загрузка конфигов, HMR, Windows).
- Есть и отдельная реализация той же модели на Rust — [`dshbox/cordis-rs`](https://github.com/dshbox/cordis-rs) (65★).

## ⚠️ Статус: developer preview

README предупреждает капсом — **«THERE WILL BE COMPATIBILITY-BREAKING CHANGES»** — и просит перед запуском прочитать [SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md). Главное оттуда:

> *«DeepSeek Harness is experimental developer-preview software. It has not undergone a security audit and must not be treated as secure or production-ready.»*
>
> *«The project can execute model-generated code and commands, load third-party plugins, and access the network, processes, credentials, and files made available to it.»*
>
> *«Sandboxing, approval prompts, and permission controls can reduce risk, but they do not guarantee isolation or prevent damage.»*

Рекомендации авторов: минимальные права; **одноразовая ВМ или контейнер**; бэкапы файлов, к которым у среды есть доступ; не давать ей чувствительные ключи и данные; проверять плагины, конфиги и предлагаемые команды до запуска.

Совместимость плагинов среда проверяет сама. При установке и старте профиля диапазон `engines.dsh` плагина сверяется с версией `dsh --version`, и несовместимый плагин запустится только с явным исключением на конкретную версию.

## 💻 Установка

> [!tip] Самый короткий путь
> ```sh
> npx @deepseek-ai/dsh web
> ```
> Нужен только Node.js. Команда поднимает веб-интерфейс на `http://127.0.0.1:3080` и открывает браузер. Флаг `--no-open` — не открывать браузер, `--port` — другой порт.

Сборка из исходников нужна для разработки плагинов. В посте этот блок свёрстан с переносами, здесь команды уже склеены:

```sh
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

| Система | Что нужно |
| :--- | :--- |
| **Gentoo** (основная) | `emerge --ask net-libs/nodejs` — подходят стабильные 24.22 и 26.12, `npm` включён USE-флагом по умолчанию. pnpm для сборки — `npm i -g pnpm`. На ветке 24 есть ещё USE `corepack` (`corepack enable pnpm`), в Node 25+ corepack из комплекта убрали |
| **Debian / Ubuntu** | штатный `nodejs` обычно старее 24.9 (в Debian 13 — 20.x), поэтому Node 24 из [NodeSource](https://github.com/nodesource/distributions) или через `nvm install 24`; pnpm — `npm i -g pnpm` |
| **Arch** | `sudo pacman -S nodejs npm pnpm` — в `extra` свежие версии |
| **Entware / RT-AX56U** | ❌ не подойдёт: в репозитории `armv7sf-k3.2` Node.js **18.20**, а нужен ≥ 24.9, да и 512 МБ ОЗУ мало. Запускать на ПК или VPS |

### На сервере и в контейнере

При запуске по SSH `dsh` не открывает браузер, а только печатает адрес с токеном входа. Порт пробрасывается обычным туннелем:

```sh
ssh -L 3080:127.0.0.1:3080 user@vps       # на своей машине
npx @deepseek-ai/dsh web --no-open        # на сервере, в каталоге проекта
```

Напечатанный адрес открывается в локальном браузере. Для постоянной публикации за reverse proxy есть флаги `--public-url` и `--trusted-host` ([гайд](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/public-deployments.md)).

Веб-сервер слушает только loopback, поэтому в контейнере проще всего общая сеть с хостом. Файловая изоляция при этом остаётся: среда видит только каталог проекта, без домашнего каталога и ключей.

```sh
podman run --rm -it --network host \
  -v "$PWD":/work -w /work \
  -v dsh-home:/dsh -e DSH_HOME=/dsh \
  docker.io/library/node:24 npx -y @deepseek-ai/dsh web --no-open
```

С `docker run` флаги те же.

## 🔑 Модели

- **DeepSeek:** Settings → Models → ключ [DeepSeek API](https://platform.deepseek.com/). Список моделей подтягивается из API DeepSeek и обновляется сам.
- **Сторонние провайдеры:** Add model provider → провайдер из встроенного каталога (`anthropic`, `openai`, `moonshotai` для Kimi, `zai` для GLM и др.) и его ключ либо переменная окружения.
- **Свой эндпоинт** — шлюз, локальный сервер, корпоративный прокси: Custom model API → Provider ID, base URL и протокол (OpenAI Chat Completions, OpenAI Responses или Anthropic Messages). Fetch available models запрашивает список моделей у самого эндпоинта.

В интерфейсе ключи только на запись. Хранятся они в `$DSH_HOME/.credentials.yaml`, а страница получает лишь замаскированную метку. Тонкие настройки (reasoning, заголовки, таймауты, повторы) лежат в `$DSH_HOME/profiles/web/cordis.patch.yml` и применяются со следующего запроса, без перезапуска. Подробности — в [гайде по моделям](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md).

## 🖥️ Режимы запуска

| Команда | Что делает |
| :--- | :--- |
| `dsh web` | веб-интерфейс (профиль `web`) |
| `dsh --profile headless "задача"` | одна сессия без интерфейса: выполнить, напечатать ответ, выйти |
| `dsh --profile acp` | агент для ACP-клиентов (редакторов) через stdio |
| `dsh --profile sdk` | JSON-RPC для SDK, есть Python SDK |
| `dsh --profile tui` | терминальный интерфейс, если установлен профиль `tui` |
| `dsh plugin --profile <имя> <аргументы pnpm>` | управление плагинами профиля |

Каталог, из которого запущен `dsh`, — рабочий корень по умолчанию. В веб-интерфейсе рабочий каталог всё равно нужно выбрать явно (Choose workspace). Есть и десктопная сборка на Electron.

## 🔌 Плагины

### Установка

```sh
dsh plugin --profile web add dsh-plugin-reactive-resume
```

`dsh plugin` передаёт аргументы в `pnpm` в каталоге профиля, так что плагин — это обычный npm-пакет или Git-репозиторий. В веб-интерфейсе плагины включаются на странице **Plugins**.

Вкладка **Discover** (каталог с поиском и установкой после подтверждения) появляется, если включить экспериментальный бандл **Custom plugin indexes**. Своего каталога в комплекте нет. Индекс — это JSON-файл, URL которого добавляешь сам, и dsh проверяет только формат, а не описания и авторство. Источник пакета показывается в окне подтверждения, его и стоит проверять ([гайд по индексам](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/plugin-market.md)).

### Топик `dsh-plugin`

README предлагает авторам плагинов ставить на репозиторий топик [`dsh-plugin`](https://github.com/topics/dsh-plugin), чтобы их находили. «6000 готовых скиллов» из поста — это число репозиториев с этим тегом на момент публикации. Сейчас их **23 550**. Тег ставит сам владелец репозитория, поэтому счётчик показывает именно репозитории, а не плагины или скиллы.

Наверху по звёздам — крупные самостоятельные проекты, у которых интеграция с dsh — один из модулей:

| Звёзд | Репозиторий | Что там для dsh |
| ---: | :--- | :--- |
| 395 758 | `morluto/rea` | [REA](../../Security/Reverse-Engineering/AI/REA%20%E2%80%94%20Reverse%20Engineer%20Anything%20%28morluto%29%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B8%20CLI%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D0%B8%D0%BA%D0%B8%2C%20Electron%2C%20APK%2C%20.NET%2C%20%D1%81%D0%B0%D0%B9%D1%82%D1%8B%3B%20Hopper-Ghidra-IDA%29.md) — реверс для ИИ-агентов; с 12.10.2026 умеет прописать себя в профиль dsh |
| 263 507 | `deepseek-ai/deepseek-harness` | сам Harness |
| 104 337 | `nexu-io/open-design` | [Open Design](../Open%20Design%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%B0%20Claude%20Design%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%2B%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%29.md); умеет работать с dsh как с агентом |
| 90 286 | `tt-a1i/archify` | скилл интерактивных диаграмм; пакет `integrations/deepseek-harness` |
| 79 709 | `ruvnet/ruflo` | собственный мета-харнесс; плагин `ruflo-deepseek-harness` (с 21.08.2026) |
| 46 517 | `Ebony-Vinyl/dsh-our-free-model` | провайдер «бесплатных моделей» — см. ниже |
| 44 937 | `reactive-resume/reactive-resume` | конструктор резюме; плагин `dsh-plugin-reactive-resume` (с 18.08.2026) — читать и править резюме из сессии |
| 40 955 | `volcengine/OpenViking` | контекстная БД для агентов; гайд по подключению к dsh |

Попадаются и репозитории только с тегом — например, загрузчик картинок PicGo (27 424★), в котором нет ни одного файла для dsh.

Узкие теги: [`dsh-skill`](https://github.com/topics/dsh-skill) — **302** репозитория, `deepseek-harness` — 19 031. Курируемый список — [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) (21 102★, CC0). Есть и сторонние «маркеты»: [dsh-market](https://github.com/2BingLing/dsh-market) («6000+ плагинов» с оценками) и [awesome-deepseek-harness-plugins](https://github.com/imsai-sh/awesome-deepseek-harness-plugins) («11 000+»); эти цифры — их собственные.

> [!warning] У плагина права всей среды
> Плагину доступны те же файлы, сеть и ключи, что и самой dsh. Перед установкой стоит прочитать код, посмотреть, куда он ходит по сети, и закрепить версию.
>
> Наглядный пример — `dsh-our-free-model`: он обещает фронтирные модели «бесплатно, без ключа и регистрации». По его же README, бесплатные каналы идут через публичные шлюзы OpenCode Zen и Kilo AI, и upstream предупреждает, что промпты могут логироваться, — код с секретами туда отправлять не стоит. Ещё десять «аккаунт-каналов» (TRAE, Qoder, Cline, MiniMax Code и др.) работают через пулы аккаунтов с ежедневным сбором бонусов — это стоит сверить с условиями самих сервисов.

## 📈 Рост

Средняя скорость набора звёзд за всё время жизни репозитория:

| Репозиторий | Звёзд | Возраст | Звёзд в день |
| :--- | ---: | ---: | ---: |
| **deepseek-ai/deepseek-harness** | 263 506 | 75 дней | **3 513** |
| morluto/rea | 395 760 | 196 дней | 2 019 |
| github/spec-kit | 143 208 | 432 дня | 332 |
| ollama/ollama | 184 995 | 1 219 дней | 152 |

По средней скорости это по-прежнему рекорд, но основная волна пришла в первые недели. По посту — больше 130 тыс. звёзд за первые трое суток, 216 тыс. к 09.09, а с сентября — около **1 000 звёзд в день**. Звёзды измеряют внимание, а не зрелость: стабильной версии пока нет.

## 💡 Итог

- Официальная открытая (MIT) агентская среда DeepSeek, где каждый компонент — плагин на Cordis. Автор Cordis и соавтор статьи о нём работают в DeepSeek, а сам фреймворк вендорится в репозиторий со своими правками.
- Ставится одной командой `npx @deepseek-ai/dsh web` (Node.js ≥ 24.9). Работает с DeepSeek, сторонними провайдерами и любым OpenAI/Anthropic-совместимым эндпоинтом.
- Developer preview: без аудита безопасности, с ломающими изменениями, текущая версия — 0.2.1-rc. Запускать в контейнере или ВМ, без доступа к рабочим ключам.
- Экосистема большая, но тег `dsh-plugin` самоприсваиваемый: 23 550 репозиториев — не 23 550 плагинов. Ставить только прочитанное, индексы плагинов подключать только доверенные.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/27114](https://t.me/bugnotfeature/27114) (17.08.2026)
- Проект: [GitHub](https://github.com/deepseek-ai/deepseek-harness) · [документация](https://deepseek-harness.github.io/deepseek-harness/) · [SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md) · [npm `@deepseek-ai/dsh`](https://www.npmjs.com/package/@deepseek-ai/dsh) · [Discussions](https://github.com/deepseek-ai/deepseek-harness/discussions)
- Гайды: [модели и провайдеры](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md) · [индексы плагинов](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/plugin-market.md) · [режимы CLI](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md) · [публикация за reverse proxy](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/public-deployments.md) · [вендорный Cordis](https://github.com/deepseek-ai/deepseek-harness/blob/master/vendor/README.md)
- Ядро: [cordiverse/cordis](https://github.com/cordiverse/cordis) · [статья arXiv 2608.25512](https://arxiv.org/abs/2608.25512) · [dshbox/cordis-rs](https://github.com/dshbox/cordis-rs)
- Экосистема: [топик `dsh-plugin`](https://github.com/topics/dsh-plugin) (23 550) · [топик `dsh-skill`](https://github.com/topics/dsh-skill) (302) · [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin)
- Связанные: [Сводная таблица AI-агентов](%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%29.md) · [ИИ-агент vs харнесс](../../Education/Youtube/%D0%90%D1%80%D1%82%D1%91%D0%BC%20%D0%A8%D1%83%D0%BC%D0%B5%D0%B9%D0%BA%D0%BE/%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20vs%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%E2%80%94%20%D0%B2%20%D1%87%D1%91%D0%BC%20%D1%80%D0%B0%D0%B7%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%85%D0%B0%D1%80%D0%BD%D0%B5%D1%81%D1%81%20%D0%BD%D0%B0%206%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%D1%85%20%28LLM%2C%20tools%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D1%86%D0%B8%D0%BA%D0%BB%3B%20Agentic%20OS%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%2C%20RLM%2C%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%2C%20prompt%20injection%29.md) · [Kimi Code CLI](Kimi%20Code%20CLI%20%28MoonshotAI%29%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE-%D0%B2%D0%B2%D0%BE%D0%B4%2C%20%D1%81%D1%83%D0%B1%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20ACP%2C%20MCP%29%2C%20%D1%84%D0%B0%D0%BA%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D1%85%D0%B0%D0%B9%D0%BF%D0%B0%20%C2%AB%D0%BF%D0%BE%D1%85%D0%BE%D1%80%D0%BE%D0%BD%D0%B8%D0%BB%D0%B8%20Claude%20Code%C2%BB.md) · [Open Design](../Open%20Design%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%B0%20Claude%20Design%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%2B%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%29.md) · [REA](../../Security/Reverse-Engineering/AI/REA%20%E2%80%94%20Reverse%20Engineer%20Anything%20%28morluto%29%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B8%20CLI%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D0%B8%D0%BA%D0%B8%2C%20Electron%2C%20APK%2C%20.NET%2C%20%D1%81%D0%B0%D0%B9%D1%82%D1%8B%3B%20Hopper-Ghidra-IDA%29.md) · [Skills Hub](../Skills/Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md) · [MCP — серверы Model Context Protocol](Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md)

#AI #Агенты #DeepSeek #Плагины #Безопасность #TypeScript
