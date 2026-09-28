---
создал заметку: 2026-09-28T16:25:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - C
  - Cpp
  - Embedded
  - clang-tidy
  - cppcheck
Источник:
  - https://clang.llvm.org/extra/clang-tidy/
  - https://github.com/danmar/cppcheck
---

# 🔧 C/C++ — clang-tidy и cppcheck

Для C/C++ статический анализ особенно важен: язык без сборщика мусора, ошибки памяти → уязвимости (переполнения, use-after-free). Два основных бесплатных инструмента дополняют друг друга. Тема близка владельцу — **прошивки роутера и дронов** пишут на C/C++.

| Инструмент | Основа | Лицензия | Особенность |
| :--- | :--- | :--- | :--- |
| **clang-tidy** | Clang/LLVM | Apache-2.0 (LLVM exc.) | глубокий (использует Clang Static Analyzer), автофиксы; **нужна compilation database** |
| **[cppcheck](https://github.com/danmar/cppcheck)** (danmar) | собственный парсер | GPL-3.0 | **не требует сборки**, низкий уровень ложных, аддон **MISRA** для embedded |

---

## 🔎 Чем отличаются на практике

- **clang-tidy** — сотни проверок по категориям: `bugprone-*`, `cert-*` (CERT Secure Coding), `clang-analyzer-*` (полноценный путь-чувствительный анализ), `cppcoreguidelines-*`, `security-*`. Точный, потому что понимает код как компилятор — но ему нужна **compilation database** (`compile_commands.json`):
  ```bash
  # сгенерировать БД компиляции (CMake):
  cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -B build
  clang-tidy -p build --checks='bugprone-*,cert-*,clang-analyzer-*' src/*.c
  clang-tidy -p build --fix src/*.c        # автоисправление
  ```
- **cppcheck** — независимый анализатор, **работает без полной сборки** (парсит сам), философия «минимум ложных срабатываний»: сильно ловит утечки памяти, переполнения буфера, UB, разыменование null.
  ```bash
  cppcheck --enable=all --inconclusive src/
  cppcheck --project=build/compile_commands.json      # можно и с БД
  cppcheck --addon=misra src/                          # проверка MISRA C
  ```

> [!tip] Для embedded/прошивок — MISRA
> Если код идёт в микроконтроллер/прошивку, аддон **MISRA** у cppcheck проверяет соответствие отраслевому стандарту безопасного C. Для дронов/роутерных модулей это ближе к делу, чем generic-правила.

**Вывод:** гонять **оба** — cppcheck быстрый и без сборки для первого прохода, clang-tidy глубокий по compile-db. Плюс встроенный `scan-build` (Clang Static Analyzer) для path-sensitive анализа.

---

## 🖥️ На системах владельца

| Система | Установка |
| :--- | :--- |
| **Gentoo** (основная) | clang-tidy: `emerge sys-devel/clang` (+ clang-extra); cppcheck: `emerge dev-util/cppcheck` |
| **Debian / Ubuntu** | `apt install clang-tidy cppcheck` |
| **Arch** | `pacman -S clang cppcheck` |
| **Entware / RT-AX56U** | ⚠️ анализировать прошивку логичнее **кросс-хостом** на ПК (с compile-db целевой сборки), а не на самом роутере. cppcheck под arm бывает, но смысла держать анализатор на устройстве мало |

> [!note] Для встроенного кода — анализ на хосте
> Прошивки роутера/дрона кросс-компилируются на ПК; статический анализ там же и запускается (по исходникам/compile-db), устройству инструменты не нужны. Связка с кросс-сборкой Gentoo — см. заметки по `crossdev`/binhost.

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Межпроцедурный анализ C/C++ (память): [Infer](Infer%20%28Meta%29%20%E2%80%94%20%D0%BC%D0%B5%D0%B6%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D0%B4%D1%83%D1%80%D0%BD%D1%8B%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%28null%2C%20%D1%83%D1%82%D0%B5%D1%87%D0%BA%D0%B8%2C%20%D0%B3%D0%BE%D0%BD%D0%BA%D0%B8%29%20%D0%B4%D0%BB%D1%8F%20Java%20C%20C%2B%2B.md)

## 🔗 Ссылки

- [clang-tidy (LLVM)](https://clang.llvm.org/extra/clang-tidy/) · [danmar/cppcheck](https://github.com/danmar/cppcheck)

#Programming #Static-Analysis #C #Cpp #Embedded #clang-tidy #cppcheck
