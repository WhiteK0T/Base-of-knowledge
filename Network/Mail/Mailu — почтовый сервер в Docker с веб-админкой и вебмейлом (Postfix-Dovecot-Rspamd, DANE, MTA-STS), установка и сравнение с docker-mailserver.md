---
создал заметку: 2026-10-14T13:00:00
author: WhiteK0T
tags:
  - Сеть
  - Почта
  - SelfHosted
  - Docker
  - Email
Источник:
  - https://t.me/open_source_friend/5851
  - https://github.com/Mailu/Mailu
  - https://mailu.io/2024.06/
  - https://setup.mailu.io/
---

# 📬 Mailu — почтовый сервер в Docker с веб-админкой и вебмейлом

**[Mailu](https://github.com/Mailu/Mailu)** — полноценный почтовый сервер из набора Docker-образов: приём и отправка почты, IMAP, антиспам, антивирус, веб-почта и **веб-панель администратора** «из коробки». Проект с 2016 года, лицензия **MIT**, все компоненты — свободное ПО, без трекеров.

| | |
| :--- | :--- |
| Звёзды / форки | **7 551** · 1 012 |
| Текущая стабильная ветка | **2024.06** — новых крупных версий с июня 2024 нет, но патч-релизы выходят постоянно: последний **2024.06.63** от 13.10.2026 |
| Архитектуры образов | amd64, arm64, armv7 |
| Документация | [mailu.io/2024.06](https://mailu.io/2024.06/) · демо-сервер: [mailu.io/master/demo.html](https://mailu.io/master/demo.html) |

Всё перечисленное в посте подтверждается README.

---

## 1. Что внутри

| Контейнер | Что делает |
| :--- | :--- |
| `front` (nginx) | вход для всех протоколов, TLS, Let's Encrypt, раздача MTA-STS |
| `smtp` (Postfix) | приём и отправка, SMTP и Submission (465/587) |
| `imap` (Dovecot) | IMAP/POP3, Sieve-фильтры, квоты, полнотекстовый поиск (xapian) |
| `antispam` (Rspamd) | спам, greylisting, DKIM-подпись исходящих, проверка SPF/DMARC, самообучение |
| `admin` (Python/Flask) | веб-панель: домены, ящики, алиасы, квоты, делегирование доменов, REST API |
| `webmail` | **Roundcube** или **SnappyMail** (PHP с защитой Snuffleupagus) |
| `resolver` (Unbound) | **валидирующий DNSSEC-резолвер** — нужен для DANE |
| опционально | `antivirus` (ClamAV), `fts_attachments` (Apache Tika — поиск по содержимому вложений), `fetchmail`, `webdav` (Radicale — календари и контакты), `oletools` (блокировка вредоносных макросов в офисных вложениях) |

### Возможности

- **Для пользователей**: алиасы, автоответ, пересылка, забор почты с других ящиков, ManageSieve, публикация OpenPGP-ключей через WKD, настройки почтовых клиентов автоматически (autoconfig).
- **Для администратора**: глобальные админы, объявления для всех, делегирование доменов, квоты, алиасы доменов, своя маршрутизация, CLI и REST API.
- **Безопасность**: TLS обязателен, **DANE** и **MTA-STS** для исходящих (письмо не уйдёт на сервер с битым TLS), Let's Encrypt, DKIM, DMARC, SPF, защита от подмены отправителя.

---

## 2. Mailu или docker-mailserver

В базе уже есть [docker-mailserver](docker-mailserver%20%E2%80%94%20production-ready%20%D0%BF%D0%BE%D1%87%D1%82%D0%BE%D0%B2%D1%8B%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B2%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%B5%20%28Postfix-Dovecot-Rspamd-ClamAV%29%2C%20%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%B0%D0%BC%D0%BD%D0%B8%20self-hosting.md) — там же подробно о главной проблеме своей почты: порт 25, PTR и репутация IP.

| | **Mailu** | **docker-mailserver** |
| :--- | :--- | :--- |
| Устройство | ~8–12 контейнеров, по одному на службу | один контейнер |
| Управление | **веб-панель** + CLI + REST API | `setup.sh` и текстовые файлы |
| Вебмейл | **есть** (Roundcube или SnappyMail) | нет, ставится отдельно |
| Хранение аккаунтов | база (SQLite — по умолчанию и рекомендуется; можно PostgreSQL или MySQL/MariaDB) | текстовые файлы или LDAP, без БД |
| Конфиг в git | частично (`mailu.env`, `docker-compose.yml`), аккаунты — в базе | целиком |
| Календари и контакты | опционально (Radicale) | нет |
| DANE, MTA-STS | встроено | настраивается вручную |
| Минимум памяти | 1 ГБ + 1 ГБ swap; с ClamAV — 3 ГБ | от 2 ГБ с ClamAV |

**Коротко:** Mailu — когда хочется «почту с панелью» для нескольких доменов и пользователей; docker-mailserver — когда удобнее всё описать файлами и держать в git, а веб-почта не нужна.

---

## 3. Требования

- **Память**: 1 ГБ RAM + 1 ГБ swap без антивируса, **3 ГБ RAM + 1 ГБ swap с ClamAV**. Поиск по вложениям (Tika) — ещё **1–2 ГБ**.
- **Процессор x86_64 с SSE4.2** (не подойдут, например, Intel Atom до 2013 года).
- **Свободные порты** на хосте: 25, 80, 110, 143, 443, 465, 587, 993, 995, 4190 — Mailu занимает их сам. Если на сервере уже есть nginx или другой веб-сервер на 80/443 — см. раздел про обратный прокси в документации (рекомендуют Traefik).
- **Статический IP, PTR-запись на имя сервера, открытый исходящий 25-й порт** — без этого почта не дойдёт (подробно — в заметке про docker-mailserver).
- **DNSSEC-валидирующий резолвер** — с версии 1.9 обязателен. Встроенный Unbound это решает; если используете свой резолвер, проверьте, что он проверяет DNSSEC.
- Без Docker Mailu не поддерживается.

---

## 4. Установка

### Docker на хосте

| Система | Команды |
| :--- | :--- |
| **Gentoo** | `emerge --ask app-containers/docker app-containers/docker-compose`, затем `rc-update add docker default && rc-service docker start` |
| **Debian / Ubuntu** | официальный репозиторий Docker: `apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin` (инструкция — [docs.docker.com](https://docs.docker.com/engine/install/debian/)), служба стартует сама |
| **Arch** | `pacman -S docker docker-compose`, затем `systemctl enable --now docker` |
| **Entware** | не подходит: на роутере с 512 МБ RAM весь стек не запустить |

Для почты обычно берут отдельный VPS. Авторы тестируют Mailu в основном на Debian stable.

### Развёртывание

1. Сгенерировать конфиг в мастере **[setup.mailu.io](https://setup.mailu.io/)**: выбрать версию 2024.06, домен, имена хостов, нужные компоненты (вебмейл, антивирус, Tika и т.п.). Мастер выдаст `docker-compose.yml` и `mailu.env` и команды для скачивания.
2. Положить их в `/mailu` и запустить:
   ```bash
   cd /mailu
   docker compose pull
   docker compose up -d
   docker compose exec admin flask mailu admin admin example.com 'ПАРОЛЬ'   # первый администратор
   ```
3. Войти в панель `https://mail.example.com/admin`, создать домен и ящики.
4. В панели на странице домена сгенерировать ключ **DKIM** и взять готовые DNS-записи: **MX, SPF, DKIM, DMARC**, при желании TLSA (DANE), autoconfig и MTA-STS. Добавить их у DNS-провайдера, у хостера — **PTR** на имя сервера.
5. Проверить доставку, например, через [mail-tester.com](https://www.mail-tester.com/).

### Обновление

В пределах ветки 2024.06 — просто `docker compose pull && docker compose up -d`. При переходе на новую ветку конфиг нужно сгенерировать заново в мастере и перенести свои настройки (так написано в CHANGELOG).

> [!tip] Полезное из CHANGELOG 2024.06
> - На процессорах с AVX можно включить усиленный аллокатор памяти: если в `docker compose logs admin` есть подсказка про `hardened-malloc`, добавьте в `mailu.env` строку `LD_PRELOAD=/usr/lib/libhardened_malloc.so` и пересоздайте контейнеры.
> - После обновления пересоберите индексы полнотекстового поиска: `docker compose exec imap doveadm fts rescan -A`.

---

## 5. Что учесть

- Документация прямо пишет: проект работает с 2016 года и обслуживает сотни ящиков, но **«не прошёл массового тестирования»** — перед боевым использованием проверьте все нужные функции. За коммерческой поддержкой авторы отправляют к Poste.io, на идеях которого основан Mailu.
- **Бэкапы**: каталог `/mailu` целиком (почта, база админки, DKIM-ключи, сертификаты).
- Если какой-то домен-получатель с битыми DANE или TLS не принимает почту, для него можно ослабить политику — это описано в FAQ.
- Логи — через `docker compose logs`; для файлов на диске FAQ советует journald + rsyslog.

## 🔗 Ссылки

- Репозиторий: https://github.com/Mailu/Mailu
- Документация (стабильная ветка): https://mailu.io/2024.06/
- Мастер конфигурации: https://setup.mailu.io/
- Демо: https://mailu.io/master/demo.html
- Исходный пост: https://t.me/open_source_friend/5851

#Сеть #Почта #SelfHosted #Docker #Email
