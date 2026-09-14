---
создал заметку: 2026-09-14T21:30:00
author: WhiteK0T
tags:
  - RustDesk
  - RemoteAccess
  - SelfHosted
  - Rust
  - OpenSource
  - Инструменты
Источник:
  - https://selectel.ru/blog/tutorials/rustdesk/
  - https://github.com/rustdesk/rustdesk
  - https://github.com/rustdesk/rustdesk-server
---

# 🖥️ RustDesk — self-hosted удалённый доступ (клиент + свой сервер)

**RustDesk** ([github.com/rustdesk/rustdesk](https://github.com/rustdesk/rustdesk), ~123k★; сервер [rustdesk-server](https://github.com/rustdesk/rustdesk-server), ~10k★; всё на **Rust**, лицензия **AGPL-3.0**) — открытая альтернатива **TeamViewer/AnyDesk** с ключевым отличием: **можно поднять полностью свой сервер** и не зависеть от чужих облаков. Клиент — Windows/macOS/Linux/Android/iOS. Соединение по возможности **P2P** (минимальная задержка), а когда прямой коннект невозможен (NAT/файрвол) — трафик идёт через **твой relay**.

> [!info] Зачем свой сервер
> Публичный сервер RustDesk перегружен и медленный, а трафик идёт через чужую инфраструктуру. Свой сервер = **контроль, скорость, приватность, работа в изолированных сетях** (например, только внутри своей LAN/VPN без выхода в интернет).

## 🧩 Архитектура серверной части

Сервер — это **два лёгких демона** (Go/Rust-бинарники, минимум ресурсов):

| Компонент | Что делает | Порты |
| :--- | :--- | :--- |
| **hbbs** (ID/Rendezvous Server) | регистрация клиентов, выдача ID, свод P2P (hole punching) | **21114/tcp** (веб-API в PRO), **21115/tcp**, **21116/tcp+udp** (главный — ID/rendezvous), **21118/tcp** (веб-клиент) |
| **hbbr** (Relay Server) | ретрансляция трафика, когда P2P не вышел | **21117/tcp** (relay), **21119/tcp** (веб-клиент) |

Практически: открой на файрволе **`21114:21119/tcp` и `21116/udp`**. Требования смешные: **1 CPU / 1 ГБ ОЗУ / ~10 ГБ** диска.

> [!tip] Ключи шифрования (Ed25519) — сердце безопасности
> Сервер использует асимметричные ключи **Ed25519**:
> - **`id_ed25519`** — приватный (для hbbr);
> - **`id_ed25519.pub`** — публичный (раздаётся клиентам и в hbbs).
>
> Сгенерировать: `rustdesk-utils genkeypair`. Клиент, знающий **публичный ключ**, гарантированно общается именно с твоим сервером (защита от MITM/подмены). При первом старте hbbs/hbbr ключи создаются автоматически в рабочей папке (`./data` в docker-варианте).

## 📦 Установка сервера — Docker Compose (проще всего)

```yaml
# docker-compose.yml
services:
  hbbs:
    container_name: hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs
    volumes:
      - ./data:/root
    network_mode: "host"        # нужен host-режим: RustDesk активно юзает UDP/hole punching
    depends_on:
      - hbbr
    restart: unless-stopped
  hbbr:
    container_name: hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    volumes:
      - ./data:/root
    network_mode: "host"
    restart: unless-stopped
```
```bash
docker compose up -d
cat ./data/id_ed25519.pub    # публичный ключ → в клиент
```
(про механику Docker см. [Внутри ядра Docker](../../Linux/Containers/%D0%92%D0%BD%D1%83%D1%82%D1%80%D0%B8%20%D1%8F%D0%B4%D1%80%D0%B0%20Docker%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%B8%D1%82%20%D0%BF%D1%80%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B5%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%B0%20%28namespaces%2C%20cgroups%2C%20OverlayFS%2C%20runc%29.md))

## 🖥️ Установка сервера на системах владельца

Готовые бинарники есть под **amd64 / arm64v8 / armv7 / i386** — то есть покрывают и десктоп, и роутер.

### Debian / Ubuntu (systemd) — как в статье

```bash
wget https://github.com/rustdesk/rustdesk-server/releases/latest/download/rustdesk-server-linux-amd64.zip
unzip rustdesk-server-linux-amd64.zip -d rustdesk && cd rustdesk/amd64
./rustdesk-utils genkeypair
```
`/etc/systemd/system/hbbs.service`:
```ini
[Unit]
Description=RustDesk HBBS (ID/Rendezvous Server)
After=network.target
[Service]
Type=simple
ExecStart=/rustdesk/amd64/hbbs -k /rustdesk/amd64/id_ed25519.pub
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
```
`/etc/systemd/system/hbbr.service` — то же, но `ExecStart=/rustdesk/amd64/hbbr -k /rustdesk/amd64/id_ed25519`. Затем:
```bash
systemctl daemon-reload
systemctl enable --now hbbs.service hbbr.service
```
Есть и `.deb`-пакеты (`rustdesk-server-hbbs_*_amd64.deb`, `..._arm64`, `..._armhf`) — ставят и юниты сразу.

### Gentoo (основная) — OpenRC, не systemd!

Статья даёт systemd-юниты, но на Gentoo нужен **OpenRC**. Бинарники бери те же (или `emerge`-и из GURU-оверлея, если есть `net-misc/rustdesk-server`). Скрипт `/etc/init.d/hbbs`:
```sh
#!/sbin/openrc-run
name="RustDesk hbbs"
command="/opt/rustdesk/hbbs"
command_args="-k /opt/rustdesk/id_ed25519.pub"
command_background="yes"
pidfile="/run/hbbs.pid"
directory="/opt/rustdesk"
output_log="/var/log/hbbs.log"
error_log="/var/log/hbbs.log"
depend() { need net; }
```
Аналогично `/etc/init.d/hbbr` (`command=/opt/rustdesk/hbbr`, `command_args="-k /opt/rustdesk/id_ed25519"`, `pidfile=/run/hbbr.pid`). Затем:
```bash
chmod +x /etc/init.d/hbbs /etc/init.d/hbbr
rc-update add hbbs default && rc-update add hbbr default
rc-service hbbs start && rc-service hbbr start
```

### Arch — systemd

Сервер: AUR `rustdesk-server-bin` (кладёт бинарники и юниты) либо Docker; клиент — AUR `rustdesk-bin` (готовый) или `rustdesk` (сборка). Юниты как в Debian-блоке, включаются через `systemctl enable --now`.

### Entware / ASUS RT-AX56U (armv7) — свой мини-сервер на роутере

Изюминка: **hbbs/hbbr лёгкие и есть под armv7** → можно держать **личный ID/relay прямо на роутере** (он и так 24/7):
```bash
# на роутере с Entware (armv7)
cd /opt/tmp
wget https://github.com/rustdesk/rustdesk-server/releases/latest/download/rustdesk-server-linux-armv7.zip
unzip rustdesk-server-linux-armv7.zip -d /opt/rustdesk
/opt/rustdesk/armv7/rustdesk-utils genkeypair
```
Entware-init `/opt/etc/init.d/S99hbbs`:
```sh
#!/bin/sh
ENABLED=yes
PROCS=hbbs
ARGS="-k /opt/rustdesk/armv7/id_ed25519.pub"
PREARGS=""
DESC=$PROCS
PATH=/opt/rustdesk/armv7:/opt/bin:/opt/sbin:$PATH
. /opt/etc/init.d/rc.func
```
(и `S99hbbr` с `PROCS=hbbr`, `ARGS="-k .../id_ed25519"`). Дать `chmod +x`, запустить `/opt/etc/init.d/S99hbbs start`.
> [!warning] Нюансы роутера
> - **512 МБ ОЗУ** у RT-AX56U — hbbs/hbbr влезают (они лёгкие), но не вешай туда ещё десяток сервисов.
> - **Relay ест трафик/канал**: статика 30–100 Кбит/с, динамика в HD — **до 3 Мбит/с** на сессию. Через домашний аплинк это ок для 1–2 сессий, не для десятков.
> - Нужен **проброс портов** снаружи (`21114:21119/tcp`, `21116/udp`) и белый/статический IP или DDNS.

## 🔨 Сборка из исходников (если бинарников мало / хочешь свежак)

- **Сервер (rustdesk-server, Rust):** просто и переносимо — `git clone … && cargo build --release`, на выходе `target/release/{hbbs,hbbr,rustdesk-utils}`. Отлично собирается на Gentoo/Arch (нужен `rust`/`cargo`). Так закроешь любую арку, где нет готового бинаря.
- **Клиент (rustdesk, Rust + Flutter/Sciter):** **тяжёлая** сборка — тянет `vcpkg`-зависимости (libvpx, libyuv, opus, aom), Flutter/Sciter, системные dev-библиотеки. На Gentoo реальнее взять **Flatpak/AppImage** или ebuild из **GURU-оверлея** (`net-misc/rustdesk`), чем собирать вручную. На Arch — `rustdesk-bin` из AUR.

## ⚙️ Подключение клиента к своему серверу

**Настройки → Сеть (ID/Relay):**
1. **Сервер ID (ID Server):** IP или домен hbbs.
2. **Ретранслятор (Relay Server):** IP hbbr.
3. **Ключ (Key):** вставить содержимое `id_ed25519.pub`.
4. Сохранить, перезапустить клиент — он получит **постоянный ID** на твоём сервере.

## 🔒 Безопасность и доступ

- **Постоянный пароль** — неконтролируемый доступ (удобно для своих машин; храни надёжно).
- **Подтверждение подключения** — удалённый юзер должен разрешить сессию (для техподдержки чужих).
- **Права сессии:** клавиатура/мышь, передача файлов, буфер обмена — выдаются точечно.
- Трафик шифруется; **публичный ключ** сервера защищает от подмены. AGPL-3.0: правишь/распространяешь — открывай исходники.

## 🔗 Связанные заметки

- Соседний инструмент удалённого доступа (проприетарный, для сравнения): [ScreenConnect](ScreenConnect.md)
- Когда P2P/relay недоступен, а нужен доступ через SSH-проброс: [SSH — визуальное руководство по туннелям](../../Network/SSH/SSH-%D0%92%D0%B8%D0%B7%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE%20%D0%BF%D0%BE%20%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8F%D0%BC.md)
- Механика Docker для контейнерного варианта: [Внутри ядра Docker](../../Linux/Containers/%D0%92%D0%BD%D1%83%D1%82%D1%80%D0%B8%20%D1%8F%D0%B4%D1%80%D0%B0%20Docker%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%B8%D1%82%20%D0%BF%D1%80%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B5%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%B0%20%28namespaces%2C%20cgroups%2C%20OverlayFS%2C%20runc%29.md)

## 🔗 Ссылки

- Клиент: [github.com/rustdesk/rustdesk](https://github.com/rustdesk/rustdesk) · Сервер: [github.com/rustdesk/rustdesk-server](https://github.com/rustdesk/rustdesk-server) (AGPL-3.0)
- Релизы сервера (amd64/arm64v8/armv7/i386): [rustdesk-server/releases](https://github.com/rustdesk/rustdesk-server/releases) · доки: [rustdesk.com/docs](https://rustdesk.com/docs/)
- Гайд-источник: [selectel.ru — RustDesk](https://selectel.ru/blog/tutorials/rustdesk/)

#RustDesk #RemoteAccess #SelfHosted #Rust #OpenSource #Инструменты
