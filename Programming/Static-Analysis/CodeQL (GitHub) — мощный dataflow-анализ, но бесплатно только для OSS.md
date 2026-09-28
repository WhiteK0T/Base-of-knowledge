---
создал заметку: 2026-09-28T16:45:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - SAST
  - CodeQL
  - Security
  - Dataflow
Источник:
  - https://github.com/github/codeql
  - https://codeql.github.com/
---

# 🧠 CodeQL (GitHub) — мощный dataflow-анализ, но бесплатно только для OSS

**CodeQL** ([codeql.github.com](https://codeql.github.com/), запросы: [github/codeql](https://github.com/github/codeql) MIT, ~10k★) — семантический анализатор GitHub, один из самых сильных бесплатных по **межпроцедурному dataflow/taint-анализу**. Идея необычная: код **компилируется в базу данных**, а потом по ней гоняются **запросы на языке QL** (декларативная логика). Так находят реальные цепочки «источник ввода → небезопасный сток» через много функций и файлов — то, что большинству инструментов не под силу.

Языки: C/C++, C#, Go, **Java/Kotlin**, JS/TS, **Python**, Ruby, Swift. Движёт GitHub Code Scanning.

> [!warning] Ключевая оговорка: лицензия ограничивает приватное использование
> Наборы **запросов** открыты (MIT), но **сам движок CodeQL CLI** по условиям GitHub бесплатен только для: **публичных OSS-репозиториев**, академии и исследований. Анализ **приватного/коммерческого** кода требует **GitHub Advanced Security (платно)**. То есть «бесплатный мощный SAST» — да, но **для открытого кода**; на закрытом проекте это уже платно. Для приватного кода бесплатные альтернативы — [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md) / [Infer](Infer%20%28Meta%29%20%E2%80%94%20%D0%BC%D0%B5%D0%B6%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D0%B4%D1%83%D1%80%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%28null%2C%20%D1%83%D1%82%D0%B5%D1%87%D0%BA%D0%B8%2C%20%D0%B3%D0%BE%D0%BD%D0%BA%D0%B8%29%20%D0%B4%D0%BB%D1%8F%20Java%20C%20C%2B%2B.md).

---

## 🔎 Как это работает

```bash
# 1. Построить БД (для компилируемых языков — «наблюдая» за сборкой)
codeql database create db --language=java --command="mvn compile"
# для Python/JS сборка не нужна:
codeql database create db --language=python

# 2. Прогнать набор запросов (security-набор)
codeql database analyze db codeql/java-queries:codeql-suites/java-security-extended.qls \
  --format=sarif-latest --output=out.sarif
```
- **Сила:** глубокий taint-анализ, легко найти нетривиальные инъекции; можно писать **свои QL-запросы** под специфичные баги.
- **Цена:** высокий порог входа (язык QL), тяжелее по времени/ресурсам (нужна БД), для компилируемых языков — рабочая сборка.
- **Проще всего** включить как **Code Scanning** в GitHub Actions на публичном репозитории — там бесплатно и «из коробки».

---

## 🖥️ На системах владельца

CodeQL CLI — отдельный дистрибутив (бинарь) + библиотеки запросов; ставится на любой Linux.

| Система | Как | Нюанс |
| :--- | :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | скачать CodeQL CLI + `git clone github/codeql`; удобнее — Code Scanning в GitHub Actions | помнить про лицензию: локальный анализ **приватного** кода — только с GHAS |
| **Entware / RT-AX56U** | ➖ тяжёлый инструмент, не для роутера | — |

> [!tip] Для владельца практично
> Если его репозитории на GitHub **публичные** — включить CodeQL Code Scanning в Actions ничего не стоит и даёт мощный анализ. Для приватного кода — оставаться на Semgrep/SpotBugs/gosec и т.п.

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Бесплатно и для приватного кода: [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md)

## 🔗 Ссылки

- [codeql.github.com](https://codeql.github.com/) · [github/codeql (запросы)](https://github.com/github/codeql)

#Programming #Static-Analysis #SAST #CodeQL #Security #Dataflow
