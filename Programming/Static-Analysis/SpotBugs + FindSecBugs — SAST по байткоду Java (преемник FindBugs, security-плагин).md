---
создал заметку: 2026-09-28T12:45:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - SAST
  - Java
  - Security
  - SpotBugs
Источник:
  - https://github.com/spotbugs/spotbugs
  - https://github.com/find-sec-bugs/find-sec-bugs
---

# 🐛 SpotBugs + FindSecBugs — SAST по байткоду Java

**SpotBugs** ([github.com/spotbugs/spotbugs](https://github.com/spotbugs/spotbugs), **LGPL-2.1**, ~3.9k★, v4.10.4 / 08.2026) — преемник заброшенного **FindBugs** (тот мёртв с ~2016). Анализирует **Java-байткод** (`.class`/`.jar`), а не исходники, и ищет ~400 паттернов багов. **FindSecBugs** ([github.com/find-sec-bugs/find-sec-bugs](https://github.com/find-sec-bugs/find-sec-bugs), **LGPL-3.0**, ~2.4k★, v1.14.0 / 06.2025) — плагин к SpotBugs, добавляющий **~140 security-детекторов** (OWASP Top 10, CWE, SANS Top 25) с taint-анализом для инъекций.

Это классика Java-SAST и хорошая **пара к [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md)**: они смотрят с разных сторон (см. ниже).

---

## 🧬 Ключевая особенность: анализ байткода, а не исходника

- SpotBugs работает по **скомпилированным** `.class`/`.jar` → **проект надо сначала собрать**. Исходники нужны лишь чтобы показать строку в отчёте.
- Плюс: видит то, что компилятор/JIT реально сгенерировал (в т.ч. из аннотаций, Lombok, сгенерированного кода), и **не зависит от языка исходника** — анализирует и Kotlin/Scala/Groovy, скомпилированные в JVM-байткод.
- Минус: без сборки не запустить; тонкие вещи уровня исходника (стиль, форматирование) — не сюда, для этого PMD/Checkstyle.

**SpotBugs vs Semgrep (оба SAST по Java):**

| | SpotBugs+FindSecBugs | Semgrep |
| :--- | :--- | :--- |
| Вход | **байткод** (нужна сборка) | **исходник** (сборка не нужна) |
| Правила | встроенные детекторы (Java-специфичные) | свой YAML, мультиязык |
| Security | FindSecBugs: taint-анализ инъекций, ~140 типов | паттерны; глубокий taint — платный Pro |
| Знание фреймворков | сильное (Spring, JSF, Struts, Hibernate…) | через правила |

Разумно гонять **оба**: SpotBugs+FindSecBugs как Java-специфичный движок по байткоду, Semgrep — для кастомных правил и не-Java частей репозитория.

---

## ⚙️ Как запускать (через систему сборки)

Обычно не отдельным бинарём, а плагином сборки — тогда FindSecBugs подключается как зависимость.

**Gradle** (`build.gradle`):
```groovy
plugins { id 'com.github.spotbugs' version '6.+' }
dependencies { spotbugsPlugins 'com.h3xstream.findsecbugs:findsecbugs-plugin:1.14.0' }
spotbugs { effort = 'max'; reportLevel = 'low' }   // максимум находок
// отчёт: ./gradlew spotbugsMain   → build/reports/spotbugs/
```

**Maven** (`pom.xml`, плагин `com.github.spotbugs:spotbugs-maven-plugin`) с тем же `findsecbugs-plugin` в `<plugins>` внутри конфигурации. Запуск: `mvn spotbugs:check`.

**CLI** (без сборочного плагина):
```bash
spotbugs -pluginList findsecbugs-plugin-1.14.0.jar -effort:max -low \
         -sarif=out.sarif -textui target/classes
```

Полезное: `-effort:max` (глубже, медленнее), уровни `-low/-medium/-high`, вывод **SARIF/XML/HTML** для CI, файл-фильтр `exclude.xml` для подавления ложных.

---

## 🖥️ На системах владельца

Нужен только **JDK** (см. [Java — платформа и особенности на Gentoo](../Java/Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)) — сам инструмент тянется как зависимость Gradle/Maven, от дистрибутива не зависит.

| Система | Как |
| :--- | :--- |
| **Gentoo** (основная) | JDK через `eselect java-vm`; SpotBugs/FindSecBugs подтянет Gradle/Maven. Отдельного ebuild не требуется |
| **Debian / Ubuntu** | JDK из репозитория; далее через сборку. Есть пакет `spotbugs`, но плагин удобнее тянуть Gradle'ом |
| **Arch** | JDK (`jdk-openjdk`); через сборку/AUR |
| **Entware / RT-AX56U** | ➖ JVM-инструмент на armv7/512 МБ — не для роутера; гонять на ПК/в CI |

> [!note] FindSecBugs обновляется неспешно
> Ядро SpotBugs живое (релиз 08.2026), а FindSecBugs выпускается редко (v1.14.0 — 06.2025). Для самых новых фреймворков детекторов может не быть — дополнять Semgrep-правилами.

## 🔗 Связанные заметки

- Терминология и место в SDLC: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Пара по исходнику и мультиязык: [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md)

## 🔗 Ссылки

- [spotbugs/spotbugs](https://github.com/spotbugs/spotbugs) · [find-sec-bugs/find-sec-bugs](https://github.com/find-sec-bugs/find-sec-bugs) · [док SpotBugs](https://spotbugs.readthedocs.io/)

#Programming #Static-Analysis #SAST #Java #Security #SpotBugs
