---
создал заметку: 2026-09-07T02:40:00
author: WhiteK0T
tags:
  - Gentoo
  - Portage
  - Сборка
  - ccache
  - distcc
  - Оптимизация
Источник:
  - https://wiki.gentoo.org/wiki/Ccache
  - https://github.com/ccache/ccache/blob/master/doc/manual.adoc
  - https://ccache.dev/
---

# ccache — кэш компилятора

> [!warning] Сразу главное
> ccache кэширует результат компиляции **одного и того же исходника с теми же флагами**. На Gentoo это означает, что при обычном `emerge -uDN @world` он почти не попадает: там компилируются **новые версии** пакетов, а новая версия — это новые исходники и другой хеш.
>
> Gentoo прямым текстом не советует включать его глобально:
>
> > *«Using ccache globally is not recommended as it will saturate the cache and have few cache hits! Enable it instead for specific packages.»*
>
> Это поправка к моей же фразе из [заметки про distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) про «бесплатно и без рисков»: бесплатно — не совсем, а пользы меньше, чем кажется.

---

## 1. Как работает и почему это важно понимать

ccache считает хеш от набора входных данных и, если такой уже видел, отдаёт готовый объектник вместо запуска компилятора.

Два основных режима:

| Режим | Что хеширует | Плюсы | Минусы |
| :--- | :--- | :--- | :--- |
| **direct** (по умолчанию включён) | исходник, список включённых заголовков из своего манифеста, флаги, компилятор | быстро, препроцессор не запускается | чувствителен к любым изменениям |
| **preprocessor** (fallback) | результат работы `cpp` | терпим к части изменений форматирования и флагов | приходится гонять препроцессор |
| **depend** (`depend_mode`, по умолчанию **выключен**) | только флаги и файлы зависимостей, без препроцессора вообще | самый дешёвый промах | попаданий меньше всего |

В хеш входит и сам компилятор — по умолчанию его mtime и размер. Значит **любое обновление gcc обнуляет весь кэш**. Это ровно та причина, по которой на Gentoo кэш «саморазрушается»: обновили `sys-devel/gcc` — и всё, что было накоплено, стало мусором, который ещё и занимает место, пока не вытеснится.

---

## 2. Когда кэш реально попадает

Это самая важная часть заметки. Честный список ситуаций, где ccache себя окупает:

| Ситуация | Попадания | Почему |
| :--- | :--- | :--- |
| **Смена USE-флага без смены версии** | **высокие** | исходники те же, меняется часть флагов и объём собираемого |
| **`emerge --emptytree` / пересборка мира** | **высокие** | ровно те же версии, что уже собирались |
| **`revdep-rebuild`, пересборка после смены ABI** | высокие | те же версии |
| **Разработка: правите файл, пересобираете пакет** | **очень высокие** | меняется один файл из тысячи |
| **Пересборка ядра** после мелкой правки конфига | высокие | большая часть `.c` не изменилась |
| **Откат на предыдущую версию пакета** | высокие | она уже собиралась |
| **Обычное `emerge -uDN @world`** | **низкие** | новые версии = новые исходники |
| **После обновления gcc** | **нулевые** | компилятор входит в хеш |
| **Первая сборка чего угодно** | нулевые | кэш пуст по определению |

Отсюда и рекомендация Gentoo: включать не глобально, а для пакетов, которые вы часто пересобираете.

---

## 3. Состояние проекта

В отличие от [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md), который заморожен с 2021 года, ccache **очень живой**: 2952 звезды, коммиты вчерашним днём, релизы каждые пару недель.

| | |
| :--- | :--- |
| Последний релиз upstream | **v4.14**, 23 августа 2026 |
| Перед ним | v4.13.6 (4 мая), v4.13.5 (26 апреля), v4.13.4, v4.13.3 |
| В дереве Gentoo | `dev-util/ccache-4.13.5`, стабильна на amd64 |
| Лицензия | GPL-3+ (сам ccache), BLAKE3 под CC0/Apache-2.0 |

Ебилд подписан: `VERIFY_SIG_METHOD=minisig`, ключ в `/usr/share/openpgp-keys/ccache.minisig`. Приятная мелочь — не все проекты так делают.

---

## 4. Умолчания, которые стоит знать

Из `doc/manual.adoc` v4.14:

| Опция | По умолчанию | Комментарий |
| :--- | :--- | :--- |
| `max_size` (`CCACHE_MAXSIZE`) | **5 GiB** | «Use 0 for no limit». Суффиксы kB/MB/GB/TB и KiB/MiB/GiB/TiB, по умолчанию GiB |
| `compression` | **включено** | zstd |
| `compression_level` | **0** | то есть дефолтный уровень zstd; больше — плотнее и медленнее |
| `direct_mode` | **true** | |
| `depend_mode` | **false** | см. раздел про distcc |
| `hash_dir` | **true** | текущий каталог входит в хеш, если сборка с `-g` |
| `base_dir` | пусто | переписывание абсолютных путей в относительные |
| `cache_dir` | `$HOME/.ccache`, иначе `$XDG_CACHE_HOME/ccache`, иначе `$HOME/.cache/ccache` | **но на Gentoo Portage переопределяет** |

Файл конфигурации ищется в `/etc/ccache.conf` и `${CCACHE_DIR}/ccache.conf`.

> [!caution] Ловушка с `PORTAGE_TMPDIR`
> На Gentoo, если `CCACHE_DIR` не задан, Portage кладёт кэш в **`${PORTAGE_TMPDIR}/ccache`**. А `PORTAGE_TMPDIR` у многих смонтирован в **tmpfs** — тогда кэш живёт в оперативке и исчезает при перезагрузке. То есть ровно то, ради чего всё затевалось, не работает. Задавайте `CCACHE_DIR` явно и на диске.

---

## 5. Установка и включение

```bash
emerge -av dev-util/ccache
```

Пакет использует тот же механизм подмены компилятора, что и distcc: в `pkg_postinst` вызывается `eselect compiler-shadow update ccache`, который раскладывает симлинки в `/usr/lib/ccache/bin/`.

### Правильный путь: точечно, а не глобально

Создаём окружение:

```bash
# /etc/portage/env/ccache.conf
FEATURES="${FEATURES} ccache"
CCACHE_DIR="/var/cache/ccache"
CCACHE_SIZE="20G"
CCACHE_UMASK="0002"
```

И назначаем его конкретным пакетам:

```bash
# /etc/portage/package.env
sys-kernel/gentoo-sources     ccache.conf
www-client/firefox            ccache.conf
dev-qt/qtwebengine            ccache.conf
media-libs/mesa               ccache.conf
```

Логика отбора: сюда попадает то, что вы **пересобираете, не меняя версии** — из-за USE-флагов, из-за `--emptytree`, из-за разработки. Тяжёлые пакеты, которые обновляются раз в квартал, в этот список не нужны: они всё равно каждый раз новые.

### Если всё-таки глобально

```bash
# /etc/portage/make.conf — вопреки рекомендации вики
FEATURES="${FEATURES} ccache"
CCACHE_DIR="/var/cache/ccache"
CCACHE_SIZE="50G"
```

Тогда закладывайте кэш побольше: при глобальном включении 5 ГБ по умолчанию вытесняются за один `@world`, и вы получаете только накладные расходы.

### Права

Portage собирает от пользователя `portage`, значит каталог должен быть ему доступен:

```bash
mkdir -p /var/cache/ccache
chown -R portage:portage /var/cache/ccache
chmod 2775 /var/cache/ccache          # setgid, чтобы новые файлы наследовали группу
```

Симптом неверных прав — сборка идёт, но `ccache -s` показывает нули или ошибки вида «Failed to create directory».

---

## 6. Связка с distcc — не так, как пишут в старых гайдах

Классический совет «пропишите `CC="ccache distcc gcc"`» — **неправильный**. Из мануала ccache, раздел *Using ccache with other compiler wrappers*:

> *«The recommended way of combining ccache with another compiler wrapper (such as "distcc") is by letting ccache execute the compiler wrapper. This is accomplished by defining **prefix_command**, for example by setting the environment variable `CCACHE_PREFIX` to the name of the wrapper (e.g. distcc).»*

И почему именно так, а не иначе:

> *«it is not recommended to use the form `ccache anotherwrapper compiler args` as the compilation command. It's also not recommended to use the masquerading technique for the other compiler wrapper. The reason is that by default, ccache will in both cases hash the mtime and size of the other wrapper instead of the real compiler, which means that: Compiler upgrades will not be detected properly.»*

То есть при неправильной связке ccache начинает считать «компилятором» бинарник distcc — и обновление gcc перестаёт инвалидировать кэш. А это уже не просто неэффективность, это **выдача объектников, собранных старым компилятором**.

Правильно:

```bash
# /etc/portage/env/ccache-distcc.conf
FEATURES="${FEATURES} ccache distcc"
CCACHE_DIR="/var/cache/ccache"
CCACHE_SIZE="20G"
CCACHE_PREFIX="distcc"
```

Порядок работы получается такой: ccache проверяет кэш → при промахе запускает `distcc gcc ...` → distcc отправляет задание на VPS → результат кладётся в кэш.

### Бонус: `depend_mode` для distcc

Из мануала, про преимущества depend-режима:

> *«Not running the preprocessor at all can be good if compilation is performed remotely, for instance when using distcc or similar; ccache then won't make potentially costly preprocessor calls on the local machine.»*

Для связки с distcc это прямо в точку: препроцессинг — единственная тяжёлая работа, которая при distcc остаётся локальной. Ценой снижения числа попаданий её можно убрать:

```bash
CCACHE_DEPEND="true"    # или depend_mode = true в ccache.conf
```

Компромисс честный, и мануал его не скрывает: *«The cache hit rate will likely be lower since any change to compiler options or source code will make the hash different»*.

---

## 7. Проверка, что работает

```bash
# статистика (CCACHE_DIR обязателен, иначе посмотрите не туда)
CCACHE_DIR=/var/cache/ccache ccache -s

# подробнее, ccache 4.x
CCACHE_DIR=/var/cache/ccache ccache -sv

# обнулить счётчики перед экспериментом
CCACHE_DIR=/var/cache/ccache ccache -z

# посмотреть текущую конфигурацию и откуда взято каждое значение
CCACHE_DIR=/var/cache/ccache ccache -p
```

Смотреть надо на отношение `cache hit` к `cache miss`. Осмысленный эксперимент:

```bash
CCACHE_DIR=/var/cache/ccache ccache -z
emerge -1 app-editors/nano            # первый раз: одни промахи
CCACHE_DIR=/var/cache/ccache ccache -s
emerge -1 app-editors/nano            # второй раз: должны быть попадания
CCACHE_DIR=/var/cache/ccache ccache -s
```

Если при второй сборке попаданий нет — почти наверняка либо кэш в tmpfs и пропал, либо права, либо `CCACHE_DIR` в окружении Portage не тот, который вы смотрите.

Отладка одного промаха:

```bash
CCACHE_DEBUG=1 CCACHE_DEBUGDIR=/tmp/ccdbg ccache gcc -c test.c
# в /tmp/ccdbg появятся *.ccache-log и *.ccache-input-* с точным содержимым хеша
```

---

## 8. Когда ломается

ccache — вечный подозреваемый в странных сборочных ошибках. Механика проста: если хеш не учёл что-то существенное, вы получаете **чужой объектник**, и сломается это где угодно, только не там, где причина.

Порядок действий при непонятной ошибке сборки:

```bash
# 1. выключить для конкретного пакета
FEATURES="-ccache" emerge -1 проблемный/пакет

# 2. если помогло — почистить кэш и повторить
CCACHE_DIR=/var/cache/ccache ccache -C     # очистить всё
CCACHE_DIR=/var/cache/ccache ccache -c     # только вытеснить лишнее по лимиту
```

Прежде чем заводить баг в Gentoo или upstream — **соберите без ccache**. Отчёт со включённым кэшем компилятора почти наверняка вернут с просьбой перепроверить.

Отдельно про `sloppiness`: этот параметр разрешает ccache «не замечать» часть входных данных ради роста попаданий. Каждое значение — это осознанный размен корректности на скорость, и трогать его без понимания последствий не стоит. Мануал для каждого варианта честно пишет *Trade-off*.

Ещё одна тонкость, `hash_dir`: по умолчанию каталог сборки входит в хеш, если собираете с отладочной информацией (`-g`). Portage собирает каждый пакет в своём каталоге вида `/var/tmp/portage/категория/пакет-версия/work`, и для одной и той же версии он стабилен — попадания будут. Но если вы держите отладочные символы (`FEATURES="splitdebug"`, `-ggdb`) и меняете `PORTAGE_TMPDIR`, кэш обнулится.

---

## 9. По системам

**Gentoo (основная):**

```bash
emerge -av dev-util/ccache
# /etc/portage/env/ccache.conf + /etc/portage/package.env, как в разделе 5
```

Не забыть `CCACHE_DIR` на диске, а не в tmpfs.

**Debian / Ubuntu:**

```bash
apt install ccache
# вариант 1: положить /usr/lib/ccache в начало PATH
export PATH="/usr/lib/ccache:$PATH"
# вариант 2: явно
export CC="ccache gcc" CXX="ccache g++"
ccache --max-size=20G
```

Для сборки пакетов через `sbuild`/`pbuilder` кэш пробрасывается в chroot отдельной опцией — иначе он будет создаваться заново внутри каждой сборки.

**Arch (планируется с июня 2026):**

```bash
pacman -S ccache
# /etc/makepkg.conf: в BUILDENV заменить !ccache на ccache
# каталог по умолчанию ~/.cache/ccache
```

Для `makechrootpkg` кэш надо явно монтировать внутрь chroot (`-d /var/cache/ccache:/build/.cache/ccache`).

**Entware / ASUS RT-AX56U:** пакета `ccache` в репозитории `armv7sf-k3.2` **нет**, и он там не нужен: на роутере ничего не компилируется. Если собираете **для** роутера кросс-компилятором на большой машине — ccache подключается на этой большой машине обычным образом, роутер об этом не знает.

---

## 10. Кому стоит

| Ситуация | Вердикт |
| :--- | :--- |
| Часто крутите USE-флаги и пересобираете одно и то же | **Да**, точечно через `package.env` |
| Разрабатываете что-то и пересобираете пакет по кругу | **Да**, самый выгодный сценарий |
| Регулярно пересобираете ядро | **Да** |
| Просто хотите, чтобы `emerge -uDN @world` шёл быстрее | **Нет.** Попаданий почти не будет, а место и накладные расходы будут |
| Уже настроен [binhost](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) | **Скорее нет** на клиенте: он и так ничего не компилирует. **Да** на сборочном сервере, где идут пересборки по USE |
| Мало места на диске | Нет: 5 ГБ по умолчанию, для глобального режима нужны десятки |
| Ловите непонятные ошибки сборки | Выключить в первую очередь |

**Где ccache точно уместен в вашей схеме:** не на локальной машине, а **на VPS внутри chroot'а сборщика**. Там пересборки одних и тех же версий из-за правок USE случаются постоянно, диск дешёвый, а ускорение прямо конвертируется в скорость появления новых пакетов в binhost.

---

## Связанные заметки

- [binhost — свой сервер бинарных пакетов](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) — где ccache уместнее всего: на сборщике
- [distcc — распределённая сборка на VPS](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) — связка через `CCACHE_PREFIX`, раздел 6
- [Kernel — сборка или обновление ядра](../Gentoo/Kernel%20-%20%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%D0%BB%D0%B8%20%D0%9E%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%8F%D0%B4%D1%80%D0%B0.md) — один из немногих сценариев с высокими попаданиями

## Ссылки

- Gentoo Wiki, ccache: https://wiki.gentoo.org/wiki/Ccache
- Официальный мануал: https://github.com/ccache/ccache/blob/master/doc/manual.adoc
- Сайт проекта: https://ccache.dev/
- Репозиторий: https://github.com/ccache/ccache
- Раздел про связку с другими обёртками: https://ccache.dev/manual/latest.html#_using_ccache_with_other_compiler_wrappers
- `/etc/portage/package.env`: https://wiki.gentoo.org/wiki//etc/portage/package.env

#Gentoo #Portage #ccache #distcc #Сборка #Компиляция #Оптимизация
