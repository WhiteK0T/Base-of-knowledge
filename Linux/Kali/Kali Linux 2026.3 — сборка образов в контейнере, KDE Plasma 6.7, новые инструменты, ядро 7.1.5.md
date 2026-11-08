---
создал заметку: 2026-11-08T21:45:00
author: WhiteK0T
tags:
  - Kali
  - Linux
  - Pentest
  - Релиз
Источник:
  - https://t.me/Mr0x45xploit/656
  - https://telegra.ph/Vypusk-Kali-Linux-20263-10-29
  - https://www.kali.org/blog/kali-linux-2026-3-release/
  - https://gitlab.com/kalilinux/build-scripts
---

# 🐉 Kali Linux 2026.3 — коротко о выпуске

Третий выпуск Kali в 2026 году вышел 26 октября. Заметка по посту [Mr0x45xploit](https://t.me/Mr0x45xploit/656), который ссылается на пересказ в [Telegraph](https://telegra.ph/Vypusk-Kali-Linux-20263-10-29). Факты сверены с [официальным анонсом](https://www.kali.org/blog/kali-linux-2026-3-release/), подробности — там.

## Главное

| Что | Суть |
| :--- | :--- |
| Сборочные скрипты | [скрипты официальных образов](https://gitlab.com/kalilinux/build-scripts) приведены к общему виду; появился `build-in-container.sh` — сборка внутри Docker или Podman, без установки зависимостей на хост. Обновлены пока не все скрипты, остальные ждут к 2026.4 |
| Рабочий стол | KDE Plasma 6.7 (в том числе отдельные виртуальные столы на каждом мониторе) и новые иконки |
| Новые инструменты | `dalfox`, `katana`, `qsreplace`, `rustscan`, `sdrangel`, `snaffler-ng` |
| Ядро и пакеты | ядро 7.1.5 (было 6.19), 126 обновлённых пакетов |
| NetHunter | новые возможности для смарт-часов и NFC, поддержка KernelSU, новые ядра устройств |

## Новые инструменты

| Инструмент | Для чего |
| :--- | :--- |
| `dalfox` | поиск XSS |
| `katana` | обход и сбор URL сайта |
| `qsreplace` | подмена значений параметров в списке URL |
| `rustscan` | быстрый сканер портов |
| `sdrangel` | приёмник и анализатор для SDR |
| `snaffler-ng` | поиск паролей и чувствительных файлов в сетевых папках SMB |

**Уточнение к пересказу в Telegraph.** SMB в описании `snaffler-ng` — сетевой протокол общих папок Windows (Server Message Block), а не «малые и средние предприятия». Кроме того, пересказ не упоминает раздел о NetHunter.

## Как обновиться и собрать свой образ

```bash
sudo apt update && sudo apt full-upgrade -y     # обновить установленную Kali
grep VERSION /etc/os-release                     # проверить версию
```

Свой образ собирается скриптами из GitLab. Скрипты сами ставят зависимости через `apt`, поэтому вне Debian-семейства удобнее собирать в контейнере через `build-in-container.sh`:

| Система | Что поставить |
| :--- | :--- |
| Debian / Ubuntu / Kali | можно собирать прямо на хосте или поставить `podman` |
| Gentoo | `emerge --ask app-containers/podman` |
| Arch | `sudo pacman -S podman` |
| Entware | неприменимо |

Параметры сборки (ветка, архитектура, вариант образа, имя хоста, дополнительные пакеты) описаны в `./build.sh --help` и README каждого скрипта.

## Связанные заметки

- [Kali Linux на флешке с постоянным хранилищем](Kali%20Linux%20%D0%BD%D0%B0%20%D1%84%D0%BB%D0%B5%D1%88%D0%BA%D0%B5%20%D1%81%20%D0%BF%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%BD%D1%8B%D0%BC%20%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B5%D0%BC%20%28persistence%29%20%E2%80%94%20%D0%BF%D0%BE%D0%BB%D0%BD%D1%8B%D0%B9%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81.md) — как поставить Kali на USB

## 🔗 Ссылки

- Пост: https://t.me/Mr0x45xploit/656
- Пересказ в Telegraph: https://telegra.ph/Vypusk-Kali-Linux-20263-10-29
- Официальный анонс: https://www.kali.org/blog/kali-linux-2026-3-release/
- Сборочные скрипты: https://gitlab.com/kalilinux/build-scripts

#Kali #Linux #Pentest #Релиз
