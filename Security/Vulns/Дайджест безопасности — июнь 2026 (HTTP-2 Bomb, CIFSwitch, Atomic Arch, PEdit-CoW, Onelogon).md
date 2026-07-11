---
создал заметку: 2026-07-02T09:30:00
author: WhiteK0T
tags:
  - Дайджест
  - Безопасность
  - CVE
  - supply-chain
  - Linux
  - Windows
Источник:
  - https://t.me/IzHmfluzM81OTAy/602
---

# 🗞️ Дайджест безопасности — июнь 2026

Подборка значимых уязвимостей и инцидентов месяца (по дайджесту [@Mr0x45xploit](https://t.me/IzHmfluzM81OTAy/602)) — **проверено по первичным источникам**, с поправками там, где формулировки поста были неточны. Два пункта уже разобраны отдельными заметками (ссылки внутри), три — раскрыты здесь.

> [!info] Сквозной мотив месяца — «старый код + новый ИИ-аудит»
> **Четыре из пяти** находок — это давно лежавшие баги (17–19 лет) или переосмысление старых, поднятые **автономными ИИ-системами анализа кода** (OpenAI Codex у HTTP/2 Bomb, AI-фреймворк семантических графов у CIFSwitch, тот же тренд у [pedit COW](Linux/CVE/CVE-2026-46331%20%E2%80%94%20pedit%20COW%20%28act_pedit%20tc%20page-cache%20LPE%29.md) и [NGINX Rift](Linux/CVE/CVE-2026-42945%20%E2%80%94%20NGINX%20Rift%20%28ngx_http_rewrite_module%20heap%20overflow%2C%20RCE-DoS%29.md)). Зрелый код массово переаудируется машинами — жди волну N-day.

---

## 1. 💣 HTTP/2 Bomb (CVE-2026-49975) — DoS через исчерпание памяти

**Суть.** Раскрыта 02.06.2026. Не «ещё один флуд», а **связка двух приёмов**: HPACK-«бомба сжатия» + удержание соединения в стиле **Slowloris** (через flow-control window). Атакующий сперва «засевает» таблицу сжатия заголовков **одной большой записью**, затем шлёт тысячи **однобайтовых ссылок** на неё — сервер на каждый запрос разворачивает огромные заголовки в память, а медленное окно держит соединения живыми → память кончается **за секунды**. Найдено с помощью **OpenAI Codex** (сшил несколько известных слабостей HTTP/2 в одну рабочую цепочку).

> [!caution] «Любой сервер ложится за секунды» — усиление радикально разное
> Коэффициент амплификации зависит от реализации HTTP/2, и разброс огромный:
> - **Envoy** — ~**5700:1** (32 ГБ за ~10 секунд),
> - **Apache httpd** — ~**4000:1**,
> - **NGINX** — всего ~**70:1**.
>
> То есть **NGINX на порядки устойчивее** Envoy/Apache. Затронуты дефолтные конфиги NGINX, Apache HTTPD, **IIS**, Envoy, **Cloudflare Pingora**. Фигурирует оценка ~880 000 сайтов «на дефолтном стеке» — это потолок поверхности, а не число реально валящихся одним пакетом.

> [!note] Это **DoS**, не RCE
> Итог атаки — недоступность/перезапуск, не выполнение кода. Митигация: обновить веб-сервер/прокси, ограничить размер и число заголовков HTTP/2, лимиты одновременных потоков и таймауты медленных соединений, WAF/anti-DoS (HAProxy/Imperva/Cloudflare выпустили защиты). На своих системах: `emerge`/`apt`/`pacman` обновление nginx; на **RT-AX56U** актуально, **если** там развёрнут nginx (`opkg upgrade nginx`) — сверься с [NGINX Rift](Linux/CVE/CVE-2026-42945%20%E2%80%94%20NGINX%20Rift%20%28ngx_http_rewrite_module%20heap%20overflow%2C%20RCE-DoS%29.md), где та же логика обновления.

## 2. 🔑 CIFSwitch (CVE-2026-46243) — 19-летний root в CIFS

**Суть.** Локальный LPE в подсистеме **CIFS** ядра Linux, живший **с 2007 года**. Когда CIFS-шара использует **Kerberos**, ядро через keyring запрашивает ключ `cifs.spnego` и вызывает **root-овый хелпер `cifs.upcall`**. Хелпер **доверяет полям, которые считает пришедшими от ядра**, но атакующий их контролирует: подделав их, он форсирует **смену namespace** и запускает **NSS-lookup до сброса привилегий** → подгружается вредоносный **NSS-модуль** → выполнение кода от root. Нашёл инженер **SpaceX Asim Manizada** ИИ-фреймворком семантических графов объектов ядра. Раскрыто 28.05.2026, патчи в репозиториях с 02.06.2026.

> [!warning] «Даёт root на множестве дистрибутивов» — но эксплуатация **не универсальна**
> Само название (CIF-**switch**) намекает: срабатывает не везде. Нужны совпадения:
> - **уязвимая версия ядра** (не любая),
> - практически — **используемый CIFS** (модуль/`mount.cifs`, Kerberos-шара),
> - **локальный** доступ недоверенного пользователя.
>
> На части современных сборок дефолтные **SELinux/AppArmor блокируют** вектор: авторы разбора называют **Ubuntu 26.04, Fedora 40–44, CentOS Stream 10, Rocky/AlmaLinux 10, SLES 16, openSUSE Leap 16**. Это не «одна команда — root везде», а **условный** LPE. Тем не менее — обновляй ядро (`emerge -u sys-kernel/*`, `apt full-upgrade`, `pacman -Syu linux`), а если CIFS не нужен — не автоподгружай модуль. Red Hat: бюллетень **RHSB-2026-005**.

## 3. 📦 Atomic Arch — крупнейший supply-chain в истории AUR

**Суть (кратко).** С 11.06.2026 — захват «осиротевших» пакетов **AUR** через штатное «усыновление»: в `PKGBUILD` подсовывался post-install, тянущий npm-пакет **`atomic-lockfile`** (Rust-инфостилер + попытка **eBPF-персистентности**). Первая волна ~**408** пакетов, за сутки через второй вектор — **1500+**.

> [!tip] Разобрано отдельно — и это прямо про твой план на Arch
> Полный разбор с детектом и очисткой: **[Atomic Arch — supply-chain атака на AUR](Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md)**. Учитывая переход на **Arch** — читай перед первой установкой из AUR: всегда просматривай `PKGBUILD` и `.install`, недоверенные пакеты ставь без слепого `makepkg -si`.

## 4. 🐧 PEdit-CoW (CVE-2026-46331) — LPE через порчу page-cache

**Суть (кратко).** LPE в tc-действии **`act_pedit`**: неполный copy-on-write пишет в **общий page-cache**, портя закэшированный setuid-бинарь **в памяти** (файл на диске чист → AIDE/`rpm -V` молчат). Нужны userns + namespace-local `CAP_NET_ADMIN` + локальный код.

> [!tip] Разобрано отдельно
> Полный разбор (предусловия, детект, митигация, блокировка модуля): **[CVE-2026-46331 — pedit COW](Linux/CVE/CVE-2026-46331%20%E2%80%94%20pedit%20COW%20%28act_pedit%20tc%20page-cache%20LPE%29.md)**. Класс тот же, что [Copy Fail](Linux/CVE/CVE-2026-31431%20%E2%80%94%20Copy%20Fail%20%28algif_aead%20AF_ALG%20LPE%29.md) и [Dirty Frag](Linux/CVE/Dirty%20Frag%20%28CVE-2026-43284%20xfrm-ESP%2C%20CVE-2026-43500%20RxRPC%29.md).

## 5. 🪟 Onelogon — атака на Netlogon / Active Directory

**Суть.** Академическая работа группы **RUB (Ruhr-Universität Bochum), WOOT'26**. Onelogon бьёт по **слабости патча 2020 года против [Zerologon](https://ru.wikipedia.org/wiki/Zerologon)**: если в доменной групповой политике оставлены **аккаунты-исключения** «для легаси, не умеющих Netlogon signing/sealing», такой аккаунт можно **захватить примерно за 30 минут**; если это учётка **контроллера домена** — компрометация всего домена. Код и данные — на GitHub исследователей.

> [!caution] Не путать с CVE-2026-41089 (это **другая** дыра Netlogon)
> В новостях июня рядом идут **две разные** вещи про Netlogon:
> - **Onelogon** — исследовательская атака на **криптопатч Zerologon**, требует **специфической конфигурации** (аккаунты в «уязвимом канале» ради легаси). «Фундаментальная проблема AD» — с оговоркой: это про наследие + послабления, а не «любой DC падает сам».
> - **CVE-2026-41089** — критический **pre-auth RCE (SYSTEM)** на DC через Netlogon RPC, раскрыт в майский Patch Tuesday (12.05.2026), **эксплуатируется в дикой природе** с 29.05.2026. Вот это «0-click на любой непропатченный DC» — **патчить немедленно**.
>
> Пост объединил тему под «Onelogon»; на деле срочность несёт именно **CVE-2026-41089** (майские обновления Microsoft).

## 💻 Применимость к твоим системам

| Пункт | Отношение к системам владельца |
| :--- | :--- |
| **HTTP/2 Bomb** | Актуально, если держишь **nginx/reverse-proxy** (десктоп или **RT-AX56U**). NGINX устойчивее прочих, но обнови и ограничь HTTP/2-лимиты |
| **CIFSwitch** | Актуально на **Linux-десктопах** при использовании **CIFS/Kerberos-шар**; обнови ядро. На **RT-AX56U** ядро вендорское — только прошивка |
| **Atomic Arch** | Прямо про **Arch** (переход в планах) — см. отдельную заметку перед установками из AUR |
| **PEdit-CoW** | Любой mainstream-дистрибутив с непропатченным ядром (Gentoo/Debian/Arch) — обнови ядро |
| **Onelogon / CVE-2026-41089** | **N/A** — это Windows **Active Directory**; у владельца нет доменных контроллеров. Знать для общего кругозора / рабочих сред |

## 🔗 Ссылки

- Источник (дайджест): [@Mr0x45xploit](https://t.me/IzHmfluzM81OTAy/602)
- HTTP/2 Bomb: [The Hacker News](https://thehackernews.com/2026/06/new-http2-bomb-vulnerability-allows.html) · [HAProxy blog](https://www.haproxy.com/blog/haproxy-cve-2026-49975-http2-bomb) · [SOC Prime](https://socprime.com/blog/cve-2026-49975-analysis/)
- CIFSwitch: [Red Hat RHSB-2026-005](https://access.redhat.com/security/vulnerabilities/RHSB-2026-005) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-cifswitch-linux-flaw-gives-root-on-multiple-distributions/) · [SecurityWeek](https://www.securityweek.com/19-year-old-linux-kernel-vulnerability-exposes-systems-to-root-access/)
- Onelogon: [RUB SoftSec (WOOT'26)](https://softsec.rub.de/publications/woot2026-onelogon/) · [rub-softsec/onelogon](https://github.com/rub-softsec/onelogon) · CVE-2026-41089: [SecurityWeek](https://www.securityweek.com/critical-windows-netlogon-vulnerability-in-attackers-crosshairs/)
- Связанные заметки: [Atomic Arch (AUR)](Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md) · [pedit COW](Linux/CVE/CVE-2026-46331%20%E2%80%94%20pedit%20COW%20%28act_pedit%20tc%20page-cache%20LPE%29.md) · [NGINX Rift](Linux/CVE/CVE-2026-42945%20%E2%80%94%20NGINX%20Rift%20%28ngx_http_rewrite_module%20heap%20overflow%2C%20RCE-DoS%29.md)

#Дайджест #Безопасность #CVE #supply-chain #Linux #Windows
