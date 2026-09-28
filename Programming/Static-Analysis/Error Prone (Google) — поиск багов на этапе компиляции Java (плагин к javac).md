---
создал заметку: 2026-09-28T13:25:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Java
  - CompileTime
  - ErrorProne
Источник:
  - https://github.com/google/error-prone
  - https://errorprone.info/
---

# 🧰 Error Prone (Google) — поиск багов на этапе компиляции Java

**Error Prone** ([github.com/google/error-prone](https://github.com/google/error-prone), **Apache-2.0**, ~7.2k★, v2.50.0 / 06.2026) — статический анализатор Java, встроенный **в компилятор**: подключается к `javac` и ловит типичные баги **прямо во время сборки**, до запуска и до отдельного скана. Умеет предлагать и **автоматически применять** исправления (suggested fixes), а через **Refaster** — шаблонный рефакторинг.

Отличается от [SpotBugs](SpotBugs%20%2B%20FindSecBugs%20%E2%80%94%20SAST%20%D0%BF%D0%BE%20%D0%B1%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B4%D1%83%20Java%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20FindBugs%2C%20security-%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%29.md)/[PMD](PMD%20%28%2B%20CPD%29%20%E2%80%94%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%B8%20%D0%B4%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%BE%D1%80%20%D0%BA%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D1%8B%20%28Java%20%D0%B8%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%29.md) не тем, *что* ищет, а *когда*: **не отдельный прогон, а часть компиляции**.

---

## 🧬 Чем подход отличается

- **Zero extra step.** Нет отдельной команды/этапа CI — проверки идут при `javac`. Баг всплывает как ошибка/предупреждение компиляции сразу.
- **Быстро и близко к разработчику** — фидбэк в момент сборки, а не «прогнали сканер раз в день».
- **Автофиксы.** Многие проверки умеют `--patch` — применить исправление автоматически.
- **Расширяемость.** Свои проверки как плагины; популярный сторонний — **[NullAway](https://github.com/uber/NullAway)** (Uber, MIT) для null-безопасности почти без рантайм-оверхеда.

Типичные находки: сравнение через `==` вместо `.equals`, перепутанные аргументы, потерянные возвращаемые значения, ошибки формата, неверные аннотации, мёртвые проверки. Это **баги качества/корректности**, security-фокуса как такового нет (для него — FindSecBugs/Semgrep).

---

## ⚙️ Подключение (пример Gradle)

```groovy
plugins { id 'net.ltgt.errorprone' version '4.+' }
dependencies { errorprone 'com.google.errorprone:error_prone_core:2.50.0' }
tasks.withType(JavaCompile) {
    options.errorprone.disableWarningsInGeneratedCode = true
    // повысить проверку до ошибки:
    options.errorprone.error('MissingOverride')
}
```
Уровни: каждая проверка имеет severity (`OFF/WARN/ERROR`), настраивается флагами `-Xep:CheckName:ERROR`. Автопатч: `-XepPatchChecks:... -XepPatchLocation:IN_PLACE`.

> [!note] Нюанс с новыми JDK
> Error Prone лезет во внутренности `javac`, поэтому на свежих JDK иногда требует `--add-exports/--add-opens` в опциях компилятора. При апгрейде JDK проверить совместимость версии Error Prone.

---

## 🖥️ На системах владельца

Нужен только JDK ([Java на Gentoo](../Java/Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)) и сборочный инструмент — Error Prone тянется как зависимость Gradle/Maven, от дистрибутива не зависит. На роутере (Entware) неактуально.

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Java-SAST по байткоду: [SpotBugs + FindSecBugs](SpotBugs%20%2B%20FindSecBugs%20%E2%80%94%20SAST%20%D0%BF%D0%BE%20%D0%B1%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B4%D1%83%20Java%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20FindBugs%2C%20security-%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%29.md)

## 🔗 Ссылки

- [google/error-prone](https://github.com/google/error-prone) · [errorprone.info](https://errorprone.info/) · [uber/NullAway](https://github.com/uber/NullAway)

#Programming #Static-Analysis #Java #CompileTime #ErrorProne
