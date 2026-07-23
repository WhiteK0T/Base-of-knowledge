---
создал заметку: 2026-07-23T10:00:00
author: WhiteK0T
tags:
  - Network
  - WebServer
  - nginx
  - ReverseProxy
  - HTTP
  - TLS
  - Linux
Источник:
  - https://nginx.org/en/docs/
  - https://github.com/nginx/nginx
---

# 🟩 nginx — веб-сервер и reverse-proxy: подробный разбор

**nginx** («engine-x») — высокопроизводительный **веб-сервер**, **reverse-proxy**, **балансировщик нагрузки** и **HTTP-кэш**. Ключевая особенность — **событийная (event-driven), асинхронная** архитектура: один рабочий процесс обслуживает **тысячи одновременных соединений** без потока-на-запрос (как было у старого Apache prefork). Отсюда низкое потребление памяти и отличная отдача статики/прокси под нагрузкой.

> [!info] Где nginx применяют
> - **Отдача статики** (файлы, SPA-фронтенд) — быстро и дёшево.
> - **Reverse-proxy** перед бэкендом (Node/Python/PHP-FPM/Go/Java) — TLS-терминация, буферизация, заголовки.
> - **Балансировщик** нагрузки на несколько апстримов.
> - **API-gateway / кэш** перед медленным бэкендом.
> - **Терминация TLS** и редирект HTTP→HTTPS.

Актуальные ветки (2026): **стабильная 1.30.x**, **mainline 1.31.x**. **HTTP/3 (QUIC)** — в mainline с 1.25.0 и в свежих стабильных сборках. Mainline обычно **рекомендуют даже в прод** (новее и без критичных багов), stable — только критические багфиксы.

## 📦 Установка по системам

| Система | Установка | Служба | Конфиг |
| :--- | :--- | :--- | :--- |
| **Gentoo** (основная) | `emerge www-servers/nginx` — набор модулей задаётся **USE/`NGINX_MODULES_*`** в `/etc/portage/make.conf` (напр. `NGINX_MODULES_HTTP="... stub_status realip gzip_static v2 ..."`), пересобрать после правки | **OpenRC:** `rc-update add nginx default && rc-service nginx start` | `/etc/nginx/nginx.conf` |
| **Debian / Ubuntu** | `apt install nginx` (из репо дистрибутива), либо подключить **официальный репозиторий nginx.org** для mainline/stable | **systemd:** `systemctl enable --now nginx` | `/etc/nginx/`, паттерн `sites-available/` + `sites-enabled/` |
| **Arch** (план с июня 2026) | `pacman -S nginx` (stable) или `nginx-mainline`; модули — отдельными пакетами `nginx-mod-*` | **systemd:** `systemctl enable --now nginx` | `/etc/nginx/nginx.conf` + `conf.d/` |
| **Entware / RT-AX56U** | `opkg install nginx` — **есть под armv7, лёгкий** (nginx как раз хорош для слабого железа). Учти: штатная веб-админка роутера уже слушает :80 — вешай nginx на **другой порт** и клади сайты на USB-диск | init-скрипт Entware: `/opt/etc/init.d/S80nginx` (`start`/`stop`/`restart`) | `/opt/etc/nginx/nginx.conf` |

> [!tip] Проверка версии и собранных модулей
> ```bash
> nginx -v          # версия
> nginx -V 2>&1     # версия + флаги сборки и список модулей (в т.ч. --with-http_v3_module)
> ```
> На Gentoo модуль работает, только если включён нужный `NGINX_MODULES_*` USE-флаг и nginx пересобран.

## 🗂️ Структура конфигурации

Конфиг — дерево **контекстов (блоков)**. Иерархия:

```nginx
# main-контекст (глобальный)
user  nginx;
worker_processes  auto;          # обычно = числу ядер

events {                         # events-контекст
    worker_connections  1024;    # соединений на воркер
}

http {                           # http-контекст (весь HTTP/HTTPS)
    include       mime.types;
    default_type  application/octet-stream;
    sendfile      on;
    keepalive_timeout  65;

    include /etc/nginx/conf.d/*.conf;          # подключаемые куски
    # (Debian) include /etc/nginx/sites-enabled/*;

    server {                     # server-контекст = виртуальный хост
        listen 80;
        server_name example.com;

        location / {             # location-контекст = маршрут
            root /var/www/example.com;
        }
    }
}
```

> [!note] Два стиля организации файлов
> - **Debian/Ubuntu:** сайты — отдельные файлы в `sites-available/`, включаются симлинком в `sites-enabled/` (`ln -s ../sites-available/site.conf .`; в Debian есть хелперы). Удобно включать/выключать сайты.
> - **Gentoo/Arch/RHEL/Entware:** обычно всё в `conf.d/*.conf` (или прямо в `nginx.conf`). Паттерна `sites-*` из коробки нет — можно сделать самому через `include`.

## 🌐 server-блоки (виртуальные хосты)

Один nginx обслуживает много доменов — каждый в своём `server`. Выбор блока — по паре **`listen` + `server_name`**:

```nginx
server {
    listen 80;
    listen [::]:80;              # IPv6
    server_name example.com www.example.com;   # можно wildcard: *.example.com
    root /var/www/example.com;
    index index.html;
}
```

- `server_name _;` — «дефолтный» блок для несовпавших имён.
- Первый `server` с `listen ... default_server;` ловит запросы без совпадения по имени.

## 🎯 location — как nginx выбирает маршрут

Порядок сопоставления `location` (важно — **не** сверху вниз, а по приоритету):

| Синтаксис | Тип | Приоритет |
| :--- | :--- | :--- |
| `location = /path` | **точное** совпадение | 1 (высший) |
| `location ^~ /path` | префикс, **без** проверки регэкспов дальше | 2 |
| `location ~ /re` / `~* /re` | **регэксп** (чувств. / без учёта регистра) | 3 (в порядке записи) |
| `location /path` | префикс (обычный) | 4 (самый длинный префикс) |

```nginx
location = /favicon.ico { access_log off; expires 30d; }
location ^~ /static/    { root /var/www; }             # /static/* — без регэкспов
location ~* \.(jpg|png|css|js)$ { expires 7d; }        # кэш ассетов
location / { try_files $uri $uri/ =404; }              # всё остальное
```

> [!warning] `root` vs `alias` — частая ошибка
> - `root /var/www;` + `location /static/` → файл ищется как `/var/www/static/<...>` (path **добавляется** к root).
> - `alias /data/files/;` + `location /static/` → `/static/x.png` маппится в `/data/files/x.png` (**заменяет** префикс location). Для `alias` **обязателен** завершающий слэш и осторожность с регэкспами.

> [!tip] try_files — основа маршрутизации
> ```nginx
> try_files $uri $uri/ /index.html;     # SPA: отдать файл, иначе index.html
> try_files $uri $uri/ /index.php?$query_string;   # PHP-фреймворк
> ```
> Проверяет файлы по очереди, отдаёт первый существующий; последний аргумент — фолбэк/внутренний редирект.

## 🔁 Reverse-proxy и балансировка

Проксирование запроса на бэкенд:

```nginx
upstream backend {
    # балансировка (по умолчанию round-robin)
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    # least_conn;               # или по числу соединений
    # ip_hash;                  # прилипание клиента к бэкенду
    keepalive 32;               # пул keep-alive соединений к апстриму
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection        "";       # для keepalive к апстриму
    }

    # WebSocket (Upgrade) — если бэкенд их использует
    location /ws/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade    $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

> [!caution] Про `X-Forwarded-*` и доверие заголовкам
> nginx **добавляет** `X-Forwarded-For`, но бэкенд должен доверять ему только **от твоего прокси**. Если бэкенд сам стоит за nginx, настрой в нём trusted proxies — иначе клиент подделает заголовок. (Ровно эта модель «доверенного прокси» ломала [Gitea — обход аутентификации через reverse-proxy (CVE-2026-20896)](../../../Security/Vulns/Apps/Gitea%20%E2%80%94%20%D0%BE%D0%B1%D1%85%D0%BE%D0%B4%20%D0%B0%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20reverse-proxy%20%28CVE-2026-20896%2C%20X-WEBAUTH-USER%2C%20Docker%29.md): доверяли `X-WEBAUTH-USER` от кого угодно.)

## 🔐 TLS / HTTPS

Полное руководство по **выпуску сертификата** (Let's Encrypt, certbot/acme.sh, HTTP-01/DNS-01, wildcard, автопродление) — в отдельной заметке: [Let's Encrypt — выпуск TLS-сертификата и связка с nginx и Apache](../Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md). Минимальный HTTPS-блок:

```nginx
server {
    listen 443 ssl;
    http2 on;                    # с 1.25.1 — отдельная директива (не "listen ... http2")
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    add_header Strict-Transport-Security "max-age=63072000" always;   # HSTS

    root /var/www/example.com;
}

server {                          # редирект HTTP→HTTPS (кроме ACME-челленджа)
    listen 80;
    server_name example.com;
    location /.well-known/acme-challenge/ { root /var/www/html; }
    location / { return 301 https://$host$request_uri; }
}
```

> [!info] HTTP/2 и HTTP/3 (QUIC)
> - **HTTP/2:** директива `http2 on;` внутри `server` (в старых версиях — `listen 443 ssl http2;`, сейчас deprecated).
> - **HTTP/3 (QUIC):** нужен модуль `http_v3` (проверь `nginx -V`), слушать **UDP 443** и анонсировать через `Alt-Svc`:
>   ```nginx
>   listen 443 quic reuseport;
>   listen 443 ssl;
>   http2 on;
>   add_header Alt-Svc 'h3=":443"; ma=86400';
>   ```
> Готовые TLS-настройки удобно генерить в [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/), проверять — [SSL Labs](https://www.ssllabs.com/ssltest/).

## 📄 Отдача статики, сжатие, кэш

```nginx
# gzip
gzip on;
gzip_types text/css application/javascript application/json image/svg+xml;
gzip_min_length 1024;

# кэш-заголовки для ассетов
location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff2?)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# кэш ответов бэкенда (proxy_cache)
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api:10m max_size=1g inactive=60m;
location /api/ {
    proxy_cache api;
    proxy_cache_valid 200 5m;
    add_header X-Cache-Status $upstream_cache_status;   # HIT/MISS в ответе
    proxy_pass http://backend;
}
```

## 🛡️ Базовая защита и лимиты

```nginx
server_tokens off;               # не светить версию nginx в заголовках/ошибках

# заголовки безопасности
add_header X-Content-Type-Options nosniff always;
add_header X-Frame-Options SAMEORIGIN always;
add_header Referrer-Policy strict-origin-when-cross-origin always;

# rate limiting: не больше 10 r/s на IP по зоне
limit_req_zone $binary_remote_addr zone=perip:10m rate=10r/s;
location /login {
    limit_req zone=perip burst=20 nodelay;
    proxy_pass http://backend;
}

# ограничить доступ по IP
location /admin/ { allow 10.0.0.0/8; deny all; }
```

> [!danger] Держи nginx обновлённым — в нём тоже бывают RCE
> nginx — не «магически безопасен». Пример: [CVE-2026-42945 «NGINX Rift»](../../../Security/Vulns/Linux/CVE/CVE-2026-42945%20%E2%80%94%20NGINX%20Rift%20%28ngx_http_rewrite_module%20heap%20overflow%2C%20RCE-DoS%29.md) — heap-overflow в `ngx_http_rewrite_module` (RCE/DoS). Обновляй пакет вовремя (GLSA/DSA-USN/Arch advisory), не открывай наружу лишние `location`, отдавай только то, что нужно.

## ⚙️ Управление службой и проверка

```bash
nginx -t                          # проверить синтаксис конфига ПЕРЕД применением
nginx -T                          # показать полный собранный конфиг (со всеми include)

# перезагрузка без разрыва соединений (graceful) — предпочтительно:
systemctl reload nginx            # systemd (Debian/Ubuntu/Arch)
rc-service nginx reload           # OpenRC (Gentoo)
/opt/etc/init.d/S80nginx restart  # Entware
nginx -s reload                   # напрямую сигналом

# полный рестарт (рвёт соединения) — только когда reload недостаточно:
systemctl restart nginx
```

> [!warning] Всегда `nginx -t` перед reload
> `reload` с битым конфигом **не применится** (nginx оставит старый рабочим), но привычка `nginx -t && reload` избавляет от сюрпризов, особенно в скриптах/деплое.

## 🔍 Логи и диагностика

- **Access-лог:** `/var/log/nginx/access.log` (кастомизируется `log_format`).
- **Error-лог:** `/var/log/nginx/error.log` — сюда падают 5xx, проблемы апстрима, права доступа; уровень `error_log ... warn|info|debug;`.
- **Статус:** модуль `stub_status` (`location /nginx_status { stub_status; }`) — активные соединения, запросы.
- Частое: **502 Bad Gateway** — бэкенд лёг/недоступен по `proxy_pass`; **403** — права на файлы/`root`; **404** — неверный `root`/`alias`/`try_files`; **413** — увеличить `client_max_body_size`.

## 🔗 Смежные заметки

- [Let's Encrypt — выпуск TLS-сертификата и связка с nginx и Apache](../Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md) — сертификаты подробно.
- [Хостинг install ISO на своём сервере для VirtFusion (nginx, прямая HTTPS без редиректов)](../%D0%A5%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3%20install%20ISO%20%D0%BD%D0%B0%20%D1%81%D0%B2%D0%BE%D1%91%D0%BC%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B5%20%D0%B4%D0%BB%D1%8F%20VirtFusion%20%E2%80%94%20%D0%BF%D1%80%D1%8F%D0%BC%D0%B0%D1%8F%20HTTPS-%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D1%80%D0%B5%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%20%28nginx%29.md) — практический пример отдачи файла на nginx.
- [CVE-2026-42945 — NGINX Rift (heap overflow в rewrite-модуле)](../../../Security/Vulns/Linux/CVE/CVE-2026-42945%20%E2%80%94%20NGINX%20Rift%20%28ngx_http_rewrite_module%20heap%20overflow%2C%20RCE-DoS%29.md) — почему важно обновляться.
- [IPTables](../../../Network/IPTables.md) — открыть 80/443/UDP-443 (QUIC) на фаерволе.

## 🔗 Ссылки

- Документация: [nginx.org/docs](https://nginx.org/en/docs/) · [Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html) · [полный список директив](https://nginx.org/en/docs/dirindex.html)
- Исходники/релизы: [github.com/nginx/nginx](https://github.com/nginx/nginx)
- TLS-настройки: [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/) · [SSL Labs](https://www.ssllabs.com/ssltest/)

#Network #WebServer #nginx #ReverseProxy #HTTP #TLS #Linux
