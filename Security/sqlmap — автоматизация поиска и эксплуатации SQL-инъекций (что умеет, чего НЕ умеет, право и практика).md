---
создал заметку: 2026-07-25T16:40:00
author: WhiteK0T
tags:
  - Pentest
  - SQLi
  - WebSecurity
  - Инструменты
  - OWASP
  - OpenSource
  - Безопасность
Источник:
  - https://github.com/sqlmapproject/sqlmap
  - https://sqlmap.org/
---

# 💉 sqlmap — автоматизация поиска и эксплуатации SQL-инъекций

**sqlmap** ([github.com/sqlmapproject/sqlmap](https://github.com/sqlmapproject/sqlmap)) — легендарная open-source утилита на **Python** для **автоматического обнаружения, верификации и эксплуатации SQL-инъекций** и захвата серверов БД. ~**38k★**, живёт с 2012 года, активно развивается, лицензия **GPLv2**. Де-факто отраслевой стандарт: берёт на себя рутину по подбору пейлоадов, определению СУБД и извлечению данных. SQLi годами держится в **OWASP Top 10**, так что инструмент актуален.

> [!warning] Правка к посту: MongoDB sqlmap НЕ поддерживает
> Пост пишет «…SQLite, **MongoDB** и десятками других». Это **ошибка**: в списке `SUPPORTED_DBMS` sqlmap **~30 SQL-СУБД**, но **MongoDB там нет**. MongoDB — **NoSQL**, и инъекции туда (NoSQLi) — **другой класс** уязвимостей и **другие инструменты** (NoSQLMap, `nosqli`). sqlmap умеет лишь *распознать* ошибку MongoDB по сигнатуре, но не эксплуатирует её. Всё остальное в посте — верно.

> [!info] Что реально поддерживается (проверено по исходникам)
> **~30 SQL-СУБД**: MySQL/MariaDB, PostgreSQL, Oracle, Microsoft SQL Server, SQLite, Microsoft Access, IBM DB2, Firebird, Sybase, SAP MaxDB, HSQLDB, H2, Informix, MonetDB, Apache Derby, Vertica, ClickHouse, CrateDB, Cubrid, Presto, Altibase, MimerSQL, Snowflake, Google Spanner, SAP HANA и др.
> **6 техник эксплуатации** (это точно): **Boolean-based blind**, **Time-based blind**, **Error-based**, **UNION query-based**, **Stacked queries**, **Out-of-band**.

## 🧰 Что умеет (подтверждено)

- **Автодетект СУБД** и оптимального вектора; тонкая настройка агрессивности (`--level`, `--risk`).
- **Дамп данных**: перечисление БД/таблиц/юзеров, выгрузка отдельных таблиц или всей базы (`--dbs`, `--tables`, `--dump`, `--dump-all`).
- **Крэк хешей паролей** встроенным словарным перебором (не «магия» — обычный dictionary-attack).
- **OS Takeover**: при высоких привилегиях у пользователя БД — заливка веб-шелла и **доступ к терминалу ОС** (`--os-shell`, `--os-pwn`), чтение/запись файлов (`--file-read`/`--file-write`).
- **Обход WAF**: tamper-скрипты (`--tamper=...`), прокси/Tor, кастомные заголовки, задержки.

```bash
# Клонируем официальный репозиторий (только оф. источник!)
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
# Проверка параметра и список БД
python3 sqlmap-dev/sqlmap.py -u "http://example.com/page.php?id=1" --dbs
```

## ⚖️ Право (РФ) — это боевой инструмент захвата БД, не «сканер для интереса»

> [!danger] Использовать ТОЛЬКО против своих/разрешённых целей
> Описание самого проекта — «database **takeover** tool». Запуск sqlmap по **чужому** сайту без письменного разрешения — это:
> - **ст. 272 УК РФ** (неправомерный доступ к компьютерной информации) — уже сам факт дампа чужой БД;
> - **ст. 273 УК РФ** (создание/использование ВПО) — применение эксплойт-функций, `--os-shell`;
> - при повреждении/утечке персональных данных добавляется **152-ФЗ** и профильные статьи.
>
> **Легально**: свои стенды и **явно авторизованный пентест по договору** (с указанием scope). Всё остальное — состав преступления, «я просто проверял» не оправдание.

## 🧪 Факты против хайпа

> [!caution] «Король ИБ в один клик» — с оговорками
> - **Шумный.** Активно палится WAF/IDS, может **заблокировать твой IP** и наследить в логах. Для реального теста нужны tamper-скрипты, тайминги, аккуратность.
> - **Разрушительный потенциал.** `--dump-all`, stacked-queries и `--os-*` могут **повредить данные/сервис** цели — на проде авторизованного теста включай осторожно, согласуй scope.
> - **Не всесилен.** Бывают ложные срабатывания/пропуски; blind-техники (особенно **time-based**) **медленные**; сложные защиты требуют ручной настройки `--level/--risk/--technique/--tamper`. Инструмент ускоряет рутину, но **не заменяет понимание** SQLi.
> - **Тренируйся легально**: DVWA, OWASP Juice Shop, `testphp.vulnweb.com`, свои уязвимые стенды — см. идею изолированных лабораторий у [WifiForge](WifiForge%20%28Black%20Hills%20InfoSec%29%20%E2%80%94%20%D0%B2%D0%B8%D1%80%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F%20Wi-Fi-%D0%BF%D0%B5%D0%BD%D1%82%D0%B5%D1%81%D1%82%D1%83%20%28mininet-wifi%2C%20%D0%B1%D0%B5%D0%B7%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%B0%29.md).

## 🖥️ Установка на системах владельца

sqlmap — чистый Python, работает везде, где есть Python 3 (поддерживается и 2.7):

| Система | Как поставить |
| :--- | :--- |
| **Gentoo (основная)** | проще всего `git clone` официального репо (свежак) или `pipx install sqlmap`; проверь также портежный пакет |
| **Debian / Ubuntu** | `sudo apt install sqlmap` (в репозиториях) — но версия отстаёт; для актуальной — git-клон |
| **Arch** | `sudo pacman -S sqlmap` (extra/community) или из git |
| **Entware / RT-AX56U** | Python на роутере есть → sqlmap **технически запустится** (armv7), но тяжёлые сканы с роутера непрактичны; не основной кейс |

> [!tip] Держи актуальную версию
> Пейлоады/техники и tamper-скрипты постоянно обновляются. Рабочий вариант — **git-клон и `git pull`** (или запуск с `--update`), а не годичной давности пакет из дистрибутива.

## 🔗 Связанные заметки

- Реальная SQLi-цепочка в дикой природе (SQLi как звено RCE): [wp2shell — RCE в ядре WordPress](Vulns/Apps/wp2shell%20%E2%80%94%20pre-auth%20RCE%20%D0%B2%20%D1%8F%D0%B4%D1%80%D0%B5%20WordPress%20%28batch%20REST%20route-confusion%20%2B%20SQLi%2C%20CVE-2026-63030%20%D0%B8%2060137%29.md)
- Мультиагентный ИИ-фреймворк для offensive security (тот же дуал-юз + право): [T3MP3ST](T3MP3ST%20%E2%80%94%20%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D1%8B%D0%B9%20%D0%98%D0%98-%D1%84%D1%80%D0%B5%D0%B9%D0%BC%D0%B2%D0%BE%D1%80%D0%BA%20%D0%B4%D0%BB%D1%8F%20offensive%20security%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D1%83%D0%BC%D0%B5%D0%B5%D1%82%2C%20%D1%84%D0%B0%D0%BA%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D1%85%D0%B0%D0%B9%D0%BF%D0%B0%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md)
- Изолированная лаборатория для легальной тренировки (идея): [WifiForge](WifiForge%20%28Black%20Hills%20InfoSec%29%20%E2%80%94%20%D0%B2%D0%B8%D1%80%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F%20Wi-Fi-%D0%BF%D0%B5%D0%BD%D1%82%D0%B5%D1%81%D1%82%D1%83%20%28mininet-wifi%2C%20%D0%B1%D0%B5%D0%B7%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%B0%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/sqlmapproject/sqlmap](https://github.com/sqlmapproject/sqlmap) (GPLv2) · сайт: [sqlmap.org](https://sqlmap.org/)
- Практика легально: [DVWA](https://github.com/digininja/DVWA) · [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)

#Pentest #SQLi #WebSecurity #Инструменты #OWASP #OpenSource #Безопасность
