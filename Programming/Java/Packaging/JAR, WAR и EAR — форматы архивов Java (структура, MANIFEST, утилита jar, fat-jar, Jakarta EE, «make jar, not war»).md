---
создал заметку: 2026-08-11T10:05:00
author: WhiteK0T
tags:
  - Java
  - JAR
  - WAR
  - EAR
  - Упаковка
  - Jakarta_EE
  - Spring_Boot
  - Программирование
Источник:
  - https://t.me/javatasks/2373
  - https://docs.oracle.com/en/java/javase/25/docs/specs/man/jar.html
  - https://jakarta.ee/release/11/
  - https://docs.spring.io/spring-boot/specification/executable-jar/launching.html
  - https://tomcat.apache.org/whichversion.html
---

# JAR, WAR и EAR: форматы архивов Java

Заметка по посту `@javatasks` [«В чём разница между jar и war?»](https://t.me/javatasks/2373). Пост фактически корректный и даёт правильную рамку; здесь она развёрнута до рабочего уровня — точные структуры каталогов, атрибуты манифеста, реальные команды `jar`/Maven/Gradle, устройство fat-jar, актуальное состояние Jakarta EE и Spring Boot на 2026 год и грабли, о которых пост не говорит.

> [!info] Коротко
> | | JAR | WAR | EAR |
> | :--- | :--- | :--- | :--- |
> | Расшифровка | **J**ava **AR**chive | **W**eb **AR**chive | **E**nterprise **AR**chive |
> | Что внутри | классы, ресурсы, зависимости | web-приложение (сервлеты, JSP, статика) | несколько EE-модулей целиком |
> | Кто запускает | `java -jar`, classpath, модуль | сервлет-контейнер (Tomcat, Jetty) | Application Server (WildFly, WebSphere) |
> | Обязательный дескриптор | `META-INF/MANIFEST.MF` | `WEB-INF/` (web.xml — опционален с Servlet 3.0) | `META-INF/application.xml` |
> | Актуальность 2026 | **основной формат** | жив, но ниша | редкость, легаси-энтерпрайз |
>
> Все три — **обычные ZIP-архивы**. Разница только в структуре каталогов, наборе дескрипторов и в том, кто их читает.

---

## 1. Все три формата — это ZIP

Пост прав: переименуй в `.zip` и распакуй. Проверить можно вообще ничего не переименовывая:

```bash
unzip -l app.jar          # список содержимого
unzip -p app.jar META-INF/MANIFEST.MF   # вывести манифест в stdout
file app.jar              # Java archive data (JAR)
```

```bash
# то же самое штатной утилитой JDK
jar --list --file app.jar
jar --describe-module --file app.jar    # если это модульный JAR
```

> [!note] Два отличия от «просто ZIP», о которых стоит знать
> 1. **`META-INF/MANIFEST.MF` должен быть первым (или вторым, после каталога `META-INF/`) элементом архива.** JDK читает манифест, не разбирая архив целиком. Если пересобрать jar обычным `zip` и положить манифест в конец — `java -jar` может не найти `Main-Class`.
> 2. **Порядок и байтовая точность элементов важны для подписи.** Подписанный jar с переупакованными элементами превращается в невалидный.
>
> Поэтому «просто перепаковать zip-ом» работает не всегда — используй `jar` или сборщик.

Формально спецификация: [JAR File Specification](https://docs.oracle.com/en/java/javase/25/docs/specs/jar/jar.html). ZIP-контейнер накладывает и свои ограничения: 4 ГБ / 65535 элементов без ZIP64, и, наоборот, свои уязвимости — **zip slip** (путь `../../etc/passwd` внутри архива) и **zip bomb** при наивной распаковке чужих архивов.

---

## 2. JAR — базовый формат

### 2.1 Структура

```
app.jar
├── META-INF/
│   ├── MANIFEST.MF              ← обязателен
│   ├── services/                ← ServiceLoader: имя интерфейса → файл со списком реализаций
│   │   └── com.example.spi.Codec
│   ├── versions/                ← multi-release JAR (JDK 9+)
│   │   ├── 17/com/example/Impl.class
│   │   └── 21/com/example/Impl.class
│   ├── *.SF, *.DSA/*.RSA/*.EC   ← если jar подписан
│   └── maven/…                  ← кладёт maven-jar-plugin, не обязательно
├── module-info.class            ← если модульный JAR (JPMS)
├── com/example/Main.class
├── com/example/Service.class
└── application.properties       ← любые ресурсы
```

### 2.2 `MANIFEST.MF` — что там реально бывает

```properties
Manifest-Version: 1.0
Created-By: 21.0.11 (Gentoo)
Main-Class: com.example.Main
Class-Path: lib/guava.jar lib/slf4j-api.jar
Multi-Release: true
Automatic-Module-Name: com.example.app
Implementation-Title: my-app
Implementation-Version: 1.4.2
Sealed: true
Enable-Native-Access: ALL-UNNAMED
```

| Атрибут | Зачем |
| :--- | :--- |
| `Main-Class` | точка входа для `java -jar app.jar` |
| `Class-Path` | список **относительных** путей к другим jar; разделитель — **пробел**, не `:`/`;` |
| `Multi-Release` | включает чтение `META-INF/versions/N/` |
| `Automatic-Module-Name` | имя automatic-модуля JPMS для не-модульного jar |
| `Implementation-Version` | доступно в рантайме через `getClass().getPackage().getImplementationVersion()` |
| `Sealed` | все классы пакета обязаны быть в этом jar |
| `Enable-Native-Access` | JDK 24+: разрешает FFM/JNI без предупреждений |

> [!warning] Формат манифеста строже, чем кажется
> - Строка **не длиннее 72 байт**; продолжение переносится на следующую строку с **одним ведущим пробелом**.
> - Файл **обязан** заканчиваться переводом строки — иначе последний атрибут молча игнорируется.
> - Кодировка — UTF-8, `Name: value` через двоеточие и пробел.
>
> Это самая частая причина «почему мой `Main-Class` не подхватился». Не пиши манифест руками — пусть его делает `jar -e` или плагин сборщика.

### 2.3 Исполняемый JAR

```bash
# компилируем
javac -d out $(find src -name '*.java')

# собираем с точкой входа (-e == --main-class)
jar --create --file app.jar --main-class com.example.Main -C out .

# запускаем
java -jar app.jar
```

> [!danger] `java -jar` **игнорирует** `-cp` и переменную `CLASSPATH`
> ```bash
> java -cp lib/guava.jar -jar app.jar     # ← guava НЕ попадёт в classpath, тихо
> ```
> При `-jar` classpath целиком берётся из `Class-Path` манифеста. Правильные варианты:
> ```bash
> java -cp "app.jar:lib/*" com.example.Main    # без -jar, класс явно
> java -p app.jar:lib -m com.example.app/com.example.Main   # модульный путь
> ```

### 2.4 Утилита `jar`: режимы и полезные опции

| Режим | Что делает |
| :--- | :--- |
| `-c` / `--create` | создать архив |
| `-t` / `--list` | показать содержимое |
| `-u` / `--update` | обновить существующий |
| `-x` / `--extract` | распаковать |
| `-d` / `--describe-module` | вывести `module-info` или имя automatic-модуля |
| `-i` / `--generate-index` | **deprecated**, может быть удалён |

```bash
# multi-release JAR: базовые классы + переопределения под JDK 21
jar --create --file app.jar --main-class com.example.Main \
    -C out-17 . --release 21 -C out-21 .
# → классы из out-21 лягут в META-INF/versions/21/

# модульный JAR с версией
jar --create --file lib.jar --module-version 1.4.2 -C out .

# воспроизводимая сборка: фиксированные таймстемпы (JDK 17+)
jar --create --file app.jar --date "2026-01-01T00:00:00Z" -C out .

# без сжатия — быстрее стартует, больше весит
jar --create --file app.jar --no-compress -C out .

# обновить манифест у готового jar
jar --update --file app.jar --manifest extra.mf
```

> [!tip] Воспроизводимые сборки
> `jar --date` фиксирует время элементов. В Maven тот же эффект даёт свойство `project.build.outputTimestamp`, в Gradle — `preserveFileTimestamps = false` + `reproducibleFileOrder = true`. Без этого два байт-в-байт одинаковых исходника дают разные jar-ы, и любая проверка контрольных сумм бессмысленна.

### 2.5 На практике jar собирает сборщик, а не `jar`

**Maven** — упаковка задаётся одной строкой:

```xml
<packaging>jar</packaging>   <!-- либо war, либо ear -->

<build><plugins>
  <plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jar-plugin</artifactId>
    <configuration>
      <archive>
        <manifest><mainClass>com.example.Main</mainClass></manifest>
      </archive>
    </configuration>
  </plugin>
</plugins></build>
```

**Gradle** (Kotlin DSL):

```kotlin
plugins { java }

tasks.jar {
    manifest { attributes("Main-Class" to "com.example.Main") }
    // воспроизводимость
    isPreserveFileTimestamps = false
    isReproducibleFileOrder = true
}
```

---

## 3. Fat-jar / uber-jar: три разных подхода

Обычный jar не тащит зависимости. Способы это исправить принципиально разные:

| Подход | Что делает | Проблемы |
| :--- | :--- | :--- |
| **Maven Shade / Gradle Shadow** | распаковывает все зависимости и складывает классы в один плоский jar | коллизии одинаковых путей, затирание `META-INF/services`, ломает подписи |
| **Spring Boot / nested jar** | вкладывает зависимости как **целые jar-файлы** в `BOOT-INF/lib/`, читает их своим загрузчиком | нестандартный layout, `java -cp` напрямую не работает |
| **Внешний `lib/` + `Class-Path`** | зависимости лежат рядом файлами | надо доставлять каталог целиком |

### 3.1 Shade — и обязательные трансформеры

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-shade-plugin</artifactId>
  <executions><execution>
    <phase>package</phase><goals><goal>shade</goal></goals>
    <configuration>
      <transformers>
        <!-- БЕЗ ЭТОГО ServiceLoader сломается: одноимённые файлы затрут друг друга -->
        <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
        <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
          <mainClass>com.example.Main</mainClass>
        </transformer>
      </transformers>
      <filters><filter>
        <artifact>*:*</artifact>
        <!-- иначе SecurityException: Invalid signature file digest -->
        <excludes>
          <exclude>META-INF/*.SF</exclude>
          <exclude>META-INF/*.DSA</exclude>
          <exclude>META-INF/*.RSA</exclude>
        </excludes>
      </filter></filters>
    </configuration>
  </execution></executions>
</plugin>
```

> [!danger] Две классические поломки shade-jar
> 1. **`java.util.ServiceConfigurationError` / «драйвер не найден»** — несколько зависимостей содержат `META-INF/services/java.sql.Driver`, при слиянии выживает один. Лечится `ServicesResourceTransformer`. Та же беда с `reference.conf` у Typesafe Config (нужен `AppendingTransformer`).
> 2. **`SecurityException: Invalid signature file digest for Manifest main attributes`** — в fat-jar затащили подписанную библиотеку (BouncyCastle, JDBC-драйверы) вместе с её `*.SF`/`*.RSA`. Подпись перестаёт сходиться. Лечится исключением файлов подписи — но помни, что при этом ты **сознательно выбрасываешь подпись** библиотеки.

### 3.2 Spring Boot — «вложенные jar», а не shade

```
app.jar
├── META-INF/MANIFEST.MF
│     Main-Class:  org.springframework.boot.loader.launch.JarLauncher
│     Start-Class: com.example.MyApplication
├── org/springframework/boot/loader/…   ← распакованный spring-boot-loader
└── BOOT-INF/
    ├── classes/        ← твои классы и ресурсы
    ├── lib/            ← зависимости ЦЕЛЫМИ jar-файлами
    └── classpath.idx
```

`Main-Class` — это **не** твой класс, а лаунчер; настоящая точка входа лежит в `Start-Class`. Лаунчеры (пакет `org.springframework.boot.loader.launch`, переехал туда в Spring Boot 3.2):

- `JarLauncher` — читает `BOOT-INF/lib/`;
- `WarLauncher` — читает `WEB-INF/lib/` и `WEB-INF/lib-provided/`;
- `PropertiesLauncher` — путь настраивается через `loader.path`.

Смысл отказа от shade — видно, какие библиотеки реально используются, и нет коллизий одинаковых имён файлов из разных jar.

> [!tip] Разложить boot-jar на слои для Docker
> ```bash
> java -Djarmode=tools -jar app.jar list-layers
> java -Djarmode=tools -jar app.jar extract --layers --destination extracted
> ```
> Старый `-Djarmode=layertools` объявлен deprecated в Spring Boot 3.3 и вычищается в ветке 4.x — в новых проектах сразу `jarmode=tools`. Смысл: зависимости меняются редко, свой код — часто, поэтому разложенные по слоям файлы дают эффективный кэш слоёв Docker вместо одного 60-мегабайтного jar, который пересобирается целиком на каждую правку.

---

## 4. WAR — Web Archive

### 4.1 Структура

```
app.war
├── META-INF/MANIFEST.MF
├── WEB-INF/                 ← НЕ отдаётся по HTTP, что бы клиент ни просил
│   ├── web.xml              ← дескриптор; с Servlet 3.0 не обязателен
│   ├── classes/             ← твои .class и ресурсы (распакованные!)
│   ├── lib/                 ← зависимости в виде .jar
│   └── tags/, *.tld         ← JSP-теги
├── index.jsp
├── css/, js/, img/          ← статика, отдаётся напрямую
└── WEB-INF/lib-provided/    ← только у Spring Boot executable war
```

Ключевые моменты, которых нет в посте:

- **`WEB-INF/` недоступен снаружи.** Это часть спецификации сервлетов, а не настройка. Поэтому туда кладут всё, что не должно утечь.
- **Порядок загрузки классов:** `WEB-INF/classes` → `WEB-INF/lib/*.jar` → классы контейнера. Внутри `lib/` порядок jar-файлов **не определён спецификацией** — на две версии одной библиотеки в `lib/` полагаться нельзя.
- **`Class-Path` из манифеста вложенных jar игнорируется** — контейнер строит classpath сам.
- **`war` нельзя запустить через `java -jar`** — там нет `Main-Class` (исключение: Spring Boot умеет собирать «executable war» с `WarLauncher`, который работает и как war для контейнера, и как самозапускаемый файл).

### 4.2 Сборка

```xml
<packaging>war</packaging>
<dependencies>
  <dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <version>6.1.0</version>
    <scope>provided</scope>   <!-- ← API даёт контейнер, в WEB-INF/lib он попасть не должен -->
  </dependency>
</dependencies>
```

```kotlin
// Gradle
plugins { war }
dependencies {
    compileOnly("jakarta.servlet:jakarta.servlet-api:6.1.0")   // аналог provided
}
```

> [!warning] `provided` — не формальность
> Если положить `jakarta.servlet-api` (или логгер контейнера) в `WEB-INF/lib`, получишь `LinkageError`, `ClassCastException` между «одинаковыми» классами из разных загрузчиков или молча неработающие аннотации. Всё, что предоставляет контейнер, должно быть `provided`/`compileOnly`.

### 4.3 Servlet 3.0+ — почему `web.xml` больше не нужен

Пост верно указывает на Servlet API 3.0 (2009) как на переломную точку. Что она дала:

```java
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/hello")          // вместо <servlet-mapping> в web.xml
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/plain; charset=UTF-8");
        resp.getWriter().write("привет");
    }
}
```

Плюс `ServletContainerInitializer` + `META-INF/services` (как фреймворки цепляются без единой строки XML), `@WebFilter`, `@WebListener`, `web-fragment.xml` внутри jar-библиотек и программная регистрация через `ServletContext.addServlet(...)`. Именно это и сделало возможным embedded-контейнер: Spring Boot просто поднимает Tomcat в том же процессе и регистрирует всё программно.

### 4.4 Embedded-контейнер и «Make jar, not war»

```java
// то, что делает Spring Boot: Tomcat живёт внутри процесса, war не нужен
@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

```bash
mvn package && java -jar target/app.jar     # всё, деплой закончен
```

> [!note] Лозунг верный, но не абсолютный
> «Make jar, not war» — про **типовой** микросервис в контейнере/облаке. Аргументы против war там: не нужен отдельно администрируемый Tomcat, версия сервера фиксируется вместе с приложением, образ Docker самодостаточен, локальный запуск = продакшн-запуск.
>
> WAR всё ещё оправдан, когда: корпоративный стандарт требует деплоя в общий сервер приложений; на одном контейнере крутится десяток приложений и нужен общий пул ресурсов/сессий; лицензия/поддержка привязаны к WebSphere/WebLogic; или нужен hot-redeploy без рестарта JVM.

---

## 5. EAR — Enterprise Archive

```
app.ear
├── META-INF/
│   ├── application.xml       ← перечень модулей (с Java EE 5 опционален)
│   └── application-client.xml
├── web-module.war            ← веб-модуль
├── ejb-module.jar            ← EJB-модуль
├── connector.rar             ← адаптер ресурсов (JCA)
├── client.jar                ← application client module
└── lib/                      ← общие для всех модулей библиотеки (Java EE 5+)
```

```xml
<application xmlns="https://jakarta.ee/xml/ns/jakartaee" version="11">
  <application-name>my-enterprise-app</application-name>
  <module><web><web-uri>web-module.war</web-uri><context-root>/app</context-root></web></module>
  <module><ejb>ejb-module.jar</ejb></module>
  <library-directory>lib</library-directory>
</application>
```

Ключевое: EAR даёт **общий загрузчик классов** для своих модулей, поэтому библиотеки из `lib/` видны всем модулям сразу и EJB можно звать локально, без сети. Ровно это и делало монолит монолитом.

**Кто это ещё разворачивает в 2026:** WildFly / JBoss EAP, IBM WebSphere (Liberty и traditional), Oracle WebLogic, Payara, Open Liberty, GlassFish. Tomcat и Jetty EAR **не умеют** — они сервлет-контейнеры, а не полные серверы приложений; им нужен war.

---

## 6. Актуальный контекст 2026

| Что | Состояние на август 2026 |
| :--- | :--- |
| **Jakarta EE 11** | текущий релиз; Servlet **6.1**, JSP 4.0, WebSocket 2.2; убраны ссылки на `SecurityManager` |
| **Jakarta EE 12** | в разработке, GA планировался на середину 2026 (сроки исторически плывут) |
| **Tomcat 11.0** | стабильная ветка под Jakarta EE 11, минимум **Java 17** |
| **Tomcat 10.1 / 9.0** | 10.1 — Jakarta EE 10 (`jakarta.*`), 9.0 — последняя ветка на `javax.*` |
| **Tomcat 12** | заявлен под Jakarta EE 12, минимум **Java 21**; дат нет |
| **Spring Boot** | 4.0 вышел 20 ноября 2025 на Spring Framework 7; 4.1 — с июня 2026. Базовая Java 17, первоклассная поддержка Java 25 |

> [!caution] `javax.*` → `jakarta.*` — самая болезненная миграция экосистемы
> В Jakarta EE 9 пространство имён сменилось целиком: `javax.servlet` → `jakarta.servlet`, `javax.persistence` → `jakarta.persistence` и т. д. Это **несовместимое** изменение: старый war не запустится на Tomcat 10.1+/11, а библиотека под `javax.*` не заработает со Spring Boot 3/4.
>
> Что делать: обновлять зависимости; для чужих jar без обновлений — [Eclipse Transformer](https://projects.eclipse.org/projects/technology.transformer) или `org.apache.tomcat:jakartaee-migration`, они переписывают байткод и ресурсы. Гибридного режима нет: приложение целиком либо на `javax.*`, либо на `jakarta.*`.

---

## 7. Дальше архивов: чем упаковывают сегодня

- **`jlink`** — собирает урезанный runtime-образ только из нужных JPMS-модулей. Требует, чтобы всё было модульным (либо `--add-modules` вручную).
  ```bash
  jlink --add-modules java.base,java.sql --output myruntime \
        --strip-debug --no-header-files --no-man-pages --compress=zip-6
  ```
- **`jpackage`** (финализирован в JDK 16) — делает нативный установщик/пакет: `.deb`, `.rpm`, `.msi`, `.dmg`, `app-image`.
  ```bash
  jpackage --type app-image --name MyApp --input target/ \
           --main-jar app.jar --main-class com.example.Main
  ```
- **GraalVM `native-image`** — компилирует в нативный бинарник: старт в миллисекундах, малое потребление памяти; ценой долгой сборки, закрытого мира (рефлексия требует конфигурации) и отсутствия JIT-пиковой производительности.
- **AppCDS / AOT-кэш** (JEP 483, JDK 24) — ускорение старта без отказа от jar.
- **Docker** — jar остаётся jar-ом, но раскладывается по слоям (см. §3.2).

---

## 8. Подпись JAR

```bash
# сгенерировать ключ (см. заметку про JCA)
keytool -genkeypair -alias mykey -keyalg EC -groupname secp384r1 \
        -sigalg SHA384withECDSA -keystore ks.p12 -storetype PKCS12 -validity 365

# подписать и проверить
jarsigner -keystore ks.p12 -tsa http://timestamp.digicert.com app.jar mykey
jarsigner -verify -verbose -certs app.jar
```

Появляются `META-INF/MANIFEST.MF` (с хешами каждого файла), `META-INF/*.SF` и блок подписи `*.EC`/`*.RSA`/`*.DSA`. В **JDK 26** добавлена постквантовая подпись jar: `jarsigner -sigalg ML-DSA-65`.

> [!warning] Что ломает подпись
> Любое изменение архива после подписи: добавление файла, пересжатие, shade, переупаковка `zip`-ом. Отсюда и `SecurityException` в fat-jar (§3.1). **`-tsa` (метка времени) обязателен**, иначе подпись «протухнет» вместе с сертификатом.

---

## 9. Факты против хайпа и типичные грабли

**«jar — это просто zip, значит можно править чем угодно»** — почти. Манифест обязан быть в начале, подпись чувствительна к порядку и байтам, а Spring Boot читает вложенные jar по смещениям внутри внешнего архива. Правь через `jar`/сборщик.

**«war умер»** — нет, он занял нишу. Умерла *дефолтность* war для нового зелёного проекта. Развёртывание в общий сервер приложений — живая практика в банках, телекоме и госсекторе, и там же живут EAR.

**«Spring Boot делает fat jar»** — терминологически неточно. Spring Boot делает **nested jar**, а не shaded/fat: зависимости лежат целыми файлами в `BOOT-INF/lib`, не распакованными. Из-за этого `java -cp app.jar com.example.Main` не сработает, а `unzip` покажет вложенные jar-ы, а не сплошную кучу классов.

**«Все три формата собираются утилитой `jar`»** — формально да (пост прав, это zip), практически никто так не делает: war собирает `maven-war-plugin`/Gradle `war`, ear — `maven-ear-plugin`. Они правильно раскладывают `WEB-INF/lib`, генерируют `application.xml` и учитывают scope зависимостей.

**`java -cp ... -jar app.jar` тихо игнорирует `-cp`.** Одна из самых частых потерь времени у новичков — никакого предупреждения не будет.

**Fat-jar не бесплатен:** размер (десятки-сотни МБ), потеря информации о том, какие библиотеки внутри (плохо для SCA-сканеров и SBOM), сломанные `META-INF/services`, конфликты версий, которые в обычном classpath хотя бы диагностируются.

**Multi-release JAR — не «сборка под несколько версий»,** а точечное переопределение отдельных классов. Базовые классы обязаны компилироваться под минимальную поддерживаемую версию, а версионные — иметь **тот же публичный API**, иначе поведение станет зависеть от JDK на машине.

**`Class-Path` в манифесте не понимает wildcard** и не работает для jar внутри war. Разделитель — пробел; пути относительны расположению jar.

**Zip Slip.** Если распаковываешь чужой архив кодом — проверяй нормализованный путь:
```java
Path target = destDir.resolve(entry.getName()).normalize();
if (!target.startsWith(destDir)) throw new IOException("Zip Slip: " + entry.getName());
```

**Порядок jar в `WEB-INF/lib` не определён.** Если приложение «работает только когда библиотека называется `a-…`» — это не решение, это отложенная авария.

---

## 10. Применимость по системам

Форматы платформо-независимы: один и тот же jar/war одинаково работает везде, где есть JDK нужной версии. Различается только **чем ты его собираешь и куда деплоишь**.

| Система | JDK | Сборщики | Контейнер / сервер | Нюансы |
| :--- | :--- | :--- | :--- | :--- |
| **Gentoo** (основная) | `emerge dev-java/openjdk` — слоты 8/11/17/21/25, из исходников (`jbootstrap`/`system-bootstrap`) | `dev-java/ant` собирается из исходников; **Maven и Gradle — только `-bin`**: `dev-java/maven-bin` (3.9.x), `dev-java/gradle-bin` | `www-servers/tomcat` — слоты **11**, **10.1**, **9**; USE `extra-webapps`, `source`, `verify-sig`; служба через OpenRC | ⚠ Maven/Gradle из исходников в дереве нет — это классическая проблема самобутстрапа Java-сборщиков. Если бинарь принципиально не годится, вариант — Maven/Gradle Wrapper (`./mvnw`, `./gradlew`) в самом проекте: качается в `~/.m2`/`~/.gradle`, Portage не трогает |
| **Debian / Ubuntu** | `apt install openjdk-21-jdk` | `apt install maven gradle ant` | `apt install tomcat10` / `tomcat11` (доступность зависит от релиза), systemd-юнит, конфиг в `/etc/tomcat*/` | Версия Gradle в репозитории обычно сильно отстаёт → на практике всё равно Wrapper или SDKMAN |
| **Arch** | `pacman -S jdk-openjdk` (или `jdk21-openjdk`) | `pacman -S maven gradle apache-ant` | `pacman -S tomcat11` / `tomcat10` | Свежие версии сборщиков приезжают раньше всех; переключение JDK — `archlinux-java set java-21-openjdk` |
| **Entware** (ASUS RT-AX56U, armv7) | ⚠️ **практичной JVM нет** | — | — | 512 МБ RAM / 256 МБ flash не для JVM и не для Tomcat. Роутер тут — транспорт/reverse-proxy к приложению на нормальном хосте, не место деплоя. Распаковать/посмотреть jar можно: `opkg install unzip` |

> [!tip] Кроссплатформенный минимум
> Разбор чужого артефакта требует ровно двух вещей — `unzip` и `java`:
> ```bash
> unzip -l app.war | head -40
> unzip -p app.jar META-INF/MANIFEST.MF
> unzip -p app.jar BOOT-INF/classpath.idx     # Spring Boot: список зависимостей
> ```

---

## 11. Чек-лист

- [ ] Новый сервис → **jar** со встроенным контейнером. WAR — только если этого требует целевая инфраструктура.
- [ ] Точка входа задаётся `-e`/плагином сборщика, а не ручной правкой `MANIFEST.MF`.
- [ ] Помни: `java -jar` игнорирует `-cp`.
- [ ] В war всё, что даёт контейнер, — `provided`/`compileOnly`.
- [ ] В shade-jar подключён `ServicesResourceTransformer` и исключены `META-INF/*.SF|DSA|RSA`.
- [ ] Для Docker — `-Djarmode=tools extract --layers`, а не один жирный слой.
- [ ] Воспроизводимость: `jar --date` / `project.build.outputTimestamp` / `preserveFileTimestamps = false`.
- [ ] Подпись — с `-tsa`; после подписи архив не трогать.
- [ ] Распаковка чужих архивов — с проверкой на Zip Slip.
- [ ] Мигрируешь на Tomcat 10.1+/Spring Boot 3+ — сначала полностью `javax.*` → `jakarta.*`.

---

## Связанные заметки

- [Java — платформа и язык (JVM, JDK/JRE, Gentoo)](../Java%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%20%28JVM%2C%20JDK-JRE%2C%20%D1%8D%D0%BA%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%29%20%D0%B8%20%D0%BE%D1%81%D0%BE%D0%B1%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B8-%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20%D0%BD%D0%B0%20Gentoo%20%28eselect%20java-vm%29%20%D0%B8%20%D0%B4%D1%80.md) — JDK/JVM, слоты OpenJDK и `eselect java-vm` на Gentoo.
- [Ключи в Java (JCA) — KeyFactory и KeyPairGenerator](../Crypto/%D0%9A%D0%BB%D1%8E%D1%87%D0%B8%20%D0%B2%20Java%20%28JCA%29%20%E2%80%94%20%D1%87%D1%82%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyFactory%20%D0%B8%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyPairGenerator%20%28SPI%2C%20KeySpec%2C%20PEM-DER%2C%20ECC%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%29.md) — ключи и подпись: `keytool`/`KeyStore` для `jarsigner`, ML-DSA в JDK 26.
- [JaCoCo — покрытие Java-кода тестами](../JaCoCo%20%E2%80%94%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20Java-%D0%BA%D0%BE%D0%B4%D0%B0%20%D1%82%D0%B5%D1%81%D1%82%D0%B0%D0%BC%D0%B8%20%28bytecode-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F%2C%20Maven-Gradle%2C%20CI-CD%2C%20%D0%BE%D1%82%D1%87%D1%91%D1%82%D1%8B%29%20%D0%B8%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BF%D0%BE%D0%BA%D1%80%D1%8B%D1%82%D0%B8%D0%B5%20%E2%89%A0%20%D0%BA%D0%B0%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%BE.md) — инструментация байткода в jar и покрытие тестами.
- [Java Generics — T, wildcards, PECS, стирание типов](../Generics/Java%20Generics%20%E2%80%94%20%D0%B4%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D0%BA%D0%B8%20%28%D0%BE%D0%B1%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D1%8F%29%3A%20T%2C%20wildcards%2C%20PECS%2C%20%D1%81%D1%82%D0%B8%D1%80%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%82%D0%B8%D0%BF%D0%BE%D0%B2%20%E2%80%94%20%D1%81%20%D0%B0%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%BC%D0%B8%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80%D0%B0%D0%BC%D0%B8.md) — стирание типов, из-за которого в архиве нет информации о параметрах типов.
- [nginx — веб-сервер и reverse-proxy](../../../Network/WebServers/nginx/nginx%20%E2%80%94%20%D0%B2%D0%B5%D0%B1-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B8%20reverse-proxy%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%2C%20server-location%2C%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%2C%20%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20TLS%2C%20%D0%BA%D1%8D%D1%88%20%28%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%29.md) — reverse-proxy перед Java-приложением вместо прямого выставления Tomcat наружу.
- [DockerScan — сканер безопасности Docker-образов](../../../Security/Vulns/Linux/DockerScan%20%28cr0hn%29%20%E2%80%94%20%D1%81%D0%BA%D0%B0%D0%BD%D0%B5%D1%80%20%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20Docker-%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%20%D0%BD%D0%B0%20Go%20%28CIS%2C%20%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D1%8B%2C%20CVE%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%B8.md) — сканирование образов, в которые уезжает собранный jar.

## Ссылки

- Пост-источник: [@javatasks/2373 — «В чём разница между jar и war?»](https://t.me/javatasks/2373)
- [`jar` Tool Reference (JDK 25)](https://docs.oracle.com/en/java/javase/25/docs/specs/man/jar.html) · [JAR File Specification](https://docs.oracle.com/en/java/javase/25/docs/specs/jar/jar.html)
- [Jakarta EE 11 Release](https://jakarta.ee/release/11/) · [Jakarta Servlet 6.1](https://jakarta.ee/specifications/servlet/6.1/)
- [Apache Tomcat — Which Version Do I Want?](https://tomcat.apache.org/whichversion.html)
- [Spring Boot — Launching Executable Jars](https://docs.spring.io/spring-boot/specification/executable-jar/launching.html) · [Spring Boot 4.0.0 available now](https://spring.io/blog/2025/11/20/spring-boot-4-0-0-available-now/)
- [Spring Boot — Dockerfiles / layered jars](https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html)
- [Maven Shade Plugin — Resource Transformers](https://maven.apache.org/plugins/maven-shade-plugin/examples/resource-transformers.html)
- Gentoo: [dev-java/openjdk](https://packages.gentoo.org/packages/dev-java/openjdk) · [dev-java/maven-bin](https://packages.gentoo.org/packages/dev-java/maven-bin) · [www-servers/tomcat](https://packages.gentoo.org/packages/www-servers/tomcat)

#Java #JAR #WAR #EAR #Упаковка #Jakarta_EE #Spring_Boot #Программирование
