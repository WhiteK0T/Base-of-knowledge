---
создал заметку: 2026-02-22T21:38:00
author: WhiteK0T
tags:
  - SCP
  - Linux
---
### Что такое SCP

**SCP** (Secure Copy) — утилита командной строки для **безопасного копирования файлов** между машинами через **SSH**. Шифрует данные и использует SSH-аутентификацию.

### Основной синтаксис

```
scp [опции] источник назначение
```

**Формат путей:**

- Локальный: `/path/to/file`
- Удалённый: `user@host:path`

### Основные опции

| Опция      | Описание                      |
| :--------- | :---------------------------- |
| `-r`       | Рекурсивно (папки)            |
| `-P порт`  | SSH порт (по умолчанию 22)    |
| `-p`       | Сохранить время/права         |
| `-C`       | Сжатие                        |
| `-v`       | Подробный вывод               |
| `-l лимит` | Ограничение скорости (Кбит/с) |
| `-i ключ`  | SSH ключ                      |

### Примеры копирования

#### Локальный → Удалённый

```bash
# Файл
scp file.txt user@192.168.1.100:/home/user/

# Папка
scp -r myfolder/ user@server:/backup/

# С портом и сжатием
scp -P 2222 -C bigfile.iso user@server:/mnt/

# Сохранить права/время
scp -p config.conf root@vps:/etc/
```


#### Удалённый → Локальный

```bash
# Скачать файл
scp user@server:/var/log/syslog ./syslog.backup

# Скачать папку
scp -r user@server:/home/backup/ ./local_backup/
```

#### Между удалёнными серверами

```bash
scp user1@server1:/file.txt user2@server2:/destination/
```

### Продвинутые примеры

```bash
# Ограничить скорость (100 Кбит/с)
scp -l 100 bigfile.iso user@server:/tmp/

# С конкретным SSH ключом
scp -i ~/.ssh/id_rsa_work file.txt user@server:/home/

# Через Jump host
scp -o "ProxyJump=user@jump.host" file.txt user@target:/path/

# Verbose + прогресс + сжатие
scp -vCp file.tar.gz user@server:/backup/
```

### Практические сценарии

```bash
# Резервное копирование сайта
scp -rC /var/www/html/ user@backup:/backups/site-$(date +%Y%m%d)/

# Скачать все логи
scp -r user@server:/var/log/*.log ./logs/

# Перенести домашнюю папку
scp -rpC ~/* newuser@newserver:~/
```

### Сравнение с другими инструментами

| Команда | Шифрование | Рекурсия | Дельта | Скорость |
| :------ | :--------- | :------- | :----- | :------- |
| `cp`    | Нет        | Да       | Нет    | Локально |
| `scp`   | SSH        | `-r`     | Нет    | Средняя  |
| `rsync` | SSH        | `-r`     | Да     | Быстрая  |

### Полезные советы

- ✅ **Всегда проверяй**: `ssh user@host ls -la путь`
- ✅ **Для больших файлов**: используй `-C` (сжатие)
- ✅ **SSH ключи**: ускоряют работу без паролей
- ❌ **Для частых передач**: лучше `rsync -avz`

**SCP** — идеально для **одноразовых** безопасных передач файлов.

#Linux 
#SCP 