---
создал заметку: 2026-11-08T11:35:00
author: WhiteK0T
tags:
  - yoinks
  - yt-dlp
  - Видео
  - CLI
  - TUI
  - Загрузчики
Источник:
  - https://github.com/pablostanley/yoinks
  - https://www.npmjs.com/package/yoinks
  - https://github.com/yt-dlp/yt-dlp#dependencies
  - https://github.com/yt-dlp/yt-dlp/wiki/EJS
---

# ⬇️ yoinks — качалка видео в терминале поверх yt-dlp

[**yoinks**](https://github.com/pablostanley/yoinks) — полноэкранное приложение в терминале для скачивания видео: вставил ссылку, выбрал разрешение или «только звук (mp3)» — файл в `~/Downloads`. Внутри работает [yt-dlp](yt-dlp.md), так что поддерживаются YouTube, X, Instagram, Threads, TikTok и ещё больше 1 800 сайтов. Интерфейс написан на [Ink](https://github.com/vadimdemedes/ink) — React для терминала: работает мышь, есть светлая и тёмная темы. Ни рекламы, ни поддельных кнопок «Скачать», как на веб-сервисах, нет — это обычная локальная программа.

| | |
| :--- | :--- |
| Лицензия, язык | MIT, TypeScript (~1 900 строк) |
| Пакет | npm `yoinks` 0.3.1 (17.07.2026), ~3,5 тыс. загрузок в месяц |
| Репозиторий | ~7 тыс. звёзд, создан 16.07.2026, 29 коммитов за два дня |
| Состояние | после 17 июля коммитов нет; около 20 PR с исправлениями без ответа, в [issue #41](https://github.com/pablostanley/yoinks/issues/41) предлагают взять сопровождение |
| Работает с | Node.js **22+**, ffmpeg, yt-dlp (скачивает сам) |

## 1. Как устроено

- **yt-dlp.** Если `yt-dlp` есть в `PATH`, yoinks берёт его. Если нет — при первом запуске скачивает самостоятельную сборку с GitHub (`releases/latest`) в `~/.yoinks/bin/`, Python не нужен.
- **ffmpeg** (склейка видео и звука высокого разрешения, извлечение mp3) — из `PATH`, а если его нет — встроенный из npm-пакета `ffmpeg-static`.
- **Выбор формата.** До 8 разрешений (`bv*[height=…]+ba` со склейкой в mp4) с примерным размером файла и `audio only · mp3` наилучшего качества.
- **Сохранение** — всегда в `~/Downloads`, имя — первые 60 символов названия ролика. Путь к файлу печатается после выхода.
- **Буфер обмена.** Запущенный без ссылки, yoinks читает буфер (`wl-paste`, `xclip` или `xsel`) и предлагает вставить оттуда адрес по Tab.
- **История** — последние 50 ссылок в `~/.config/yoinks/history.json`.

## 2. Что важно знать до установки

- **Нужен Node 22+, а не 18+, как написано в README.** Интерфейсная библиотека Ink 7 требует Node 22. На Node 18 программа падает сразу при запуске с `SyntaxError: Invalid regular expression flags` — разбор и исправление в [PR #37](https://github.com/pablostanley/yoinks/pull/37), не влит. Из коробки Node 22+ есть в Gentoo, Arch и Ubuntu 26.04. В Debian 13 стоит 20, в Ubuntu 24.04 — 18, в Entware — 18.
- **Скачанный yt-dlp не обновляется.** YouTube регулярно меняет выдачу, и старый yt-dlp перестаёт находить форматы: `Requested format is not available` в [issue #8](https://github.com/pablostanley/yoinks/issues/8) лечится обновлением. Если yt-dlp скачал сам yoinks — `~/.yoinks/bin/yt-dlp -U`. Лучше поставить yt-dlp из репозитория, тогда его обновляет менеджер пакетов (раздел 3).
- **Для YouTube нужен JavaScript-движок.** Свежему yt-dlp для полной поддержки YouTube нужны компоненты `yt-dlp-ejs` — в самостоятельную сборку они уже встроены — и движок JavaScript. По умолчанию включён только Deno; Node.js, который для yoinks и так стоит, включается ключом `--js-runtimes node`. yoinks вызывает yt-dlp с `--no-warnings`, поэтому предупреждение об отсутствии движка не видно — остаётся только ошибка про формат. Решение — конфиг yt-dlp (раздел 4).
- **Проверка «вы не бот».** На неё жалуются в [issue #26](https://github.com/pablostanley/yoinks/issues/26). У yoinks нет ключа для cookies браузера (PR закрыт), но yt-dlp читает свой конфиг, и `--cookies-from-browser` можно вписать туда.
- **Бинарник yt-dlp скачивается без проверки контрольной суммы,** хотя yt-dlp публикует подписанные `SHA2-256SUMS`. Ещё одна причина ставить yt-dlp из репозитория.
- **Архитектуры.** Для Linux yoinks выбирает только `yt-dlp_linux` (x86-64) или `yt-dlp_linux_aarch64`. На 32-битном ARM и на musl-системах (Alpine) скачанная сборка не запустится — нужен свой `yt-dlp` в `PATH`.
- **Пока нет:** плейлистов (`--no-playlist`), выбора папки `-o`, флагов для скриптов (`--best`, `--mp3`), самообновления. Всё это в планах README, часть уже есть в PR, но не влита.
- **Право.** Скачивание может нарушать правила площадки. README прямо говорит: инструмент для личного архива, скачивайте то, что вправе хранить.

## 3. Установка

| Система | Node 22+, ffmpeg, yt-dlp |
| :--- | :--- |
| Gentoo | `emerge --ask net-libs/nodejs media-video/ffmpeg net-misc/yt-dlp`; по желанию Deno — `dev-lang/deno-bin` |
| Arch | `sudo pacman -S nodejs npm ffmpeg yt-dlp deno` |
| Debian 13 | Node 22 — из репозитория NodeSource: `curl -fsSL https://deb.nodesource.com/setup_22.x \| sudo -E bash - && sudo apt install nodejs ffmpeg`; свежий yt-dlp — `sudo apt install -t trixie-backports yt-dlp` (в основном репозитории версия апреля 2025) |
| Ubuntu 24.04 | Node 22 — тоже NodeSource; yt-dlp в репозитории от 2024 года — пусть yoinks скачает свой или `pipx install yt-dlp` |
| Ubuntu 26.04 | `sudo apt install nodejs npm ffmpeg` (Node 22); yt-dlp из репозитория от марта 2026 — лучше `pipx install yt-dlp` |
| Entware | не подойдёт: Node 18, yt-dlp из ленты от февраля 2026 и 512 МБ памяти. На роутере проще звать `yt-dlp` напрямую |

```bash
npm install -g yoinks     # или без установки: npx yoinks
```

## 4. Использование

```bash
yoinks https://youtu.be/<id>   # сразу к выбору формата
yoinks                         # спросит ссылку; если она в буфере — Tab
yoinks --theme light           # auto | light | dark на этот запуск
```

Клавиши: `↑`/`↓`, `j`/`k` или цифры — выбор, `Enter` — скачать, `Esc` — назад, `Ctrl+T` — тема, `Ctrl+C` — выход. Кнопки, список форматов и подсказки кликаются мышью.

Конфиг yt-dlp, который подхватит и yoinks, — `~/.config/yt-dlp/config`:

```text
# Node.js как JavaScript-движок для YouTube (Deno, если он стоит, включён и так)
--js-runtimes node
# при проверке «вы не бот»: cookies из браузера, где вы вошли в YouTube
# --cookies-from-browser firefox
```

Конфиг действует на все запуски yt-dlp, не только из yoinks.

## 5. То же без yoinks

yoinks — удобная обёртка над двумя командами yt-dlp. Без интерфейса они выглядят так:

```bash
# видео до 1080p, склейка в mp4, как у yoinks
yt-dlp -f 'bv*[height<=1080]+ba/b' --merge-output-format mp4 -o "$HOME/Downloads/%(title).60s.%(ext)s" <ссылка>
# только звук в mp3 наилучшего качества
yt-dlp -f 'ba/b' -x --audio-format mp3 --audio-quality 0 -o "$HOME/Downloads/%(title).60s.%(ext)s" <ссылка>
```

Плейлисты, своя папка, субтитры и обложки — это уже ключи самого yt-dlp, которых у yoinks пока нет.

## Связанные заметки

- [yt-dlp — движок загрузки видео](yt-dlp.md) — всё, что умеет движок под капотом
- [Загрузчики видео — какой выбрать](%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%D0%BE%D0%B9%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C.md) — сравнение оболочек над yt-dlp
- [Open Video Downloader](Open%20Video%20Downloader.md) — то же «вставил ссылку → скачал», но в окне и с пакетной загрузкой
- [Tartube](Tartube.md) — если нужны подписки на каналы, а не разовые ролики

## 🔗 Ссылки

- Репозиторий: https://github.com/pablostanley/yoinks
- npm: https://www.npmjs.com/package/yoinks
- PR #37 (минимум Node 22): https://github.com/pablostanley/yoinks/pull/37
- Зависимости yt-dlp: https://github.com/yt-dlp/yt-dlp#dependencies
- yt-dlp и JavaScript-движки (EJS): https://github.com/yt-dlp/yt-dlp/wiki/EJS

#yoinks #yt-dlp #Видео #CLI #TUI #Загрузчики
