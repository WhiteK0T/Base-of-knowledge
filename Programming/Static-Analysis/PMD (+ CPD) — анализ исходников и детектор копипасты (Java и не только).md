---
создал заметку: 2026-09-28T13:05:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Java
  - CodeQuality
  - PMD
Источник:
  - https://github.com/pmd/pmd
  - https://pmd.github.io/
---

# 📏 PMD (+ CPD) — анализ исходников и детектор копипасты

**PMD** ([github.com/pmd/pmd](https://github.com/pmd/pmd), BSD-подобная лицензия, ~5.5k★, v7.28.0 / 09.2026) — статический анализатор **исходного кода** по AST. В отличие от [SpotBugs](SpotBugs%20%2B%20FindSecBugs%20%E2%80%94%20SAST%20%D0%BF%D0%BE%20%D0%B1%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B4%D1%83%20Java%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20FindBugs%2C%20security-%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%29.md) (тот по байткоду), PMD **не требует компиляции** и ловит проблемы уровня исходника: мёртвый код, переусложнённые конструкции, нарушения best-practices, потенциальные баги. Мультиязычный (Java, Apex, JavaScript, Kotlin, XML и др.). В комплекте — **CPD** (Copy-Paste Detector), отдельный детектор дублирующегося кода.

> [!note] PMD — про качество, не про security
> Важно не переоценить: PMD в первую очередь **качество и best-practices**, а не поиск уязвимостей. Security-правил мало. Для безопасности Java — SpotBugs+FindSecBugs или [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md); PMD — рядом, для чистоты кода.

---

## 🧩 Место в связке инструментов Java

| Инструмент | Вход | Основной фокус |
| :--- | :--- | :--- |
| **PMD** | исходник (AST) | качество, best-practices, дублирование |
| **SpotBugs+FindSecBugs** | байткод | баги + security (taint) |
| **Semgrep** | исходник | кастомные правила, security, мультиязык |
| **Checkstyle** | исходник | форматирование/стиль (ещё уже, чем PMD) |

PMD и SpotBugs **дополняют** друг друга: разный вход (исходник vs байткод) → разные находки. Часто гоняют оба.

---

## ⚙️ Запуск

```bash
# анализ исходников по набору правил
pmd check -d src/main/java -R rulesets/java/quickstart.xml -f text
pmd check -d src/ -R category/java/bestpractices.xml -f sarif -r out.sarif  # для CI

# CPD — поиск копипасты (порог в токенах)
pmd cpd --minimum-tokens 100 --files src/ --language java
```
- **Правила** — наборы (`category/java/bestpractices.xml`, `errorprone.xml`, `design.xml`…); свои правила пишутся на **XPath** по AST или на Java.
- **Интеграции:** плагины Maven (`maven-pmd-plugin`) и Gradle (`pmd`), IDE, вывод **SARIF/XML/HTML** для CI.
- `quickstart.xml` — разумный стартовый набор без шума.

---

## 🖥️ На системах владельца

Нужен **JDK** ([Java на Gentoo](../Java/Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md)); PMD ставится как дистрибутив-архив, через Maven/Gradle или пакет. На **Debian/Ubuntu/Arch** есть в репозиториях (`pmd`); на **Gentoo** — через сборочный плагин или ручной архив. На **Entware/роутере** — не по адресу (JVM-инструмент).

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Пара по байткоду с security: [SpotBugs + FindSecBugs](SpotBugs%20%2B%20FindSecBugs%20%E2%80%94%20SAST%20%D0%BF%D0%BE%20%D0%B1%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B4%D1%83%20Java%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20FindBugs%2C%20security-%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%29.md)

## 🔗 Ссылки

- [pmd/pmd](https://github.com/pmd/pmd) · [док PMD](https://pmd.github.io/) · [CPD](https://pmd.github.io/latest/pmd_userdocs_cpd.html)

#Programming #Static-Analysis #Java #CodeQuality #PMD
