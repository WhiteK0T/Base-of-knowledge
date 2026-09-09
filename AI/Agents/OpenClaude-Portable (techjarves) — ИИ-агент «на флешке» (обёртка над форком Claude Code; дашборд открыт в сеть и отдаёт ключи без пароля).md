---
создал заметку: 2026-09-09T23:55:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - Безопасность
  - Портативный_софт
  - Node-js
  - Лицензии
Источник:
  - https://t.me/bugnotfeature/27581
  - https://github.com/techjarves/OpenClaude-Portable
  - https://github.com/Gitlawb/openclaude
---

# 🔌 OpenClaude-Portable — «ИИ-агент на флешке»: что это на самом деле

**OpenClaude-Portable** ([github.com/techjarves/OpenClaude-Portable](https://github.com/techjarves/OpenClaude-Portable)) — набор launcher-скриптов, который разворачивает кодинг-агента прямо в своей папке: скачивает Node.js, ставит движок из npm, хранит настройки и ключи рядом. **1374★, 441 форк, MIT**, создан 30.04.2026.

> [!danger] Коротко — прежде чем втыкать флешку в чужой компьютер
> Три вещи, которых нет в посте.
> **Первое:** это **не самостоятельный агент**, а обёртка (17 файлов) над сторонним движком `@gitlawb/openclaude`, а тот, по его же файлу LICENSE, — **производная от проприетарного Claude Code**, распространяемая **без разрешения Anthropic**. Слово «опенсорсный» тут работает только для скриптов-обёртки.
> **Второе:** встроенный веб-дашборд **слушает все сетевые интерфейсы**, без пароля, с `Access-Control-Allow-Origin: *`, и по `GET /api/config` **отдаёт твои API-ключи в открытом виде**. Проверил вживую — сокет `*:3000`, хотя в консоль он пишет «running at http://localhost:3000».
> **Третье:** ветка `main`, которую ты клонируешь, **не менялась с 07.05.2026**. Все исправления (bind на 127.0.0.1, скрытие ключей, свежий Node, проверка контрольных сумм) лежат в ветке `dev` и **не влиты**.

---

## ✅ Проверка заявлений из поста

| Заявление | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «опенсорсный ИИ-агент» | ⚠️ | Обёртка — честный MIT. Но сам агент — `@gitlawb/openclaude`, и в его LICENSE написано: *«This project does not have Anthropic's authorization to distribute their proprietary source»*. GitHub классифицировать лицензию не может и показывает **NOASSERTION** |
| «релизнулся буквально недавно» | ❌ | Репозиторий создан 30.04.2026, **все 17 коммитов `main` уложились в неделю** (30.04–07.05.2026), дальше тишина четыре месяца. **Релизов — ноль**, скачивать нечего, только клон или ZIP |
| «собрал 1,3 тысячу звёзд» | ✅ | 1374★ — верно. Но звёзды принадлежат **обёртке из 17 файлов**; у движка, который делает всю работу, — **33 043★** |
| «не требует установки» | ⚠️ | Установка есть, просто в свою папку: первый запуск качает **Node.js ~25 МБ** и делает `npm install @gitlawb/openclaude@latest` (**31,3 МБ**). Нужен интернет и `curl`, на медленной флешке авторы сами обещают 10–15 минут |
| «запускается на **ЛЮБОМ** компе» | ❌ | В `start.sh` явно: только **linux/darwin** и только **x86_64/arm64**, иначе `Unsupported Architecture`. Плюс официальные сборки Node — glibc-only, на Alpine/musl не заведётся |
| «поддерживает 9 нейронок» | ✅ | Ровно 9: NVIDIA NIM, DeepSeek, OpenRouter, Gemini, Anthropic, OpenAI, Ollama, LM Studio, Custom OpenAI-совместимый |
| «настройки, ключи и история сохраняются прямо в папке, локально» | ⚠️ | Формально да — `HOME`, `XDG_*` и `CLAUDE_CONFIG_DIR` переопределяются в `data/`. Но «локально» ≠ «безопасно»: ключ лежит **открытым текстом** в `data/ai_settings.env` без `chmod`, а дашборд раздаёт его по сети |
| «совместим с Windows/Mac/Linux» | ✅ | Да, есть `START.bat` и `start.sh` |

---

## 🧅 Три слоя, о которых пост не говорит

```
пост  →  OpenClaude-Portable (17 файлов, 1374★, MIT)   ← про это заметка
             └── npm @gitlawb/openclaude@latest (31,3 МБ, 33 043★)
                     └── производная от Claude Code (Anthropic, проприетарный)
```

Обёртка не пишет ни агента, ни поддержку моделей — она скачивает Node, ставит npm-пакет и подставляет переменные окружения. Вся функциональность, включая «9 нейронок», — из движка. Забавная деталь: в описании репозитория на GitHub стоит *«Run **Claude Code** from a USB drive»*, хотя Claude Code там нет вообще.

---

## ⚖️ Лицензия — главный сюрприз

Файл `LICENSE` движка стоит прочитать целиком, там всё сказано прямым текстом:

> **NOTICE**
> This repository contains code derived from **Anthropic's Claude Code CLI**.
> The original Claude Code source is **proprietary software**: Copyright (c) Anthropic PBC. All rights reserved. Subject to Anthropic's Commercial Terms of Service.
> Modifications and additions by OpenClaude contributors are offered under the MIT License **where legally permissible** […]
> The underlying derived code remains subject to Anthropic's copyright. **This project does not have Anthropic's authorization to distribute their proprietary source. Users and contributors should evaluate their own legal position.**

И в README движка: *«"Claude" and "Claude Code" are trademarks of Anthropic PBC»*, *«not affiliated with, endorsed by, or sponsored by Anthropic»*.

При этом в шапке README висит бейдж **`license MIT`** — и именно его видит большинство. GitHub, разбирая настоящий файл, ставит `NOASSERTION`.

> [!warning] Что это значит практически
> Личный эксперимент дома — одно. Принести это на флешке на рабочий компьютер, где есть политика по лицензиям на ПО, — совсем другое: авторы сами пишут, что права на распространение у них нет. Оценивать риск придётся самому, готового «MIT, всё чисто» тут нет.

---

## 🔓 Дашборд: открыт в сеть и раздаёт ключи

Это самая серьёзная находка, и она проверяется за минуту.

**Что в коде** (`dashboard/server.mjs`, ветка `main`): `const PORT = 3000;`, а ниже — `server.listen(PORT, callback)`. У `listen` **не задан адрес**, значит Node слушает все интерфейсы, а не петлевой. Сообщение в консоли «Dashboard running at http://localhost:3000» вводит в заблуждение.

**Проверил вживую** — запустил сервер и посмотрел сокет:

```
$ ss -ltn
State   Recv-Q  Send-Q   Local Address:Port   Peer Address:Port
LISTEN  0       511                *:3000              *:*
```

`*:3000`, а не `127.0.0.1:3000`. Запрос отвечает `HTTP/1.1 200 OK` с заголовком `Access-Control-Allow-Origin: *`.

**Аутентификации нет нигде** — ни токена, ни пароля, ни проверки Origin. При этом открыты, в частности:

| Эндпоинт | Что делает |
| :--- | :--- |
| `GET /api/config` | возвращает разобранный `ai_settings.env` — **вместе с `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`** |
| `GET /api/config/export` | отдаёт файл настроек целиком |
| `POST /api/config/import` | **перезаписывает** файл настроек присланным содержимым |
| `POST /api/agent/approve` | подтверждает ожидающий вызов инструмента |
| `POST /api/workdir` | меняет рабочий каталог агента |

А среди инструментов агента есть `execute_command`, исполняемый через `execSync`. Подтверждение на запись (`WRITE_TOOLS` — это `write_file` и `execute_command`) требуется, но приходит оно по тому же незащищённому HTTP.

> [!danger] Почему это особенно плохо именно здесь
> Весь смысл продукта — «носи на флешке и втыкай в любой компьютер». То есть типичная среда использования — **чужая или публичная сеть**: коворкинг, офис, кафе, общага. Пока открыт дашборд, любой в той же сети может забрать ключи от твоих платных API, подменить `OPENAI_BASE_URL` на свой сервер и читать все дальнейшие запросы, и дотянуться до выполнения команд на машине.

### Как закрыть

1. **Не открывать дашборд.** Пункты меню 1 и 2 — терминальный режим, сеть не слушается вообще. Проблема только в пункте 3.
2. **Однострочная правка**, если дашборд нужен: в `dashboard/server.mjs` добавить адрес первым аргументом после порта — `server.listen(PORT, '127.0.0.1', ...)`. Ровно так это сделано в ветке `dev`.
3. **Проверить у себя** после запуска: `ss -ltn | grep 3000` — должно быть `127.0.0.1:3000`, а не `*:3000`.
4. Заблокировать порт снаружи: `iptables -A INPUT -p tcp --dport 3000 ! -i lo -j DROP`.

### Ключи

`ai_settings.env` пишется обычным перенаправлением в файл — **`chmod` в скриптах нет вообще** (единственный `chmod` во всём репозитории — `chmod +x` для бинарника Ollama). На ext4 файл получит права по umask, обычно `644`, то есть читаемый любым пользователем машины. А на флешке с FAT32/exFAT прав нет в принципе — ключ читает кто угодно, кто взял флешку в руки. Отдельного шифрования или пароля на хранилище нет.

---

## 🧟 Что ещё устарело в `main`

- **Node.js прибит к 22.14.0** (вышла 11.02.2025). В ветке 22.x с тех пор **17 релизов**, актуальная — 22.23.2 (28.07.2026), а текущая LTS вообще 24.21.0. Часть этих релизов — с исправлениями безопасности.
- **Контрольные суммы не проверяются.** Архив Node качается с `nodejs.org` (и запасным `r2.nodejs.org`) по HTTPS, но `sha256sum`/`shasum` в скриптах `main` не встречается ни разу.
- **Движок ставится как `@latest`**, без пина версии и без lock-файла: `npm install @gitlawb/openclaude@latest --no-audit`. Каждая новая установка тянет то, что сейчас лежит в npm.
- **README описывает файлы, которых нет.** В схеме проекта фигурирует `RESUME.bat` — в `main` его не существует.
- 17 открытых issue, и типовые заголовки говорят сами за себя: «OpenClaude Engine install is incomplete», «not able to open the start.bat», «unable to connect the model», «Failed to Create file».

---

## ✅ Ветка `dev` чинит почти всё — но её не влили

Справедливости ради: автор всё это уже исправил. В `dev` (3 коммита впереди, 50 изменённых файлов, последний — 09.09.2026):

| Проблема в `main` | Как в `dev` |
| :--- | :--- |
| `listen` без адреса — все интерфейсы | `server.listen(port, '127.0.0.1', resolve)` |
| `GET /api/config` отдаёт ключ | `publicConfig()` вырезает поле `key`, оставляя только `hasKey: true/false` |
| ключи утекают в вывод | добавлена `redact()` — вычищает ключи и шаблоны `sk-ant-`, `sk-or-`, `sk-` |
| произвольный base URL | `validateBaseURL()` требует HTTPS для удалённых адресов |
| Node 22.14.0 без проверки | `NODE_VERSION="22.23.2"` **и проверка `sha256sum`** |
| тестов нет | появились `tests/` и workflow `.github/workflows/test.yml` |

Плюс код разложен по `lib/` вместо одного файла на 1085 строк.

**Но `main` остаётся прежним.** Кнопка «Code → Download ZIP», `git clone` без `-b dev` и любой гайд из интернета дадут именно уязвимую версию. Если всё же ставить — то `git clone -b dev`.

---

## 👍 Что сделано хорошо

Чтобы не выглядело односторонне:

- **Изоляция конфигов реальная.** `HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME` и `CLAUDE_CONFIG_DIR` переопределяются в `data/` — дочерние процессы действительно не гадят в домашний каталог. Ollama тоже качается в `data/ollama/`.
- **Идея speed-proxy толковая.** `tools/local-proxy.js` режет системный промпт движка с ~10 000 токенов до ~300 перед отправкой в Ollama — на CPU это разница между «минута до первого токена» и «десять секунд». Приём рабочий сам по себе, независимо от этого проекта.
- **Режимы разделены честно.** «Limitless Mode» — это ровно `--dangerously-skip-permissions`, и в меню он подсвечен красным с предупреждением «Commands will execute without confirmation!». Автовыбор через 10 секунд — Normal Mode, а не Limitless.
- Подбор провайдеров вменяемый: есть бесплатные пути (NVIDIA NIM, бесплатные модели OpenRouter, Gemini) и полностью офлайновый (Ollama, LM Studio).

---

## 💻 По системам

Пакета нигде нет — это набор скриптов, ставится клонированием.

### Gentoo (основная)

```bash
git clone -b dev https://github.com/techjarves/OpenClaude-Portable.git   # именно dev
cd OpenClaude-Portable && chmod +x start.sh && ./start.sh
```

Скрипт всё равно скачает свой Node 22.x в `engine/`. Если хочется своего, собранного из исходников, — запускать движок напрямую, минуя обёртку:

```bash
emerge -av net-libs/nodejs        # свой Node вместо скачанного бинаря
npx @gitlawb/openclaude@0.30.0    # версию лучше пинить явно
```

Так отпадают и непроверенный бинарь Node, и дашборд как класс. Юридический вопрос с лицензией движка при этом никуда не девается.

### Debian / Ubuntu

```bash
sudo apt install curl nodejs npm
git clone -b dev https://github.com/techjarves/OpenClaude-Portable.git
```

`curl` — единственное явное требование скрипта. Если дашборд всё-таки открываешь на `main`-версии, закрой порт: `sudo ufw deny 3000`.

### Arch (с июня 2026)

```bash
sudo pacman -S curl nodejs npm
git clone -b dev https://github.com/techjarves/OpenClaude-Portable.git
```

В AUR пакета нет. Проверка после запуска дашборда — `ss -ltn | grep 3000`.

### Entware / ASUS RT-AX56U (armv7, 512 МБ RAM, 256 МБ flash)

❌ **Отказ на старте.** `start.sh` принимает только `x86_64`/`amd64` и `arm64`/`aarch64`; для armv7 сразу `[ERROR] Unsupported Architecture`. Даже если обойти проверку — сборок Node 22 под armv7 у nodejs.org нет, а в Entware лежит `node v18.20.2`, чего движку недостаточно. Плюс 31,3 МБ npm-пакета и кэш npm на 256 МБ flash.

Роутер здесь может быть только **хранилищем**: положить папку на USB-диск, подключённый к RT-AX56U, и забирать её на нормальную машину.

---

## 🎯 Итог

| | |
| :--- | :--- |
| **Идея** | Хорошая и рабочая: полностью переносимая папка с агентом, своим Node, своими конфигами и офлайн-моделями. Изоляция от домашнего каталога сделана честно |
| **Реализация в `main`** | Дашборд открыт на все интерфейсы без пароля и отдаёт API-ключи; ключи лежат открытым текстом без `chmod`; Node 22.14.0 без проверки контрольных сумм; движок ставится `@latest`. И это ровно та ветка, которую скачивают |
| **Юридически** | Движок — производная проприетарного Claude Code, распространяемая **без разрешения Anthropic** по признанию самих авторов. «Опенсорс» относится только к скриптам-обёртке |
| **Если всё же пробовать** | `git clone -b dev`, терминальный режим вместо дашборда, ключ от **дешёвого или бесплатного** провайдера (NVIDIA NIM, OpenRouter free, Gemini), а не боевой ключ от Anthropic/OpenAI. И не на чужом компьютере в чужой сети |

Если нужен именно портативный агент — практичнее взять что-то без проприетарной родословной: [mini-swe-agent](mini-swe-agent%20%E2%80%94%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%C2%AB%D0%B2%20100%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%C2%BB%20%28%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20190%20%D0%B8%20618%20%D0%9C%D0%91%20%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B5%D0%B9%3B%2074%25%20%D0%BD%D0%B0%20SWE-bench%20%D0%B4%D0%B0%D1%91%D1%82%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C%3B%20%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D1%8B%20%D0%BF%D0%BE%20%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E%20%D0%BD%D0%B5%D1%82%29.md) ставится в venv, который так же можно носить на флешке, а модель подключается любая.

---

## 🔗 Связанные заметки

- Минималистичный агент без юридических вопросов, тоже под любую модель: [mini-swe-agent](mini-swe-agent%20%E2%80%94%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%C2%AB%D0%B2%20100%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%C2%BB%20%28%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20190%20%D0%B8%20618%20%D0%9C%D0%91%20%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B5%D0%B9%3B%2074%25%20%D0%BD%D0%B0%20SWE-bench%20%D0%B4%D0%B0%D1%91%D1%82%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C%3B%20%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D1%8B%20%D0%BF%D0%BE%20%D1%83%D0%BC%D0%BE%D0%BB%D1%87%D0%B0%D0%BD%D0%B8%D1%8E%20%D0%BD%D0%B5%D1%82%29.md)
- Оригинал, от которого произошёл движок: [Claude Code — гайд](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)
- Ещё одна обвязка «чужие модели в интерфейсе Claude Code»: [free-claude-code (FCC)](../ProxyLLM/free-claude-code%20%28FCC%29%20%E2%80%94%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%20%D0%B2%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81%D0%B5%20Claude%20Code%20%281%2C3%20%D0%BC%D0%BB%D1%80%D0%B4%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%BE%D0%B2%2C%20%D0%B0%20%D0%BD%D0%B5%201%2C5%3B%20%D0%B8%D0%B7%2050%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D1%87%D0%B0%D1%81%D1%82%D1%8C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B5%2C%20Claude%20%D1%81%D1%80%D0%B5%D0%B4%D0%B8%20%D0%BD%D0%B8%D1%85%20%D0%BD%D0%B5%D1%82%29.md)
- Переключение провайдеров и аккаунтов без флешки: [CCS (Claude Code Switch)](../ProxyLLM/CCS%20%28Claude%20Code%20Switch%29%20%E2%80%94%20%D0%BF%D0%B5%D1%80%D0%B5%D0%BA%D0%BB%D1%8E%D1%87%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D0%B8%20%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20Claude%20Code.md)
- Офлайн-режим: [Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) · [LM Studio](../Local-LLM/LM%20Studio%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF-GUI%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)
- Откуда взять ключ подешевле: [Бесплатные AI-API](../ProxyLLM/%D0%91%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B5%20AI-API%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D1%81%20free-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BE%D0%BC%20%D0%BA%20LLM%20%28OpenRouter%2C%20Groq%2C%20Cerebras%20%D0%B8%20%D0%B4%D1%80.%29.md)

## 🔗 Ссылки

- Обёртка: [github.com/techjarves/OpenClaude-Portable](https://github.com/techjarves/OpenClaude-Portable) (MIT) · ветка с исправлениями: [dev](https://github.com/techjarves/OpenClaude-Portable/tree/dev)
- Движок: [github.com/Gitlawb/openclaude](https://github.com/Gitlawb/openclaude) · его [LICENSE](https://github.com/Gitlawb/openclaude/blob/main/LICENSE) · npm: [@gitlawb/openclaude](https://www.npmjs.com/package/@gitlawb/openclaude)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/27581)

#AI #Агенты #Безопасность #Портативный_софт #Node-js #Лицензии
