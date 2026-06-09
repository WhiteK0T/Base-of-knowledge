---
создал заметку: 2026-06-09T17:00:00
author: WhiteK0T
tags:
  - qBittorrent
  - Torrent
  - libtorrent
  - WebUI
  - Gentoo
  - Network
Источник:
  - https://www.qbittorrent.org/
  - https://github.com/qbittorrent/qBittorrent
  - https://packages.gentoo.org/packages/net-p2p/qbittorrent
---

# 🧲 qBittorrent — настройка и headless-сервер (WebUI)

[**qBittorrent**](https://www.qbittorrent.org/) — свободный (GPL) кроссплатформенный BitTorrent-клиент на **Qt** поверх библиотеки **libtorrent-rasterbar**. Главная альтернатива µTorrent: **без рекламы, без майнеров, открытый код**. Умеет встроенный поиск по трекерам, RSS-автозагрузку, веб-интерфейс (WebUI) и удалённое управление по HTTP API.

Актуальная ветка — **5.2.x** (на libtorrent-rasterbar **1.2** или **2.0**, Qt 6). В 5.2 появились: лимиты сидирования **на категорию**, сохранение трекеров из tracker-list между запусками, асинхронный подсчёт хэшей (UI не виснет при добавлении больших торрентов), сборки под ARM64.

> [!info] Связанные заметки
> Расшифровка колонки флагов пиров — [Флаги пиров qBittorrent](Torrent%20Flags.md). Автообновление раздач через этот же WebUI — [emonoda](emonoda%20%E2%80%94%20автообновление%20торрентов%20%28qBittorrent%2C%20Gentoo%29.md).

## 🖥️ GUI или nox (headless)

| Вариант | Что это | Когда |
| :--- | :--- | :--- |
| **qbittorrent** (GUI) | полноценное окно на Qt | десктоп |
| **qbittorrent-nox** | «no X» — без GUI, только демон + **WebUI** | сервер/NAS, удалённое управление |

Для домашнего сервера/качалки нужен именно **qbittorrent-nox**: запускается фоном, управляется из браузера по `http://<host>:8080`.

## 🛠️ Установка

### Gentoo

Пакет — `net-p2p/qbittorrent`. Ключевые USE-флаги:

| USE | По умолч. | Назначение |
| :--- | :---: | :--- |
| `gui` | ✓ | графический интерфейс (Qt). Для headless **выключить** |
| `webui` | — | собрать **qbittorrent-nox** + веб-интерфейс |
| `dbus` | ✓ | уведомления и power-management через D-Bus (на сервере не нужен) |

**Десктоп (GUI + WebUI):**

```bash
echo "net-p2p/qbittorrent gui webui" >> /etc/portage/package.use/qbittorrent
emerge -av net-p2p/qbittorrent
```

**Только headless-сервер (nox, без GUI):**

```bash
echo "net-p2p/qbittorrent -gui webui -dbus" >> /etc/portage/package.use/qbittorrent
emerge -av net-p2p/qbittorrent
```

Тянет за собой `net-libs/libtorrent-rasterbar` и Qt6.

### Debian / Ubuntu

```bash
sudo apt install qbittorrent        # GUI
sudo apt install qbittorrent-nox    # headless + WebUI
```

Свежие версии — из официального PPA `ppa:qbittorrent-team/qbittorrent-stable`.

### Arch

```bash
sudo pacman -S qbittorrent          # GUI (qt6)
sudo pacman -S qbittorrent-nox      # headless + WebUI
```

### Entware (роутеры/NAS)

> [!warning] На роутер qBittorrent практически не ставится
> qBittorrent — тяжёлый клиент (Qt + libtorrent-rasterbar). В **Entware** под ARM-архитектуры роутеров (`armv7`, `aarch64`) пакета `qbittorrent-nox` **нет** — нет и нужных зависимостей (Qt/libtorrent-rasterbar в репозитории не собраны, см. Entware issue #641). На роутере используют лёгкие клиенты:
> ```bash
> opkg update
> opkg install transmission-daemon-openssl transmission-web   # рекомендуемый, есть WebUI
> # или: rtorrent-rakshasa (+ ruTorrent), или aria2
> ```

> [!note] Конкретно про ASUS RT-AX56U
> AX56U — это **BCM6755 (armv7), 512 МБ RAM, 256 МБ flash**, и он уже **снят с поддержки в Asuswrt-Merlin**. Решающий фактор — **пакета `qbittorrent-nox` под `armv7` в Entware просто нет**. Реальные варианты на этом роутере:
> 1. **Entware → transmission-daemon** — лёгкий демон с WebUI.
> 2. Встроенный в прошивку ASUS **Download Master**.
> 3. **Не качать на роутере**, а держать **qBittorrent-nox на полноценной машине** (Gentoo/Debian/Arch-сервер), а роутер использовать только как сетевой узел/хранилище. Обычно это лучший вариант.

Официальные сборки и установщики для всех ОС — на [qbittorrent.org/download](https://www.qbittorrent.org/download).

## 🚀 Первый запуск headless

```bash
qbittorrent-nox
```

При первом старте в консоль печатается **временный случайный пароль** WebUI (в свежих версиях; в старых дефолт был `admin` / `adminadmin`):

```
The WebUI administrator username is: admin
The WebUI administrator password was not set. A temporary password is provided: <случайный>
```

Заходишь на `http://<host>:8080`, логин `admin` + этот пароль, и сразу меняешь его в *Настройки → Веб-интерфейс*.

> [!tip] Обход аутентификации в локалке
> *Настройки → Веб-интерфейс → «Обходить аутентификацию для клиентов на localhost»* — удобно, когда к WebUI ходят только локальные инструменты (например [emonoda](emonoda%20%E2%80%94%20автообновление%20торрентов%20%28qBittorrent%2C%20Gentoo%29.md)); тогда логин/пароль им не нужны.

## ⚙️ Запуск как служба

**OpenRC (Gentoo).** В пакете есть init-скрипт; запуск от отдельного пользователя:

```bash
rc-update add qbittorrent default
rc-service qbittorrent start
# конфиг сервиса (пользователь, опции) — /etc/conf.d/qbittorrent
```

**systemd** (если используется) — юзер-юнит `~/.config/systemd/user/qbittorrent.service`:

```ini
[Unit]
Description=qBittorrent-nox
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/qbittorrent-nox --webui-port=8080
Restart=on-failure

[Install]
WantedBy=default.target
```

```bash
systemctl --user enable --now qbittorrent
loginctl enable-linger $USER   # чтобы крутился без активной сессии
```

## 🔧 Ключевые настройки

### Сеть и подключения

- **Фиксированный порт.** *Соединение → Порт для входящих* — задать постоянный порт и **пробросить его** на роутере (или включить UPnP/NAT-PMP). Без открытого порта остаёшься «за NAT» (мало входящих пиров).
- **Шифрование протокола.** *BitTorrent → Режим шифрования* — `Разрешено` / `Принудительно`. Принудительное прячет торрент-трафик от примитивного DPI провайдера (но не от серьёзного анализа).
- **Anonymous mode** — убирает идентифицирующую информацию из объявлений трекеру.
- **µTP + TCP**, ограничение числа соединений, лимиты скорости (в т.ч. альтернативные «ночные» по расписанию).

### Категории и метки

- **Категории** (*Category*) — одна категория = свой **путь сохранения** (напр. категория `Movies` → `/mnt/dat1T/Movies`). Включи *«Сохранять торренты в подпапку по категории»* / задай путь категории — раскладка по диску происходит сама.
- **Метки** (*Tags*) — несколько произвольных ярлыков на торрент, ортогонально категории.

> [!note] qBittorrent и emonoda
> [emonoda](emonoda%20%E2%80%94%20автообновление%20торрентов%20%28qBittorrent%2C%20Gentoo%29.md) при обновлении торрента **не переносит категорию/метку** на новую версию (плагин qB не поддерживает «кастомы») — после апдейта категорию может понадобиться вернуть вручную.

### Сидирование и очередь

- **Лимиты сидирования:** по рейтингу (ratio) и/или времени — глобально, на торрент и (с 5.2) **на категорию**. По достижении — пауза или удаление.
- **Очередь:** ограничение числа одновременно активных закачек/раздач.
- **Последовательная загрузка** (*Sequential download*) и *«сначала первый и последний кусок»* — для предпросмотра медиа.

### Где лежат файлы

| Путь | Что |
| :--- | :--- |
| `~/.config/qBittorrent/qBittorrent.conf` | основной конфиг |
| `~/.config/qBittorrent/categories.json` | категории и их пути |
| `~/.local/share/qBittorrent/BT_backup/` | `*.fastresume` и `*.torrent` каждого торрента |
| `~/.local/share/qBittorrent/logs/` | логи |

`BT_backup` — это **внутреннее** хранилище клиента; для emonoda нужна **отдельная** папка-копия `.torrent` (см. опцию *«Сохранять копию .torrent в:»*).

## 🔎 Поиск и 📡 RSS

- **Встроенный поиск** (*View → Search*) работает через **плагины поиска** (Python-скрипты под конкретные трекеры) — нужен установленный Python.
- **RSS + авто-загрузчик** (*RSS → Download Rules*) — подписка на ленту трекера и правила (regex по названию, фильтр сезона/качества), новые серии скачиваются автоматически. Альтернатива emonoda там, где у трекера есть RSS.

## 🔌 Автоматизация

- **WebUI API** (`/api/v2/...`) — управление из скриптов/инструментов; на нём же работает emonoda.
- **«Выполнить программу при завершении»** (*Настройки → Загрузки → Run external program on completion*) — постобработка: распаковка, перемещение, уведомление. Подстановки: `%N` имя, `%F` путь к файлу, `%D` папка сохранения, `%L` категория и т.д.

## 🔐 Приватность

- **Привязка к интерфейсу** (*Соединение → Сетевой интерфейс*) — заставить qBittorrent ходить **только через VPN-интерфейс** (`tun0`/`wg0`); если VPN отпал — трафик не утечёт мимо (простой kill-switch).
- Шифрование протокола + anonymous mode (см. выше). Помни: трекеры и пиры всё равно видят твой IP — приватность даёт VPN, а не сам клиент.

## 🩺 Частое

- **0 пиров / «соединение: брандмауэр»** — закрыт/не проброшен входящий порт.
- **Забыл пароль WebUI** — остановить демон и удалить строки `WebUI\Password_*` из `qBittorrent.conf`; при следующем старте сгенерится временный.
- **Файлы качаются не туда** — проверь путь по умолчанию и пути категорий (категория переопределяет общий путь сохранения).

## 🔗 См. также

- [Флаги пиров qBittorrent](Torrent%20Flags.md)
- [emonoda — автообновление торрентов](emonoda%20%E2%80%94%20автообновление%20торрентов%20%28qBittorrent%2C%20Gentoo%29.md)
- Документация/вики: <https://github.com/qbittorrent/qBittorrent/wiki>

#qBittorrent #Torrent #libtorrent #WebUI #Gentoo #Network
