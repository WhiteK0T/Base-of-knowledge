---
создал заметку: 2026-06-08T19:00:00
author: WhiteK0T
tags:
  - cURL
  - Linux
  - Сеть
  - Шпаргалка
Источник:
  - https://curl.se/docs/manpage.html
  - https://t.me/javaproglib/7699
---

# 🌐 cURL — шпаргалка

**cURL** — утилита для передачи данных по сети (HTTP/HTTPS, FTP, SFTP и десятки других протоколов). Ниже — практическая выжимка.

## ⬇️ Загрузка файлов

| Команда | Что делает |
| :--- | :--- |
| `curl -O <url>` | сохранить под **именем из URL** |
| `curl -o <имя> <url>` | сохранить под **своим именем** |
| `curl -L -O <url>` | следовать за **редиректами** (`-L`) — почти всегда нужно |
| `curl -# -O <url>` | показать **прогресс-бар** вместо таблицы статистики |
| `curl -OJ <url>` | взять имя из заголовка `Content-Disposition` (`-J` + `-O`) |
| `curl -O <url1> -O <url2>` | скачать **несколько** файлов за раз |

## 🔁 Докачка и надёжность (нестабильная сеть)

| Команда | Что делает |
| :--- | :--- |
| `curl -C - -O <url>` | **докачать** с места обрыва (`-C -` — авто-смещение) |
| `curl -C - -# -O <url>` | докачка + прогресс-бар |
| `curl --limit-rate 10M -O <url>` | **ограничить скорость** (не забивать канал) |
| `curl --retry 5 --retry-delay 5 --retry-all-errors -O <url>` | встроенный **авто-ретрай** (5 попыток, пауза 5с, на любые ошибки) |

**Ретрай-цикл вручную** (повторять, пока не скачается):

```bash
while ! curl -C - -O <url>; do sleep 5; done
```

> [!note] Когда работает докачка
> `-C -` использует HTTP-заголовок `Range` (или аналог в FTP/SFTP). Сервер должен поддерживать частичную отдачу — иначе curl скачает заново.

## 🔐 Аутентификация и заголовки

| Команда | Что делает |
| :--- | :--- |
| `curl -u user:pass <url>` | базовая HTTP-аутентификация |
| `curl -H "Authorization: Bearer <token>" <url>` | произвольный заголовок (Bearer-токен) |
| `curl -H "Accept: application/json" <url>` | задать заголовок запроса |
| `curl -b cookies.txt -c cookies.txt <url>` | читать/сохранять cookies |
| `curl -A "MyAgent/1.0" <url>` | свой User-Agent |

## 📡 Методы и API (POST/JSON)

```bash
# POST с JSON
curl -X POST https://api.example.com/orders \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "test"}'

# Тело из файла
curl -X POST https://api.example.com/orders \
  -H "Content-Type: application/json" \
  -d @order.json

# form-data (загрузка файла)
curl -F "file=@photo.jpg" -F "field=value" https://api.example.com/upload

# URL-кодирование параметров / GET с query
curl -G --data-urlencode "q=привет мир" https://api.example.com/search
```

| Флаг | Назначение |
| :--- | :--- |
| `-X <METHOD>` | задать HTTP-метод (`GET`/`POST`/`PUT`/`DELETE`…) |
| `-d <data>` | тело запроса (по умолчанию делает POST) |
| `-d @file` | тело из файла |
| `-F` | multipart/form-data (загрузка файлов) |
| `-G` | отправить `-d`-данные как query string в GET |

## 🛠️ Диагностика и полезное

| Команда | Что делает |
| :--- | :--- |
| `curl -I <url>` | только **заголовки** ответа (HEAD) |
| `curl -v <url>` | подробный лог (запрос/ответ, TLS) |
| `curl -s <url>` | «тихий» режим (без прогресса), удобно в скриптах |
| `curl -sS <url>` | тихо, но **показывать ошибки** |
| `curl -k <url>` | не проверять TLS-сертификат (**небезопасно**, для теста) |
| `curl -o /dev/null -s -w "%{http_code}\n" <url>` | вывести только **HTTP-код** ответа |
| `curl --connect-timeout 5 --max-time 30 <url>` | таймауты на коннект / всю операцию |
| `curl -x http://proxy:8080 <url>` | через прокси |
| `curl --resolve host:443:1.2.3.4 <url>` | подменить DNS для хоста (тест без правки `/etc/hosts`) |

См. также: [SCP](SCP.md) — копирование файлов по SSH.

#cURL #Linux #Сеть #Шпаргалка
