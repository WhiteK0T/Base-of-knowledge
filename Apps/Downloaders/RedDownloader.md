---
создал заметку: 2026-07-02T13:00:00
author: WhiteK0T
tags:
  - RedDownloader
  - Reddit
  - Python
  - Загрузчики
  - Библиотека
Источник:
  - https://t.me/open_source_friend/5739
  - https://github.com/Jackhammer9/RedDownloader
---

# 🐍⬇️ RedDownloader — скачивание медиа с Reddit из Python

[**RedDownloader**](https://github.com/Jackhammer9/RedDownloader) (*Jackhammer9*, **Python**, лицензия **GPL-3.0**, ~**157★**, живой — v4.4.1 от декабря 2025) — **Python-библиотека** для скачивания медиа из постов **Reddit** по URL: картинки, видео, GIF, **галереи**, аудио (извлечение MP3), а также одиночные ссылки **YouTube/Imgur**. Тип медиа определяется автоматически; можно задать имя файла, путь и **качество видео** (144–1080p). **Ключевое:** это **библиотека**, а не готовое приложение с кнопкой — работаешь из Python-кода.

> [!info] Как выглядит использование
> ```bash
> pip install RedDownloader
> ```
> ```python
> from RedDownloader import RedDownloader
> RedDownloader.Download("https://www.reddit.com/r/.../comments/.../", quality=720)
> ```
> **Авторизация не нужна:** библиотека тянет медиа напрямую с `i.redd.it` / `v.redd.it`, без PRAW-бота и ключей Reddit API.

## 🧪 Факты против хайпа

> [!note] Это не «программа», а библиотека — и ниша у неё узкая
> Пост подал RedDownloader как готовый «инструмент/программу». На деле это **зависимость для твоих Python-скриптов/ботов** (в темах репо так и указано: `library`, `reddit-bot`). Для **разовой** загрузки одного поста проще и мощнее универсальный **yt-dlp** — он тоже умеет Reddit (`v.redd.it`, галереи) и ещё 1000+ сайтов. **Бери RedDownloader, когда** встраиваешь скачивание Reddit **в свой Python-пайплайн/бот**; для «скачать вот это видео руками» — [yt-dlp](yt-dlp.md).

> [!caution] Без API-ключа = зависимость от «сырых» URL Reddit
> Подход «без авторизации» удобен, но хрупок: Reddit периодически **ужесточает доступ** и **режет rate-limit** для неаутентифицированных запросов. Массовая/частая выкачка может **упираться в 429/блокировки**; для стабильных объёмов официальный путь — Reddit API с ключом (это уже не про эту либу). Не долби чужой сервер в цикле без пауз.

> [!tip] Для видео с v.redd.it держи ffmpeg
> Видео, размещённые на Reddit (`v.redd.it`), хранят **видео и аудио раздельными потоками** (DASH). Чтобы на выходе было видео **со звуком**, в системе обычно нужен **ffmpeg** — поставь его заранее, иначе рискуешь получить немой ролик или ошибку склейки.

> [!note] Право и этика — по-простому
> Reddit-контент создают пользователи. Личное сохранение — обычно ок, но **републикация** чужого материала может нарушать авторские права, а автоматизированный сбор — **условия Reddit/его API**. Качай для себя, уважай источники и лицензии.

## 💻 Как это ложится на твои системы

Чистый Python без нативных GUI-зависимостей → ставится где угодно, где есть Python 3 и `pip`. Для видео со звуком — плюс **ffmpeg**.

| Система | Установка |
| :--- | :--- |
| **Gentoo** (основная) | `emerge dev-lang/python media-video/ffmpeg`; из-за PEP 668 ставь либу в **venv** или через `pipx`: `python -m venv venv && ./venv/bin/pip install RedDownloader` |
| **Debian / Ubuntu** | `sudo apt install python3-venv pipx ffmpeg`, затем `pipx install RedDownloader` или venv |
| **Arch** | `sudo pacman -S python python-pipx ffmpeg`, затем `pipx install RedDownloader` |
| **Entware / RT-AX56U** | ✅ Реально: `opkg install python3 python3-pip ffmpeg`, затем `pip3 install RedDownloader`. Можно поднять **headless-архиватор Reddit** прямо на роутере с сохранением на **USB-диск**. Учти **512 МБ RAM** — большие 1080p-видео качай по одному, не пакетами |

## 💡 Кому полезно

- **Пишущим Python-ботов/скриптов**, которым нужно программно тянуть медиа Reddit (архиваторы, дайджесты, пайплайны).
- **Не** тем, кому надо «разово скачать видео» — там быстрее [yt-dlp](yt-dlp.md) (см. подборку [Загрузчики видео — какой выбрать](%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%D0%BE%D0%B9%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C.md)).
- Интересный сценарий для владельца: лёгкий **автосейв нужных сабреддитов на USB роутера** (Entware).

## 🔗 Ссылки

- Репозиторий: [github.com/Jackhammer9/RedDownloader](https://github.com/Jackhammer9/RedDownloader) (GPL-3.0) · PyPI: `pip install RedDownloader`
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5739)
- Связанные: [yt-dlp](yt-dlp.md) · [Загрузчики видео — какой выбрать](%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%D0%BE%D0%B9%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C.md)

#RedDownloader #Reddit #Python #Загрузчики #Библиотека
