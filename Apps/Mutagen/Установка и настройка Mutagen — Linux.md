---
создал заметку: 2026-06-08T18:06:00
author: WhiteK0T
tags:
  - Mutagen
  - Linux
  - Синхронизация
  - SSH
Источник:
  - https://github.com/mutagen-io/mutagen/releases
  - https://mutagen.io/documentation/introduction/installation
---

# 🐧 Установка и настройка Mutagen — Linux

Обзор и справочник команд — в [Mutagen](Mutagen.md). Здесь — установка под Linux.

## 1. Установка

**Через Homebrew (Linuxbrew):**

```bash
brew install mutagen-io/mutagen/mutagen
```

**Или вручную (бинарник):** официального пакета в apt/dnf нет, поэтому проще скачать релиз и положить в `PATH`:

```bash
# подставь актуальную версию и архитектуру с https://github.com/mutagen-io/mutagen/releases/latest
curl -LO https://github.com/mutagen-io/mutagen/releases/latest/download/mutagen_linux_amd64_vX.Y.Z.tar.gz
tar -xzf mutagen_linux_amd64_*.tar.gz
sudo mv mutagen /usr/local/bin/
mutagen version
```

> Mutagen ставится только на **локальную** машину. На сервер ничего ставить не нужно — агент доставляется по SSH.

## 2. Запуск демона

```bash
mutagen daemon start
```

Автозапуск при входе в систему (один раз):

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

#Mutagen #Linux #Синхронизация #SSH
