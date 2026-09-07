---
создал заметку: 2026-09-07T07:10:00
author: WhiteK0T
tags:
  - Gentoo
  - Сборка
  - sccache
  - ccache
  - Rust
  - Кэш
  - Оптимизация
Источник:
  - https://github.com/mozilla/sccache
  - https://github.com/mozilla/sccache/blob/main/docs/DistributedQuickstart.md
  - https://github.com/mozilla/sccache/blob/main/docs/Rust.md
  - https://github.com/mozilla/sccache/blob/main/docs/Local.md
  - https://github.com/gentoo/gentoo/tree/master/dev-util/sccache
---

# sccache — кэш компиляции и распределённая сборка в одном

> [!info] Что это
> Инструмент от Mozilla на Rust, который закрывает сразу две задачи: работает как [ccache](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md) и как [icecream](icecream%20%28icecc%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%81%D0%BE%20%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%20%D1%88%D0%B5%D0%B4%D1%83%D0%BB%D0%B5%D1%80%D0%BE%D0%BC%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D0%B0%20%D0%BD%D0%B5%D1%82%20%D1%81%202022%2C%20%D0%B2%20Gentoo%20~amd64%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%BB%D0%B8%D0%BA%D1%82%20%D1%81%20network-sandbox%29.md), плюс умеет то, чего нет ни у кого из них — **Rust, CUDA, MSVC** и хранение кэша в облаке.
>
> Дословно из README про распределённый режим:
>
> > *«sccache also provides icecream-style distributed compilation (automatic packaging of local toolchains) for all supported compilers (including Rust). The distributed compilation system includes several security features that icecream lacks such as authentication, transport layer encryption, and sandboxed compiler execution on build servers.»*
>
> Главная оговорка для нас: **интеграции с Portage нет**. В `SUPPORTED_FEATURES` есть `ccache`, `distcc`, `icecream` — и всё.

---

## 1. Состояние проекта — лучшее в классе

| | sccache | ccache | distcc | icecream |
| :--- | :--- | :--- | :--- | :--- |
| Звёзд | **7657** | 2952 | 2303 | 1821 |
| Последний релиз | **v0.17.0, 29.07.2026** | v4.14, 23.08.2026 | 3.4, **2021** | 1.4, **2022** |
| Последний коммит | 03.09.2026 | 06.09.2026 | 05.2026 | 03.2026 |
| Открытых issue | 517 | 71 | 163 | 90 |
| Лицензия | Apache-2.0 | GPL-3+ | GPL-2 | GPL-2 |
| В Gentoo | `dev-util/sccache-0.16.0` | `dev-util/ccache-4.13.5` | `sys-devel/distcc-3.4-r9` | `sys-devel/icecream-1.4-r1` |
| Стабильность в Gentoo | **`amd64 arm64`** | `amd64` и др. | `amd64` и др. | **`~amd64`** везде |

Пятьсот с лишним открытых issue — не признак заброшенности, а следствие широты охвата: девять облачных бэкендов, пять компиляторов, три ОС. Релизы выходят раз в полтора месяца.

В дереве Gentoo четыре версии: `0.14.0`, `0.14.0-r1`, `0.15.0`, `0.16.0`. Стабильна на **amd64 и arm64** — в отличие от icecream, который не стабилизирован нигде.

---

## 2. Что умеет кэшировать

Из README:

> *«sccache supports gcc, clang, MSVC, rustc, NVCC, NVC++, hipcc, and Wind River's diab compiler.»*

| Язык / компилятор | ccache | sccache |
| :--- | :--- | :--- |
| C, C++, Objective-C (gcc/clang) | ✅ | ✅ |
| Ассемблер | ✅ | ✅ |
| **Rust (rustc)** | ❌ | ✅ |
| **CUDA (nvcc, clang)** | частично | ✅ |
| **AMD ROCm HIP (hipcc)** | ❌ | ✅ |
| **MSVC** | ✅ (4.x) | ✅ |
| NVC++, Wind River diab | ❌ | ✅ |
| C++20 модули | ❌ | частично, **только Clang** |

По C++20-модулям стоит прочитать оговорку целиком: поддержаны `-fmodule-file=`, `-fmodule-output=`, `--precompile`, `-fmodules-reduced-bmi`; а `-fmodules`, `-fcxx-modules`, `-fprebuilt-module-path` **обходят кэш**. Модули **GCC и MSVC не поддержаны вовсе**.

---

## 3. Как считается хеш

Из `docs/Caching.md`. Хеширование — **blake3**, как и у ccache 4.x.

**Для C/C++** хешируется результат препроцессора (`-E`), плюс:

> *«Hash of the compiler binary, Programming language, Flag required to compile for the given language, File in which to generate dependencies, Commandline arguments for dependency generation / the preprocessor / specifying the architecture, Extra files that need to have their contents hashed, Whether the compilation is generating profiling or coverage data, Color mode, Environment variables»*

**Для Rust** — интереснее, потому что единицей компиляции служит крейт целиком:

> *«Path to the rustc executable, Host triple for this rustc, Path to the rustc sysroot, digests of all the shared libraries in rustc's $sysroot/lib, A shared, caching reader for rlib dependencies (for dist-client), Parsed arguments from the rustc invocation»*

Обратите внимание: в хеш входят **все разделяемые библиотеки из sysroot компилятора**. Значит обновление `dev-lang/rust` обнуляет кэш Rust целиком — ровно как обновление gcc обнуляет кэш C у ccache.

---

## 4. Preprocessor cache mode — то, чего раньше не было

Старые сравнения «sccache против ccache» упирались в один довод: у ccache есть direct mode, а sccache всегда гоняет препроцессор, поэтому медленнее на попаданиях. **Это устарело.**

Из `docs/Local.md`:

> *«This is inspired by ccache's direct mode and works roughly the same. It adds a cache that allows to skip preprocessing when compiling C/C++. This can make it much faster to return compilation results from cache since preprocessing is a major expense for these.»*

> *«Preprocessor cache mode is controlled by a configuration option which is true by default»*

Режим **включён по умолчанию**, но отключается сам в целом ряде случаев:

- компилируется не C и не C++;
- компилятор не GCC и не Clang;
- **кэш не локальный** (то есть с любым облачным бэкендом режим не работает);
- присутствуют `-MP`, `-Xpreprocessor` или `-Wp,`;
- время модификации какого-то заголовка «слишком свежее» — защита от гонки;
- в исходнике встречаются `__DATE__`, `__TIME__`, `__TIMESTAMP__`.

И честный список случаев, когда режим **может отдать протухший результат**:

> *«When a source file was compiled and its results were cached, a header file would have been included if it existed, but it did not exist at the time. sccache does not know about such files, so it cannot invalidate the result if the header file later exists.»*

Плюс если вручную включить `ignore_time_macros`.

Управляется переменной `SCCACHE_DIRECT=true|false`.

---

## 5. Хранилища — главное отличие от ccache

ccache умеет локальный диск и (с 4.x) удалённые бэкенды через свой протокол. sccache умеет девять:

| Бэкенд | USE-флаг в Gentoo | Зачем |
| :--- | :--- | :--- |
| Локальный диск | — (по умолчанию) | обычный сценарий |
| **S3** и Cloudflare R2 | `s3` | общий кэш на команду |
| Google Cloud Storage | `gcs` | |
| Azure Blob | `azure` | |
| **Redis** | `redis` | быстрый общий кэш в своей сети |
| **Memcached** | `memcached` | |
| **WebDAV** | `webdav` | *совместим с ccache, Bazel и Gradle* |
| GitHub Actions cache | — | для CI |
| Alibaba OSS, Tencent COS | — | |

Плюс **многоуровневый кэш** с автоматическим backfill: локальный диск как первый уровень, S3 как второй, при попадании во второй результат подтягивается в первый.

Умолчания локального кэша (`docs/Local.md`):

| Параметр | Значение |
| :--- | :--- |
| Каталог | `~/.cache/sccache` (Linux), переменная `SCCACHE_DIR` |
| **Размер** | **10 ГБ** (у ccache — 5 GiB), переменная `SCCACHE_CACHE_SIZE` |

> [!warning] Один сервер на кэш
> *«The local storage only supports a single sccache server at a time. Multiple concurrent servers will race and cause spurious build failures.»*
>
> sccache работает по клиент-серверной модели: фоновый процесс слушает `127.0.0.1:4226` (меняется через `SCCACHE_SERVER_PORT`, либо unix-сокет через `SCCACHE_SERVER_UDS`) и завершается сам после 10 минут простоя. Два таких сервера на один каталог кэша — гарантированные плавающие ошибки сборки.

---

## 6. Rust — ради чего это в основном и ставят

Единственный кэш компилятора, который знает про `rustc`. Подключение тривиальное:

```bash
export RUSTC_WRAPPER=/usr/bin/sccache
cargo build
```

либо навсегда, в `~/.cargo/config.toml`:

```toml
[build]
rustc-wrapper = "/usr/bin/sccache"
```

Нужен cargo 1.40 или новее.

### Ограничения — их много, и они важны

Полный список из `docs/Rust.md`:

- `--emit` обязателен, и из значений поддержаны только `link`, `metadata`, `dep-info`, причём `link` обязан присутствовать;
- `--crate-name` обязателен;
- `--out-dir` обязателен, а `-o file` **не поддерживается**;
- компиляция со stdin не поддерживается;
- значения из `env!` учитываются в кэше только начиная с Rust 1.46;
- **процедурные макросы, читающие файлы с диска, могут кэшироваться неправильно**;
- **инкрементальную компиляцию нужно выключить**;
- **крейты, вызывающие системный линкер, не кэшируются вообще**: `bin`, `dylib`, `cdylib`, `proc-macro`.

Последние два пункта решают всё. Cargo по умолчанию включает инкрементальную компиляцию для членов воркспейса в профиле debug, так что без этого кэш просто не наполняется:

```bash
export CARGO_INCREMENTAL=0
```

А запрет на `bin`-крейты означает, что финальный бинарник вашего проекта каждый раз собирается заново. Кэшируются **зависимости** — и это как раз то, где уходит основное время: типичный проект тянет полторы сотни крейтов, из которых ваш код — один.

README даже предлагает обходной приём:

> *«You may be able to improve compilation time of large `bin` crates by converting them to a `lib` crate with a thin `bin` wrapper.»*

### Практический вывод для Gentoo

Пакеты вроде `dev-lang/rust`, `www-client/firefox` и всего, что собирается через `cargo.eclass`, — самые тяжёлые в системе, и [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) их не ускоряет вообще. sccache — единственный инструмент, который здесь хоть что-то даёт. Но кэш наполнится, только если вы **пересобираете ту же версию**: при обычном обновлении версия новая, исходники новые, попаданий нет. Та же логика, что [у ccache на Gentoo](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md).

Настоящая ниша — **свои проекты на Rust**, где вы пересобираете код по десять раз в день.

---

## 7. Распределённая сборка (`sccache-dist`)

Архитектура повторяет icecream: шедулер плюс сборочные серверы, тулчейн упаковывается и уезжает на узлы. Отличия — в безопасности.

### Аутентификация и шифрование, которых нет у icecream

Конфиг шедулера (`docs/DistributedQuickstart.md`):

```toml
# The socket address the scheduler will listen on. It's strongly recommended
# to listen on localhost and put a HTTPS server in front of it.
public_addr = "127.0.0.1:10600"

[client_auth]
type = "token"
token = "my client token"

[server_auth]
type = "jwt_hs256"
secret_key = "my secret key"
```

Клиенты — по токену, серверы — по JWT HS256, а поверх рекомендуется HTTPS-обёртка. Сравните с icecream, где **вообще ничего**, и README которого прямо говорит *«Never use icecream in untrusted environments»*.

### Песочница на сборочных серверах

```toml
[builder]
type = "overlay"
build_dir = "/tmp/build"
bwrap_path = "/usr/bin/bwrap"
```

> *«The build server requires bubblewrap to sandbox execution, at least version 0.3.0.»*
> *«Due to bubblewrap requirements currently the build server *must* be run as root.»*

Требование root такое же, как у icecream, но задание хотя бы исполняется в песочнице, а не просто в chroot.

> [!warning] Зависимость не прописана в ебилде
> Проверил `dev-util/sccache-0.16.0`: в `DEPEND` при `dist-server` тянется только `dev-libs/openssl`. **`sys-apps/bubblewrap` там нет.** Ставить самому:
> ```bash
> emerge -av sys-apps/bubblewrap   # 0.12.0 в дереве
> bwrap --version
> ```

### Порты и статус

| Что | Порт |
| :--- | :--- |
| Шедулер | 10600 (рекомендуется только localhost + HTTPS впереди) |
| Сборочный сервер | 10501 |
| Локальный сервер кэша | 4226 |

```bash
sccache --dist-status
# {"SchedulerStatus":["https://...",{"num_servers":3,"num_cpus":56,"in_progress":24}]}
```

Ограничения по платформам: шедулер и сборочный сервер — **только Linux** (и FreeBSD, отдельным документом). Клиенты на macOS и Windows поддержаны, но, по признанию документации, *«have seen significantly less testing»*.

Любопытная деталь: для упаковки тулчейнов не под linux64 sccache использует **скрипт из icecream**:

> *«Clients that are not targeting linux64 require the `icecc-create-env` script… You can install icecream to get this script.»*

### Готовые сервисы в Gentoo

Приятный сюрприз: ебилд ставит полноценные службы для обоих демонов — и OpenRC, и systemd:

```
/etc/init.d/sccache-scheduler   /etc/conf.d/sccache-scheduler
/etc/init.d/sccache-server      /etc/conf.d/sccache-server
/etc/sccache/{scheduler,server}.conf
```

`/etc/conf.d/sccache-server`:

```bash
#SCCACHE_SERVER_CONF="/etc/sccache/server.conf"
#SCCACHE_SERVER_LOGLEVEL=info      # error warn info debug trace
#SSD_NICELEVEL=15
#SSD_IONICELEVEL=3
```

Это лучше, чем у апстрима, где предлагается просто запускать бинарник руками.

---

## 8. Установка на Gentoo и главная проблема

```bash
emerge -av dev-util/sccache
```

Пакет `dev-util/sccache-0.16.0`, Apache-2.0, стабилен на amd64 и arm64. USE-флаги — ровно по бэкендам:

```
IUSE="azure dist-client dist-server gcs memcached redis s3 webdav"
```

По умолчанию собирается `--no-default-features`, то есть только локальный кэш. Нужен S3 — включаете `s3`, нужен распределённый режим — `dist-client` на клиенте и `dist-server` на сборщике.

Ебилд регистрируется в системе подмены компилятора:

```bash
insinto /usr/share/shadowman/tools
newins - sccache <<<"${EPREFIX}/usr/lib/sccache/bin"
```

То есть каталог `/usr/lib/sccache/bin` с симлинками `gcc`, `g++` и прочими **создаётся**, как у ccache, distcc и icecream.

### Но `FEATURES="sccache"` не существует

И вот здесь проблема. Portage знает ровно три обёртки — `doebuild.py`:

```python
ccache = "ccache" in mysettings.features
distcc = "distcc" in mysettings.features
icecream = "icecream" in mysettings.features
```

`sccache` в этот список не входит, значит каталог подмены сам в `PATH` не попадёт. Совет из старых гайдов про `PREROOTPATH` тоже мёртв: в современном Portage эта переменная встречается только в `save-ebuild-env.sh`, то есть при сохранении окружения, а как пользовательский механизм не работает.

**Что можно сделать.** Прописать `PATH` через окружение пакета:

```bash
# /etc/portage/env/sccache.conf
PATH="/usr/lib/sccache/bin:${PATH}"
SCCACHE_DIR="/var/cache/sccache"
SCCACHE_CACHE_SIZE="20G"
CARGO_INCREMENTAL="0"
RUSTC_WRAPPER="/usr/bin/sccache"
```

```bash
# /etc/portage/package.env
dev-lang/rust        sccache.conf
www-client/firefox   sccache.conf
```

> [!caution] Это не поддерживаемая конфигурация
> Официальной интеграции нет, и вести себя это может неожиданно: Portage собирает от пользователя `portage`, каталог кэша должен быть ему доступен; фоновый сервер sccache — отдельный процесс, который переживает сборку; при `FEATURES="network-sandbox"` (включена по умолчанию) облачные бэкенды из фазы сборки будут недоступны точно так же, как это происходит [у icecream](icecream%20%28icecc%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%81%D0%BE%20%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%20%D1%88%D0%B5%D0%B4%D1%83%D0%BB%D0%B5%D1%80%D0%BE%D0%BC%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D0%B0%20%D0%BD%D0%B5%D1%82%20%D1%81%202022%2C%20%D0%B2%20Gentoo%20~amd64%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%BB%D0%B8%D0%BA%D1%82%20%D1%81%20network-sandbox%29.md).
>
> Обязательно проверьте `sccache --show-stats` **до и после** сборки: если счётчики не выросли, значит обёртка не подхватилась и вы просто собирали как обычно.
>
> Для Portage штатный и предсказуемый выбор — `FEATURES="ccache"`. sccache стоит держать для **своих** проектов, вне emerge.

---

## 9. Проверка и обслуживание

```bash
sccache --start-server         # поднять фоновый сервер вручную
sccache --show-stats           # сводка попаданий и промахов
sccache --zero-stats           # обнулить счётчики
sccache --stop-server          # остановить (сам умрёт через 10 минут простоя)
sccache --dist-status          # состояние распределённого кластера

SCCACHE_LOG=trace sccache --start-server   # диагностика
SCCACHE_RECACHE=1 cargo build              # принудительно перезаписать кэш
```

Осмысленный эксперимент — тот же, что с ccache: обнулить счётчики, собрать, посмотреть, собрать ещё раз, посмотреть снова. Если во второй раз попаданий нет, ищите причину среди ограничений раздела 6.

Переменные, которые пригодятся:

| Переменная | Смысл |
| :--- | :--- |
| `SCCACHE_DIR` | каталог локального кэша |
| `SCCACHE_CACHE_SIZE` | размер, по умолчанию 10 ГБ |
| `SCCACHE_DIRECT` | включить/выключить preprocessor cache mode |
| `SCCACHE_BASEDIRS` | нормализация абсолютных путей — иначе сборка из другого каталога промахивается |
| `SCCACHE_SERVER_PORT` / `SCCACHE_SERVER_UDS` | порт или unix-сокет фонового сервера |
| `SCCACHE_RECACHE` | перезаписать запись в кэше |
| `SCCACHE_LOG` | уровень логирования |
| `RUSTC_WRAPPER` | подключение к cargo |

---

## 10. Ограничения и грабли

| Что | Суть |
| :--- | :--- |
| **Абсолютные пути** | *«By default, absolute paths to files must match to get a cache hit»*. Лечится `SCCACHE_BASEDIRS` |
| **Rust: bin-крейты** | не кэшируются вообще, потому что дёргают системный линкер |
| **Rust: инкрементальная сборка** | несовместима, нужен `CARGO_INCREMENTAL=0` |
| **Proc-macro, читающие файлы** | *«may not be cached properly»* — тихая порча |
| **Preprocessor cache mode + облако** | взаимоисключающи: режим работает только с локальным хранилищем |
| **C++20 модули GCC** | обходят кэш молча |
| **Один сервер на кэш** | параллельные серверы дают плавающие ошибки |
| **Нет интеграции с Portage** | раздел 8 |
| **dist-server требует root** | из-за bubblewrap |
| **bubblewrap не в зависимостях** | ставить руками |

---

## 11. По системам

**Gentoo:**

```bash
emerge -av dev-util/sccache
# для распределённого режима на сервере:
USE="dist-server" emerge -av dev-util/sccache sys-apps/bubblewrap
rc-update add sccache-scheduler default
rc-update add sccache-server default
```

**Debian / Ubuntu:**

```bash
apt install sccache          # либо cargo install sccache --features="dist-client"
apt install bubblewrap       # для сборочного сервера
```

**Arch (планируется с июня 2026):**

```bash
pacman -S sccache
# для makepkg проще всего через RUSTC_WRAPPER в /etc/makepkg.conf
```

**Entware / ASUS RT-AX56U:** пакета нет и не будет — это Rust-бинарник заметного размера, а роутеру нечего компилировать.

**Кроссплатформенно:** `cargo install sccache`, есть готовые бинарники под Linux, macOS и Windows, а также GitHub Action для кэша в CI.

---

## 12. Кому стоит

| Ситуация | Вердикт |
| :--- | :--- |
| **Свои проекты на Rust** | **Да, это его главная ниша.** Ничто другое rustc не кэширует |
| CUDA или HIP | **Да**, альтернатив нет |
| Общий кэш на команду или CI | **Да** — S3, Redis, WebDAV, GHA |
| Нужен кэш **для emerge** | **Нет**, берите `FEATURES="ccache"`: интеграция штатная и предсказуемая |
| Нужна распределённая сборка для Portage | **Нет**, берите [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) или [binhost](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) |
| Распределённая сборка вне Portage, но с безопасностью | **Да**, лучше icecream: токены, TLS, песочница |
| Кластер из машин, которым нельзя доверять | **Да**, единственный вариант из четырёх |

**Итог для локальной Gentoo плюс VPS:** для системы — binhost, для C-пакетов при пересборках — ccache, а sccache имеет смысл держать отдельно, под `cargo build` собственных проектов. Смешивать его с emerge можно, но это самодеятельность, которую придётся проверять счётчиками.

---

## Связанные заметки

- [ccache — кэш компилятора](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md) — штатный выбор для Portage
- [icecream (icecc)](icecream%20%28icecc%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%81%D0%BE%20%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%20%D1%88%D0%B5%D0%B4%D1%83%D0%BB%D0%B5%D1%80%D0%BE%D0%BC%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D0%B0%20%D0%BD%D0%B5%D1%82%20%D1%81%202022%2C%20%D0%B2%20Gentoo%20~amd64%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%BB%D0%B8%D0%BA%D1%82%20%D1%81%20network-sandbox%29.md) — чью схему распределения sccache повторяет, но с шифрованием
- [distcc — распределённая сборка на VPS](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) — штатный распределитель для Portage
- [binhost — свой сервер бинарных пакетов](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) — то, что закрывает задачу целиком
- [Learning Rust (dumindu)](../../Programming/Rust/Learning%20Rust%20%28dumindu%29%20%E2%80%94%20%D1%81%D0%B6%D0%B0%D1%82%D1%8B%D0%B9%20%D1%83%D1%87%D0%B5%D0%B1%D0%BD%D0%B8%D0%BA%20%D0%BF%D0%BE%20Rust%20%E2%80%94%2031%20%D0%B3%D0%BB%D0%B0%D0%B2%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%C2%AB%D0%B7%D0%B0%20%D0%BC%D0%B5%D1%81%D1%8F%D1%86%C2%BB%20%D0%B8%20%C2%AB%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%C2%BB%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F%20NON-AI%2C%20%D1%87%D0%B5%D0%BC%20%D0%B4%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D1%8C%29.md) — если Rust только начинается

## Ссылки

- Репозиторий: https://github.com/mozilla/sccache
- README (первоисточник цитат): https://github.com/mozilla/sccache/blob/main/README.md
- Оговорки по Rust: https://github.com/mozilla/sccache/blob/main/docs/Rust.md
- Локальный кэш и preprocessor cache mode: https://github.com/mozilla/sccache/blob/main/docs/Local.md
- Как считаются хеши: https://github.com/mozilla/sccache/blob/main/docs/Caching.md
- Распределённая сборка, быстрый старт: https://github.com/mozilla/sccache/blob/main/docs/DistributedQuickstart.md
- Многоуровневый кэш: https://github.com/mozilla/sccache/blob/main/docs/MultiLevel.md
- Ебилд в Gentoo: https://github.com/gentoo/gentoo/tree/master/dev-util/sccache
- GitHub Action: https://github.com/marketplace/actions/sccache-action

#Gentoo #sccache #ccache #distcc #icecream #Rust #CUDA #Сборка #Компиляция #Кэш #Оптимизация
