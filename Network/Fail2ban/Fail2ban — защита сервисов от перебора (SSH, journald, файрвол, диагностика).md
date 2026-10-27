---
создал заметку: 2026-10-28
author: WhiteK0T
tags:
  - Security
  - Linux
  - SSH
  - Hardening
  - Network
  - OpenSource
Источник:
  - https://github.com/fail2ban/fail2ban
  - https://github.com/fail2ban/fail2ban/blob/1.1.0/man/jail.conf.5
  - https://github.com/fail2ban/fail2ban/blob/1.1.0/config/jail.conf
  - https://github.com/fail2ban/fail2ban/blob/1.1.0/man/fail2ban-client.1
  - https://github.com/fail2ban/fail2ban/blob/1.1.0/config/filter.d/sshd.conf
  - https://github.com/fail2ban/fail2ban/blob/1.1.0/config/action.d/nftables.conf
  - https://packages.gentoo.org/packages/net-analyzer/fail2ban
  - https://packages.debian.org/trixie/fail2ban
  - https://archlinux.org/packages/extra/any/fail2ban/
  - https://bin.entware.net/armv7sf-k3.2/Packages
---

# Fail2ban — защита сервисов от перебора

[Fail2ban](https://github.com/fail2ban/fail2ban) — демон на Python, который находит заданные события в логах и выполняет действие при достижении порога. Типичный сценарий: несколько неудачных входов с одного IP → временная блокировка адреса в файрволе. Поддерживает OpenSSH, веб-серверы, почтовые службы и другие сервисы, для которых есть подходящий фильтр. Лицензия — GPL-2.0-or-later.

Основа заметки — присланный текст поста «Я настроил Fail2ban и забыл о брутфорсе» из CodeGuard: PySec Edition. Прямая ссылка на публикацию не предоставлена; настройки ниже сверены с upstream-документацией и пакетами на **28 октября 2026 года**.

## Как устроена блокировка

**Jail** связывает источник событий, фильтр и действие:

1. **Backend** читает файл или systemd journal.
2. **Filter** распознаёт сообщения и извлекает IP. У SSH это штатный `sshd`.
3. Fail2ban считает обнаруженные ошибки с каждого адреса за `findtime`.
4. При достижении `maxretry` запускает **action**: например, добавляет IP в набор nftables на `bantime`.

Параметры из поста задают следующий режим:

| Параметр | Значение | Смысл |
| :--- | :--- | :--- |
| `maxretry` | `3` | порог — три учитываемых фильтром события с одного IP |
| `findtime` | `600` / `10m` | скользящее окно последних десяти минут |
| `bantime` | `3600` / `1h` | блокировка на час |
| `port` | `ssh` | для действия с ограничением по портам — порт SSH из `/etc/services`, обычно TCP/22 |

Три события не обязательно равны трём подключениям: одно SSH-соединение допускает несколько попыток аутентификации, а набор учитываемых сообщений зависит от фильтра и его режима. Исходные сообщения не исчезают из журнала после бана.

Fail2ban уменьшает скорость перебора с повторяющихся адресов. Распределённый подбор с множества IP и редкие попытки ниже порога остаются возможны. Основная защита SSH — вход по ключам, ограничение доступа и обновления; смена порта лишь уменьшает часть фонового шума. Это ограничение прямо отмечено в [README проекта](https://github.com/fail2ban/fail2ban#fail2ban-ban-hosts-that-cause-multiple-authentication-errors).

## Установка

Ниже для обычного Linux-сервера выбран **nftables**. Если файрвол управляется через UFW/firewalld или используется iptables, согласовать `banaction` с этой схемой; поддерживаемые действия находятся в `action.d/`. Самостоятельно включать ещё один менеджер файрвола поверх существующего не требуется.

<details><summary>Gentoo / OpenRC</summary>

```bash
sudo emerge --ask net-analyzer/fail2ban net-firewall/nftables
```

Для OpenRC использовать файловый backend и работающий syslog-демон. USE-флаг `systemd` для этого сценария не нужен. Пакет и доступные USE-флаги: [Gentoo Packages](https://packages.gentoo.org/packages/net-analyzer/fail2ban).

</details>

<details><summary>Debian / Ubuntu / systemd</summary>

```bash
sudo apt update
sudo apt install fail2ban python3-systemd nftables
```

`python3-systemd` нужен для чтения journal. Явное указание пакета полезно и при установке без рекомендуемых зависимостей. Наличие `/var/log/auth.log` зависит от установки и настройки syslog: этот файл есть не на каждой системе.

</details>

<details><summary>Arch / systemd</summary>

```bash
sudo pacman -Syu fail2ban nftables
```

`python-systemd` входит в зависимости [официального пакета](https://archlinux.org/packages/extra/any/fail2ban/). Использовать backend `systemd`, если SSH пишет в journal.

</details>

Entware рассматривается отдельно ниже: там другие пути, init-скрипт и часто Dropbear вместо OpenSSH.

## Локальная настройка SSH

Не редактировать поставляемый `jail.conf`. Создать **небольшой** `/etc/fail2ban/jail.d/sshd.local`, содержащий только переопределения. Полная копия `jail.conf` в `jail.local` сохраняется при обновлении, но одновременно закрепляет старые значения всех скопированных настроек.

Порядок чтения: `jail.conf` → `jail.d/*.conf` → `jail.local` → `jail.d/*.local`; внутри каталогов — по алфавиту. Поэтому проверить и уже существующие локальные файлы: более поздний может изменить ту же настройку. См. [jail.conf(5)](https://github.com/fail2ban/fail2ban/blob/1.1.0/man/jail.conf.5).

Перед включением оставить текущую SSH-сессию открытой и иметь резервный доступ. В `ignoreip` при необходимости добавить **свой доверенный адрес или VPN-подсеть**, учитывая IPv4 и IPv6. Широкая общая подсеть за NAT исключит из защиты всех её пользователей.

Выбрать **один** из вариантов ниже и сохранить его в `sshd.local`.

<details><summary>Вариант A: Debian / Ubuntu / Arch — чтение systemd journal</summary>

```ini
[sshd]
enabled = true
backend = systemd
logpath =
port = 22
banaction = nftables[type=multiport]
ignoreip = 127.0.0.1/8 ::1
maxretry = 3
findtime = 10m
bantime = 1h
```

При `backend = systemd` источник выбирает `journalmatch` из фильтра `sshd`; файловый `logpath` не используется. Здесь он явно очищен. Настройка backend находится именно в `[sshd]`, чтобы не переключить файловые jails nginx или почты на journal.

Проверить наличие сообщений SSH:

```bash
sudo journalctl _COMM=sshd -n 30 --no-pager
sudo journalctl -u ssh.service -u sshd.service -n 30 --no-pager
```

Название unit и процесс, записывающий сообщения, зависят от дистрибутива и версии OpenSSH. Если ошибки видны в журнале, но не учитываются Fail2ban, проверить фактические поля journal и актуальность штатного фильтра. В частности, новые OpenSSH могут писать часть событий от `sshd-session`.

</details>

<details><summary>Вариант B: Gentoo / OpenRC или другая система с текстовым логом</summary>

```ini
[sshd]
enabled = true
backend = polling
logpath = /var/log/auth.log
port = 22
banaction = nftables[type=multiport]
ignoreip = 127.0.0.1/8 ::1
maxretry = 3
findtime = 10m
bantime = 1h
```

`/var/log/auth.log` — пример для syslog, настроенного писать аутентификацию в этот файл. На конкретной Gentoo это может быть `/var/log/auth.log`, `/var/log/secure` или `/var/log/messages`. Сначала найти файл с реальными ошибками SSH и подставить его путь. `polling` читает файл без Python-модуля inotify.

```bash
sudo tail -n 30 /var/log/auth.log
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
```

`fail2ban-regex` показывает, распознаёт ли фильтр сообщения; сам по себе этот тест не доказывает, что файрвол блокирует подключения.

</details>

При нестандартном порте заменить `22` на реальный порт **сервера**; Fail2ban не читает `sshd_config`, чтобы автоматически его определить. Если sshd слушает несколько портов, перечислить их через запятую. Это порты назначения, а не случайный исходящий порт клиента в сообщении лога.

Явный `filter = sshd` для стандартного jail обычно не нужен: он наследуется из поставляемой конфигурации. Начать со штатного режима фильтра; более агрессивный режим расширяет набор событий и требует проверки ложных срабатываний.

## Проверка конфигурации и запуск

Сначала выполнить проверку; переходить к запуску только при успешном результате:

<details><summary>Проверка без запуска демона</summary>

```bash
sudo fail2ban-client -t
sudo fail2ban-client -d
```

`-t` проверяет конфигурацию, `-d` выводит собранные команды с учётом переопределений. Они не подтверждают работоспособность блокировки в ядре.

</details>

<details><summary>Gentoo / OpenRC — автозапуск и запуск</summary>

```bash
sudo rc-update add fail2ban default
sudo rc-service fail2ban start
```

После изменения уже работающей конфигурации:

```bash
sudo fail2ban-client reload
```

</details>

<details><summary>Debian / Ubuntu / Arch — systemd</summary>

```bash
sudo systemctl enable --now fail2ban
sudo fail2ban-client reload
sudo systemctl status fail2ban --no-pager
```

`reload` применяет изменения и в случае, когда пакет уже запустил демон при установке. Если служба ранее завершилась с ошибкой, после исправления выполнить `sudo systemctl restart fail2ban`.

</details>

## Убедиться, что защита работает

<details><summary>Статус jail и фактические параметры</summary>

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
sudo fail2ban-client get sshd maxretry
sudo fail2ban-client get sshd findtime
sudo fail2ban-client get sshd bantime
sudo fail2ban-client get sshd ignoreip
sudo fail2ban-client get sshd actions
```

Для journal:

```bash
sudo fail2ban-client get sshd journalmatch
```

Для файлового backend:

```bash
sudo fail2ban-client get sshd logpath
```

В `status sshd` смотреть `Currently banned`, `Total banned`, список IP и источник событий (`File list` либо `Journal matches`). Нулевой счётчик бана сам по себе не является ошибкой.

</details>

<details><summary>Проверить действие на тестовом адресе и снять бан</summary>

```bash
sudo fail2ban-client set sshd banip 192.0.2.123
sudo fail2ban-client status sshd
sudo nft list ruleset
sudo fail2ban-client set sshd unbanip 192.0.2.123
```

`192.0.2.123` — адрес для документации, не адрес администратора. Тест проверяет создание бана и правил, но не чтение SSH-логов. Полный тест — несколько неудачных входов с отдельного контролируемого адреса, появление событий в jail и отказ **нового** подключения после бана. Не проводить его с единственного адреса управления.

Для действия iptables вместо nftables проверить `sudo iptables -S` и, при использовании IPv6, `sudo ip6tables -S`. Снятие бана своего адреса выполняется той же командой `unbanip` через резервный доступ.

</details>

Создание правил может происходить при первом бане. Если jail показывает бан, но трафик проходит, проверить ошибки action, правильность порта, семейство адресов и цепочку, через которую идут пакеты. Обычная защита SSH на самом сервере относится к входящему трафику; сервис за Docker/DNAT может потребовать правил в цепочке пересылки. Перезагрузка файрвола с очисткой правил также требует повторной проверки защиты Fail2ban.

## Частые причины отсутствия банов

| Наблюдение | Что проверить |
| :--- | :--- |
| `Have not found any log file` | файл существует и содержит события; если SSH пишет только в journal — выбрать `systemd` |
| backend `systemd` не загружается | установлен `python3-systemd` / `python-systemd`, права доступа к журналу |
| события SSH есть, `Total failed` не растёт | `journalmatch`, формат сообщений, фильтр и его режим, дата и часовой пояс лога |
| статус показывает бан, подключения проходят | action действительно выполнился; порт, IPv4/IPv6, цепочка, правила после перезапуска файрвола |
| заблокирован общий офисный адрес | все пользователи за NAT делят один IP; подобрать порог или узкое доверенное исключение |

Лог самого Fail2ban искать по `logtarget` в `/etc/fail2ban/fail2ban.conf` и локальных переопределениях. Это может быть `/var/log/fail2ban.log` или журнал systemd. `journalctl -u fail2ban` помогает разбирать запуск службы, но не обязательно содержит все события банов при записи в файл.

## Entware / ASUS: пакет есть, настройка зависит от прошивки

В [основном ARMv7 feed](https://bin.entware.net/armv7sf-k3.2/Packages) на дату проверки есть **`fail2ban` 1.1.0-2**. Содержимое `.ipk` подтверждает пути `/opt/etc/fail2ban/`, `/opt/bin/fail2ban-client` и init-скрипт **`/opt/etc/init.d/S95fail2ban`**. Скрипт поставляется с `ENABLED=yes`.

<details><summary>Установка и просмотр файлов Entware</summary>

```sh
opkg update
opkg install fail2ban
opkg files fail2ban
```

Локальные изменения разместить в `/opt/etc/fail2ban/jail.d/`. Проверить конфигурацию до запуска:

```sh
/opt/bin/fail2ban-client -t
/opt/etc/init.d/S95fail2ban start
/opt/bin/fail2ban-client status
```

Следующую команду выполнять только если проверка предыдущей завершилась успешно. При уже работающем демоне после изменения настроек использовать `/opt/bin/fail2ban-client reload`.

</details>

На роутере SSH может обслуживать **Dropbear** прошивки: тогда нужен jail/filter `dropbear`, а не `sshd`. Источник логов — файл, в который действительно пишет прошивка; возможный `/tmp/syslog.log` сначала проверить. В Entware использовать файловый backend, например `polling`. Пакет зависит от iptables, но наличие утилиты не гарантирует совместимость всех actions с ядром и правилами прошивки.

Для собственного jail указать реальный лог, порт и подходящий action, проверить сообщения через `/opt/bin/fail2ban-regex`, затем провести тест бана. Не переносить Linux-конфигурацию с `backend = systemd` на роутер. Штатный [фильтр Dropbear](https://github.com/fail2ban/fail2ban/blob/1.1.0/config/filter.d/dropbear.conf) распознаёт определённые форматы сообщений — совпадение с прошивкой нужно проверить отдельно. Доступ к SSH роутера из WAN предпочтительно закрыть и администрировать через LAN/VPN.

## Веб и почта

Для каждого сервиса включать отдельный jail с подходящим фильтром и реальным источником ошибок. Наличие HTTP 401/404 само по себе не означает перебор: правило должно соответствовать приложению. За reverse proxy/CDN важно корректно получать IP клиента из доверенной цепочки прокси; блокировка адреса прокси отключит доступ всем. Если клиентский IP отсутствует на сетевом уровне origin, бан его в локальном файрволе не остановит запросы через CDN — нужно действие на том уровне, где этот адрес виден.

Подбирать исключения, порог и длительность по реальным логам. Дополнительные настройки вроде `bantime.increment` имеет смысл вводить после проверки базового jail, чтобы ошибочное срабатывание не превращалось в длительную потерю доступа.

## Связанные заметки и источники

- [SSH — ключи](../SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md), [базовое руководство](../SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md), [продвинутое руководство](../SSH/SSH-%D0%9F%D1%80%D0%BE%D0%B4%D0%B2%D0%B8%D0%BD%D1%83%D1%82%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md).
- [IPTables](../IPTables.md).
- [Как защитить Linux-сервер — 10 шагов (конспект Просто DevOps)](../../Education/Youtube/%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%BE%20Devops/%D0%9A%D0%B0%D0%BA%20%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B8%D1%82%D1%8C%20Linux-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%E2%80%94%2010%20%D1%88%D0%B0%D0%B3%D0%BE%D0%B2%20%28%D0%BA%D0%BE%D0%BD%D1%81%D0%BF%D0%B5%D0%BA%D1%82%3A%20SSH%20%D0%BF%D0%BE%20%D0%BA%D0%BB%D1%8E%D1%87%D0%B0%D0%BC%2C%20%D1%84%D0%B0%D0%B9%D1%80%D0%B2%D0%BE%D0%BB%2C%20fail2ban%2C%20%D0%BB%D0%BE%D0%B3%D0%B8%20%D0%B2%20Loki%2C%20%D0%B0%D0%BB%D0%B5%D1%80%D1%82%D1%8B%2C%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B2%D0%B7%D0%BB%D0%BE%D0%BC%D0%B0%29.md).
- [Проект Fail2ban](https://github.com/fail2ban/fail2ban), [поставляемый jail.conf](https://github.com/fail2ban/fail2ban/blob/1.1.0/config/jail.conf), [jail.conf(5)](https://github.com/fail2ban/fail2ban/blob/1.1.0/man/jail.conf.5).
- [Команды fail2ban-client](https://github.com/fail2ban/fail2ban/blob/1.1.0/man/fail2ban-client.1), [фильтр sshd](https://github.com/fail2ban/fail2ban/blob/1.1.0/config/filter.d/sshd.conf), [action nftables](https://github.com/fail2ban/fail2ban/blob/1.1.0/config/action.d/nftables.conf).
- [Пакет Entware](https://bin.entware.net/armv7sf-k3.2/fail2ban_1.1.0-2_armv7-3.2.ipk) — источник проверенных путей и init-скрипта.

#Security #Linux #SSH #Hardening #Network #OpenSource
