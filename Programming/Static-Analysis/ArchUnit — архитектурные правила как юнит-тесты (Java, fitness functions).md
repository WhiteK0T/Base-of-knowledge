---
создал заметку: 2026-09-28T14:25:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Java
  - Architecture
  - ArchUnit
  - Testing
Источник:
  - https://github.com/TNG/ArchUnit
  - https://www.archunit.org/
---

# 🏛️ ArchUnit — архитектурные правила как юнит-тесты

**ArchUnit** ([github.com/TNG/ArchUnit](https://github.com/TNG/ArchUnit), **Apache-2.0**, ~3.8k★, v1.5.1 / 09.2026) — необычный жанр статического анализа: библиотека, которой ты **описываешь архитектурные правила на Java и гоняешь их как обычные юнит-тесты** (JUnit). Нарушил слоистость — упал тест, сломалась сборка. Это «architecture fitness functions»: статический контроль **структуры**, а не багов или уязвимостей.

Под капотом ArchUnit импортирует **байткод** классов и проверяет граф зависимостей — компиляция нужна (это тесты), внешний сканер — нет.

---

## 🧬 Что можно закрепить

- **Слоистость:** `controller` не лезет напрямую в `repository`, минуя `service`.
- **Границы пакетов/модулей:** кто на кого может зависеть.
- **Отсутствие циклов** между пакетами.
- **Именование/аннотации:** классы в `..service..` кончаются на `Service`; поля с `@Autowired` запрещены; и т.п.

Пример правила:
```java
@Test
void controllers_should_not_access_repositories_directly() {
    ArchRule rule = noClasses().that().resideInAPackage("..controller..")
        .should().dependOnClassesThat().resideInAPackage("..repository..");
    rule.check(new ClassFileImporter().importPackages("com.myapp"));
}
```
Есть готовые шаблоны (`layeredArchitecture()`, `onionArchitecture()`, `slices()...should().beFreeOfCycles()`).

> [!note] Это не про security и не про баги
> ArchUnit **не ищет уязвимости или дефекты кода** — он не даёт архитектуре «расползаться» со временем. Ставить в один ряд с Semgrep/SpotBugs неверно: это перпендикулярная задача (governance структуры). Поэтому и живёт вместе с тестами, а не в security-CI.

---

## 🧩 Место в наборе

| Задача | Инструмент |
| :--- | :--- |
| архитектурные инварианты | **ArchUnit** |
| security-паттерны | Semgrep, FindSecBugs |
| качество/стиль | PMD, Checkstyle |
| корректность (null/утечки) | Infer, Error Prone |

---

## 🖥️ На системах владельца

Просто **тестовая зависимость Java-проекта** (Maven/Gradle), нужен JDK ([Java на Gentoo](../Java/Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)). От дистрибутива не зависит; на роутере неактуально.

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Корректность на этапе сборки: [Error Prone](Error%20Prone%20%28Google%29%20%E2%80%94%20%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%20%D0%B1%D0%B0%D0%B3%D0%BE%D0%B2%20%D0%BD%D0%B0%20%D1%8D%D1%82%D0%B0%D0%BF%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%86%D0%B8%D0%B8%20Java%20%28%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20%D0%BA%20javac%29.md)

## 🔗 Ссылки

- [TNG/ArchUnit](https://github.com/TNG/ArchUnit) · [archunit.org](https://www.archunit.org/)

#Programming #Static-Analysis #Java #Architecture #ArchUnit #Testing
