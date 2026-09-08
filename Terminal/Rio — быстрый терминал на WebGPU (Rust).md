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
  - https://rioterm.com
  - https://rioterm.com/docs/config
  - https://rioterm.com/changelog
  - https://github.com/raphamorim/rio
  - https://github.com/gentoo/guru/tree/master/x11-terms/rio
  - https://itshaman.ru/news/software/rio-bystryi-terminal-s-podderzhkoi-webgpu-dlya-linux
---

# 🌊 Rio — быстрый GPU-терминал на Rust

**Rio** ([rioterm.com](https://rioterm.com), [github.com/raphamorim/rio](https://github.com/raphamorim/rio)) — кроссплатформенный аппаратно-ускоренный эмулятор терминала на **Rust**. Автор — Raphael Amorim, репозиторий создан 05.10.2022, первый релиз `v0.0.3` — 19.05.2023. От «голого» [Alacritty](Alacritty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D0%BD%D0%B0%20OpenGL%20%28%D0%BC%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D0%B8%D0%B7%D0%BC%29.md) отличается тем, что из коробки умеет **вкладки и сплиты**, оставаясь быстрым GPU-терминалом с текстовым конфигом.

> [!info] Состояние на 08.09.2026 (сверено по репозиторию)
> | | |
> | :--- | :--- |
> | Актуальный релиз | **v0.5.27** от 30.08.2026 |
> | Звёзд / форков / открытых issue | 7 468 · 344 · **294** |
> | Лицензия / язык | MIT · Rust |
> | Последний коммит | 08.09.2026 — разработка идёт очень активно |

## ⏱️ Если у тебя 0.4.4 — ты отстал на 31 релиз

`v0.4.4` вышел **12.05.2026**. Между ним и текущим `v0.5.27` — **31 стабильный релиз** за ~3,5 месяца. Обновляться стоит: в этот промежуток попали и крупные новые возможности, и починка вещей, которые в 0.4.4 просто сломаны.

> [!warning] Темп релизов — это и плюс, и минус
> Пример августа 2026: `0.5.9`, `0.5.10`, `0.5.11`, `0.5.12`, `0.5.13` вышли **за два дня** (4–5 августа). При этом в нумерации **пропущены** `0.4.8`, `0.5.4`, `0.5.6`, `0.5.7`, `0.5.17` — релизы отзывались. Плюс 294 открытых issue. Rio — быстро развивающийся проект, а не «поставил и забыл»: если нужна предсказуемость, [Alacritty](Alacritty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D0%BD%D0%B0%20OpenGL%20%28%D0%BC%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D0%B8%D0%B7%D0%BC%29.md) или [Konsole](Konsole%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20KDE%20%28%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D0%B8%2C%20split-view%2C%20Qt%29.md) спокойнее.

### Что появилось после 0.4.4

| Версия | Что важного |
| :--- | :--- |
| **0.4.11** (20.07) | Большой блок починок шрифтов: сброс кэшей глифов при смене шрифта (раньше после перезагрузки конфига оставалась старая метрика или падение), правильный выбор лица в `.ttc`-коллекциях, приоритет заданного bold над метаданными веса. Заработала и стала перезагружаться на лету `fonts.features`. Починены `ctrl+цифра` и `ctrl+знак` (Rio сам считает управляющий байт: `ctrl+6` → `0x1E`). `[bindings]` перезагружаются без перезапуска окна. Исправлен шрифт, менявшийся **на два шага** за нажатие |
| **0.4.12** (22.07) | **Quake-режим** — выпадающий терминал по системному хоткею. **Shell integration** через OSC 133 (семантические зоны промпта), OSC 1337 `SetUserVar`. Полностью восстановлены Sixel и iTerm2-картинки с корректным поведением в скроллбэке |
| **0.5.0** (27.07) | Ядро вынесено в отдельные библиотеки **`rio-vt`** (VT-конечный автомат без рендерера) и **`librio`** (C ABI для встраивания). Новые действия `ToggleQuake`, `ScrollToPrevPrompt`, `ScrollToNextPrompt`. Колесо мыши прокручивает одну строку за щелчок (раньше требовалось два). `scroll.multiplier`, `window.quake-*-percentage` |
| **0.5.3** (31.07) | **Ускорение движка ~2,7×** на обычном тексте (865 → 2305 МиБ/с), 3× на CJK и эмодзи (243 → 723 МиБ/с), 1,5× на перерисовке TUI. Измерено [rio-vt-benchmark](https://github.com/raphamorim/rio-vt-benchmark) |
| **0.5.5** (01.08) | Починен эхо-лаг ввода 150–200 мс в TUI с синхронизированным выводом (mode 2026) через Windows ConPTY |

> [!tip] Практический вывод для 0.4.4
> Если пользуешься лигатурами, Nerd Font, CJK-шрифтами или вариативными шрифтами — обновление обязательно: почти весь этот пласт починен только в **0.4.11**. Плюс `ctrl+цифра` в TUI-программах до 0.4.11 работал неправильно.

## 🧩 Чем рендерит — и почему «WebGPU» уже неточно

Исторически Rio продвигался как терминал на **WebGPU** (wgpu), и в старых версиях так и было. В 0.5.x архитектура изменилась. Из `sugarloaf/Cargo.toml` (v0.5.27):

```toml
# Pull in `wgpu` + the librashader filter chain. Required on Windows
# and WASM (no native backend yet); optional on Linux + macOS where
# the native Vulkan / Metal backends cover everything except the
# librashader CRT/scanline filters.
wgpu = [ "dep:wgpu", ... ]
```

А в `frontends/rioterm/Cargo.toml`:

```toml
[features]
default = ["wayland", "x11"]     # wgpu в default НЕ входит
```

То есть на Linux по умолчанию работает **нативный Vulkan**, а не wgpu; wgpu обязателен только для Windows и WASM. Перечень бэкендов в `rio-backend/src/config/renderer.rs` — всего три варианта:

```rust
pub enum Backend {
    #[cfg(target_os = "macos")] Metal,   // нативный Metal
    Vulkan,                              // нативный на Linux, wgpu-Vulkan в остальных случаях
    Webgpu,                              // «зонтик» wgpu: Metal/Vulkan/DX12/GL/WebGPU
}
```

> [!caution] Значений `Automatic`, `Dx12` и `GL` в конфиге **нет**
> Их часто приводят в старых статьях (и в предыдущей редакции этой заметки). Такого варианта не существует: умолчание задаётся атрибутом `#[cfg_attr(target_os = "linux", default)]` на `Vulkan`, а роль «выбери сам» играет `Webgpu`. Если написать `backend = "GL"`, значение просто не разберётся.

## ✨ Возможности

- **Вкладки и сплиты** (`navigation.mode`: `Tab` / `NativeTab` (только macOS) / `Plain`, `use-split`).
- **Quake-режим** — выпадающий терминал (с 0.4.12), действие `ToggleQuake`.
- **Shell integration** через OSC 133: прыжки по промптам `ScrollToPrevPrompt` / `ScrollToNextPrompt`.
- Лигатуры и тонкая настройка OpenType-фич: `fonts.features = ["-calt", "-liga"]` **выключает** лигатуры.
- Картинки: **Sixel**, протоколы **iTerm2** и **Kitty**.
- **Vi-режим**, поиск, палитра команд, прозрачность, размытие фона, фоновое изображение.
- **RetroArch/librashader-шейдеры** (CRT-фильтры) через `renderer.filters` — ⚠️ только в сборке с фичей `wgpu`, см. раздел про Gentoo.
- Экспериментальный **CPU-рендерер** `renderer.use-cpu` (tiny-skia) — без картинок, GPU-фильтров и скруглений.
- Горячая перезагрузка конфига, нативные ARM64-сборки.

## 📦 Установка

> [!danger] `apt install rio` установит НЕ ТОТ Rio
> В Debian и Ubuntu пакет с именем `rio` — это **`rio` версии 1.07**, *«Command line Diamond Rio MP3 player controller»*, утилита для MP3-плеера Diamond Rio конца 1990-х. Она лежит в `main`/`universe` во всех текущих выпусках (trixie `1.07-16`, Ubuntu questing/plucky `1.07-16`) и к терминалу отношения не имеет. Терминала Rio в репозиториях Debian/Ubuntu **нет вообще**.

```bash
# Arch — в ОФИЦИАЛЬНОМ репозитории extra (не AUR!)
sudo pacman -S rio                    # extra/rio 0.5.27-1

# Gentoo — оверлей GURU
eselect repository enable guru && emaint sync -r guru
emerge --ask x11-terms/rio            # rio-0.5.27, KEYWORDS="~amd64"

# Debian / Ubuntu — только .deb из релизов GitHub (пакет называется rioterm)
# выбери сборку под свою сессию: _wayland или _x11
wget https://github.com/raphamorim/rio/releases/download/v0.5.27/rioterm_0.5.27_amd64_wayland.deb
sudo apt install ./rioterm_0.5.27_amd64_wayland.deb

# Flatpak (любой дистрибутив с Flathub) — версия совпадает с апстримом
flatpak install flathub com.rioterm.Rio
```

> [!warning] В релизах — раздельные сборки под Wayland и X11
> Ассеты `v0.5.27` называются `rioterm_0.5.27_amd64_wayland.deb` / `..._amd64_x11.deb` (аналогично `.rpm` и `arm64`). Это **разные бинарники**, а не универсальный пакет: поставишь x11-сборку под Wayland — получишь работу через XWayland либо отказ старта. Имя пакета — **`rioterm`**, что заодно снимает конфликт с MP3-шным `rio`.

### Gentoo: чего не будет в сборке из GURU

Ебилд `rio-0.5.27.ebuild` собирает так:

```bash
RUST_MIN_VER="1.96.1"
IUSE="+wayland +X"
REQUIRED_USE="|| ( wayland X )"
KEYWORDS="~amd64"                     # arm64 в GURU не keyworded

src_configure() {
    local myfeatures=( $(usev wayland) $(usev X x11) )
    cargo_src_configure --verbose --no-default-features
}
```

Фичи — только `wayland` и `x11`. **`wgpu` не включается**, а в исходнике поле `filters` объявлено как

```rust
#[cfg(feature = "wgpu")]
pub filters: Vec<Filter>,
```

Значит в стандартной GURU-сборке **CRT/RetroArch-фильтры недоступны**, и `backend = "Webgpu"` тоже не даст wgpu-путь — остаётся нативный Vulkan (которого для обычной работы хватает с запасом). Нужны фильтры — собирай сам с `--features wgpu`. Крейты ебилд тянет отдельным архивом из `gentoo-crate-dist`, из сборочных зависимостей — `app-text/scdoc` (для man-страниц) и `dev-build/cmake`.

> [!danger] Не для роутера/Entware
> Rio — графическое приложение (Wayland/X11/Metal/DX), требует GPU и дисплея. На ASUS RT-AX56U (Entware, без графики) **неприменимо** — терминал ставится на десктоп, а к роутеру подключаешься по [SSH](../Network/SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md) уже из него.

## ⚙️ Конфиг (`~/.config/rio/config.toml`)

Формат — **TOML**. Linux/macOS — `~/.config/rio/config.toml` (или `$XDG_CONFIG_HOME/rio/`), Windows — `%USERPROFILE%\AppData\Local\rio\config.toml`. Путь переопределяется `RIO_CONFIG_HOME`. Изменения подхватываются **на лету**.

Секции верхнего уровня в 0.5.x: `adaptive-theme`, `colors`, `cursor`, `bell`, `developer`, `editor`, `effects`, `env-vars`, `fonts`, `hints`, `keyboard`, `navigation`, `option-as-alt`, `padding`, `panel`, `platform`, `renderer`, `scroll`, `shell`, `theme`, `title`, `window`, `working-dir`.

```toml
# ── Общее ──────────────────────────────────────────────
confirm-before-quit = true
copy-on-select = false
line-height = 1.0                # умолчание
padding = [10]
scrollback-history-limit = 10000 # умолчание
theme = "dracula"                # умолчание — "" (без темы); темы в ~/.config/rio/themes/

# ── Окно ───────────────────────────────────────────────
[window]
width = 800                      # умолчания: 800 × 490
height = 490
mode = "Windowed"                # Windowed | Maximized | Fullscreen
opacity = 1.0                    # умолчание 1.0
blur = true                      # bool ИЛИ "MacosGlassRegular" / "MacosGlassClear"
decorations = "Enabled"          # Enabled | Disabled | Transparent | Buttonless
quake-width-percentage = 100     # размеры выпадающего терминала
quake-height-percentage = 40

# ── Рендер ─────────────────────────────────────────────
[renderer]
backend = "Vulkan"               # Vulkan | Webgpu | Metal (macOS). Умолчание на Linux — Vulkan
strategy = "events"              # events (умолчание, экономно) | game (макс. плавность)
disable-occluded-render = true
disable-unfocused-render = false
use-cpu = false                  # экспериментальный CPU-рендерер (tiny-skia)

# ── Шрифты ─────────────────────────────────────────────
[fonts]
size = 14                        # умолчание
family = "JetBrains Mono"
features = ["-calt", "-liga"]    # минус выключает фичу: так гасятся лигатуры
hinting = true

[fonts.bold]
family = "JetBrains Mono"
weight = 600                     # вернули в 0.4.11; пинит ось wght у вариативных шрифтов

# ── Прокрутка ──────────────────────────────────────────
[scroll]
multiplier = 3.0

# ── Цвета (если не используешь theme) ──────────────────
[colors]
background = '#1e1e2e'
foreground = '#cdd6f4'
cursor = '#f5e0dc'

# ── Курсор ─────────────────────────────────────────────
[cursor]
shape = "block"                  # block | underline | beam
blinking = false                 # умолчание

# ── Навигация: вкладки/сплиты ──────────────────────────
[navigation]
mode = "Tab"                     # Tab | NativeTab (только macOS) | Plain
use-split = true
hide-if-single = true
unfocused-split-opacity = 0.7

# ── Оболочка ───────────────────────────────────────────
[shell]
program = "/bin/bash"
args = ["--login"]               # умолчание на Unix
```

> [!tip] Бэкенд рендера
> Оставляй `backend` незаданным — на Linux это уже `Vulkan`. Если видишь артефакты, пробуй `"Webgpu"`: он перебирает доступные API через wgpu — **но только если сборка собрана с фичей `wgpu`** (GURU-сборка — нет). На совсем старом железе без Vulkan остаётся экспериментальный `use-cpu = true`. `strategy = "game"` даёт максимально плавную прокрутку ценой нагрузки на GPU.

## ⌨️ Горячие клавиши по умолчанию (Linux, v0.5.27)

Сверено по `frontends/rioterm/src/bindings/mod.rs`, блок `#[cfg(not(any(target_os = "macos", target_os = "windows", test)))]`.

| Сочетание | Действие |
| :--- | :--- |
| `Ctrl+Shift+C` / `V` | копировать / вставить (`Shift+Insert` — вставка выделения) |
| `Ctrl+Shift+T` | новая вкладка |
| `Ctrl+Tab` / `Ctrl+Shift+Tab` | следующая / предыдущая вкладка |
| `Ctrl+Shift+W` | закрыть **сплит, а если его нет — вкладку** (`CloseCurrentSplitOrTab`) |
| `Ctrl+Shift+N` | новое окно |
| `Ctrl+Shift+R` | сплит вправо |
| `Ctrl+Shift+D` | сплит вниз |
| `Ctrl+Shift+[` / `]` | предыдущий / следующий **сплит** — и они же на вкладки, см. ниже |
| `Ctrl+Shift+Alt+←↑↓→` | двигать разделитель сплита |
| `Ctrl+=` / `Ctrl+-` / `Ctrl+0` | шрифт +/−/сброс |
| `Ctrl+Shift+F` / `B` | поиск вперёд / назад |
| `Ctrl+Shift+P` | палитра команд |
| `Ctrl+Shift+,` | открыть конфиг |

> [!caution] Двух вещей из старых шпаргалок на Linux нет
> - **`Ctrl+Shift+1…9` для перехода к вкладке не существует.** Привязки `Action::SelectTab(0..7)` и `SelectLastTab` объявлены только в блоке `#[cfg(all(target_os = "macos", ...))]` и висят на `Cmd+1…9`. На Linux переключение — `Ctrl+Tab` или `Ctrl+Shift+[`/`]`.
> - **`Ctrl+Shift+[` / `]` перегружены.** При `use-split = true` эти же сочетания навешиваются и на переключение сплитов, и на переключение вкладок. Если поведение кажется странным — переопредели их в `[bindings]` (с 0.4.11 они перезагружаются на лету, а неизвестное действие теперь отвергается с ошибкой, а не молча снимает привязку).

## ✅ Проверка утверждений

| Утверждение | Вердикт | Пояснение |
| :--- | :--- | :--- |
| «Rio рендерит через WebGPU» | ⚠️ Уже неточно | В 0.5.x на Linux по умолчанию **нативный Vulkan**; `wgpu` не входит в `default` фич и обязателен лишь для Windows/WASM |
| «`backend` умеет `Automatic` / `GL` / `Dx12`» | ❌ Нет | В `enum Backend` ровно три варианта: `Metal`, `Vulkan`, `Webgpu` |
| «Rio ставится из AUR: `yay -S rio`» | ❌ Устарело | Он в **официальном `extra`**: `pacman -S rio` (0.5.27-1). В AUR из подходящего только заброшенный `rio-git` 0.2.12 |
| «В Debian/Ubuntu пакета нет» | ✅ Терминала нет | Но пакет `rio` там **есть** — это MP3-контроллер Diamond Rio 1.07. Ставить надо `.deb` с именем `rioterm` |
| «CRT-фильтры работают везде» | ❌ Не в Gentoo | `filters` объявлено под `#[cfg(feature = "wgpu")]`, а ебилд GURU собирает без этой фичи |
| «`Ctrl+Shift+1…9` — переход к вкладке» | ❌ Только macOS | На Linux таких привязок в исходнике нет |
| «Свежая версия — 0.4.x» | ❌ Нет | 0.4.4 — от 12.05.2026; актуальна **0.5.27** от 30.08.2026, между ними 31 релиз |
| «Обновление 0.4.4 → 0.5.x даёт прирост скорости» | ✅ Да | 0.5.3: парсинг обычного текста 865 → 2305 МиБ/с (~2,7×), CJK и эмодзи 243 → 723 МиБ/с |
| «Проект стабильный и зрелый» | ⚠️ Спорно | 294 открытых issue, 31 релиз за 3,5 месяца, пять пропущенных (отозванных) номеров версий |

## ⚖️ Сравнение терминалов

| | Rio | [Alacritty](Alacritty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D0%BD%D0%B0%20OpenGL%20%28%D0%BC%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D0%B8%D0%B7%D0%BC%29.md) | [kitty](kitty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D1%81%20kittens%20%D0%B8%20%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%BE%D0%B9%20%28OpenGL%29.md) | [Konsole](Konsole%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20KDE%20%28%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D0%B8%2C%20split-view%2C%20Qt%29.md) |
| :--- | :--- | :--- | :--- | :--- |
| Рендер | Vulkan / Metal нативно, wgpu опционально | OpenGL | OpenGL | Qt (CPU) |
| Вкладки/сплиты | да | нет | да | да |
| Quake-режим | да (с 0.4.12) | нет | нет | да (KDE) |
| Картинки | Kitty/iTerm2/Sixel | нет | свой протокол + Sixel | нет |
| Shell integration | OSC 133 (с 0.4.12) | нет | да | частично |
| Настройка | TOML-конфиг | TOML-конфиг | конфиг | GUI/профили |
| Скриптинг/расширения | `librio` (C ABI) | — | kittens + remote | D-Bus / KPart |
| Windows | нативно | нативно | только WSL | нет |
| Язык / лицензия | Rust / MIT | Rust / Apache-MIT | Python+C+Go / GPL-3 | C++/Qt / GPL-2 |

## 💡 Когда выбирать

- Нужен **GPU-терминал со вкладками, сплитами, quake-режимом и картинками** из коробки, без tmux.
- Готов жить с быстрым темпом релизов и обновляться — взамен получаешь заметный прирост скорости 0.5.x.
- Нужен **предельный минимализм и стабильность** — [Alacritty](Alacritty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D0%BD%D0%B0%20OpenGL%20%28%D0%BC%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D0%B8%D0%B7%D0%BC%29.md); нужен зрелый скриптинг — [kitty](kitty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D1%81%20kittens%20%D0%B8%20%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%BE%D0%B9%20%28OpenGL%29.md).
- Сессии, переживающие обрыв SSH, ни один из них не даёт — это [tmux](tmux%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8%D0%BF%D0%BB%D0%B5%D0%BA%D1%81%D0%BE%D1%80%20%28%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B8%2C%20%D0%BE%D0%BA%D0%BD%D0%B0%2C%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D0%B8%29.md).

## 🔗 Ссылки

- Сайт/доки: [rioterm.com](https://rioterm.com) · [docs/config](https://rioterm.com/docs/config) · [changelog](https://rioterm.com/changelog) · репозиторий: [github.com/raphamorim/rio](https://github.com/raphamorim/rio)
- Пакеты: [Arch extra/rio](https://archlinux.org/packages/extra/x86_64/rio/) · [GURU x11-terms/rio](https://github.com/gentoo/guru/tree/master/x11-terms/rio) · [Flathub com.rioterm.Rio](https://flathub.org/apps/com.rioterm.Rio)
- Обзор: [itshaman.ru](https://itshaman.ru/news/software/rio-bystryi-terminal-s-podderzhkoi-webgpu-dlya-linux)
- Связанные: [Alacritty — GPU-терминал](Alacritty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D0%BD%D0%B0%20OpenGL%20%28%D0%BC%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D0%B8%D0%B7%D0%BC%29.md) · [kitty — kittens и графика](kitty%20%E2%80%94%20GPU-%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20%D1%81%20kittens%20%D0%B8%20%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%BE%D0%B9%20%28OpenGL%29.md) · [Konsole — терминал KDE](Konsole%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%20KDE%20%28%D0%BF%D1%80%D0%BE%D1%84%D0%B8%D0%BB%D0%B8%2C%20split-view%2C%20Qt%29.md) · [tmux — мультиплексор](tmux%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8%D0%BF%D0%BB%D0%B5%D0%BA%D1%81%D0%BE%D1%80%20%28%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B8%2C%20%D0%BE%D0%BA%D0%BD%D0%B0%2C%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D0%B8%29.md) · [SSH — базовое руководство](../Network/SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md)

#Terminal #Rio #WebGPU #Rust #Linux
