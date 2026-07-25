---
создал заметку: 2026-07-25T21:10:00
author: WhiteK0T
tags:
  - Java
  - Generics
  - Дженерики
  - TypeSafety
  - PECS
  - JVM
Источник:
  - https://t.me/javalib/7282
  - https://docs.oracle.com/javase/tutorial/java/generics/
---

# 🧬 Java Generics — дженерики (обобщения): T, wildcards, PECS, стирание типов

**Дженерики (обобщения)** — механизм параметризации типами: класс/метод/интерфейс пишется один раз, а конкретный тип подставляется при использовании. Главная цель — **типобезопасность на этапе компиляции** и **отказ от ручных приведений (cast)**. Компилятор ловит `list.add("строку")` в `List<Integer>` ещё до запуска, а не в рантайме через `ClassCastException`.

> [!info] Зачем это (в трёх пунктах)
> - **Безопасность типов**: ошибки — на компиляции, а не в проде.
> - **Без приведений**: `Integer i = list.get(0)` вместо `(Integer) list.get(0)`.
> - **Переиспользование**: один `Box<T>` / один `map(...)` работает для всех типов.
> - Конвенции имён параметров: **`T`** (Type), **`E`** (Element), **`K`/`V`** (Key/Value), **`R`** (Result), **`N`** (Number).

---

## 1. Обобщённый класс — `Box<T>`

```java
public class Box<T> {
    private T value;
    public Box(T value) { this.value = value; }
    public T get() { return value; }
    public void set(T value) { this.value = value; }
}

Box<String> b = new Box<>("hi");   // diamond <> (Java 7+): тип выводится
String s = b.get();                // без каста
// var + diamond (Java 10+): тип берётся из инициализатора
var box = new Box<Integer>(42);
```

## 2. Обобщённый метод — `<T> void print(T val)`

Параметр типа объявляется **перед** возвращаемым значением. Метод может быть обобщённым и в необобщённом классе.

```java
public static <T> T firstOrNull(List<T> list) {
    return list.isEmpty() ? null : list.get(0);
}
// современный вариант — вернуть Optional вместо null:
public static <T> Optional<T> first(List<T> list) {
    return list.stream().findFirst();
}
```

## 3. Ограниченный тип — `<T extends Number>` (верхняя граница)

`T` обязан быть `Number` или его подклассом → внутри можно звать методы `Number` (`doubleValue()` и т.п.).

```java
public static <T extends Number> double sum(List<T> nums) {
    return nums.stream().mapToDouble(Number::doubleValue).sum();
}
sum(List.of(1, 2, 3));        // Integer
sum(List.of(1.5, 2.5));       // Double
```

## 4. Несколько границ — `<T extends A & B>`

`T` реализует **и** `A`, **и** `B`. Если среди них есть класс — он идёт **первым**, дальше интерфейсы.

```java
// T должен и сравниваться, и быть сериализуемым
public static <T extends Comparable<T> & Serializable> T max(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}
```

## 5–7. Wildcards (подстановочные типы)

| Форма | Что значит | Когда |
| :--- | :--- | :--- |
| `<?>` | неизвестный тип (unbounded) | только **читаем** как `Object`, тип не важен |
| `<? extends T>` | некий **подкласс** T (upper bound) | **читаем** из коллекции (producer) |
| `<? super T>` | некий **суперкласс** T (lower bound) | **пишем** в коллекцию (consumer) |

```java
// <?> — печать любого списка
static void printAll(List<?> list) {
    for (Object o : list) System.out.println(o);
}

// <? extends Number> — читаем числа, НЕ добавляем
static double total(List<? extends Number> nums) {
    double s = 0;
    for (Number n : nums) s += n.doubleValue();   // читать можно
    // nums.add(1);  // ❌ не компилируется
    return s;
}

// <? super Integer> — пишем Integer
static void fill(List<? super Integer> sink) {
    for (int i = 0; i < 3; i++) sink.add(i);      // писать можно
}
fill(new ArrayList<Number>());   // ок: Number — супертип Integer
fill(new ArrayList<Object>());   // ок
```

## 8. Правило PECS — **P**roducer **E**xtends, **C**onsumer **S**uper

Если коллекция **отдаёт** данные (producer) — `extends`; если **принимает** (consumer) — `super`. Канонический пример — `Collections.copy` / свой `copy`:

```java
public static <T> void copy(List<? super T> dst, List<? extends T> src) {
    for (T item : src) dst.add(item);   // src — producer (extends), dst — consumer (super)
}
// реальный пример из JDK: Stream.collect, Collectors, Comparator.comparing и т.д.
Comparator<String> byLen = Comparator.comparingInt(String::length);
```

## 9. Сырой тип (raw type) — `List list = new ArrayList()`

Существует только для совместимости со старым (до Java 5) кодом. **Избегай** — теряется вся проверка типов.

```java
List raw = new ArrayList();   // ⚠️ raw type
raw.add("s"); raw.add(42);    // компилятор молчит
Integer x = (Integer) raw.get(0);  // 💥 ClassCastException в рантайме
```

## 10. Стирание типов (type erasure) — **фундамент, объясняющий половину ограничений**

JVM про дженерики **ничего не знает**: компилятор проверяет типы, а потом **стирает** их (заменяет на границу или `Object`) и вставляет касты. Поэтому в рантайме `List<String>` и `List<Integer>` — это один и тот же `List`.

```java
List<String> a = new ArrayList<>();
List<Integer> b = new ArrayList<>();
a.getClass() == b.getClass();   // true! оба ArrayList
```

Отсюда запреты:

```java
// T.class     — ❌ нет типа в рантайме
// new T()      — ❌ неизвестно, что создавать
// obj instanceof T   — ❌ (см. правку ниже)
```

> [!warning] Правки/нюансы к посту — тонкости стирания
> - **`instanceof` с сырым/wildcard-типом РАЗРЕШЁН**: `x instanceof List` и `x instanceof List<?>` — ок; запрещён только `x instanceof List<String>` и `x instanceof T`. С Java 16 работает pattern matching: `if (o instanceof List<?> l) { ... }`.
> - **Обойти `new T()` / `T.class`** — передать **токен типа** `Class<T>`:
>   ```java
>   static <T> T create(Class<T> type) throws Exception {
>       return type.getDeclaredConstructor().newInstance();
>   }
>   ```
> - **Обойти `new T[]`** — через рефлексию: `(T[]) Array.newInstance(clazz, n)`, либо хранить `List<T>`.
> - **Перегрузка не работает** по стёртым типам: `void f(List<String>)` и `void f(List<Integer>)` — конфликт (одна сигнатура после стирания).

## 11. Обобщённый конструктор

Конструктор может иметь свой параметр типа, даже если класс необобщённый:

```java
class Wrapper {
    <T> Wrapper(T val) { System.out.println(val.getClass()); }
}
new Wrapper(42);       // Integer
new Wrapper("text");   // String
```

## 12. Обобщённый интерфейс — но не изобретай `Mapper` заново

```java
interface Mapper<F, T> { T map(F input); }
```

> [!tip] В JDK это уже есть — `java.util.function.Function<F, T>`
> Пример из поста (`Mapper<F,T>`) — это ровно **`Function<F, T>`** из стандартной библиотеки. Не плоди свой интерфейс: бери `Function`, он ещё умеет композицию (`andThen`, `compose`).
> ```java
> Function<UserDto, User> toEntity = dto -> new User(dto.name(), dto.email());
> List<User> users = dtos.stream().map(toEntity).toList();   // Java 16+: .toList()
> ```

## 13. Только объекты, не примитивы

`List<int>` невозможен — только `List<Integer>` (autoboxing оборачивает автоматически). Для производительности на больших объёмах чисел используй **примитивные стримы** (`IntStream`, `LongStream`) или массивы `int[]`, чтобы избежать боксинга.

## 14. Нельзя создавать массивы дженериков — `new T[]` / `new List<String>[]`

Массивы **ковариантны и знают свой тип в рантайме**, а дженерики стёрты — поэтому язык это запрещает (иначе дыра в типобезопасности). Решения:

```java
// вместо T[] — коллекция
List<T> items = new ArrayList<>();
// если массив реально нужен — токен типа + рефлексия:
@SuppressWarnings("unchecked")
T[] arr = (T[]) Array.newInstance(clazz, size);
```

## 15. Нельзя вставлять в `<? extends T>` (кроме `null`)

```java
List<? extends Number> nums = new ArrayList<Integer>();
// nums.add(1);      // ❌ компилятор не знает точный подтип
nums.add(null);      // ✅ единственное исключение — null подходит любому типу
```

Нужна вставка → бери `<? super T>` (см. PECS, п.7–8).

---

## 🚀 Актуальные примеры (Java 17/21 LTS)

> [!info] Дженерики в реальном коде
> **Обобщённый репозиторий (паттерн Spring Data):**
> ```java
> interface Repository<T, ID> {
>     Optional<T> findById(ID id);
>     List<T> findAll();
>     T save(T entity);
> }
> ```
> **Обобщённый record (Java 16+) — типобезопасный результат:**
> ```java
> record Result<T>(T value, boolean ok, String error) {
>     static <T> Result<T> ok(T v)      { return new Result<>(v, true, null); }
>     static <T> Result<T> fail(String e){ return new Result<>(null, false, e); }
> }
> ```
> **Дженерики + Stream + Collectors:**
> ```java
> static <T, K> Map<K, List<T>> groupBy(List<T> items, Function<T, K> key) {
>     return items.stream().collect(Collectors.groupingBy(key));
> }
> Map<String, List<User>> byCity = groupBy(users, User::city);
> ```
> **Sealed + generics (Java 17+) — типобезопасный `Either`:**
> ```java
> sealed interface Either<L, R> permits Left, Right {}
> record Left<L, R>(L error) implements Either<L, R> {}
> record Right<L, R>(R value) implements Either<L, R> {}
> ```

## 🖥️ Применимость

Дженерики — **фича языка/компилятора**, не системная утилита: от ОС не зависят, нужен лишь **JDK** (см. [Java — платформа и установка на Gentoo](../Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)). Diamond `<>` — с Java 7, `var` — с Java 10, обобщённые records/sealed — с Java 16/17. На **Gentoo** просто собери нужный слот `dev-java/openjdk` и выбери его через `eselect java-vm`.

## ⚠️ Частые грабли (сводка)

- Путают `extends`/`super` → запомни **PECS**.
- Пытаются `new T()`, `T.class`, `T[]` → это стирание типов, нужен `Class<T>`-токен или `List<T>`.
- Оставляют **raw types** (из старого кода) → включи предупреждения компилятора (`-Xlint:unchecked`).
- Забывают, что `List<Dog>` **не** является `List<Animal>` (инвариантность) → для этого и нужны wildcards.

## 🔗 Связанные заметки

- Платформа/JVM/JDK и установка на Gentoo: [Java — платформа и язык](../Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)
- Дженерики в коллекциях на практике (`Comparable<T>`, `Comparator<T>`): [PriorityQueue](../JCF/PriorityQueue.md)

## 🔗 Ссылки

- Официальный туториал: [docs.oracle.com — Generics](https://docs.oracle.com/javase/tutorial/java/generics/)
- Спецификация wildcards и PECS: *Effective Java* (Joshua Bloch), Item 31 «Use bounded wildcards»
- Источник новости: [@javalib](https://t.me/javalib/7282)

#Java #Generics #Дженерики #TypeSafety #PECS #JVM
