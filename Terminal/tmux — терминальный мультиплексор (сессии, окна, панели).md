---
создал заметку: 2026-06-16T14:30:00
author: WhiteK0T
tags:
  - Terminal
  - tmux
  - Linux
  - SSH
Источник:
  - https://github.com/tmux/tmux
  - https://man.openbsd.org/tmux
---

# 🪟 tmux — терминальный мультиплексор (сессии, окна, панели)

**tmux** ([github.com/tmux/tmux](https://github.com/tmux/tmux)) — терминальный **мультиплексор**: внутри одного окна терминала он держит несколько **сессий → окон → панелей**, а главное — **сессия живёт на сервере tmux и переживает отключение**. Закрыл ssh / упала сеть — процессы продолжают работать, переподключился (`tmux attach`) и продолжил с того же места. Идеальная пара к минималистичным эмуляторам вроде [Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md): сам терминал тонкий и быстрый, а вкладки/сплиты даёт tmux.

> [!info] Модель: сервер → сессия → окно → панель
> При первом запуске поднимается фоновый **сервер** tmux. В нём — **сессии** (рабочие пространства), в сессии — **окна** (как вкладки), в окне — **панели** (сплиты). Клиент (`attach`) лишь подключается к серверу; отключение клиента (`detach`) не убивает сессию.

## 🚀 Базовые команды (из шелла)

| Команда | Действие |
| :--- | :--- |
| `tmux` | новая безымянная сессия |
| `tmux new -s work` | новая сессия с именем `work` |
| `tmux ls` | список сессий |
| `tmux attach -t work` (`tmux a -t work`) | подключиться к сессии |
| `tmux detach` (или `prefix d`) | отключиться, оставив сессию жить |
| `tmux kill-session -t work` | убить сессию |
| `tmux kill-server` | убить сервер и все сессии |

## ⌨️ Префикс и горячие клавиши

Почти всё внутри tmux — через **префикс** (по умолчанию `Ctrl-b`), затем клавиша. Ниже — самое нужное (значения для дефолтного префикса):

| Сочетание | Действие |
| :--- | :--- |
| `prefix c` | новое окно |
| `prefix ,` | переименовать окно |
| `prefix n` / `prefix p` | следующее / предыдущее окно |
| `prefix 0…9` | перейти к окну по номеру |
| `prefix w` | список окон/сессий |
| `prefix %` | разделить панель **вертикально** |
| `prefix "` | разделить панель **горизонтально** |
| `prefix ←↑↓→` | перейти между панелями |
| `prefix z` | развернуть/свернуть панель (zoom) |
| `prefix x` | закрыть панель |
| `prefix [` | режим прокрутки/копирования (выход — `q`) |
| `prefix d` | detach (отключиться) |
| `prefix ?` | список всех привязок |

## 📦 Установка

tmux есть везде, включая роутер — в отличие от GUI-терминалов.

```bash
# Gentoo
emerge --ask app-misc/tmux

# Debian / Ubuntu
sudo apt install tmux

# Arch
sudo pacman -S tmux

# Entware (ASUS RT-AX56U, armv7) — РАБОТАЕТ и очень полезен
opkg install tmux
```

> [!tip] tmux на роутере — то, что нужно
> В отличие от [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md)/[Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) (графика, на Entware неприменимы), tmux — консольный и ставится на роутер из коробки. Запусти долгий процесс (бэкап на USB, `emonoda`, мониторинг) внутри `tmux` по [SSH](../Network/SSH/SSH-Базовое%20руководство.md) — оборвётся соединение, а задача продолжит работать; вернёшься через `tmux attach`.

## ⚙️ Конфиг (`~/.config/tmux/tmux.conf` или `~/.tmux.conf`)

```bash
# ── Префикс на Ctrl-a (удобнее, чем Ctrl-b) ────────────
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# ── Базовое поведение ──────────────────────────────────
set -g mouse on                 # мышь: выделение, ресайз, выбор панелей
set -g base-index 1             # окна с 1, а не с 0
setw -g pane-base-index 1
set -sg escape-time 10          # без задержки Esc (важно для vim)
set -g history-limit 100000     # буфер прокрутки

# ── Перезагрузка конфига по prefix r ───────────────────
bind r source-file ~/.config/tmux/tmux.conf \; display "tmux.conf перезагружен"

# ── Сплиты | и - в текущем каталоге ────────────────────
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# ── Навигация по панелям как в vim (h j k l) ───────────
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# ── Vi-режим копирования (v — выделить, y — копировать) ─
setw -g mode-keys vi
bind -T copy-mode-vi v send -X begin-selection
bind -T copy-mode-vi y send -X copy-selection-and-cancel

# ── Цвета (truecolor) ──────────────────────────────────
set -g default-terminal "tmux-256color"
set -ga terminal-overrides ",*256col*:Tc"

# ── Статус-бар ─────────────────────────────────────────
set -g status-interval 5
set -g status-right "#H  %Y-%m-%d %H:%M"
```

> [!warning] Применение конфига
> Конфиг читается при старте **сервера**. Если tmux уже запущен — либо `prefix r` (с привязкой выше), либо `tmux kill-server` и заново. Путь `~/.config/tmux/tmux.conf` понимают свежие версии; на старых — клади в `~/.tmux.conf`.

## 🔌 Плагины (TPM, опционально)

[TPM](https://github.com/tmux-plugins/tpm) — менеджер плагинов:

```bash
git clone https://github.com/tmux-plugins/tpm ~/.config/tmux/plugins/tpm
```

```bash
# в конце tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'   # сохранение/восстановление сессий
set -g @plugin 'tmux-plugins/tmux-continuum'   # автосейв сессий
run '~/.config/tmux/plugins/tpm/tpm'           # ВАЖНО: последней строкой
```

Установка плагинов внутри tmux — `prefix I` (заглавная).

## 💡 Когда полезно

- **Удалённая работа по SSH**: процессы переживают обрыв связи (главный кейс).
- **Вкладки/сплиты** для минималистичных терминалов ([Alacritty](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md), у которого их нет by design).
- Долгие задачи на сервере/роутере, которые нельзя прерывать.
- В [Rio](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) вкладки/сплиты есть свои, но **persist-сессии** через SSH всё равно даёт только tmux.

## 🔗 Ссылки

- Репозиторий: [github.com/tmux/tmux](https://github.com/tmux/tmux) · man: [man.openbsd.org/tmux](https://man.openbsd.org/tmux) · плагины: [github.com/tmux-plugins](https://github.com/tmux-plugins)
- Связанные: [Alacritty — GPU-терминал](Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) · [Rio — терминал на WebGPU](Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) · [kitty — kittens и графика](kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md) · [Konsole — терминал KDE](Konsole%20%E2%80%94%20терминал%20KDE%20%28профили%2C%20split-view%2C%20Qt%29.md) · [SSH — базовое руководство](../Network/SSH/SSH-Базовое%20руководство.md)

#Terminal #tmux #Linux #SSH
