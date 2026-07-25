---
создал заметку: 2026-07-25T20:30:00
author: WhiteK0T
tags:
  - Java
  - JVM
  - JDK
  - Gentoo
  - Portage
  - OpenJDK
  - Backend
Источник:
  - https://packages.gentoo.org/packages/dev-java/openjdk
  - https://wiki.gentoo.org/wiki/Java
  - https://openjdk.org/
---

# ☕ Java — платформа и язык (JVM, JDK/JRE, экосистема)

**Java** — это одновременно **язык** и **платформа**. Код компилируется не в машинный код, а в **байткод**, который исполняет **JVM** (Java Virtual Machine). Отсюда девиз «**write once, run anywhere**»: один `.jar` работает на любой ОС, где есть JVM. JVM с JIT-компиляцией и мощным GC даёт производительность, близкую к нативной, на **долгоживущих** серверных нагрузках.

> [!info] Разбор терминов (их часто путают)
> - **JVM** — виртуальная машина, исполняет байткод (`.class`), делает JIT-компиляцию и сборку мусора.
> - **JRE** (Java Runtime Environment) — JVM + стандартные библиотеки, «только запускать». С Java 11 отдельного JRE официально нет — используют JDK или урезанный образ через `jlink`.
> - **JDK** (Java Development Kit) — JRE + компилятор `javac`, `jar`, `jshell`, `javadoc` и др. **Разработчику нужен JDK.**
> - **OpenJDK** — эталонная **open-source** реализация (GPLv2+CE). Сборки: Temurin (Eclipse Adoptium), Oracle OpenJDK, Amazon Corretto, Azul Zulu, Liberica — это **одна платформа**, разные дистрибуции с разной поддержкой.

## 🧭 Версии и LTS

Java выходит **каждые полгода** (март/сентябрь), но для прода важны **LTS**-версии:

| Версия | Тип | Примечание |
| :--- | :--- | :--- |
| **21** | LTS | текущий «дефолт» для нового прода |
| **17** | LTS | всё ещё массово в проде |
| **11** | LTS | легаси, но живо |
| **8** | LTS | древнее легаси (много старых проектов) |
| **25** | LTS (свежая) | новейшая LTS-линия |
| 22–24, 26+ | feature-релизы | 6 мес. поддержки, для прода не берут |

> [!tip] Правило выбора
> Для нового проекта — **последняя LTS** (21 или 25). Feature-релизы (не-LTS) — только чтобы пощупать новые фичи, в прод не ставить: поддержка всего 6 месяцев.

## ⚙️ Что важно понимать про JVM

- **JIT-компиляция**: байткод сначала интерпретируется, «горячие» методы компилируются в нативный код (C1/C2). Отсюда **прогрев** (warm-up): пик производительности — не сразу после старта.
- **Сборщики мусора (GC)**: **G1** (по умолчанию), **ZGC** и **Shenandoah** (сверхнизкие паузы), **Parallel** (throughput), Serial (маленькие heap). Выбор GC — важный тюнинг для латентности/пропускной способности.
- **Память**: heap (`-Xmx`/`-Xms`), metaspace, стеки потоков. Диагностика — heap dump, `jmap`, `jstat`.
- **Диагностика на проде**: `jstack` (стеки потоков), `jcmd`, `jfr` (Java Flight Recorder — низкооверхедный профайлинг), `async-profiler` (флейм-графы). При 100% CPU: `top -H` → hex TID → `jstack | grep nid=0x...`.
- **Экосистема сборки**: **Maven** (`pom.xml`) и **Gradle** (`build.gradle`) — зависимости из Maven Central, плагины, тесты, покрытие (см. [JaCoCo](JaCoCo%20%E2%80%94%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20Java-%D0%BA%D0%BE%D0%B4%D0%B0%20%D1%82%D0%B5%D1%81%D1%82%D0%B0%D0%BC%D0%B8%20%28bytecode-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%2C%20Maven-Gradle%2C%20CI-CD%2C%20%D0%BE%D1%82%D1%87%D1%91%D1%82%D1%8B%29%20%D0%B8%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%E2%89%A0%20%D0%BA%D0%B0%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE.md)).

## 🐧 Gentoo (основная система) — сборка из исходников

На Gentoo Java-инфраструктура крутится вокруг **eselect java-vm** и слотированных JDK. Раз ты собираешь из исходников — основной пакет это **`dev-java/openjdk`** (полноценная компиляция OpenJDK), а не бинарный `-bin`.

> [!info] `dev-java/openjdk` — слоты и USE (проверено по packages.gentoo.org)
> **Слоты** (можно держать несколько JDK одновременно): `8`, `11`, `17`, `21`, `25`, а также beta/alpha `27`/`28`.
> **USE-флаги**:
> | Флаг | По умолч. | Что делает |
> | :--- | :--- | :--- |
> | `jbootstrap` | ✅ | собрать бутстрап-JDK и им скомпилировать целевой (полностью из исходников, дольше) |
> | `system-bootstrap` | ✅ | использовать **уже установленный** JDK как загрузочный компилятор (быстрее, если JDK уже есть) |
> | `headless-awt` | ➖ | **без GUI** (AWT/Swing) — то, что нужно на **сервере/без иксов** |
> | `javafx` | ➖ | поддержка JavaFX (тянет `dev-java/openjfx`) |
> | `source` | ➖ | установить исходники стандартной библиотеки (удобно для навигации в IDE) |
> | `systemtap` | ➖ | пробы SystemTap/DTrace |
> | `alsa`, `cups`, `doc`, `examples` | ➖ | звук / печать / документация / примеры |

> [!warning] «Курица и яйцо»: чем собирать первый JDK
> Компилятор Java написан на Java → чтобы собрать OpenJDK, **нужен уже готовый JDK**. Два пути:
> - **`system-bootstrap`** (по умолчанию) — берёт установленный JDK как загрузочный. Быстрее, но нужен предыдущий JDK в системе.
> - **`jbootstrap`** — Portage сам соберёт промежуточный бутстрап. Честный full-source, но **заметно дольше** (по сути собираешь JDK дважды).
> На **чистой** системе первый JDK иногда проще поднять через временный `openjdk-bin` как бутстрап, а потом пересобрать `openjdk` из исходников и `emerge -C` бинарный. Ты бином не пользуешься — но как разовый bootstrap-костыль это законный приём.

> [!info] Переключение JVM — `eselect java-vm` (ключевая специфика Gentoo)
> Несколько JDK живут в **слотах** одновременно; активная выбирается через eselect:
> ```bash
> eselect java-vm list                     # какие JVM установлены
> eselect java-vm set system openjdk-21    # системная JVM по умолчанию
> eselect java-vm set user  openjdk-17     # своя JVM только для пользователя (перебивает системную)
> java-config --list-available-vms         # альтернативный инструмент
> ```
> Переменная окружения **`GENTOO_VM`** и файлы в `/etc/env.d/` фиксируют выбор. `virtual/jdk` / `virtual/jre` — виртуальные пакеты, которые тянут актуальную реализацию.

```bash
# пример: собрать OpenJDK 21 без GUI (сервер), задать флаги
echo 'dev-java/openjdk:21 headless-awt -javafx source' >> /etc/portage/package.use/openjdk
emerge -av dev-java/openjdk:21
eselect java-vm set system openjdk-21
```

> [!tip] Сборка OpenJDK — долгая; облегчить
> Полная компиляция OpenJDK — тяжёлая. Помогают: `system-bootstrap` (не собирать бутстрап заново), `ccache`, побольше `MAKEOPTS`/RAM. На сервере ставь **`headless-awt`** и **`-javafx`** — не тащить графику. Отдельные библиотеки (`dev-java/*`) в Gentoo часто идут через `java-pkg-simple` — большинство прикладных Java-либ всё равно тянутся Maven/Gradle, а не Portage.

## 🖥️ Установка на других системах владельца

| Система | Как поставить |
| :--- | :--- |
| **Debian / Ubuntu** | `sudo apt install openjdk-21-jdk` (или 17). Несколько версий — `update-alternatives --config java`. Свежие сборки — репозиторий **Adoptium/Temurin** (`packages.adoptium.net`) |
| **Arch** | `sudo pacman -S jdk-openjdk` (последняя) или `jdk21-openjdk`/`jdk17-openjdk`. Переключение — `archlinux-java set java-21-openjdk`, `archlinux-java status` |
| **Entware / RT-AX56U (armv7)** | ⚠️ полноценной JVM в Entware обычно **нет** (Java на роутере — экзотика, тяжело для `512 МБ RAM`). Если очень нужно — только очень лёгкие JVM (сомнительно на этом железе). Практически: **не сценарий** для роутера |

## 🧪 Факты против хайпа

> [!caution] Мифы про Java
> - **«Java медленная»** — устаревший миф. На **долгоживущем** серверном коде JIT+G1/ZGC дают производительность, близкую к нативной. Слабое место — **старт и warm-up** (для коротких CLI/лямбд), что лечат AOT/CDS, GraalVM native-image, Project Leyden.
> - **«Java = Oracle / платно»** — нет. **OpenJDK свободен** (GPLv2+CE). Платит поддержку только тот, кто берёт **Oracle JDK** по их лицензии; для 99% случаев бери Temurin/Corretto/Zulu/собранный на Gentoo `openjdk`.
> - **«Java = JavaScript»** — нет, это **разные языки**, совпадение в названии историческое.
> - **«Java прожорлива по памяти»** — JVM резервирует heap и метаданные заранее; настраивается (`-Xmx`, выбор GC, контейнерные флаги `-XX:MaxRAMPercentage`). В контейнерах обязательно задавай лимиты, иначе JVM видит всю память хоста.
> - **Проверяй качество тестов, а не только их наличие** — покрытие ≠ качество, см. [JaCoCo](JaCoCo%20%E2%80%94%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20Java-%D0%BA%D0%BE%D0%B4%D0%B0%20%D1%82%D0%B5%D1%81%D1%82%D0%B0%D0%BC%D0%B8%20%28bytecode-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%2C%20Maven-Gradle%2C%20CI-CD%2C%20%D0%BE%D1%82%D1%87%D1%91%D1%82%D1%8B%29%20%D0%B8%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%E2%89%A0%20%D0%BA%D0%B0%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE.md) (и mutation testing).

## 🔗 Связанные заметки

- Тестовое покрытие Java-кода и почему покрытие ≠ качество: [JaCoCo](JaCoCo%20%E2%80%94%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20Java-%D0%BA%D0%BE%D0%B4%D0%B0%20%D1%82%D0%B5%D1%81%D1%82%D0%B0%D0%BC%D0%B8%20%28bytecode-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%2C%20Maven-Gradle%2C%20CI-CD%2C%20%D0%BE%D1%82%D1%87%D1%91%D1%82%D1%8B%29%20%D0%B8%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%E2%89%A0%20%D0%BA%D0%B0%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE.md)
- ORM и неочевидный порядок SQL при flush: [Hibernate](Hibernate/Hibernate%20%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D1%8F%D0%B5%D1%82%20SQL%20%D0%BD%D0%B5%20%D0%B2%20%D0%BF%D0%BE%D1%80%D1%8F%D0%B4%D0%BA%D0%B5%20%D0%B2%D0%B0%D1%88%D0%B5%D0%B3%D0%BE%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%BF%D0%BE%D1%80%D1%8F%D0%B4%D0%BE%D0%BA%20action%20queue%20%D0%BF%D1%80%D0%B8%20flush%29.md)
- Структуры данных JCF: [PriorityQueue](JCF/PriorityQueue.md)
- Другой серверный рантайм для сравнения (event loop vs потоки, экосистема): [Node.js](../JavaScript/NodeJS/Node.js%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BD%D1%8B%D0%B9%20JavaScript-%D1%80%D0%B0%D0%BD%D1%82%D0%B0%D0%B9%D0%BC%20%28V8%2C%20event%20loop%2C%20npm%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%D0%B8%20%D0%B4%D1%80.md)

## 🔗 Ссылки

- Официально: [openjdk.org](https://openjdk.org/) · пакет: [packages.gentoo.org/dev-java/openjdk](https://packages.gentoo.org/packages/dev-java/openjdk)
- Gentoo Java: [wiki.gentoo.org/wiki/Java](https://wiki.gentoo.org/wiki/Java)
- Свободные сборки: [Eclipse Temurin (Adoptium)](https://adoptium.net/) · [Amazon Corretto](https://aws.amazon.com/corretto/) · [Azul Zulu](https://www.azul.com/downloads/)

#Java #JVM #JDK #Gentoo #Portage #OpenJDK #Backend
