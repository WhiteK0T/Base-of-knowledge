---
создал заметку: 2026-06-08T18:05:00
author: WhiteK0T
tags:
  - Mutagen
  - Windows
  - Синхронизация
  - SSH
Источник:
  - https://github.com/mutagen-io/mutagen/releases
  - https://github.com/mutagen-io/scoop-mutagen
---

# 🪟 Установка и настройка Mutagen — Windows

Обзор и справочник команд — в [Mutagen](Mutagen.md). Здесь — установка под Windows.

## 1. Установка

**Через [Scoop](https://scoop.sh/) (рекомендуется):**

```powershell
scoop bucket add mutagen https://github.com/mutagen-io/scoop-mutagen
scoop install mutagen
```

**Или вручную:** скачать бинарник с [GitHub Releases](https://github.com/mutagen-io/mutagen/releases/latest) и добавить его в `PATH`.

> Mutagen ставится только на **локальную** машину. На сервер ничего ставить не нужно — агент доставляется по SSH.

## 2. Запуск демона

```powershell
mutagen daemon start
```

Автозапуск при входе в систему (один раз):

```powershell
mutagen daemon register
```

## 3. SSH-конфиг

Mutagen использует системный SSH (`~/.ssh/config`, на Windows — `C:\Users\<имя>\.ssh\config`). Пропиши хост:

```
Host my-server
    HostName 123.45.67.89
    User vova
    Port 2222
    IdentityFile ~/.ssh/my_server_key
```

Настройка ключей и SSH — см. [SSH-Ключи](../../Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md) и [SSH-Базовое руководство](../../Network/SSH/SSH-%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md).

## 4. Запуск синхронизации

```powershell
mutagen sync create --name=my-project `
  "C:\Users\vova\Projects\my-project" `
  "my-server:/home/vova/projects/my-project"
```

Или, если используешь проектный файл `mutagen.yml` (см. [Mutagen](Mutagen.md)), из папки с ним:

```powershell
mutagen project start
```

> [!tip] Права на папку сервера
> Если папку на сервере создавал `root`, а подключаешься обычным пользователем — Mutagen не сможет писать. Поправь владельца: `ssh my-server "sudo chown -R vova:vova /home/vova/projects"`.

#Mutagen #Windows #Синхронизация #SSH
