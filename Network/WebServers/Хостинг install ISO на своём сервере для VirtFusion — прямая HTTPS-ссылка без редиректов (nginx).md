---
создал заметку: 2026-07-05T23:11:00
author: WhiteK0T
tags:
  - Network
  - WebServer
  - nginx
  - HTTPS
  - VirtFusion
  - VPS
  - ISO
Источник:
  - https://virtfusion.com/
---

# 📀 Хостинг install ISO на своём сервере для VirtFusion

Задача: отдать ISO по **прямой HTTPS-ссылке**, которая
- начинается с валидного HTTPS-сертификата,
- оканчивается на `.iso`,
- отдаёт файл сразу (HTTP 200), **без редиректов** (никаких 301/302).

В панель VirtFusion URL вставляется **без** префикса `https://`, например:
`files.example.com/iso/install-amd64-mod.iso`

> [!info] Зачем это надо
> VirtFusion при монтировании кастомного ISO **скачивает образ по URL** в момент старта VPS. Он требует именно **прямую** HTTPS-ссылку на `.iso` без промежуточных редиректов — поэтому весь фокус в том, чтобы сервер отдал файл строго `200 OK`.

---

## 0. Предпосылки

- Есть сервер (можно домашний Xeon), доступный из интернета.
- Есть доменное имя, A-запись которого указывает на публичный IP сервера,
  напр. `files.example.com`. (Домашний провайдер не должен блокировать
  входящие 80/443; при CGNAT/сером IP — не сработает, нужен проброс/белый IP.)
- Открыты порты **80** (для выпуска сертификата по HTTP-01) и **443**.
- Установлен nginx.

**Gentoo:**
```bash
emerge -av www-servers/nginx app-crypt/acme-sh   # или app-crypt/certbot
```
**Debian/Ubuntu:**
```bash
apt install nginx certbot python3-certbot-nginx
```
**Arch (план с июня 2026):**
```bash
pacman -S nginx certbot certbot-nginx
```
**Entware / RT-AX56U:** роутер как постоянный веб-хост под это ставить не стоит
(мало flash/RAM, порт 80/443 часто занят админкой). Если очень нужно временно
раздать файл — есть лёгкий `opkg install nginx` + `acme.sh` через **DNS-01**,
но проще поднять раздачу на десктопе/VPS.

> [!tip] Firewall — не забудь открыть порты
> На хосте с фаерволом пропусти входящие 80/443 (nftables/iptables на Linux либо
> панель провайдера). Порт **80 нужен даже если сайт только по HTTPS** — по нему
> проходит ACME-челлендж выпуска/продления сертификата.

---

## 1. Положить ISO в webroot

```bash
mkdir -p /var/www/iso
cp /путь/к/install-amd64-mod.iso /var/www/iso/
chmod 644 /var/www/iso/install-amd64-mod.iso
```

> [!note] Проверь контрольную сумму образа
> Перед раздачей убедись, что ISO не бился при копировании — иначе установка в
> VPS упадёт на середине:
> ```bash
> sha256sum /var/www/iso/install-amd64-mod.iso   # сверь с эталоном источника
> ```

---

## 2. Минимальный конфиг nginx (без редиректов на сам .iso)

`/etc/nginx/conf.d/iso.conf` (или в `sites-available` на Debian):

```nginx
# HTTP: нужен только для ACME-челленджа и (опц.) редиректа на HTTPS.
# ВАЖНО: на путь /iso/*.iso редирект НЕ вешаем — VirtFusion берёт HTTPS-URL
# напрямую, а редирект с HTTP тут просто не задействуется.
server {
    listen 80;
    server_name files.example.com;

    # путь для выпуска/обновления сертификата
    location /.well-known/acme-challenge/ {
        root /var/www/iso;
    }
    # всё остальное можно увести на HTTPS (на .iso это не влияет —
    # его VirtFusion запрашивает по https:// напрямую)
    location / { return 301 https://$host$request_uri; }
}

server {
    listen 443 ssl;
    http2 on;
    server_name files.example.com;

    ssl_certificate     /etc/letsencrypt/live/files.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/files.example.com/privkey.pem;

    root /var/www/iso;

    # отдаём .iso напрямую, 200, без единого редиректа
    location = /install-amd64-mod.iso {
        default_type application/octet-stream;
        add_header Content-Disposition "attachment; filename=install-amd64-mod.iso";
        try_files /install-amd64-mod.iso =404;
    }
}
```

Проверить конфиг и перезагрузить:
```bash
nginx -t && systemctl reload nginx    # или: rc-service nginx reload
```

---

## 3. Сертификат Let's Encrypt

> [!tip] Подробно про выпуск и связку сертификата — в отдельной заметке
> Здесь — только быстрый минимум под эту задачу. Полное руководство (методы
> проверки HTTP-01/DNS-01, wildcard, автопродление, связка с **nginx и Apache**,
> контекст РФ) — в заметке [Let's Encrypt — выпуск TLS-сертификата и связка с nginx и Apache](Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md).

Вариант A — certbot (проще всего с плагином nginx):
```bash
certbot --nginx -d files.example.com
```

Вариант B — acme.sh (webroot-режим, без правки конфига плагином):
```bash
acme.sh --issue -d files.example.com -w /var/www/iso
acme.sh --install-cert -d files.example.com \
  --key-file       /etc/letsencrypt/live/files.example.com/privkey.pem \
  --fullchain-file /etc/letsencrypt/live/files.example.com/fullchain.pem \
  --reloadcmd      "nginx -s reload"
```

После выпуска — снова `nginx -t && reload`, если конфиг менялся вручную.

---

## 4. Проверка ПЕРЕД вставкой в панель

```bash
curl -sI https://files.example.com/iso/install-amd64-mod.iso | head
```

Должно быть:
- строка `HTTP/2 200` (или `HTTP/1.1 200 OK`);
- **нет** заголовка `location:` (иначе это редирект — VirtFusion отвергнет);
- `content-type: application/octet-stream` и `content-length` = размер ISO.

> [!tip] Проверь и весь маршрут редиректов
> `curl -sIL` пройдёт по всем перенаправлениям и покажет цепочку — убедись, что
> на нужном URL **нет ни одного** промежуточного 301/302:
> ```bash
> curl -sIL https://files.example.com/install-amd64-mod.iso | grep -Ei 'HTTP/|location'
> ```

Если путь другой (файл лежит не в `/iso/`), подгони URL под свой `root`.
В конфиге выше файл лежит в `/var/www/iso/`, а `root` = `/var/www/iso`, значит
URL — `files.example.com/install-amd64-mod.iso` (без `/iso/`). Проверь именно
ту ссылку, которую будешь вставлять.

---

## 5. Вставка в VirtFusion

В поле URL (без `https://`):
```
files.example.com/install-amd64-mod.iso
```
Затем: смонтировать ISO → boot order на CD → загрузить VNC-консоль →
установка идёт сама → `halt` → в панели отмонтировать ISO → boot на диск.

Сервер с ISO должен быть **доступен в момент загрузки** VPS (VirtFusion
скачивает образ по URL при старте). После установки его можно погасить.

---

## Частые грабли
- **Редирект на .iso** (напр. общий `return 301` на весь `server`, или
  Cloudflare «Always Use HTTPS»/страничные редиректы) → 302/301 → отказ.
  Отдавай сам файл строго 200.
- **Cloudflare-прокси** перед сервером: сертификат будет валиден, но убедись,
  что SSL mode = Full и на путь .iso нет page-rule с редиректом; большие файлы
  free-план не всегда любит — при проблемах отключи проксирование (серое
  облако) для этого поддомена.
- **Только HTTP** (нет сертификата) → провайдер требует HTTPS → откажет.
- **Файл не кончается на .iso** в URL → откажет.
- **Сервер погашен во время старта VPS** → VirtFusion не скачает образ.
  Держи раздачу поднятой до конца установки.

---

## 🔗 Ссылки

- Связанные заметки: [Let's Encrypt — выпуск TLS-сертификата и связка с nginx и Apache](Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md)

#Network #WebServer #nginx #HTTPS #VirtFusion #VPS #ISO
