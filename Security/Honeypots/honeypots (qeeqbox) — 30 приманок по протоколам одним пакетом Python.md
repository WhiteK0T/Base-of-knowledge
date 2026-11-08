---
создал заметку: 2026-11-09T12:35:00
author: WhiteK0T
tags:
  - Безопасность
  - Honeypot
  - Мониторинг
  - Python
Источник:
  - https://github.com/qeeqbox/honeypots
---

# 🍯 honeypots (qeeqbox) — 30 приманок одним пакетом

[**qeeqbox/honeypots**](https://github.com/qeeqbox/honeypots) — один PyPI-пакет, внутри которого **30 приманок по разным протоколам**. Удобен, когда нужно быстро «накидать» сенсоров сразу на кучу портов: приманка поднимается за 1–2 секунды, работает неблокирующе, её можно звать из CLI или использовать как объект в своём Python-коде.

| | |
| :--- | :--- |
| Что это | набор из 30 приманок в одном пакете |
| Язык/лицензия | Python, AGPL-3.0; ~1 тыс. звёзд, активен |
| Вывод | Postgres, файл(ы), терминал, Syslog |
| Применение | входит в [T-Pot](T-Pot%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%D0%B7%2020%2B%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BE%D0%BA%20%D0%B2%20Docker%20%D1%81%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D0%B0%D0%BC%D0%B8%20Elastic%20%28Deutsche%20Telekom%29.md) |

## Что умеет

Протоколы: dhcp, dns, elastic, ftp, http(s), http(s)-proxy, imap, ipp, irc, ldap, memcache, mssql, mysql, ntp, oracle, pjl, pop3, postgres, rdp, redis, sip, smb, smtp, snmp, socks5, ssh, telnet, vnc. Опция `capture_commands` в `--options` собирает больше данных о действиях атакующего (поддержка зависит от конкретной приманки). Можно поднимать несколько экземпляров одного типа.

```bash
pip3 install honeypots
honeypots --setup ssh,http,https     # поднять сразу несколько
honeypots --list                     # список всех доступных
```

## Установка по платформам

| Система | Как ставить |
| :--- | :--- |
| Debian / Ubuntu / Gentoo / Arch | `pip3 install honeypots` в виртуальном окружении (Python из штатного менеджера) |
| Entware | частично реально: пакет на чистом Python (`opkg install python3`), но 30 сервисов разом роутеру тяжело — поднимать 1–2 нужных (`--setup ssh`), а не всё |

## Чтобы не подставиться

- Чем больше портов открыли — тем больше поверхность; на слабом хосте брать только нужные приманки.
- Вывод по возможности сразу в БД/Syslog, чтобы данные не терялись.
- Как и любую приманку — держать в изолированном сегменте без реальных секретов.

## Связанные заметки

- [Honeypot — приманки: обзор и как выбрать](Honeypot%20%E2%80%94%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B8%3A%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C%20%28Cowrie%2C%20T-Pot%2C%20Dionaea%2C%20Conpot%2C%20OpenCanary%2C%20Canarytokens%2C%20Beelzebub%29.md) — когда удобен «комбайн» на много протоколов
- [T-Pot — платформа приманок](T-Pot%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%D0%B7%2020%2B%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BE%D0%BA%20%D0%B2%20Docker%20%D1%81%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D0%B0%D0%BC%D0%B8%20Elastic%20%28Deutsche%20Telekom%29.md) — использует этот пакет

## 🔗 Ссылки

- GitHub: https://github.com/qeeqbox/honeypots

#Безопасность #Honeypot #Мониторинг #Python
