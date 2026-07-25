---
создал заметку: 2026-07-25T20:10:00
author: WhiteK0T
tags:
  - JavaScript
  - NodeJS
  - Runtime
  - Gentoo
  - Portage
  - Backend
  - npm
Источник:
  - https://nodejs.org/
  - https://packages.gentoo.org/packages/net-libs/nodejs
  - https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule
---

# 🟢 Node.js — серверный JavaScript-рантайм (V8, event loop, npm)

**Node.js** — среда исполнения **JavaScript вне браузера**, построенная на движке **V8** (тот же, что в Chrome) и библиотеке **libuv** (асинхронный I/O). Позволяет писать на JS backend, CLI-утилиты, инструменты сборки, десктоп (Electron) и т.д. Ключевая идея — **однопоточный event loop + неблокирующий I/O**: один поток обрабатывает тысячи соединений, не создавая поток на каждого клиента.

> [!info] Коротко о сути
> - **Движок**: V8 (компилирует JS в машинный код, JIT).
> - **I/O**: libuv — event loop + пул потоков для операций, которые нельзя сделать асинхронно на уровне ОС (файлы, DNS, крипта).
> - **Модель**: один основной JS-поток; тяжёлые вычисления его **блокируют** (см. «факты против хайпа»).
> - **Экосистема**: **npm** — крупнейший реестр пакетов в мире (регистрация зависимостей, семвер, `package.json`).

## 🧭 Версии и график релизов (актуально на июль 2026)

| Линия | Статус | Примечание |
| :--- | :--- | :--- |
| **26.x** | Current | вышла в мае 2026; станет LTS в октябре 2026 |
| **24.x** | Active LTS | рекомендуемая для прода **сейчас** |
| **22.x** | Maintenance LTS | только исправления безопасности |
| 20.x и старше | EOL / почти EOL | не использовать для нового |

> [!warning] Смена схемы версионирования с октября 2026
> Node.js **уходит от двух мажоров в год к одному**: с **v27 (октябрь 2026)** будет **один мажор в год (в апреле)**, и **все релизы становятся LTS** — исчезает деление на «нечётные = нестабильные / чётные = LTS». То есть привычное правило «ставь только чётную версию» **скоро перестанет действовать**. Планируя апгрейды на 2026–2027, держи это в голове.

## ⚙️ Архитектура (что важно понимать)

- **Event loop (libuv)** проходит фазы: таймеры → отложенные колбэки → poll (I/O) → check (`setImmediate`) → close. Понимание фаз объясняет порядок `setTimeout` vs `setImmediate` vs `process.nextTick`.
- **Пул потоков libuv** (по умолчанию 4, `UV_THREADPOOL_SIZE`) — для fs, DNS (`getaddrinfo`), `crypto.pbkdf2` и т.п. Не путать с «многопоточным JS»: сам JS — один поток.
- **`worker_threads`** — реальная параллельность для **CPU-bound** задач (отдельные V8-изоляты, обмен через `MessagePort`/`SharedArrayBuffer`).
- **`cluster`** / несколько процессов за реверс-прокси — масштабирование по ядрам (каждый процесс — свой event loop).
- **CommonJS (`require`) vs ESM (`import`)** — сейчас нативно поддержаны оба; `"type": "module"` в `package.json` переключает трактовку `.js`. Смешивание — источник частых ошибок.

## 🧩 Экосистема и инструменты

- **Менеджеры пакетов**: `npm` (штатный), **pnpm** (экономит диск через hardlinks — актуально для владельца), **yarn**. Переключение между ними — через **Corepack** (`corepack enable`), но он **экспериментальный**.
- **`package.json`** — манифест: зависимости, скрипты (`npm run`), поля `type`/`exports`/`engines`. **`package-lock.json`** фиксирует точные версии — коммить его.
- **`npm ci`** (вместо `npm install`) в CI: ставит строго по lock-файлу, воспроизводимо.
- **Встроенные фичи современных Node** (пригодятся вместо зависимостей): нативный **тест-раннер** (`node --test`), режим **`--watch`**, глобальный **`fetch`**, чтение **`.env`** (`--env-file`), **single executable applications** (упаковка в один бинарь), экспериментальная **модель прав** (`--permission`, ограничение доступа к fs/сети/child_process).

## 🐧 Gentoo (основная система) — сборка из исходников

На Gentoo `net-libs/nodejs` **и так собирается из исходников** (компилируется V8 — это долго и прожорливо по RAM/CPU; на слабой машине готовься к длинной сборке, может помочь `ccache`).

> [!info] USE-флаги `net-libs/nodejs` (проверено по packages.gentoo.org)
> | Флаг | По умолч. | Что делает |
> | :--- | :--- | :--- |
> | `npm` | ✅ | ставить менеджер npm вместе с node |
> | `inspector` | ✅ | V8 inspector (отладка через `--inspect`, Chrome DevTools) |
> | `snapshot` | ✅ | снапшот стартового состояния → быстрее запуск |
> | `system-icu` | ✅ | использовать системный `dev-libs/icu`, а не встроенный (меньше сборка, но нужен свежий icu) |
> | `system-ssl` | ✅ | использовать системный OpenSSL вместо встроенного |
> | `corepack` | ➖ | включить экспериментальный Corepack (pnpm/yarn) |
> | `pax-kernel` | ➖ | сборка под PaX-ядро (hardened) |
> | `lto` (global) | ➖ | Link-Time Optimization — дольше сборка, чуть быстрее рантайм |
> | `debug`, `doc`, `test` | ➖ | отладочная сборка / документация / тесты |

```bash
# посмотреть флаги и версии
equery uses net-libs/nodejs        # или: emerge -pv net-libs/nodejs
# зафиксировать флаги (пример: pnpm через corepack, без doc)
echo 'net-libs/nodejs corepack -doc' >> /etc/portage/package.use/nodejs
emerge -av net-libs/nodejs
```

> [!warning] Нет слотов → в Portage только ОДНА версия Node одновременно
> В отличие от `dev-java/openjdk` (слоты), у `net-libs/nodejs` **нет слотирования** и нет `eselect nodejs` — системно живёт **ровно одна** версия. Если под разные проекты нужны разные версии Node — это **не задача Portage**. Держи стабильную **системную** версию из `emerge`, а под конкретные проекты используй **fnm** (быстрый, на Rust) или **nvm**/**volta** в своём `$HOME` — они не трогают систему.

> [!caution] Hardened/PaX: V8 требует W^X-исключений (JIT)
> На **hardened**-профиле собери с USE `pax-kernel` и учти: JIT V8 генерирует исполняемый код в памяти, что конфликтует с MPROTECT. Если node падает на старте под PaX — пометь бинарь: `paxctl-ng -m /usr/bin/node` (снять `MPROTECT`). На обычном (не hardened) ядре это не нужно.

> [!tip] `system-ssl` / `system-icu` — палка о двух концах
> Для source-сборщика это правильно (не тащить дубли библиотек, единый OpenSSL). **Но**: если системный OpenSSL/icu разъедутся по версии с тем, что ждёт данный релиз Node, сборка/рантайм могут ломаться. В редких случаях лечится временным **отключением** флага (взять встроенную библиотеку): `net-libs/nodejs -system-ssl` / `-system-icu`.

> [!danger] Не ставь глобальные npm-пакеты в системный prefix
> `npm i -g` в системный Node пишет в `/usr/...` и **конфликтует с Portage** (Portage не знает об этих файлах). Настрой пользовательский префикс:
> ```bash
> npm config set prefix "$HOME/.npm-global"
> export PATH="$HOME/.npm-global/bin:$PATH"   # в ~/.bashrc / ~/.zshrc
> ```
> И **никогда** `sudo npm -g`. Ещё лучше — версии Node под проекты держать через fnm/nvm, где всё в `$HOME`.

## 🖥️ Установка на других системах владельца

| Система | Как поставить |
| :--- | :--- |
| **Debian / Ubuntu** | в репозитории node **сильно отстаёт**. Для свежего: официальный **NodeSource** (`deb.nodesource.com`, скрипт добавляет apt-репо нужной мажорной линии) **или** `nvm`/`fnm` в `$HOME`. `sudo apt install nodejs npm` — только если версия из репо устраивает |
| **Arch** | `sudo pacman -S nodejs npm` — rolling, версия свежая; для нескольких версий — `nvm`/`fnm` (в т.ч. из AUR). Пакеты `nodejs-lts-*` для LTS-линий |
| **Entware / RT-AX56U (armv7)** | `opkg update && opkg install node node-npm` — **пакет есть**, но версия обычно **заметно отстаёт**, а V8 тяжёл: `256 МБ flash` + `512 МБ RAM` ограничивают. Годится для **лёгких скриптов/утилит**, не для тяжёлых сборок фронтенда. Перед установкой сверься: `opkg list \| grep -i node` и оцени, влезет ли в flash |

> [!tip] Рекомендация под сетап владельца
> На Gentoo — **системный Node из `emerge`** как база + **fnm** для версий под проекты. На роутере — Node только для мелочи. **pnpm** (через `corepack`) экономит место — полезно и на десктопе, и особенно на роутере.

## 🧪 Факты против хайпа

> [!caution] Чему не верить в маркетинге Node
> - **«Многопоточный / быстрый как C»** — нет. JS-код исполняется в **одном** потоке. **CPU-bound** задача (тяжёлый цикл, синхронная крипта, парсинг гигабайтов) **блокирует event loop** и вешает весь сервер. Решение — `worker_threads`, `cluster`, вынос в нативный код или другой сервис.
> - **«Асинхронно = параллельно»** — нет. Асинхронность про **ожидание I/O** без блокировки, а не про параллельные вычисления.
> - **«npm безопасен по умолчанию»** — нет. Реестр открытый → **supply-chain риски**: тайпсквоттинг, вредоносные `postinstall`-скрипты, компрометация популярных пакетов. Защита: коммить lock-файл, `npm ci`, `npm audit`, при подозрении `npm i --ignore-scripts`, инструменты вроде Socket/`npq`. Не тащи зависимость ради трёх строк.
> - **`node_modules` тяжёлый** — классический мем («самый тяжёлый объект во Вселенной»). **pnpm** сильно помогает (общий store + hardlinks).
> - **«Node подходит для всего»** — для **I/O-bound** (API, прокси, real-time) отлично; для **CPU-bound** (тяжёлая математика, ML) — обычно нет, там уместнее другие рантаймы (в т.ч. [Java/JVM](../../Java/Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)).

## 🩺 Диагностика на проде

- **Отладка**: `node --inspect` + Chrome DevTools (нужен USE `inspector`).
- **Профилирование**: `node --prof` → `--prof-process`, флейм-графы (`0x`, `clinic`), `--cpu-prof`/`--heap-prof`.
- **Зависание/100% CPU**: если event loop заблокирован — стек висит в **userspace** (V8), и `strace` покажет **пусто** (см. заметку про strace — это диагноз «копай профайлером», а не syscalls). Смотри `node --prof`, `clinic doctor`, метрики event-loop lag.
- **Утечки памяти**: heap snapshot (`--heap-prof`, DevTools Memory), следи за `process.memoryUsage()`.

## 🔗 Связанные заметки

- Другой серверный рантайм для сравнения (JVM, тоже про CPU-bound и экосистему сборки): [Java — платформа и язык (JVM, JDK, установка на Gentoo)](../../Java/Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)

## 🔗 Ссылки

- Официально: [nodejs.org](https://nodejs.org/) · пакет: [packages.gentoo.org/net-libs/nodejs](https://packages.gentoo.org/packages/net-libs/nodejs)
- Смена графика релизов: [Evolving the Node.js Release Schedule](https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule)
- Менеджеры версий: [fnm](https://github.com/Schniz/fnm) · [nvm](https://github.com/nvm-sh/nvm) · экономный менеджер пакетов [pnpm](https://pnpm.io/)

#JavaScript #NodeJS #Runtime #Gentoo #Portage #Backend #npm
