---
создал заметку: 2026-10-28T00:10:00
author: WhiteK0T
tags:
  - tcpdump
  - Linux
  - Сеть
  - Безопасность
  - DFIR
  - Диагностика
  - Шпаргалка
Источник:
  - https://t.me/+3X56uL4A-UM3Njgy
  - https://www.tcpdump.org/manpages/tcpdump.1.html
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
---

# 📡 tcpdump — захват трафика и фильтры для разбора инцидента (шпаргалка)

**tcpdump** — консольный анализатор трафика на базе **libpcap**. Он отвечает на вопросы «кто, куда и что передавал»: печатает заголовки пакетов прямо в терминал или пишет их в `.pcap`, который потом открывают в Wireshark. Фильтр (синтаксис **pcap-filter**, он же BPF) компилируется в байт-код и выполняется **в ядре**, поэтому лишние пакеты отбрасываются ещё до копирования в tcpdump — на нагруженном интерфейсе это важно.

Основа — пост «10 фильтров tcpdump для расследования инцидента» из канала [CodeGuard: PySec Edition](https://t.me/+3X56uL4A-UM3Njgy). Каждый фильтр прогнан на **tcpdump 4.99.7 / libpcap 1.11.0** по тестовому pcap (IPv4 и IPv6, SYN / SYN-ACK / RST, DNS по UDP и TCP, QUIC, SSH, ARP, ICMP), поведение сборок сверено с исходниками и пакетами Gentoo, Debian, Arch и Entware.

> [!warning] Нужны root или `CAP_NET_RAW`
> Захват с интерфейса — `sudo tcpdump ...`. Без прав: `You don't have permission to perform this capture on that device (… CAP_NET_RAW may be required)`. Чтение готового файла (`-r`) прав не требует.

## 🚀 10 команд из поста — с уточнениями

`eth0` — имя из поста; на современных системах интерфейсы называются `enp3s0`, `ens3` и т.п. Список — `tcpdump -D`, все сразу — `-i any`. Флаг `-n` добавлен везде, почему — в п. 7.

| # | Задача | Команда | Что важно знать |
| :--- | :--- | :--- | :--- |
| 1 | Трафик на порт | `tcpdump -n -i eth0 port 443` | Оба направления, **TCP и UDP**: сюда попадает и QUIC (HTTP/3). Только TCP — `tcp port 443`, только QUIC — `udp port 443` |
| 2 | Между двумя хостами | `tcpdump -n -i eth0 host 192.168.1.10 and host 10.0.0.5` | В обе стороны |
| 3 | Попытки соединения | `tcpdump -n -i eth0 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack = 0'` | Только SYN без ACK. Вариант `tcp[tcpflags] & tcp-syn != 0` ловит ещё и **SYN-ACK** — ответы сервера. Популярный `tcp[13] = 2` пропускает SYN с флагами ECN (`ECE`/`CWR`). Работает **только для IPv4** — про IPv6 раздел ниже |
| 4 | Без своего SSH | `tcpdump -n -i eth0 "not (tcp port 22 and host ${SSH_CLIENT%% *})"` | Прячет только **свою** сессию: `$SSH_CLIENT` начинается с твоего IP. Простое `not port 22` скрывает весь SSH, включая перебор паролей извне. Под `sudo -i`/`su -` переменная теряется — подставь IP руками |
| 5 | Подсеть | `tcpdump -n -i eth0 net 192.168.1.0/24` | Источник **или** получатель в подсети — то есть и выход в интернет. Только внутренний трафик: `src net 192.168.1.0/24 and dst net 192.168.1.0/24` |
| 6 | RST-пакеты | `tcpdump -n -i eth0 'tcp[tcpflags] & tcp-rst != 0'` | Ловит и `RST`, и `RST-ACK`. Поток RST в ответ на SYN — закрытые порты (кто-то сканирует); RST посреди сессии — обрыв или вмешательство middlebox. Только IPv4 |
| 7 | DNS | `tcpdump -n -i eth0 port 53` | UDP и TCP. **`-n` обязателен**: без него tcpdump сам шлёт обратные DNS-запросы (PTR) на каждый новый адрес — они попадают в тот же вывод и тормозят его. DoT (`port 853`) и DoH (443) видны только как шифрованный поток |
| 8 | Что отправил хост | `tcpdump -n -i eth0 src host 192.168.1.10` | Фильтр по **адресу отправителя**. «Всё, что уходит с интерфейса этой машины» — `-Q out` (на Linux): `tcpdump -n -i eth0 -Q out` |
| 9 | Запись в файл | `tcpdump -n -i eth0 -w capture.pcap` | С `-w` на экран ничего не выводится; писать и печатать одновременно — `--print`. Про `Permission denied` — раздел «Права» ниже |
| 10 | Ограничить число пакетов | `tcpdump -n -i eth0 -c 100` | Остановится после 100 пакетов, **прошедших фильтр** |

> [!tip] Фильтр — в одинарные кавычки
> `( ) & | !` и `$` — спецсимволы shell. Фильтр с ними пиши в `'...'`. Двойные кавычки — только когда нужна подстановка переменной, как в п. 4.

## 🧩 Синтаксис фильтров

| Примитив | Пример | Совпадает, если… |
| :--- | :--- | :--- |
| `host` | `host 10.0.0.5` | адрес источника или получателя (IPv4/IPv6/ARP) |
| `net` | `net 10.0.0.0/8` | адрес в подсети (IPv6 тоже: `net 2001:db8::/32`) |
| `port`, `portrange` | `port 53`, `portrange 8000-8100` | порт TCP/UDP/SCTP |
| `src`, `dst` | `src host …`, `dst port 22` | только указанное направление; без них — любое |
| протокол | `tcp`, `udp`, `icmp`, `icmp6`, `arp`, `ip`, `ip6` | тип пакета |
| длина | `greater 1000`, `less 100` | длина пакета `>=` / `<=` |
| MAC | `ether host 02:00:00:00:00:01` | адрес канального уровня |
| байты пакета | `tcp[13] = 2`, `ip[8] < 5` | произвольное поле заголовка (`proto[смещение:размер]`) |

Операторы — `and` (`&&`), `or` (`||`), `not` (`!`). `not` связывает сильнее всех, а **`and` и `or` равноправны и читаются слева направо**:

```bash
tcpdump -n 'host 192.168.1.10 and port 80 or port 443'     # = (host … and port 80) or port 443 — весь 443 любых хостов
tcpdump -n 'host 192.168.1.10 and (port 80 or port 443)'   # то, что имелось в виду
```

## ⚠️ IPv6: `tcp[...]` не видит IPv6-пакеты

`pcap-filter(7)`: арифметика над заголовками транспортного уровня (`tcp[13]`, `tcp[tcpflags]`) **проверяет только IPv4**. В тесте фильтр SYN из поста пропустил IPv6-SYN. Для IPv6 флаги читают через `ip6[]`: заголовок IPv6 — 40 байт, флаги TCP — 13-й байт TCP, значит `ip6[53]`; `ip6[6] = 6` — следующий заголовок TCP. Работает, пока между IPv6 и TCP нет заголовков расширений (для обычного TCP так и есть).

```bash
# SYN без ACK — IPv4 и IPv6
tcpdump -n -i eth0 'tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn or (ip6[6] = 6 and ip6[53] & 0x12 = 0x02)'

# RST — IPv4 и IPv6
tcpdump -n -i eth0 'tcp[tcpflags] & tcp-rst != 0 or (ip6[6] = 6 and ip6[53] & 0x04 != 0)'
```

Биты байта флагов: `FIN 0x01`, `SYN 0x02`, `RST 0x04`, `PSH 0x08`, `ACK 0x10`, `URG 0x20`.

## 🛡️ Готовые фильтры для разбора инцидента

```bash
# Перебор SSH: кто стучится (IPv4), топ источников
tcpdump -n -l -i eth0 'dst port 22 and tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn' \
  | awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn

# Сканирование: на какие порты приходят SYN (первые 1000)
tcpdump -n -l -i eth0 -c 1000 'tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn' \
  | awk '{sub(/:$/,"",$5); n=split($5,a,"."); print a[n]}' | sort -n | uniq -c

# Какие домены запрашивают; много длинных TXT?-имён — подозрение на DNS-туннель
tcpdump -n -l -i eth0 port 53 | grep -oE '(A|AAAA|TXT|MX|CNAME)\? [^ ]+'

# HTTP-запросы в открытом виде: 0x47455420 = "GET " в начале данных TCP
tcpdump -n -A -i eth0 'tcp[((tcp[12] & 0xf0) >> 2):4] = 0x47455420'

# TLS ClientHello — в hex видно имя сайта (SNI), если клиент не использует ECH
tcpdump -n -X -i eth0 'tcp[((tcp[12] & 0xf0) >> 2)] = 0x16 and tcp[((tcp[12] & 0xf0) >> 2) + 5] = 0x01'

# Что уходит из LAN наружу
tcpdump -n -i eth0 'src net 192.168.1.0/24 and not dst net 192.168.1.0/24'

# ARP: -e показывает MAC; один IP шлюза с двумя MAC — подмена
tcpdump -n -e -i eth0 arp

# ICMP: крупные пакеты — возможный туннель (обычный ping — около 100 байт)
tcpdump -n -i eth0 'icmp and greater 200'

# Только заголовки, без содержимого: меньше файл, нет чужих данных в pcap
tcpdump -n -i eth0 -s 128 -w headers.pcap
```

`((tcp[12] & 0xf0) >> 2)` — длина TCP-заголовка в байтах (с опциями), т.е. смещение начала данных. Все фильтры с `tcp[...]` — только IPv4.

## 👀 Вывод: что добавить к команде

| Флаг | Что даёт |
| :--- | :--- |
| `-n` | без DNS и `/etc/services`: адреса и порты числами. В 4.99 `-n` выключает и то и другое; `-nn` из старых шпаргалок не нужен, но и не мешает |
| `-v`, `-vv` | больше полей: TTL, ID, длины, контрольные суммы |
| `-A` / `-X` | содержимое пакета: ASCII / hex+ASCII |
| `-e` | заголовок канального уровня (MAC, VLAN) |
| `-tttt` | полная дата и время у каждого пакета (для отчёта по инциденту) |
| `-q` | короткие строки |
| `-l` | построчная буферизация — нужна, когда вывод идёт в `grep`, `awk`, `tee` |
| `-D` | список интерфейсов |
| `-i any` | все интерфейсы сразу (на Linux вместо Ethernet-заголовка — псевдозаголовок; с `-e` видно, с какого интерфейса пакет) |

## 💾 Запись, чтение и долгий захват

| Задача | Команда |
| :--- | :--- |
| Записать и видеть на экране | `tcpdump -n -i eth0 -w capture.pcap --print` |
| Прочитать файл | `tcpdump -n -r capture.pcap` (права root не нужны) |
| Вырезать из большого файла | `tcpdump -r big.pcap -w host.pcap 'host 10.0.0.5'` |
| Кольцевой буфер: 10 файлов по 100 МБ | `tcpdump -n -i eth0 -C 100 -W 10 -w ring.pcap` → `ring.pcap0` … `ring.pcap9`, дальше по кругу. Единица `-C` — миллионы байт |
| Новый файл каждый час | `tcpdump -n -i eth0 -G 3600 -w 'cap-%Y%m%d-%H%M.pcap'` — без шаблона даты в имени файл перезаписывается |
| Сжимать закрытые файлы | добавить `-z gzip` к `-C`/`-G` |

`-w -` пишет pcap в stdout, `-U` сбрасывает каждый пакет сразу — так захват передают другой программе, в том числе Wireshark на своём ПК:

```bash
# захват на сервере → Wireshark на ПК (свой SSH исключён, чтобы не захватывать сам поток)
ssh root@<IP-сервера> "tcpdump -n -i eth0 -U -w - 'not port 22'" | wireshark -k -i -
```

## 🔐 Права и `Permission denied` при `-w`

Сборки tcpdump по-разному **сбрасывают root** после открытия интерфейса (флаг `-Z`; при сборке с `--with-user` — по умолчанию). От этого зависит, куда можно писать файл:

| Система | Что происходит | Что делать |
| :--- | :--- | :--- |
| **Gentoo** | `USE=caps` (по умолчанию): права сбрасываются на пользователя `pcap`, но для создания файлов сохраняется `CAP_DAC_OVERRIDE` — писать можно куда угодно, владельцем файла станет `pcap` | ничего; `-Z root` — если файл нужен от root |
| **Debian / Ubuntu** | собрано `--with-user=tcpdump` без libcap-ng: файл открывает уже пользователь `tcpdump`, ему нужен каталог с правом записи. Плюс **AppArmor-профиль**: писать можно только в файлы `*.pcap`, `*.pcapng`, `*.cap` (с цифрой на конце — для `-C`/`-W`) | писать в `/tmp/capture.pcap` или запускать с `-Z root`; расширение — всегда `.pcap` |
| **Arch** | собрано без `--with-user`: работает от root до конца | ничего |
| **Entware** | SSH-вход на Asuswrt — уже uid 0, права не сбрасываются | писать **на USB-диск** (`/opt/...`, `/tmp/mnt/<диск>/`), а не в `/tmp` — там tmpfs в RAM |

Пример ошибки на Debian: `sudo tcpdump -i eth0 -w /root/cap.pcap` → `tcpdump: /root/cap.pcap: Permission denied`.

## 💻 Установка на твоих системах

| Система | Установка |
| :--- | :--- |
| **Gentoo** | `emerge --ask net-analyzer/tcpdump`. USE-флаги: `caps` (по умолчанию, сброс прав на `pcap`), `suid` — запуск без sudo членам группы `pcap` (`usermod -aG pcap <user>`), `ssl`, `smi`, `samba` (разбор SMB) |
| **Debian / Ubuntu** | `sudo apt install tcpdump` |
| **Arch** | `sudo pacman -S tcpdump` |
| **Entware / RT-AX56U** | `opkg install tcpdump` — **4.99.6-1**, ~0,9 МБ + `libpcap` 1.10.6. Рядом в репозитории: `ngrep` (grep по содержимому пакетов, 30 КБ), `rpcapd` (удалённый захват для Wireshark). Пакет `wireshark` (4.6.2, ~92 МБ установленный) для роутера тяжёл — удобнее гнать трафик по SSH в Wireshark на ПК |

### 📶 На роутере (RT-AX56U, Asuswrt-Merlin)

- LAN-мост — `br0`, имя WAN-интерфейса — `nvram get wan0_ifname` (при PPPoE трафик идёт через `ppp0`).
- В неинтерактивной SSH-сессии `/opt/bin` может не быть в `PATH` — указывай полный путь:

```bash
# DNS-запросы клиентов LAN
/opt/bin/tcpdump -n -l -i br0 port 53

# захват с роутера прямо в Wireshark на ПК
ssh admin@<IP-роутера> "/opt/bin/tcpdump -n -i br0 -U -w - 'not port 22'" | wireshark -k -i -
```

## 🔗 Ссылки

- Пост: канал [CodeGuard: PySec Edition](https://t.me/+3X56uL4A-UM3Njgy)
- man: [tcpdump(1)](https://www.tcpdump.org/manpages/tcpdump.1.html) · [pcap-filter(7)](https://www.tcpdump.org/manpages/pcap-filter.7.html)
- Связанные: [lsof (открытые сокеты и порты)](lsof.md) · [strace](strace.md) · [cURL](curl.md) · [NetWatch — сетевая форензика в терминале](../../Network/NetWatch.md) · [Netcat](../../Network/Net%20Cat.md)

#tcpdump #Linux #Сеть #Безопасность #DFIR #Диагностика #Шпаргалка
