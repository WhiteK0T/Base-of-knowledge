---
создал заметку: 2026-06-19T20:30:00
author: WhiteK0T
tags:
  - FileManager
  - far2l
  - FAR
  - Terminal
  - Linux
  - TUI
Источник:
  - https://github.com/elfmz/far2l
  - https://github.com/WhiteK0T/far2l-build-script
  - http://farmanager.com/
---

# 🗂️ far2l — порт FAR Manager на Linux/macOS/BSD (двухпанельный)

**far2l** ([elfmz/far2l](https://github.com/elfmz/far2l), GPLv2) — порт легендарного **FAR Manager v2** на Linux/macOS/BSD: ортодоксальный **двухпанельный** файловый менеджер (стиль Norton/Volkov Commander) со встроенным редактором, вьювером, плагинами и сетевыми протоколами. Это **тот самый FAR**, но нативно в терминале на Unix. Текущая версия — **v2.8.0** (март 2026), статус — **BETA** («use on your own risk»).

> [!tip] У меня есть свой скрипт сборки far2l
> Для **Debian/Ubuntu** есть мой автоматический сборщик из исходников: **[WhiteK0T/far2l-build-script](https://github.com/WhiteK0T/far2l-build-script)** (MIT). Он сам определяет версию ОС, ставит правильные зависимости (wxWidgets 3.0/3.2), собирает в параллель и кладёт бинарь в `/usr/local/bin`. См. раздел «Установка» ниже.

> [!info] Почему «v2», а не [far3](Far%20Manager%203%20%28far3%29%20%E2%80%94%20%D0%BE%D1%80%D1%82%D0%BE%D0%B4%D0%BE%D0%BA%D1%81%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Windows.md)
> Оригинальный [Far Manager 3](Far%20Manager%203%20%28far3%29%20%E2%80%94%20%D0%BE%D1%80%D1%82%D0%BE%D0%B4%D0%BE%D0%BA%D1%81%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Windows.md) сильно завязан на Win32-консоль и API Windows. far2l взял за основу **v2** и переписал платформо-зависимый слой под Unix (свой бэкенд терминала, буфер обмена, плагины). Поэтому на Linux «родной FAR» — это **far2l**, а не far3 (тот идёт только под Windows / через Wine).

## ✨ Возможности

- **Двухпанельный ортодоксальный интерфейс**, клавиатуро-центричный (F1–F10, как в Norton/FAR), с поддержкой мыши.
- **Встроенный редактор** с подсветкой синтаксиса (плагин **Colorer**), вьювер, **hex-редактор**.
- **Сеть — плагин NetRocks:** SFTP, SCP, FTP, FTPS, **SMB**, NFS, WebDAV, **AWS S3** (ходить по удалённым ФС как по локальным).
- **Архивы — multiarc** (zip/tar/7z и пр.), просмотр изображений, 20+ рабочих плагинов.
- **Скриптинг на Python** (опционально), макросы.
- **True color**, несколько бэкендов отображения: **TTY** (чистый терминал), **TTY|X / TTY|Xi** (X11), **GUI** (wxWidgets/SDL); интеграция буфера обмена несколькими методами.

> [!note] Бэкенды: TTY vs GUI
> far2l умеет работать как **в чистом терминале (TTY)** — удобно по SSH на сервере, — так и в **GUI-окне** (wxWidgets), где доступны все клавиши/мышь без ограничений эмулятора. Для удалённой работы по [SSH](../Network/SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md) ставь TTY-сборку; есть и спец-механизм проброса клавиш far2l поверх ssh.

## 📦 Установка

Целевые десктоп-системы владельца. far2l есть в ряде репозиториев, плюс собирается из исходников (CMake).

### Debian / Ubuntu — мой скрипт (из исходников)

```bash
curl -fsSL https://raw.githubusercontent.com/WhiteK0T/far2l-build-script/refs/heads/main/far-build.sh -o far-build.sh
chmod +x far-build.sh
sudo ./far-build.sh
```

Скрипт: определяет версию ОС (Ubuntu 22.04/24.04, Debian 12/13), ставит зависимости (нужный wxWidgets), делает shallow-clone far2l, конфигурит CMake, собирает `-j$(nproc)` и ставит в `/usr/local/bin`. Кастомизация — через переменные (`CMAKE_INSTALL_PREFIX`, Release/Debug). Альтернативно с **23.10** far2l есть в **официальных репах** (`sudo apt install far2l`) и в PPA — но пакет бывает старее апстрима.

### Другие системы

```bash
# Arch — AUR
yay -S far2l            # или far2l-git под свежий мастер

# Gentoo — в основном дереве нет: сборка из исходников
sudo emerge dev-util/cmake   # + g++, pkg-config, git, wxGTK (USE по бэкенду)
git clone --depth 1 https://github.com/elfmz/far2l && cd far2l
cmake -B _build -DCMAKE_BUILD_TYPE=Release && cmake --build _build -j$(nproc)
sudo cmake --install _build

# macOS / Linux — Homebrew; есть также AppImage, Fedora COPR, OpenSUSE, Docker
brew install far2l
```

Минимальные зависимости: CMake, pkg-config, g++, git. Опционально: `libwxgtk3.x`, `libx11-dev`, `libxml2-dev`, `libssh-dev`, `libssl-dev`, `libsmbclient-dev`, `python3-dev` (под нужные плагины/бэкенды).

> [!danger] Роутер / Entware — N/A
> far2l — C++-приложение с wxWidgets/TTY-бэкендом; сборка на ASUS RT-AX56U (armv7, 256 МБ flash) непрактична, в opkg его нет. К роутеру подключайся по SSH из far2l/терминала на десктопе; на самом роутере — `mc` (если есть в opkg) или `ls`/`find`.

## 💡 Кому полезно

- Привык к **FAR/Norton Commander** и хочешь тот же воркфлоу нативно на Linux/macOS (а не через Wine).
- Нужен мощный **двухпанельник** с встроенным редактором, архивами и **сетью (SFTP/SMB/S3)** в одном окне.
- Любишь клавиатуро-центричную работу; mouse — опционально.
- Альтернативы: [elio](elio%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D1%81%20%D0%BF%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20%28Rust%29.md) (современный, с превью-картинками), Midnight Commander, yazi/lf/ranger/nnn.

## 🔗 Ссылки

- Репозиторий: [github.com/elfmz/far2l](https://github.com/elfmz/far2l) · оригинал FAR: [farmanager.com](http://farmanager.com/)
- **Мой скрипт сборки:** [github.com/WhiteK0T/far2l-build-script](https://github.com/WhiteK0T/far2l-build-script)
- Связанные: [Far Manager 3 (far3, Windows-оригинал)](Far%20Manager%203%20%28far3%29%20%E2%80%94%20%D0%BE%D1%80%D1%82%D0%BE%D0%B4%D0%BE%D0%BA%D1%81%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Windows.md) · [elio (TUI-менеджер с превью)](elio%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D1%81%20%D0%BF%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20%28Rust%29.md) · [SSH-Базовое руководство](../Network/SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md)

#FileManager #far2l #FAR #Terminal #Linux #TUI
