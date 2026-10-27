---
создал заметку: 2026-08-13T12:40:00
обновлено: 2026-10-27T20:30:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Память
  - Контекст
  - Tencent
  - MCP
  - Docker
  - OpenSource
Источник:
  - https://t.me/bugnotfeature/26785
  - https://github.com/TencentCloud/TencentDB-Agent-Memory
  - https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/813
  - https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/73
  - https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/964
---

# TencentDB Agent Memory — командная память для ИИ-агентов со сжатием контекста

**TencentDB Agent Memory** — открытый проект Tencent Cloud: «память» для ИИ-агентов из четырёх активов — Chat Memory, Skill, Wiki, CodeGraph — плюс **сжиматель контекста**, который заменяет громоздкие результаты инструментов краткими выжимками. Работает с OpenClaw и Hermes Agent как плагин, а с Claude Code и CodeBuddy — через прозрачный прокси к LLM.

Данные сверены 27.10.2026 по репозиторию, issues, Docker Hub и npm (первая версия заметки — 13.08.2026).

| | |
| :--- | :--- |
| Репозиторий | [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory), создан 07.04.2026 |
| Звёзды / форки | **30 021** · 2 914 |
| Лицензия / язык | **MIT** (GitHub показывает NOASSERTION из-за шапки Tencent перед текстом MIT) · TypeScript |
| Версии | релиз репозитория **v2.0.3** и Docker-образы **1.0.3** — оба от 26.10.2026; npm-плагин для OpenClaw `@tencentdb-agent-memory/memory-tencentdb` — 1.0.3 (22.09.2026) |
| Ветки | по умолчанию — `feat/server_team` (полный стек), в `main` — плагин для OpenClaw и Hermes и таблица бенчмарков |
| Открытые issues и PR | 904 |

Ссылка из поста (`github.com/Tencent/...`) перенаправляет на организацию `TencentCloud`; README теперь клонирует правильный адрес.

---

## 🧩 Как устроено

Полный стек — **четыре сервиса в Docker**:

| Сервис | Порт | Что делает |
| :--- | :---: | :--- |
| Memory Core | `8420` | хранение и обработка памяти, auth, data plane для skill/RAG |
| Panel UI (Memory Hub) | `8125` | веб-панель: команды, агенты, ревью и выдача активов |
| Knowledge | `8424` | Wiki и CodeGraph |
| Proxy | `8096` | прозрачный прокси LLM-запросов (протоколы Anthropic и OpenAI) |

Агент (Claude Code, CodeBuddy, OpenClaw, Hermes) ходит не напрямую в модель, а через `MemoryProxy`:
- на входе прокси подмешивает в системный промпт нужные навыки и память;
- на выходе асинхронно извлекает из диалога новые знания.

Хранилище — SQLite в томе контейнера, с недавних версий есть и вариант с MongoDB (`start-all-mongo.sh`).

Память слоистая: **L0** (сырой диалог) → **L1** (факты, предпочтения, ограничения) → **L2** (сцены вокруг задачи) → **L3** (персона, долгосрочный профиль). Обычно в контекст попадают L2/L3, а за конкретными фактами система спускается в L1/L0 через BM25, векторы и RRF.

Управление активами сделано всерьёз:
- у каждого актива есть владелец, версия и статус;
- видимость — `private`, `team`, `restricted` или `agent`;
- есть ACL и привязка к конкретному агенту.

Модель «память как инвентарь, который выдают агенту под роль» заметно взрослее, чем «свалить всё в векторы».

> [!note] Заимствования проект указывает сам
> В разделе Acknowledgements сказано:
> - CodeGraph **использует код** проекта [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph);
> - управление скиллами построено на **части кода Skill из Hermes Agent** (Nous Research);
> - идея Wiki взята из гиста Карпаты про «LLM Wiki».

---

## 📈 Бенчмарки

Таблица живёт в README ветки `main`. В README ветки по умолчанию остался только PersonaMem. Базовая линия везде — **OpenClaw без плагина**:

| Способность | Бенчмарк | OpenClaw | + плагин | Δ успеха | Токенов было | Стало | Δ токенов |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Короткая память | WideSearch | 33% | **50%** | **+51.52%** | 221.31M | **85.64M** | **−61.38%** |
| Короткая память | SWE-bench | 58.4% | **64.2%** | **+9.93%** | 3474.1M | **2375.4M** | **−33.09%** |
| Короткая память | AA-LCR | 44.0% | **47.5%** | **+7.95%** | 112.0M | **77.3M** | **−30.98%** |
| Долгая память | PersonaMem | 48% | **76%** | **+59%** | — | — | — |

Все бенчмарки — признанные:
- [WideSearch](https://widesearch-seed.github.io/) (ICLR 2026) — широкий сбор информации в таблицу;
- [AA-LCR](https://artificialanalysis.ai/articles/announcing-aa-lcr) (Artificial Analysis) — рассуждения по документам на 100k+ токенов;
- PersonaMem (COLM 2025) — около 6000 вопросов по историям на 32k/128k/1M токенов.

SWE-bench прогоняется как **50 последовательных задач** в одной сессии, чтобы смоделировать накопление контекста.

Как читать эти цифры:
- **Для кодинга ориентир — SWE-bench, около −33 %.** Заголовочные −61 % получены на WideSearch. Сжиматель работает только с результатами вызовов инструментов, а в поиске это огромные шумные веб-страницы, которые отлично ужимаются. В кодинге результат инструмента — чаще diff, вывод компилятора или содержимое файла, где выкидывать почти нечего.
- **Строка SWE-bench расходится с собственной арифметикой.** Из напечатанных чисел получается (3474,1 − 2375,4) / 3474,1 = **31,6 %**, а не 33,09 %; остальные строки сходятся точно. На это указывает [issue #813](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/813) от 05.08.2026, ответа команды нет.
- **Экономия считается по основной модели.** Сжатие делает вторая LLM (см. ниже), её расход в таблицу не входит.
- **Замеры — для OpenClaw.** Для подключения Claude Code через `MemoryProxy` опубликованных цифр нет.

### Воспроизводимость

Публичного харнесса для повторения бенчмарков пока нет:
- [Issue #73](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/73): пользователь прогнал «OpenClaw против OpenClaw + плагин» на локальной Qwen3.6-27B-FP8 — разницы в успешности не было, а токенов ушло больше. Мейнтейнер ответил, что качество извлечения L1 сильно зависит от способностей модели, а насчёт публикации скриптов «оценят внутри». 06.10.2026 issue закрыт без публикации скриптов.
- Предложения сообщества — [#106](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/106) и [#812](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/812) с готовым харнессом — открыты. PR #204 с гайдом по воспроизведению закрыт без слияния.

---

## ⚙️ Как устроен сжиматель

Механика из трёх частей, по коду (`MemoryCore/src/offload_server/`):

**1. Суммаризатор результатов инструментов** (`prompts/l1-prompt.ts`). Каждая пара «вызов инструмента + результат» уходит отдельной LLM. Та возвращает JSON:
- краткое описание вызова;
- `summary` до 200 символов;
- главное — **`score` от 0 до 10**: насколько summary способна заменить оригинал.

Параметры вызова обрезаются до 500 символов, результат — до 2000.

**2. Карта задачи в Mermaid** (`prompts/l2-prompt.ts`). Системный промпт (на китайском) просит модель построить «когнитивный автомат состояний» в виде `flowchart TD`:
- форма узла кодирует тип действия;
- статус узла — `done|doing|paused|blocked`;
- отдельные «когнитивные надгробия» отмечают тупиковые решения, чтобы агент не наступал на те же грабли;
- сверху — метаданные `taskGoal`, `progress` 0–100 и таймстемпы.

Размер карты — в пределах 4000 символов.

**3. Четыре уровня сжатия** (`compact/compressor.ts`) выбираются по доле занятого окна контекста:

| Уровень | Порог | Что делает |
| :--- | :---: | :--- |
| `fastpath` | < 50% | переприменяет уже подтверждённые замены, ничего нового не сжимает |
| `mild` | ≥ 50% | сканирует **первые 70%** сообщений и меняет результаты инструментов на summary — по убыванию score и только пока `score ≥ 4` |
| `aggressive` | ≥ 85% | режет крупные результаты до 2000 символов и удаляет сообщения, защищая «хвост» после последнего сообщения пользователя (минимум 10 сообщений) |
| `emergency` | ≥ 95% | то же жёстче, но Mermaid-карты вынимаются и сохраняются в первую очередь |

Ещё две хорошие детали:
- в `mild` замена не делается, если summary не короче оригинала;
- токены считаются настоящим tiktoken, а не оценкой «символы делить на 4».

---

## 💸 Вторая модель

> [!caution] Сжатие и извлечение памяти делает отдельная LLM
> В `.env.example` две независимые группы настроек:
> - `MEMORY_LLM_BASE_URL` / `_API_KEY` / `_MODEL` / `_PROTOCOL` (`openai` или `anthropic`) — внутренняя модель: суммаризация, Mermaid-карты, ingest Wiki;
> - `PROXY_UPSTREAM_URL` / `_API_KEY` / `_MODEL` — модель, с которой вы реально работаете.
>
> Каждый вызов инструмента вашего агента порождает дополнительный вызов внутренней модели.

Механизм окупается, только когда суммаризатор достаточно умён, чтобы его summary действительно заменяла оригинал. Если ставить на роль `MEMORY_LLM` лёгкую или локальную модель, экономии может не быть вовсе — это и показал #73.

---

## ⚠️ Что учесть перед установкой

**Claude Code пока не пишет память.** [Issue #964](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/964) (12.08.2026): полный стек по официальной инструкции, Claude Code через прокси. Инъекция, авторизация и выбор агента работают, а захват диалога — нет: счётчики `pipelineWorker` в `/health` нулевые, в панели ноль записей на всех слоях. 13.08 мейнтейнер пообещал внутреннюю проверку; на 27.10 issue открыт. Для работы в Claude Code это блокер — перед установкой проверьте его статус.

**Обновление образов.** В `.env` образы указаны как `:latest`. Скрипт запуска переиспользует уже скачанный локальный `:latest` и не замечает обновлений на Docker Hub. Чтобы обновиться, сделайте `docker pull` или закрепите тег, например `agentmemory/memory-core:1.0.3`.

**Поток обращений.** Открыто 904 issue и PR: внешние патчи приходят быстрее, чем их разбирают.

### Сеть и авторизация

> [!danger] Гейт авторизации по умолчанию выключен, а порты открыты наружу
> Скрипты публикуют порты на **все интерфейсы** (`-p "${MEMORY_CORE_PORT}:8420"`, внутри контейнера — `0.0.0.0`). То же у прокси и панели.
>
> `MEMORY_CORE_GATEWAY_API_KEY` в `.env.example` по умолчанию пустой, и Bearer-проверка выключена. Комментарий рядом объясняет почему: с непустым ключом **прокси перестаёт работать**, потому что он этот заголовок не отправляет. Включить ключ предлагают «после того, как починят на стороне прокси» — на 27.10.2026 это не исправлено.
>
> Любой в локальной сети, кто дотянется до `:8420`, читает и пишет всю командную память.

Открытость в LAN задумана: переменная `MEMORY_HUB_PROXY_PUBLIC_URL` подставляет LAN-адрес, «чтобы с чужого компьютера можно было просто скопировать URL из карточки».

**Что делать:**
- привязывать порты к петле: `-p 127.0.0.1:8420:8420` и так далее, поправив скрипты запуска;
- либо закрыть порты файрволом;
- снаружи ходить только через SSH-туннель или WireGuard.

Через `MemoryProxy` проходит **весь** диалог с моделью, включая содержимое файлов, а `PROXY_UPSTREAM_API_KEY` лежит в конфиге прокси. Это ещё один довод не выставлять прокси в сеть.

---

## 💻 Установка по системам

Основной путь — Docker. Три образа под `linux/amd64` и `linux/arm64`, compose не нужен — скрипты используют обычный `docker run`. Суммарно около **880 МБ** в сжатом виде:

| Образ | Размер |
| :--- | ---: |
| memory-core | 248 МБ |
| memory-hub | 449 МБ |
| memory-proxy | 186 МБ |

Полная инструкция — в [INSTALL.md](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/INSTALL.md): отдельный Memory Hub, прокси с Claude Code и CodeBuddy, остановка и очистка, порты.

> [!important] Расход ОЗУ я не замерял
> Размеры образов взяты из Docker Hub API, а потребление памяти тремя Node-сервисами под нагрузкой — нет. Померьте сами, прежде чем ставить на слабую машину.

### Gentoo (основная система)

```bash
sudo emerge -av app-containers/docker app-containers/docker-cli

# OpenRC
sudo rc-update add docker default
sudo rc-service docker start
sudo usermod -aG docker "$USER"   # перелогиниться

git clone https://github.com/TencentCloud/TencentDB-Agent-Memory.git
cd TencentDB-Agent-Memory/deploy/global-images
cp .env.example .env
$EDITOR .env      # заполнить обе группы: MEMORY_LLM_* и PROXY_UPSTREAM_*
./start-all.sh
```

Ядро должно быть собрано с опциями для контейнеров. При сомнениях проверьте `CONFIG_NAMESPACES`, `CONFIG_CGROUPS`, `CONFIG_OVERLAY_FS` — например, скриптом `check-config.sh` из исходников Docker.

Сборка сервисов из исходников без Docker требует `>=net-libs/nodejs-22.16` (`"node": ">=22.16.0"` в `package.json`) и `pnpm`: проект собран как pnpm-workspace.

### Debian / Ubuntu

```bash
sudo apt update && sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

Дальше — те же команды `git clone` … `./start-all.sh`. Для пути без Docker: штатный `nodejs` в Debian 13 и Ubuntu 24.04 **старее 22.16**, ставьте NodeSource или `nvm`.

### Arch

```bash
sudo pacman -S docker
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

Сборка из исходников здесь проще всего: `sudo pacman -S nodejs pnpm` даёт свежий Node.

### Entware (ASUS RT-AX56U)

> [!danger] Не встанет
> Любой из причин достаточно:
> - **Docker'а на Entware нет**, а проект распространяется образами;
> - **512 МБ ОЗУ** на роутере против трёх Node-сервисов, SQLite и векторного поиска;
> - **armv7**, а образы собраны под `amd64` и `arm64` — 32-битной сборки нет;
> - Node в Entware — 18.x, а требуется `>=22.16`.
>
> Роутер может быть только клиентом: пробросить туннель до машины, где стек уже работает.

---

## 🎯 Стоит ли ставить

**Где смысл есть.** Команда из нескольких людей и агентов, где каждый новый агент заново изучает проект. Управление активами с владельцами, версиями, видимостью и ACL здесь сделано всерьёз, и саму модель «памяти как инвентаря» стоит подсмотреть, даже если стек не ставить.

**Где смысла мало — один человек с Claude Code:**
- экономия на кодинге — около трети, а не 60 %, и публичного способа её воспроизвести нет;
- за сжатие платишь токенами второй модели;
- захват диалога из Claude Code сейчас не работает (#964);
- четыре сервиса и ~880 МБ образов;
- гейт авторизации выключен, а включить его нельзя, не сломав прокси.

**Разумная позиция:** дождаться закрытия #964 и публичного харнесса, а пока прочитать `l2-prompt.ts` и забрать себе идею Mermaid-карты задачи. Она хороша сама по себе и не требует ставить ничего.

---

## 🔗 Связанные заметки

- [Obsidian Mind](Obsidian%20Mind%20%E2%80%94%20%D0%BF%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B2%20Obsidian-%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B5.md) — та же задача (постоянная память для агентов), но local-first и на порядок проще: без Docker, без второй LLM, память лежит в обычном Obsidian-хранилище. Прямая альтернатива для одиночки.
- [Memora](Memora%20%28agentic-box%29%20%E2%80%94%20%D0%BF%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20MCP.md) — один MCP-сервер на SQLite вместо четырёх сервисов.
- [Supermemory](Supermemory%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%B8%20%D0%B8%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2.md) — коммерческий движок памяти с облаком и локальным сервером.
- [MiMo Code](../../MiMo%20Code%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%B4%D0%BB%D1%8F%20%D0%BA%D0%BE%D0%B4%D0%B0%20%D1%81%20%D0%B4%D0%BE%D0%BB%D0%B3%D0%BE%D0%B9%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%D1%8E%20%28Xiaomi%29.md) — агент, у которого долгая память встроена, а не прикручена сбоку.
- [Claude Code — гайд](../../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) — штатные средства Claude Code: `CLAUDE.md`, компактификация, `/compact`. Первое, что стоит выжать, прежде чем ставить внешнюю память.
- [MCP](../MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) — альтернативный способ дать агенту доступ к внешним знаниям.
- [PixelRAG](../PixelRAG%20%E2%80%94%20RAG%20%D0%BF%D0%BE%20%D1%81%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D0%B0%D0%BC%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20HTML%20%28visual%20RAG%2C%20VLM-%D1%8D%D0%BC%D0%B1%D0%B5%D0%B4%D0%B4%D0%B8%D0%BD%D0%B3%D0%B8%2C%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20Claude%20Code%29.md) — другой подход к RAG для агентов, для сравнения с Wiki-слоем.
- [Scan (Foglamp)](../../../Code-Graph/Scan%20%28Foglamp%29%20%E2%80%94%20%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2%D1%83%D1%8E%20%D0%B1%D0%B0%D0%B7%D1%83%20%D0%B2%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%B3%D1%80%D0%B0%D1%84%20%D1%80%D1%83%D0%BA%D0%B0%D0%BC%D0%B8%20%D1%82%D0%B2%D0%BE%D0%B5%D0%B3%D0%BE%20%D0%B6%D0%B5%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%B0%20%28Claude%20Code%2C%20Codex%29.md) и [Understand Anything](../../../Code-Graph/Understand%20Anything%20%E2%80%94%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D0%B3%D1%80%D0%B0%D1%84%20%D0%B7%D0%BD%D0%B0%D0%BD%D0%B8%D0%B9%20%D0%BF%D0%BE%20%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%B1%D0%B0%D0%B7%D0%B5.md) — про графы кода: с чем сравнивать модуль CodeGraph.
- [LiteLLM](../../../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md) — если нужен просто шлюз к LLM без всей истории с памятью.
- [OpenCode Zen](../../../ProxyLLM/OpenCode%20Zen%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B5%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%20%D0%B4%D0%BB%D1%8F%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%C2%AB%D0%BC%D0%B8%D0%BB%D0%BB%D0%B8%D0%B0%D1%80%D0%B4%D0%B0%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%C2%BB%20%E2%80%94%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BB%D0%B8%D0%BC%D0%B8%D1%82%D1%8B%20%D0%B8%20%D1%87%D0%B5%D0%BC%20%D0%BF%D0%BB%D0%B0%D1%82%D0%B8%D1%88%D1%8C%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D0%B4%D0%B5%D0%BD%D0%B5%D0%B3%29.md) — чем платят за «бесплатные» токены; полезный контекст к вопросу «сколько стоит вторая модель».
- [awesome-hermes-agent](../../../Skills/awesome-hermes-agent%20%280xNyk%29%20%E2%80%94%20%D0%BD%D0%B5%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D1%8B%D0%B9%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%20Hermes%20Agent%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%2C%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%2C%20%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C%29%2C%20%D1%81%20%D0%BC%D0%B5%D1%82%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%B7%D1%80%D0%B5%D0%BB%D0%BE%D1%81%D1%82%D0%B8.md) — экосистема, из которой взят код управления скиллами.
- [Ollama](../../../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) и [llama.cpp](../../../Local-LLM/llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) — если решите ставить `MEMORY_LLM` локально; сначала перечитайте раздел про #73.
- [skillcheck](../../../Skills/skillcheck%20%28sx4im%29%20%E2%80%94%20A-B-%D1%82%D0%B5%D1%81%D1%82%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%28SKILL.md%2C%20AGENTS.md%2C%20CLAUDE.md%29%20%D1%81%D0%BE%20%D1%81%D0%BB%D0%B5%D0%BF%D0%BE%D0%B9%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%BE%D0%B9%20%D0%B8%20bootstrap-CI%2C%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B3%D0%B4%D0%B5%20%D0%BE%D0%BD%D0%B0%20%D0%B2%D1%80%D1%91%D1%82.md) — как вообще проверять, что скилл или обвязка что-то дают.
- [Сводная таблица AI-агентов](../../%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%BE%D0%BA%D1%82%D1%8F%D0%B1%D1%80%D1%8C%202026%29.md) — общая картина по агентам.

## 🔗 Ссылки

- [Репозиторий (TencentCloud/TencentDB-Agent-Memory)](https://github.com/TencentCloud/TencentDB-Agent-Memory) · [INSTALL.md](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/feat/server_team/INSTALL.md) · [релизы](https://github.com/TencentCloud/TencentDB-Agent-Memory/releases)
- [README ветки `main` с таблицей бенчмарков](https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/README.md)
- [Issue #813 — арифметика строки SWE-bench](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/813)
- [Issue #73 — воспроизведение на локальной модели](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/73)
- [Issue #964 — Claude Code не пишет память](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/964)
- [Issue #812 — предложенный воспроизводимый харнесс](https://github.com/TencentCloud/TencentDB-Agent-Memory/issues/812)
- [WideSearch — бенчмарк широкого поиска (ICLR 2026)](https://widesearch-seed.github.io/)
- [AA-LCR — бенчмарк длинного контекста (Artificial Analysis)](https://artificialanalysis.ai/articles/announcing-aa-lcr)
- [Пост-источник (bugnotfeature/26785)](https://t.me/bugnotfeature/26785)

#AI #Агенты #Память #Контекст #Tencent #MCP #Docker #OpenSource
