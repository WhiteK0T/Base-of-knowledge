---
author: WhiteK0T
создал заметку: 2026-02-06T20:45:00
tags:
  - Debian
  - Ubuntu
  - sid
  - stable
---
Нужно было  установить gcc-14.3, но в стандартной ветке был только 14.2, пришлось подключать тестовую ветку, так как не хотелось устанавливать руками и потом руками обновлять по мере необходимости.

Для стабильного Debian 13 (stable), но со свежим пакетом из Sid, используют APT pinning: база остаётся stable, а нужный пакет (gcc-14.3) берут из unstable/Sid.

#### 1. Включить репозитории stable + sid

Пример для Debian 13 (trixie) 
Подключаем sid репу вместе со стандартным репозиторием: 
```
# /etc/apt/sources.list
deb http://deb.debian.org/debian trixie main contrib non-free non-free-firmware 
deb http://deb.debian.org/debian sid main contrib non-free non-free-firmware
```

#### 2. Настраиваем приоритеты (APT pinning)

Создай `/etc/apt/preferences`:

```
Package: *
Pin: release a=stable
Pin-Priority: 700

Package: *
Pin: release a=unstable
Pin-Priority: 500
```

Так система по умолчанию всегда будет выбирать пакеты из stable, а из unstable что‑то возьмётся только если явно попросишь.

#### 3. Обновить индексы

`sudo apt update`

#### 4. Поставить только gcc-14.3 из Sid

Допустим, нужные пакеты в Sid называются `gcc-14`, `g++-14`, `gcc-14-base` (точные имена можно посмотреть на packages.debian.org для Sid). Тогда установка так:

```bash
sudo apt -t unstable install gcc-14 g++-14 gcc-14-base
```

Ключевые моменты:

- `-t unstable` говорит apt тянуть пакет (и его зависимости) именно из ветки Sid.    
- Остальная система остаётся на stable, потому что её приоритет выше и для обычного `apt upgrade` источником будет только stable.

[https://pkgs.org/download/gcc-14-base](https://pkgs.org/download/gcc-14-base)

#### 5. Не дать Sid «утащить» пол‑системы

Перед установкой удобно посмотреть, что именно будет обновлено:

```bash 
sudo apt -s -t unstable install gcc-14 g++-14 gcc-14-base
```

Опция `-s` делает «сухой прогон» без реальных изменений. Если список пакетов небольшой и основная масса остаётся из stable, можно выполнять команду без `-s`.

#Debian 
#Ubuntu 
#sid 
#stable 