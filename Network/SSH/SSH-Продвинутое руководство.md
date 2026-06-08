---
создал заметку: 2026-06-05T14:05:00
author: WhiteK0T
tags:
  - SSH
  - Linux
  - Network
  - Security
Источник:
  - https://habr.com/ru/articles/435546/
  - https://wiki.merionet.ru/
---

# SSH — Продвинутое руководство

Туннели, проброс портов, SOCKS-прокси, VPN поверх SSH, прыжки по хостам, мультиплексирование и прочие приёмы для сетевых инженеров и специалистов по безопасности. Основы — в [SSH — Базовое руководство](SSH-Базовое%20руководство.md); про ключи — [SSH-Ключи](SSH-Ключи.md).

> [!warning] Предупреждение безопасности
> Туннели и SOCKS-прокси могут открыть внутренние сетевые ресурсы ненадёжным сетям (вплоть до интернета). Всегда понимайте, что именно слушает листенер и к чему у него есть доступ.

## Проброс портов и туннели

> [!tip] Наглядно
> Схемы всех видов проброса (локальный, удалённый, bastion, домашняя сеть) с воспроизводимыми лабами — в [Визуальном руководстве по туннелям SSH](SSH-Визуальное%20руководство%20по%20туннелям.md).

### Локальная переадресация (-L)

Открывает порт на **локальной** машине, подключённый к порту на удалённой стороне туннеля:

```bash
localhost:~$ ssh -L 9999:127.0.0.1:80 user@remoteserver
```

`-L` — «локальная сторона прослушивания»: порт 9999 на localhost переадресуется на порт 80, причём `127.0.0.1` здесь — localhost **удалённого** сервера. Чтобы листенер был доступен другим узлам локальной сети:

```bash
localhost:~$ ssh -L 0.0.0.0:9999:127.0.0.1:80 user@remoteserver
```

### Туннель на сторонний (третий) хост

```bash
localhost:~$ ssh -L 0.0.0.0:9999:10.10.10.10:80 user@remoteserver
```

Трафик от `remoteserver` к `10.10.10.10` **уже не в SSH-туннеле**; для веб-сервера на `10.10.10.10` источником запросов будет `remoteserver`.

### Обратный туннель (-R)

Прослушивающий порт открывается на **удалённом** сервере и подключается обратно к локальному порту:

```bash
localhost:~$ ssh -R 0.0.0.0:1999:127.0.0.1:902 user@remoteserver
```

Соединение с порта 1999 на `remoteserver` идёт к порту 902 на нашем клиенте.

### Динамическая переадресация — SOCKS-прокси (-D)

`ssh` работает как SOCKS-прокси: трафик идёт через диапазон портов удалённого сервера. В логах целевых систем источником будет удалённый сервер.

```bash
localhost:~$ ssh -D 8888 user@remoteserver
localhost:~$ netstat -pan | grep 8888     # проверка листенера
```

По умолчанию слушается только `127.0.0.1`. Чтобы открыть всем интерфейсам:

```bash
localhost:~$ ssh -D 0.0.0.0:8888 user@remoteserver
```

Настройка клиентов:
- **Firefox:** Настройки → Основные → Параметры сети → указать IP и порт SOCKS. Включите «DNS-запросы через прокси», чтобы и резолвинг шёл через туннель.
- **Chrome:** `google-chrome --proxy-server="socks5://192.168.1.10:8888"`
- **Прочие приложения:** через `proxychains` (например, RDP): `proxychains rdesktop $RemoteWindowsServer`.

> Проверяйте `tcpdump`-ом, что DNS-запросы действительно уходят в туннель, а не светятся в открытой сети.

### Обратный SOCKS-прокси (-R без целевого порта)

SOCKS-прокси слушает на удалённом конце; подключения к нему выходят из туннеля как трафик с нашего localhost:

```bash
localhost:~$ ssh -R 0.0.0.0:1999 user@remoteserver
```

### Просмотр активных туннелей

```bash
lsof -i | egrep 'ssh'        # активные ssh-подключения
lsof -i -n | egrep 'ssh'     # с IP вместо имён хостов (-n)
```

### Диагностика и ограничение

Если удалённые туннели не работают, проверьте `netstat`, к каким интерфейсам привязан листенер. Даже при `0.0.0.0` листенер привяжется только к `127.0.0.1`, если в `sshd_config` стоит `GatewayPorts no`.

Ограничение проброса портов на сервере (`/etc/ssh/sshd_config`):

```bash
# Разрешить переадресацию только на указанные адреса
PermitOpen host:port
PermitOpen IPv4_addr:port
PermitOpen [IPv6_addr]:port

# Управление переадресацией в целом
AllowTCPForwarding yes      # по умолчанию
AllowTCPForwarding no       # запретить весь проброс портов
AllowTCPForwarding local    # только локальный
AllowTCPForwarding remote   # только удалённый
```

### Изменение проброса на лету (escape-последовательности)

В рамках живой сессии можно менять переадресацию. Нажмите `Enter`, затем `~C` — откроется консоль `ssh>`:

```
localhost:~$ ~C
ssh> -L 1445:remote-win2k3:445   # добавить локальный проброс
Forwarding port.
```

Доступны `-L`/`-R`/`-D` для добавления и `-KL`/`-KR`/`-KD` для отмены. (`~.` — принудительно разорвать зависшую сессию, `~?` — список escape-команд.)

## VPN поверх SSH

Полноценный VPN через `tun`-интерфейсы (уровень 3) снимает ограничения SOCKS-прокси и `proxychains`, которые не умеют работать с сырыми сокетами (например, не выйдет `nmap -sS`). Подключение опускается до **уровня 3** с обычной маршрутизацией. Нужны **права root с обеих сторон**.

Включить в `sshd_config`:

```
PermitRootLogin yes
PermitTunnel yes
```

Установить соединение с инициализацией tun-устройств и настроить адреса:

```bash
# клиент
localhost:~# ssh -v -w any root@remoteserver
localhost:~# ip addr add 10.10.10.2/32 peer 10.10.10.10 dev tun0
localhost:~# ip link set tun0 up

# сервер
remoteserver:~# ip addr add 10.10.10.10/32 peer 10.10.10.2 dev tun0
remoteserver:~# ip link set tun0 up
```

Маршрут подсети через туннель и NAT на удалённой стороне:

```bash
localhost:~#    ip route add 10.10.10.0/24 dev tun0
remoteserver:~# echo 1 > /proc/sys/net/ipv4/ip_forward
remoteserver:~# iptables -t nat -A POSTROUTING -s 10.10.10.2 -o enp7s0 -j MASQUERADE
```

Диагностика — `tcpdump` и `ping` (ICMP идёт через туннель). Подробнее про iptables — [IPTables](../IPTables.md).

## sshuttle — VPN без задержек TCP-over-TCP

SSH-туннели — это TCP поверх TCP, что при больших объёмах трафика (SOCKS-прокси) даёт рост задержки. `sshuttle` решает проблему:

```bash
sudo apt install sshuttle
# или из исходников:
git clone https://github.com/sshuttle/sshuttle.git && cd sshuttle && ./setup.py install
```

Завернуть весь трафик в туннель:

```bash
$ sudo sshuttle -r user@remote_ip -x remote_ip 0/0 -vv
```

`Ctrl+C` — разорвать; ключ `-D` — запустить демоном. Проверка внешнего IP: `curl ipinfo.io`.

## Прыжки по хостам -J / ProxyJump

Чтобы добраться до целевой сети через цепочку хостов:

```bash
localhost:~$ ssh -J host1,host2,host3 user@host4.internal
```

Это **не** то же самое, что последовательные `ssh host1 → ssh host2`: `-J` использует переадресацию, localhost аутентифицируется на `host4` своими ключами, и сессия полностью зашифрована до конца. В `ssh_config` — опция `ProxyJump`.

## Мультиплексирование ControlMaster

По умолчанию каждое новое `ssh`/`scp` к серверу — отдельная сессия с повторной аутентификацией. `ControlMaster` переиспользует существующее соединение — заметно быстрее:

```
Host remoteserver
        HostName remoteserver.example.org
        ControlMaster auto
        ControlPath ~/.ssh/control/%r@%h:%p
        ControlPersist 10m
```

`ControlPath` — сокет, который проверяют новые соединения; `ControlPersist 10m` держит мастер-сессию открытой ещё 10 минут после выхода. Разовый вариант из командной строки:

```bash
$ ssh -MNf user@host    # -M мастер, -N без команды, -f в фон
```

## Прочие приёмы

### Удалённый перехват пакетов в Wireshark

```bash
$ ssh root@remoteserver 'tcpdump -c 1000 -nn -w - not port 22' | wireshark -k -i -
```

### Копирование папки через tar по SSH

Сжать `bzip2` на лету и распаковать на той стороне:

```bash
$ tar -cvj /datafolder | ssh remoteserver "tar -xj -C /datafolder"
```

### GUI-приложения через X11 (-X)

```bash
$ ssh -X remoteserver vmware
```

Требует `X11Forwarding yes` в `sshd_config` и «иксы» на обеих сторонах.

### SSH через Tor

```bash
$ torsocks ssh myuntracableuser@remoteserver   # прокси через порт 9050
```

Следите за opsec: **куда уходят DNS-запросы?**

### SSH к инстансу AWS EC2

```bash
$ chmod 400 ~/.ssh/my-ec2-key.pem
$ ssh -i ~/.ssh/my-ec2-key.pem ubuntu@my-ec2-public
```

Удобно прописать в `~/.ssh/config`:

```
Host my-ec2-public
   Hostname ec2???.compute-1.amazonaws.com
   User ubuntu
   IdentityFile ~/.ssh/my-ec2-key.pem
```

### Потоковое видео через SFTP в VLC

`File → Open Network Stream → sftp://`:

```
sftp://remoteserver//media/uploads/myvideo.mkv
```

## Безопасность сервиса SSH

- **Двухфакторная аутентификация.** Сам по себе SSH уже двухфакторен (пароль + ключ); аппаратный токен или Google Authenticator добавляют отдельное физическое устройство.
- **Защита от брутфорса.** Перенос SSH на нестандартный порт (`Port ##` в `sshd_config`) убирает шум в логах. Блокировка по порогу попыток — через `iptables` или связку [OSSEC](https://hackertarget.com/enable-ossec-active-response/) (HIDS). См. также [IPTables](../IPTables.md).

## Полезные man-страницы

```bash
man ssh
man ssh_config
man sshd_config
```

#SSH
#Linux
#Network
#Security
