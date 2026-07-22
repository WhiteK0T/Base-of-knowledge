---
создал заметку: 2026-07-22T10:30:00
author: WhiteK0T
tags:
  - Network
  - WebServer
  - TLS
  - HTTPS
  - LetsEncrypt
  - ACME
  - nginx
  - Apache
  - Security
Источник:
  - https://letsencrypt.org/docs/
  - https://github.com/acmesh-official/acme.sh
  - https://eff-certbot.readthedocs.io/
---

# 🔐 Let's Encrypt — выпуск TLS-сертификата и связка с nginx и Apache

Практическое руководство: как получить **бесплатный TLS/SSL-сертификат** (Let's Encrypt по протоколу **ACME**) и подключить его к **nginx** и **Apache**. Покрыты оба ACME-клиента — **certbot** (официальный, с плагинами) и **acme.sh** (лёгкий shell-скрипт), способы проверки владения доменом (**HTTP-01 / DNS-01 / TLS-ALPN-01**), **wildcard**, **автопродление** и грабли.

> [!info] Как это работает в двух словах
> **ACME** — протокол автоматической выдачи сертификатов. Клиент на твоём сервере доказывает удостоверяющему центру (CA), что домен **действительно твой** (проходит *challenge*), CA выдаёт сертификат сроком **90 дней**. Продление автоматическое — поэтому короткий срок не проблема. Всё бесплатно, без регистрации.

## 🧩 Выбор способа проверки владения (challenge)

| Метод | Как доказываем | Когда использовать | Wildcard |
| :--- | :--- | :--- | :--- |
| **HTTP-01** | CA читает файл по `http://домен/.well-known/acme-challenge/…` | стандарт: сервер смотрит в интернет, открыт порт **80** | ❌ нет |
| **DNS-01** | кладём **TXT-запись** `_acme-challenge.домен` | нужен **wildcard** `*.домен`, или порт 80 закрыт/за NAT, или сервер внутренний | ✅ да |
| **TLS-ALPN-01** | спецрукопожатие на порту **443** | порт 80 занят/закрыт, а 443 свободен | ❌ нет |

> [!tip] Что выбрать
> - Обычный сайт с белым IP и портом 80 → **HTTP-01** (проще всего).
> - **Wildcard** (`*.example.com`) или сервер за CGNAT/серым IP, роутер, «внутренний» хост → **DNS-01** (нужен API твоего DNS-провайдера или ручная TXT-запись).

## 🏭 Удостоверяющие центры (CA) и клиенты

- **CA:** по умолчанию — **Let's Encrypt**. Альтернативы на том же ACME: **ZeroSSL**, **Buypass**, **Google Trust Services**. У Let's Encrypt есть [лимиты](https://letsencrypt.org/docs/rate-limits/) (напр. 50 сертификатов на зарегистрированный домен в неделю) — при отладке используй **staging**-окружение (`--staging` / `--server letsencrypt_test`), чтобы не выжечь лимит.
- **Клиенты:**
  - **certbot** — официальный от EFF, Python, есть **плагины `--nginx` / `--apache`**, которые сами правят конфиг. Удобно для «одной командой».
  - **acme.sh** — чистый **shell-скрипт** (нужен только `curl`/`openssl`/`socat`), не тянет Python, огромный список DNS-API. Идеален для **роутеров/embedded** и когда не хочешь, чтобы клиент лез в конфиг веб-сервера.
  - **lego** (Go, один бинарь), **Caddy** (веб-сервер со встроенным ACME — HTTPS «из коробки») — как альтернативы.

## 📦 Установка клиента по системам

| Система | certbot | acme.sh |
| :--- | :--- | :--- |
| **Gentoo** (основная) | `emerge app-crypt/certbot` (+ `app-crypt/certbot-nginx` / `app-crypt/certbot-apache` для плагинов) | `emerge app-crypt/acme-sh` |
| **Debian / Ubuntu** | `apt install certbot python3-certbot-nginx python3-certbot-apache` | `curl https://get.acme.sh \| sh -s email=you@example.com` |
| **Arch** (план с июня 2026) | `pacman -S certbot certbot-nginx certbot-apache` | из AUR: `yay -S acme.sh-git`, либо официальный установщик |
| **Entware / RT-AX56U** | ⚠️ `opkg install python3` + pip — тяжело для 512 МБ; **не рекомендуется** | ✅ **предпочтительно**: `opkg install acme.sh` (или установщик); ставь только нужный DNS-API (напр. `dns_cf.sh` для Cloudflare) и работай через **DNS-01** — не надо открывать порт 80 на роутере |

> [!note] certbot: snap/pip для самой свежей версии
> Если в дистрибутиве старый certbot и нужен новый плагин/фича — EFF предлагает ставить через **snap** или **pipx/venv**. На Gentoo/Arch/Debian для типовых задач достаточно пакета из репозитория.

## 🚀 Способ 1. certbot — «одной командой» (правит конфиг сам)

Плагин сам находит `server`/`VirtualHost`, вставляет `ssl_certificate*` и (по желанию) редирект на HTTPS.

**nginx:**
```bash
certbot --nginx -d example.com -d www.example.com
```
**Apache:**
```bash
certbot --apache -d example.com -d www.example.com
```
Certbot спросит e-mail (для уведомлений об истечении), согласие с ToS и хотите ли редирект HTTP→HTTPS. Готово — сертификат в `/etc/letsencrypt/live/example.com/`.

> [!tip] Только выпустить, конфиг править руками — режим `certonly`
> Если не хочешь, чтобы certbot трогал конфиг (например, у тебя тонко настроенный nginx):
> ```bash
> # webroot: файлы challenge кладутся в каталог, который уже отдаёт веб-сервер
> certbot certonly --webroot -w /var/www/html -d example.com
> # или без веб-сервера вообще (certbot сам поднимет временный на :80)
> certbot certonly --standalone -d example.com
> ```

## 🚀 Способ 2. acme.sh — лёгкий, не трогает веб-сервер

**Выпуск (webroot, HTTP-01):**
```bash
acme.sh --issue -d example.com -w /var/www/html
```
**Выпуск (standalone, если порт 80 свободен):**
```bash
acme.sh --issue -d example.com --standalone
```
**Wildcard (DNS-01, пример Cloudflare):**
```bash
export CF_Token="cloudflare_api_token"
acme.sh --issue --dns dns_cf -d example.com -d '*.example.com'
```
**Установка сертификата в нужные пути + команда перезапуска веб-сервера:**
```bash
acme.sh --install-cert -d example.com \
  --key-file       /etc/ssl/example.com/privkey.pem \
  --fullchain-file /etc/ssl/example.com/fullchain.pem \
  --reloadcmd      "nginx -s reload"        # или "apachectl graceful" / "rc-service apache2 reload"
```

> [!warning] acme.sh по умолчанию берёт CA ZeroSSL
> Начиная с недавних версий, acme.sh по умолчанию использует **ZeroSSL** (требует привязки e-mail при регистрации аккаунта). Чтобы явно взять Let's Encrypt:
> ```bash
> acme.sh --set-default-ca --server letsencrypt
> ```

## 🔗 Подключение сертификата вручную

Где бы ты ни выпустил сертификат, веб-серверу нужны два файла: **цепочка (fullchain)** и **приватный ключ**.

### nginx

```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # современные протоколы и заголовок HSTS (по желанию)
    ssl_protocols TLSv1.2 TLSv1.3;
    add_header Strict-Transport-Security "max-age=63072000" always;

    root /var/www/example.com;
}

# редирект HTTP→HTTPS + оставляем путь для ACME-челленджа
server {
    listen 80;
    server_name example.com;
    location /.well-known/acme-challenge/ { root /var/www/html; }
    location / { return 301 https://$host$request_uri; }
}
```
Проверить и применить:
```bash
nginx -t && systemctl reload nginx     # OpenRC (Gentoo): rc-service nginx reload
```

### Apache (httpd)

Включить модули (Debian: `a2enmod ssl headers rewrite`; Gentoo — USE-флаг `apache2_modules_ssl`; Arch — раскомментировать `LoadModule ssl_module` в `httpd.conf`):

```apache
<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/example.com

    SSLEngine on
    SSLCertificateFile      /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile   /etc/letsencrypt/live/example.com/privkey.pem
    # на современных Apache (>=2.4.8) fullchain кладётся в SSLCertificateFile;
    # отдельный SSLCertificateChainFile уже не нужен

    Protocols h2 http/1.1
    Header always set Strict-Transport-Security "max-age=63072000"
</VirtualHost>

<VirtualHost *:80>
    ServerName example.com
    # путь для ACME-челленджа не редиректим
    Alias /.well-known/acme-challenge/ /var/www/html/.well-known/acme-challenge/
    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/\.well-known/acme-challenge/
    RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
</VirtualHost>
```
Проверить и применить:
```bash
apachectl configtest && systemctl reload apache2   # Gentoo: rc-service apache2 reload; Arch: httpd
```

> [!note] Различие путей у Apache в дистрибутивах
> Служба и конфиги называются по-разному: **Debian/Ubuntu** — `apache2`, конфиги в `sites-available/` (`a2ensite`); **Gentoo/Arch/RHEL** — `httpd`, конфиг `/etc/httpd/` или `/etc/apache2/` (Gentoo) с `vhosts.d/`. Команда перезагрузки и имя службы (`apache2` vs `httpd`) отличаются — подставляй своё.

## ♻️ Автопродление (сертификат живёт 90 дней)

> [!tip] Проверяй продление в «сухом» режиме — не дожидаясь реального истечения
> ```bash
> certbot renew --dry-run     # certbot: имитация продления всех сертификатов
> acme.sh --renew -d example.com --force   # acme.sh: принудительно
> ```

- **certbot** при установке из пакета обычно **сам ставит** systemd-таймер (`systemctl list-timers | grep certbot`) или cron — продлевает и перезагружает веб-сервер автоматически. Проверь, что таймер активен.
- **acme.sh** при установке прописывает **свою cron-задачу** (`acme.sh --install-cronjob`); продление вызывает `--reloadcmd`.
- **Gentoo (OpenRC, нет systemd-таймеров):** добавь cron вручную, напр. в `/etc/cron.daily/`:
  ```bash
  #!/bin/sh
  certbot renew --quiet --deploy-hook "rc-service nginx reload"
  ```
- **Ключевой момент:** после продления веб-сервер должен **перечитать** сертификат — через `--deploy-hook` (certbot) или `--reloadcmd` (acme.sh). Без этого он продолжит отдавать старый до перезапуска.

## 🇷🇺 Контекст РФ

> [!info] Let's Encrypt в России работает; про «нац. УЦ» — отдельная история
> - Для **обычных сайтов** Let's Encrypt/ZeroSSL прекрасно выпускаются и на `.ru`/`.рф` — иностранный CA тут ни при чём, всё автоматизировано.
> - **НУЦ Минцифры (Russian Trusted Root CA)** — отдельный национальный УЦ, сертификаты выпускаются через Госуслуги. Нюанс: его корень **не в доверии** у Chrome/Firefox/Opera по умолчанию — «из коробки» доверяют лишь **Яндекс.Браузер** и **Atom**; остальным нужно вручную ставить корневой сертификат. Для своих проектов это обычно **не нужно** — бери Let's Encrypt; нац. УЦ актуален для госсервисов и случаев, когда иностранный CA отозвал/не выдал сертификат.

## 🧯 Частые грабли

- **Порт 80 закрыт/за NAT/CGNAT** → HTTP-01 не пройдёт. Решение: **DNS-01** (или проброс порта, белый IP).
- **Редирект на путь челленджа** — общий `return 301`/`RewriteRule` перехватывает `/.well-known/acme-challenge/` → валидация падает. **Исключай** этот путь из редиректа (см. конфиги выше).
- **Забыли reload после продления** → браузер видит просроченный серт, хотя файл уже новый. Нужен deploy-hook/reloadcmd.
- **Rate limit Let's Encrypt** при отладке → используй `--staging`, потом переключайся на прод.
- **Cloudflare-прокси (оранжевое облако)**: сертификат на origin всё равно нужен (mode **Full/Full strict**); HTTP-01 через прокси может мешать — надёжнее **DNS-01** или Cloudflare Origin CA.
- **Права на `privkey.pem`** — ключ должен быть `600`/`640` и недоступен посторонним; веб-сервер читает его от root на старте.
- **Wildcard только через DNS-01** — HTTP-01 wildcard не умеет.

## 🔗 Ссылки

- Документация: [Let's Encrypt Docs](https://letsencrypt.org/docs/) · [certbot (EFF)](https://eff-certbot.readthedocs.io/) · [acme.sh (GitHub)](https://github.com/acmesh-official/acme.sh) · [список DNS-API acme.sh](https://github.com/acmesh-official/acme.sh/wiki/dnsapi)
- Проверка настроек TLS: [SSL Labs](https://www.ssllabs.com/ssltest/) · [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/)
- Применение на практике: [Хостинг install ISO на своём сервере для VirtFusion (nginx, без редиректов)](%D0%A5%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20install%20ISO%20%D0%BD%D0%B0%20%D1%81%D0%B2%D0%BE%D1%91%D0%BC%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B5%20%D0%B4%D0%BB%D1%8F%20VirtFusion%20%E2%80%94%20%D0%BF%D1%80%D1%8F%D0%BC%D0%B0%D1%8F%20HTTPS-%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D1%80%D0%B5%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%20%28nginx%29.md)

#Network #WebServer #TLS #HTTPS #LetsEncrypt #ACME #nginx #Apache #Security
