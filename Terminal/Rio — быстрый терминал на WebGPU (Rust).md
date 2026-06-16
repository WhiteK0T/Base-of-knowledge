---
создал заметку: 2026-06-16T14:00:00
author: WhiteK0T
tags:
  - Terminal
  - Rio
  - WebGPU
  - Rust
  - Linux
Источник:
  - https://itshaman.ru/news/software/rio-bystryi-terminal-s-podderzhkoi-webgpu-dlya-linux
  - https://rioterm.com
  - https://github.com/raphamorim/rio
---

# 🌊 Rio — быстрый терминал на WebGPU (Rust)

**Rio** ([rioterm.com](https://rioterm.com), [github.com/raphamorim/rio](https://github.com/raphamorim/rio)) — кроссплатформенный аппаратно-ускоренный эмулятор терминала на **Rust**, рендерящий через **WebGPU** (WGPU). Автор — Raphael Amorim, первый релиз в 2023. От «голого» [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) отличается тем, что из коробки умеет **вкладки и сплиты** — но при этом остаётся быстрым GPU-терминалом, настраиваемым текстовым конфигом.

> [!info] WebGPU вместо OpenGL
> Rio рендерит через WGPU (реализация стандарта WebGPU на Rust) и сам выбирает низкоуровневый бэкенд: **Vulkan** (Linux), **Metal** (macOS), **DX12** (Windows). Это современнее, чем OpenGL у Alacritty, и даёт переносимость на разные GPU. Парсинг ANSI, обработку событий и сетку Rio переиспользует из кода Alacritty.

## ✨ Возможности

- **Вкладки и сплиты** (навигация Tab / NativeTab / Plain, режим `use-split`).
- **Лигатуры** шрифтов (`->` → `→`), Sixel и протоколы картинок **iTerm2 / Kitty**.
- **Vi-режим**, прозрачность, размытие фона (blur), фоновое изображение.
- **RetroArch-шейдеры** (CRT-фильтры и т.п.) через `filters`.
- Темы, горячая перезагрузка конфига, **нативные ARM64-сборки** (вплоть до Raspberry Pi).

## 📦 Установка

Целевые десктоп-системы владельца (Gentoo, Debian/Ubuntu, Arch). Универсальный путь — **Flatpak** с Flathub.

```bash
# Flatpak (любой дистрибутив с настроенным Flathub)
flatpak install flathub com.rioterm.Rio     # точный ID проверь: flatpak search rio

# Arch (AUR)
yay -S rio

# Gentoo — в основном дереве нет; через оверлей GURU либо cargo:
eselect repository enable guru && emaint sync -r guru && emerge --ask rio
# или из исходников (нужен Rust-тулчейн):
cargo install --git https://github.com/raphamorim/rio

# Debian / Ubuntu — пакета в apt нет: Flatpak (выше) или .deb из релизов GitHub
```

> [!danger] Не для роутера/Entware
> Rio — графическое приложение (Wayland/X11/Metal/DX), требует GPU и дисплея. На ASUS RT-AX56U (Entware, без графики) **неприменимо** — терминал-эмулятор ставится на десктоп, а к роутеру подключаешься по [SSH](../Network/SSH/SSH-Базовое%20руководство.md) уже из него.

## ⚙️ Конфиг (`~/.config/rio/config.toml`)

Формат — **TOML**. Расположение: Linux/macOS — `~/.config/rio/config.toml` (или `$XDG_CONFIG_HOME/rio/`), Windows — `%USERPROFILE%\AppData\Local\rio\config.toml`. Путь переопределяется переменной `RIO_CONFIG_HOME`. Изменения **подхватываются на лету** (горячая перезагрузка).

```toml
# ── Общее ──────────────────────────────────────────────
confirm-before-quit = true
copy-on-select = false
line-height = 1.0
padding = [10]                 # отступ вокруг текста, px
scrollback-history-limit = 10000
theme = "dracula"              # темы из ~/.config/rio/themes/

# ── Окно ───────────────────────────────────────────────
[window]
width = 800
height = 500
mode = "Windowed"              # Windowed | Maximized | Fullscreen
opacity = 0.95                 # прозрачность 0.0–1.0
blur = true                    # размытие фона под окном
decorations = "Enabled"        # Enabled | Disabled | Transparent | Buttonless

# ── Рендер (GPU) ───────────────────────────────────────
[renderer]
backend = "Vulkan"             # Automatic | Vulkan | Metal | Webgpu | Dx12 | GL
target-fps = 120
strategy = "events"            # events (экономно) | game (макс. плавность)
disable-occluded-render = true

# ── Шрифты ─────────────────────────────────────────────
[fonts]
size = 13
family = "JetBrains Mono"      # одинаковый для regular/bold/italic, если не задано отдельно

[fonts.bold]
family = "JetBrains Mono"
style = "default"

# ── Цвета (если не используешь theme) ──────────────────
[colors]
background = '#1e1e2e'
foreground = '#cdd6f4'
cursor = '#f5e0dc'

# ── Курсор ─────────────────────────────────────────────
[cursor]
shape = "block"                # block | underline | beam
blinking = false

# ── Навигация: вкладки/сплиты ──────────────────────────
[navigation]
mode = "Tab"                   # Tab | NativeTab | Plain
use-split = true
hide-if-single = true          # прятать панель вкладок, если вкладка одна

# ── Оболочка ───────────────────────────────────────────
[shell]
program = "/bin/bash"
args = ["--login"]
```

> [!tip] Бэкенд рендера
> `backend = "Automatic"` (по умолчанию) сам выберет лучший доступный API. Если на Linux артефакты/тормоза — попробуй явно `"Vulkan"`, на старом железе без Vulkan — `"GL"`. `strategy = "game"` даёт максимально плавную прокрутку ценой большей нагрузки на GPU.

## ⌨️ Горячие клавиши по умолчанию

Linux/Windows (на macOS обычно `Cmd` вместо `Ctrl+Shift`):

| Сочетание | Действие |
| :--- | :--- |
| `Ctrl+Shift+C` / `V` | копировать / вставить |
| `Ctrl+Shift+T` | новая вкладка |
| `Ctrl+Shift+W` | закрыть вкладку |
| `Ctrl+Shift+1…9` | перейти к вкладке № |
| `Ctrl+Shift+N` | новое окно |
| `Ctrl+Shift+R` | сплит вправо |
| `Ctrl+Shift+D` | сплит вниз |
| `Ctrl+Shift+[` / `]` | предыдущий / следующий сплит |
| `Ctrl+=` / `Ctrl+-` / `Ctrl+0` | шрифт +/−/сброс |
| `Ctrl+Shift+F` / `B` | поиск вперёд / назад |
| `Ctrl+Shift+P` | палитра команд |
| `Ctrl+Shift+,` | открыть конфиг |

## ⚖️ Сравнение терминалов

| | Rio | [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) | [kitty](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md) | [Konsole](Konsole%20%E2%80%94%20терминал%20KDE%20%28профили%2C%20split-view%2C%20Qt%29.md) |
| :--- | :--- | :--- | :--- | :--- |
| Рендер | **WebGPU** | OpenGL | OpenGL | Qt (CPU) |
| Вкладки/сплиты | да | нет | да | да |
| Картинки | Kitty/iTerm2/Sixel | нет | свой протокол + Sixel | нет |
| Настройка | TOML-конфиг | TOML-конфиг | конфиг | GUI/профили |
| Скриптинг/расширения | — | — | kittens + remote | D-Bus / KPart |
| Windows | нативно | нативно | только WSL | нет |
| Язык / лицензия | Rust / MIT | Rust / Apache-MIT | Python+C+Go / GPL-3 | C++/Qt / GPL-2 |
| Вес | средний | лёгкий | средний | тяжелее |

## 💡 Когда выбирать

- Хочешь **GPU-терминал со вкладками/сплитами и картинками** из коробки, без tmux.
- Нравится современный стек (WebGPU) и кроссплатформа (вплоть до ARM64/Raspberry Pi).
- Если нужен **предельный минимализм** и максимальная стабильность — смотри [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md).

## 🔗 Ссылки

- Сайт/доки: [rioterm.com](https://rioterm.com) · [docs/config](https://rioterm.com/docs/config) · репозиторий: [github.com/raphamorim/rio](https://github.com/raphamorim/rio)
- Обзор: [itshaman.ru](https://itshaman.ru/news/software/rio-bystryi-terminal-s-podderzhkoi-webgpu-dlya-linux)
- Связанные: [Alacritty — GPU-терминал](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) · [kitty — kittens и графика](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md) · [Konsole — терминал KDE](Konsole%20%E2%80%94%20терминал%20KDE%20%28профили%2C%20split-view%2C%20Qt%29.md) · [tmux — мультиплексор](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md) · [SSH — базовое руководство](../Network/SSH/SSH-Базовое%20руководство.md)

#Terminal #Rio #WebGPU #Rust #Linux
