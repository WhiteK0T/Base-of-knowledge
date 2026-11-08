---
создал заметку: 2026-11-09T12:05:00
author: WhiteK0T
tags:
  - Безопасность
  - Honeypot
  - Мониторинг
  - Python
Источник:
  - https://github.com/thinkst/opencanary
  - http://opencanary.org
---

# 🍯 OpenCanary — лёгкие приманки-ловушки

[**OpenCanary**](https://github.com/thinkst/opencanary) — многопротокольная приманка-демон с крайне низким расходом ресурсов (идёт даже на Raspberry Pi). Главный сценарий — **раннее обнаружение внутри своей сети**: вы ставите её в сегмент, где легитимного трафика к ней быть не должно, и любое срабатывание означает, что кто-то уже проник и сканирует/подбирает. Это open-source-версия коммерческого продукта Thinkst Canary.

| | |
| :--- | :--- |
| Что это | low-interaction приманка-tripwire, демон на Python |
| Лицензия | BSD-3-Clause; ~3,1 тыс. звёзд, активен |
| Версия | v0.9.10 (сентябрь 2026), Python 3.10+ |
| Автор | Thinkst Applied Research |

## Как работает

Демон поднимает несколько ложных сетевых сервисов (SSH, HTTP, FTP, RDP, MySQL/MSSQL, SMB/Windows-шара, VNC, SNMP, Telnet, git и др.). Как только кто-то к ним обращается или пытается войти — OpenCanary **шлёт оповещение** (email, syslog, вебхук, в т. ч. в мессенджер). Никакой эмуляции оболочки: задача не «записать команды», а мгновенно сообщить о самом факте контакта. Отсюда почти нулевой риск — поверхность атаки минимальна.

## Установка по платформам

Ядро — кроссплатформенный Python-пакет; больше всего модулей на Linux.

| Система | Установка |
| :--- | :--- |
| Debian / Ubuntu | `sudo apt install python3-venv python3-dev libssl-dev libpcap-dev` → `python3 -m venv env && . env/bin/activate && pip install opencanary` |
| Gentoo | интерпретатор из Portage (`dev-lang/python`), дальше тот же `venv` + `pip install opencanary` |
| Arch | `sudo pacman -S python libpcap` → `venv` + `pip install opencanary` |
| Entware | Python на роутере есть (`opkg install python3`), базовые модули поднимутся, но scapy (для SNMP) и Samba-модуль тяжёлые — брать только лёгкие сервисы |

Опционально: `pip install scapy pcapy-ng` для SNMP, пакет `samba` — для модуля Windows-шары, `iptables` (не nftables) — для модуля детекта портскана (только Linux).

```bash
opencanaryd --copyconfig          # создать ~/.opencanary.conf
# включить нужные сервисы в конфиге, затем:
opencanaryd --start
```

Есть и Docker-образ (`docker compose`), если удобнее в контейнере.

## Чтобы не подставиться

- Смысл именно во внутреннем размещении: сработало — значит, незваный гость уже в сети.
- Оповещения заводить на канал, который вы реально читаете, иначе ловушка бесполезна.
- Риск низкий, но сам хост всё равно держать без лишних секретов.

## Связанные заметки

- [Honeypot — приманки: обзор и как выбрать](Honeypot%20%E2%80%94%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B8%3A%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C%20%28Cowrie%2C%20T-Pot%2C%20Dionaea%2C%20Conpot%2C%20OpenCanary%2C%20Canarytokens%2C%20Beelzebub%29.md) — когда брать tripwire, а когда полноценную приманку
- [Canarytokens — токены-ловушки](Canarytokens%20%E2%80%94%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D1%8B-%D0%BB%D0%BE%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20%28%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%2C%20URL%2C%20AWS-%D0%BA%D0%BB%D1%8E%D1%87%29%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%28Thinkst%29.md) — тот же принцип «любой контакт подозрителен», но без сервиса

## 🔗 Ссылки

- GitHub: https://github.com/thinkst/opencanary
- Сайт: http://opencanary.org

#Безопасность #Honeypot #Мониторинг #Python
