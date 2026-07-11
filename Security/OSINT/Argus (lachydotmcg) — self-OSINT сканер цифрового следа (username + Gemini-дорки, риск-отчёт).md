---
создал заметку: 2026-07-11T05:40:00
author: WhiteK0T
tags:
  - OSINT
  - Security
  - Privacy
  - Self-OSINT
  - Python
  - Gemini
Источник:
  - https://github.com/lachydotmcg/argus
  - https://t.me/+3X56uL4A-UM3Njgy
---

# 🛡️ Argus (lachydotmcg) — self-OSINT сканер твоего цифрового следа

[**Argus**](https://github.com/lachydotmcg/argus) (автор **lachydotmcg**, **Python**, лицензия **MIT**) — **self-OSINT**-инструмент: «посмотри на себя глазами интернета». Проверяет ник по **30+ платформам** и через **Google Gemini** ищет «живые» упоминания (утечки, брокеры данных, документы, форумы), затем **ИИ оценивает** каждую находку и выдаёт **итоговый риск-отчёт**. Идея — не «пробить кого-то», а **найти и подчистить свой** цифровой след.

> [!caution] Важно про зрелость: проект крошечный и «сырой по доверию»
> На момент заметки это **почти неизвестный репозиторий (~1★, июнь 2026, один автор)**, без аудита и большого сообщества. Функционально выглядит рабочим, но по **доверию** это другой класс, чем Sherlock/Maigret. Учитывая, что тул **отправляет твои идентификаторы в Google Gemini** (см. ниже), к «privacy-инструменту от неизвестного автора» подходи с прохладной головой: читай код, гоняй в изоляции.

## ✨ Что умеет

- **Username enumeration** — быстрая проверка ника на **30+ платформах** **локально, без API-ключей** («как Sherlock, но curated»).
- **Live web intelligence (через Gemini)** — целевые **Google-dork**-запросы прогоняются через **Gemini API с Search-grounding**: «реальные, свежие, с цитатами» результаты — брокеры данных, breach-листинги, засвеченные документы, упоминания на форумах.
- **Intelligent profile matching** — ИИ ранжирует каждый найденный профиль: **HIGH / MEDIUM / LOW / UNLIKELY** (отсев ложных срабатываний).
- **Риск-отчёт** — финальный вердикт: **LOW / MODERATE / HIGH / SEVERE**.
- **Вывод:** интерактив в терминале + **HTML-отчёт** (`reports/argus_*.html`) + **JSON**.
- **Monitor-режим** (`python main.py --monitor`) — хранит состояние локально, алертит **только на новое/изменённое**; уведомления в **Discord** или по **SMTP**.
- **Опционально:** **Have I Been Pwned** (мониторинг утечек), **Google Custom Search API** (точные дорки).

## ⚠️ Что важно понимать (факты против хайпа)

> [!warning] Privacy-парадокс: «всё локально» — только наполовину
> README честно пишет «everything runs locally, no telemetry, no accounts» — но **вся соль (web intelligence) уходит наружу**: твои ники и поисковые запросы отправляются в **Google Gemini**, а опционально — в **HIBP** и на **Discord/SMTP**. То есть локально крутится только username-проверка; «умная» часть — это **запросы о тебе к LLM Google**. Для кого-то это приемлемо (данные и так «в интернете»), но называть это чисто локальной приватностью нельзя.

> [!note] «Живые Google Dork-запросы» — с оговоркой
> Точное выполнение дорков-операторов через Gemini — **best-effort** (модель «понимает» запрос через grounding, но не гарантирует буквальное исполнение). **Гарантированные** дорки — только если подключить **Google Custom Search API** (100 бесплатных запросов/сутки). Без CSE это скорее «умный поиск по смыслу», чем строгий dork.

> [!info] Gemini API — бесплатный тариф, но ключ нужен
> Для web-intelligence нужен ключ **Google AI Studio** (`aistudio.google.com`) — бесплатный тариф есть. Username-часть работает и **без** него. Версия модели Gemini в доке не зафиксирована — учитывай, что бесплатные лимиты/модели у Google меняются.

## ⚖️ Использование по закону (self-OSINT vs чужой профиль)

> [!caution] На себе — да; на других — только с разрешения
> Инструмент **спроектирован под self-OSINT** (сканируй **себя**). Пробивать **чужой** ник/профиль без согласия — это уже сбор персональных данных о человеке:
> - **РФ:** нарушение неприкосновенности частной жизни — **ст. 137 УК РФ**; незаконная обработка ПДн — **152-ФЗ** (и **ст. 13.11 КоАП**); при доступе к закрытому — **ст. 272 УК РФ**.
> - Легально: **свой** след, либо цель, на которую есть **явное письменное разрешение** (например, в рамках пентеста/расследования по договору).
>
> Полезный follow-up: нашёл лишнее — **убери** (см. [privacy-settings — настройки приватности сервисов](../privacy-settings%20%28StellarSand%29%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4%20%D0%BF%D0%BE%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%D0%BC%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B0%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B4%D0%BB%D1%8F%2060%2B%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9%2C%20%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%9E%D0%A1.md)).

## 🖥️ По системам

Чистый Python-CLI + venv.

```bash
git clone https://github.com/lachydotmcg/argus && cd argus
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py            # интерактив; --monitor для режима слежения
```

| Система | Применимость |
| :--- | :--- |
| **Gentoo** (основная) | ✅ Python + venv из Portage; интернет для Gemini/CSE. Держи ключи в env, не в репо |
| **Debian / Ubuntu** | ✅ `python3-venv` + pip |
| **Arch** (план с июня 2026) | ✅ Python из репо; venv |
| **Entware / RT-AX56U** | ⚠️ Технически Python на роутере есть, но смысла мало: тул интерактивный, генерит HTML-отчёты и ходит в Gemini — удобнее с десктопа. На armv7/512 МБ — не целевая среда |

## 🔗 Ссылки

- Репозиторий: [github.com/lachydotmcg/argus](https://github.com/lachydotmcg/argus) (MIT)
- Источник новости: канал **CodeGuard: PySec Edition** (в посте прямой ссылки на репо не было — плейсхолдер `<your-repo-url>`; репозиторий найден по описанию)
- Связанные: [OpenSERP — self-hosted SERP для OSINT/LLM](OpenSERP%20%E2%80%94%20self-hosted%20SERP-API%20%D0%B8%20CLI%20%28Google-Yandex-Baidu%20%D0%B8%20%D0%B4%D1%80.%29%20%D0%B4%D0%BB%D1%8F%20OSINT%2C%20LLM%20%D0%B8%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md) · [awesome-osint-arsenal (Sherlock/Maigret и др.)](awesome-osint-arsenal%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20750%2B%20OSINT-recon-DFIR-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B5%D1%80%D0%B5%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%29.md) · [OSINT-Terminal — дашборд OSINT-инструментов](OSINT-Terminal%20%E2%80%94%20self-hosted%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%20%D0%B8%D0%B7%20438%20OSINT-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%B1%D0%B5%D0%B7%20API-%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B9%2C%203D-%D0%B3%D0%BB%D0%BE%D0%B1%D1%83%D1%81%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md) · [Web Check — OSINT-досье на сайт](Web%20Check%20%E2%80%94%20OSINT-%D0%B4%D0%BE%D1%81%D1%8C%D0%B5%20%D0%BD%D0%B0%20%D1%81%D0%B0%D0%B9%D1%82%20%28DNS-SSL-%D0%B7%D0%B0%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BA%D0%B8-%D1%81%D1%82%D0%B5%D0%BA-%D0%BF%D0%BE%D1%80%D1%82%D1%8B%29.md)

#OSINT #Security #Privacy #Self-OSINT #Python #Gemini
