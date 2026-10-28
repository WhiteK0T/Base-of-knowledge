---
создал заметку: 2026-10-28T21:40:00
author: WhiteK0T
tags:
  - PostgreSQL
  - psql
  - СУБД
  - SQL
  - CLI
  - DevOps
  - Шпаргалка
Источник:
  - https://www.postgresql.org/docs/current/app-psql.html
  - https://www.postgresql.org/docs/current/libpq-connect.html
  - https://www.postgresql.org/docs/current/libpq-pgpass.html
  - https://www.postgresql.org/docs/current/libpq-pgservice.html
  - https://www.postgresql.org/docs/current/sql-copy.html
  - https://www.postgresql.org/docs/release/18.0/
---

# 🐘 psql — шпаргалка: подключение, метакоманды, вывод, импорт-экспорт и скрипты

**psql** — штатный консольный клиент PostgreSQL. Он принимает ввод двух видов:

- **SQL** — psql отправляет его на сервер; команда заканчивается `;` (или `\g`) и может занимать несколько строк;
- **метакоманды** `\…` — их выполняет сам psql; они заканчиваются концом строки, `;` после них не нужна.

Именно метакоманды делают psql удобнее голого драйвера: описание объектов (`\d`), форматы вывода, переменные и условия, `\copy` между файлом на твоей машине и таблицей на сервере.

Все команды и запросы ниже проверены на **psql 18.6** с тестовым кластером PostgreSQL 18.6 (база `shop`, таблицы `customers` и `orders`); выводы в блоках — настоящие. Пакеты сверены с Gentoo, Debian/Ubuntu, Arch и фидом Entware. Архитектура, роли, индексы и бэкапы — в [опорной заметке по PostgreSQL](PostgreSQL%20%E2%80%94%20%D0%BE%D0%BF%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BA%D0%B0%20%28%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0%20MVCC-WAL%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D1%80%D0%BE%D0%BB%D0%B8%2C%20%D1%82%D0%B8%D0%BF%D1%8B%2C%20%D0%B8%D0%BD%D0%B4%D0%B5%D0%BA%D1%81%D1%8B%2C%20EXPLAIN%2C%20%D0%B1%D1%8D%D0%BA%D0%B0%D0%BF%2C%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%29.md).

> [!tip] Версия psql — не ниже версии сервера
> Со **старыми** серверами psql работает без проблем: метакоманды `\d` поддерживают серверы вплоть до 9.2. С сервером **новее** клиента метакоманды могут выдавать ошибки. В 18-й версии к тому же изменилась обработка `\.` в CSV, и release notes предупреждают: у старых клиентов с сервером 18 возможны проблемы с `\copy`. Ставь клиент той же версии, что и сервер, или новее.

## 🔌 Подключение

| Способ | Команда |
| :--- | :--- |
| Ключи | `psql -h db.example.com -p 5432 -U app -d shop` |
| URI | `psql "postgresql://app@db.example.com:5432/shop?sslmode=verify-full"` |
| Строка «ключ=значение» | `psql "host=db.example.com dbname=shop user=app sslmode=require"` |
| Локально, суперпользователем | `sudo -u postgres psql` — вход по `peer`: имя пользователя ОС = имя роли |
| Именованный сервис | `psql service=shop` (файл `~/.pg_service.conf`, ниже) |
| В Docker-контейнере | `docker exec -it pg psql -U postgres -d shop` |
| Список баз и выход | `psql -l` |
| Одна команда и выход | `psql -d shop -c 'SELECT now()'` |

Без параметров psql подключается через локальный Unix-сокет; роль совпадает с именем пользователя ОС, а **база — с именем роли**. Отсюда частая ошибка `FATAL: database "ivan" does not exist`: укажи базу явно — `psql -d postgres`.

### 🔑 Пароли

```bash
# ~/.pgpass — хост:порт:база:роль:пароль, * — любое значение
cat > ~/.pgpass <<'EOF'
db.example.com:5432:shop:app:S3cret
localhost:5432:*:postgres:0ther#pass
EOF
chmod 600 ~/.pgpass
```

- Права — **строго 0600**, иначе libpq пропускает файл: `WARNING: password file "…/.pgpass" has group or world access; permissions should be u=rw (0600) or less`. Другой файл — `PGPASSFILE=/path`.
- `PGPASSWORD=… psql` тоже работает, но пароль виден процессам того же пользователя и root (`/proc/<pid>/environ`) и оседает в истории shell — `.pgpass` надёжнее.
- `-W` — запросить пароль сразу, `-w` — **никогда не спрашивать**. В cron и CI с `-w` psql не зависнет на вопросе о пароле, а сразу выйдет с ошибкой `fe_sendauth: no password supplied` и кодом 2.

### 🌍 Переменные окружения

Это переменные libpq — их понимают и `pg_dump`, `pg_restore`, `pg_isready`, и драйверы на базе libpq.

| Переменная | Что задаёт |
| :--- | :--- |
| `PGHOST`, `PGPORT`, `PGUSER`, `PGDATABASE` | то же, что `-h`, `-p`, `-U`, `-d` |
| `PGPASSFILE` | файл паролей вместо `~/.pgpass` |
| `PGSERVICE`, `PGSERVICEFILE` | имя сервиса и файл сервисов |
| `PGSSLMODE` | `disable`, `prefer` (по умолчанию: TLS, если сервер умеет, иначе без него), `require`, `verify-ca`, `verify-full` (проверка сертификата и имени хоста) |
| `PGAPPNAME` | имя программы в `pg_stat_activity.application_name` |
| `PGCONNECT_TIMEOUT` | таймаут подключения в секундах |
| `PGOPTIONS` | параметры сессии: `PGOPTIONS='-c statement_timeout=5s' psql …` |

### 📇 Файл сервисов

```ini
# ~/.pg_service.conf
[shop]
host=db.example.com
port=5432
dbname=shop
user=app
sslmode=verify-full
```

Подключение — `psql service=shop` или `PGSERVICE=shop psql`. Пароль по-прежнему берётся из `.pgpass`. В psql 18 имя сервиса доступно в переменной `:SERVICE` и в приглашении (`%s`).

### 🚇 SSH-туннель и несколько хостов

```bash
# порт сервера наружу не открыт — пробрасываем его по SSH
ssh -N -L 5433:localhost:5432 user@<IP-сервера> &
psql -h localhost -p 5433 -U app -d shop

# перебрать хосты по порядку и остаться на том, что принимает запись (primary)
psql "host=pg1,pg2 port=5432 dbname=shop target_session_attrs=read-write connect_timeout=3"
```

Подробнее о пробросе портов — в [визуальном руководстве по SSH-туннелям](../../Network/SSH/SSH-%D0%92%D0%B8%D0%B7%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE%20%D0%BF%D0%BE%20%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8F%D0%BC.md).

### Внутри psql

| Команда | Что делает |
| :--- | :--- |
| `\c shop` | переключиться на базу `shop` |
| `\c shop app` | на базу и роль |
| `\c - - pg2 5433` | `-` означает «оставить как есть»: сменить только хост и порт |
| `\conninfo` | текущее подключение; в 18 — таблица: база, роль, хост, порт, SSL, PID процесса, суперпользователь ли |
| `\password app` | сменить пароль: psql сам вычисляет SCRAM-хеш, и в историю и журнал сервера попадает только хеш — в отличие от `ALTER ROLE app PASSWORD '…'` |

```
      Connection Information
      Parameter       |   Value
----------------------+-----------
 Database             | shop
 Client User          | app
 Host                 | 127.0.0.1
 Server Port          | 54329
 Options              |
 Protocol Version     | 3.0
 Password Used        | true
 GSSAPI Authenticated | false
 Backend PID          | 718614
 SSL Connection       | false
 Superuser            | off
 Hot Standby          | off
(12 rows)
```

## 🗂️ Что есть в базе: метакоманды `\d`

| Команда | Что показывает |
| :--- | :--- |
| `\l`, `\l+` | базы; с `+` — ещё размер и табличное пространство |
| `\dn` | схемы |
| `\dt`, `\dt+` | таблицы; с `+` — размер и метод доступа |
| `\d orders` | столбцы, индексы, ограничения, внешние ключи |
| `\d+ orders` | плюс хранение столбцов, статистика, комментарии |
| `\di`, `\dv`, `\dm`, `\ds` | индексы, представления, материализованные представления, последовательности |
| `\df имя` | функции; `\dfp` — только процедуры, `\dft` — только триггерные |
| `\sf имя`, `\sv имя` | исходник функции, определение представления (`\df+` с версии 16 исходник не показывает) |
| `\du` | роли и их атрибуты |
| `\drg` | кто в какой роли состоит (с 16; из `\du` эта колонка убрана) |
| `\dp orders` (= `\z`) | права на таблицы, представления, последовательности |
| `\ddp` | права по умолчанию (`ALTER DEFAULT PRIVILEGES`) |
| `\dx` | установленные расширения (в 18 — и версия по умолчанию) |
| `\dconfig`, `\dconfig *timeout*` | параметры сервера, отличные от умолчаний; с шаблоном — любые (с 15) |
| `\dT`, `\dD` | типы, домены |
| `\dP` | секционированные таблицы и индексы |
| `\dRp`, `\dRs` | публикации и подписки логической репликации |
| `\h CREATE INDEX` | синтаксис SQL-команды; `\h` — список всех |
| `\?` | все метакоманды; `\? variables` — спецпеременные, `\? options` — ключи запуска |

**Модификаторы** пишутся слитно с командой: `+` — больше подробностей, `S` — включить системные объекты (`\dfS`, `\dtS`), `x` — развёрнутый вывод (с 18: `\dtx`, `\lx+`).

**Шаблоны:** `\dt public.*` — все таблицы схемы, `\dt *order*` — по подстроке, `\df app.calc_*`, `\d "Orders"` — имя в двойных кавычках, если в нём есть заглавные буквы.

```
shop=> \d orders
                               Table "public.orders"
   Column    |     Type      | Collation | Nullable |           Default
-------------+---------------+-----------+----------+------------------------------
 id          | bigint        |           | not null | generated always as identity
 customer_id | integer       |           |          |
 amount      | numeric(10,2) |           |          |
 status      | text          |           |          |
 created_at  | date          |           |          |
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
    "orders_customer_id_idx" btree (customer_id)
Foreign-key constraints:
    "orders_customer_id_fkey" FOREIGN KEY (customer_id) REFERENCES customers(id)
```

## ⌨️ Ввод, выполнение, история

| Команда | Что делает |
| :--- | :--- |
| `\e` | открыть текущий (или последний) запрос в `$PSQL_EDITOR` / `$EDITOR`; после сохранения и выхода запрос выполнится |
| `\ef имя`, `\ev имя` | открыть в редакторе определение функции / представления |
| `\p`, `\r` | показать / очистить буфер запроса |
| `\i файл.sql`, `\ir файл.sql` | выполнить файл; `\ir` ищет путь относительно текущего скрипта |
| `\o файл.txt` … `\o` | направить весь вывод в файл / вернуть на экран |
| `\g файл.txt` | выполнить запрос, результат записать в файл |
| `\g (format=csv tuples_only) имя.csv` | то же с разовыми настройками вывода |
| `\gx` | выполнить с развёрнутым выводом (только этот запрос) |
| `\gdesc` | показать столбцы и типы результата, **не выполняя** запрос |
| `\watch 5` | повторять запрос каждые 5 с; `\watch i=0.5 c=10` — 10 раз (`c=` с 16), `m=1` — остановиться, когда строк станет меньше одной (с 17) |
| `\timing on` | показывать время каждого запроса |
| `\errverbose` | последняя ошибка с кодом SQLSTATE и местом в исходниках сервера |
| `\s`, `\s файл` | показать / сохранить историю |
| `\! команда` | выполнить команду shell; `\!` без аргумента — открыть shell |
| `\q`, Ctrl-D | выход |
| Ctrl-C | отменить выполняющийся запрос (с 17 — ещё и зависшую попытку подключения) |

```sql
-- результат запроса — сразу в программу
SELECT name FROM customers \g | wc -l

-- мониторинг: сколько сеансов в каком состоянии, обновление раз в 2 секунды (Ctrl-C — стоп)
SELECT state, count(*) FROM pg_stat_activity WHERE state IS NOT NULL GROUP BY 1 \watch 2
```

```
shop=> SELECT * FROM nosuch;
ERROR:  relation "nosuch" does not exist
LINE 1: SELECT * FROM nosuch;
                      ^
shop=> \errverbose
ERROR:  42P01: relation "nosuch" does not exist
LINE 1: SELECT * FROM nosuch;
                      ^
LOCATION:  parserOpenTable, parse_relation.c:1498
```

## 👀 Вывод результатов

| Команда | Что делает |
| :--- | :--- |
| `\x auto` | развёрнутый вывод «поле — значение», когда строка не влезает в ширину терминала (`\x on` / `\x off` — всегда / никогда) |
| `\pset null '∅'` | показывать NULL видимым символом; по умолчанию это пустая строка, её не отличить от `''` |
| `\pset linestyle unicode`, `\pset border 2` | рамки псевдографикой |
| `\pset format wrapped` | переносить длинные значения по ширине терминала |
| `\pset format csv` (`html`, `asciidoc`, `latex`, `unaligned`) | формат вывода |
| `\t` | только строки: без заголовка и `(N rows)` |
| `\a`, `\f ';'` | вывод без выравнивания; разделитель полей (по умолчанию — вертикальная черта) |
| `\pset pager off` | выключить пейджер |
| `\C 'Заголовок'` | заголовок над таблицей |
| `\crosstabview` | сводная таблица: 1-й столбец результата — строки, 2-й — колонки, 3-й — значения |

```
shop=> \pset null '∅'
shop=> \pset linestyle unicode
shop=> \pset border 2
shop=> SELECT id, name, city FROM customers ORDER BY id;
┌────┬───────┬────────┐
│ id │ name  │  city  │
├────┼───────┼────────┤
│  1 │ Анна  │ Москва │
│  2 │ Борис │ Казань │
│  3 │ Вера  │ ∅      │
│  4 │ Глеб  │ Москва │
└────┴───────┴────────┘
(4 rows)

shop=> SELECT c.city, o.status, count(*)
shop->   FROM orders o JOIN customers c ON c.id = o.customer_id
shop->  GROUP BY 1, 2 ORDER BY 1, 2 \crosstabview
┌────────┬─────┬──────┬─────────┐
│  city  │ new │ paid │ shipped │
├────────┼─────┼──────┼─────────┤
│ Казань │  16 │   17 │      17 │
│ Москва │  33 │   34 │      33 │
│ ∅      │  17 │   16 │      17 │
└────────┴─────┴──────┴─────────┘
(3 rows)
```

**Пейджер.** Длинный результат psql отдаёт пейджеру: `$PSQL_PAGER`, иначе `$PAGER`, иначе `more`. `export PSQL_PAGER='less -S'` не переносит длинные строки — таблицу листают вбок стрелками. Ещё удобнее **pspg** — табличный пейджер с закреплёнными заголовком и первым столбцом: `export PSQL_PAGER=pspg`. Установка: Gentoo — `emerge dev-db/pspg`, Debian/Ubuntu — `apt install pspg`, Arch — AUR `pspg` (`yay -S pspg`); в Entware pspg нет, там есть `less`.

## 🧮 Переменные и условия

```sql
\set city 'Казань'
\set tbl customers
SELECT name FROM :"tbl" WHERE city = :'city';
```

| Запись | Что подставит psql |
| :--- | :--- |
| `:var` | значение как есть — числа, куски SQL |
| `:'var'` | строковый литерал с экранированием: `O'Brien` → `'O''Brien'` |
| `:"var"` | идентификатор в двойных кавычках |
| `:{?var}` | `TRUE` / `FALSE` — задана ли переменная |
| `\set` без аргументов | показать все переменные; `\unset var` — удалить |
| `\prompt 'Дата: ' since` | спросить значение у пользователя |
| `psql -v since=2026-03-01` | задать переменную при запуске |

**`\gset`** — сохранить результат запроса в переменные (имена — по столбцам), **`\gexec`** — выполнить каждую ячейку результата как отдельную команду:

```sql
SELECT count(*) AS n, max(amount) AS top FROM orders \gset
\echo заказов: :n, максимум: :top
-- заказов: 200, максимум: 99.90

-- VACUUM ANALYZE всех пользовательских таблиц: каждая команда — отдельно, вне транзакции
SELECT format('VACUUM (ANALYZE) %I.%I', schemaname, relname)
  FROM pg_stat_user_tables ORDER BY 1 \gexec

-- параметр уходит на сервер отдельно от текста запроса (с 16): никакой склейки строк
SELECT * FROM customers WHERE city = $1 \bind 'Москва' \g
```

Условия — `\if`, `\elif`, `\else`, `\endif`. Пример: отчёт с параметром по умолчанию.

```sql
-- report.sql
\set ON_ERROR_STOP on
\if :{?since}
\else
  \set since '2026-01-01'
\endif
SELECT count(*) AS cnt, count(*) > 0 AS found
  FROM orders WHERE created_at >= :'since' \gset
\if :found
  \echo 'заказов с' :since '—' :cnt
\else
  \warn 'нет заказов с' :since
\endif
```

```
$ psql -X -d shop -f report.sql
заказов с 2026-01-01 — 200
$ psql -X -d shop -v since=2026-03-01 -f report.sql
заказов с 2026-03-01 — 62
$ psql -X -d shop -v since=2027-01-01 -f report.sql
нет заказов с 2027-01-01
```

> [!warning] `\if` принимает только логические значения
> `true`/`false`, `on`/`off`, `yes`/`no`, `1`/`0`. При `\if :cnt` со значением 200 psql пишет `unrecognized value "200" for "\if expression": Boolean expected`, **считает условие ложным и идёт дальше** — даже при `ON_ERROR_STOP`. Поэтому условие вычисляй в SQL: `count(*) > 0 AS found`.

После каждого запроса psql заполняет переменные `ERROR` (`true`/`false`), `SQLSTATE`, `LAST_ERROR_MESSAGE`, `ROW_COUNT`, а после `\!` (с 16) — `SHELL_EXIT_CODE` и `SHELL_ERROR`. На них удобно строить `\if` в скриптах.

## 🤖 Скрипты, cron и CI

Базовый шаблон для миграции или любого скрипта, который должен выполниться целиком или не выполниться совсем:

```bash
psql -X -1 -v ON_ERROR_STOP=1 -d shop -f migrate.sql
```

| Ключ | Зачем |
| :--- | :--- |
| `-X` | не читать `~/.psqlrc`: скрипт не зависит от личных настроек (`\x auto`, `\timing`, пейджер) |
| `-v ON_ERROR_STOP=1` | остановиться на первой ошибке и вернуть код 3 |
| `-1` | выполнить весь файл одной транзакцией |
| `-q` | без служебных строк `INSERT 0 1`, `CREATE TABLE` |
| `-At` | без выравнивания, заголовков и `(N rows)` — для разбора в shell |
| `-F ','`, `-F $'\t'` | разделитель полей для `-A` |
| `--csv` | настоящий CSV с заголовком, кавычки и запятые в значениях экранируются |
| `-o файл` | вывод в файл |
| `-e`, `-a`, `-b` | печатать отправленные запросы / все входные строки / только запросы с ошибкой |
| `-L файл.log` | дублировать в файл запросы и их результаты |
| `-0`, `-z` | NUL как разделитель записей / полей (для `xargs -0`) |

**Коды возврата:**

| Код | Когда |
| :--- | :--- |
| `0` | всё выполнено — **в том числе если были ошибки SQL, но `ON_ERROR_STOP` не включён** |
| `1` | ошибка самого psql (например, нет файла для `-f`) или ошибка SQL в `-c` |
| `2` | не удалось подключиться (или соединение оборвалось в неинтерактивном режиме) |
| `3` | ошибка в скрипте при включённом `ON_ERROR_STOP` |

**Как ведут себя ошибки** — проверено на файле `bad.sql` из трёх команд: `INSERT …; SELECT 1/0; SELECT 'after error';`.

| Запуск | Результат |
| :--- | :--- |
| `psql -f bad.sql` | ошибка печатается, скрипт идёт дальше, INSERT сохранён, **код 0** |
| `psql -v ON_ERROR_STOP=1 -f bad.sql` | остановка на ошибке, код 3; **всё, что выполнилось до ошибки, уже закоммичено** |
| `psql -1 -f bad.sql` | после ошибки каждая команда получает `current transaction is aborted`, в конце — откат; **код 0** |
| `psql -1 -v ON_ERROR_STOP=1 -f bad.sql` | откат всего файла, код 3 — правильный вариант |
| `psql -c "INSERT …; SELECT 1/0;"` | несколько команд в одном `-c` — **одна транзакция**: INSERT откатился, код 1 |
| `psql -c "INSERT …" -c "SELECT 1/0"` | каждый `-c` выполняется отдельно: INSERT сохранён, код 1 |

> [!warning] Ограничения `-c`
> - В `-c` — либо только SQL, либо **одна** метакоманда: `psql -c 'SELECT 1 \gx'` → `syntax error at or near "\"`. Смешивать можно несколькими `-c`, через heredoc или `-f`.
> - Переменные **не подставляются**: `psql -v name=x -c "SELECT :'name'"` → `syntax error at or near ":"`.
> - `\watch` из отдельного `-c` не видит запрос: `\watch cannot be used with an empty query`.
>
> Во всех трёх случаях передавай текст через stdin: `echo "SELECT :'name'" | psql -X -v "name=O'Brien"`.

```bash
# многострочный скрипт прямо в shell; 'SQL' в кавычках — shell не трогает $ и `
psql -X -q -v ON_ERROR_STOP=1 -d shop <<'SQL'
BEGIN;
UPDATE orders SET status = 'shipped' WHERE status = 'paid' AND created_at < current_date - 7;
INSERT INTO audit(action) VALUES ('auto-ship');
COMMIT;
SQL

# значения в переменные shell
total=$(psql -X -At -d shop -c "SELECT count(*) FROM orders")

# построчный разбор результата
psql -X -At -F $'\t' -d shop -c "SELECT id, name FROM customers ORDER BY id" |
while IFS=$'\t' read -r id name; do
  echo "клиент $id: $name"
done

# ANALYZE во всех базах кластера — от суперпользователя или роли с pg_maintain (с 17);
# обычная роль получит по WARNING «permission denied to analyze» на каждую чужую и системную таблицу
psql -X -At -U postgres -d postgres -c "SELECT datname FROM pg_database WHERE datallowconn AND NOT datistemplate" |
while read -r db; do
  psql -X -q -U postgres -d "$db" -c 'ANALYZE'
done

# ждать, пока сервер начнёт принимать подключения (CI, скрипты запуска)
until pg_isready -h db.example.com -p 5432 -q; do sleep 1; done
```

`pg_isready` поставляется в том же клиентском пакете и возвращает `0` — сервер принимает подключения, `1` — отклоняет (например, ещё запускается), `2` — не отвечает, `3` — неверные параметры.

## 📥 Импорт и экспорт: `\copy` и `COPY`

|  | `COPY … TO / FROM 'файл'` | `\copy … to / from 'файл'` |
| :--- | :--- | :--- |
| Где лежит файл | на **сервере БД**; читает и пишет процесс `postgres` | на машине, **где запущен psql** |
| Какие нужны права | суперпользователь или роли `pg_read_server_files` / `pg_write_server_files` | обычные права на таблицу |
| Как работает | сервер сам открывает файл | psql выполняет `COPY … FROM STDIN` / `TO STDOUT` и передаёт данные по соединению |

Обычная роль на серверный `COPY` в файл получит:

```
ERROR:  permission denied to COPY to a file
DETAIL:  Only roles with privileges of the "pg_write_server_files" role may COPY to a file.
HINT:  Anyone can COPY to stdout or from stdin. psql's \copy command also works for anyone.
```

```sql
-- таблица в CSV с заголовком (путь — относительно текущего каталога psql)
\copy customers TO 'customers.csv' WITH (FORMAT csv, HEADER)

-- результат запроса в CSV
\copy (SELECT status, count(*) FROM orders GROUP BY 1 ORDER BY 1) TO 'stat.csv' WITH (FORMAT csv, HEADER)

-- загрузка CSV, в том числе только в часть столбцов
\copy customers_import FROM 'customers.csv' WITH (FORMAT csv, HEADER)
\copy customers_import(id, name) FROM 'part.csv' WITH (FORMAT csv, HEADER)

-- длинный многострочный запрос: обычный COPY … TO STDOUT, а \g направит его вывод в файл
COPY (SELECT status, count(*)
        FROM orders
       GROUP BY 1 ORDER BY 1)
TO STDOUT WITH (FORMAT csv, HEADER) \g stat.csv
```

> [!warning] `\copy` — в одну строку
> Как любая метакоманда, `\copy` заканчивается концом строки. Перенос строки внутри запроса даёт `\copy: parse error at end of line`. Для длинного запроса используй `COPY … TO STDOUT … \g файл` (последний пример выше) или заранее создай `CREATE TEMP VIEW`.

```bash
# выгрузка из shell без \copy: COPY TO STDOUT + перенаправление
psql -X -d shop -c "COPY (SELECT id, name FROM customers ORDER BY id) TO STDOUT WITH (FORMAT csv, HEADER)" > customers.csv

# загрузка из пайпа
cut -d, -f1-2 customers.csv | psql -X -d shop -c "\copy customers_import(id, name) FROM STDIN WITH (FORMAT csv, HEADER)"

# таблица с сервера на сервер без промежуточного файла
psql -X -h old -d shop -c "\copy orders TO STDOUT" | psql -X -h new -d shop -c "\copy orders FROM STDIN"
```

В скрипте `-f` запись `FROM STDIN` читает данные **из самого скрипта** (строки сразу после команды, конец — `\.`). Чтобы взять данные из stdin процесса psql, пиши `FROM PSTDIN`:

```bash
# import.sql:  \copy customers_import(id, name) FROM PSTDIN WITH (FORMAT csv, HEADER)
cut -d, -f1-2 customers.csv | psql -X -v ON_ERROR_STOP=1 -d shop -f import.sql
```

## 💾 Дампы и восстановление через psql

```bash
# SQL-дамп и восстановление «всё или ничего»
pg_dump -d shop > shop.sql
createdb -O app shop_new
psql -X -1 -v ON_ERROR_STOP=1 -d shop_new -f shop.sql

# сжатый дамп — восстанавливать тоже в новую пустую базу
pg_dump -d shop | gzip > shop.sql.gz
createdb -O app shop_gz
gunzip -c shop.sql.gz | psql -X -1 -v ON_ERROR_STOP=1 -d shop_gz

# сразу на другой сервер (база shop на new уже создана и пуста)
pg_dump -h old -d shop | psql -X -v ON_ERROR_STOP=1 -h new -d shop

# роли и табличные пространства pg_dump не сохраняет — их выгружают отдельно
pg_dumpall --roles-only > roles.sql
```

Дамп в формате custom (`pg_dump -Fc`) psql не прочитает: `The input is a PostgreSQL custom-format dump. Use the pg_restore command-line client to restore this dump to a database.` Его восстанавливают через `pg_restore -d shop_new shop.dump`, а посмотреть как SQL можно так: `pg_restore -f - shop.dump | less`. Бэкапы по расписанию с проверкой восстановления — в заметке про [Databasus](Databasus%20%E2%80%94%20self-hosted%20%D0%B1%D1%8D%D0%BA%D0%B0%D0%BF%D1%8B%20PostgreSQL%20%D1%81%20PITR%20%D0%B8%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%BE%D0%B9%20%D0%B2%D0%BE%D1%81%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%28%D0%B0%20%D1%82%D0%B0%D0%BA%D0%B6%D0%B5%20MySQL%2C%20MariaDB%2C%20MongoDB%29.md).

> [!caution] `\restrict` в начале дампа
> Начиная с выпусков августа 2025 года (17.6, 16.10, 15.14, 14.19, 13.22 и вся ветка 18) pg_dump ставит в начало SQL-дампа `\restrict <ключ>`, а в конец — `\unrestrict <ключ>`. Между ними psql отказывается выполнять метакоманды (`backslash commands are restricted; only \unrestrict is allowed`): так вредоносный сервер или подложенный дамп не подсунут `\! команду` (CVE-2025-8714). Более старый psql этой команды не знает, выдаёт `invalid command \restrict`, а с `ON_ERROR_STOP` останавливает восстановление на первой же строке. Решение — обновить клиент. Ключ можно задать вручную: `pg_dump --restrict-key=…`.

## 🩺 Частые запросы администратора

```sql
-- что выполняется прямо сейчас
SELECT pid, usename, application_name AS app, state,
       now() - query_start AS duration, wait_event_type AS wait,
       left(query, 50) AS query
FROM pg_stat_activity
WHERE state <> 'idle' AND pid <> pg_backend_pid()
ORDER BY duration DESC;

-- кто кого блокирует
SELECT blocked.pid  AS blocked_pid,  left(blocked.query, 40)  AS blocked_query,
       blocking.pid AS blocking_pid, left(blocking.query, 40) AS blocking_query
FROM pg_stat_activity blocked
JOIN LATERAL unnest(pg_blocking_pids(blocked.pid)) AS b(pid) ON true
JOIN pg_stat_activity blocking ON blocking.pid = b.pid;

-- самые долгие открытые транзакции (мешают autovacuum, держат блокировки)
SELECT pid, usename, now() - xact_start AS xact_age, state, left(query, 40) AS query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL AND pid <> pg_backend_pid()
ORDER BY xact_age DESC LIMIT 5;

-- остановить: сначала отменить запрос, если не помогло — завершить сеанс
SELECT pg_cancel_backend(12345);
SELECT pg_terminate_backend(12345);
```

Так выглядит блокировка: один сеанс держит `LOCK TABLE orders`, второй (`application_name = report`) ждёт:

```
  pid   | usename |  app   | state  |    duration     |  wait   |            query
--------+---------+--------+--------+-----------------+---------+-----------------------------
 719520 | app     | psql   | active | 00:00:02.003777 | Timeout | SELECT pg_sleep(6);
 719524 | app     | report | active | 00:00:01.000349 | Lock    | SELECT count(*) FROM orders

 blocked_pid |        blocked_query        | blocking_pid |   blocking_query
-------------+-----------------------------+--------------+---------------------
      719524 | SELECT count(*) FROM orders |       719520 | SELECT pg_sleep(6);
```

```sql
-- размеры баз
SELECT datname, pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database ORDER BY pg_database_size(datname) DESC;

-- топ таблиц: всего / данные / индексы
SELECT relname AS table,
       pg_size_pretty(pg_total_relation_size(relid)) AS total,
       pg_size_pretty(pg_relation_size(relid))       AS data,
       pg_size_pretty(pg_indexes_size(relid))        AS indexes
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;

-- индексы, которыми ни разу не пользовались с момента сброса статистики (кроме уникальных)
SELECT s.relname AS table, s.indexrelname AS index, s.idx_scan,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s JOIN pg_index i USING (indexrelid)
WHERE s.idx_scan = 0 AND NOT i.indisunique
ORDER BY pg_relation_size(s.indexrelid) DESC;

-- значение параметра и откуда оно взялось; pending_restart = нужен перезапуск
SELECT name, setting, unit, source, sourcefile, pending_restart
FROM pg_settings WHERE name IN ('work_mem', 'shared_buffers', 'max_connections');

-- версия сервера и к чему подключён
SHOW server_version;
SELECT current_user, current_database(), inet_server_addr(), inet_server_port();

-- план с реальным выполнением; в 18 BUFFERS включается сам, в 17 и раньше — EXPLAIN (ANALYZE, BUFFERS)
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 2;
```

`EXPLAIN ANALYZE` **по-настоящему выполняет** запрос. Для `UPDATE`/`DELETE` оборачивай его в `BEGIN; … ROLLBACK;`.

## ⚙️ `~/.psqlrc`

Файл выполняется при каждом запуске psql — в том числе с `-c` и `-f`, поэтому в скриптах его отключают ключом `-X`. Рабочий вариант:

```
\set QUIET 1
\pset null '∅'
\pset linestyle unicode
\pset border 2
\x auto
\timing on
\set ON_ERROR_ROLLBACK interactive
\set COMP_KEYWORD_CASE upper
\set HISTFILE ~/.psql_history-:DBNAME
\set HISTCONTROL ignoredups
\set PROMPT1 '%n@%M:%>/%/%R%x%# '
\set PROMPT2 '%w%R%x%# '
\set activity 'SELECT pid, usename, datname, state, now() - query_start AS duration, left(query, 60) AS query FROM pg_stat_activity WHERE state <> \'idle\' AND pid <> pg_backend_pid() ORDER BY duration DESC NULLS LAST;'
\set QUIET 0
```

- `QUIET 1` … `QUIET 0` — не печатать при старте подтверждения вроде `Null display is "∅".`
- **`ON_ERROR_ROLLBACK interactive`** — в интерактивной сессии ошибка внутри `BEGIN … COMMIT` не ломает всю транзакцию: psql ставит savepoint перед каждой командой и откатывается только к нему. Опечатка в десятом запросе длинной ручной транзакции больше не требует начинать всё заново. На скрипты значение `interactive` не влияет.
- `HISTFILE ~/.psql_history-:DBNAME` — отдельная история для каждой базы.
- `COMP_KEYWORD_CASE upper` — Tab дополняет ключевые слова заглавными.
- `\set activity '…'` — **именованный запрос**: в psql набираешь `:activity` и получаешь список активных сеансов. Так же удобно держать запросы про блокировки и размеры.
- Для огромных `SELECT` пригодится `\set FETCH_COUNT 1000`: psql забирает результат порциями, а не загружает его в память целиком.
- `\set AUTOCOMMIT off` — каждая команда открывает транзакцию, и до `COMMIT` ничего не сохраняется. Это страхует от случайного `DELETE`, но забытая открытая транзакция держит блокировки.

**Приглашение** — `%n@%M:%>/%/%R%x%# ` даёт `app@db.example.com:5432/shop=> `, а в открытой транзакции — `…/shop=*> `.

| Код | Что подставляет |
| :--- | :--- |
| `%n` | роль |
| `%M`, `%m` | хост полностью / до первой точки (`[local]` для Unix-сокета) |
| `%>` | порт |
| `%/` | база |
| `%R` | в PROMPT1: `=` обычно, `!` — нет соединения; в PROMPT2 — чего ждёт psql: `-` — продолжения команды, `'` — конца строки, `(` — закрывающей скобки |
| `%x` | состояние транзакции: пусто — нет транзакции, `*` — открыта, `!` — сломана (нужен `ROLLBACK`) |
| `%#` | `#` у суперпользователя, `>` у остальных |
| `%s` | имя сервиса (с 18) |
| `%w` | пробелы шириной последнего PROMPT1 — чтобы продолжение строки шло ровно под началом |

## 💻 Установка только клиента

Сервер для работы с удалёнными базами не нужен — достаточно клиентского пакета (в нём также `pg_dump`, `pg_restore`, `pg_isready`, `createdb`, `createuser`).

| Система | Установка |
| :--- | :--- |
| **Gentoo** | `echo 'dev-db/postgresql -server' > /etc/portage/package.use/postgresql`, затем `emerge --ask dev-db/postgresql`: без флага `server` ставятся только клиенты и библиотеки. Флаг `readline` (включён по умолчанию) даёт историю и Tab-дополнение. Несколько версий — слоты, выбор: `eselect postgresql list` / `eselect postgresql set 18`. Альтернативный клиент с автодополнением — `dev-db/pgcli` |
| **Debian / Ubuntu** | `sudo apt install postgresql-client` — версия из дистрибутива (Debian 13 — 17, Ubuntu 24.04 — 16). Версия 18 — из репозитория PGDG: `sudo apt install -y postgresql-common && sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh && sudo apt install postgresql-client-18` |
| **Arch** | `sudo pacman -S postgresql-libs` (18.6): psql, pg_dump, pg_restore, pg_isready и libpq; пакет `postgresql` — это уже сервер |
| **Entware / RT-AX56U** | `opkg install pgsql-cli` — psql **17.5** (~250 КБ, подтянет `libpq` и `libreadline`). В `pgsql-cli-extra` — createdb, createuser, vacuumdb, pgbench, **но без pg_dump**: pg_dump, pg_restore и pg_isready есть только в `pgsql-server` (6,6 МБ архив, ~17 МБ после установки) |

> [!warning] Entware: libpq собран без TLS
> `libpq` в фиде Entware не слинкован с OpenSSL. `sslmode=require` и строже дают ошибку `sslmode value "require" invalid when SSL support is not compiled in`, а режим по умолчанию `prefer` молча подключается **без шифрования**. К базе за пределами домашней сети с роутера ходи только через SSH-туннель или VPN. И помни про версии: клиент 17.5 с сервером 18 — тот самый случай «psql старше сервера» из начала заметки.

## 🔗 Ссылки

- Документация: [psql](https://www.postgresql.org/docs/current/app-psql.html) · [строки подключения и переменные libpq](https://www.postgresql.org/docs/current/libpq-connect.html) · [.pgpass](https://www.postgresql.org/docs/current/libpq-pgpass.html) · [файл сервисов](https://www.postgresql.org/docs/current/libpq-pgservice.html) · [COPY](https://www.postgresql.org/docs/current/sql-copy.html) · [Release notes 18](https://www.postgresql.org/docs/release/18.0/)
- pspg: https://github.com/okbob/pspg
- Связанные заметки: [PostgreSQL — опорная заметка](PostgreSQL%20%E2%80%94%20%D0%BE%D0%BF%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BA%D0%B0%20%28%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0%20MVCC-WAL%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D1%80%D0%BE%D0%BB%D0%B8%2C%20%D1%82%D0%B8%D0%BF%D1%8B%2C%20%D0%B8%D0%BD%D0%B4%D0%B5%D0%BA%D1%81%D1%8B%2C%20EXPLAIN%2C%20%D0%B1%D1%8D%D0%BA%D0%B0%D0%BF%2C%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%29.md) · [VACUUM FULL — bloat и dead tuples](VACUUM%20FULL%20%E2%80%94%20%D0%B2%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%82%20%D0%BC%D0%B5%D1%81%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%B4%D0%B8%D1%81%D0%BA%D0%B5%20%D0%B2%20PostgreSQL%20%28bloat%2C%20dead%20tuples%2C%20pg_repack%29.md) · [Databasus — бэкапы PostgreSQL](Databasus%20%E2%80%94%20self-hosted%20%D0%B1%D1%8D%D0%BA%D0%B0%D0%BF%D1%8B%20PostgreSQL%20%D1%81%20PITR%20%D0%B8%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%BE%D0%B9%20%D0%B2%D0%BE%D1%81%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%28%D0%B0%20%D1%82%D0%B0%D0%BA%D0%B6%D0%B5%20MySQL%2C%20MariaDB%2C%20MongoDB%29.md) · [SSH-туннели](../../Network/SSH/SSH-%D0%92%D0%B8%D0%B7%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE%20%D0%BF%D0%BE%20%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8F%D0%BC.md)

#PostgreSQL #psql #СУБД #SQL #CLI #DevOps #Шпаргалка
