---
создал заметку: 2026-06-16T15:30:00
author: WhiteK0T
tags:
  - Terminal
  - Konsole
  - KDE
  - Qt
  - Linux
Источник:
  - https://konsole.kde.org
  - https://docs.kde.org/?application=konsole
---

# 🖥️ Konsole — терминал KDE (профили, split-view, Qt)

**Konsole** ([konsole.kde.org](https://konsole.kde.org)) — штатный эмулятор терминала **KDE**, часть KDE Applications, на **Qt / KDE Frameworks**. В отличие от GPU-терминалов ([Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md), [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md), [kitty](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md)) делает ставку не на скорость рендера, а на **интеграцию с KDE и удобную настройку мышью**: профили, вкладки, разделение окна, D-Bus-скриптинг, встраивание в другие приложения KDE (терминал в Dolphin, Kate, Kdevelop — это Konsole как KPart).

> [!info] Не GPU-рендеринг — и это нормально
> Konsole рисует средствами Qt (CPU/обычная отрисовка), без OpenGL/WebGPU. Для повседневной работы это незаметно; гнаться за GPU-ускорением имеет смысл при экстремальном выводе (логи мегабайтами). Зато Konsole — самый «домашний» вариант на **KDE Plasma** и настраивается без правки конфигов руками.

## ✨ Возможности

- **Профили** — наборы настроек (шрифт, цвета, команда, поведение), переключаются на лету.
- **Вкладки и split-view** (разделение окна по горизонтали/вертикали).
- **Цветовые схемы**, прозрачность/размытие фона (на KWin), темы.
- **Закладки** каталогов/SSH, поиск по выводу, экспорт вывода.
- **D-Bus** — скриптование терминала из других программ (`qdbus org.kde.konsole ...`).
- **KPart** — встраивается как виджет-терминал в Dolphin/Kate/KDevelop.

## 📦 Установка

```bash
# Gentoo
emerge --ask kde-apps/konsole

# Debian / Ubuntu
sudo apt install konsole

# Arch
sudo pacman -S konsole
```

> [!note] Тянет зависимости KDE
> Вне KDE Plasma Konsole притащит часть KDE Frameworks/Qt. На GNOME/других DE работать будет, но «весит» больше, чем тонкий [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md). На Plasma всё это и так уже стоит.

> [!danger] Не для роутера/Entware
> Графическое Qt-приложение, нужен дисплей. На ASUS RT-AX56U (Entware) **неприменимо** — к роутеру по [SSH](../Network/SSH/SSH-Базовое%20руководство.md), долгие задачи в [tmux](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md).

## ⚙️ Настройка: GUI-профили (а не текстовый конфиг)

Главный путь — **меню**: «Настройки → Изменить текущий профиль» (шрифт, схема, прокрутка, поведение). Но всё это лежит и в файлах (INI), их можно править руками или переносить между машинами:

| Файл | Что хранит |
| :--- | :--- |
| `~/.config/konsolerc` | общие настройки приложения, профиль по умолчанию |
| `~/.local/share/konsole/<Имя>.profile` | профиль (шрифт, команда, прокрутка…) |
| `~/.local/share/konsole/<Имя>.colorscheme` | цветовая схема |

Пример профиля `~/.local/share/konsole/Coding.profile`:

```ini
[General]
Name=Coding
Command=/bin/bash
Parent=FALLBACK/

[Appearance]
ColorScheme=Breeze
Font=JetBrains Mono,12,-1,5,50,0,0,0,0,0

[Scrolling]
HistoryMode=2          ; 0=нет, 1=фиксированный, 2=безлимит
HistorySize=10000      ; для HistoryMode=1

[Cursor Options]
CursorShape=0          ; 0=Block, 1=IBeam, 2=Underline
BlinkingCursorEnabled=true

[Terminal Features]
BlinkingTextEnabled=true
```

Сделать профиль дефолтным — в `~/.config/konsolerc`:

```ini
[Desktop Entry]
DefaultProfile=Coding.profile
```

> [!tip] Строка Font — это формат Qt
> `Font=JetBrains Mono,12,...` — сериализованный `QFont`: семейство, размер, далее служебные поля. Проще выставить шрифт в GUI (профиль → «Внешний вид»), чем собирать строку вручную. Изменения профиля применяются сразу к новым сессиям.

## ⌨️ Горячие клавиши по умолчанию

| Сочетание | Действие |
| :--- | :--- |
| `Ctrl+Shift+C` / `V` | копировать / вставить |
| `Ctrl+Shift+T` | новая вкладка |
| `Ctrl+Shift+N` | новое окно |
| `Ctrl+Shift+W` | закрыть вкладку |
| `Ctrl+Shift+Q` | закрыть окно |
| `Shift+←` / `→` | предыдущая / следующая вкладка |
| `Ctrl+Alt+←` / `→` | переместить вкладку |
| `Ctrl+(` | сплит влево/вправо |
| `Ctrl+)` | сплит сверху/снизу |
| `Ctrl+Shift+[` / `]` | сжать / расширить панель |
| `Ctrl+Shift+H` | отсоединить панель (view) |
| `Ctrl+Shift+L` | отсоединить вкладку |
| `Ctrl+Shift+F` | поиск (`F3` / `Shift+F3` — далее / назад) |
| `Ctrl++` / `Ctrl+-` / `Ctrl+0` | шрифт +/−/сброс |
| `Ctrl+Shift+K` | очистить буфер и сбросить |
| `F11` | полноэкранный режим |

> [!note] Всё переназначается в GUI
> «Настройки → Комбинации клавиш» — полный редактор шорткатов Konsole; список выше — дефолты «из коробки».

## ⚖️ Сравнение терминалов

| | [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) | [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) | [kitty](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md) | Konsole |
| :--- | :--- | :--- | :--- | :--- |
| Рендер | WebGPU | OpenGL | OpenGL | **Qt (CPU)** |
| Вкладки/сплиты | да | нет | да | да |
| Картинки | Kitty/iTerm2/Sixel | нет | свой протокол + Sixel | нет |
| Настройка | TOML-конфиг | TOML-конфиг | конфиг | **GUI/профили** |
| Скриптинг/расширения | — | — | kittens + remote | **D-Bus / KPart** |
| Windows | нативно | нативно | только WSL | нет |
| Язык / лицензия | Rust / MIT | Rust / Apache-MIT | Python+C+Go / GPL-3 | C++/Qt / GPL-2 |
| Вес | средний | лёгкий | средний | **тяжелее** (KDE/Qt) |

## 💡 Когда выбирать

- Сидишь на **KDE Plasma** — Konsole самый родной, удобный и без бубна с конфигами.
- Нужна **настройка мышью**, профили под разные задачи, split-view и интеграция с Dolphin/Kate.
- Если важны **скорость рендера/минимализм** — [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md); **картинки/kittens** — [kitty](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md); современный **WebGPU** — [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md).

## 🔗 Ссылки

- Сайт: [konsole.kde.org](https://konsole.kde.org) · документация: [docs.kde.org → Konsole](https://docs.kde.org/?application=konsole)
- Связанные: [kitty](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md) · [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) · [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) · [tmux — мультиплексор](tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md) · [SSH — базовое руководство](../Network/SSH/SSH-Базовое%20руководство.md)

#Terminal #Konsole #KDE #Qt #Linux
