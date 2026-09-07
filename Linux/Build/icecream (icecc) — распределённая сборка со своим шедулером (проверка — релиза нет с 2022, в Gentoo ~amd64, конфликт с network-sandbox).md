---
создал заметку: 2026-09-07T05:20:00
author: WhiteK0T
tags:
  - Gentoo
  - Portage
  - Сборка
  - icecream
  - distcc
  - Оптимизация
Источник:
  - https://github.com/icecc/icecream
  - https://github.com/icecc/icecream/blob/master/README.md
  - https://github.com/gentoo/gentoo/tree/master/sys-devel/icecream
  - https://github.com/gentoo/portage/blob/master/lib/portage/package/ebuild/doebuild.py
---

# icecream (icecc) — распределённая сборка с центральным шедулером

> [!info] Что это
> Форк distcc от SUSE. Из README дословно:
>
> > *«Icecream was created by SUSE based on distcc. Like distcc, Icecream takes compile jobs from a build and distributes them among remote machines allowing a parallel build. But unlike distcc, Icecream uses a central server that dynamically schedules the compile jobs to the fastest free server.»*
>
> Два принципиальных отличия от [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md): **шедулер**, который сам решает, кому отдать задание, и **раздача тулчейна** — компилятор уезжает на узлы вместе с работой, поэтому совпадение версий gcc не требуется.
>
> И два предупреждения: **последний релиз — 1.4 от 4 марта 2022 года**, а на Gentoo связка с Portage конфликтует с включённой по умолчанию песочницей сети (раздел 4).

---

## 1. Чем принципиально отличается от distcc

| | distcc | icecream |
| :--- | :--- | :--- |
| Кто выбирает исполнителя | клиент, по порядку в списке хостов | **шедулер**, по текущей загрузке |
| Совпадение версий gcc | **обязательно** | не требуется — тулчейн едет с заданием |
| Обнаружение узлов | статический список | **броадкаст** UDP или явный адрес |
| Узел ушёл в офлайн | задание падает | шедулер его просто не выберет |
| Разные архитектуры | нужен crossdev на помощниках | поддерживается через `ICECC_VERSION` |
| Мониторинг | `distccmon-text` | `icemon` с графикой |
| Транспорт | TCP или SSH | только TCP |
| Шифрование | через SSH | **нет** |

Из README, раздел «I use distcc, why should I change?»:

> *«If you're sitting alone home and use your partner's computer to speed up your compilation and both these machines run the same Linux version, you're fine with distcc (as 95% of the users reading this chapter will be, I'm sure).»*

И перечень случаев, когда distcc не подходит:

> - *«you're changing compiler versions often and still want to speed up your compilation»*
> - *«you don't know what machines will be on-line at compile time»*
> - *«**most important**: you're sitting in an office with several co-workers that do not like if you overload their workstations when they play doom (distcc doesn't have a scheduler)»*

Последний пункт — суть проекта. icecream родился в офисе SUSE, где десятки рабочих станций и надо было не мешать людям работать.

---

## 2. Раздача тулчейна — главная фича

В обычном режиме демон сам собирает тарбол с окружением и рассылает его:

> *«Under normal circumstances this is handled transparently by the icecream daemon, which will prepare a tarball with the environment when needed. This is the recommended way, as the daemon will also automatically update the tarball whenever your compiler changes.»*

Вручную это делается так:

```bash
icecc --build-native
# получится ddaea39ca1a7c88522b185eca04da2d8.tar.bz2 — переименуйте во что-то внятное
export ICECC_VERSION=/path/to/gcc-15.2-amd64.tar.gz
```

Файл уезжает на узлы, распаковывается в chroot, и задание исполняется **вашим** компилятором.

> [!warning] Цена этой фичи — root на узлах
> Из README: *«This requires that the icecream daemon runs as root»*, и раньше: *«note: they _all_ must be running as root. In the future icecream might gain the ability to know when machines can't accept a different env, but for now it is all or nothing»*.
>
> То есть либо все демоны в сети работают от root и умеют chroot, либо ни один не принимает чужое окружение — и тогда сеть должна быть однородной, как у distcc.

### `-march=native` всё равно нельзя

Тонкость, которую легко упустить. Раздача тулчейна решает проблему **версий** gcc, но не проблему **флагов**: `-march=native` раскрывается компилятором в момент запуска, по тому процессору, на котором он исполняется. А исполняется он на удалённом узле. Значит ваш же gcc, приехавший в тарболе, на чужой машине определит чужой CPU.

README про Gentoo говорит ровно это, только другими словами:

> *«It is recommended to remove all processor specific optimizations from the CFLAGS line in /etc/portage/make.conf. On the aKademy cluster it proved useful to use only "-O2", otherwise there are often internal compiler errors, if not all computers have the same processor type/version»*

---

## 3. Состояние проекта

| | |
| :--- | :--- |
| Репозиторий | `icecc/icecream`, 1821★, GPL-2.0 |
| **Последний релиз** | **1.4, 4 марта 2022** |
| Предыдущие | 1.4rc1 (2020), 1.3.1 (2020), 1.3 (2019) |
| Последний коммит | 4 марта 2026 |
| Открытых issue | 90 |
| В Gentoo | `sys-devel/icecream-1.4-r1` |
| **Ключворды в Gentoo** | `~amd64 ~arm ~hppa ~loong ~ppc ~sparc ~x86` — **нестабильна везде** |

Проект не мёртв, но релизов нет четыре с половиной года — примерно как у [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) (3.4 от 2021). Отдельно стоит отметить, что в Gentoo пакет **не стабилизирован ни на одной архитектуре** — понадобится:

```bash
echo "sys-devel/icecream ~amd64" >> /etc/portage/package.accept_keywords/icecream
```

---

## 4. Главная засада на Gentoo — песочница сети

Это то, чего нет ни в одном гайде, но что проверяется по исходникам Portage.

`network-sandbox` входит в **умолчания** Portage (`cnf/make.globals`), то есть фаза `src_compile` выполняется в отдельном сетевом неймспейсе без связи с внешним миром. Для локальной сборки это правильно, но icecc нужно достучаться до шедулера.

Для distcc в Portage сделано исключение — `lib/portage/package/ebuild/doebuild.py`:

```python
if (
    not networked
    and mysettings.get("EBUILD_PHASE") not in ("depend", "nofetch")
    and ("network-sandbox-proxy" in features or "distcc" in features)
):
    # Provide a SOCKS5-over-UNIX-socket proxy to escape sandbox
    ...
    mysettings["PORTAGE_SOCKS5_PROXY"] = proxy
    mysettings["DISTCC_SOCKS_PROXY"] = proxy
```

В списке — `network-sandbox-proxy` и **`distcc`**. Слова `icecream` там **нет**.

Практический вывод: с `FEATURES="icecream"` и умолчаниями компиляция уходит в неймспейс без сети, icecc не находит шедулер и молча сваливается на локальную сборку. Вы увидите, что «всё работает», только медленно.

Апстримный README знает об этом и предлагает грубое решение:

> *«To use icecream with emerge/ebuild use `PREROOTPATH="/opt/icecream/libexec/icecc/bin" FEATURES="-network-sandbox" emerge bla`»*

На современной Gentoo `PREROOTPATH` уже не нужен (см. раздел 7), а вот отключать песочницу придётся:

```bash
FEATURES="icecream -network-sandbox" emerge -av пакет
```

Или, если icecream используется постоянно, — в `/etc/portage/make.conf`. Взамен вы теряете защиту от ебилдов, которые лезут в сеть на этапе сборки; для распределённой сборки это осознанный размен.

---

## 5. Установка и настройка на Gentoo

```bash
echo "sys-devel/icecream ~amd64" >> /etc/portage/package.accept_keywords/icecream
emerge -av sys-devel/icecream dev-util/icemon
```

Из ебилда `icecream-1.4-r1`: EAPI 8, зависимости `app-arch/libarchive`, `app-arch/zstd`, `dev-libs/lzo`, `sys-libs/libcap-ng`, плюс `acct-user/icecream` и `acct-group/icecream` — **пользователь заводится автоматически**. Собирается с `--enable-clang-rewrite-includes --enable-clang-wrappers`, то есть clang поддержан из коробки.

Регистрация в системе подмены компилятора — тот же shadowman, что у distcc и ccache:

```bash
eselect compiler-shadow update icecc   # выполняется в pkg_postinst
# каталог символических ссылок: /usr/libexec/icecc/bin
```

Монитор в Gentoo есть: `dev-util/icemon-3.3_p20250520`.

### Конфигурация: `/etc/conf.d/icecream`

Gentoo кладёт туда конфиг, унаследованный от SUSE. Разбор всех переменных:

| Переменная | По умолчанию | Смысл |
| :--- | :--- | :--- |
| `ICECREAM_RUN_SCHEDULER` | `no` | **запускать ли шедулер на этой машине** |
| `ICECREAM_SCHEDULER_HOST` | пусто | адрес шедулера, если броадкаст не проходит |
| `ICECREAM_NETNAME` | пусто | имя сети — можно держать несколько независимых кластеров в одной LAN |
| `ICECREAM_MAX_JOBS` | пусто (по числу CPU) | сколько заданий принимать. **`0` трактуется как `1` и заодно ставит `--no-remote`** |
| `ICECREAM_ALLOW_REMOTE` | `yes` | принимать ли чужие задания |
| `ICECREAM_NICE_LEVEL` | `5` | приоритет компиляторов |
| `ICECREAM_BASEDIR` | `/var/cache/icecream` | куда распаковываются присланные окружения. *«In a big network this can grow quite a bit»* |
| `ICECREAM_LOG_FILE` | `/var/log/icecream/iceccd` | лог демона |
| `ICECREAM_SCHEDULER_LOG_FILE` | `/var/log/icecream/scheduler` | лог шедулера |

Одна служба поднимает и демон, и — если попросили — шедулер:

```bash
# OpenRC
rc-update add icecream default
rc-service icecream start

# systemd — два отдельных юнита
systemctl enable --now iceccd.service
systemctl enable --now icecc-scheduler.service
```

Ебилд также ставит logrotate-конфиг и определения служб для firewalld.

### Схема на две машины

```bash
# --- VPS: шедулер + рабочий демон ---
# /etc/conf.d/icecream
ICECREAM_RUN_SCHEDULER="yes"
ICECREAM_ALLOW_REMOTE="yes"
ICECREAM_MAX_JOBS="16"

# --- локальная машина: только демон, шедулер указан явно ---
ICECREAM_RUN_SCHEDULER="no"
ICECREAM_SCHEDULER_HOST="vps.example.com"
ICECREAM_ALLOW_REMOTE="no"     # не принимать чужие задания, только раздавать свои
ICECREAM_MAX_JOBS="4"
```

Рекомендация README для однородной сети другая — держать шедулер на всех:

> *«Recommended is to start the scheduler and daemon on everybody's machine. The icecream schedulers will choose one to be the master and everyone will connect to it. When the scheduler machine goes down a new master will be selected automatically.»*

Для двух узлов это избыточно.

---

## 6. Порты

Из README:

> - *TCP/10245 on the daemon computers (required)*
> - *TCP/8765 for the the scheduler computer (required)*
> - *TCP/8766 for the telnet interface to the scheduler (optional)*
> - *UDP/8765 for broadcast to find the scheduler (optional)*

> [!danger] Шифрования нет вообще
> Дословно из README: *«WARNING: Never use icecream in untrusted environments.»*
>
> В отличие от distcc, у icecream **нет SSH-режима**. По сети идут исходники, объектники и — в гетерогенном режиме — целый тарбол с вашим компилятором, который на той стороне распаковывается и исполняется. Выставлять порты 10245 и 8765 в интернет нельзя категорически.
>
> Для связки «локальная машина плюс VPS» это значит: только через **VPN или SSH-туннель**, и `ICECREAM_SCHEDULER_HOST` тогда указывает на локальный конец туннеля. UDP-броадкаст через интернет не работает по определению, так что адрес шедулера придётся задавать явно в любом случае.

---

## 7. Подключение к Portage

```bash
# /etc/portage/make.conf
FEATURES="${FEATURES} icecream -network-sandbox"
MAKEOPTS="-j20 -l8"
```

`PREROOTPATH` из README на современной Gentoo не нужен: Portage сам разбирается с PATH. Код из `doebuild.py`:

```python
masquerades = []
if distcc:
    masquerades.append(("distcc", "distcc"))
if icecream:
    masquerades.append(("icecream", "icecc"))
if ccache:
    masquerades.append(("ccache", "ccache"))

for feature, m in masquerades:
    for l in possible_libexecdirs:
        masqdir = os.path.join(os.sep, eprefix_lstrip, "usr", l, m)
        p = os.path.join(masqdir, "bin")
        ...
        mysettings["PATH"] = p + ":" + mysettings["PATH"]
```

Каждый каталог **добавляется в начало**, поэтому итоговый порядок в `PATH` получается обратным списку: **ccache → icecream → distcc → остальное**. Это ровно то, что нужно: сначала кэш, потом распределение. Ничего вручную выстраивать не надо.

Полезная деталь оттуда же: если каталог подмены не найден, Portage печатает предупреждение и **сам выключает FEATURES**:

```python
writemsg("Warning: %s requested but no masquerade dir can be found in /usr/lib*/%s/bin\n" % (m, m))
mysettings.features.remove(feature)
```

То есть при неустановленном `eselect compiler-shadow` вы увидите предупреждение, а сборка тихо пойдёт локально.

---

## 8. Связка с ccache

Тот же принцип, что и с distcc, — через префикс. Из README icecream:

> *«The easiest way to use ccache with icecream is to set CCACHE_PREFIX to icecc (the actual icecream client wrapper): `export CCACHE_PREFIX=icecc`. This will make ccache prefix any compilation command it needs to do with icecc, making it use icecream for the compilation (but not for preprocessing alone).»*

И важное предупреждение о рекурсии:

> *«In this case icecc's symlinks in /usr/lib/icecc/bin should **not** be in your path... If both ccache and icecc's symlinks are in the path it is likely the two wrappers will mistake each other for the real compiler and icecc will complain that it has recursively invoked itself.»*

Здесь возникает противоречие с тем, как это устроено в Portage: он кладёт в PATH **оба** каталога подмены. На практике это работает, потому что ccache стоит первым и вызывает не «gcc из PATH», а именно `icecc` через `CCACHE_PREFIX`. Но если вы настраиваете icecream вне Portage — руками, для своего проекта, — держите в PATH что-то одно.

Трезвая оценка от самих авторов icecream, кстати, совпадает с [моим разбором ccache](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md):

> *«Note however that ccache isn't really worth the trouble if you're not recompiling your project three times a day from scratch (it adds some overhead in comparing the source files and uses quite some disk space).»*

---

## 9. Проверка и мониторинг

```bash
# графический монитор кластера
icemon
USE_SCHEDULER=vps.example.com icemon    # если шедулер не находится броадкастом

# отладка клиента
ICECC_DEBUG=debug emerge -1 пакет
# уровни: error, warning, info, debug

# подробность демона и шедулера — ключом -v, до -vvv
# логи
tail -f /var/log/icecream/iceccd
tail -f /var/log/icecream/scheduler

# telnet-интерфейс шедулера (если включён порт 8766)
telnet localhost 8766
```

Главный признак, что распределение работает, — в `icemon` видны задания на удалённых узлах. Если всё исполняется локально, проверяйте по порядку: песочница сети (раздел 4), доступность порта 8765, наличие каталога подмены.

---

## 10. icecream против distcc для схемы «локальная машина + VPS»

Честный разбор применительно к сценарию с одним удалённым сервером.

| Критерий | icecream | distcc |
| :--- | :--- | :--- |
| Совпадение версий gcc | **не нужно** | обязательно |
| Шифрование канала | **нет**, нужен VPN или туннель | есть, режим `@host` |
| Обнаружение узлов | броадкаст бесполезен через интернет | список хостов и так статический |
| Балансировка | шедулер, но балансировать нечего | не нужна |
| Требует root на узлах | **да**, для chroot с чужим окружением | нет |
| Песочница Portage | **конфликтует**, нужен `-network-sandbox` | обходится штатно через SOCKS5-прокси |
| Состояние проекта | релиз 2022 | релиз 2021 |
| Стабильность в Gentoo | `~amd64` | **стабильна** |

**Вывод:** для двух машин через интернет icecream проигрывает distcc по всем практическим пунктам, кроме одного — независимости от версии gcc. Его сильные стороны (шедулер, автообнаружение, гетерогенность) раскрываются в локальной сети из нескольких машин, где нельзя предсказать, кто свободен.

Ситуации, где icecream уместнее:

- офис или домашняя сеть с **тремя и более** машинами;
- машины с разными дистрибутивами и версиями компилятора;
- узлы то появляются, то исчезают;
- нужно не мешать владельцам чужих машин — шедулер учитывает загрузку.

---

## 11. По системам

**Gentoo (основная):**

```bash
echo "sys-devel/icecream ~amd64" >> /etc/portage/package.accept_keywords/icecream
emerge -av sys-devel/icecream dev-util/icemon
# /etc/conf.d/icecream — раздел 5
rc-update add icecream default
# make.conf: FEATURES="icecream -network-sandbox"
```

**Debian / Ubuntu:**

```bash
apt install icecc icecc-monitor
# конфиг: /etc/icecc/icecc.conf
#   ICECC_SCHEDULER_HOST, ICECC_NETNAME, ICECC_MAX_JOBS, ICECC_ALLOW_REMOTE
systemctl enable --now iceccd
systemctl enable --now icecc-scheduler   # только на машине-шедулере
export PATH=/usr/lib/icecc/bin:$PATH
```

**Arch (планируется с июня 2026):**

```bash
pacman -S icecream
# /etc/conf.d/icecream (тот же SUSE-формат)
systemctl enable --now iceccd icecc-scheduler
export PATH=/usr/lib/icecc/bin:$PATH
# для makepkg: BUILDENV в /etc/makepkg.conf и явный PATH
```

**Entware / ASUS RT-AX56U:** пакета нет и быть не может — 512 МБ ОЗУ, armv7, и распаковка чужих тулчейнов в chroot на роутере лишена смысла.

---

## 12. Кому стоит

| Ситуация | Вердикт |
| :--- | :--- |
| Три и более машины в одной LAN | **Да**, это его сценарий |
| Машины на разных дистрибутивах и версиях gcc | **Да**, ради `ICECC_VERSION` |
| Ноутбук плюс один VPS через интернет | **Нет**, берите [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) или [binhost](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) |
| Сеть, где вы не хозяин всем машинам | **Нет**: нужен root на узлах, а шифрования нет |
| Не готовы отключать `network-sandbox` | **Нет** |
| Нужен красивый монитор кластера | Да, `icemon` — сильная сторона |

---

## Связанные заметки

- [distcc — распределённая сборка на VPS](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) — прямой конкурент, сравнение в разделе 10
- [ccache — кэш компилятора](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md) — связка через `CCACHE_PREFIX=icecc`
- [binhost — свой сервер бинарных пакетов](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) — что обычно лучше для одного удалённого сервера
- [crossdev — кросс-компиляция](crossdev%20%E2%80%94%20%D0%BA%D1%80%D0%BE%D1%81%D1%81-%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%86%D0%B8%D1%8F%20%D0%B2%20Gentoo%20%28%D0%BE%D1%82%D0%B4%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B9%2C%20%D1%81%D1%82%D0%B0%D0%B4%D0%B8%D0%B8%20s0-s4%2C%20emerge-CTARGET%3B%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%B4%D0%BB%D1%8F%20Entware-%D1%80%D0%BE%D1%83%D1%82%D0%B5%D1%80%D0%B0%20%D0%BE%D0%BD%20%D0%BD%D0%B5%20%D0%BF%D0%BE%D0%B4%D0%BE%D0%B9%D0%B4%D1%91%D1%82%29.md) — у icecream своя схема для разных архитектур, через `ICECC_VERSION`

## Ссылки

- Репозиторий: https://github.com/icecc/icecream
- README (первоисточник всех цитат): https://github.com/icecc/icecream/blob/master/README.md
- Монитор icemon: https://github.com/icecc/icemon
- Консольный монитор icecream-sundae: https://github.com/JPEWdev/icecream-sundae
- Ебилд в Gentoo: https://github.com/gentoo/gentoo/tree/master/sys-devel/icecream
- Обработка FEATURES в Portage: https://github.com/gentoo/portage/blob/master/lib/portage/package/ebuild/doebuild.py

#Gentoo #Portage #icecream #icecc #distcc #ccache #Сборка #Компиляция #Оптимизация
