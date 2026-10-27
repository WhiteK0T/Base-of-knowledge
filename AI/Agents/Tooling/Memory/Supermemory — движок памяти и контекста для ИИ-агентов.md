---
создал заметку: 2026-09-10T01:30:00
обновлено: 2026-10-27T20:30:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Память
  - Бенчмарки
  - MCP
  - Self-hosted
Источник:
  - https://t.me/bugnotfeature/27627
  - https://github.com/supermemoryai/supermemory
  - https://supermemory.ai/docs
  - https://supermemory.ai/docs/self-hosting/overview
  - https://supermemory.ai/pricing/
---

# 🧠 Supermemory — движок памяти и контекста для ИИ-агентов

**Supermemory** ([github.com/supermemoryai/supermemory](https://github.com/supermemoryai/supermemory)) — движок памяти и контекста для ИИ. Он извлекает факты из диалогов, строит профиль пользователя, разрешает противоречия и «забывает» устаревшее. Продукт коммерческий, компания из Сан-Франциско. Работать с ним можно двумя способами:
- через облачный API;
- через локальный сервер **Supermemory Local** — готовый бинарник или Docker-образ.

Данные сверены 27.10.2026 по репозиторию, релизам, документации и странице тарифов (первая версия заметки — 10.09.2026).

| | |
| :--- | :--- |
| Репозиторий | [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory), с 27.02.2024, разработка активная |
| Звёзды / форки | **31 431** · 2 764 |
| Лицензия | **MIT** — на SDK, MCP, документацию и UI-компоненты в репозитории |
| Движок | **закрытый**: сервер собирается из отдельной непубличной кодовой базы, бесплатен в пределах лайт-лицензии |
| Локальный сервер | **Supermemory Local 0.0.9** (12.10.2026): бинарники под Linux и macOS, Docker-образ под amd64 и arm64; под Windows — 0.0.8 |
| Порт / данные | `6767` · `~/.supermemory` (бинарник) или том `supermemory_supermemory-data` (Docker) |

---

## 📦 Что открыто, а что нет

Документация теперь говорит прямо:
- *«The SDKs and other components in the public repository are open source; the downloadable self-hosted server binary is built from a separate, non-public codebase»*;
- *«Self-hosted is free within its lite license limit… The server binary is not open source»*.

В открытом репозитории (около 940 файлов) лежат:
- документация `apps/docs` — больше половины объёма;
- MCP-сервер `apps/mcp`, который ходит в облачный API;
- SDK под TypeScript и Python и обёртки под Vercel AI SDK, Mastra, LangChain и др.;
- UI-компоненты — например, виджет графа памяти `packages/memory-graph`;
- песочницы и расширения.

Кода движка и сборки сервера в репозитории нет. Релизы `server-v*` выкладывают готовые бинарники, а Docker-образ публикуется отдельно.

## 💻 Локальный сервер

### Установка

**Скриптом** — тянет бинарник из релизов того же репозитория:

```bash
curl -fsSL https://supermemory.ai/install | bash      # можно закрепить версию: bash -s -- 0.0.9
```

Скрипт скачивает `manifest.json` с **sha256 для каждой платформы** и проверяет контрольную сумму. Перед откатом версии он предупреждает о бэкапе.

**Через Docker** (с 0.0.9) — исходники и сборка не нужны:

```bash
release_url=https://github.com/supermemoryai/supermemory/releases
curl -fL "$release_url/download/server-v0.0.9/compose.yaml" -o compose.yaml
export OPENAI_API_KEY=...            # ключ своего LLM-провайдера
export SUPERMEMORY_VERSION=0.0.9
docker compose up -d --wait --wait-timeout 180

# локальный API-ключ сервера (отдельный от ключа LLM)
docker compose exec -T supermemory cat /data/api-key
```

Подробности Docker-варианта:
- образ — `docker.io/supermemory/supermemory`;
- Compose публикует порт **только на `127.0.0.1:6767`**;
- данные, ключ, конфиг и кэш моделей лежат в именованном томе;
- при обновлении том нельзя удалять — `docker compose down -v` уничтожит хранилище.

| Платформа (0.0.9) | Размер бинарника |
| :--- | ---: |
| linux-x64 | ~297 МБ |
| linux-arm64 | ~269 МБ |
| darwin-arm64 | ~258 МБ |
| darwin-x64 | ~272 МБ |
| windows-x64 | ~278 МБ (остаётся на 0.0.8) |

### Что нужно для работы

- **Память:** около 1,6 ГБ ОЗУ после загрузки плюс до 1 ГБ на индексацию (`SUPERMEMORY_EMBEDDING_RAM_LIMIT`). Сверх лимита новые документы ждут в очереди, а не теряются. Рабочий набор — около 2,6 ГБ.
- **Эмбеддинги** по умолчанию локальные (`Xenova/bge-base-en-v1.5`, без ключа); можно переключить на OpenAI, Gemini или Ollama.
- **LLM** нужен хотя бы один: OpenAI, Anthropic, Gemini, Groq или любой OpenAI-совместимый эндпоинт. Полностью офлайн — через Ollama (`gpt-oss:20b`). Телеметрия отключается `SUPERMEMORY_DISABLE_TELEMETRY=1`.
- **Внешние ключи для части форматов:**
  - PDF — `GEMINI_API_KEY`;
  - картинки — Gemini или Vertex AI;
  - веб-страницы читаются через Firecrawl (`FIRECRAWL_API_KEY`).
- **Ключ API** обязателен даже для запросов с localhost (с 0.0.9).

Чем локальный сервер отличается от облака:
- в нём нет коннекторов (Google Drive, Notion, Gmail, OneDrive) и облачного Supermemory MCP;
- плагины для Claude Code, Muse Code, Codex и OpenCode можно направить на локальный сервер через `SUPERMEMORY_API_URL=http://localhost:6767`.

> [!warning] Версия 0.0.x — делайте бэкап перед обновлением
> Схема данных ещё меняется. В примечаниях к 0.0.8 описана ошибка 0.0.7: обновление rc-хранилища **молча стирало поисковые векторы**. Документы оставались в списке, но поиск по ним ничего не находил; в 0.0.8 это лечится при загрузке. В 0.0.9 убран режим `WORKFLOW_ENGINE=direct`, а перед миграцией сервер сам проверяет наличие полного бэкапа.

## 📈 Что означают цифры из README

README заявляет **«#1 on every major AI memory benchmark»** — LongMemEval, LoCoMo и ConvoMem. Отдельно названы **95 % Recall@15 при сокращении контекста на 99,4 %** и профиль пользователя примерно за 50 мс.

**95 % — это Recall@15.** На бенчмарке [LongMemEval](https://github.com/xiaowu0162/LongMemEval) (500 вопросов, MIT, 1 177★) это доля вопросов, где нужное воспоминание попало в 15 найденных фрагментов. Это метрика **поиска**: модель ещё должна собрать из этих фрагментов правильный ответ. По категориям:

| Категория | Recall@15 |
| :--- | ---: |
| Assistant recall | 100 % |
| Knowledge Updates | 99 % |
| User recall | 97 % |
| Multi-session | 93 % |
| Temporal Reasoning | 91 % |
| Preference | 90 % |

**99,4 % сходится с первоисточником.** В варианте `longmemeval_s` история на один вопрос — около 115 тыс. токенов (~40 сессий), Supermemory добавляет около 720: 1 − 720/115 000 ≈ 99,4 %. При @10 и @5 — 99,6 % и 99,8 % (меньше выдача — меньше токенов, ниже recall).

**«Первое место» — результат собственных прогонов.** Публичных лидербордов нет ни у одного из трёх бенчмарков:

| Бенчмарк | Репозиторий | Последний пуш |
| :--- | :--- | :--- |
| LongMemEval | [xiaowu0162/LongMemEval](https://github.com/xiaowu0162/LongMemEval) | 11.05.2026 |
| LoCoMo | [snap-research/locomo](https://github.com/snap-research/locomo) | 13.08.2024 |
| ConvoMem | [SalesforceAIResearch/ConvoMem](https://github.com/SalesforceAIResearch/ConvoMem) — ссылка в README ведёт на старый адрес `Salesforce/ConvoMem` | 02.06.2026 |

Замеры сделаны открытым харнессом [MemoryBench](https://github.com/supermemoryai/memorybench) (MIT, 331★). Он гоняет Supermemory, Mem0, Zep и др. на одних данных и считает три метрики — качество, задержку и стоимость, — поэтому результат можно перепроверить самостоятельно. Независимых публикаций с такой проверкой пока нет.

**Облачная конфигурация и локальная — не одно и то же.** Документация пишет об этом прямо:

> *Local runs the extraction pipeline on whatever model you bring. Enterprise runs it on Supermemory's proprietary models, purpose-tuned for long-horizon data understanding — higher-quality memories at a lower effective cost…*

Значит, рекордные цифры относятся к облаку с собственными моделями вендора. Локально качество зависит от вашей модели, и насколько оно ниже — не опубликовано.

**Около 50 мс** — это время получения профиля пользователя (`profile()`), а не поиска по памяти.

Ещё одна новая цифра из README — файловая система **SMFS** (Supermemory Filesystem): в 3 раза меньше токенов на Claude (24M против 72M) и в 1,75 раза меньше на Codex на бенчмарке xAFS из 110 вопросов. Это тоже замер самого вендора, разбор — на их [странице исследований](https://supermemory.ai/research).

## 💰 Тарифы облака

| План | Цена | Что даёт |
| :--- | :--- | :--- |
| **Free** | $0 | кредитов на **$5/мес**, полный API поиска и памяти, **все плагины** (Claude Code, Cursor, Hermes и др.), 1 место |
| **Pro** | $19/мес | кредитов на $20/мес, автопополнение с лимитом, приоритетная поддержка, 3 места |
| **Max** | $100/мес | кредитов на $130/мес, коннектор Gmail |
| **Scale** | $399/мес | кредитов на $600/мес, неограниченно мест с доступом по тегам, S3 и веб-краулер, продвинутый разбор PDF, SOC 2, HIPAA BAA, опция self-hosting |
| **Enterprise** | по договорённости | SSO, air-gapped self-hosting, выделенный инженер, SLA |

Цены операций одинаковы на всех планах; SM-токены — это реально обработанные уникальные токены:

| Операция | Цена |
| :--- | :--- |
| память | $0,005 за 1K SM-токенов текста, $0,010 — для «богатого» контента |
| SuperRAG | $0,001 / $0,002 за 1K SM-токенов |
| поиск | $0,005 за 1000 запросов |
| переранжирование, переписывание запроса и пр. | $0,10 за 1000 |

## 🖥️ По системам

Пакета нет ни в одном дистрибутиве. Варианты: облачный API, бинарник из установщика или Docker-образ. Из исходников движок не собрать — их нет в открытом доступе. Если принципиально не запускать чужие бинарники, остаются облачный API или изоляция: контейнер либо `sys-apps/bubblewrap` для бинарника.

| Система | Как поставить |
| :--- | :--- |
| **Gentoo** (основная) | Docker: `emerge --ask app-containers/docker app-containers/docker-cli app-containers/docker-compose`, затем `rc-update add docker default && rc-service docker start` (OpenRC). Либо бинарник через установщик. Для SDK — `emerge --ask net-libs/nodejs` |
| **Debian / Ubuntu** | `sudo apt install docker.io docker-compose` (Debian 13) или `docker.io docker-compose-v2` (Ubuntu 24.04), затем `sudo systemctl enable --now docker`. SDK — `npm install supermemory` или `pip install supermemory` |
| **Arch** | `sudo pacman -S docker docker-compose`, `sudo systemctl enable --now docker`; либо установщик. В AUR пакета нет |
| **Entware / RT-AX56U** | ❌ сборок под armv7 нет (только x64 и arm64), бинарник почти 300 МБ при 256 МБ флеша, а базовые 1,6 ГБ ОЗУ втрое больше всей памяти роутера. Применимо только облачное подключение с нормальной машины |

## 🎯 Итог

- **Что это:** крупный живой проект (31k★) с SDK под популярные фреймворки, MCP и плагинами для Claude Code, Codex, OpenCode, Muse Code, Hermes. Инженерная культура высокая: установщик проверяет sha256, Docker-порт привязан к localhost, ключ API обязателен, харнесс MemoryBench открыт.
- **Что открыто:** SDK, MCP, документация и UI — под MIT. Сам движок закрыт и бесплатен для локального запуска в пределах лайт-лицензии.
- **Что означают рекорды:** 95 % — это Recall@15 поиска на LongMemEval. «Первое место» получено собственным харнессом на облачной конфигурации с проприетарными моделями; локально результат зависит от вашей модели.
- **Кому подойдёт:** тем, кто строит продукт и готов платить за API. Для личного использования локальный сервер рабочий, но это ~300 МБ закрытого кода и ~2,6 ГБ ОЗУ ради задачи, которую одному человеку часто закрывают [файлы в Obsidian](Obsidian%20Mind%20%E2%80%94%20%D0%BF%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B2%20Obsidian-%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B5.md) или [Memora](Memora%20%28agentic-box%29%20%E2%80%94%20%D0%BF%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20MCP.md).

Скилл Supermemory для агента стоит дёшево: `name` + `description` — **80 токенов** (0,04 % окна в 200k), тело подгружается по требованию.

---

## 🔗 Связанные заметки

- Командная память со сжатием контекста: [TencentDB Agent Memory](TencentDB%20Agent%20Memory%20%E2%80%94%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D1%81%D0%BE%20%D1%81%D0%B6%D0%B0%D1%82%D0%B8%D0%B5%D0%BC%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B0.md)
- Память на обычных файлах, без вендора и без бинарников: [Obsidian Mind](Obsidian%20Mind%20%E2%80%94%20%D0%BF%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B2%20Obsidian-%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B5.md)
- Открытый MCP-сервер памяти на SQLite: [Memora](Memora%20%28agentic-box%29%20%E2%80%94%20%D0%BF%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20MCP.md)
- Через что подключается облачный вариант: [MCP — серверы Model Context Protocol](../MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md)
- Граф кодовой базы с замерами экономии токенов: [codebase-memory-mcp](../../../Code-Graph/codebase-memory-mcp%20%28DeusData%29%20%E2%80%94%20%D0%B3%D1%80%D0%B0%D1%84%20%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%B1%D0%B0%D0%B7%D1%8B%20%D0%BD%D0%B0%20C%20%28162%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0%2C%20%D0%B0%20%D0%BD%D0%B5%20158%3B%20%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%B3%D0%BE%20%D0%BD%D0%B5%D1%82%3B%20%E2%88%9299%25%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%E2%88%9290%25%20%D0%B2%20%D0%B8%D1%85%20%D0%B6%D0%B5%20%D1%81%D1%82%D0%B0%D1%82%D1%8C%D0%B5%29.md)
- Чтобы гонять локальный движок полностью офлайн: [Ollama](../../../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)
- Где живут плагины памяти: [Claude Code — гайд](../../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

## 🔗 Ссылки

- Репозиторий: [github.com/supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) (MIT) · релизы движка: [server-v*](https://github.com/supermemoryai/supermemory/releases)
- Документация: [supermemory.ai/docs](https://supermemory.ai/docs) · self-hosting: [overview](https://supermemory.ai/docs/self-hosting/overview) · [Docker](https://github.com/supermemoryai/supermemory/blob/main/apps/docs/self-hosting/docker.mdx) · [Local vs Enterprise](https://supermemory.ai/docs/self-hosting/local-vs-enterprise) · тарифы: [supermemory.ai/pricing](https://supermemory.ai/pricing/)
- Харнесс бенчмарков: [supermemoryai/memorybench](https://github.com/supermemoryai/memorybench) (MIT)
- Сами бенчмарки: [LongMemEval](https://github.com/xiaowu0162/LongMemEval) · [LoCoMo](https://github.com/snap-research/locomo) · [ConvoMem](https://github.com/SalesforceAIResearch/ConvoMem)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/27627)

#AI #Агенты #Память #Бенчмарки #MCP #Self-hosted
