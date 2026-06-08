---
создал заметку: 2026-06-08T20:00:00
author: WhiteK0T
tags:
  - NetWatch
  - Сеть
  - Rust
  - Безопасность
  - TUI
Источник:
  - https://github.com/matthart1983/netwatch
  - https://t.me/open_source_friend/5666
---

# 🛰️ NetWatch — сетевая форензика в терминале

**NetWatch** (автор — Matt Hart, лицензия **MIT**) — **TUI для сетевой форензики в реальном времени** на **Rust** (Linux и macOS). Делает глубокий разбор пакетов (deep packet inspection) на «живой» скорости, практически без конфигурации.

## ✨ Ключевые возможности

- **Расшифровка TLS 1.3** через `SSLKEYLOGFILE` — тот же механизм, что у Wireshark.
- **JA4/JA4Q-фингерпринтинг** — идентификация TLS/QUIC-клиентов.
- **17 декодеров протоколов L7** — TLS, QUIC, HTTP, DNS, SSH, MQTT, SNMP и др.
- **Атрибуция процессов на уровне ядра** через eBPF kprobes (с мягким фолбэком на `lsof`/PKTAP).
- **Сетевая аналитика угроз** — обнаружение сканов портов, beaconing, DNS-туннелей.
- **Flight Recorder** — захват «инцидент-бандлов» с контекстом для разбора.
- **Landlock-песочница** на Linux — ограничение доступа к ФС после инициализации.
- **Сборка TCP-потоков** и анализ таймингов рукопожатий.
- **9 вкладок:** dashboard, connections, packets, topology, timeline, processes, AI insights и др.

## 🧩 Требования

- **libpcap** — `sudo apt install libpcap-dev` (Linux; на macOS встроен).
- **Rust 1.70+** (для сборки из исходников).
- **Root / повышенные привилегии** — для захвата пакетов и eBPF.

## 📦 Установка

```bash
# Homebrew
brew install matthart1983/tap/netwatch

# Cargo
cargo install netwatch-tui

# Из исходников
git clone https://github.com/matthart1983/netwatch.git && cd netwatch
cargo build --release
```

Есть готовые бинарники: Linux (x86_64, aarch64, статические сборки) и macOS (Intel, Apple Silicon).

## 🚀 Запуск и режимы

```bash
netwatch          # ограниченный режим
sudo netwatch     # полный режим (health-пробы + захват пакетов)

netwatch --generate-config   # первичная настройка конфига
```

**Запуск без root на Linux** (через capabilities):

```bash
sudo setcap 'cap_net_raw,cap_bpf,cap_perfmon+eip' "$(which netwatch)"
netwatch
```

> [!note] После обновления бинарника
> `setcap` приходится **выдавать заново** — `cargo install` перезаписывает файл и сбрасывает capabilities.

**Расшифровка TLS 1.3** (ключи берутся из лога твоего же клиента):

```bash
SSLKEYLOGFILE=/tmp/sslkeylog.txt curl https://example.com
```

Если ключей нет — захват не ломается, такие записи просто остаются «непрозрачными».

## ⌨️ Навигация по TUI

| Клавиша | Действие |
| :--- | :--- |
| `1`–`9` | переключение вкладок (виды анализа) |
| `c` | старт/стоп захвата (вкладка Packets) |
| `/` | дисплей-фильтр (синтаксис в стиле Wireshark) |
| `s` | режимы просмотра потока (stream view) |
| `R` / `F` / `E` | Flight Recorder: arm / freeze / export bundle |
| `T` / `W` | traceroute / whois |
| `,` / `t` / `?` | настройки / смена темы / помощь |
| `q` | выход |

## 🔎 Дисплей-фильтры (вкладка Packets)

Поддерживаются протокол, IP, порт, текстовый поиск, L7-протокол (`app:tls`), SNI, JA4-фингерпринты и булевы комбинаторы:

```
tcp and port 443
app:tls
decrypted:true
ja4:t13d1516h2_8daaf6152771_b186095e22b6
```

## ⚠️ Заметки и оговорки

- **Мягкая деградация:** фичи, требующие привилегий, показывают понятное сообщение, а не падают.
- **Песочница** Landlock — только Linux; allow-list на чтение/запись после инициализации.
- **AI Insights** — опционально; локальный Ollama или облачные модели, ключи API в NetWatch не хранятся.
- **Темы:** 7 встроенных (Dark, Ocean, Solarized, Dracula, Nord, Sky, Paper) с мгновенным переключением.

## 🔗 Связанные проекты (того же автора)

- **SysWatch** и **DiskWatch** — мониторинг системы и дисков.
- **ESSH** — SSH-клиент на чистом Rust для параллельной удалённой диагностики.
- **NetWatch Cloud** — хостинговый флит-мониторинг (агент + дашборд).

#NetWatch #Сеть #Rust #Безопасность #TUI
