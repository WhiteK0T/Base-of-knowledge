---
создал заметку: 2026-10-27T21:15:00
author: WhiteK0T
tags:
  - Tools
  - Codex
  - Генератор
  - Python
Источник:
  - https://learn.chatgpt.com/docs/developer-commands?surface=cli
---

# 🖼️ codex-cli-poster — генератор постера-шпаргалки Codex CLI

Скрипт [`poster.py`](poster.py) собирает постер **2560×1440** для заметки [Codex CLI — шпаргалка команд](../../AI/Agents/Codex%20CLI%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) и кладёт его в `Cache/Codex-CLI/codex-cli-cheatsheet-2560x1440.png`.

Движок и оформление взяты из [claude-code-poster](../claude-code-poster/README.md):
- цветные шапки блоков с иконками, светлые подложки;
- клавиши нарисованы «кнопками», подзаголовки — курсивом с линией;
- команды — моноширинным жирным;
- шрифты — Inter и JetBrains Mono.

Отличаются содержимое и бейдж: синий **EXP** отмечает экспериментальные функции и бету.

## Как устроен

1. Содержимое лежит в самом скрипте, в списке `BLOCKS`: блок = заголовок, иконка, цвет и разделы со строками. Строка — это команда и пояснение (третьим элементом можно указать `EXP` или `NEW`), или клавиши через `K("Ctrl", "C")`.
2. `COLUMNS` задаёт, какие блоки в какой из пяти колонок.
3. Скрипт собирает HTML и делает headless-скриншот Firefox (или Chromium). Затем через Pillow проверяет, не упёрлась ли какая-то колонка в низ, и сжимает PNG.
4. Шрифты скачиваются один раз в `~/.cache/bok-poster-fonts/` — общий кэш с claude-code-poster, в репозиторий они не попадают.

## Запуск

<details><summary>Команды</summary>

```bash
python3 Tools/codex-cli-poster/poster.py                 # PNG в Cache/, дата сверки — сегодня
python3 Tools/codex-cli-poster/poster.py --size 20       # кегль меньше, если не влезает (по умолчанию 21)
python3 Tools/codex-cli-poster/poster.py --date 27.10.2026 --html /tmp/poster.html   # с датой и промежуточным HTML
```

</details>

Скрипт печатает «низ колонок» в пикселях. Если какая-то колонка дошла почти до 1440, уменьшите `--size` или перенесите блок в другую колонку через `COLUMNS`.

## Зависимости по системам

| Система | Что поставить |
| :--- | :--- |
| **Gentoo** | `emerge --ask www-client/firefox dev-python/pillow` (или `www-client/firefox-bin`) |
| **Debian / Ubuntu** | `apt install firefox-esr python3-pil` (Ubuntu: `firefox` из snap или PPA Mozilla) |
| **Arch** | `pacman -S firefox python-pillow` |
| **Entware** | не подходит: нужен полноценный браузер для рендеринга |

Вместо Firefox подойдёт Chromium (`chromium`, `google-chrome`) — скрипт найдёт его сам. Pillow необязателен: без него постер соберётся, но без проверки высоты и сжатия. Для иконок в шапках нужен шрифт Noto Color Emoji.

## Когда пересобирать

После правок заметки-шпаргалки:
1. перенесите изменения в `BLOCKS`;
2. запустите скрипт и проверьте картинку;
3. обновите дату и версию Codex в описании постера в заметке. Версия ещё указана в подписи внизу постера — она задаётся в `build_html`.

#Tools #Codex #Генератор #Python
