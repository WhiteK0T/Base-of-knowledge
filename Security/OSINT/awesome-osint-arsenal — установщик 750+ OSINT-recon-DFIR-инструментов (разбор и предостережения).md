---
создал заметку: 2026-06-21T14:00:00
author: WhiteK0T
tags:
  - OSINT
  - Security
  - Recon
  - Pentest
  - Установщик
  - Kali
Источник:
  - https://github.com/rawfilejson/awesome-osint-arsenal
  - https://t.me/open_source_friend/5698
---

# 🕵️ awesome-osint-arsenal — установщик 750+ OSINT/recon/DFIR-инструментов (разбор и предостережения)

[**awesome-osint-arsenal**](https://github.com/rawfilejson/awesome-osint-arsenal) — это **не «awesome»-список ссылок**, а **bash-установщик**: одной командой ставит большую пачку инструментов для **OSINT, разведки (recon), пентеста (red team), мониторинга (blue team), форензики (DFIR) и хардвар-хакинга**. Ориентирован на **Kali / apt-дистрибутивы**. Язык — Shell (100%), ~1.3k★ (растёт; код не менялся с мая 2026). Установка модульная — отдельные скрипты под каждую область.

> [!danger] Только для авторизованных задач — это инструмент двойного назначения
> Сам автор в README пишет: *«This repository is for educational and authorized security research only. Always obtain written permission before testing systems you do not own.»* Здесь собраны в том числе **наступательные** инструменты (C2 Sliver, BloodHound, Nuclei). Применять их к чужим системам **без письменного разрешения владельца — преступление**.
> - **РФ:** ст. 272 УК (неправомерный доступ), 273 (вредоносное ПО), 138 (тайна переписки) — реальные сроки.
> - Легальные сценарии: **свои** стенды/лаборатории, CTF, пентест-энгейджмент с договором и scope, обучение в изолированной ВМ.

> [!warning] Факты против поста (сверено с README)
> - В Telegram сказано «**100+** инструментов» — в README заявлено **751+ инструментов в 50 категориях** (число «100+» занижено / устарело).
> - Название содержит «awesome-», но это **не курируемый список ссылок**, а **скрипты-инсталляторы** (`install.sh`, `osint.sh`, `redteam.sh`, …). Не путать с форматом awesome-list.
> - «Установка одной командой» — правда, но это **`sudo bash`-скрипт от третьего лица**, который массово ставит пакеты, репозитории, pip/go-модули. Это серьёзное вмешательство в систему — см. предупреждение ниже.

> [!caution] Supply-chain: `sudo bash install.sh` — доверяй, но проверяй
> Запуск `sudo bash` из чужого репозитория = **полный root-доступ скрипта к твоей машине**. Перед запуском:
> 1. **Прочитай скрипты** (`install.sh` и модули) и `tools.json` — что именно ставится и откуда.
> 2. Ставь **в одноразовую ВМ/контейнер** (или прямо в Kali-ВМ), не на рабочую/основную систему.
> 3. Закрепи коммит (`git checkout <sha>`), не гоняй «вслепую» свежий `main`.
> 4. Поставит десятки сторонних репо/бинарей — это расширяет твою поверхность атаки и замусоривает систему.

## 📦 Что ставит (модульные скрипты)

| Скрипт | Область | Примеры инструментов |
| :--- | :--- | :--- |
| `osint.sh` | OSINT / recon | Sherlock, Maigret, Amass |
| `redteam.sh` | наступательная ИБ | Sliver (C2), BloodHound, Nuclei, Mimikatz |
| `blueteam.sh` | защита / мониторинг | Wazuh, Sigma, Suricata, Velociraptor |
| `forensics.sh` | DFIR / форензика / RE | Volatility, Ghidra, radare2 |
| `hardware.sh` | RF / SDR / IoT | binwalk, hackrf, openocd |
| `labs.sh` | тренировочные стенды | DVWA, Juice Shop |
| `termux.sh` | Android-подмножество | без `sudo` |
| `install.sh` | всё сразу | вызывает модули |

Категории покрытия: SOCMINT (соцсети), GEOINT (геоданные), сетевой recon, dark web, утечки/breaches, форензика, hardware-hacking, тренировочные платформы.

## 🚀 Установка (для своего стенда / Kali-ВМ)

```bash
# полный набор
git clone https://github.com/rawfilejson/awesome-osint-arsenal
cd awesome-osint-arsenal
sudo bash install.sh

# или только нужный модуль (рекомендуется — меньше мусора)
sudo bash osint.sh        # только OSINT-инструменты
bash termux.sh            # Android/Termux, без sudo
```

> [!info] Поддержка платформ (из README)
> - ✅ **Лучше всего:** Kali, **Debian/Ubuntu**, Parrot, Mint, Pop!_OS (apt-based) — основной путь.
> - 🟡 **Частично:** **Arch/Manjaro**, Fedora/RHEL — автоопределение пакетного менеджера, иначе откат на `git`/`pip`/`go`.
> - 📱 **Mobile:** Termux на Android.
> - Open-source инструменты сохраняют свои лицензии; единой лицензии у репозитория по сути нет (см. атрибуцию авторов).

| Система владельца | Применимость |
| :--- | :--- |
| **Gentoo** (основная) | официально **не поддержан** (скрипты заточены под apt; на Arch/прочих — fallback на git/pip/go). На Gentoo разумнее ставить нужные инструменты **точечно из Portage**, а не гонять чужой инсталлятор |
| **Debian / Ubuntu** | поддержан напрямую — но лучше в **отдельной ВМ**, а не на основной системе |
| **Arch** (план с июня 2026) | частично (автодетект + fallback); ставь в ВМ |
| **Entware / RT-AX56U** | **N/A** — десктоп/Kali-инструментарий; на роутер не ставится |

## 💡 Кому и зачем

- Быстро поднять **учебный/пентест-стенд** в Kali-ВМ, не собирая полсотни инструментов вручную.
- Студентам ИБ/участникам **CTF** — единая точка для recon/OSINT/форензики на изолированной машине.
- **Не** для «попробовать на ком-нибудь»: без авторизации и scope это противозаконно и небезопасно (для тебя же).

## 🔗 Ссылки

- Репозиторий: [github.com/rawfilejson/awesome-osint-arsenal](https://github.com/rawfilejson/awesome-osint-arsenal)
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5698)
- Связанные: [Web Check — OSINT-досье на сайт](Web%20Check%20%E2%80%94%20OSINT-%D0%B4%D0%BE%D1%81%D1%8C%D0%B5%20%D0%BD%D0%B0%20%D1%81%D0%B0%D0%B9%D1%82%20%28DNS-SSL-%D0%B7%D0%B0%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BA%D0%B8-%D1%81%D1%82%D0%B5%D0%BA-%D0%BF%D0%BE%D1%80%D1%82%D1%8B%29.md) · [Storm-Breaker — фишинг вебки/микрофона/геолокации (разбор и защита)](../Social-Engineering/Storm-Breaker%20%E2%80%94%20%D1%84%D0%B8%D1%88%D0%B8%D0%BD%D0%B3%20%D0%B2%D0%B5%D0%B1%D0%BA%D0%B8-%D0%BC%D0%B8%D0%BA%D1%80%D0%BE%D1%84%D0%BE%D0%BD%D0%B0-%D0%B3%D0%B5%D0%BE%D0%BB%D0%BE%D0%BA%D0%B0%D1%86%D0%B8%D0%B8%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0%29.md)

#OSINT #Security #Recon #Pentest #Установщик #Kali
