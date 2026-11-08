---
создал заметку: 2026-06-08T21:30:00
author: WhiteK0T
tags:
  - yt-dlp
  - Видео
  - CLI
  - Загрузчики
Источник:
  - https://github.com/yt-dlp/yt-dlp
---

# ⬇️ yt-dlp — движок загрузки видео (CLI)

[**yt-dlp**](https://github.com/yt-dlp/yt-dlp) (лицензия **Unlicense**, Python) — поддерживаемый форк youtube-dl и фактический **стандарт** для скачивания видео из 1000+ сайтов. Это **движок**, поверх которого работает большинство GUI-качалок (VidBee, Open Video Downloader, ytDownloader, Tartube, Seal). Быстро обновляется и обходит блокировки YouTube — поэтому надёжнее веб-сервисов.

## 📦 Установка

```bash
# через pip
python3 -m pip install -U yt-dlp

# Homebrew (macOS/Linux)
brew install yt-dlp

# или просто скачать бинарник с GitHub Releases и положить в PATH
```

YouTube то и дело меняет выдачу, поэтому yt-dlp нужен свежий: старые версии перестают находить форматы. Версии в репозиториях на ноябрь 2026:

| Система | Команда | Версия |
| :--- | :--- | :--- |
| Gentoo | `emerge --ask net-misc/yt-dlp` | 2026.10.26 |
| Arch | `sudo pacman -S yt-dlp` | 2026.10.26 |
| Debian 13 | `sudo apt install -t trixie-backports yt-dlp` | 2026.10.26 (в основном репозитории — 2025.04.30) |
| Ubuntu | `pipx install yt-dlp` | в 24.04 — 2024.04.09, в 26.04 — 2026.03.17 |
| Entware | `opkg install yt-dlp` | 2026.2.4 — для YouTube может не хватить |

Самостоятельная сборка с GitHub обновляет себя сама: `yt-dlp -U`.

> [!note] FFmpeg
> Для склейки видео+аудио и перекодирования нужен **FFmpeg** в `PATH`. Без него многие форматы (особенно >1080p на YouTube) не соберутся.

## ⚡ Базовые команды

```bash
yt-dlp <URL>                              # скачать в лучшем доступном качестве
yt-dlp -f "bv*+ba/b" <URL>                # лучшее видео+аудио (явно)
yt-dlp -F <URL>                           # показать доступные форматы
yt-dlp -f 137+140 <URL>                   # выбрать конкретные форматы по id
yt-dlp -x --audio-format mp3 <URL>        # извлечь только аудио в mp3
yt-dlp -o "%(title)s.%(ext)s" <URL>       # шаблон имени файла
yt-dlp --download-archive done.txt <URL>  # не качать повторно (архив скачанного)
yt-dlp <URL_плейлиста>                     # плейлист целиком
```

| Флаг | Назначение |
| :--- | :--- |
| `-f` / `-F` | выбор формата / список форматов |
| `-x --audio-format` | извлечь аудио |
| `-o` | шаблон имени (output template) |
| `--write-subs --sub-langs ru,en` | субтитры |
| `-N 4` | многопоточная загрузка фрагментов |
| `--cookies-from-browser firefox` | приватные/возрастные видео через куки браузера |

## 🧩 YouTube: JavaScript-движок и конфиг

Для полной поддержки YouTube yt-dlp решает его JavaScript-задачи внешним движком ([EJS](https://github.com/yt-dlp/yt-dlp/wiki/EJS)). Нужны две вещи:
- **компоненты `yt-dlp-ejs`.** В самостоятельные сборки с GitHub они уже встроены; при установке через pip — `pip install -U "yt-dlp[default]"`;
- **JavaScript-движок:** Deno (рекомендуют, включён по умолчанию), Node.js, Bun или QuickJS. Кроме Deno, движки нужно включить явно: `--js-runtimes node`.

Без движка часть форматов YouTube недоступна, и yt-dlp пишет об этом предупреждение. Обёртки, которые запускают его с `--no-warnings`, это предупреждение скрывают — остаётся только `Requested format is not available`.

Постоянные ключи удобно держать в конфиге `~/.config/yt-dlp/config`. Его читают и обёртки, если они не передают `--ignore-config`:

```text
--js-runtimes node
# --cookies-from-browser firefox
```

> [!warning] Правовой момент
> Качай только тот контент, на который имеешь право; учитывай ToS площадок и авторские права.

Какую обёртку выбрать поверх движка — см. [Загрузчики видео — какой выбрать](%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%D0%BE%D0%B9%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C.md).

#yt-dlp #Видео #CLI #Загрузчики
