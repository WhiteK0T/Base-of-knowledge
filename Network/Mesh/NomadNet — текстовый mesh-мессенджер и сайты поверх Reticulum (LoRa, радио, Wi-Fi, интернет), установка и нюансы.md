---
создал заметку: 2026-10-14T10:00:00
author: WhiteK0T
tags:
  - Сеть
  - Mesh
  - Reticulum
  - LoRa
  - Приватность
  - Мессенджер
Источник:
  - https://t.me/open_source_friend/5838
  - https://github.com/markqvist/NomadNet
  - https://github.com/markqvist/Reticulum
  - https://github.com/markqvist/LXMF
  - https://reticulum.network/manual/
---

# 📡 NomadNet — текстовый mesh-мессенджер и «сайты» поверх Reticulum

**[Nomad Network](https://github.com/markqvist/NomadNet)** — консольная программа (TUI на `urwid`) для зашифрованной переписки, просмотра страниц и обмена файлами в сети **Reticulum**. Ей не нужны ни интернет, ни вообще IP-сеть: связь может идти по LoRa, пакетному радио, последовательной линии, Wi-Fi, Ethernet, интернету или всему сразу. Никаких регистраций и серверов: адрес — это хеш вашего криптографического ключа.

| | |
| :--- | :--- |
| Автор | Mark Qvist (он же автор Reticulum, LXMF, Sideband и RNode) |
| Язык / лицензия | Python 3.8+ · **GPL-3.0** |
| Версия | **1.4.4** (30.09.2026); Reticulum (`rns`) 1.5.7, LXMF 1.2.1 |
| Статус | **beta** — так пишет сам автор |
| Звёзды | NomadNet 2,6k · Reticulum 7,5k |

---

## 1. Из чего состоит

```
NomadNet / Sideband / MeshChatX     ← программы для людей
          LXMF                      ← протокол сообщений (как «почта»: доставка, хранение для офлайн-адресатов)
        Reticulum (rns)             ← сетевой стек: адресация, шифрование, маршрутизация
LoRa (RNode) · радио-TNC · serial · Wi-Fi · TCP/UDP · I2P   ← физические каналы, любые вперемешку
```

- **Reticulum** — сетевой стек вместо IP. Адрес узла — хеш открытого ключа, поэтому он не зависит от того, по какому каналу вы подключены. Весь трафик шифруется (X25519 + Ed25519, AES-256-CBC, прямая секретность; примитивы берутся из OpenSSL через `cryptography`). Работает даже на каналах **300 бит/с**.
- **LXMF** — протокол сообщений поверх Reticulum. Умеет хранить сообщения на промежуточных узлах (propagation nodes), пока адресат офлайн.
- **NomadNet** — клиент: переписка, встроенный текстовый браузер, свой узел со страницами и файлами, групповой чат RRC.

### Что умеет NomadNet

- зашифрованные сообщения с доставкой офлайн-адресатам через распределённое хранилище;
- **узлы со страницами**: что-то вроде маленьких сайтов на своём языке разметки **micron**. Страницы можно генерировать на стороне узла скриптами на Python, PHP, bash;
- обмен файлами через узлы;
- групповой чат в реальном времени (RRC);
- картинки в терминалах, которые умеют их показывать;
- режим демона без интерфейса — узел для хранения сообщений и раздачи страниц.

---

## 2. Важно знать заранее

> [!warning] GitHub — только зеркало, поддержки нет
> С конца декабря 2025 автор отошёл от публичной работы над проектом: репозиторий помечен как **публичное зеркало**, issue и обсуждения не обслуживаются, обновления выходят «когда выйдут». При этом релизы продолжаются — последние вышли 29–30 сентября 2026. Сам протокол Reticulum в общественном достоянии с 2016 года, код открыт — дальнейшее развитие автор оставил сообществу.

> [!warning] Ставьте только оригинал
> README предупреждает о **поддельных клонах** NomadNet и связанных программ, во многом сгенерированных LLM и нарушающих GPL. Ставьте из PyPI (`nomadnet`, `rns`, `lxmf`) или из репозиториев `markqvist`. Список признанных программ — в разделе [Programs Using Reticulum](https://reticulum.network/manual/software.html) руководства.

- **Лицензия Reticulum — не стандартная.** Это MIT с двумя дополнительными запретами: нельзя использовать в системах, способных намеренно причинять вред людям, и **нельзя использовать для обучения ИИ-моделей** и наборов данных для них. Поэтому GitHub и не распознаёт её. Сам NomadNet — обычная GPL-3.0.
- **Это не замена Telegram.** Интерфейс консольный, пользователей мало, скорость по LoRa — сотни байт в секунду. Сильная сторона — связь там, где нет интернета или ему не доверяют.
- **Право.** Шифрованный трафик в любительском радиодиапазоне во многих странах запрещён. LoRa в нелицензируемых диапазонах (в России — 868 МГц, с ограничениями мощности и доли времени передачи) — законна. Подробности — в правилах вашей страны.

---

## 3. Установка

Программы ставятся из PyPI; в репозиториях дистрибутивов их почти нет.

| Система | Как поставить |
| :--- | :--- |
| **Gentoo** | ebuild в основном дереве нет: `emerge --ask dev-python/pipx`, затем `pipx install nomadnet` (опционально `pipx install rns`, `pipx install lxmf` для утилит) |
| **Debian / Ubuntu** | пакетов нет: `sudo apt install pipx`, затем `pipx install nomadnet` |
| **Arch** | AUR: `yay -S nomadnet` (тянет `python-rns`, обе в версиях 1.4.4 и 1.5.5) или `pipx install nomadnet` |
| **Entware** | `opkg install python3 python3-pip python3-cryptography`, затем `pip install rns lxmf nomadnet`. Роутеру хватит ресурсов на **транспортный узел Reticulum** (`rnsd`) или узел хранения сообщений (`nomadnet --daemon`) |

`pipx` ставит программу в отдельное окружение и не конфликтует с системным Python (на Debian 12+ и Arch обычный `pip install` без venv запрещён). Альтернатива из README — `break-system-packages = true` в `~/.config/pip/pip.conf` — ломает защиту системных пакетов, лучше не надо.

### Первый запуск

```bash
nomadnet                 # TUI; при первом запуске откроется раздел Guide с инструкцией
nomadnet --daemon        # узел без интерфейса (хранение сообщений, страницы)
rnstatus                 # состояние интерфейсов Reticulum (из пакета rns)
```

Конфиг Reticulum создаётся в `~/.reticulum/config`, NomadNet — в `~/.nomadnetwork/`.

### Подключиться к сети через интернет

Без своего радио можно сразу подключиться к общей опорной сети через интернет. Узлы для подключения перечислены в разделе [Bootstrapping Connectivity](https://reticulum.network/manual/gettingstartedfast.html#bootstrapping-connectivity) руководства. В `~/.reticulum/config` добавляется интерфейс такого вида:

```ini
[[Опорный узел]]
  type = TCPClientInterface
  enabled = yes
  target_host = <адрес узла из руководства>
  target_port = <порт>
```

Дальше оставьте NomadNet работать: он начнёт получать анонсы узлов со страницами. Узел по известному адресу открывается через `Ctrl+U` в разделе **Network**.

### LoRa и радио

Для LoRa нужно устройство **RNode** — плата с LoRa-радио (например, LilyGO T-Beam, T3S3, Heltec) с прошивкой RNode. Прошивается утилитой `rnodeconf --autoinstall` из пакета `rns`. Затем в конфиг Reticulum добавляется интерфейс `RNodeInterface` с портом, частотой и мощностью. Пакетные радио-TNC подключаются через `KISSInterface`. Подробно — в разделе [Interfaces](https://reticulum.network/manual/interfaces.html) руководства.

### Автозапуск узла

```bash
# Gentoo (OpenRC): /etc/init.d/rnsd — простой вариант через supervise-daemon
command="/home/<пользователь>/.local/bin/rnsd"
command_user="<пользователь>"
supervisor="supervise-daemon"
```

На Debian и Arch — unit systemd с `ExecStart=%h/.local/bin/rnsd` (пользовательский: `systemctl --user enable --now rnsd`). На Entware — init-скрипт в `/opt/etc/init.d/`.

---

## 4. Другие клиенты

| Клиент | Платформы | Чем удобен |
| :--- | :--- | :--- |
| **[Sideband](https://github.com/markqvist/Sideband)** | Android, Linux, macOS, Windows | графический интерфейс, карта, голосовые; тот же протокол LXMF |
| **[MeshChatX](https://meshchatx.com/)** | десктоп, веб-интерфейс | мессенджер в браузере |
| **[Columba](https://github.com/torlando-tech/columba)** | Android | мобильный клиент |
| **[Ren Browser](https://github.com/Quad4-Software/Ren-Browser)** | десктоп | браузер страниц NomadNet |

Все они в одной сети: пользователь NomadNet пишет пользователю Sideband напрямую.

## 🔗 Ссылки

- NomadNet: https://github.com/markqvist/NomadNet
- Reticulum и руководство: https://github.com/markqvist/Reticulum · https://reticulum.network/manual/
- LXMF: https://github.com/markqvist/LXMF
- Исходный пост: https://t.me/open_source_friend/5838

#Сеть #Mesh #Reticulum #LoRa #Приватность #Мессенджер
