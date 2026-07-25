---
создал заметку: 2026-07-25T18:45:00
author: WhiteK0T
tags:
  - Java
  - Тестирование
  - Coverage
  - JaCoCo
  - Maven
  - Gradle
  - CI-CD
Источник:
  - https://t.me/javaproglib/7793
  - https://github.com/jacoco/jacoco
---

# ⚙️ JaCoCo — покрытие Java-кода тестами (и почему покрытие ≠ качество)

**JaCoCo** (Java Code Coverage, [github.com/jacoco/jacoco](https://github.com/jacoco/jacoco)) — де-факто **стандартная библиотека покрытия для JVM**, от команды **EclEmma**. Меряет, какие участки кода реально исполняются тестами, и выдаёт отчёты в HTML/XML/CSV. Лицензия **EPL-2.0**, ~4.6k★, живёт с 2012, активна; актуальная версия — **0.8.15** (июнь 2026). Работает с **Java-агентом**, встраивается в **Maven/Gradle/Ant** и любой CI/CD.

> [!info] Чем отличается от встроенного покрытия IDE (посыл поста)
> Покрытие в IntelliJ IDEA удобно **локально** при разработке. JaCoCo нужен там, где важны **машиночитаемые отчёты и автоматизация**: единый формат для CI, **пороговые гейты** («сборка падает, если покрытие ниже X»), интеграция с **SonarQube**, история метрик по проекту. Это не «замена IDE», а слой для **сборки и пайплайна**.

## 📊 Что именно измеряет

JaCoCo считает покрытие на уровне **байткода** (точнее, чем «по строкам»), по нескольким счётчикам:

| Счётчик | Что показывает |
| :--- | :--- |
| **Instructions (C0)** | доля исполненных байткод-инструкций — базовая метрика JaCoCo |
| **Branches (C1)** | покрытие веток (`if`/`switch`/тернарники) — исполнена ли каждая ветка условия |
| **Lines** | строки исходника (маппинг байткода обратно на строки) |
| **Methods / Classes** | сколько методов/классов затронуто хотя бы раз |
| **Cyclomatic Complexity** | цикломатическая сложность (число независимых путей) — полезно как индикатор «сложных» мест |

## 🧬 Как это работает

1. **On-the-fly инструментация**: при запуске тестов подключается Java-агент (`-javaagent:jacocoagent.jar`), который на лету инструментирует классы и пишет данные исполнения в файл **`jacoco.exec`** (бинарный).
2. **Генерация отчёта**: из `.exec` + исходников/классов формируются **HTML** (для глаз), **XML/CSV** (для машин — CI, SonarQube).
3. Есть и **offline-инструментация** (заранее модифицированные классы) — нужна в редких случаях (конфликт агентов, PowerMock).

## 🧩 Подключение

> [!info] Maven (`jacoco-maven-plugin`)
> ```xml
> <plugin>
>   <groupId>org.jacoco</groupId>
>   <artifactId>jacoco-maven-plugin</artifactId>
>   <version>0.8.15</version>
>   <executions>
>     <execution><id>prepare-agent</id>
>       <goals><goal>prepare-agent</goal></goals></execution>   <!-- вешает javaagent на тесты -->
>     <execution><id>report</id><phase>test</phase>
>       <goals><goal>report</goal></goals></execution>          <!-- HTML/XML/CSV после тестов -->
>     <execution><id>check</id>
>       <goals><goal>check</goal></goals>                       <!-- гейт: минимальный % -->
>     </execution>
>   </executions>
> </plugin>
> ```
> Отчёт: `target/site/jacoco/index.html`, XML: `target/site/jacoco/jacoco.xml`.

> [!info] Gradle (плагин `jacoco`)
> ```groovy
> plugins { id 'jacoco' }
> jacoco { toolVersion = "0.8.15" }
> test { finalizedBy jacocoTestReport }
> jacocoTestReport {
>   dependsOn test
>   reports { xml.required = true; html.required = true }
> }
> // гейт:
> jacocoTestCoverageVerification {
>   violationRules { rule { limit { minimum = 0.70 } } }
> }
> ```

> [!info] Интеграции
> - **SonarQube**: скорми ему **`jacoco.xml`** (`sonar.coverage.jacoco.xmlReportPaths`) — Sonar сам покажет покрытие и тренды.
> - **CI/CD**: Jenkins (плагин JaCoCo), **GitLab CI** (регэксп покрытия + артефакт HTML/`cobertura`-конвертация), GitHub Actions — любой, кто умеет читать XML.
> - **Исключения**: убирай из подсчёта DTO/сгенерированный код — паттерны в `excludes`, а для **Lombok** добавь `lombok.addLombokGeneratedAnnotation = true` (JaCoCo с версии 0.8.x игнорирует `@Generated`).

## ⚠️ Главное: высокое покрытие ≠ хорошие тесты

> [!warning] Покрытие — метрика необходимая, но НЕ достаточная
> JaCoCo показывает, что код **исполнился** тестом, но **не** что тест что-то **проверил**. Тест без единого `assert`, «прогоняющий» метод, даст **100% покрытия и ноль пользы**. Гоняться за красивой цифрой (особенно за **100%**) — вредно: провоцирует бессмысленные тесты и трату времени на геттеры/DTO.
> - Ставь **реалистичный порог** (часто 70–80% на бизнес-логику), исключай тривиальный/сгенерированный код.
> - Проверяй **качество утверждений** отдельно — **mutation testing** (**PIT/pitest**): он вносит мутации в код и смотрит, **падают** ли тесты. «Убитые мутанты» честнее говорят о силе тестов, чем строки покрытия.
> - Смотри покрытие как **карту непротестированных мест**, а не как KPI для отчёта начальству.

## 🧯 Подводные камни

- **Совместимость с версией байткода JDK.** Под новый Java нужен достаточно **свежий JaCoCo** — поддержка новых class-file версий приезжает с новыми релизами. Ошибки вида «Unsupported class file major version» = обнови JaCoCo.
- **Lombok / сгенерированный код** искажает цифры — настраивай исключения (см. выше).
- **Лямбды/`switch`/строковые switch** иногда дают неочевидные «непокрытые ветки» на уровне байткода — это особенность инструментации, не всегда «ты не дописал тест».
- **PowerMock и агенты**, конфликтующие с инструментацией, могут потребовать **offline-инструментации**.
- Покрытие меряется только тем, что **прогоняется в тестах на JVM**; ручные/внешние e2e-проверки оно не учитывает.

## 🖥️ Применимость

JaCoCo — **не системная утилита**, а **плагин системы сборки** (Maven/Gradle), поэтому **от ОС не зависит**: работает одинаково на Gentoo/Debian/Arch/Windows — нужен лишь **JDK + Maven/Gradle**. Ставить отдельно ничего не надо: версия объявляется в `pom.xml`/`build.gradle`. Важнее ОС — **совместимость версии JaCoCo с твоим JDK**. Роутеру (**RT-AX56U/Entware**) неактуально — Java-сборка там не ведётся.

## 🔗 Ссылки

- Репозиторий: [github.com/jacoco/jacoco](https://github.com/jacoco/jacoco) (EPL-2.0) · документация: [jacoco.org/jacoco](https://www.jacoco.org/jacoco/)
- Дополняет покрытие проверкой качества тестов: [PIT / pitest](https://pitest.org/)
- Источник новости: [@javaproglib](https://t.me/javaproglib/7793)

#Java #Тестирование #Coverage #JaCoCo #Maven #Gradle #CI-CD
