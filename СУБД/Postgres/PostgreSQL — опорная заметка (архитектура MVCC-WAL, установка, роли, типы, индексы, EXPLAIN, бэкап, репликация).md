---
создал заметку: 2026-07-23T13:00:00
author: WhiteK0T
tags:
  - PostgreSQL
  - СУБД
  - Database
  - SQL
  - MVCC
  - WAL
  - DevOps
  - Architecture
Источник:
  - https://www.postgresql.org/docs/current/
  - https://www.postgresql.org/about/news/postgresql-18-released-3142/
---

# 🐘 PostgreSQL — опорная заметка

**PostgreSQL** (Postgres) — свободная объектно-реляционная СУБД с 30+ годами разработки, лицензия PostgreSQL License (BSD-подобная, разрешает всё). Ставка проекта — **строгое соответствие стандарту SQL, надёжность (ACID) и расширяемость**: типы, функции, индексы, языки процедур можно добавлять, не трогая ядро. Это «дефолтная» реляционка для новых проектов, если нет причины взять другую.

> [!info] Postgres vs MySQL — одной строкой
> Postgres исторически строже к стандарту, богаче на типы (`jsonb`, массивы, диапазоны, гео), сильнее в сложных запросах, оконных функциях, CTE и расширениях (PostGIS, Citus). MySQL/MariaDB проще и местами быстрее на примитивном OLTP-чтении. Для «правильной» бизнес-логики и аналитики по умолчанию берут Postgres.

---

## 🧱 Актуальные версии (на июль 2026)

| Ветка | Статус | Примечание |
| :--- | :--- | :--- |
| **18.x** (18.4) | **текущая стабильная** | вышла 25 сен 2025; крупные новшества — **асинхронный I/O** (`io_method`, до ~3× на seq scan/vacuum), **`uuidv7()`** (сортируемые UUID → лучше как PK), OAuth-аутентификация, **быстрый `pg_upgrade`** с сохранением статистики планировщика, skip-scan для B-tree, виртуальные генерируемые столбцы |
| 17 / 16 / 15 / 14 | поддерживаются | получают только багфиксы/секьюрити |
| **19** | **beta** | релиз ожидается ~сентябрь-октябрь 2026 |

> [!note] Политика версий
> Мажорная версия выходит раз в год (осенью), поддерживается **5 лет**. Минорные (`18.1`, `18.2`…) — только исправления, ставятся без миграции данных. Апгрейд мажора — `pg_upgrade` (быстрый, in-place) либо `pg_dump`/`pg_restore` (медленно, но надёжно и меняет формат).

---

## ⚙️ Архитектура (что происходит внутри)

### Процессная модель
Postgres — **мультипроцессный** (не потоки): главный процесс `postmaster` форкает **отдельный backend-процесс на каждое клиентское подключение**. Отсюда важное следствие: **соединения дорогие** (память + fork), поэтому при сотнях клиентов почти всегда нужен **пул соединений** (PgBouncer — см. ниже). Плюс фоновые служебные процессы: `autovacuum launcher`, `background writer`, `checkpointer`, `WAL writer`, `archiver`, `walsender`/`walreceiver` (репликация).

### MVCC — многоверсионность
Каждая транзакция видит **согласованный снимок** данных. При `UPDATE`/`DELETE` строка не переписывается на месте, а создаётся **новая версия**, старая помечается «мёртвой» (dead tuple) и живёт, пока её видят другие транзакции. Читатели не блокируют писателей и наоборот. Плата — **раздувание (bloat)** и потребность в `VACUUM`.

> [!tip] Про уборку мёртвых строк — отдельная заметка
> Как bloat возникает, чем `VACUUM` отличается от `VACUUM FULL`, autovacuum и `pg_repack` — подробно в [VACUUM FULL — обслуживание PostgreSQL (bloat, dead tuples)](VACUUM%20FULL%20%E2%80%94%20%D0%B2%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%82%20%D0%BC%D0%B5%D1%81%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%B4%D0%B8%D1%81%D0%BA%D0%B5%20%D0%B2%20PostgreSQL%20%28bloat%2C%20dead%20tuples%2C%20pg_repack%29.md).

### WAL — журнал упреждающей записи
Перед изменением страниц данных Postgres пишет запись в **WAL (Write-Ahead Log)**. Это фундамент **надёжности (durability, буква D в ACID)** и одновременно основа **репликации и PITR**:
- при `COMMIT` фиксируется именно WAL → после сбоя БД доигрывает журнал и восстанавливается;
- **checkpoint** периодически сбрасывает грязные страницы на диск;
- WAL-поток можно **стримить на реплику** или **архивировать** для восстановления на точку во времени.

### Память
- **`shared_buffers`** — общий кэш страниц (ориентир ~25 % RAM на выделенном сервере);
- **`work_mem`** — память на операцию сортировки/хеша **на каждый узел плана** (осторожно: умножается на число операций × соединений);
- **`maintenance_work_mem`** — под `VACUUM`, `CREATE INDEX`;
- **`effective_cache_size`** — подсказка планировщику, сколько всего кэша (ОС + Postgres) доступно (не выделяет память, влияет на выбор плана).

### Хранение
Кластер БД живёт в **`PGDATA`** (каталог данных). Логически: **кластер → базы → схемы → таблицы**. `schema` — пространство имён внутри БД (по умолчанию `public`); удобно для мультиарендности и организации.

---

## 📦 Установка (все 4 платформы владельца)

| Система | Установка | Инициализация кластера | Служба |
| :--- | :--- | :--- | :--- |
| **Gentoo** (основная) | `emerge dev-db/postgresql` (слот версии; USE-флаги: `server`, `ssl`, `nls`, `icu`, опц. `python`/`perl` для PL-языков) | `emerge --config dev-db/postgresql:18` создаёт кластер в `/var/lib/postgresql/18/data` | **OpenRC**: `rc-service postgresql-18 start`, `rc-update add postgresql-18 default`; конфиг службы — `/etc/conf.d/postgresql-18` |
| **Debian / Ubuntu** | `apt install postgresql postgresql-contrib` (свежие ветки — из репозитория **PGDG** `apt.postgresql.org`) | кластер создаётся автоматически при установке; управление — `pg_ctlcluster` / `pg_lsclusters` | **systemd**: `systemctl enable --now postgresql`; конфиги в `/etc/postgresql/18/main/` |
| **Arch** (план с июня 2026) | `pacman -S postgresql` | вручную от пользователя `postgres`: `initdb -D /var/lib/postgres/data --locale=ru_RU.UTF-8` | **systemd**: `systemctl enable --now postgresql` |
| **Entware / RT-AX56U** | `opkg install postgresql postgresql-cli` (armv7) | `initdb` в каталог на **USB-диске** (не во flash!), напр. `/opt/var/lib/pgsql` | init-скрипт `/opt/etc/init.d/S*postgresql` |

> [!caution] Entware / роутер — только учебный стенд
> 512 МБ RAM и слабый armv7 у RT-AX56U годятся лишь «пощупать» одиночный Postgres. **`PGDATA` держи на USB-диске**, а не во внутренней flash (256 МБ, ограниченный ресурс перезаписи). Продовые нагрузки, репликация, тяжёлые расширения (PostGIS собирается тяжело) — не для этого железа; тренируйся на десктопе/VPS.

> [!tip] Docker — быстрее всего пощупать
> `docker run -d --name pg -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres:18` — готовый кластер за секунды, удобно для экспериментов и CI. Данные — в volume (`-v pgdata:/var/lib/postgresql/data`), иначе исчезнут с контейнером.

### Первый вход
```bash
sudo -u postgres psql          # системный суперюзер postgres, вход по peer-аутентификации
```
```sql
CREATE ROLE app LOGIN PASSWORD 'секрет';
CREATE DATABASE appdb OWNER app;
\c appdb                        -- переключиться на базу
```

---

## 🔐 Аутентификация и роли

### pg_hba.conf — кто, откуда, как
Файл **`pg_hba.conf`** (Host-Based Authentication) решает **кому разрешено** подключаться — правила читаются сверху вниз, первое совпадение выигрывает:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
local   all       all                   peer          # локально по имени ОС-пользователя
host    appdb     app   127.0.0.1/32    scram-sha-256  # по паролю, TCP
host    all       all   0.0.0.0/0       reject         # остальных — отказ
```

> [!warning] Не оставляй `trust` и `md5`
> Метод **`trust`** пускает **без пароля кого угодно** — только для локальной отладки, никогда не в проде/сети. Пароли — только **`scram-sha-256`** (современный, стойкий); устаревший `md5` уводи. После правки `pg_hba.conf` нужен **`reload`** (не рестарт): `SELECT pg_reload_conf();` или `systemctl reload postgresql`.

### Роли и права
В Postgres **пользователь = роль** с флагом `LOGIN`. Роли можно вкладывать (роль-группа + роли-члены), выдавать гранулярные права:

```sql
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly;
-- Row-Level Security — доступ построчно (мультиарендность)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_iso ON orders USING (tenant_id = current_setting('app.tenant')::int);
```

---

## 🧬 Типы данных — сильная сторона Postgres

| Категория | Типы | Заметка |
| :--- | :--- | :--- |
| Числа | `smallint`, `integer`, `bigint`, `numeric(p,s)`, `real`, `double precision` | `numeric` — точная арифметика (деньги!), не `float` |
| Строки | `text`, `varchar(n)`, `char(n)` | почти всегда бери **`text`** — без искусственного лимита, скорость та же |
| Дата/время | `timestamptz`, `date`, `time`, `interval` | **всегда `timestamptz`** (с таймзоной), не голый `timestamp` |
| Идентификаторы | `uuid` (+ `gen_random_uuid()`, **`uuidv7()` в PG18**), `bigserial`/`GENERATED … AS IDENTITY` | UUIDv7 сортируемый → дружелюбнее к B-tree, чем случайный v4 |
| Структуры | **`jsonb`**, массивы `int[]`, `hstore`, `range`/`multirange`, композитные | `jsonb` — бинарный JSON, индексируется GIN; для полу-структурных данных |
| Прочее | `boolean`, `inet`/`cidr`/`macaddr`, `bytea`, `enum`, `tsvector` (полнотекст), `geometry` (PostGIS) | сетевые и гео-типы — из коробки/расширением |

> [!tip] JSONB, а не JSON
> `jsonb` хранит разобранное бинарное представление (быстрый доступ, операторы `->`, `->>`, `@>`, индекс GIN). Тип `json` хранит сырой текст — берут редко (когда важен точный исходный формат/порядок ключей). Но не превращай Postgres в документную БД: если данные реляционные — держи их в столбцах.

---

## 🔎 Индексы

Индекс ускоряет чтение ценой замедления записи и места на диске. Типы под разные задачи:

| Тип | Для чего | Пример |
| :--- | :--- | :--- |
| **B-tree** (по умолчанию) | равенство и диапазоны `=`, `<`, `>`, `BETWEEN`, `ORDER BY` | `CREATE INDEX ON users(email);` |
| **GIN** | «много значений в одном поле» — `jsonb`, массивы, полнотекст | `CREATE INDEX ON docs USING gin(payload);` |
| **GiST** | геометрия, диапазоны, ближайшие соседи (KNN) | гео-поиск, `range`-перекрытия |
| **BRIN** | огромные таблицы, естественно упорядоченные (время, id) | крошечный индекс на млрд строк по `created_at` |
| **Hash** | только строгое `=` | редко нужен (B-tree обычно не хуже) |

Дополнительно — **частичные** (`WHERE deleted = false`), **по выражению** (`lower(email)`), **покрывающие** (`INCLUDE (…)` — index-only scan), **составные** (порядок столбцов важен: сначала по чему фильтруешь на равенство).

> [!warning] Индекс — не бесплатный
> Каждый индекс замедляет `INSERT`/`UPDATE`/`DELETE` и жрёт диск. Не индексируй «на всякий случай». Ненужные/дублирующие индексы ищи через `pg_stat_user_indexes` (`idx_scan = 0`). Создание в проде — `CREATE INDEX CONCURRENTLY` (не блокирует запись, но медленнее).

---

## 📊 EXPLAIN — как читается план запроса

Планировщик Postgres **стоимостный**: выбирает план по оценкам. Смотреть, что реально произошло:

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123;
```

- **`EXPLAIN`** — только предполагаемый план и оценки; **`ANALYZE`** — реально выполняет и показывает фактическое время/строки; **`BUFFERS`** — сколько страниц из кэша/с диска.
- Красные флаги: **`Seq Scan`** по большой таблице там, где ждёшь индекс; **сильное расхождение** оценки `rows` и факта (устаревшая статистика → `ANALYZE table;`); дорогой `Sort` на диске (мал `work_mem`); вложенные циклы на больших наборах.
- `Index Scan` / `Index Only Scan` — хорошо; `Bitmap Heap Scan` — норм для средней селективности.

> [!tip] Статистика планировщика
> Планы зависят от статистики распределения данных, которую собирает `ANALYZE` (и autovacuum). После массовой загрузки данных — запусти `ANALYZE` вручную, иначе планировщик «слепой». `pg_stat_statements` (расширение) покажет самые дорогие/частые запросы на проде — включай первым делом.

---

## 🔄 Транзакции и уровни изоляции

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;      -- либо ROLLBACK; всё или ничего (атомарность)
```

| Уровень изоляции | Что предотвращает | Postgres |
| :--- | :--- | :--- |
| **Read Committed** (по умолчанию) | грязное чтение | каждая команда видит свежий снимок |
| **Repeatable Read** | + неповторяемое чтение, фантомы | снимок на всю транзакцию (реально это snapshot isolation) |
| **Serializable** | + аномалии сериализации (SSI) | как будто транзакции шли по очереди; может откатить с `serialization_failure` — приложение должно **повторить** |

> [!note] Deadlock и блокировки
> Postgres сам обнаруживает взаимоблокировки и откатывает одну из транзакций (`deadlock_timeout`). Явные блокировки — `SELECT … FOR UPDATE` (пессимистично) или версия-столбец/`xmin` (оптимистично). Долгие открытые транзакции **держат dead tuples** и мешают autovacuum — не оставляй `BEGIN` висеть; следи за `pg_stat_activity` (`state = 'idle in transaction'`).

---

## 💾 Резервное копирование и восстановление

| Способ | Что делает | Когда |
| :--- | :--- | :--- |
| **`pg_dump`** | логический дамп одной БД (SQL или `-Fc` custom) | переносимо между версиями/платформами; восстановление `pg_restore` |
| **`pg_dumpall`** | + роли и глобальные объекты всего кластера | полный логический бэкап |
| **`pg_basebackup`** | физическая копия каталога кластера | основа реплики и PITR |
| **PITR** (WAL-архив) | базовая копия + непрерывный архив WAL → откат на **любую точку во времени** | прод, минимизация потери данных (RPO→секунды) |

```bash
pg_dump -Fc appdb > appdb.dump                 # бэкап
pg_restore -d appdb_new appdb.dump             # восстановление
pg_basebackup -D /backup/base -Fp -Xs -P       # физическая базовая копия
```

> [!caution] «Бэкап есть» ≠ «бэкап работает»
> Регулярно **проверяй восстановление** на отдельном хосте. Дамп, который никогда не разворачивали, — это гипотеза, а не бэкап. Для прода — `pg_basebackup` + архив WAL (или готовые pgBackRest / barman), а не только ночной `pg_dump`.

---

## 🌐 Репликация и масштабирование

- **Физическая (streaming) репликация** — реплика получает поток WAL и применяет его байт-в-байт. Реплики **read-only** (hot standby) → масштабируют **чтение** и дают отказоустойчивость. Синхронная (ждём подтверждения реплики, нет потерь) или асинхронная (быстрее, возможна потеря последних транзакций при аварии).
- **Логическая репликация** (`CREATE PUBLICATION` / `SUBSCRIPTION`) — по таблицам, между **разными мажорными версиями**; годится для апгрейда с минимальным простоем и выборочной репликации.
- **Автопереключение (failover)** штатно Postgres **не делает** — нужен внешний оркестратор: **Patroni** (+ etcd/Consul), repmgr, pg_auto_failover.
- **Горизонтальное масштабирование записи (шардинг)** из коробки нет — берут расширение **Citus** или distributed SQL. Подробно — в [Шардирование БД — shard key, hot shard, cross-shard, Citus](../%D0%A8%D0%B0%D1%80%D0%B4%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%91%D0%94%20%E2%80%94%20%D0%B7%D0%B0%D1%87%D0%B5%D0%BC%2C%20shard%20key%2C%20hot%20shard%2C%20cross-shard%20%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D1%8B%20%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B2%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%D1%82%D1%8C%20%28Citus%2C%20routing%20layer%29.md).

> [!tip] Пул соединений обязателен под нагрузкой
> Из-за «процесс на соединение» сотни коннектов = сотни backend-процессов = память кончилась. Ставь **PgBouncer** (лёгкий, режим `transaction` — один серверный коннект обслуживает много клиентских между транзакциями). Обычно PgBouncer живёт рядом с приложением или на сервере БД.

---

## 🧩 Расширения — киллер-фича

`CREATE EXTENSION` добавляет функциональность без правки ядра:

- **`pg_stat_statements`** — статистика по запросам (ставь первым);
- **PostGIS** — геоданные (де-факто стандарт ГИС);
- **`pgcrypto`** — хеши/шифрование; **`uuid-ossp`** — UUID (в PG18 многое уже в ядре);
- **`pg_trgm`** — нечёткий поиск / `LIKE '%...%'` по индексу;
- **Citus** — распределённые таблицы (шардинг);
- **TimescaleDB** — временные ряды; **pgvector** — векторный поиск для эмбеддингов/RAG.

---

## 🛠️ Управление службой и psql

```bash
# systemd (Debian/Ubuntu/Arch)
systemctl status  postgresql
systemctl reload  postgresql     # применить postgresql.conf / pg_hba.conf без разрыва сессий

# OpenRC (Gentoo)
rc-service postgresql-18 restart
rc-update add postgresql-18 default
```

Полезное в `psql`:
```
\l            список баз            \dt      таблицы
\c dbname     подключиться          \d table описание таблицы
\du           роли                  \di      индексы
\x            расширенный вывод      \timing  показывать время запросов
\e            открыть запрос в $EDITOR       \q  выход
```

> [!note] reload vs restart
> Большинство параметров `postgresql.conf` подхватываются по **`reload`**. Но часть (`shared_buffers`, `max_connections`, `wal_level`, `listen_addresses`) требует **полного `restart`** — колонка `pending_restart` в `pg_settings` подскажет, что ещё не применилось.

---

## 💡 Практические выводы

- Для нового проекта Postgres — разумный дефолт: стандарт SQL, надёжность, богатые типы, расширения.
- **Пиши `timestamptz`, `text`, `numeric` для денег, `jsonb` (не `json`)** — избежишь классических граблей.
- Три вещи, которые окупаются сразу: **`pg_stat_statements`**, продуманные **индексы под реальные запросы**, регулярно **проверяемый бэкап**.
- Помни про MVCC: настрой **autovacuum**, не держи долгие транзакции, следи за bloat ([VACUUM FULL — обслуживание PostgreSQL (bloat, dead tuples)](VACUUM%20FULL%20%E2%80%94%20%D0%B2%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%82%20%D0%BC%D0%B5%D1%81%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%B4%D0%B8%D1%81%D0%BA%D0%B5%20%D0%B2%20PostgreSQL%20%28bloat%2C%20dead%20tuples%2C%20pg_repack%29.md)).
- Под нагрузкой — **пул соединений** (PgBouncer) и, при упоре в один сервер, реплики чтения → и лишь потом шардинг ([Шардирование БД — shard key, hot shard, cross-shard, Citus](../%D0%A8%D0%B0%D1%80%D0%B4%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%91%D0%94%20%E2%80%94%20%D0%B7%D0%B0%D1%87%D0%B5%D0%BC%2C%20shard%20key%2C%20hot%20shard%2C%20cross-shard%20%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D1%8B%20%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B2%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%D1%82%D1%8C%20%28Citus%2C%20routing%20layer%29.md)).

## 🔗 Ссылки

- Официально: [PostgreSQL Docs (current)](https://www.postgresql.org/docs/current/) · [Release notes 18](https://www.postgresql.org/docs/release/18.0/)
- Связанные заметки: [VACUUM FULL — обслуживание PostgreSQL (bloat, dead tuples)](VACUUM%20FULL%20%E2%80%94%20%D0%B2%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%82%20%D0%BC%D0%B5%D1%81%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%B4%D0%B8%D1%81%D0%BA%D0%B5%20%D0%B2%20PostgreSQL%20%28bloat%2C%20dead%20tuples%2C%20pg_repack%29.md) · [Шардирование БД — shard key, hot shard, cross-shard, Citus](../%D0%A8%D0%B0%D1%80%D0%B4%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%91%D0%94%20%E2%80%94%20%D0%B7%D0%B0%D1%87%D0%B5%D0%BC%2C%20shard%20key%2C%20hot%20shard%2C%20cross-shard%20%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D1%8B%20%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B2%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%D1%82%D1%8C%20%28Citus%2C%20routing%20layer%29.md)

#PostgreSQL #СУБД #Database #SQL #MVCC #WAL #DevOps #Architecture
