---
создал заметку: 2026-09-28T14:05:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Java
  - C
  - Infer
  - Correctness
Источник:
  - https://github.com/facebook/infer
  - https://fbinfer.com/
---

# 🔬 Infer (Meta) — межпроцедурный анализ (null, утечки, гонки)

**Infer** ([github.com/facebook/infer](https://github.com/facebook/infer), **MIT**, ~15.7k★, v1.3.0 / 05.2026) — статический анализатор от Meta на основе **separation logic / абстрактной интерпретации**. Главное отличие от большинства бесплатных инструментов — **настоящий межпроцедурный (interprocedural) анализ**: прослеживает свойства через вызовы функций и файлы. Именно то, что у [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md) OSS платно, а тут — открыто.

Языки: **Java, C, C++, Objective-C**.

---

## 🧬 Что ловит и как

Infer ориентирован на **надёжность/корректность**, а не на классические web-уязвимости:
- **null-dereference** (разыменование null),
- **утечки ресурсов/памяти** (незакрытые файлы, сокеты; в C/C++ — память),
- **гонки данных** (анализатор **RacerD**),
- **проблемы памяти** (движок **Pulse**: use-after-free и т.п. в C/C++).

Работает через **захват сборки** — оборачивает команду компиляции:
```bash
infer run -- javac App.java
infer run -- mvn compile          # или gradle
infer run -- make                 # C/C++
# отчёт: infer-out/, вывод в текст/JSON
```
То есть Infer видит реальные единицы компиляции проекта, а не отдельные файлы.

> [!note] Это про баги, а не про инъекции
> Infer силён в null/утечках/гонках, но **не заменяет security-SAST**: для SQLi/XSS/инъекций нужны FindSecBugs/Semgrep. И исторически поддержка **Java слабее**, чем C/ObjC (фокус Meta — мобильный C/ObjC/Java-Android). Прогон бывает медленным и требует чистой сборки.

---

## 🧩 Место в наборе

| Нужно | Инструмент |
| :--- | :--- |
| null/утечки/гонки, межпроцедурно, бесплатно | **Infer** |
| security-паттерны/инъекции Java | FindSecBugs, Semgrep |
| качество/стиль | PMD, Checkstyle |
| баги при компиляции | Error Prone |

---

## 🖥️ На системах владельца

Infer ставится как бинарный дистрибутив (OCaml-сборка) или из исходников; удобно — **через Docker** (`infer` официальный образ), чтобы не собирать. Нужны JDK/тулчейн целевого языка.

| Система | Как |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | официальный бинарник/`docker run ... infer`; сборка из исходников тяжёлая (OCaml) |
| **Entware / RT-AX56U** | ➖ не для роутера (armv7, ресурсы); гонять на ПК/в CI |

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Security-SAST Java (то, чего Infer не делает): [SpotBugs + FindSecBugs](SpotBugs%20%2B%20FindSecBugs%20%E2%80%94%20SAST%20%D0%BF%D0%BE%20%D0%B1%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B4%D1%83%20Java%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20FindBugs%2C%20security-%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%29.md)

## 🔗 Ссылки

- [facebook/infer](https://github.com/facebook/infer) · [fbinfer.com](https://fbinfer.com/)

#Programming #Static-Analysis #Java #C #Infer #Correctness
