---
создал заметку: 2026-06-08T18:30:00
author: WhiteK0T
tags:
  - Сериализация
  - Java
  - Apache_Fory
  - Производительность
Источник:
  - https://github.com/apache/fory
  - https://fory.apache.org/
  - https://t.me/javaproglib/7697
---

# ⚡ Apache Fory — высокопроизводительная сериализация

**Apache Fory** (ранее **Fury**, переименован в 2025) — кроссязыковой фреймворк сериализации с упором на скорость. Лицензия **Apache 2.0**, проект под зонтиком Apache.

Позиционируется как **drop-in замена** для JDK-сериализации, Kryo, Hessian — с совместимым API, но кратно быстрее.

## 🚀 Ключевые особенности

- **Скорость.** Сериализаторы компилируются в рантайме (**JIT**) + **zero-copy** доступ (row-format). Заявляют **до 170×** к JDK-сериализации на отдельных нагрузках.
- **Ссылки.** Корректно обрабатывает **shared и циклические** ссылки между объектами.
- **Schema evolution.** В compatible-режиме поля можно **добавлять/удалять независимо** на обеих сторонах.
- **GraalVM.** Поддержка native image через AOT-компиляцию.
- **Xlang-режим.** Кроссязыковая сериализация для ~11 языков: Java, Python, C++, Go, Rust, JS/TS, C#, Swift, Dart, Scala, Kotlin.

## ☕ Базовое использование (Java)

```java
Fory fory = Fory.builder()
    .withLanguage(Language.JAVA)
    .requireClassRegistration(true)   // безопасность: только зарегистрированные классы
    .build();
fory.register(Order.class);

byte[] bytes = fory.serialize(order);
Order decoded = (Order) fory.deserialize(bytes);
```

**Зависимость (Maven):**

```xml
<dependency>
  <groupId>org.apache.fory</groupId>
  <artifactId>fory-core</artifactId>
  <version>1.1.0</version>
</dependency>
```

**Gradle:** `implementation "org.apache.fory:fory-core:1.1.0"`

## 🎯 Когда применять

Там, где сериализация — узкое место: высоконагруженный **RPC**, **кэширование**, межсервисный обмен данными, **кроссязыковые пайплайны** (например, Java ↔ Python).

> [!warning] Безопасность десериализации
> Как и любая мощная библиотека сериализации, Fory при десериализации **недоверенных данных** потенциально опасен. Рекомендуется включать `requireClassRegistration(true)` и регистрировать только нужные классы — это ограничивает, какие типы могут быть инстанцированы, и снижает риск deserialization-атак.

> [!note] Про имя
> Если встречаешь в статьях/зависимостях **Fury** (`io.fury`) — это прежнее имя того же проекта. Актуальное — **Fory** (`org.apache.fory`).

#Сериализация #Java #Apache_Fory #Производительность
