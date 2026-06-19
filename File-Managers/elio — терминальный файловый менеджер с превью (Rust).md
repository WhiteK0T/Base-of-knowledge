---
создал заметку: 2026-06-19T19:55:00
author: WhiteK0T
tags:
  - FileManager
  - elio
  - Terminal
  - Rust
  - TUI
  - Linux
Источник:
  - https://t.me/open_source_friend/5672
  - https://github.com/elio-fm/elio
  - https://elio-fm.github.io/
---

# 📂 elio — терминальный файловый менеджер с превью (Rust)

**elio** ([github.com/elio-fm/elio](https://github.com/elio-fm/elio), MIT, ~661★) — «snappy, batteries-included» **TUI-файловый менеджер**: трёхпанельный интерфейс с богатыми превью (включая **картинки прямо в терминале**), массовыми операциями и корзиной. Написан на **Rust** (UI на [ratatui](https://github.com/ratatui/ratatui)). Зрелее многих «новостных» проектов — **v1.9.0** (июнь 2026), ~494 коммита.

> [!info] Что такое «трёхпанельный» (Miller columns)
> Слева — **Places** (закладки/быстрый доступ), по центру — **Files** (содержимое текущей папки), справа — **Preview** (превью выделенного файла). Видишь структуру, содержимое и предпросмотр одновременно — удобно навигировать, не открывая файлы.

## ✨ Возможности

- **Превью почти всего:** текст, код (подсветка), документы, архивы, медиа, бинарники с метаданными.
- **Картинки в терминале:** инлайн-рендер через **Kitty Graphics**, **Sixel**, **iTerm2 Inline** (нужен терминал с поддержкой — см. [kitty](../Terminal/kitty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D1%81%20kittens%20%D0%B8%20%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%BE%D0%B9%20%28OpenGL%29.md) / [Rio](../Terminal/Rio%20%E2%80%94%20%D0%B1%D1%8B%D1%81%D1%82%D1%80%D1%8B%D0%B9%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D0%BD%D0%B0%20WebGPU%20%28Rust%29.md)).
- **Файловые операции:** создание, переименование, удаление, **корзина с восстановлением**, **массовое переименование** (bulk rename), симлинки.
- **Поиск/навигация:** fuzzy-поиск файлов/папок, интеграция с **zoxide** (прыжки по частым каталогам), grid/list-виды с зумом, **vim-хоткеи** (hjkl, моушены) + мышь.
- **Shell-интеграция:** `cd-on-exit` обёртки для **bash / zsh / fish / Nushell** (выходишь из elio — попадаешь в выбранную папку).
- **Темы:** кастомизация через `theme.toml`, биндинги — в `[keys]` конфига.

> [!note] Зависимости для богатых превью (опционально)
> Сам elio лёгкий, но для части превью нужны внешние утилиты: **Poppler** (PDF), **FFmpeg/FFprobe** (медиа), **resvg** (SVG), **7z/unar** (архивы), **FontForge** (шрифты). Для иконок — **Nerd Font**. Без них базовые превью (текст/код) работают, а спец-форматы просто не предпросматриваются.

## 📦 Установка

Целевые десктоп-системы владельца. elio есть в нескольких пакетных менеджерах, плюс ставится из crates.io.

```bash
# Универсально — из crates.io (нужен Rust-тулчейн)
cargo install elio

# Arch — AUR
yay -S elio            # уточни точное имя пакета в AUR

# Debian / Ubuntu — официальный apt-репозиторий проекта (см. README) либо .deb из релизов
# Fedora — COPR

# Gentoo — в основном дереве нет: cargo install elio
#   (или через оверлей, если появится ebuild)

# macOS / Linux — Homebrew
brew install elio      # точный tap/формулу проверь на странице проекта
```

> [!danger] Роутер / Entware — практически N/A
> Хоть elio и TUI, он требует **сборки Rust** и тяжёлых утилит-превью; на ASUS RT-AX56U (armv7, 256 МБ flash) это непрактично, в репозитории Entware его нет. Для файловых операций на роутере — `mc` (Midnight Commander, если есть в opkg), [lf](https://github.com/gokcehan/lf)/[nnn](https://github.com/jarun/nnn) полегче, либо просто `ls`/`find` по [SSH](../Network/SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md).

## ⚙️ Конфиг

- Основной конфиг: `~/.config/elio/config.toml` (Linux/BSD; на macOS/Windows — платформенные пути).
- Хоткеи — секция `[keys]`; тема — отдельный `theme.toml`.

## 💡 Кому полезно

- Любишь **навигацию из терминала** и хочешь видеть **превью (в т.ч. картинки)** без выхода в GUI-файлменеджер.
- Уже в экосистеме **vim + zoxide + Nerd Font** — elio ложится естественно (cd-on-exit, fuzzy, zoxide).
- Альтернативы в той же нише: **yazi**, **lf**, **ranger**, **nnn**, **Midnight Commander** — если elio покажется тяжёлым/избыточным.

## 🔗 Ссылки

- Репозиторий: [github.com/elio-fm/elio](https://github.com/elio-fm/elio) · сайт: [elio-fm.github.io](https://elio-fm.github.io/)
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5672)
- Связанные: [kitty (протокол картинок)](../Terminal/kitty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D1%81%20kittens%20%D0%B8%20%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%BE%D0%B9%20%28OpenGL%29.md) · [Rio (терминал на WebGPU)](../Terminal/Rio%20%E2%80%94%20%D0%B1%D1%8B%D1%81%D1%82%D1%80%D1%8B%D0%B9%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D0%BD%D0%B0%20WebGPU%20%28Rust%29.md) · [Сравнение пакетных менеджеров](../Linux/Package-Manager/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2.md)

#FileManager #elio #Terminal #Rust #TUI #Linux
