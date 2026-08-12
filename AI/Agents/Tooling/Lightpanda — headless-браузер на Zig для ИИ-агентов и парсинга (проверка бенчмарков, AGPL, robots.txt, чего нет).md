---
создал заметку: 2026-08-11T11:20:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Парсинг
  - Браузер
  - Zig
  - CDP
  - MCP
  - Опенсорс
Источник:
  - https://t.me/bugnotfeature/26646
  - https://github.com/lightpanda-io/browser
  - https://github.com/lightpanda-io/demo/blob/main/BENCHMARKS.md
  - https://lightpanda.io
---

# Lightpanda — headless-браузер на Zig для ИИ-агентов и парсинга

Разбор поста [@bugnotfeature/26646](https://t.me/bugnotfeature/26646) («Нашли имбу для парсинга и ИИ-агентов — ультралегкий браузер Lightpanda, который в 11 раз быстрее Chrome»). Проект **реальный и интересный**, но пост цитирует бенчмарк полуторагодовалой давности и умалчивает о трёх вещах, которые решают, можно ли вообще брать инструмент: **лицензия AGPL-3.0**, **beta-статус без рендеринга** и **выключенное по умолчанию соблюдение `robots.txt`**.

> [!info] Что это на самом деле
> `lightpanda-io/browser` — headless-браузер, написанный **с нуля на Zig**. Не форк Chromium и не патч WebKit. Внутри: загрузка по HTTP через **libcurl**, парсер HTML **html5ever** (из Servo), исполнение JS через **v8**, и — ключевое — **графического движка рендеринга нет вообще**.
>
> - Лицензия: **AGPL-3.0** + обязательный CLA для контрибьюторов
> - Статус: **Beta**, текущий релиз **0.3.6** (25 июля 2026), pre-1.0
> - 33,8k звёзд, 1,5k форков, ~79 открытых issue, активная разработка (коммиты ежедневно)
> - Интерфейсы: CDP-сервер (Puppeteer/Playwright), нативный **MCP-сервер**, agent-режим с LLM, CLI-дамп в HTML/Markdown
>
> *Данные проверены по GitHub API и README на 11 августа 2026.*

---

## 1. Проверка утверждений поста

| Утверждение поста | Вердикт | Как на самом деле |
| :--- | :--- | :--- |
| «в **11 раз** быстрее Chrome» | ⚠️ **устаревшее число** | «11x faster» — формулировка из README от **18 февраля 2025**. Текущий README самого вендора заявляет **~9x** (4,81 с против 46,70 с) |
| «ест в **9 раз** меньше ОЗУ» | ⚠️ **устаревшее и заниженное** | «9x less» — оттуда же, из февраля 2025. Сейчас вендор заявляет **~16x** (123 МБ против 2 ГБ), а при одном процессе разрыв ещё больше |
| «совместим с Playwright и Puppeteer» | 🟡 **частично** | Есть CDP-сервер. Puppeteer через `browserWSEndpoint` работает и есть в README. Playwright — только `connectOverCDP()`, и это **открытые issue**: [#3076](https://github.com/lightpanda-io/browser/issues/3076) (Playwright Test не запускается без костылей), [#1838](https://github.com/lightpanda-io/browser/issues/1838) (краш `CRSession._onMessage`) |
| «устанавливается одной командой через Docker» | ✅ **верно** | `docker run -d -p 127.0.0.1:9222:9222 lightpanda/browser:nightly`, образы под amd64 и arm64 |
| «ультралёгкий» | ✅ **верно** | 27 МБ на процесс в лучшем случае — против 1,3 ГБ у Chrome |
| «не перегружать сервер или ПК» | ✅ по ресурсам, ❌ по чужим серверам | Свой сервер — да. А вот **чужие** он перегружает: см. §6 |

Пост, по сути, скопировал маркетинговую врезку полуторагодовалой давности. Забавно, что при этом он **занизил** главное преимущество проекта — память.

---

## 2. Бенчмарк: что там на самом деле измеряли

Вендор публикует [полную методику](https://github.com/lightpanda-io/demo/blob/main/BENCHMARKS.md) — за это ему плюс, потому что цифры из неё интереснее, чем заголовок.

**Условия:** AWS EC2 **m5.xlarge**, свежая Ubuntu; краулер на Go с библиотекой `chromedp`; Google Chrome **143.0.7499.169** в headless; память через `smem` (с учётом shared pages). Обходятся **933 страницы** сайта `demo-browser.lightpanda.io/amiibo/`.

| Конкурентность | Lightpanda | Chrome | Выигрыш по времени | Выигрыш по памяти |
| :--- | :--- | :--- | :--- | :--- |
| 1 процесс / 1 вкладка | 51,68 с · 27,2 МБ | 82,83 с · 1,3 ГБ | **1,6x** | **~48x** |
| 2 | 29,79 с · 31,7 МБ | 53,11 с · 1,3 ГБ | 1,8x | ~42x |
| 5 | 11,70 с · 43,9 МБ | 45,66 с · 1,6 ГБ | 3,9x | ~37x |
| 10 | 6,76 с · 63,7 МБ | 45,62 с · 1,7 ГБ | 6,7x | ~27x |
| **25** | **4,81 с · 123,0 МБ** | **46,70 с · 2,0 ГБ** | **9,7x** | **~16x** |
| 100 | 5,23 с · 410,2 МБ | 69 мин · 4,2 ГБ | катастрофа у Chrome | ~10x |

> [!tip] Главный вывод, которого нет ни в посте, ни в README
> **«В 9–11 раз быстрее» — это не скорость обработки страницы, это пропускная способность.** При одном процессе Lightpanda быстрее Chrome всего в **1,6 раза** — потому что и там, и там основное время тратится на сеть и на тот же самый v8.
>
> Разрыв растёт из-за **памяти**: 27 МБ против 1,3 ГБ означает, что в тот же объём ОЗУ влезает в десятки раз больше параллельных экземпляров. Экономия памяти конвертируется в конкурентность, а конкурентность — в общую скорость обхода.
>
> Практический смысл: если тебе надо обойти **три страницы**, Lightpanda почти не выиграет. Если **сто тысяч** — выиграет очень заметно и на порядок дешевле по железу.

> [!caution] Оговорки к бенчмарку — честно
> - **Сайт-мишень принадлежит самому вендору** (`demo-browser.lightpanda.io/amiibo/`) — это каталожная демка, а не тяжёлый React/Angular-SPA. На реальном приложении с гидратацией, вебсокетами и ленивой подгрузкой картина будет другой.
> - **Строка «100 pages» в README неточна**: 123 МБ / ~5 с — это строка **25 процессов**, и страниц во всех прогонах 933, а не 100. Сравнение при этом честное (25 против 25), но подпись вводит в заблуждение.
> - **Разные модели параллелизма**: Chrome — вкладки в одном процессе, Lightpanda — отдельные процессы. Авторы это сами оговаривают.
> - README говорит `m5.large`, а сама методичка — `m5.xlarge`. Мелочь, но показывает, насколько бережно стоит относиться к маркетинговым врезкам.

---

## 3. Чего в Lightpanda нет (самое важное)

> [!danger] Это не «замена Chrome», а другой инструмент
> **Нет графического движка рендеринга.** Отсюда сразу:
> - ❌ **скриншоты** — нечего снимать;
> - ❌ **PDF-экспорт**, печать;
> - ❌ **canvas / WebGL**-рендеринг, визуальные регресс-тесты;
> - ❌ вычисленная геометрия — `getBoundingClientRect()`, реальный layout, «виден ли элемент на экране»;
> - ❌ всё, что построено на скриншотах: visual-RAG-подходы вроде [PixelRAG — RAG по скриншотам страниц](PixelRAG%20%E2%80%94%20RAG%20%D0%BF%D0%BE%20%D1%81%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D0%B0%D0%BC%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20HTML%20%28visual%20RAG%2C%20VLM-%D1%8D%D0%BC%D0%B1%D0%B5%D0%B4%D0%B4%D0%B8%D0%BD%D0%B3%D0%B8%2C%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20Claude%20Code%29.md), компьютерное зрение агента вроде [Cua Driver — компьютерное управление для ИИ-агентов](Cua%20Driver%20%E2%80%94%20%D1%84%D0%BE%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D0%B5%D1%80%20%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28computer%20use%2C%20MCP%29.md).
>
> Если твой пайплайн упирается в «сделай скриншот и отдай VLM» — Lightpanda не подойдёт **архитектурно**, а не «пока не подойдёт».

Остальное по чек-листу из README и открытых issue:

| Ограничение | Детали |
| :--- | :--- |
| **CORS не реализован** | [#2015](https://github.com/lightpanda-io/browser/issues/2015), открыт с 27 марта 2026. Единственный невыполненный пункт в списке фич README |
| **Сотни Web API отсутствуют** | Прямая цитата README: *«There are hundreds of Web APIs… Coverage will increase over time»* |
| **Beta, возможны краши** | *«You may still encounter errors or crashes»*. Версия 0.3.6 — до 1.0 далеко |
| **Утечка памяти** | `Frame.removeNode` отвязывает узлы, но не освобождает память — течёт на долгоживущих страницах (открытая issue от 14.05.2026) |
| **Только glibc** | На Alpine/musl бинарник падает с `cannot execute: required file not found`. Нужен образ `debian:bookworm-slim`/`ubuntu:24.04` или сборка из исходников |
| **Нет нативного Windows** | Только WSL2; компиляция под Windows — открытая issue |
| **Нет Android/Termux** | Bionic libc не подходит glibc-бинарнику (открытая issue) |
| **Только x86_64 и aarch64** | В релизах нет armv7 — см. §7 про роутер |

---

## 4. Лицензия: AGPL-3.0 — то, о чём пост молчит

> [!danger] AGPL-3.0 — это не «просто опенсорс»
> **GNU Affero GPL v3** отличается от обычной GPL одним пунктом, ровно под такой сценарий: если ты предоставляешь пользователям доступ к модифицированной версии **по сети** (SaaS, внутренний сервис, публичный API), ты обязан предоставить им **исходный код своей модификации**. «Мы не распространяем бинарник, у нас облако» от обязательства не спасает.
>
> Что это значит на практике:
> - **Просто запускать** немодифицированный Lightpanda и ходить в него по CDP из своего кода — обязательств по раскрытию твоего кода это само по себе не порождает: твой краулер — отдельная программа, общающаяся по сетевому протоколу.
> - **Патчить сам Lightpanda** и крутить его в своём сервисе — раскрывать патчи придётся.
> - **Линковать как библиотеку** (обсуждается в issue «Use as a C library») — вот тут AGPL пойдёт дальше и утянет за собой.
> - Во многих компаниях AGPL просто **в чёрном списке** юротдела, независимо от нюансов.
>
> Плюс **обязательный CLA** для контрибьюторов — типичная схема «open core»: права собираются в одну компанию, чтобы позже иметь возможность продавать коммерческую лицензию или сменить модель лицензирования. Не криминал, но помнить стоит: у проекта есть коммерческая компания и облачный тариф.
>
> Я не юрист, и это не юридическая консультация — но для сравнения: Puppeteer и Playwright под **Apache 2.0**, а Chromium — **BSD**. Разница принципиальная.

---

## 5. Телеметрия включена по умолчанию

```bash
export LIGHTPANDA_DISABLE_TELEMETRY=true
# в Docker:
docker run -d -e LIGHTPANDA_DISABLE_TELEMETRY=true -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

Прямая цитата README: *«By default, Lightpanda collects and sends usage telemetry»*. Отключается одной переменной, но по умолчанию — **включено**. Заодно: `LIGHTPANDA_DISABLE_CORE_DUMP` подавляет core dump'ы при крашах (в них может утечь содержимое страниц и куки).

---

## 6. `robots.txt` не соблюдается по умолчанию — и это уже вылилось в скандал

> [!danger] Флаг `--obey-robots` — **опциональный**
> Обрати внимание на все примеры в README: `--obey-robots` **везде передан явно**. Значит, по умолчанию его нет и `robots.txt` игнорируется.
>
> 6 августа 2026 в трекере появилась issue [#3156 «Lightpanda clients are currently attacking Haskell infrastructure»](https://github.com/lightpanda-io/browser/issues/3156):
> > *«The Haskell infrastructure team is currently battling a flood of Lightpanda clients scraping every link on their GitLab server, which has `robots.txt` configured to block them. Why is this not working as expected and why is respecting robots.txt disabled by default?»*
>
> На момент написания заметки issue **открыта**, 16 комментариев. То есть инструмент уже используется так, что кладёт публичную инфраструктуру опенсорс-проектов.

**Практические выводы:**

- Всегда передавай `--obey-robots`. Хочешь — заверни в алиас/врапер, чтобы не забыть.
- Ставь **rate limit и задержки** на своей стороне: Lightpanda настолько дешёвый, что 100 параллельных процессов запускаются «случайно», а чужой сервер этого не переживёт.
- Ставь честный `User-Agent` с контактом — чтобы админ мог написать тебе, а не банить подсеть.
- Юридически: в РФ парсинг **общедоступных** данных сам по себе не запрещён, но отдельно регулируются персональные данные (152-ФЗ), авторские права на контент БД (ГК РФ ст. 1334 — извлечение существенной части базы данных) и нарушение работы информационных систем при избыточной нагрузке. Пользовательское соглашение сайта — отдельный слой. То, что технически легко, не равно «можно».

---

## 7. Установка на твоих системах

| Система | Как ставить | Нюансы |
| :--- | :--- | :--- |
| **Gentoo** (основная) | **Ebuild'а в дереве нет** — собирать из исходников. Хорошая новость: нужная версия Zig **уже есть**: `dev-lang/zig-0.15.2` (README требует ровно `0.15.2`). Плюс `dev-lang/rust` (для html5ever) и зависимости сборки v8 | Именно твой сценарий — всё из исходников. Сборка v8 долгая и прожорливая (закладывай несколько ГБ ОЗУ и десятки минут). `make build` или `zig build -Doptimize=ReleaseFast run`. Можно вшить v8-снапшот: `zig build snapshot_creator -- src/snapshot.bin` |
| **Debian / Ubuntu** | Официальный `.deb` из релизов: `lightpanda_0.3.6_amd64.deb` / `_arm64.deb`. Либо бинарник из nightly | Самый простой путь. Сборка из исходников: `apt install xz-utils ca-certificates pkg-config libglib2.0-dev clang make curl git` + Rust |
| **Arch** (планируется) | AUR, **три пакета**: `lightpanda` (сборка из исходников, 0.3.6-2), `lightpanda-bin` (0.3.6-1), `lightpanda-nightly-bin`. `yay -S lightpanda` | Голосов у пакетов пока по нулям — AUR-мейнтейнер новый, PKGBUILD перед сборкой стоит прочитать |
| **Docker** (везде) | `docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly` | amd64 + arm64. ⚠️ Порт биндить **на `127.0.0.1`**, а не на `0.0.0.0`: открытый наружу CDP — это полноценное удалённое управление браузером без аутентификации |
| **Entware** (ASUS RT-AX56U) | ❌ **не заработает** | Роутер — **armv7**, а релизы собираются только под **x86_64** и **aarch64**. Плюс glibc-линковка (в Entware — musl) и 512 МБ ОЗУ на всё. Даже если пересобрать — v8 на 256 МБ flash не поместится. Роутер тут максимум прокси/транспорт к парсеру на нормальном хосте |

---

## 8. Как пользоваться

### Разовый дамп страницы

```bash
./lightpanda fetch --obey-robots --dump html \
    --log-format pretty --log-level info \
    https://example.com/

# сразу в markdown — удобно скармливать LLM
./lightpanda fetch --obey-robots --dump markdown https://example.com/

# управление ожиданием динамики
./lightpanda fetch --obey-robots --dump markdown \
    --wait-until networkidle --wait-selector "#content" --wait-ms 2000 \
    https://example.com/
```

### CDP-сервер + Puppeteer

```bash
./lightpanda serve --obey-robots --host 127.0.0.1 --port 9222
```

```js
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({ browserWSEndpoint: 'ws://127.0.0.1:9222' });
const context = await browser.createBrowserContext();
const page = await context.newPage();

await page.goto('https://example.com/', { waitUntil: 'networkidle0' });
const links = await page.evaluate(() =>
    Array.from(document.querySelectorAll('a')).map(a => a.getAttribute('href')));
console.log(links);

await page.close();
await context.close();
await browser.disconnect();
```

Playwright цепляется через `chromium.connectOverCDP('http://127.0.0.1:9222')`, но полноценный Playwright Test пока не гарантирован (см. §1).

### MCP-сервер — для ИИ-агентов

По stdio:

```json
{
  "mcpServers": {
    "lightpanda": { "command": "/path/to/lightpanda", "args": ["mcp"] }
  }
}
```

По HTTP, с изоляцией сессий между агентами:

```bash
lightpanda mcp --port 9223
# клиенты шлют JSON-RPC на http://host:9223/mcp
# заголовок Mcp-Session-Id: свой → изолированная сессия; одинаковый → общий контекст
# инструменты session_new / session_list / session_close; DELETE /mcp закрывает сессию
```

Подробнее про сам протокол — [MCP — серверы Model Context Protocol](MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md).

### Agent-режим и PandaScript

```bash
./lightpanda agent                                 # ключ API берётся из окружения
./lightpanda agent --task "какая топовая новость на news.ycombinator.com?"
./lightpanda agent --no-llm                        # REPL без модели
./lightpanda agent --provider gemini --task "..."
./lightpanda run session.js                        # воспроизвести записанный сценарий
```

Поддерживаются Anthropic, OpenAI, Gemini, Google Vertex AI, Hugging Face и локальные модели через Ollama.

> [!tip] PandaScript — самая недооценённая фича
> Результат сессии агента сохраняется командой `/save` как **PandaScript**: обычный JavaScript с несколькими нативными примитивами браузера. Дальше он гоняется через `lightpanda run script.js` — **детерминированно и без единого токена LLM**.
>
> Это правильный паттерн для продакшена: прототипируешь дорогой моделью один раз, а в бою крутится дешёвый воспроизводимый скрипт. Ровно то, чего не хватает большинству «агентов-парсеров», которые жгут токены на каждом запуске.

---

## 9. Когда брать, а когда нет

**Брать, если:**
- нужен **массовый** обход страниц с исполнением JS (краулер, индексатор, мониторинг цен, сбор датасета), и упираешься в RAM/стоимость железа;
- нужен дешёвый инструмент «дай текст страницы в markdown» для RAG-пайплайна или агента;
- нужен MCP-сервер, чтобы агент ходил в веб, и важна изоляция сессий;
- ты держишь много параллельных экземпляров — там выигрыш максимальный;
- AGPL для твоего сценария не проблема.

**Не брать, если:**
- нужны **скриншоты, PDF, визуальные тесты, canvas/WebGL** — архитектурно невозможно;
- нужен **e2e-тест реального UI**: без layout нельзя проверить, что кнопка действительно видна и кликабельна там, где ожидается;
- нужен **гарантированно совместимый** Playwright Test — пока нет;
- сайты защищены антиботом с фингерпринтингом: Lightpanda — не Chrome и палится иначе (см. [Fingerprint Detector — браузерный фингерпринтинг](../../../Apps/Browser-Extensions/Fingerprint%20Detector%20%E2%80%94%20%D0%B4%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%BE%D1%80%20%D0%B8%20%D1%81%D0%BF%D1%83%D1%84%D0%B5%D1%80%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%84%D0%B8%D0%BD%D0%B3%D0%B5%D1%80%D0%BF%D1%80%D0%B8%D0%BD%D1%82%D0%B8%D0%BD%D0%B3%D0%B0%20%28Chrome%2C%20mr-r3b00t%29.md));
- **AGPL** несовместима с политикой компании;
- нужна стабильность продакшена без сюрпризов — beta 0.3.x, краши и утечки в трекере есть.

**Разумная альтернатива при сомнениях:** Playwright/Puppeteer поверх обычного Chromium (Apache 2.0, полная совместимость, скриншоты) — дороже по железу, но предсказуемее. Lightpanda имеет смысл ставить туда, где именно масштаб стал проблемой.

---

## 10. Чек-лист перед внедрением

- [ ] Прочитать **LICENSE** (AGPL-3.0) и согласовать с тем, кто отвечает за лицензии.
- [ ] `--obey-robots` во **всех** вызовах, плюс свой rate limit и внятный User-Agent.
- [ ] `LIGHTPANDA_DISABLE_TELEMETRY=true`.
- [ ] CDP-порт — только на `127.0.0.1` или за файрволом; наружу не выставлять.
- [ ] Проверить на **своих** целевых сайтах, а не на демке вендора: тяжёлые SPA ведут себя иначе.
- [ ] Убедиться, что скриншоты/PDF в пайплайне не нужны.
- [ ] Зафиксировать версию (`0.3.6`, а не `nightly`) — API пока меняется.
- [ ] Для долгоживущих процессов — периодический рестарт: утечка памяти в трекере открыта.
- [ ] Базовый образ на glibc, если Docker свой.

---

## Связанные заметки

- [MCP — серверы Model Context Protocol](MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) — протокол, по которому Lightpanda отдаёт браузер ИИ-агентам.
- [Cua Driver — компьютерное управление для ИИ-агентов](Cua%20Driver%20%E2%80%94%20%D1%84%D0%BE%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D0%B5%D1%80%20%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28computer%20use%2C%20MCP%29.md) — противоположный подход: агент управляет **настоящим** десктопом и видит картинку.
- [PixelRAG — RAG по скриншотам страниц](PixelRAG%20%E2%80%94%20RAG%20%D0%BF%D0%BE%20%D1%81%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D0%B0%D0%BC%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20HTML%20%28visual%20RAG%2C%20VLM-%D1%8D%D0%BC%D0%B1%D0%B5%D0%B4%D0%B4%D0%B8%D0%BD%D0%B3%D0%B8%2C%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20Claude%20Code%29.md) — RAG по скриншотам страниц; с Lightpanda несовместим в принципе (нет рендеринга).
- [hh-ai-agent — ИИ-агент на Ollama+Playwright](../hh-ai-agent%20%28fikstt2%29%20%E2%80%94%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%B0%D0%B2%D1%82%D0%BE-%D0%BE%D1%82%D0%BA%D0%BB%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%BD%D0%B0%20HH.ru%20%28Ollama%2BPlaywright%29%20%2B%20%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20%D0%BA%D0%BE%D0%B4%D0%B0.md) — практический пример агента поверх Playwright, кандидат на такую замену.
- [OpenSERP — self-hosted SERP-API](../../../Security/OSINT/OpenSERP%20%E2%80%94%20self-hosted%20SERP-API%20%D0%B8%20CLI%20%28Google-Yandex-Baidu%20%D0%B8%20%D0%B4%D1%80.%29%20%D0%B4%D0%BB%D1%8F%20OSINT%2C%20LLM%20%D0%B8%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md) — self-hosted SERP-API: соседняя задача (выдача поисковика), те же вопросы права.
- [Fingerprint Detector — браузерный фингерпринтинг](../../../Apps/Browser-Extensions/Fingerprint%20Detector%20%E2%80%94%20%D0%B4%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%BE%D1%80%20%D0%B8%20%D1%81%D0%BF%D1%83%D1%84%D0%B5%D1%80%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%84%D0%B8%D0%BD%D0%B3%D0%B5%D1%80%D0%BF%D1%80%D0%B8%D0%BD%D1%82%D0%B8%D0%BD%D0%B3%D0%B0%20%28Chrome%2C%20mr-r3b00t%29.md) — как сайты определяют автоматизированный браузер.

## Ссылки

- Пост-источник: [@bugnotfeature/26646](https://t.me/bugnotfeature/26646)
- [github.com/lightpanda-io/browser](https://github.com/lightpanda-io/browser) — AGPL-3.0, Zig, 33,8k ★
- [Методика бенчмарков (BENCHMARKS.md)](https://github.com/lightpanda-io/demo/blob/main/BENCHMARKS.md)
- [lightpanda.io](https://lightpanda.io) · [документация agent-режима](https://lightpanda.io/docs/usage/agent) · [PandaScript](https://lightpanda.io/docs/usage/pandascript) · [MCP-сервер](https://lightpanda.io/docs/open-source/guides/mcp-server)
- [Docker Hub: lightpanda/browser](https://hub.docker.com/r/lightpanda/browser)
- Issue [#2015 — CORS не реализован](https://github.com/lightpanda-io/browser/issues/2015) · [#3156 — жалоба Haskell-инфраструктуры](https://github.com/lightpanda-io/browser/issues/3156) · [#3076 — совместимость с Playwright Test](https://github.com/lightpanda-io/browser/issues/3076)
- [Текст лицензии AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html)

#AI #Агенты #Парсинг #Браузер #Zig #CDP #MCP #Опенсорс
