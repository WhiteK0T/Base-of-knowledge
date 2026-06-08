---
создал заметку: 2026-06-05T18:45:00
author: WhiteK0T
tags:
  - SSH
  - Linux
  - Network
  - CheatSheet
Источник:
  - https://itmozg.ru/vizualnoe-rukovodstvo-po-tunneljam-ssh/
  - https://iximiuz.com/en/posts/ssh-tunnels/
---

# Визуальное руководство по туннелям SSH

Наглядная шпаргалка по SSH-туннелям: локальный и удалённый проброс портов, режим bastion-хоста и проброс из домашней сети — с диаграммами и воспроизводимыми лабами на Docker. Дополняет раздел «Проброс портов и туннели» в [SSH — Продвинутое руководство](SSH-Продвинутое%20руководство.md).

SSH – это еще один пример древней технологии, которая широко используется и сегодня. Вполне возможно, что освоение пары трюков с SSH в долгосрочной перспективе более выгодно, чем освоение дюжины инструментов Cloud Native, которым суждено устареть в следующем квартале.

Одна из моих любимых особенностей этой технологии – туннели SSH. Не имея ничего, кроме стандартных инструментов, и часто используя всего одну команду, вы можете добиться следующего:

- Доступ к внутренним конечным точкам VPC через публичный экземпляр EC2.
- Открыть порт с локального хоста виртуальной машины разработчика в браузере хоста.
- Открыть любой локальный сервер из домашней/частной сети внешнему миру.

И многое другое

Но несмотря на то, что я ежедневно использую SSH-туннели, мне всегда требуется время, чтобы найти нужную команду. Должен ли это быть локальный или удаленный туннель? Какие должны быть флаги? Должен ли это быть локальный_порт:удаленный_порт или наоборот? Итак, я решил наконец разобраться с этим, и в результате получилась серия лабораторных работ и наглядная шпаргалка.

![Сводная схема туннелей SSH](../../Cache/ssh/Визуальное%20руководство%20по%20туннелям%20SSH/ssh-tunnels-2000-opt-1024x652.png)

[Полная версия (1.5 MB)](../../Cache/ssh/Визуальное%20руководство%20по%20туннелям%20SSH/ssh-tunnels.png)

## Необходимые условия

Туннели SSH – это соединение хостов по сети, поэтому в каждой из приведенных ниже лабораторных работ, как ожидается, будет задействовано несколько “машин”. Однако мне лень создавать полноценные экземпляры, особенно когда вместо них можно использовать контейнеры. Поэтому в итоге я использовал только одну виртуальную машину vagrant с установленным на ней Docker.

Теоретически, подойдет любая Linux-машина с установленным на ней Docker Engine. Однако запустить приведенные ниже примеры как есть с помощью Docker Desktop не удастся, поскольку предполагается возможность доступа к контейнерам машин по их IP-адресам.

В качестве альтернативы, лабораторные работы можно выполнить с помощью [Lima (QEMU + nerdctl + containerd + BuildKit)](https://github.com/lima-vm/lima), но не забудьте сначала выполнить `limactl shell bash`.

Каждый пример требует наличия на хосте действующей пары ключей без парольной фразы, которая затем монтируется в контейнеры для упрощения управления доступом. Если у вас нет такой пары, сгенерировать ее можно просто с помощью `ssh-keygen` на хосте.

**Важно:** демоны SSH в контейнерах здесь предназначены исключительно для образовательных целей — контейнеры в этом посте предназначены для представления полноценных «машин» с SSH-клиентами и серверами на них. Имейте в виду, что использование SSH в реальных контейнерах редко бывает хорошей идеей!

## Переадресация локального порта

Начнем с того, что я использую чаще всего. Часто бывает, что есть служба, прослушивающая localhost или частный интерфейс машины, к которому я могу подключиться только по SSH через его публичный IP. И мне крайне необходимо получить доступ к этому порту извне. Несколько типичных примеров:

- Доступ к базе данных (MySQL, Postgres, Redis и т.д.) с помощью причудливого пользовательского интерфейса с вашего ноутбука.
- Использование браузера для доступа к веб-приложению, открытому только для частной сети.
- Доступ к порту контейнера с вашего ноутбука без публикации его на публичном интерфейсе сервера.

Все вышеперечисленные случаи использования могут быть решены с помощью одной команды `ssh`:

```bash
ssh -L [local_addr:]local_port:remote_addr:remote_port [user@]sshd_addr
```

Флаг `-L` указывает на то, что мы запускаем локальную проброску портов. На самом деле это означает следующее:

- На вашей машине клиент SSH начнет слушать `local_port` (скорее всего, на `localhost`, но это зависит от ситуации – [проверьте настройки `GatewayPorts`](https://linux.die.net/man/5/sshd_config#GatewayPorts)).
- Любой трафик на этот порт будет перенаправлен на `remote_private_addr:remote_port` на машине, к которой вы подключились по SSH.

Вот как это выглядит на схеме:

![Схема: локальная переадресация порта](../../Cache/ssh/Визуальное%20руководство%20по%20туннелям%20SSH/local-port-forwarding-2000-opt-1024x717.png)

Профессиональный совет: Используйте `ssh -f -N -L` для запуска сеанса переадресации портов в фоновом режиме.

### Лабораторная работа 1: Использование туннелей SSH для локальной переадресации портов

Лабораторная работа воспроизводит настройку из приведенной выше схемы. Во-первых, нам нужно подготовить сервер – машину с демоном SSH и простым веб-сервисом, прослушивающим 127.0.0.1:80:

```bash
$ docker buildx build -t server:latest -<<'EOD'
# syntax=docker/dockerfile:1
FROM alpine:3

# Install the dependencies:
RUN apk add --no-cache openssh-server curl python3
RUN mkdir /root/.ssh && chmod 0700 /root/.ssh && ssh-keygen -A

# Prepare the entrypoint that starts the daemons:
COPY --chmod=755 <<'EOF' /entrypoint.sh
#!/bin/sh
set -euo pipefail

for file in /tmp/ssh/*.pub; do
  cat ${file} >> /root/.ssh/authorized_keys
done
chmod 600 /root/.ssh/authorized_keys

# Minimal config for the SSH server:
sed -i '/AllowTcpForwarding/d' /etc/ssh/sshd_config
sed -i '/PermitOpen/d' /etc/ssh/sshd_config
/usr/sbin/sshd -e -D &

python3 -m http.server --bind 127.0.0.1 ${PORT} &

sleep infinity
EOF

# Run it:
CMD ["/entrypoint.sh"]
EOD
```

Запускаем сервер и записываем его IP-адрес:

```bash
$ docker run -d --rm \
   -e PORT=80 \
   -v $HOME/.ssh:/tmp/ssh \
   --name server \
   server:latest

SERVER_IP=$(
  docker inspect \
    -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  server
)
```

Поскольку веб-служба прослушивает localhost, она не будет доступна извне (т.е. из хост-системы в данном конкретном случае):

```bash
$ curl ${SERVER_IP}
curl: (7) Failed to connect to 172.17.0.2 port 80: Connection refused
```

Но изнутри “сервера” работает просто отлично:

```bash
$ ssh -o StrictHostKeyChecking=no root@${SERVER_IP}
7b3e49181769:$# curl localhost
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
...
```

**И вот в чем хитрость:** привяжите `localhost:80` сервера к `localhost:8080` хоста, используя локальную переадресацию портов:

```bash
$ ssh -o StrictHostKeyChecking=no -f -N -L 8080:localhost:80 root@${SERVER_IP}
```

Теперь вы должны иметь возможность получить доступ к веб-службе на локальном порту хост-системы:

```bash
$ curl localhost:8080
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
...
```

Несколько более многословный (но более явный и гибкий) способ достижения той же цели – использование формы `local_addr:local_port:remote_addr:remote_port`:

```bash
$ ssh -o StrictHostKeyChecking=no -f -N -L \
  localhost:8080:localhost:80 \
  root@${SERVER_IP}
```

## Локальная переадресация портов с хостом Bastion

Это может быть неочевидно на первый взгляд, но команда `ssh -L` позволяет перенаправить локальный порт на удаленный порт на _любой машине_, а не только на самом SSH-сервере. Обратите внимание, что `remote_addr` и `sshd_addr` могут иметь одинаковое значение, а могут и не иметь:

```bash
ssh -L [local_addr:]local_port:remote_addr:remote_port [user@]sshd_addr
```

Не уверен, насколько правомерно здесь использование термина [_bastion host_](https://en.wikipedia.org/wiki/Bastion_host), но именно так я представляю себе этот сценарий:

![Схема: локальная переадресация через bastion-хост](../../Cache/ssh/Визуальное%20руководство%20по%20туннелям%20SSH/local-port-forwarding-bastion-2000-opt-1024x668.png)

Я часто использую этот трюк для вызова конечных точек, которые доступны с хоста bastion, но не с моего ноутбука (например, использование экземпляра EC2 с частным и публичным интерфейсами для подключения к кластеру OpenSearch, развернутому полностью в VPC).

### Лаборатория 2: Локальная переадресация портов с хостом Bastion

И снова лабораторная работа воспроизводит установку из приведенной выше схемы. Сначала нам нужно подготовить хост бастиона – машину, на которой установлен только демон SSH:

```bash
$ docker buildx build -t bastion:latest -<<'EOD'
# syntax=docker/dockerfile:1
FROM alpine:3

# Install the dependencies:
RUN apk add --no-cache openssh-server
RUN mkdir /root/.ssh && chmod 0700 /root/.ssh && ssh-keygen -A

# Prepare the entrypoint that starts the SSH daemon:
COPY --chmod=755 <<'EOF' /entrypoint.sh
#!/bin/sh
set -euo pipefail

for file in /tmp/ssh/*.pub; do
  cat ${file} >> /root/.ssh/authorized_keys
done
chmod 600 /root/.ssh/authorized_keys

# Minimal config for the SSH server:
sed -i '/AllowTcpForwarding/d' /etc/ssh/sshd_config
sed -i '/PermitOpen/d' /etc/ssh/sshd_config
/usr/sbin/sshd -e -D &

sleep infinity
EOF

# Run it:
CMD ["/entrypoint.sh"]
EOD
```

Запускаем бастионный хост и записываем его IP:

```bash
$ docker run -d --rm \
    -v $HOME/.ssh:/tmp/ssh \
    --name bastion \
    bastion:latest

BASTION_IP=$(
  docker inspect \
    -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  bastion
)
```

Теперь запускаем целевую веб-службу на отдельной “машине”:

```bash
$ docker run -d --rm \
    --name server \
    python:3-alpine \
    python3 -m http.server 80

SERVER_IP=$(
  docker inspect \
    -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  server
)
```

Представим, что вызов `curl ${SERVER_IP}` непосредственно с хоста по какой-то причине невозможен (например, как если бы не было маршрута от хоста к этому IP-адресу). Значит, нам нужно запустить переадресацию портов:

```bash
$ ssh -o StrictHostKeyChecking=no -f -N -L 8080:${SERVER_IP}:80 root@${BASTION_IP}
```

**Обратите внимание, что переменные SERVER_IP и BASTION_IP имеют разные значения в приведенной выше команде.**

Проверяем, что все работает:

```bash
$ curl localhost:8080
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
...
```

## Удаленная переадресация портов

Другой популярный (но скорее обратный) сценарий – когда вы хотите на время открыть локальную службу для внешнего мира. Разумеется, для этого вам понадобится публичный сервер входящего шлюза. Но не бойтесь! В качестве такого шлюза можно использовать любой сервер с публичным доступом, на котором установлен демон SSH:

```bash
ssh -R [remote_addr:]remote_port:local_addr:local_port [user@]gateway_addr
```

Приведенная выше команда выглядит не сложнее, чем ее аналог `ssh -L`. Но есть один подводный камень…

**По умолчанию вышеуказанный SSH-туннель позволяет использовать в качестве удаленного адреса только localhost шлюза.** Другими словами, ваш локальный порт станет доступным только изнутри самого сервера шлюза, и, скорее всего, это не то, что вам действительно нужно. Например, я обычно хочу использовать публичный адрес шлюза в качестве удаленного адреса, чтобы открыть доступ к моим локальным службам в публичный интернет. Для этого SSH-сервер должен быть настроен с параметром [GatewayPorts yes](https://linux.die.net/man/5/sshd_config#GatewayPorts).

Вот для чего можно использовать удаленное перенаправление портов:

- Выставление службы dev с вашего ноутбука в публичный Интернет для демонстрации.
- Хм… Я могу придумать несколько эзотерических примеров, но сомневаюсь, что стоит делиться ими здесь. Любопытно услышать, для чего другие люди могут использовать удаленное перенаправление портов!

Вот как удаленное перенаправление портов выглядит на схеме:

![Схема: удалённая переадресация порта](../../Cache/ssh/Визуальное%20руководство%20по%20туннелям%20SSH/remote-port-forwarding-2000-opt-1024x648.png)

**Профессиональный совет:** Используйте `ssh -f -N -R` для запуска сеанса переадресации портов в фоновом режиме.

### Лабораторная работа 3: Использование туннелей SSH для удаленной переадресации портов

Лабораторная работа воспроизводит установку, показанную на схеме выше. Сначала нам нужно подготовить “dev machine” – компьютер с SSH-клиентом и локальным веб-сервером:

```bash
$ docker buildx build -t devel:latest -<<'EOD'
# syntax=docker/dockerfile:1
FROM alpine:3

# Install dependencies:
RUN apk add --no-cache openssh-client curl python3
RUN mkdir /root/.ssh && chmod 0700 /root/.ssh

# Prepare the entrypoint that starts the web service:
COPY --chmod=755 <<'EOF' /entrypoint.sh
#!/bin/sh
set -euo pipefail

cp /tmp/ssh/* /root/.ssh
chmod 600 /root/.ssh/*

python3 -m http.server --bind 127.0.0.1 ${PORT} &

sleep infinity
EOF

# Run it:
CMD ["/entrypoint.sh"]
EOD
```

Запуск виртуальной машины:

```bash
$ docker run -d --rm \
    -e PORT=80 \
    -v $HOME/.ssh:/tmp/ssh \
    --name devel \
    devel:latest
```

Подготовка сервера шлюза – простой SSH-сервер с `GatewayPorts`, установленным на `yes` в `sshd_config`:

```bash
$ docker buildx build -t gateway:latest -<<'EOD'
# syntax=docker/dockerfile:1
FROM alpine:3

# Install the dependencies:
RUN apk add --no-cache openssh-server
RUN mkdir /root/.ssh && chmod 0700 /root/.ssh && ssh-keygen -A

# Prepare the entrypoint that starts the SSH server:
COPY --chmod=755 <<'EOF' /entrypoint.sh
#!/bin/sh
set -euo pipefail

for file in /tmp/ssh/*.pub; do
  cat ${file} >> /root/.ssh/authorized_keys
done
chmod 600 /root/.ssh/authorized_keys

sed -i '/AllowTcpForwarding/d' /etc/ssh/sshd_config
sed -i '/PermitOpen/d' /etc/ssh/sshd_config
sed -i '/GatewayPorts/d' /etc/ssh/sshd_config
echo 'GatewayPorts yes' >> /etc/ssh/sshd_config

/usr/sbin/sshd -e -D &

sleep infinity
EOF

# Run it:
CMD ["/entrypoint.sh"]
EOD
```

Запуск сервера шлюза и запись его IP-адреса:

```bash
$ docker run -d --rm \
    -v $HOME/.ssh:/tmp/ssh \
    --name gateway \
    gateway:latest

GATEWAY_IP=$(
  docker inspect \
    -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  gateway
)
```

Теперь **изнутри dev-машины запустите удаленное перенаправление портов:**

```bash
$ docker exec -it -e GATEWAY_IP=${GATEWAY_IP} devel sh
/ $# ssh -o StrictHostKeyChecking=no -f -N -R 0.0.0.0:8080:localhost:80 root@${GATEWAY_IP}
/ $# exit  # or detach with ctrl-p, ctrl-q
```

И проверьте, что локальный порт машины dev стал открытым на публичном интерфейсе шлюза (с хост-системы):

```bash
$ curl ${GATEWAY_IP}:8080
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
...
```

## Удаленная переадресация портов из домашней/частной сети

Подобно локальной переадресации портов, удаленная переадресация портов имеет свой собственный режим бастионного хоста. Но на этот раз в роли бастиона выступает машина с SSH-клиентом (например, ваш ноутбук dev). В частности, он позволяет открывать порты из домашней (или частной) сети, к которой имеет доступ ваш ноутбук, во внешний мир через входящий шлюз:

```bash
ssh -R [remote_addr:]remote_port:local_addr:local_port [user@]gateway_addr
```

Выглядит почти так же, как и простой удаленный SSH-туннель, но пара `local_addr:local_port` становится адресом устройства в домашней сети. Вот как это можно изобразить на схеме:

![Схема: удалённая переадресация из домашней сети](../../Cache/ssh/Визуальное%20руководство%20по%20туннелям%20SSH/remote-port-forwarding-home-network-2000-opt-1024x558.png)

Поскольку я обычно использую свой ноутбук в качестве тонкого клиента, а реальная разработка происходит на домашнем сервере, я полагаюсь на такую удаленную переадресацию портов, когда мне нужно выставить службу разработчика с домашнего сервера в публичный Интернет, и единственной машиной с доступом к шлюзу является мой ноутбук.

### Лаборатория 4: Удаленная переадресация портов из домашней/частной сети

Как обычно, лаборатория воспроизводит установку из приведенной выше схемы. Сначала нам нужно подготовить “машину dev”:

```bash
$ docker buildx build -t devel:latest -<<'EOD'
# syntax=docker/dockerfile:1
FROM alpine:3

# Install the dependencies:
RUN apk add --no-cache openssh-client
RUN mkdir /root/.ssh && chmod 0700 /root/.ssh

# This time we run nothing (at first):
COPY --chmod=755 <<'EOF' /entrypoint.sh
#!/bin/sh
set -euo pipefail

cp /tmp/ssh/* /root/.ssh
chmod 600 /root/.ssh/*

sleep infinity
EOF

# Run it:
CMD ["/entrypoint.sh"]
EOD
```

Запуск “dev machine”:

```bash
$ docker run -d --rm \
    -v $HOME/.ssh:/tmp/ssh \
    --name devel \
    devel:latest
```

Запуск частного dev-сервера с использованием отдельной “машины” и указанием ее IP-адреса:

```bash
$ docker run -d --rm \
    --name server \
    python:3-alpine \
    python3 -m http.server 80

SERVER_IP=$(
  docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  server
)
```

Подготовка сервера входящего шлюза:

```bash
$ docker buildx build -t gateway:latest -<<'EOD'
# syntax=docker/dockerfile:1
FROM alpine:3

# Install the dependencies:
RUN apk add --no-cache openssh-server
RUN mkdir /root/.ssh && chmod 0700 /root/.ssh && ssh-keygen -A

# Prepare the entrypoint that starts the SSH daemon:
COPY --chmod=755 <<'EOF' /entrypoint.sh
#!/bin/sh
set -euo pipefail

for file in /tmp/ssh/*.pub; do
  cat ${file} >> /root/.ssh/authorized_keys
done
chmod 600 /root/.ssh/authorized_keys

sed -i '/AllowTcpForwarding/d' /etc/ssh/sshd_config
sed -i '/PermitOpen/d' /etc/ssh/sshd_config
sed -i '/GatewayPorts/d' /etc/ssh/sshd_config
echo 'GatewayPorts yes' >> /etc/ssh/sshd_config

/usr/sbin/sshd -e -D &

sleep infinity
EOF

# Run it:
CMD ["/entrypoint.sh"]
EOD
```

И запустить его:

```bash
$ docker run -d --rm \
    -v $HOME/.ssh:/tmp/ssh \
    --name gateway \
    gateway:latest

GATEWAY_IP=$(
  docker inspect \
    -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
  gateway
)
```

Теперь, **находясь внутри ”dev machine”, запустите удаленный проброс портов SERVER-GATEWAY:**

```bash
$ docker exec -it -e GATEWAY_IP=${GATEWAY_IP} -e SERVER_IP=${SERVER_IP} devel sh
/ $# ssh -o StrictHostKeyChecking=no -f -N -R 0.0.0.0:8080:${SERVER_IP}:80 root@${GATEWAY_IP}
/ $# exit  # or detach with ctrl-p, ctrl-q
```

Наконец, проверьте, что сервер dev стал доступен на публичном интерфейсе шлюза (из хост-системы):

```bash
$ curl ${GATEWAY_IP}:8080
<!DOCTYPE HTML>
<html lang="en">
<head>
...
```

## Подведение итогов

После выполнения всех этих лабораторных работ и рисунков я заметил следующее:

- Слово “**local**” может означать как **машину клиента SSH**, так и хост, доступный с этой машины.
- Слово “**remote**” может означать как **машину сервера SSH (sshd)**, так и доступный с нее хост.
- Локальная проброска портов (`ssh -L`) подразумевает, что именно клиент `ssh` начинает прослушивать новый порт.
- Удаленное перенаправление портов (`ssh -R`) подразумевает, что именно сервер `sshd` начинает прослушивать дополнительный порт.

#SSH
#Linux
#Network
#CheatSheet
