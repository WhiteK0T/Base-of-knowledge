---
создал заметку: 2026-06-16T15:00:00
author: WhiteK0T
tags:
  - Terminal
  - kitty
  - OpenGL
  - Linux
Источник:
  - https://sw.kovidgoyal.net/kitty/
  - https://github.com/kovidgoyal/kitty
---

# 🐱 kitty — GPU-терминал с kittens и графикой (OpenGL)

**kitty** ([sw.kovidgoyal.net/kitty](https://sw.kovidgoyal.net/kitty/), [github.com/kovidgoyal/kitty](https://github.com/kovidgoyal/kitty)) — быстрый, **функционально богатый** GPU-терминал на **OpenGL** от Kovid Goyal (автор Calibre). Написан на Python + C + Go, лицензия **GPL-3.0**. В отличие от минималистичного [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md), kitty — это «комбайн»: вкладки, сплиты (layouts), **собственный протокол вывода картинок**, расширения-**kittens** и удалённое управление из коробки.

> [!info] «kitty graphics protocol» — де-факто стандарт картинок в терминале
> kitty придумал популярный протокол показа изображений прямо в терминале; его сегодня поддерживают и другие (в т.ч. [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md)). Картинки рисует встроенный kitten `icat`: `kitten icat image.png`.

## ✨ Возможности

- **Вкладки и сплиты** — раскладки `enabled_layouts splits, stack, tall, fat, grid`.
- **kittens** — мини-утилиты: `icat` (картинки), `diff` (попиксельный дифф/файлы), `hints` (выбор URL/путей мышью-клавиатурой), `ssh` (умный SSH с пробросом конфига/окружения), `unicode_input`, `themes`.
- **Лигатуры**, гиперссылки (OSC 8), truecolor.
- **Remote control** — управлять терминалом скриптами (`kitty @ ...`), сокет/пайп.
- **Платформы:** Linux и macOS. **Нативного Windows нет** — только через WSL.

## 📦 Установка

```bash
# Gentoo
emerge --ask x11-terms/kitty

# Debian / Ubuntu (в репозиториях; для свежей версии — официальный установщик)
sudo apt install kitty
# или последняя версия в ~/.local:
#   curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin

# Arch
sudo pacman -S kitty
```

> [!danger] Не для роутера/Entware
> kitty — графическое OpenGL-приложение, нужен GPU и дисплей. На ASUS RT-AX56U (Entware) **неприменимо**. Но к роутеру удобно ходить kitten'ом `ssh` (`kitten ssh user@router`), а долгие задачи на нём держать в [tmux](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md).

## ⚙️ Конфиг (`~/.config/kitty/kitty.conf`)

Формат — **не TOML**, а собственный: строки вида `ключ значение`, комментарии с `#`, подключение файлов через `include`. Путь меняется переменной `KITTY_CONFIG_DIRECTORY`. Перезагрузка конфига — `ctrl+shift+f5` (или опция `auto_reload_config yes`).

```conf
# ── Шрифт ──────────────────────────────────────────────
font_family      JetBrains Mono
bold_font        auto
italic_font      auto
font_size        12.0

# ── Курсор ─────────────────────────────────────────────
cursor_shape           block
cursor_blink_interval  0

# ── Прокрутка / мышь ───────────────────────────────────
scrollback_lines   10000
mouse_hide_wait    3.0

# ── Окно ───────────────────────────────────────────────
window_padding_width   10
background_opacity     0.95
# include для темы (готовые — kitten themes):
# include current-theme.conf

# ── Цвета (если не подключаешь тему через include) ─────
background  #1e1e2e
foreground  #cdd6f4

# ── Вкладки и раскладки ────────────────────────────────
tab_bar_style    powerline
tab_bar_edge     top
enabled_layouts  splits, stack, tall

# ── Оболочка ───────────────────────────────────────────
shell  /bin/bash

# ── Горячие клавиши ────────────────────────────────────
map ctrl+shift+t        new_tab_with_cwd
map ctrl+shift+enter    launch --location=hsplit --cwd=current
map ctrl+shift+\        launch --location=vsplit --cwd=current
map ctrl+shift+]        next_tab
map ctrl+shift+[        previous_tab
map ctrl+shift+w        close_window
auto_reload_config      yes
```

> [!tip] Темы и kittens
> Сменить тему интерактивно — `kitten themes` (запишет `include`-файл, применится сразу). Полезные kitten'ы на каждый день: `kitten icat file.png` (картинка), `kitten diff a b` (красивый дифф), `kitten ssh host` (SSH с пробросом своего kitty-конфига на удалённую машину).

## ⚖️ kitty vs Rio vs Alacritty

| | kitty | [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) | [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) |
| :--- | :--- | :--- | :--- |
| Рендер | OpenGL | WebGPU | OpenGL |
| Вкладки/сплиты | **да** (layouts) | да | нет |
| Картинки | **свой протокол** + Sixel | Kitty/iTerm2/Sixel | нет |
| Расширения | **kittens** (icat/ssh/diff…) | — | — |
| Remote control | **да** | нет | нет |
| Windows | только WSL | нативно | нативно |
| Язык / лицензия | Python+C+Go / GPL-3.0 | Rust / MIT | Rust / Apache-MIT |

## 💡 Когда выбирать

- Нужен **богатый** терминал «всё включено»: вкладки, сплиты, картинки, скриптуемость — без внешних утилит.
- Активно показываешь **изображения/графики** в терминале или пользуешься kittens (`diff`, `ssh`, `icat`).
- Если важен **минимализм/максимальная скорость** — [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md); если хочется современный **WebGPU**-стек — [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md).

## 🔗 Ссылки

- Сайт/доки: [sw.kovidgoyal.net/kitty](https://sw.kovidgoyal.net/kitty/) · [конфиг](https://sw.kovidgoyal.net/kitty/conf/) · репозиторий: [github.com/kovidgoyal/kitty](https://github.com/kovidgoyal/kitty)
- Связанные: [Rio — терминал на WebGPU](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) · [Alacritty — минимализм](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) · [Konsole — терминал KDE](Konsole%20%E2%80%94%20терминал%20KDE%20%28профили%2C%20split-view%2C%20Qt%29.md) · [tmux — мультиплексор](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md) · [SSH — базовое руководство](../Network/SSH/SSH-Базовое%20руководство.md)

#Terminal #kitty #OpenGL #Linux
