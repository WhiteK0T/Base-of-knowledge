---
создал заметку: 2026-09-09T17:30:00
author: WhiteK0T
tags:
  - Хостинг
  - PaaS
  - Render
  - Deploy
  - DevOps
Источник:
  - https://t.me/bugnotfeature/27257
  - https://render.com/pricing
  - https://render.com/docs/free
---

# Render — бесплатный хостинг для MVP: что реально бесплатно

**Render** — американский PaaS (platform-as-a-service): подключаешь Git-репозиторий, Render сам собирает и разворачивает приложение, выдаёт HTTPS-домен `*.onrender.com`, TLS и CDN. Аналог Heroku/Railway/Fly.io. Умеет web services, private services, background workers, cron jobs, workflows, статические сайты, Postgres и Key Value (Redis-совместимый).

Пост в «Не баг, а фича» рекламирует бесплатный тариф. Цифры в посте **взяты из реального прайса**, но описывают не то, что кажется: 5 ГБ и 25 сервисов — это лимиты **тарифа воркспейса Hobby**, а бесплатный **компьют** ограничен отдельно и куда жёстче.

---

## Проверка заявлений поста

| Заявление поста | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «БЕСПЛАТНО деплоить сайты, апишки и **целые воркфлоу**» | ⚠️ | Сайты и API — да. **Workflows бесплатного плана не имеют вообще**: каждый запуск задачи тарифицируется |
| «до 5 Гб пропускной способности» | ✅ | Цифра верна. Но это **самый низкий** тариф самого же Render (Pro — 25 ГБ, Scale — 1 ТБ), трафик общий на весь воркспейс, сверх лимита — $0,15/ГБ |
| «богатый бесплатный тариф» | ❌ | Для сравнения: Vercel на бесплатном Hobby даёт **100 ГБ** Fast Data Transfer — в 20 раз больше |
| «до 25 сервисов нахаляву» | ❌ | 25 — лимит на **количество** сервисов в Hobby-воркспейсе. Бесплатного компьюта дают **750 инстанс-часов в месяц на весь воркспейс** ≈ один сервис в режиме 24/7 |
| «Не имеет привязки карты для регистрации» | ✅ | Правда. Но обратная сторона: **без карты Render просто отключает сервисы** при превышении лимитов |
| «Можно подключить ЛЮБОГО агента» | ⚠️ | Официально поддержаны Claude Code, Claude Desktop, Codex (CLI и Desktop), Cursor, OpenCode. Остальные — вручную через URL MCP-сервера |
| «или создать кастомный домен» | ✅ | На free-инстансах домены и управляемый TLS действительно есть. Но Hobby включает **2 домена**, дальше — $0,25/домен/мес |
| «Идеально для прототипов MVP» | ✅ | С этим согласна и документация — но формулировкой пожёстче: *«Do not use them for production applications»* |
| «базовый сервер буквально ни за что» | ⚠️ | Этот «сервер» — **0,1 CPU и 512 МБ RAM**, засыпает после 15 минут тишины и просыпается около минуты |

---

## Что бесплатно, а что нет

Прямая цитата из FAQ прайса:

> With Render's Free compute plans, you can spin up **web services, Render Key Value instances, and Render Postgres databases** at no charge.

И из документации:

> **Other service types don't support Free instances.**

| Тип сервиса | Free-план |
| :--- | :--- |
| Web service | ✅ есть (0,1 CPU / 512 МБ) |
| Static site | ✅ бесплатен всегда, инстанс-часы не ест |
| Render Postgres | ✅ есть (0,1 CPU / 256 МБ, 1 ГБ диска) |
| Render Key Value | ✅ есть |
| **Background worker** | ❌ только платно |
| **Cron job** | ❌ только платно |
| **Private service** | ❌ только платно |
| **Workflows** | ❌ только платно |

Workflows тарифицируются по факту запуска: план `flex` — **$0,20 за CPU-час и $0,05 за ГБ-час**, фиксированные планы — от $0,40/час за 2 CPU / 4 ГБ. Никакого бесплатного порога у них нет, так что «целые воркфлоу бесплатно» из поста — неверно.

---

## Главная арифметика: 750 часов против 25 сервисов

Два независимых лимита, которые пост склеил в один:

1. **Лимит воркспейса Hobby** — *«Hobby workspaces are limited to 25 total services»*. Это про то, сколько сервисов можно **создать**.
2. **Лимит бесплатного компьюта** — *«Render grants 750 Free instance hours to each workspace per calendar month»*. Это про то, сколько они могут **работать**.

В месяце 720–744 часа. Значит **750 часов ≈ ровно один сервис, работающий круглосуточно**. Два всегда-включённых сервиса выберут лимит примерно к середине месяца, и тогда:

> If you consume all of your Free instance hours during a given month, Render **suspends all of your Free web services** until the start of the next month.

Смягчающее обстоятельство: спящий сервис часы не тратит («spun-down services don't consume Free instance hours»). Поэтому 25 демо-сервисов, которые дёргают пару раз в неделю, в 750 часов теоретически влезут — но это сценарий «25 витрин, которые почти всегда спят», а не «25 работающих проектов».

Плюс отдельные потолки: **только один бесплатный Postgres и только один бесплатный Key Value на воркспейс**, и **Hobby-воркспейс — на одного человека** («limited to a single member»), максимум два окружения на проект.

---

## Ограничения бесплатного web service

Список из [документации](https://render.com/docs/free) — то, о чём пост не сказал ни слова:

- **Засыпание.** *«Render spins down a Free web service that goes 15 minutes without receiving any inbound traffic»*, включая WebSocket-сообщения. Пробуждение — *«about one minute»*, всё это время браузеру показывают заглушку Render.
- **Эфемерная ФС.** Любые изменения файлов теряются при редеплое, рестарте и засыпании. Диск (persistent disk) на free подключить нельзя — только SQLite «до первого сна».
- **Нет shell.** Ни SSH, ни консоли в дашборде, ни one-off jobs.
- **Нет масштабирования** больше одного инстанса и нет edge caching.
- **SMTP заблокирован:** *«Free web services can't send outbound network traffic on ports 25, 465, or 587»* — почту слать только через HTTP-API (Resend, SendGrid и т. п.).
- **Порты 18012, 18013, 19099** заняты платформой.
- **Приватная сеть только на выход:** входящий трафик из приватной сети free-сервис не принимает.
- **Отключение за исходящий трафик:** *«Render may suspend a Free web service that initiates an uncommonly high volume of traffic over the public internet»* — то есть парсеры, выгрузки в S3 и активные обращения к внешним API на free-плане ходят по краю.
- **robots.txt = disallow all, пока сервис спит.** Запрос к `/robots.txt` у спящего сервиса получает готовый «запретить всё» и даже не будит инстанс. Для сайта, который надо индексировать, — прямой вред.
- Render может перезапустить бесплатный сервис в любой момент.

## Бесплатные базы: сроки жизни

**Postgres**: фиксированные 1 ГБ, максимум одна база на воркспейс, **истекает через 30 дней после создания**, дальше 14 дней грейс-периода на апгрейд — и удаление вместе с данными. Плюс: *«Free Render Postgres databases don't support any form of backups»* и нет пулинга соединений.

**Key Value**: одна на воркспейс и **только в памяти** — *«whenever an instance restarts, all of its data is lost»*. При апгрейде на платный план данные тоже теряются.

Вывод: бесплатный Render — это песочница на месяц, а не место, где живут данные.

---

## Что на «бесплатном» тарифе всё-таки стоит денег

| Ресурс | Включено в Hobby | Сверх лимита |
| :--- | :--- | :--- |
| Исходящий трафик | 5 ГБ/мес на весь воркспейс | $0,15 за ГБ (публичный интернет) |
| Минуты сборки (build pipeline) | 500 мин/мес | $5 за 1000 минут |
| Кастомные домены | 2 | $0,25 за домен в месяц |
| Инстанс-часы free-компьюта | 750/мес | не докупаются — сервисы гасятся до следующего месяца |

Входящий трафик бесплатен, за трафик от DDoS-атаки Render не выставляет счёт.

## Чем оборачивается «без карты»

Заявление поста верное, но у него есть цена. Из FAQ документации, вопрос *«All of my services run on free instances. Can I still be billed?»*:

> Yes, if you've added a payment method. […] **If you haven't added a payment method and you would incur charges, Render instead disables your services for the duration of the current billing period.**

То есть отсутствие карты — это не «безлимитная халява», а **жёсткий предохранитель**: выбрал 5 ГБ трафика или 500 минут сборки — всё гаснет до начала следующего расчётного периода. Для пет-проекта это скорее плюс (никакого внезапного счёта), для чего-то, что хочется показывать людям, — риск.

---

## Регионы и задержка

Доступные регионы: **Oregon, Ohio, Virginia (США), Frankfurt (Германия), Singapore**. Ничего ближе Франкфурта для пользователей из РФ и СНГ нет — это ~40–60 мс RTT в лучшем случае, плюс до минуты на пробуждение спящего инстанса. Для API прототипа терпимо, для интерактивного фронтенда — заметно.

Юридические документы (`/terms`, `/acceptable-use`) отдаются только JS-рендером, статически текст вытащить не удалось — про ограничения по юрисдикциям здесь ничего не утверждаю, проверять надо глазами в браузере.

---

## «Подключить любого агента» — что это на самом деле

Речь про [MCP-сервер Render](https://render.com/docs/mcp-server) и официальные скиллы/плагины. Документация называет конкретный список: **Claude Code, Claude Desktop, Codex Desktop, Codex CLI, Cursor**, а CLI при установке скиллов детектит ещё и **OpenCode**. Любой другой MCP-клиент подключить можно, но руками, прописав URL сервера — «любого агента из коробки» тут нет.

Сервер открытый: [`render-oss/render-mcp-server`](https://github.com/render-oss/render-mcp-server), Apache-2.0, Go, 165 звёзд, последний релиз v0.3.0 (14.01.2026), коммиты идут (последний — 08.09.2026).

Важное предупреждение из их же документации, которое стоит прочитать до подключения:

> Before proceeding, make sure you're comfortable granting your AI tool access to your Render account. **The MCP server supports potentially destructive operations, including modifying a service's environment variables and triggering deploys.**

То есть агент с этим MCP может выкатить деплой и поменять секреты. Подробнее про сам протокол — [MCP — серверы Model Context Protocol](../../AI/Agents/Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md).

Ссылка «со скиллами отсюда» в посте ведёт на их же прошлый пост про rampstack — разбор этого набора: [rampstack-skills — 103 скилла «вместо команды разработки»](../../AI/Skills/rampstack-skills%20%E2%80%94%20103%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%B0%20%C2%AB%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%C2%BB%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%2014%20163%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B0%20%D0%B2%20%D1%84%D0%BE%D0%BD%D0%B5%2C%20%D0%BD%D0%B5%D0%B9%D1%80%D0%BE-CEO%20%D0%BD%D0%B5%D1%82%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%B8%20%D0%B2%D0%BD%D0%B5%20%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D0%B0%29.md).

---

## Render CLI — установка на своих системах

Сервис облачный, ставить локально нужно только CLI: [`render-oss/cli`](https://github.com/render-oss/cli), **Apache-2.0**, Go, актуальная версия **v2.26.0** (01.09.2026), 114 звёзд, репозиторий живой.

Официальный установщик покрывает только Homebrew, WinGet, `curl | sh` и прямую загрузку архива; для всего остального авторы прямо пишут: *«We recommend building from source only if no other installation method works for your system»*.

### Gentoo (основная)

В Portage пакета нет (`render-cli` в дереве отсутствует; `acct-group/render` и `media-gfx/renderdoc` — не про это). Собираем из исходников, как и всё остальное:

```bash
emerge -av dev-lang/go
git clone https://github.com/render-oss/cli.git
cd cli
go build -o render
sudo install -m0755 render /usr/local/bin/render
```

`go build` тянет зависимости из сети — если в системе включён `FEATURES="network-sandbox"`, собирать надо вне ebuild, вручную, как выше.

### Debian / Ubuntu

В `apt` пакета нет. Либо официальный скрипт:

```bash
curl -fsSL https://raw.githubusercontent.com/render-oss/cli/refs/heads/main/bin/install.sh | sh
```

либо, без выполнения чужого скрипта из интернета, — прямой архив:

```bash
curl -L https://github.com/render-oss/cli/releases/download/v2.26.0/cli_2.26.0_linux_amd64.zip -o render.zip
unzip render.zip && sudo install -m0755 cli_v2.26.0 /usr/local/bin/render
```

### Arch

В официальных репозиториях нет. В AUR есть **`render-cli-bin`**, но на момент проверки он на версии **2.23.0** при актуальной 2.26.0 (три релиза отставания) и всего 1 голос:

```bash
yay -S render-cli-bin     # отстаёт от upstream
```

Надёжнее собрать из исходников тем же `go build`, что и на Gentoo, — Go в Arch ставится как `pacman -S go`.

### Entware (ASUS RT-AX56U, armv7)

В `opkg` пакета нет (поиск по подстроке `render` в репозитории Entware ничего релевантного не даёт). Зато готовая сборка под armv7 у Render есть, и она **статическая**:

```
cli_v2.26.0: ELF 32-bit LSB executable, ARM, EABI5, statically linked, stripped
```

Статическая линковка означает, что зависимость от musl/glibc Entware неважна — бинарь запустится как есть. Два нюанса:

1. **Официальный `install.sh` на роутере не сработает.** В нём захардкожен список архитектур:

   ```sh
   case "${ARCH}" in
     x86_64*) ARCH_NAME=amd64 ;;
     arm64*)  ARCH_NAME=arm64 ;;
     aarch64*) ARCH_NAME=arm64 ;;
     *) error "Unsupported architecture: ${ARCH}" ;;
   esac
   ```

   `armv7l` попадает в `*)` и получает `Unsupported architecture`. Качать архив нужно руками.

2. **Размер.** Распакованный бинарь — **25,1 МБ**. Во внутренние 256 МБ флеша это класть не надо, только на USB-раздел с Entware:

   ```bash
   cd /opt/tmp
   wget https://github.com/render-oss/cli/releases/download/v2.26.0/cli_2.26.0_linux_arm.zip
   unzip cli_2.26.0_linux_arm.zip
   install -m0755 cli_v2.26.0 /opt/bin/render
   render login
   ```

Практический смысл на роутере скромный — разве что дёргать деплой или смотреть логи по SSH с телефона.

### Телеметрия CLI

С версии 2.26.0 включена по умолчанию: *«The Render CLI enables usage telemetry by default in version 2.26.0 and later»*. Собираются имя команды (без аргументов и значений флагов), код возврата, длительность, ОС и случайный UUID установки. Выключается:

```bash
export RENDER_CLI_DISABLE_ANALYTICS=1
# или общепринятый
export DO_NOT_TRACK=1
```

Посмотреть, что именно уходит: `export RENDER_LOG_ANALYTICS=1`.

---

## Когда Render уместен, а когда нет

**Уместен:**

- посмотреть, как выглядит деплой из Git без своей инфраструктуры;
- статический сайт или демо-фронтенд (статика инстанс-часы не тратит вообще);
- API-заглушка для мобильного/фронтового прототипа, которую не жалко подождать минуту при первом запросе;
- временный Postgres на месяц под учебный проект.

**Не уместен:**

- всё, что должно отвечать быстро и всегда — засыпание на 15 минутах не отключается;
- телеграм-боты на вебхуках и любые чувствительные к холодному старту вещи;
- хранилище данных: 30 дней на Postgres, RAM-only Key Value, эфемерная ФС;
- фоновая обработка и расписания — воркеры и cron платные;
- рассылка почты напрямую — SMTP-порты закрыты;
- скрейперы и всё с большим исходящим трафиком — рискуешь и лимитом в 5 ГБ, и правилом про «uncommonly high volume of traffic».

**Альтернатива под контроль:** свой VPS с nginx — тогда нет ни засыпания, ни лимита трафика, ни срока жизни базы. См. [nginx — веб-сервер и reverse-proxy](nginx/nginx%20%E2%80%94%20%D0%B2%D0%B5%D0%B1-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B8%20reverse-proxy%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%2C%20server-location%2C%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%2C%20%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20TLS%2C%20%D0%BA%D1%8D%D1%88%20%28%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%29.md) и [Let's Encrypt — выпуск TLS-сертификата](Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md).

---

## Итог

Render — нормальный PaaS с честно описанным бесплатным тарифом; вся неточность на стороне поста, а не сервиса. Документация Render сама всё перечисляет и сама же пишет: *«Do not use them for production applications»*.

Из шести «фишек» поста две сформулированы неверно (воркфлоу бесплатными не бывают; 25 сервисов ≠ 25 работающих сервисов), одна перевёрнута (5 ГБ — это мало, а не «богато»), одна подана как чистый плюс без обратной стороны (нет карты — значит, гасят при перерасходе), и ни разу не упомянуты засыпание на 15 минутах, минута холодного старта, 0,1 CPU / 512 МБ и 30-дневный срок жизни бесплатного Postgres.

Как песочница на выходные — годится. Как «бесплатный сервер для MVP», который можно показывать людям, — нет.

---

## Источники

- Пост-первоисточник: <https://t.me/bugnotfeature/27257>
- Render — Deploy for Free: <https://render.com/docs/free>
- Render — прайс и тарифы воркспейсов: <https://render.com/pricing>
- Render — Platform Features by Plan: <https://render.com/docs/platform-features-by-plan>
- Render — Compute plans: <https://render.com/docs/compute-plans>
- Render — Outbound bandwidth: <https://render.com/docs/outbound-bandwidth>
- Render — Workflows, Limits & Pricing: <https://render.com/docs/workflows-limits>
- Render — Regions: <https://render.com/docs/regions>
- Render — CLI: <https://render.com/docs/cli>
- Render — MCP Server: <https://render.com/docs/mcp-server>
- Render — Using Render with Coding Agents: <https://render.com/docs/llm-support>
- Исходники CLI: <https://github.com/render-oss/cli>
- Исходники MCP-сервера: <https://github.com/render-oss/render-mcp-server>
- Vercel — лимиты тарифов (для сравнения трафика): <https://vercel.com/docs/limits>

#Хостинг #PaaS #Render #Deploy #DevOps
