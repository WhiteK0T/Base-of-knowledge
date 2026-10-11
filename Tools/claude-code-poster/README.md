---
создал заметку: 2026-10-12T02:00:00
author: WhiteK0T
tags:
  - Tools
  - Claude_Code
  - Генератор
  - Python
Источник:
  - https://t.me/bugnotfeature/27215
---

# 🖼️ claude-code-poster — генератор постера-шпаргалки Claude Code

Скрипт [`poster.py`](poster.py) собирает постер **2560×1440** для заметки [Claude Code — шпаргалка команд](../../AI/Agents/Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) и кладёт его в `Cache/Claude-Code/claude-code-cheatsheet-2560x1440.png`.

Оформление повторяет исходную шпаргалку из [поста «Не баг, а фича»](https://t.me/bugnotfeature/27215): цвета шапок и подложек сняты с оригинала по пикселям, клавиши нарисованы «кнопками», подзаголовки курсивом с линией, команды моноширинным жирным, новые пункты помечены красным бейджем **NEW**. Шрифты — Inter и JetBrains Mono.

## Как устроен

1. Содержимое лежит в самом скрипте, в списке `BLOCKS`: блок = заголовок, иконка, цвет и разделы со строками. Строка — это команда и пояснение (третьим элементом можно указать `NEW`), или клавиши через `K("Ctrl", "C")`.
2. `COLUMNS` задаёт, какие блоки в какой из пяти колонок.
3. Скрипт собирает HTML, делает headless-скриншот Firefox (или Chromium), затем через Pillow проверяет, не упёрлась ли какая-то колонка в низ, и сжимает PNG.
4. Шрифты скачиваются один раз в `~/.cache/bok-poster-fonts/` — в репозиторий они не попадают.

## Запуск

```bash
python3 Tools/claude-code-poster/poster.py                 # PNG в Cache/, дата сверки — сегодня
python3 Tools/claude-code-poster/poster.py --size 19       # кегль меньше, если не влезает
python3 Tools/claude-code-poster/poster.py --date 12.10.2026 --html /tmp/poster.html   # с датой и промежуточным HTML
```

Скрипт печатает «низ колонок» в пикселях. Если какая-то колонка дошла почти до 1440 — уменьшите `--size` или перенесите блок в другую колонку через `COLUMNS`.

## Зависимости по системам

| Система | Что поставить |
| :--- | :--- |
| **Gentoo** | `emerge --ask www-client/firefox dev-python/pillow` (или `www-client/firefox-bin`) |
| **Debian / Ubuntu** | `apt install firefox-esr python3-pil` (Ubuntu: `firefox` из snap или PPA Mozilla) |
| **Arch** | `pacman -S firefox python-pillow` |
| **Entware** | не подходит: нужен полноценный браузер для рендеринга |

Вместо Firefox подойдёт Chromium (`chromium`, `google-chrome`) — скрипт найдёт его сам. Pillow необязателен: без него постер соберётся, но без проверки высоты и сжатия.

## Когда пересобирать

После правок заметки-шпаргалки: перенесите изменения в `BLOCKS`, запустите скрипт, проверьте картинку и обновите дату в описании постера в заметке.

#Tools #Claude_Code #Генератор #Python
