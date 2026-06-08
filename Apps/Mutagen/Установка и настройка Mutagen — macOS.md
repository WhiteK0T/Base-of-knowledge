---
создал заметку: 2026-06-08T18:07:00
author: WhiteK0T
tags:
  - Mutagen
  - macOS
  - Синхронизация
  - SSH
Источник:
  - https://mutagen.io/documentation/introduction/installation
  - https://github.com/mutagen-io/mutagen/releases
---

# 🍎 Установка и настройка Mutagen — macOS

Обзор и справочник команд — в [Mutagen](Mutagen.md). Здесь — установка под macOS.

## 1. Установка

**Через [Homebrew](https://brew.sh/) (рекомендуется):**

```bash
brew install mutagen-io/mutagen/mutagen
```

(Пре-релизные каналы: `mutagen-beta` — стабильный RC, `mutagen-edge` — ночные сборки.)

**Или вручную:** скачать бинарник с [GitHub Releases](https://github.com/mutagen-io/mutagen/releases/latest) и добавить в `PATH`.

> Mutagen ставится только на **локальную** машину. На сервер ничего ставить не нужно — агент доставляется по SSH.

## 2. Запуск демона

```bash
mutagen daemon start
```

Автозапуск при включении Mac (один раз):

```bash
mutagen daemon register
```

## 3. SSH-конфиг

Mutagen использует системный SSH (`~/.ssh/config`). Пропиши хост:

```
Host my-server
    HostName 123.45.67.89
    User vova
    Port 2222
    IdentityFile ~/.ssh/my_server_key
```

Настройка ключей и SSH — см. [SSH-Ключи](../../Linux/Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md) и [SSH-Базовое руководство](../../Linux/Network/SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md).

## 4. Запуск синхронизации

```bash
mutagen sync create --name=my-project \
  ~/Projects/my-project \
  my-server:/home/vova/projects/my-project
```

Или, если используешь проектный файл `mutagen.yml` (см. [Mutagen](Mutagen.md)), из папки с ним:

```bash
mutagen project start
```

> [!tip] Права на папку сервера
> Если папку на сервере создавал `root`, а подключаешься обычным пользователем — Mutagen не сможет писать. Поправь владельца: `ssh my-server "sudo chown -R vova:vova /home/vova/projects"`.

> [!tip] После перезагрузки Mac синхронизация не идёт
> Запусти демон `mutagen daemon start` или настрой автозапуск `mutagen daemon register`.

#Mutagen #macOS #Синхронизация #SSH
