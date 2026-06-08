---
создал заметку: 2026-06-06T12:00:00
author: WhiteK0T
tags:
  - Samba
  - Linux
  - Network
  - CheatSheet
---

# Полное руководство по настройке Samba (smb.conf) в Linux

Данное руководство охватывает настройку файлового сервера Samba для расшаривания целого диска (`/mnt/dat1T/`) и отдельной папки на другом диске (`/mnt/dat500/BOOK/`). Включает специфику для **Gentoo Linux** (Portage и OpenRC).

---

## 1. Установка Samba

```bash
# Debian / Ubuntu / Astra Linux
sudo apt update && sudo apt install samba samba-common-bin

# RHEL / CentOS / Fedora / AlmaLinux
sudo dnf install samba samba-client

# Arch Linux / Manjaro
sudo pacman -S samba

# Gentoo Linux
# 1. Настроим USE-флаги (ACL для прав, zeroconf для обнаружения в сети)
echo "net-fs/samba acl client zeroconf" | sudo tee -a /etc/portage/package.use/samba
# 2. Установка
sudo emerge --ask net-fs/samba
```

---

## 2. Права на файловую систему

До правки конфига убедитесь, что у пользователя Samba есть доступ к путям на уровне файловой системы (ext4, xfs, btrfs и т.д.).

```bash
# Вариант A — через группу (рекомендуется для гибкости)
sudo groupadd sambashare
sudo usermod -aG sambashare $USER
sudo chown -R root:sambashare /mnt/dat1T /mnt/dat500/BOOK
sudo chmod -R 2775 /mnt/dat1T /mnt/dat500/BOOK

# Вариант B — если один владелец
sudo chown -R youruser:youruser /mnt/dat1T /mnt/dat500/BOOK
sudo chmod -R 0755 /mnt/dat1T /mnt/dat500/BOOK
```

> **Важно:** Родительские каталоги `/mnt` и `/mnt/dat500` должны быть как минимум `o+x` (выполнимы для других), иначе Samba не сможет "дойти" до вложенной папки `BOOK`. Проверить можно командой `namei -l /mnt/dat500/BOOK`.

---

## 3. Бэкап и редактирование smb.conf

```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
sudo nano /etc/samba/smb.conf
```

### Рабочий пример `/etc/samba/smb.conf`

```ini
[global]
    workgroup = WORKGROUP
    server string = Linux File Server
    server role = standalone server

    # Логи
    log file = /var/log/samba/log.%m
    max log size = 1000
    logging = file
    log level = 1               # 0 — тихо, 3+ — подробно для отладки

    # Безопасность и протоколы
    security = user
    map to guest = Bad User
    min protocol = SMB2
    max protocol = SMB3

    # Ограничение доступа (второй рубеж после firewall)
    hosts allow = 192.168.1.0/24 127.0.0.1
    hosts deny = 0.0.0.0/0
    interfaces = lo eth0        # слушать только LAN-интерфейс, не весь мир
    bind interfaces only = yes

    # Производительность
    socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=65536 SO_SNDBUF=65536
    read raw = yes
    write raw = yes
    strict locking = no

    # Кодировка
    unix charset = UTF-8
    dos charset = CP866

    # Отключение принтеров
    load printers = no
    printing = bsd
    printcap name = /dev/null
    disable spoolss = yes

# =========================================================
# Шара 1: весь диск /mnt/dat1T
# =========================================================
[Data1T]
    comment = 1TB Data Disk
    path = /mnt/dat1T
    browseable = yes
    read only = no
    writable = yes
    guest ok = no
    valid users = youruser admin
    force user = youruser
    force group = sambashare
    create mask = 0664
    directory mask = 2775
    force create mode = 0664
    force directory mode = 2775
    hide dot files = yes
    veto files = /Thumbs.db/.DS_Store/._*/
    delete veto files = yes

# =========================================================
# Шара 2: папка BOOK на втором диске
# =========================================================
[Books]
    comment = Books Library
    path = /mnt/dat500/BOOK
    browseable = yes
    read only = no
    writable = yes
    # yes — если нужен публичный доступ без пароля
    guest ok = yes
    guest only = no
    valid users = youruser admin
    force user = youruser
    force group = sambashare
    create mask = 0664
    directory mask = 2775
    force create mode = 0664
    force directory mode = 2775
    veto files = /Thumbs.db/.DS_Store/._*/
    delete veto files = yes
```

**Обязательно замените** `youruser` на имя вашего реального Linux-пользователя.

### Краткое пояснение ключевых опций

| Параметр | Назначение |
|---|---|
| `security = user` | Аутентификация по логину/паролю. |
| `min protocol = SMB2` | Отключаем устаревший и небезопасный SMB1. |
| `valid users` | Список допущенных пользователей. |
| `force user / force group` | Все файлы создаются от указанного UID/GID. Избавляет от проблем с правами ("Access denied" при удалении чужих файлов). |
| `create mask / directory mask` | Права по умолчанию на новые файлы/каталоги. |
| `veto files` | Блокируем создание мусорных файлов Windows/macOS. |
| `map to guest = Bad User` | Неверный логин → гостевой доступ (работает, если у шары `guest ok = yes`). |

---

## 4. Создание Samba-пользователя

Пользователь Samba **не равен** системному — его пароль хранится в отдельной базе (`passdb.tdb`). Системный пользователь с таким именем уже должен существовать.

```bash
# Добавить пользователя в базу Samba и задать пароль
sudo smbpasswd -a youruser

# Активировать пользователя
sudo smbpasswd -e youruser
```

Проверка списка пользователей Samba:
```bash
sudo pdbedit -L
```

---

## 5. Проверка конфига и управление службой

### 5.1. Проверка синтаксиса (обязательно для всех дистрибутивов)
```bash
testparm -s
```
*Если `testparm` не выдал ошибок, можно перезапускать службу.*

### 5.2. Перезапуск и автозагрузка

**Для Gentoo (OpenRC — стандартная система инициализации):**
```bash
# Добавляем в автозагрузку
sudo rc-update add samba default

# Перезапускаем (скрипт samba в OpenRC сам запустит и smbd, и nmbd)
sudo rc-service samba restart
```

**Для Gentoo (если используется профиль systemd) / Debian / Ubuntu / Arch:**
```bash
sudo systemctl enable --now smbd nmbd
sudo systemctl restart smbd nmbd
```

**Для RHEL / CentOS / Fedora:**
```bash
sudo systemctl enable --now smb nmb
sudo systemctl restart smb nmb
```

### 5.3. Перечитать конфиг без рестарта

После правки `smb.conf` не обязательно перезапускать службу и рвать активные сессии — Samba перечитает конфиг сама:
```bash
sudo smbcontrol all reload-config
```

---

## 6. Настройка Firewall (Межсетевой экран)

Samba использует порты: TCP 139, 445 и UDP 137, 138.

```bash
# UFW (Ubuntu/Debian/Gentoo)
sudo ufw allow samba
# или явно: sudo ufw allow 139,445/tcp && sudo ufw allow 137,138/udp

# firewalld (RHEL/Fedora/CentOS)
sudo firewall-cmd --permanent --add-service=samba
sudo firewall-cmd --reload

# iptables (Gentoo / классический Linux)
sudo iptables -A INPUT -p tcp -m multiport --dports 139,445 -j ACCEPT
sudo iptables -A INPUT -p udp -m multiport --dports 137,138 -j ACCEPT
# Не забудьте сохранить правила (например, через iptables-save или rc-service iptables save)
```

---

## 7. Проверка с клиента

**С Linux-машины:**
```bash
# Посмотреть список шар
smbclient -L //IP_СЕРВЕРА -U youruser

# Смонтировать диск (пароль спросит интерактивно)
sudo mount -t cifs //IP_СЕРВЕРА/Data1T /mnt/test -o username=youruser,uid=1000,gid=1000
```

#### Постоянное монтирование (credentials-файл + fstab)

Хранить пароль в команде `mount` небезопасно — он светится в `history` и `ps`. Правильнее вынести его в файл с правами `600`:
```bash
# /root/.smbcreds
username=youruser
password=ВАШ_ПАРОЛЬ
```
```bash
sudo chmod 600 /root/.smbcreds
```
Затем строка в `/etc/fstab` — шара поднимется автоматически при загрузке:
```bash
//IP_СЕРВЕРА/Data1T  /mnt/test  cifs  credentials=/root/.smbcreds,uid=1000,gid=1000,iocharset=utf8,_netdev  0  0
```
Опция `_netdev` откладывает монтирование до поднятия сети. Проверить: `sudo mount -a`.

**С Windows:**
Откройте проводник и введите в адресную строку:
`\\IP_СЕРВЕРА\Data1T` и `\\IP_СЕРВЕРА\Books`

Либо подключить сетевой диск из командной строки (буква `Z:`, переподключение после перезагрузки):
```bat
net use Z: \\IP_СЕРВЕРА\Data1T /user:youruser /persistent:yes
```

**С macOS:**
В Finder: `Cmd + K` -> `smb://IP_СЕРВЕРА/Data1T`

---

## 8. Частые проблемы и решения

> **Диагностика:** кто сейчас подключён, какие шары открыты и какие файлы заблокированы — покажет `smbstatus` (`smbstatus -b` — только сессии, `smbstatus -L` — только локи). Первое, что стоит смотреть при «файл занят» и проблемах доступа.

### 1. «Access denied» при записи или удалении файлов
*   **Причина:** Не хватает прав на уровне файловой системы Linux.
*   **Решение:** Проверьте вывод `namei -l /mnt/dat500/BOOK`. Убедитесь, что параметры `force user` и `force group` в `smb.conf` указаны верно, а у пользователя есть права на запись в сам каталог (`chmod 2775`).

### 2. SELinux блокирует доступ (RHEL / Fedora / AlmaLinux)
Если включен SELinux (проверить: `sestatus`), он запретит Samba читать произвольные директории.
```bash
sudo semanage fcontext -a -t samba_share_t "/mnt/dat1T(/.*)?"
sudo semanage fcontext -a -t samba_share_t "/mnt/dat500/BOOK(/.*)?"
sudo restorecon -Rv /mnt/dat1T /mnt/dat500/BOOK
```

### 3. AppArmor блокирует доступ (Ubuntu / Debian)
Встречается редко, но если в логах (`/var/log/samba/log.smbd`) есть ошибки `apparmor="DENIED"`:
```bash
sudo aa-complain /etc/apparmor.d/usr.sbin.smbd
# или добавить пути в /etc/apparmor.d/local/usr.sbin.smbd
```

### 4. Сервер не виден в "Сетевом окружении" Windows
*   **Причина:** Не работает служба NetBIOS или закрыт UDP 137/138.
*   **Решение:** Убедитесь, что `nmbd` запущен. В современных Windows 10/11 обнаружение по SMB1 отключено в целях безопасности. **Правильный способ:** подключаться напрямую по IP (`\\192.168.1.10`) или добавить запись в локальный DNS/файл `hosts`.
*   *Альтернатива:* Установить Avahi (mDNS/Bonjour), чтобы сервер был виден как `servername.local`.

### 5. Низкая скорость передачи по сети
Добавьте в секцию `[global]` следующие параметры для оптимизации асинхронного ввода-вывода:
```ini
    aio read size = 1
    aio write size = 1
    use sendfile = yes
    server signing = disabled
```
*(Примечание: `server signing = disabled` немного снижает безопасность, но значительно повышает скорость на гигабитных и быстрее сетях).*

Если на сервере и клиенте по несколько сетевых карт — включите агрегацию каналов SMB3 (трафик пойдёт по всем линкам сразу):
```ini
    server multi channel support = yes
```

---

## 9. Дополнительно: vfs-модули

Модули `vfs objects` подключаются **в секции конкретной шары**. Если их несколько — перечисляются в одной строке через пробел (порядок важен), например: `vfs objects = catia fruit streams_xattr recycle`.

### 9.1. Совместимость с macOS (vfs_fruit)

Без этого Finder криво работает с ресурс-форками, спотлайт-индексами и плодит `.DS_Store`/`._*`-файлы. Добавьте в шару, к которой ходят с Mac:
```ini
    vfs objects = catia fruit streams_xattr
    fruit:metadata = stream
    fruit:posix_rename = yes
    fruit:veto_appledouble = no
```

### 9.2. Корзина (vfs_recycle)

Удалённые по сети файлы уходят в скрытую папку `.recycle` внутри шары, а не пропадают безвозвратно — спасает от случайного удаления:
```ini
    vfs objects = recycle
    recycle:repository = .recycle
    recycle:keeptree = yes          # сохранять структуру каталогов
    recycle:versions = yes          # не затирать одноимённые, а нумеровать
    recycle:exclude = *.tmp *.temp
    recycle:exclude_dir = /tmp /cache
```
Периодически чистите `.recycle` — Samba сама её не опустошает.

---

Подробнее про правила firewall — в заметке [IPTables](IPTables.md).

#Samba
#Linux
#Network
#CheatSheet