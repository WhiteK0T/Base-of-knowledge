---
создал заметку: 2026-11-09T12:20:00
author: WhiteK0T
tags:
  - Безопасность
  - Honeypot
  - Мониторинг
  - ICS
Источник:
  - https://github.com/mushorg/conpot
  - https://conpot.readthedocs.io/
---

# 🍯 Conpot — приманка для промышленных сетей (ICS/SCADA)

[**Conpot**](https://github.com/mushorg/conpot) — приманка, которая прикидывается **промышленным контроллером** (ПЛК/RTU) и собирает данные о том, кто и как атакует индустриальные сети. Это редкая ниша: обычные honeypot'ы ловят интернет-ботов, а Conpot заточен под протоколы АСУ ТП, по которым ходят целевые атаки на производство и энергетику.

| | |
| :--- | :--- |
| Что это | low-interaction ICS/SCADA honeypot |
| Язык/лицензия | Python, GPLv2; ~1,5 тыс. звёзд, активен |
| Версия | v1.0.0 (сентябрь 2026), требует Python ≥ 3.14 |
| Автор | проект mushorg (The Honeynet Project) |

## Что эмулирует

Промышленные и сопутствующие протоколы: **Modbus**, **S7comm** (Siemens S7), **BACnet** (здания), **EtherNet/IP**, **IPMI**, **Kamstrup** (счётчики), а также HTTP, SNMP, TFTP, FTP для «обвязки». Поведение задаётся **шаблонами** устройств (`--template`), так что приманку можно выдать за конкретную модель ПЛК. Это делает её правдоподобной для сканеров вроде Shodan и целевых инструментов.

## Установка по платформам

Зависимости из git-версии управляются через `uv`.

| Система | Как ставить |
| :--- | :--- |
| Debian / Ubuntu | `sudo apt install gcc python3-dev` → поставить `uv` → `uv sync --group dev` → `uv run conpot --template default -f` |
| Gentoo | Python из Portage + `uv`; дальше те же шаги |
| Arch | `sudo pacman -S python gcc` + `uv`, затем аналогично |
| Entware | неприменимо — нужен Python 3.14, которого в репозитории роутера нет |

Есть и быстрый вариант через Docker; Conpot также входит в [T-Pot](T-Pot%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%D0%B7%2020%2B%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BE%D0%BA%20%D0%B2%20Docker%20%D1%81%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D0%B0%D0%BC%D0%B8%20Elastic%20%28Deutsche%20Telekom%29.md).

## Чтобы не подставиться

- Ставить в изоляции: это приманка, её будут атаковать.
- Нельзя подключать к **настоящей** технологической сети — приманка должна лишь имитировать устройство, а не быть мостом к реальному оборудованию.
- Шаблон выбирать под легенду, но без реальных параметров вашего производства.

## Связанные заметки

- [Honeypot — приманки: обзор и как выбрать](Honeypot%20%E2%80%94%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B8%3A%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C%20%28Cowrie%2C%20T-Pot%2C%20Dionaea%2C%20Conpot%2C%20OpenCanary%2C%20Canarytokens%2C%20Beelzebub%29.md) — Conpot как нишевый ICS-вариант
- [T-Pot — платформа приманок](T-Pot%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%D0%B7%2020%2B%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BE%D0%BA%20%D0%B2%20Docker%20%D1%81%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D0%B0%D0%BC%D0%B8%20Elastic%20%28Deutsche%20Telekom%29.md) — включает Conpot

## 🔗 Ссылки

- GitHub: https://github.com/mushorg/conpot
- Документация: https://conpot.readthedocs.io/

#Безопасность #Honeypot #Мониторинг #ICS
