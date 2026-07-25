---
создал заметку: 2026-07-25T15:40:00
author: WhiteK0T
tags:
  - OSINT
  - Recon
  - Подборка
  - ThreatIntel
  - Приватность
  - OpenSource
  - Безопасность
Источник:
  - https://github.com/frangelbarrera/OSINT-BIBLE
---

# 🕵️ OSINT Bible 2026 — гид-каталог по OSINT (не просто список инструментов)

**OSINT Bible 2026** ([github.com/frangelbarrera/OSINT-BIBLE](https://github.com/frangelbarrera/OSINT-BIBLE)) — большой курируемый **гид по OSINT**: заявлено **450+ инструментов**, но по факту это **не только список ссылок**, а целая методичка на **47 разделов** — с процедурами, этикой, юридическими аспектами, OPSEC и шаблонами отчётов. GPL-3.0, ~**634★**, создан в декабре 2025, активно обновляется (последний пуш — июль 2026).

> [!tip] Правка к посту: это БОЛЬШЕ, чем «450+ инструментов в одном репо»
> Пост подаёт его как агрегатор ссылок — на деле репозиторий **шире и полезнее**, чем реклама:
> - **47 разделов** (в описании GitHub — «35», но каталог дорос до 47 + приложения): помимо инструментов есть **Fundamentals**, **4-Step Methodology**, **Legal Considerations**, **Professional Methodologies**, **Investigator OPSEC & Sock Puppets**, **Report Templates / Deliverables**, **AI Agent Skills & MCP**, детект дипфейков (**C2PA + SynthID**), **Counter-OSINT Self-Audit** (как проверить свой цифровой след).
> - То есть это **справочник + методология + этика**, который читают, а не только «пачка ссылок для установки». Это его главный плюс перед обычными awesome-list.

> [!info] Что внутри (по разделам README)
> Разделы поста присутствуют и подтверждены: **Internet Search** (поисковики + Google Dorks), **Social Networks** (FB/Twitter/Instagram/TikTok), **GEOINT & Images** (геолокация, поиск по фото), **Domain/IP/DNS** (Whois, поддомены, **Shodan**, **Censys**), **Email/Phone Investigation**, **Blockchain/Crypto**, **Data Breaches**, **Username Enumeration** (**Sherlock**, **Maigret** — «500+ платформ»). Плюс то, чего в посте нет: Deep/Dark Web, Metadata, Network Scanning, All-in-One фреймворки (**Maltego**, **SpiderFoot**), Threat Intelligence Feeds, ICS/OT OSINT, Financial/Cloud/Mobile/Decentralized-Social OSINT, Satellite OSINT, Regional OSINT.

## ⚠️ Факты против хайпа

> [!caution] Это КАТАЛОГ — сам ничего не «пробивает», и часть инструментов платные/спорные
> - Репозиторий — **навигатор по ссылкам** (awesome-list с описаниями), а не рабочий инструмент: он **ничего не сканирует**, ты идёшь на сторонние сервисы/ставишь CLI сам.
> - Часть перечисленного — **платные и этически спорные** сервисы распознавания лиц (**PimEyes**, Lenso.ai): поиск живых людей по фото — зона приватности/закона, не «безобидный тулкит».
> - Ссылки **со временем протухают**, «450+» — по заявлению самого репо; качество пунктов разное. Проверяй каждый инструмент отдельно.

> [!danger] Юридическая рамка (РФ) — это важно именно для OSINT
> OSINT легален как **сбор из открытых источников**, но конкретные разделы этого гида — про **чужие персональные данные**, и тут легко выйти за рамки:
> - **Data Breaches / «поиск по слитым базам»** и **Email/Phone Investigation**: работа со слитыми персональными данными в РФ регулируется **152-ФЗ**; распространение/использование может нарушать закон, а доступ к чужим системам — **ст. 272/273 УК РФ**.
> - **Слежка за конкретным человеком** (face search, соцсети, деанон) без законного основания — риск по **ст. 137 УК РФ** (неприкосновенность частной жизни).
> - Легально — **свой** цифровой след (Counter-OSINT self-audit), обучение, threat intel по инфраструктуре, расследования **по договору/с разрешения**. Сам репозиторий несёт сильный **ethical disclaimer** и разделы Legal/GDPR (это плюс) — читай их, а не только список тулов.

## 🧩 Как это соотносится с тем, что уже в базе

У тебя уже есть несколько OSINT-каталогов — OSINT Bible **не дубль**, а другой жанр:

| Заметка | Жанр | Отличие |
| :--- | :--- | :--- |
| **OSINT Bible** (эта) | **Гид + методология + этика** | читаешь как справочник; сильные разделы про право, OPSEC, отчёты, AI/MCP |
| [awesome-osint-arsenal](awesome-osint-arsenal%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20750%2B%20OSINT-recon-DFIR-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B5%D1%80%D0%B5%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%29.md) | **Инсталлятор** 750+ инструментов | скрипт ставит тулзы пачкой (и в этом же риск) |
| [OSINT-Terminal](OSINT-Terminal%20%E2%80%94%20self-hosted%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%20%D0%B8%D0%B7%20438%20OSINT-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%B1%D0%B5%D0%B7%20API-%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B9%2C%203D-%D0%B3%D0%BB%D0%BE%D0%B1%D1%83%D1%81%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md) | **Дашборд** 438 инструментов | веб-панель без API-ключей, 3D-глобус |
| [awesome-osint-chrome-extensions](awesome-osint-chrome-extensions%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D1%8B%D1%85%20%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B4%D0%BB%D1%8F%20OSINT%20%28Chrome-Brave%29.md) | **Браузерные расширения** | OSINT прямо во вкладке |

Вывод: **Bible — за методом, право и структуру**; arsenal/Terminal — когда нужен готовый набор/панель.

## 🖥️ Применимость на системах владельца

Сам каталог **ОС-независим** (читается в браузере/на GitHub). Но многие перечисленные **CLI-инструменты** (Sherlock, Maigret, theHarvester, SpiderFoot…) ставятся у тебя:

| Система | Как ставить инструменты из гида |
| :--- | :--- |
| **Gentoo (основная) / Debian-Ubuntu / Arch** | Python-CLI — через **pipx**/`pip --user` или из git; часть есть в репозиториях (`emerge`/`apt`/`pacman`/AUR). Проверяй каждый отдельно |
| **Entware / RT-AX56U** | Python на роутере есть, но тяжёлые тулзы/зависимости часто **не влезут/бессмысленны** — не основной кейс |

## 🔗 Связанные заметки

- Инсталлятор 750+ OSINT-инструментов (и предостережения): [awesome-osint-arsenal](awesome-osint-arsenal%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20750%2B%20OSINT-recon-DFIR-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B5%D1%80%D0%B5%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%29.md)
- Дашборд из 438 инструментов без API-ключей: [OSINT-Terminal](OSINT-Terminal%20%E2%80%94%20self-hosted%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%20%D0%B8%D0%B7%20438%20OSINT-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%B1%D0%B5%D0%B7%20API-%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B9%2C%203D-%D0%B3%D0%BB%D0%BE%D0%B1%D1%83%D1%81%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md)
- Браузерные расширения для OSINT: [awesome-osint-chrome-extensions](awesome-osint-chrome-extensions%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D1%8B%D1%85%20%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B4%D0%BB%D1%8F%20OSINT%20%28Chrome-Brave%29.md)
- Разбор поста-подборки с акцентом на законность: [OSINT-подборка из поста (5 ресурсов)](OSINT-%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%D0%B7%20%D0%BF%D0%BE%D1%81%D1%82%D0%B0%20%285%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D0%B2%29%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D1%80%D0%B0%D0%BD%D0%BE%20%D0%B8%20%D0%BE%20%D0%B7%D0%B0%D0%BA%D0%BE%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8.md)

## 🔗 Ссылки

- Репозиторий: [github.com/frangelbarrera/OSINT-BIBLE](https://github.com/frangelbarrera/OSINT-BIBLE) (GPL-3.0)

#OSINT #Recon #Подборка #ThreatIntel #Приватность #OpenSource #Безопасность
