---
создал заметку: 2026-07-25T02:30:00
author: WhiteK0T
tags:
  - Security
  - OSINT
  - Разведка
  - Подборка
  - Право
Источник:
  - https://t.me/bugnotfeature/26612
  - https://github.com/MobileFirstLLC/social-media-hacker-list
  - https://github.com/HackTricks-wiki/hacktricks
---

# 🔎 OSINT-подборка из поста (5 ресурсов) — разбор и о законности

Пост собрал 5 ресурсов «для OSINT-разведки и пробива». Ниже — что это **на самом деле**, потому что половина подписей в посте не соответствует содержимому, а слово «пробив» задаёт неверную (и юридически опасную) рамку.

> [!caution] Сначала о рамке: OSINT ≠ «пробив»
> **OSINT** = сбор данных из **открытых** источников для **законных** задач (ИБ-защита, конкурентная разведка, журналистика, проверка контрагента, self-OSINT — что о тебе есть в сети). **«Пробив»** в русском обиходе = добыча **закрытых персональных данных** (по базам, «за деньги пробьём») — это **преступление**: в РФ — ст. 137 УК (неприкосновенность частной жизни), нарушение 152-ФЗ, часто ст. 272 УК (неправомерный доступ). Слежка/деанон/травля частного лица — незаконны независимо от инструмента. Инструменты ниже — **двойного назначения**; держи их для **авторизованных/оборонительных/учебных** задач.

## 📋 Что в подборке на самом деле

| # | Ресурс | Пост говорит | Реально |
| :-- | :--- | :--- | :--- |
| 1 | **[Social Media Hacker List](https://github.com/MobileFirstLLC/social-media-hacker-list)** (MobileFirstLLC) | «пробив в соцсетях: парсеры, трекеры, обход капч» | ❌ мимо: описание репо — **«apps and tools for enhancing social media experiences»**, т.е. **продуктивные/маркетинговые** тулзы для соцсетей. «Hacker» здесь = «лайфхак», а не деанон. CC0, ~1950★, живой |
| 2 | **[HackHub / Ultimate Hacker Simulator](https://store.steampowered.com/app/2980270/HackHub__Ultimate_Hacker_Simulator/)** | «симулятор обучит базе OSINT» | ⚠️ это **игра в Steam** (развлечение про «хакерскую» фантазию). Реальным навыкам OSINT она не учит — не путай геймплей с методикой |
| 3 | **[Sitdeck](https://sitdeck.com/)** | «мониторим весь мир, 180 источников» | ✅ дашборд **ситуационной осведомлённости**: события мира (конфликты, кибератаки, перелёты, землетрясения, выборы…). Полезно для situational awareness; вероятно **коммерческий** сервис — смотри тариф/условия |
| 4 | **[Master-OSINT-Toolkit](https://github.com/techenthusiast167/Master-OSINT-Toolkit-)** (techenthusiast167) | «огромный сборник для разведки и пробива» | ⚠️ не «огромный»: Python-тулкит (гео по фото, соцпрофили, проверка утечек e-mail, домен/IP, доркинг, Wayback). **~400★, без лицензии, последний коммит сентябрь 2025** (застой) — проверяй актуальность |
| 5 | **[hacktricks](https://github.com/HackTricks-wiki/hacktricks)** | «популярнейшая база по OSINT и хакингу, 12k★» | ⚠️ звёзд ~11.9k — да, но это **вики по пентесту/эксплуатации** (CTF, атаки на веб/AD/облака), **OSINT там мало**. Отличный ресурс, но по назначению это **hacking-методология**, не OSINT-каталог. Лицензии в репо нет |

## ✅ Что из этого реально стоит внимания

- **hacktricks** — маст-хэв как **пентест-справочник** (но именно пентест, не OSINT). Читать на [book.hacktricks.wiki](https://book.hacktricks.wiki).
- **Sitdeck** — если нужна карта мировых событий в одном окне (OSINT-мониторинг).
- **Master-OSINT-Toolkit** — как учебный набор скриптов, с оглядкой на застой и отсутствие лицензии.
- **Social Media Hacker List** — полезен, но как **список тулзов для соцсетей**, а не «пробив».
- Игру-симулятор — как развлечение, не как обучение.

> [!tip] В базе уже есть более сильные OSINT-заметки — начни с них
> По качеству/адаптации к твоим системам полезнее уже разобранное: [awesome-osint-arsenal](awesome-osint-arsenal%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20750%2B%20OSINT-recon-DFIR-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B5%D1%80%D0%B5%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%29.md) (установщик 750+ инструментов), [OSINT-Terminal](OSINT-Terminal%20%E2%80%94%20self-hosted%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%20%D0%B8%D0%B7%20438%20OSINT-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%B1%D0%B5%D0%B7%20API-%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B9%2C%203D-%D0%B3%D0%BB%D0%BE%D0%B1%D1%83%D1%81%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md) (дашборд 438 тулзов), [OpenSERP](OpenSERP%20%E2%80%94%20self-hosted%20SERP-API%20%D0%B8%20CLI%20%28Google-Yandex-Baidu%20%D0%B8%20%D0%B4%D1%80.%29%20%D0%B4%D0%BB%D1%8F%20OSINT%2C%20LLM%20%D0%B8%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md) (self-hosted SERP-API), [Argus](Argus%20%28lachydotmcg%29%20%E2%80%94%20self-OSINT%20%D1%81%D0%BA%D0%B0%D0%BD%D0%B5%D1%80%20%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%BE%D0%B3%D0%BE%20%D1%81%D0%BB%D0%B5%D0%B4%D0%B0%20%28username%20%2B%20Gemini-%D0%B4%D0%BE%D1%80%D0%BA%D0%B8%2C%20%D1%80%D0%B8%D1%81%D0%BA-%D0%BE%D1%82%D1%87%D1%91%D1%82%29.md) (self-OSINT — что о **тебе** в сети), [awesome-osint-chrome-extensions](awesome-osint-chrome-extensions%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D1%8B%D1%85%20%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B4%D0%BB%D1%8F%20OSINT%20%28Chrome-Brave%29.md).

## 🖥️ Применимость на системах владельца

| Ресурс | Где запускать |
| :--- | :--- |
| hacktricks / Social Media list | ✅ просто читаешь (веб/GitHub) с любой системы |
| Master-OSINT-Toolkit | ✅ Python на десктопе (Gentoo/Debian/Arch); на роутере Entware тяжёлые зависимости не нужны |
| Sitdeck | ✅ веб-сервис в браузере |

## 🔗 Связанные заметки

- [awesome-osint-arsenal — установщик 750+ инструментов](awesome-osint-arsenal%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20750%2B%20OSINT-recon-DFIR-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B5%D1%80%D0%B5%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%29.md) · [OSINT-Terminal — дашборд 438 тулзов](OSINT-Terminal%20%E2%80%94%20self-hosted%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%20%D0%B8%D0%B7%20438%20OSINT-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D0%B1%D0%B5%D0%B7%20API-%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%B9%2C%203D-%D0%B3%D0%BB%D0%BE%D0%B1%D1%83%D1%81%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md) · [OpenSERP — self-hosted SERP-API](OpenSERP%20%E2%80%94%20self-hosted%20SERP-API%20%D0%B8%20CLI%20%28Google-Yandex-Baidu%20%D0%B8%20%D0%B4%D1%80.%29%20%D0%B4%D0%BB%D1%8F%20OSINT%2C%20LLM%20%D0%B8%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md)
- [Argus — self-OSINT сканер цифрового следа](Argus%20%28lachydotmcg%29%20%E2%80%94%20self-OSINT%20%D1%81%D0%BA%D0%B0%D0%BD%D0%B5%D1%80%20%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%BE%D0%B3%D0%BE%20%D1%81%D0%BB%D0%B5%D0%B4%D0%B0%20%28username%20%2B%20Gemini-%D0%B4%D0%BE%D1%80%D0%BA%D0%B8%2C%20%D1%80%D0%B8%D1%81%D0%BA-%D0%BE%D1%82%D1%87%D1%91%D1%82%29.md) · [awesome-osint-chrome-extensions](awesome-osint-chrome-extensions%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D1%8B%D1%85%20%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B4%D0%BB%D1%8F%20OSINT%20%28Chrome-Brave%29.md)

## 🔗 Ссылки

- Репозитории/сервисы: [Social Media Hacker List](https://github.com/MobileFirstLLC/social-media-hacker-list) · [HackHub (Steam)](https://store.steampowered.com/app/2980270/HackHub__Ultimate_Hacker_Simulator/) · [Sitdeck](https://sitdeck.com/) · [Master-OSINT-Toolkit](https://github.com/techenthusiast167/Master-OSINT-Toolkit-) · [hacktricks](https://github.com/HackTricks-wiki/hacktricks)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26612)

#Security #OSINT #Разведка #Подборка #Право
