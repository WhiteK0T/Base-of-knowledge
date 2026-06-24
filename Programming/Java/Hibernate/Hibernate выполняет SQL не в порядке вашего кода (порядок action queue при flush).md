---
создал заметку: 2026-06-24T14:00:00
author: WhiteK0T
tags:
  - Hibernate
  - JPA
  - Java
  - ORM
  - БазыДанных
Источник:
  - https://t.me/javaproglib/7732
  - https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html
---

# 🙈 Hibernate выполняет SQL не в порядке вашего кода (порядок action queue при flush)

Код читается **сверху вниз**, но **Hibernate так не работает**. Между вызовами `repo.save()`/`repo.delete()` SQL **не уходит в БД сразу** — операции копятся в **очереди действий (`ActionQueue`)** в рамках persistence-контекста. И в момент **flush** Hibernate выполняет их **в фиксированном порядке по типу операции**, а не в порядке, в котором вы их вызвали.

## 📋 Фиксированный порядок выполнения при flush

| # | Операция | Что это |
| :--- | :--- | :--- |
| 1 | **Orphan removal** | удаление «осиротевших» сущностей (`orphanRemoval = true`) |
| 2 | **INSERT** | вставка новых сущностей |
| 3 | **UPDATE** | апдейты изменённых сущностей |
| 4 | **Collection deletion** | удаление элементов коллекций |
| 5 | **Collection update** | обновление коллекций |
| 6 | **Collection insertion** | вставка элементов коллекций |
| 7 | **DELETE** | удаление сущностей |

Главное следствие: **`INSERT` (шаг 2) всегда раньше `DELETE` (шаг 7)** — даже если в коде вы сначала удалили, потом вставили.

## 💥 Классическая ловушка: delete + insert с тем же уникальным ключом

```java
// бизнес-логика: заменить строку с тем же unique-значением
repo.delete(oldRow);   // (1) в коде — сначала удалить
repo.save(newRow);     // (2) потом вставить (тот же email/unique-поле)
// commit → flush
```

Вы ожидаете `DELETE` → `INSERT`. Но Hibernate при flush сделает **`INSERT` → `DELETE`** — и на шаге INSERT поймает **`ConstraintViolationException`** (нарушение `UNIQUE`), потому что старая строка ещё физически в таблице.

> [!warning] Это не баг, а дизайн
> Фиксированный порядок нужен для **батчинга** (группировать однотипные statements и слать пачкой через JDBC batch) и для **корректности ссылочной целостности** в типичных кейсах (родителей вставить до детей, детей удалить до родителей). Но именно сценарий «переиспользование уникального значения в одном flush» этот порядок ломает.

## ✅ Как чинить

### 1. Явный `flush()` между операциями (самое прямое)

Принудительно выгнать накопленный SQL в БД **в порядке кода**, до следующей операции:

```java
repo.delete(oldRow);
entityManager.flush();   // ← DELETE уходит в БД прямо сейчас
repo.save(newRow);       // теперь INSERT не столкнётся со старой строкой
```

В Spring Data JPA удобно `repo.saveAndFlush(...)` или `deleteAllInBatch` + flush. Минус: частые flush **снижают эффективность батчинга** — не злоупотребляй в циклах.

### 2. Отложенные (deferred) ограничения на уровне БД

Перенести проверку `UNIQUE`/FK **на момент commit**, а не на каждый statement — тогда промежуточная коллизия внутри транзакции допустима:

```sql
-- PostgreSQL: ограничение проверяется при COMMIT, а не сразу
ALTER TABLE users
  ADD CONSTRAINT uq_users_email UNIQUE (email)
  DEFERRABLE INITIALLY DEFERRED;
```

> [!caution] Не во всех СУБД и не для всех ограничений
> - **PostgreSQL / Oracle** — поддерживают `DEFERRABLE` ограничения (UNIQUE, FK, PK). В Postgres `NOT NULL` и `CHECK` отложить **нельзя**.
> - **MySQL / MariaDB** — отложенных ограничений **нет вообще**: этот путь недоступен, останутся варианты 1 и 3.
> - Отложенные FK помогают и при циклических ссылках.

### 3. Переделать модель / логику (часто самое правильное)

- **`UPDATE` вместо delete+insert:** если меняется не ключ — просто измени существующую сущность (`merge`/сеттеры в managed-объекте). Часто «удалить и создать заново» — лишнее.
- **Upsert** (`INSERT ... ON CONFLICT DO UPDATE` в Postgres) на уровне нативного запроса.
- **Soft delete** (флаг `deleted`/частичный уникальный индекс), чтобы коллизии ключей не возникало.

## 🧠 Почему ещё это важно знать

- **Поведение flush непредсказуемо «на глаз»:** flush срабатывает не только на commit, но и **перед выполнением запросов** (при `FlushModeType.AUTO`, по умолчанию) — чтобы запрос видел свежие данные. Поэтому «сюрприз с порядком» может выстрелить и до commit.
- **Внутри одного типа** порядок тоже можно настроить для батчинга: `hibernate.order_inserts=true`, `hibernate.order_updates=true`, `hibernate.jdbc.batch_size=N` — группируют statements по таблице.
- **Диагностика:** включи `hibernate.show_sql=true` / логгер `org.hibernate.SQL` (и `org.hibernate.orm.jdbc.bind` для параметров), чтобы увидеть **реальный** порядок и момент ухода SQL. Удобно вместе с p6spy/datasource-proxy.

## 💡 Кратко

- Hibernate копит операции и при **flush** льёт их в **фиксированном порядке по типу** (orphan → insert → update → collection del/upd/ins → delete), **а не в порядке кода**.
- Грабли №1: **delete + insert с одним уникальным значением** → `INSERT` раньше `DELETE` → `ConstraintViolationException`.
- Лечение: **`flush()` между операциями**, **`DEFERRABLE` ограничения** (Postgres/Oracle, не MySQL), либо **переделать на UPDATE/upsert/soft-delete**.

## 🔗 Ссылки

- Hibernate User Guide: [Flushing](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#flushing) (`ActionQueue`, порядок действий)
- PostgreSQL: [SET CONSTRAINTS / DEFERRABLE](https://www.postgresql.org/docs/current/sql-set-constraints.html)
- Источник: [@javaproglib](https://t.me/javaproglib/7732)
- Связанные: [VACUUM FULL — возврат места на диске в PostgreSQL](../../../%D0%A1%D0%A3%D0%91%D0%94/Postgres/VACUUM%20FULL%20%E2%80%94%20%D0%B2%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%82%20%D0%BC%D0%B5%D1%81%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%B4%D0%B8%D1%81%D0%BA%D0%B5%20%D0%B2%20PostgreSQL%20%28bloat%2C%20dead%20tuples%2C%20pg_repack%29.md)

#Hibernate #JPA #Java #ORM #БазыДанных
