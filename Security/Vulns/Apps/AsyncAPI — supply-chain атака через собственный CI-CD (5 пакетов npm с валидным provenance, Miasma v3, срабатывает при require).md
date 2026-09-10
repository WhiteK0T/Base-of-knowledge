---
создал заметку: 2026-09-10T10:00:00
author: WhiteK0T
tags:
  - Безопасность
  - supply-chain
  - npm
  - CI-CD
  - Node-js
  - RAT
Источник:
  - https://t.me/IzHmfluzM81OTAy/628
  - https://www.stepsecurity.io/blog/compromised-next-branch-pushes-malicious-asyncapi-generator-generator-helpers-and-generator-components-to-npm
  - https://research.jfrog.com/post/miasma-worm-returns-to-npm/
---

# 📦 AsyncAPI — когда вредонос публикует твой собственный CI/CD

**14 июля 2026** атакующий получил право пуша в два репозитория проекта **AsyncAPI** и не стал ничего публиковать сам: он просто закоммитил дроппер, а **штатные GitHub Actions проекта сами собрали, подписали и выложили заражённые пакеты в npm** — с валидными OIDC-аттестациями provenance. Ни одного украденного npm-токена в этой истории нет.

> [!danger] Почему это важнее обычного «увели токен»
> **Provenance подтверждает происхождение, а не содержимое.** Аттестация SLSA честно говорит: «этот пакет собран воркфлоу `release-with-changesets.yml` из ветки `next` репозитория `asyncapi/generator`». Всё правда. Она не говорит, что коммит, запустивший воркфлоу, был легитимным. Если ветка, запускающая релиз, принимает прямой пуш — доверенный конвейер выпустит вредонос с безупречной подписью.

---

## ⏱️ Хронология (UTC, 14.07.2026)

| Время | Что произошло |
| :--- | :--- |
| **06:58** | Пуш коммита `3eab3ec9` прямо в ветку `next` репозитория `asyncapi/generator`. Автор коммита — незаданный дефолт git: **«Your Name» `<you@example.com>`**, аккаунт GitHub не резолвится (`invalid-email-address`), коммит не подписан |
| **07:10** | Через 12 секунд после пуша сработал `release-with-changesets.yml` и опубликовал **три пакета** через npm OIDC trusted publisher |
| **07:51–07:56** | Тот же атакующий с той же подписью начал пушить в `asyncapi/spec-json-schemas`, ветка `master`. Коммит `36269ce8` с сообщением `fix: correct JSON schema` внедрил дроппер в `index.js` — **через 15 минут после публичного раскрытия первой атаки** |
| **08:06 / 08:30** | Воркфлоу `if-nodejs-release.yml` (срабатывает на пуш в `master` с префиксом `fix:` или `feat:`) опубликовал `@asyncapi/specs@6.11.2-alpha.1`, затем `6.11.2` |
| **11:12–11:18** | Все пять вредоносных версий сняты с npm |

### Затронутые версии

| Пакет | Вредоносная версия | Безопасная | Окно доступности |
| :--- | :--- | :--- | ---: |
| `@asyncapi/generator` | 3.3.1 | 3.3.0 | 4 ч 02 мин |
| `@asyncapi/generator-helpers` | 1.1.1 | 1.1.0 | 4 ч 02 мин |
| `@asyncapi/generator-components` | 0.7.1 | 0.7.0 | 4 ч 03 мин |
| `@asyncapi/specs` | 6.11.2 | 6.11.1 | 2 ч 48 мин |
| `@asyncapi/specs` | 6.11.2-alpha.1 | 6.11.1 | 3 ч 12 мин |

**Проверил сам в реестре npm (10.09.2026):** все пять версий действительно unpublished, `latest` сейчас — `generator@3.4.0`, `generator-helpers@1.1.0`, `generator-components@0.8.0`, `specs@6.11.1`. Свежая установка безопасна.

> [!warning] Транзитивная поверхность больше прямой
> `@asyncapi/specs` — это **2,66 млн загрузок в неделю**, и он тянется как прямая зависимость `@asyncapi/parser` (**970 тыс./нед.**) по диапазону `^6.11.1`, который **включает вредоносную 6.11.2**. Проверил актуальный `@asyncapi/parser@3.6.3` — диапазон `^6.11.1` там **до сих пор**. То есть словить заражённую версию можно было, вообще не зная про существование AsyncAPI.

---

## 🧬 Как работал дроппер

Ключевая особенность: **это не install-скрипт**.

```
require() поражённого модуля
   └─ Stage 1: spawn("node", ["-e", <stage2>], {detached, stdio:"ignore", windowsHide})
        └─ Stage 2: скачать sync.js с публичного IPFS-шлюза → положить в скрытый каталог «NodeJS»
             └─ Stage 3: Miasma v3 — 3,08 МБ упакованного Node.js-приложения
```

- **Ни `preinstall`, ни `install`, ни `postinstall`** ни в одном из `package.json`. `npm install --ignore-scripts` тут не помогает вообще. JFrog предполагает, что так сделано намеренно — как обход **npm v12, где выполнение скриптов заблокировано по умолчанию**.
- Код внедрён **в тело модуля** трёх легитимных файлов: `apps/generator/lib/templates/config/validator.js`, `packages/helpers/src/utils.js`, `packages/components/src/utils/ErrorHandling.js`. Node вычисляет его сразу при загрузке — ждать вызова функции не нужно.
- Один и тот же обфусцированный блок (~**7,7 КБ**, obfuscator.io) вписан **в одну строку и сдвинут вправо примерно 881 пробелом** (JFrog; StepSecurity оценивает «около тысячи»), чтобы он ушёл за край в side-by-side диффе. Приём против глазного ревью, простой и действенный.
- Пути сброса: `~/.local/share/NodeJS/sync.js` (Linux), `~/Library/Application Support/NodeJS/sync.js` (macOS), `%LOCALAPPDATA%\NodeJS\sync.js` (Windows).

> [!tip] Практическое следствие для скоупинга инцидента
> Наличие версии в lock-файле или в кэше **не равно компрометации**: код не исполняется при установке. Но и обратное верно — он может сработать **сильно позже**, когда сборка или CI впервые загрузит библиотеку. Проверять надо не «стояла ли версия», а «загружался ли модуль».

---

## 🐍 Что такое Miasma v3 — и чего он на самом деле делал

Здесь важно не перегнуть. В расшифрованном пейлоаде действительно есть модули на все случаи жизни: сбор учёток (130+ типов файлов), боковое движение по локальной сети, метаморфный мутатор, распространение через npm и **отравление ИИ-инструментов** (`recon/ai-tool-poisoner.js` — Claude Code, GitHub Copilot, Cursor). Шесть независимых каналов C2: HTTP, Nostr-реле, IPFS, BitTorrent DHT, libp2p GossipSub и дед-дроп в Ethereum.

**Но JFrog прямо пишет, что в этой кампании большинство этих возможностей выключены в «запечённой» конфигурации:**

> Although the codebase also contains credential theft, package propagation, AI-tool poisoning, and metamorphic mutation modules, **those capabilities are disabled** in this deployment's baked configuration… the observed configuration uses it primarily as a persistent **remote access trojan (RAT)** rather than a self-spreading npm worm.

Это согласуется с параметрами конфига, которые вытащил StepSecurity: `safeMode: true`, `propagate.npm: false`, `batch.defaultStrategy: CANARY` (сначала 5 % целей, потом волнами по 100), кампания `miasma-train-p1`.

**Что было включено:** персистентность (systemd, crontab, launchd, Registry Run), связь с C2 и **произвольное выполнение команд** через `comm/shell-executor.js`. Этого более чем достаточно: любые данные и учётки, доступные скомпрометированному пользователю, доступны и оператору.

| Инфраструктура | Значение |
| :--- | :--- |
| Основной C2 | `http://85.137.53.71:8080` (команды), `:8081` (выгрузка), `:8091` (управление прокси) |
| Nostr | `wss://relay.damus.io`, `wss://relay.nostr.com/` |
| BitTorrent DHT | `router.bittorrent.com:6881`, `dht.transmissionbt.com:6881` |
| Ethereum dead-drop | `0x12c37A86a0Ed0beBe5d1d6a43E42f07860eAc710` |
| IPFS CID | `QmQobZSp1wRPrpSEQ56qnyq7ecZh5Bg5k1fnjt4SUwwHb9` (generator), `Qmet4fhsAaWMBUxNDfREHwgiyDeSWy4YSYs9wiKUW5jGyf` (specs) |

---

## 🔁 Это уже второй заход на те же пакеты

JFrog отмечает: те же четыре имени пакетов засветились в кампании **Shai-Hulud (ноябрь 2025)** — но с другими версиями (`generator@2.8.5/2.8.6`, `specs@6.8.2/6.8.3/6.9.1/6.10.1` и т.д.), другой доставкой и другой инфраструктурой. Те старые вредоносные версии из npm давно удалены. А июньская волна Miasma 2026 шла через install-хуки в захваченных пакетах `@redhat-cloud-services`.

То есть один и тот же проект пробивают повторно, а семейство вредоноса эволюционирует от install-хуков к load-time триггеру.

---

## 🧯 Что делать (даже если ты не пользуешься AsyncAPI)

**Если версии могли попасть:**

1. **Пересобрать lock-файл.** Версии сняты с npm, свежая установка их не подтянет, но lock, созданный между 07:10 и 11:18 UTC 14.07.2026, всё ещё может их пинить:
   ```bash
   rm package-lock.json   # или yarn.lock / pnpm-lock.yaml
   npm install
   ```
   Для транзитива через `@asyncapi/parser` — форсировать через `overrides`:
   ```json
   "overrides": { "@asyncapi/specs": "6.11.1" }
   ```
2. **Поискать файл сброса** по путям выше и убить осиротевшие процессы `node`, запущенные из каталога `NodeJS` в домашней папке:
   ```bash
   ls -la ~/.local/share/NodeJS/ 2>/dev/null
   pgrep -af 'NodeJS/sync.js'
   ```
3. **Ротировать всё, что лежало на машине:** npm-токены, GitHub PAT и deploy-ключи, SSH-ключи, `~/.aws/credentials`, пароли и куки браузеров.
4. **Проверить сетевые логи** сборок за окно: обращения к `ipfs.io`, к `85.137.53.71`, к bootstrap-узлам BitTorrent DHT, к Nostr-реле.

**Выводы на будущее — их три, и они не про AsyncAPI:**

- **Ветка, с которой уезжает релиз, должна быть защищена как продакшен.** Прямой пуш в `next`/`master`, запускающий публикацию без ревью, — это и есть вся уязвимость. Trusted Publishing убрал долгоживущие токены, но не заменил branch protection.
- **`--ignore-scripts` больше не панацея.** Полезная привычка, но вредонос научился жить в теле модуля.
- **Cooldown на свежие версии** — самая простая защита с хорошим КПД: почти все такие пакеты выявляют за часы, а здесь окно было **меньше четырёх с половиной часов**.

> [!caution] Отдельно про ИИ-ассистентов
> Модуль отравления ИИ-инструментов в этой кампании был выключен — но он существует и нацелен в том числе на **[Claude Code](../../../AI/Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)**. Если поражённая машина использовалась для ИИ-ассистированной разработки, код, написанный в том окне, стоит перечитать глазами. Общее правило то же, что и всегда: агент выполняется с твоими правами и видит твоё окружение.

---

## 💻 Проверка на своих системах

| Система | Что делать |
| :--- | :--- |
| **Gentoo** (основная) | Проект на Node? Проверь lock-файлы: `grep -rn "6\.11\.2\|3\.3\.1\|1\.1\.1\|0\.7\.1" package-lock.json`. Node из портежа — `net-libs/nodejs`, подробности в [заметке про Node.js](../../../Programming/JavaScript/NodeJS/Node.js%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9%20JavaScript-%D1%80%D0%B0%D0%BD%D1%82%D0%B0%D0%B9%D0%BC%20%28V8%2C%20event%20loop%2C%20npm%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%D0%B8%20%D0%B4%D1%80.md) |
| **Debian / Ubuntu** | То же самое; плюс проверить `~/.npm/_cacache` — кэш мог сохранить тарболл, хотя сам по себе он безвреден без загрузки модуля |
| **Arch** (с июня 2026) | Аналогично. Заодно вспомни [Atomic Arch](../Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md) — тот же класс атаки, только через AUR |
| **Entware / RT-AX56U** | ➖ нерелевантно: `node` там v18.20.2 и npm-проектов на роутере нет. Но если когда-нибудь заведёшь — те же правила |

---

## 🔗 Связанные заметки

- Такая же supply-chain атака, только через AUR: [Atomic Arch](../Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md)
- Про сам рантайм и npm: [Node.js — серверный JavaScript-рантайм](../../../Programming/JavaScript/NodeJS/Node.js%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9%20JavaScript-%D1%80%D0%B0%D0%BD%D1%82%D0%B0%D0%B9%D0%BC%20%28V8%2C%20event%20loop%2C%20npm%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%D0%B8%20%D0%B4%D1%80.md)
- Про ИИ-ассистента, которого целит модуль отравления: [Claude Code — гайд](../../../AI/Agents/Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)

## 🔗 Ссылки

- Разбор StepSecurity (хронология, деобфускация, IoC): [stepsecurity.io](https://www.stepsecurity.io/blog/compromised-next-branch-pushes-malicious-asyncapi-generator-generator-helpers-and-generator-components-to-npm)
- Разбор JFrog (Miasma v3, сравнение с Shai-Hulud): [research.jfrog.com](https://research.jfrog.com/post/miasma-worm-returns-to-npm/)
- Репозитории: [asyncapi/generator](https://github.com/asyncapi/generator) · [asyncapi/spec-json-schemas](https://github.com/asyncapi/spec-json-schemas)
- Источник новости: [@Mr0x45xploit](https://t.me/IzHmfluzM81OTAy/628)

#Безопасность #supply-chain #npm #CI-CD #Node-js #RAT
