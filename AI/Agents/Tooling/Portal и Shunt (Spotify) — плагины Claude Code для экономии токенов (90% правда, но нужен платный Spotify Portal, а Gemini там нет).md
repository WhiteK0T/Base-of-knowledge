---
создал заметку: 2026-09-10T00:40:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Плагины
  - Токены
  - Backstage
  - Хуки
Источник:
  - https://t.me/bugnotfeature/27593
  - https://github.com/spotify/portal-ai-plugins
  - https://backstage.spotify.com/
---

# 🔀 Portal и Shunt (Spotify) — экономия токенов в Claude Code: цифра верна, условия — нет

**spotify/portal-ai-plugins** ([github.com/spotify/portal-ai-plugins](https://github.com/spotify/portal-ai-plugins)) — маркетплейс из двух плагинов для Claude Code (а также Codex и Cursor). Репозиторий **настоящий, из организации `spotify`**: **794★, 44 форка, Apache-2.0**, создан 23.07.2026, 6 коммитов от трёх сотрудников Spotify, последний — 17.08.2026.

> [!warning] Коротко
> Цифра **90 % экономии — настоящая**, она взята прямо из README и подтверждается их же таблицей. Но пост опустил два условия, без которых всё это не работает.
> **Первое:** «Portal» — это **не роутер к дешёвым моделям**, а платный корпоративный портал разработчика Spotify (Backstage). CLI, вокруг которого построены оба плагина, распространяется по **коммерческой лицензии**: *«you must obtain a license»*. Без подписки на Spotify Portal плагины бесполезны.
> **Второе:** **Gemini 2.5 Flash в репозитории не упоминается ни разу** — я прогрепал всё дерево. Делегирование идёт в «режимы AiKA» на твоём экземпляре Portal, а какая там модель — решает администратор портала, не плагин.
> И третье, помельче: 90 % — это экономия **на операции чтения файлов**, а не «расход токенов в Claude Code на 90 %».

---

## ✅ Проверка заявлений из поста

| Заявление | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «Spotify выкатили плагины» | ✅ | Организация `spotify`, Apache-2.0, авторы — сотрудники. Всё честно |
| «Всего два плагина — Portal и Shunt» | ✅ | Именно так: `portal` (6 скиллов) и `shunt` (2 скилла + 2 хука + 2 скрипта) |
| «Portal даёт Claude Code кидать лёгкие задачи дешёвым моделям» | ❌ | Portal вообще не про это. Его 6 воркфлоу: `setup`, `doctor`, `search` по каталогу сервисов, `service` (справка по сервису), `actions`, `feedback`. Это клиент **портала разработчика**, а делегированием занимается только Shunt |
| «дешёвым моделям **по типу Gemini 2.5 Flash**» | ❌ | Строки `gemini` в репозитории **нет**. Работа уходит в **AiKA-режимы** (`bulk-reader`, `code-writer`) на твоём Portal-экземпляре; модель задаётся при создании режима на стороне сервера |
| «если Claude будет читать файл 350+ строк» | ✅ | Точно: `SHUNT_MIN_LINES` по умолчанию **350**, настраивается переменной окружения |
| «сокращает расход токенов на 90 %» | ⚠️ | В README: *«Mean bulk-read savings: **90 %**»* и *«saving 82-94 % of tokens on large file reads»*. Верно **для чтения крупных файлов**, а не для сессии целиком. Плюс замер сделан **не тем, что лежит в репозитории** — см. ниже |
| «чуть ли не в ДЕСЯТКИ раз» | ⚠️ | 94 % — это 16 раз, но только на лучшем из четырёх сценариев. Средние 90 % — это 10 раз |
| Что «всё бесплатно» (пост обрывается на «Более того, всё…») | ❌ | Плагины — Apache-2.0, а вот `@spotify/portal-cli` — **Commercial License** |

---

## 💰 Главное условие: нужен платный Spotify Portal

Оба плагина — тонкая обёртка над `npx @spotify/portal-cli`. Достал `LICENSE.md` из npm-пакета (версия 0.4.3):

> **# Commercial License**
> Copyright (c) 2025 Spotify. All rights reserved.
> This software is part of the "Spotify Portal for Backstage". **To use it, you must obtain a license and agree to the License Terms.** Commercial licenses can be obtained at https://backstage.spotify.com/.

То есть репозиторий с плагинами открыт (Apache-2.0), но всё, что он делает, — вызывает проприетарный CLI, требующий подписки.

**Spotify Portal for Backstage** — это коммерческий внутренний портал разработчика на базе [Backstage](https://backstage.io). А **AiKA** («AI Knowledge Assistant») — один из premium-плагинов, идущих в комплекте; на сайте прямо: *«These **premium** Spotify plugins come with Portal. AiKA — Meet the AI Knowledge Assistant that knows what your org knows»*. Публичного прайса нет, на сайте только «Talk to us» и «Try Portal».

> [!info] Кому это адресовано
> Целевая аудитория — **компании, у которых уже развёрнут Spotify Portal**. Для них плагины действительно ценны: агент получает доступ к каталогу сервисов, владельцам, инцидентам и документации организации, а тяжёлое чтение уходит на дешёвый воркер внутри их же контура. Для одиночного разработчика без корпоративного Portal — не применимо вообще: ни `portal`, ни `shunt` не заработают.

---

## 🧠 Что на самом деле делает Shunt

Механика простая и, надо сказать, изящная — три слоя:

1. **Хуки** (`PreToolUse`) перехватывают `Read` и `Bash`. `check-file-size` блокирует чтение файла длиннее 350 строк, `check-bash-read` ловит `cat`/`head`/`tail`/`less`/`more` на больших файлах.
2. **Скрипты** `bulk-read` и `code-write` вызывают AiKA через одну команду `portal-cli actions aika:invoke-chat`.
3. **Скиллы** объясняют агенту, когда и как звать скрипты.

Проверил хук вживую на их же тестовом файле (`websocket-handler.ts`, 602 строки):

```json
{"decision": "block", "reason": "File is 602 lines (threshold: 350). Use the /bulk-reader skill
 to delegate this read to AiKA instead of reading it directly. If you need exact content for
 editing, re-read with an offset/limit for just the section you need."}
```

Пропускаются: точечные чтения с `offset`/`limit`, файлы меньше порога, несуществующие файлы, пайпы (`cat file | grep`) и редиректы.

Авторы честно перечислили, что **не** делегируется: отладка (нужно рассуждение, а не саммари), редактирование (нужен точный текст), мелкие файлы (накладные расходы съедают выгоду) и архитектурные решения.

> [!tip] Экономия не исчезает, а переезжает
> Формулировка в их же коде: *«Re-sending files is free where it matters, because the corpus goes to the worker model and never enters Claude's context»*. Ключевое — **«where it matters»**: токены экономятся в **контексте Claude**, а не вообще. Каждый уточняющий вопрос заново отправляет весь корпус файлов дешёвой модели, потому что `aika:invoke-chat` не хранит историю. В корпоративной установке за воркер платит организация — поэтому для неё это выгодно; но «расход токенов сократился в десять раз» и «счёт уменьшился в десять раз» — разные утверждения.

---

## 📊 Бенчмарк: цифры настоящие, но локально не воспроизводятся

Таблица из README:

| Сценарий | Строк | Без shunt | С shunt | Экономия |
| :--- | ---: | ---: | ---: | ---: |
| Один большой файл | 4 014 | 33 684 | 5 737 | 82 % |
| Исходник + тест | 7 408 | 75 990 | 4 148 | 94 % |
| Несколько файлов | 1 281 | 16 221 | 821 | 94 % |

Среднее по трём — ровно **90 %**, арифметика сходится. Но два уточнения:

**Замер сделан на чём-то другом.** README говорит: *«Tested against a 162K-line Java monorepo»*. А фикстуры, на которых работает опубликованный `evals/run.sh --benchmark`, — **три файла на TypeScript**:

| Файл в репозитории | Строк | Байт |
| :--- | ---: | ---: |
| `websocket-handler.ts` | 602 | 48 024 |
| `user-service.ts` | 35 | 1 051 |
| `order-service.test.ts` | 55 | 1 669 |

Посчитал «токены без shunt» их же методом (в `benchmarks.json` указано `chars / 4`): для первого сценария выходит **12 006** вместо 33 684, для пары «исходник + тест» — **680** вместо 75 990. Да и сам `benchmarks.json` описывает первый сценарий как «Read a **602-line** service», тогда как в таблице README напротив него стоит 4 014 строк. Вывод: цифры относятся к внутреннему Java-монорепо Spotify, и **повторить публикуемый результат на публичных фикстурах нельзя**.

**Токены оценены делением на четыре.** В `benchmarks.json` прямо: `"token_estimate": "chars / 4 (conservative approximation for code)"` — это грубая прикидка, а не подсчёт настоящим токенизатором.

---

## 👍 Инженерное качество — высокое

Тут придираться не к чему, и это стоит отметить:

- **51 тест, и они реально проходят.** Запустил `bash evals/run.sh` (Portal для этого не нужен) — `Total: 51 passed, 0 failed, 51 total`. Это 17 кейсов на хук `Read`, 17 на хук `Bash` и 17 на транспорт с подменённым `portal-cli`.
- **Скиллы дешёвые.** Посчитал через `tiktoken` (`o200k_base`): `name` + `description` всех восьми скиллов — **357 токенов**, то есть **0,18 %** окна в 200k. Постоянно в контексте висит очень мало.

| Скилл | name+desc | тело |
| :--- | ---: | ---: |
| `portal`: actions / doctor / feedback / search / service / setup | 38 / 46 / 50 / 44 / 62 / 42 | 202 / 504 / 352 / 182 / 275 / 594 |
| `shunt`: bulk-reader / code-writer | 36 / 39 | 91 / 125 |
| **Итого** | **357** | **2 325** |

- **Правильная гигиена секретов.** В `skills/setup/SKILL.md` первым пунктом: *«Never ask the user to paste access tokens, authorization codes, or other credentials into chat»*. Приятный контраст с тем, что попадается в чужих скиллах.
- **Честный раздел ограничений.** Авторы сами пишут, что у `code-writer` нет хук-принуждения, что запрос ограничен `ARG_MAX`, и что генерация может не уложиться в таймаут.

---

## ⚠️ Три подводных камня, если всё же ставить

**1. Нужен `jq`.** Хуки написаны на bash и парсят JSON через `jq`. Без него хук валится с `jq: command not found` (проверил) — правда, «fail open»: чтение всё равно разрешается, просто в вывод сыплются ошибки и экономии нет.

**2. На Linux лимит на делегирование втрое меньше, чем на macOS.** Запрос уходит через argv, а Linux дополнительно ограничивает **одиночный аргумент** 128 КиБ (`MAX_ARG_STRLEN`) независимо от общего `ARG_MAX` (у меня в системе он 2 МиБ). Поэтому в `aika.sh` захардкожено:

```bash
case "$(uname -s)" in
  Linux) SHUNT_MAX_PAYLOAD_BYTES=120000 ;;
  *)     SHUNT_MAX_PAYLOAD_BYTES=400000 ;;
esac
```

То есть за одно делегирование на Linux влезает **~117 КБ**. Их же тестовый `websocket-handler.ts` весит 48 КБ — двух таких файлов уже почти впритык. Большие пачки придётся дробить вручную.

**3. Без работающего Portal шунт делает только хуже.** Хук блокирует чтение и советует `/bulk-reader`, который без авторизации в Portal упадёт. Формально не смертельно — в тексте блокировки есть запасной путь («перечитай с offset/limit»), — но каждое чтение файла длиннее 350 строк превращается в постраничное. Если Portal нет, **ставить надо только `portal`… а он тоже без Portal не нужен**. Проще не ставить ни того, ни другого.

---

## 💻 По системам

Плагины ставятся средствами самого Claude Code, дистрибутив ни при чём:

```bash
claude plugin marketplace add spotify/portal-ai-plugins
claude plugin install portal@portal
claude plugin install shunt@portal      # опционально
# затем в новой сессии:
/portal:setup
```

Нативных зависимостей всего две — **Node.js** (для `npx @spotify/portal-cli`) и **jq**.

| Система | Что поставить |
| :--- | :--- |
| **Gentoo** (основная) | `emerge -av net-libs/nodejs app-misc/jq` — оба в ::gentoo есть и собираются из исходников |
| **Debian / Ubuntu** | `sudo apt install nodejs npm jq` |
| **Arch** (с июня 2026) | `sudo pacman -S nodejs npm jq` |
| **Entware / RT-AX56U** | ➖ нерелевантно: Claude Code на роутере не живёт. `jq` в Entware, кстати, есть (`jq`, `jq-full`), а `node` там v18.20.2 |

Codex и Cursor тоже поддержаны — в репозитории лежат `.codex-plugin/` и `.cursor-plugin/`, но **shunt пока только под Claude Code** (*«Claude Code only for now»*), потому что хуки — механизм Claude Code.

---

## 🎯 Итог

| | |
| :--- | :--- |
| **Что правда** | Плагины настоящие, от Spotify, Apache-2.0, инженерно аккуратные: 51 тест проходит, скиллы стоят 357 токенов, гигиена секретов на месте. Порог 350 строк — верный, 90 % экономии — их собственный опубликованный замер |
| **Что переврал пост** | «Portal кидает задачи дешёвым моделям» — Portal это корпоративный портал разработчика, делегирует только Shunt. «Gemini 2.5 Flash» — выдумка, в репозитории такой строки нет. «Сокращаем расход токенов на 90 %» — на 90 % сокращается чтение больших файлов, а не сессия |
| **Скрытое условие** | `@spotify/portal-cli` — **коммерческая лицензия**, нужна подписка на Spotify Portal for Backstage с включённым AiKA. Без неё оба плагина бесполезны |
| **Кому реально пригодится** | Командам, у которых Spotify Portal уже развёрнут. Всем остальным — разве что как **образец того, как устроен плагин с хуками**: хук на `PreToolUse`, скрипт с именованными аргументами, скилл-инструкция. Схема переносится на любой свой дешёвый бэкенд за вечер |

Сама идея — блокировать чтение крупных файлов хуком и отдавать их модели подешевле — рабочая и не требует Spotify: `hooks.json` с матчером на `Read`, свой скрипт вместо `bulk-read`, и вместо AiKA любой дешёвый провайдер из [подборки бесплатных API](../../ProxyLLM/%D0%91%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B5%20AI-API%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D1%81%20free-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BE%D0%BC%20%D0%BA%20LLM%20%28OpenRouter%2C%20Groq%2C%20Cerebras%20%D0%B8%20%D0%B4%D1%80.%29.md).

---

## 🔗 Связанные заметки

- Что такое хуки и плагины Claude Code: [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)
- Другой плагин на хуках, для сравнения устройства: [claude-code-prompt-improver](claude-code-prompt-improver%20%E2%80%94%20%D1%85%D1%83%D0%BA-%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20Claude%20Code%2C%20%D1%83%D0%BB%D1%83%D1%87%D1%88%D0%B0%D1%8E%D1%89%D0%B8%D0%B9%20%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D1%8B%20%C2%AB%D0%BD%D1%83%D0%B4%D0%B6%D0%B0%D0%BC%D0%B8%C2%BB%20%28%D1%8F%D1%81%D0%BD%D0%B5%D0%B5%20%D1%81%20%D0%BF%D0%B5%D1%80%D0%B2%D0%BE%D0%B3%D0%BE%20%D1%80%D0%B0%D0%B7%D0%B0%29%2C%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2.md)
- Ещё одно обещание экономии токенов, тоже с проверкой: [TencentDB Agent Memory (−61 %)](TencentDB%20Agent%20Memory%20%E2%80%94%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D1%81%D0%BE%20%D1%81%D0%B6%D0%B0%D1%82%D0%B8%D0%B5%D0%BC%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%C2%AB%E2%88%9261%25%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%C2%BB%29.md)
- Как считается «сколько скилл стоит в фоне»: [Diagram Design (206 токенов)](../../Skills/Diagram%20Design%20%28cathrynlavery%29%20%E2%80%94%2039%20%D1%82%D0%B8%D0%BF%D0%BE%D0%B2%20%D0%B4%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28206%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D1%88%D1%80%D0%B8%D1%84%D1%82%D1%8B%20%D0%B8%D0%B7%20Google%2C%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20Claude%20Code%29.md)
- Агент, где вопрос цены решается выбором модели, а не делегированием: [mini-swe-agent](../mini-swe-agent%20%E2%80%94%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%C2%AB%D0%B2%20100%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%C2%BB%20%28%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20190%20%D0%B8%20618%20%D0%9C%D0%91%20%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B5%D0%B9%3B%2074%25%20%D0%BD%D0%B0%20SWE-bench%20%D0%B4%D0%B0%D1%91%D1%82%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C%3B%20%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D1%8B%20%D0%BF%D0%BE%20%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E%20%D0%BD%D0%B5%D1%82%29.md)
- Дешёвые и бесплатные провайдеры для своего варианта делегирования: [Бесплатные AI-API](../../ProxyLLM/%D0%91%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B5%20AI-API%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D1%81%20free-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BE%D0%BC%20%D0%BA%20LLM%20%28OpenRouter%2C%20Groq%2C%20Cerebras%20%D0%B8%20%D0%B4%D1%80.%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/spotify/portal-ai-plugins](https://github.com/spotify/portal-ai-plugins) (Apache-2.0) · README шунта: [plugins/shunt](https://github.com/spotify/portal-ai-plugins/tree/main/plugins/shunt)
- CLI (коммерческая лицензия): [@spotify/portal-cli](https://www.npmjs.com/package/@spotify/portal-cli) · продукт: [backstage.spotify.com](https://backstage.spotify.com/) · [portal.spotify.com](https://portal.spotify.com)
- Апстрим-проект: [backstage.io](https://backstage.io) (Apache-2.0)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/27593)

#AI #Claude_Code #Плагины #Токены #Backstage #Хуки
