---
создал заметку: 2026-06-16T14:10:00
author: WhiteK0T
tags:
  - Terminal
  - Alacritty
  - OpenGL
  - Rust
  - Linux
Источник:
  - https://habr.com/ru/articles/746730/
  - https://github.com/alacritty/alacritty
  - https://alacritty.org
---

# ⚡ Alacritty — GPU-терминал на OpenGL (минимализм)

**Alacritty** ([github.com/alacritty/alacritty](https://github.com/alacritty/alacritty)) — быстрый кроссплатформенный эмулятор терминала на **Rust** с **GPU-ускорением через OpenGL** (минимум — OpenGL ES 2.0). Философия — **«делать одно дело хорошо»**: это просто очень быстрый терминал с разумными дефолтами и гибким текстовым конфигом, без вкладок, сплитов и GUI-настроек. Двойная лицензия **Apache 2.0 / MIT**.

> [!info] Намеренный минимализм
> Вкладок и разделения окна **нет by design** — авторы считают, что это задача оконного менеджера или мультиплексора. Связка-классика: **Alacritty + [tmux](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md)** (или WM) даёт вкладки/сплиты, оставляя сам терминал тонким и быстрым. Нет и графического редактора настроек — только конфиг-файл.

## ✨ Что важно знать

- **GPU-рендеринг** (OpenGL) → высокая пропускная способность и плавность даже на потоке вывода.
- **Платформы:** Linux, BSD, macOS, Windows (на Windows нужен ConPTY — Win10 1809+).
- **Скроллбэк**, поиск, vi-режим, подсказки-хинты (hints) для URL/путей.
- **Горячая перезагрузка** конфига (`live_config_reload`).
- **Нет**: вкладок, сплитов, картинок (Sixel/Kitty), GUI-настроек — это сознательный выбор.

## 📦 Установка

Alacritty есть в штатных репозиториях основных дистрибутивов:

```bash
# Gentoo
emerge --ask x11-terms/alacritty

# Debian / Ubuntu
sudo apt install alacritty          # есть в universe; свежее — PPA aslatter/ppa

# Arch
sudo pacman -S alacritty
```

> [!danger] Не для роутера/Entware
> Это графическое X11/Wayland-приложение, требует GPU и дисплея. На ASUS RT-AX56U (Entware) **неприменимо** — ставится на десктоп, а к роутеру подключаешься по [SSH](../Network/SSH/SSH-Базовое%20руководство.md).

## ⚙️ Конфиг (`~/.config/alacritty/alacritty.toml`)

> [!warning] Формат TOML, а не YAML
> Со свежих версий (0.13+) Alacritty перешёл с `alacritty.yml` на **`alacritty.toml`**. Старые YAML-конфиги из интернета **не подойдут** — нужен TOML. Также `import` теперь живёт в таблице `[general]`.

Файл ищется по порядку: `$XDG_CONFIG_HOME/alacritty/alacritty.toml` → `$HOME/.config/alacritty/alacritty.toml` → `$HOME/.alacritty.toml` → `/etc/alacritty/alacritty.toml` (Windows: `%APPDATA%\alacritty\alacritty.toml`).

```toml
# ── Общее ──────────────────────────────────────────────
[general]
import = ["~/.config/alacritty/themes/dracula.toml"]   # модульные конфиги/темы
live_config_reload = true

# ── Окно ───────────────────────────────────────────────
[window]
padding = { x = 10, y = 10 }
opacity = 0.95
decorations = "Full"           # Full | None | Transparent | Buttonless
startup_mode = "Windowed"      # Windowed | Maximized | Fullscreen

# ── Прокрутка ──────────────────────────────────────────
[scrolling]
history = 10000                # строк в буфере (макс. 100000)
multiplier = 3

# ── Шрифт ──────────────────────────────────────────────
[font]
size = 12.0
normal = { family = "JetBrains Mono", style = "Regular" }
bold   = { style = "Bold" }    # family наследуется от normal

# ── Цвета (если не подключаешь тему через import) ──────
[colors.primary]
background = "#1e1e2e"
foreground = "#cdd6f4"

# ── Курсор ─────────────────────────────────────────────
[cursor]
style = { shape = "Block", blinking = "Off" }   # Block | Underline | Beam

# ── Оболочка ───────────────────────────────────────────
[terminal]
shell = { program = "/bin/bash", args = ["--login"] }

# ── Клавиши ────────────────────────────────────────────
[keyboard]
bindings = [
  { key = "V", mods = "Control|Shift", action = "Paste" },
  { key = "C", mods = "Control|Shift", action = "Copy"  },
  { key = "Equals", mods = "Control",  action = "IncreaseFontSize" },
  { key = "Minus",  mods = "Control",  action = "DecreaseFontSize" },
]
```

> [!tip] Темы через import
> Держи цветовые схемы отдельными `.toml` и подключай через `[general].import` — удобно переключать. Готовые темы есть в репозитории [alacritty/alacritty-theme](https://github.com/alacritty/alacritty-theme). Поскольку `live_config_reload = true`, правки применяются без перезапуска.

## ⚖️ Alacritty vs Rio

| | Alacritty | [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) |
| :--- | :--- | :--- |
| Рендер | OpenGL | WebGPU (Vulkan/Metal/DX12) |
| Вкладки/сплиты | **нет** (tmux/WM) | встроены |
| Философия | **минимализм**, одно дело | богаче из коробки |
| Зрелость | проверенный, стабильный | моложе |
| Картинки (Sixel/Kitty) | нет | да |
| Язык | Rust | Rust |

## 💡 Когда выбирать

- Нужен **максимально быстрый и стабильный** терминал, а вкладки/сплиты ты и так держишь на [tmux](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md) или WM.
- Ценишь минимализм и предсказуемость, не нужен «комбайн».
- Если хочется вкладок/сплитов/картинок **внутри** терминала — смотри [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md).

## 🔗 Ссылки

- Репозиторий: [github.com/alacritty/alacritty](https://github.com/alacritty/alacritty) · сайт: [alacritty.org](https://alacritty.org) · темы: [alacritty/alacritty-theme](https://github.com/alacritty/alacritty-theme)
- Обзор: [habr.com/ru/articles/746730](https://habr.com/ru/articles/746730/)
- Связанные: [Rio — терминал на WebGPU](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) · [kitty — kittens и графика](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md) · [Konsole — терминал KDE](Konsole%20%E2%80%94%20терминал%20KDE%20%28профили%2C%20split-view%2C%20Qt%29.md) · [tmux — мультиплексор](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md) · [SSH — базовое руководство](../Network/SSH/SSH-Базовое%20руководство.md)

#Terminal #Alacritty #OpenGL #Rust #Linux
