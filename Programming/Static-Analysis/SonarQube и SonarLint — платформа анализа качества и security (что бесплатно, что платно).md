---
создал заметку: 2026-09-28T13:45:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - SAST
  - CodeQuality
  - SonarQube
  - Java
Источник:
  - https://github.com/SonarSource/sonarqube
  - https://www.sonarsource.com/
---

# 📊 SonarQube и SonarLint — платформа анализа качества и security

**SonarQube** ([github.com/SonarSource/sonarqube](https://github.com/SonarSource/sonarqube), **LGPL-3.0** — Community Edition, ~11k★) — не просто анализатор, а **серверная платформа**: сканирует код на 30+ языках, копит метрики во времени, ведёт дашборд, **quality gates** (пропускать/блокировать PR по порогам), учитывает технический долг. **SonarLint** (ныне «SonarQube for IDE», бесплатный плагин) даёт те же проверки **на лету в редакторе**, в т.ч. в connected-режиме с сервером.

> [!warning] Главное: что бесплатно, а что платно
> Community Edition **открыта (LGPL) и бесплатна**, но у неё **потолок**. Ключевые вещи — в **платных** редакциях (Developer/Enterprise/Data Center):
> - 🔒 **taint-анализ / межпроцедурный dataflow** (реальный поиск инъекций через несколько функций) — **только Developer+**. В Community security-правила поверхностные.
> - 🔒 **анализ веток и PR-декорации**, ряд языков (C/C++, ABAP и др.), безопасность на уровне «SAST по dataflow».
>
> То есть «SonarQube ловит SQL-инъекции» — да, но по-настоящему (с прослеживанием потока) это **платная** функция. Для бесплатного глубокого анализа честнее [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md) + [SpotBugs+FindSecBugs](SpotBugs%20%2B%20FindSecBugs%20%E2%80%94%20SAST%20%D0%BF%D0%BE%20%D0%B1%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B4%D1%83%20Java%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20FindBugs%2C%20security-%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%29.md).

---

## 🧩 Когда SonarQube оправдан

Сила — не в разовом скане, а в **процессе для команды/долгого проекта**: единый дашборд, тренд техдолга, quality gate в CI, «не ухудшать покрытие/не плодить code smells». Для соло-ревью одного репозитория это тяжёлый молоток — там проще CLI-инструменты (Semgrep/PMD/SpotBugs). Для постоянного проекта с историей — окупается.

**SonarLint без сервера** — бесплатный и лёгкий: подсветка проблем прямо в IDE по мере набора; хороший вход, если не нужен серверный дашборд.

---

## ⚙️ Развёртывание

SonarQube — **JVM-сервер** с бандлом Elasticsearch (+ БД PostgreSQL для продакшена). Обычно через Docker:
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
# затем сканер в проекте:
sonar-scanner -Dsonar.projectKey=myproj -Dsonar.host.url=http://localhost:9000 -Dsonar.login=<token>
```
Сканер есть отдельный (`sonar-scanner`) и как плагины Maven/Gradle. Требует прилично RAM (ES внутри).

---

## 🖥️ На системах владельца

| Система | Как | Нюанс |
| :--- | :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | Docker-образ `sonarqube:community`; либо SonarLint-плагин в IDE без сервера | сервер прожорлив (JVM+Elasticsearch, ≥2–4 ГБ RAM). Для лёгкого старта — SonarLint |
| **Entware / RT-AX56U** | ➖ исключено: JVM + Elasticsearch на armv7/512 МБ RAM нежизнеспособны | — |

> [!note] Бренды
> Sonar переименовал линейку: **SonarQube Server** (self-host), **SonarQube Cloud** (бывш. SonarCloud, SaaS), **SonarQube for IDE** (бывш. SonarLint). Суть та же.

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Бесплатные CLI-альтернативы: [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md) · [PMD](PMD%20%28%2B%20CPD%29%20%E2%80%94%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%B8%D1%81%D1%85%D0%BE%D0%B4%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%B8%20%D0%B4%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%BE%D1%80%20%D0%BA%D0%BE%D0%BF%D0%B8%D0%BF%D0%B0%D1%81%D1%82%D1%8B%20%28Java%20%D0%B8%20%D0%BD%D0%B5%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%29.md)

## 🔗 Ссылки

- [SonarSource/sonarqube](https://github.com/SonarSource/sonarqube) · [sonarsource.com](https://www.sonarsource.com/)

#Programming #Static-Analysis #SAST #CodeQuality #SonarQube #Java
