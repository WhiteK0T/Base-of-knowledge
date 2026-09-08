---
создал заметку: 2026-09-09T10:30:00
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
  - https://github.com/cordiverse/cordis
---

# 🔌 DeepSeek Harness (dsh) — агентская среда «всё есть плагин»

Разбор [поста «Не баг, а фича» от 17.08.2026](https://t.me/bugnotfeature/27114). Проект настоящий, официальный и действительно бьёт рекорды роста — цифры поста подтвердились. Но пост умалчивает о двух вещах, и именно они важнее всего: **это developer preview с прямым предупреждением о риске**, а «6000 готовых скиллов» — не то, чем кажется.

Проверено 09.09.2026 по репозиторию, npm, GitHub Search API и документации проекта.

> [!info] Факты
> | | |
> | :--- | :--- |
> | Репозиторий | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness), создан **13.08.2026** |
> | Звёзд / форков | **216 175** · 25 523 |
> | Лицензия / язык | **MIT** · TypeScript |
> | Версия в npm | `@deepseek-ai/dsh` — **0.1.2-rc.1** (03.09.2026), 17 версий с 10.08.2026 |
> | Ядро | [Cordis](https://github.com/cordiverse/cordis) — 8 234★, за ним статья [arXiv 2608.25512](https://arxiv.org/abs/2608.25512) |
> | Issues | **отключены**, обратная связь только через Discussions |
> | Автор | DeepSeek AI, организация `deepseek-ai` (104 тыс. подписчиков) |

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «Самый быстрорастущий репозиторий» | ✅ Похоже на правду | **8 314 звёзд в день** в среднем. Для сравнения: Spec Kit — 351, Ollama — 154 |
| «За трое суток больше 130 000 звёзд» | ✅ Правдоподобно | Репозиторий создан 13.08, пост от 17.08. Сейчас 216 175 |
| «Плагином может быть всё: модели, сессии, скиллы, песочницы, интерфейс» | ✅ Верно | Заявленная архитектура — `everything-is-a-plugin` |
| «Своя архитектура на **Cordis**» | ⚠️ Cordis чужой | Это отдельный проект `cordiverse/cordis`, не разработка DeepSeek. Своё у Harness — то, что построено поверх |
| «Сообщество сделало **6000 готовых скиллов**» | ❌ **Считается не то** | Это счётчик репозиториев с топиком `dsh-plugin`. Топик **самоприсваиваемый**, и в нём полно постороннего — разбор ниже |
| «Нейронка запустила среду» | ⚠️ Формулировка | Harness сделала компания DeepSeek, а не модель сама по себе |
| Установка пятью командами через `pnpm` | ⚠️ Путь для разработчика | Есть способ проще: `npx @deepseek-ai/dsh web` — одна команда |
| **Ничего про статус и риски** | ❌ **Умолчание** | Developer preview + отдельный документ SAFETY.md, см. ниже |

## 🔴 Главное умолчание: это developer preview, и авторы честно предупреждают

README начинается с предупреждения капсом, а рядом лежит отдельный `SAFETY.md`. Оттуда, дословно:

> *«DeepSeek Harness is experimental developer-preview software. It has not undergone a security audit and must not be treated as secure or production-ready.»*
>
> *«The project can execute model-generated code and commands, load third-party plugins, and access the network, processes, credentials, and files made available to it. Incorrect model output, defects, misconfiguration, malicious input, or untrusted plugins may damage the host computer, modify or delete files, disclose data or credentials…»*
>
> *«Sandboxing, approval prompts, and permission controls can reduce risk, but they do not guarantee isolation or prevent damage.»*

Рекомендации самих авторов: запускать с минимальными правами, **предпочитать одноразовую виртуалку или контейнер**, держать бэкапы, проверять плагины и предлагаемые команды до запуска.

В README отдельно: **«THERE WILL BE COMPATIBILITY-BREAKING CHANGES»**. Версия в npm — `0.1.2-rc.1`, то есть даже не 0.1.2.

> [!danger] Почему это в связке с постом опаснее, чем по отдельности
> Пост зовёт «скачать 6000 готовых скиллов» по ссылке на топик и утверждает, что «сработает вообще с ЛЮБЫМИ компонентами». А документация проекта прямо говорит, что **непроверенные сторонние плагины могут повредить машину, удалить файлы и слить учётные данные**, и что песочница этого не гарантирует.
>
> Ставить это стоит в контейнере или отдельной виртуалке, а не в рабочее окружение с ключами и доступом к репозиториям.

## 🔢 Про «6000 скиллов»: топик самоприсваиваемый

Ссылка из поста ведёт на [github.com/topics/dsh-plugin](https://github.com/topics/dsh-plugin). Сейчас там **14 024** репозитория — цифра выросла, но считает она не скиллы, а «сколько репозиториев поставили себе этот тег».

А тег ставится вручную кем угодно. README проекта сам это предлагает:

> *«Add the `dsh-plugin` topic to your plugin repository for discoverability.»*

Отсортировал топик по звёздам и посмотрел, что там на самом деле:

| Звёзд | Репозиторий | Что это на самом деле |
| ---: | :--- | :--- |
| 216 176 | `deepseek-ai/deepseek-harness` | сам Harness — не плагин |
| 94 913 | `nexu-io/open-design` | [Open Design](../Open%20Design%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%B0%20Claude%20Design%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%2B%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%29.md) — самостоятельный проект |
| 71 654 | `ruvnet/ruflo` | «the original agent meta-harness» — **конкурент**, не плагин |
| 42 342 | `amruthpillai/reactive-resume` | **конструктор резюме** |
| 29 243 | `freestylefly/awesome-gpt-image-2` | библиотека промптов для GPT-Image |
| 27 157 | `Molunerfinn/PicGo` | **загрузчик картинок** |

Конструктор резюме и загрузчик картинок — давние популярные проекты, к DeepSeek Harness отношения не имеющие. Они просто повесили модный тег ради видимости в трендах.

> [!caution] Знакомый шаблон
> Ровно то же самое разбиралось в заметке про [Skills Hub](../Skills/Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md), где «90 700 скиллов» оказались на 98 % чужими записями. Большое число в каталоге почти никогда не означает большое число пригодных вещей — считать надо не строки, а то, что за ними стоит.

Есть и более узкие теги: `dsh-skill` — **162** репозитория, `deepseek-harness` — 10 316. Первый ближе к тому, что пост называет «скиллами».

## 📈 Рост: цифры действительно рекордные

Проверил среднюю скорость набора звёзд за всё время жизни репозиториев:

| Репозиторий | Звёзд | Возраст | Звёзд в день |
| :--- | ---: | ---: | ---: |
| **deepseek-ai/deepseek-harness** | 216 175 | 26 дней | **8 314** |
| github/spec-kit | 134 160 | 382 дня | 351 |
| ollama/ollama | 180 475 | 1 170 дней | 154 |

Это в 24 раза быстрее Spec Kit и в 54 раза быстрее Ollama. Здесь пост не преувеличивает.

Оговорка: звёзды измеряют внимание, а не пригодность. При отключённых issues и версии `0.1.2-rc.1` судить о качестве по этой цифре нельзя.

## 🧩 Что такое Cordis

Пост называет Cordis «своей архитектурой» Harness. На деле это **отдельный проект** — [`cordiverse/cordis`](https://github.com/cordiverse/cordis), 8 234★, «Meta-Framework of Spatiotemporal Composability», с научной статьёй в основе ([arXiv 2608.25512](https://arxiv.org/abs/2608.25512)). Harness построен **поверх** него.

Косвенное подтверждение зрелости идеи: уже появился Rust-порт `dshbox/cordis-rs`, описывающий Cordis как «the plugin framework at the core of DeepSeek Harness».

## 💻 Установка

> [!tip] Простой путь, который пост не привёл
> ```sh
> npx @deepseek-ai/dsh web
> ```
> Одна команда, нужен только Node.js. Поднимает веб-интерфейс на `http://127.0.0.1:3080` и открывает браузер. Флаг `--no-open` — не открывать.

Путь из поста — это сборка из исходников, для разработчиков плагинов:

```sh
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

Внимание: в самом посте этот блок свёрстан с переносами так, что `git clone` и адрес, а также `cd` и имя каталога оказались на разных строках. Скопировав как есть, получишь ошибку — команды нужно склеить.

| Система | Что нужно |
| :--- | :--- |
| **Gentoo** (основная) | `emerge net-libs/nodejs`; для сборки из исходников ещё `pnpm` (`npm i -g pnpm` или `emerge sys-apps/corepack`). Запускать **в контейнере**, см. предупреждение выше |
| **Debian / Ubuntu** | Node.js из NodeSource или `nvm`, дальше `npx`. Для изоляции — `podman`/`docker` либо отдельная ВМ |
| **Arch** | `pacman -S nodejs npm pnpm` |
| **Entware / RT-AX56U** | ❌ Неприменимо: TypeScript-среда с Node.js и локальным веб-интерфейсом на 512 МБ ОЗУ и 256 МБ флеша не поднимется |

## 💡 Итог

- Проект **настоящий и официальный**, MIT, от DeepSeek. Рекорд роста подтверждается: 8 314 звёзд в день.
- Архитектура «всё есть плагин» на базе Cordis — идея интересная, за ней стоит научная работа. Но **Cordis не разработка DeepSeek**.
- Главное, чего нет в посте: **developer preview без аудита безопасности**, прямое предупреждение о выполнении сгенерированного кода и о том, что песочница ничего не гарантирует, и совет авторов запускать в одноразовой виртуалке.
- «6000 скиллов» — это счётчик самоприсваиваемого топика, где среди верхних позиций конструктор резюме, загрузчик картинок и прямой конкурент. Более осмысленный тег `dsh-skill` даёт **162** репозитория.
- Пробовать стоит, но **в контейнере и без доступа к ключам**. Ставить сторонние плагины из топика без чтения кода — прямо против рекомендаций авторов.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/27114](https://t.me/bugnotfeature/27114) (17.08.2026)
- Проект: [GitHub](https://github.com/deepseek-ai/deepseek-harness) · [документация](https://deepseek-harness.github.io/deepseek-harness/) · [SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md) · [npm `@deepseek-ai/dsh`](https://www.npmjs.com/package/@deepseek-ai/dsh)
- Ядро: [cordiverse/cordis](https://github.com/cordiverse/cordis) · [статья arXiv](https://arxiv.org/abs/2608.25512)
- Экосистема: [топик `dsh-plugin`](https://github.com/topics/dsh-plugin) (14 024) · [топик `dsh-skill`](https://github.com/topics/dsh-skill) (162)
- Связанные: [Сводная таблица AI-агентов](%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md) · [Kimi Code CLI](Kimi%20Code%20CLI%20%28MoonshotAI%29%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE-%D0%B2%D0%B2%D0%BE%D0%B4%2C%20%D1%81%D1%83%D0%B1%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20ACP%2C%20MCP%29%2C%20%D1%84%D0%B0%D0%BA%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D1%85%D0%B0%D0%B9%D0%BF%D0%B0%20%C2%AB%D0%BF%D0%BE%D1%85%D0%BE%D1%80%D0%BE%D0%BD%D0%B8%D0%BB%D0%B8%20Claude%20Code%C2%BB.md) · [Skills Hub — как считают каталоги](../Skills/Skills%20Hub%20%28Hermes%20Agent%2C%20Nous%20Research%29%20%E2%80%94%2090%20700%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%BC%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%B5%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2098%25%20%D1%87%D1%83%D0%B6%D0%B8%D0%B5%2C%2090%25%20%D0%B2%20%C2%AB%D0%BF%D1%80%D0%BE%D1%87%D0%B5%D0%B5%C2%BB%2C%2076%25%20%D0%B1%D0%B5%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%B0%29.md) · [Open Design](../Open%20Design%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%B0%20Claude%20Design%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%2B%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%29.md) · [MCP — серверы Model Context Protocol](Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md)

#AI #Агенты #DeepSeek #Плагины #Безопасность #TypeScript
