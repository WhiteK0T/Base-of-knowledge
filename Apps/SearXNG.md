---
создал заметку: 2026-04-20T00:57:00
author: WhiteK0T
tags:
  - opensource
  - searxng
  - searchengine
Источник:
  - https://forum.samohosting.ru/t/searxng-vash-lichnyj-anonimnyj-poiskovyj-dvizhok/2175
---
# 🔍 SearXNG: Ваш личный анонимный поисковый движок

**SearXNG** — это мощный мета-поисковый движок с открытым исходным кодом, который позволяет объединить результаты из множества поисковых систем (Google, Bing, DuckDuckGo и др.) в одном интерфейсе, обеспечивая при этом максимальную приватность.

## 🚀 Основная концепция
В отличие от обычных поисковиков, SearXNG не собирает ваши данные, не использует трекеры и не создает ваш «цифровой профиль». Он выступает в роли посредника: отправляет запросы к сторонним сервисам от своего имени, скрывая ваш IP-адрес и историю поиска.

## ✨ Ключевые преимущества
* **Приватность (Privacy First):** Никакого отслеживания, нет рекламных алгоритмов, нет сбора персональных данных.
* **Агрегация результатов:** Вы получаете ответы сразу из десятков источников в одном окне.
* **Отсутствие «пузыря фильтров»:** Результаты поиска не подстраиваются под ваши прошлые интересы, что дает более объективную картину.
* **Open Source:** Полная прозрачность кода и возможность самостоятельного хостинга.
* **Кастомизация:** Возможность выбора конкретных поисковых движков для каждого запроса.

## 🛠 Технические возможности
* **Self-hosting:** Идеальное решение для тех, кто хочет развернуть собственный экземпляр на своем сервере (через Docker или напрямую).
* **Поддержка расширений:** Можно настроить поиск по изображениям, видео, новостям и даже специализированным научным базам.
* **Чистый интерфейс:** Минималистичный дизайн без навязчивой рекламы.

## 📦 Ссылки на проект
* **GitHub:** [https://github.com/searxng/searxng](https://github.com/searxng/searxng)
* **Документация:** [https://docs.searxng.org/](https://docs.searxng.org/)

## ⚙️ Как установить?
1.  [Официальная документация по установке](https://docs.searxng.org/admin/installation.html)
2.  [LXC контейнер PVE через скрипты-помощники](https://community-scripts.org/scripts/searxng)
3.  Runtipi
4.  Docker

docker-compose.yml
```yml
services:
  searxng:
    container_name: searxng
    image: searxng/searxng:latest
    restart: unless-stopped
    volumes:
      - ./config/:/etc/searxng
      - ./data/:/var/cache/searxng
    ports:
      - 8888:8080
    environment:
      # Указать адрес Вашего сервера формата http://server_ip/
      - BASE_URL=${SERVER_URL}
      #для генерации секрета можете использовать "openssl rand -hex 32"
      - SEARXNG_SECRET=${SEARXNG_SECRET_KEY}
networks: {}
```

## 🛠 Как включить опцию ответа на запрос не только html, но и json:

1.  Нас с Вами будет интересовать файл **settings.yml**, который в разных вариантах установки может быть по разному пути.

Например в докере искать тут
```
/etc/searxng/settings.yml
```
В LXC созданном через скрипты помощники
```
/usr/local/searxng/searxng-src/searx/settings.yml
```

2. В файле нас будет интересовать блок search
Куда после уже имеющегося - html, мы добавим json

```yml
search:
....
  # formats: [html, csv, json, rss]
  formats:
    - html
    - json
```

3. Проверить, что оно заработало можно введя в строку браузера
```
http://ip:port/search?q=<Любой текст Вашего запроса>&format=json
```
В ответ Вы должны получить не 404 Forbidden , а json с ответом.

---
*Источник: [Samohosting Forum](https://forum.samohosting.ru/t/searxng-vash-lichnyj-anonimnyj-poiskovyj-dvizhok/2175)*
#privacy 
#searchengine 
#opensource 
#searxng