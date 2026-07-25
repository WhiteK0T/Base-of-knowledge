---
создал заметку: 2026-07-25T08:10:00
author: WhiteK0T
tags:
  - Сеть
  - Почта
  - SelfHosted
  - TempMail
  - CatchAll
  - Python
  - Инструменты
Источник:
  - https://t.me/open_source_friend/5807
  - https://github.com/haileyydev/maildrop
---

# ✉️ maildrop — простой самохостируемый catch-all почтовый ящик (Python)

**maildrop** ([github.com/haileyydev/maildrop](https://github.com/haileyydev/maildrop)) — лёгкий self-hosted почтовый сервис на **Python (Flask + свой SMTP)**: принимает письма на **любой адрес твоего домена** (catch-all), показывает их в чистом веб-UI, умеет генерить случайные адреса и защищать отдельные ящики паролем. Отправка — **опциональная** второстепенная фича. GPL-3.0, ~664★. По сути — это **самохостируемый одноразовый/расходный мейл** (тема репо так и помечена: `disposable-email`), близкий родственник [opentrashmail](opentrashmail%20%28HaschekSolutions%29%20%E2%80%94%20%D1%81%D0%B0%D0%BC%D0%BE%D1%85%D0%BE%D1%81%D1%82%D0%B8%D1%80%D1%83%D0%B5%D0%BC%D1%8B%D0%B9%20catch-all%20trashmail%20%D1%81%D0%BE%20%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%20%D0%BC%D0%B5%D0%B9%D0%BB-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%BC%20%28Web-JSON%20API-RSS-%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B8%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B.md).

> [!warning] Правка к посту: это НЕ полноценный почтовый аккаунт
> Пост описывает «почтовый ящик… отправку и получение сообщений» — звучит как обычная почта. На деле maildrop — **catch-all inbox для приёма** (расходные/одноразовые адреса), а не полноценный мейл-аккаунт:
> - **Основное — приём**: ловит письма на *любой* адрес на твоём домене (`что_угодно@твойдомен`). Удобно плодить адреса под регистрации.
> - **Отправка есть, но опциональна** и вторична (отдельный [Sending Guide](https://github.com/haileyydev/maildrop/blob/main/docs/SENDING.md)) — это не замена Gmail/своему полному серверу.
> - Хранилище — **плоский файл** (`INBOX_FILE_NAME`, лимит `MAX_INBOX_SIZE`, **автоочистка** ящиков). То есть письма эфемерны by design, это не архивный мейл-стор. Для «настоящего» сервера с IMAP/папками — это [docker-mailserver](docker-mailserver%20%E2%80%94%20production-ready%20%D0%BF%D0%BE%D1%87%D1%82%D0%BE%D0%B2%D1%8B%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B2%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%B5%20%28Postfix-Dovecot-Rspamd-ClamAV%29%2C%20%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%B0%D0%BC%D0%BD%D0%B8%20self-hosting.md).

> [!caution] Подводные камни self-hosting (те же, что у любого приёма почты)
> - **Порт 25 наружу**: SMTP слушает 25-й порт, а его **массово блокируют домашние провайдеры** (входящий/исходящий). README прямо предупреждает: возможно, понадобится **VPS/облако или туннель**. На домашнем канале + RT-AX56U — скорее всего не заведётся напрямую.
> - **Нужен домен + DNS**: `A`-запись на IP сервера и **`MX`** на домен приёма. Без своего домена смысла нет.
> - **Запуск от root**: чтобы SMTP слушал порт 25, «`sudo python app.py`» — приложение бежит **под root**. Безопаснее гонять **в Docker** (есть офиц. образ `haileyydev/maildrop:latest`), а не рутом на хосте.
> - **Catch-all = слабая приватность по умолчанию**: кто дотянется до веб-UI, тот видит входящие. Защищай: `PROTECTED_ADDRESSES` (regex) + `PASSWORD` для чувствительных ящиков, **reverse-proxy c HTTPS/авторизацией**, файрвол. Не выставляй голым в интернет.

> [!info] Что умеет (по README)
> - Генерация **случайных** адресов и свои **кастомные** адреса.
> - **Пароль на отдельные ящики** (`PROTECTED_ADDRESSES` + `PASSWORD`).
> - Чистый UI, простая установка, **автоочистка** ящиков, лимит размера инбокса.
> - **Опциональная отправка** писем.
> - **JSON API** ([API Reference](https://github.com/haileyydev/maildrop/blob/main/docs/API.md)) — можно дёргать программно.
> - Конфиг через `.env`/переменные окружения (`FLASK_*`, `SMTP_*`, `DOMAIN`, лимиты).

> [!note] Зрелость
> Проект живой, но **некрупный**: создан **сентябрь 2025**, последний коммит — **июнь 2026** (на момент заметки ~1.5 мес затишья), ~664★, 55 форков, 3 открытых issue. **Релизов/тегов нет** — ставится из исходников (venv+pip) или из Docker-образа. Ждать «энтерпрайза» не стоит: это аккуратный простой инструмент.

## 🖥️ Применимость на системах владельца

Ключевое — **где живёт публичный IP + открытый порт 25 + домен**:

| Система | Как |
| :--- | :--- |
| **VPS / облако** | ✅ лучший вариант: там порт 25 обычно доступен, публичный IP есть. Через Docker (`haileyydev/maildrop:latest`), спереди — reverse-proxy с HTTPS |
| **Gentoo (основная) / Debian-Ubuntu / Arch** (дома) | ⚠️ технически запустится (Docker или python venv), но **домашний провайдер, вероятно, режет порт 25** → нужен туннель или всё же облако. Плюс домен с MX-записью |
| **Windows** | ⚠️ через Docker Desktop возможно, но по профилю нерелевантно |
| **Entware / RT-AX56U** | ➖ не тот кейс: Flask+SMTP «от root» на armv7/512 МБ — плохая идея, Docker на роутере нет, и порт 25 наружу всё равно упрётся в провайдера |

> [!tip] Тебе по профилю (self-host + расходная почта)
> Если хочется **свой** одноразовый мейл на своём домене и по минимуму возни — maildrop проще [opentrashmail](opentrashmail%20%28HaschekSolutions%29%20%E2%80%94%20%D1%81%D0%B0%D0%BC%D0%BE%D1%85%D0%BE%D1%81%D1%82%D0%B8%D1%80%D1%83%D0%B5%D0%BC%D1%8B%D0%B9%20catch-all%20trashmail%20%D1%81%D0%BE%20%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%20%D0%BC%D0%B5%D0%B9%D0%BB-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%BC%20%28Web-JSON%20API-RSS-%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B8%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B.md). Но если нужны **RSS/вебхуки/мульти-домен и автоматизация приёма 2FA** — бери opentrashmail (там богаче API и интеграции). Нужен **полный** почтовый сервер (IMAP, ящики, DKIM/DMARC) — это уже [docker-mailserver](docker-mailserver%20%E2%80%94%20production-ready%20%D0%BF%D0%BE%D1%87%D1%82%D0%BE%D0%B2%D1%8B%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B2%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%B5%20%28Postfix-Dovecot-Rspamd-ClamAV%29%2C%20%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%B0%D0%BC%D0%BD%D0%B8%20self-hosting.md). Разово поймать код без своего сервера — публичная [temp-mail](../../Apps/MailWave%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%B0%D1%8F%20%D0%BE%D0%B4%D0%BD%D0%BE%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F%20%28temp-mail%29%20%D0%BF%D0%BE%D1%87%D1%82%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D0%B8%20%28%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0%20%D0%BE%D1%82%20%D1%81%D0%BF%D0%B0%D0%BC%D0%B0%29%2C%20%D0%B3%D0%B4%D0%B5%20%D0%BF%D0%BE%D0%BB%D0%B5%D0%B7%D0%BD%D0%BE%20%D0%B8%20%D0%B3%D0%B4%D0%B5%20%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE.md). Практически: подними на **VPS в Docker**, за reverse-proxy с HTTPS, чувствительные адреса — под паролем.

## 🔗 Связанные заметки

- Более функциональный родственник (RSS/вебхуки/API, мульти-домен): [opentrashmail — свой catch-all trashmail с API](opentrashmail%20%28HaschekSolutions%29%20%E2%80%94%20%D1%81%D0%B0%D0%BC%D0%BE%D1%85%D0%BE%D1%81%D1%82%D0%B8%D1%80%D1%83%D0%B5%D0%BC%D1%8B%D0%B9%20catch-all%20trashmail%20%D1%81%D0%BE%20%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%20%D0%BC%D0%B5%D0%B9%D0%BB-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BE%D0%BC%20%28Web-JSON%20API-RSS-%D0%B2%D0%B5%D0%B1%D1%85%D1%83%D0%BA%D0%B8%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B.md)
- Когда нужен ПОЛНЫЙ почтовый сервер (IMAP, отправка, антиспам): [docker-mailserver — почтовый сервер в контейнере](docker-mailserver%20%E2%80%94%20production-ready%20%D0%BF%D0%BE%D1%87%D1%82%D0%BE%D0%B2%D1%8B%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B2%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%B5%20%28Postfix-Dovecot-Rspamd-ClamAV%29%2C%20%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%B0%D0%BC%D0%BD%D0%B8%20self-hosting.md)
- Публичная одноразовая почта без своего сервера: [MailWave — temp-mail без регистрации](../../Apps/MailWave%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%B0%D1%8F%20%D0%BE%D0%B4%D0%BD%D0%BE%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F%20%28temp-mail%29%20%D0%BF%D0%BE%D1%87%D1%82%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D0%B8%20%28%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0%20%D0%BE%D1%82%20%D1%81%D0%BF%D0%B0%D0%BC%D0%B0%29%2C%20%D0%B3%D0%B4%D0%B5%20%D0%BF%D0%BE%D0%BB%D0%B5%D0%B7%D0%BD%D0%BE%20%D0%B8%20%D0%B3%D0%B4%D0%B5%20%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE.md)

## 🔗 Ссылки

- Репозиторий: [github.com/haileyydev/maildrop](https://github.com/haileyydev/maildrop) · [Sending](https://github.com/haileyydev/maildrop/blob/main/docs/SENDING.md) · [API](https://github.com/haileyydev/maildrop/blob/main/docs/API.md)
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5807)

#Сеть #Почта #SelfHosted #TempMail #CatchAll #Python #Инструменты
