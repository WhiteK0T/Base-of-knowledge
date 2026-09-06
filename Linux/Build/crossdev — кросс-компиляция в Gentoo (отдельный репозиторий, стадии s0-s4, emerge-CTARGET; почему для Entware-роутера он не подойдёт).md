---
создал заметку: 2026-09-07T03:55:00
author: WhiteK0T
tags:
  - Gentoo
  - Portage
  - Сборка
  - crossdev
  - Кросс-компиляция
  - ARM
  - Embedded
Источник:
  - https://wiki.gentoo.org/wiki/Crossdev
  - https://wiki.gentoo.org/wiki/Distcc/Cross-Compiling
  - https://wiki.gentoo.org/wiki/Cross_build_environment
---

# crossdev — кросс-компиляция в Gentoo

> [!info] Что это
> `sys-devel/crossdev` собирает **полный кросс-тулчейн** под другую архитектуру средствами самого Portage: binutils, gcc, libc и заголовки ядра. После этого появляется `emerge-<CTARGET>`, которым обычные ебилды собираются под целевую платформу.
>
> Свежая версия в дереве — **20260501-r1** (стабильная на amd64), в тестировании до `20260623`.
>
> Забегая вперёд: для **сборки под роутер с Entware** crossdev не подойдёт, и в разделе 8 разобрано, почему именно — с конкретными цифрами.

---

## 1. Когда это нужно, а когда нет

| Задача | crossdev? |
| :--- | :--- |
| Собрать пакеты под Raspberry Pi / arm64-сервер, не мучая их процессор | **Да**, основной сценарий |
| Прошивка для микроконтроллера (`arm-none-eabi`) | **Да** |
| [binhost](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) для машины другой архитектуры | **Да**, VPS на amd64 собирает пакеты для arm64 |
| Помощники [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) другой архитектуры | **Да**, ради этого и появился раздел Distcc/Cross-Compiling |
| Ускорить сборку **для своей же** архитектуры | **Нет.** Дословно из вики: *«Crossdev does not create a cross compiler for a target that matches the host tuple»* — здесь нужен chroot |
| Собрать `.ipk` для Entware-роутера | **Нет**, раздел 8 |

---

## 2. Установка и обязательный отдельный репозиторий

Это первое, обо что спотыкаются: crossdev **пишет свои ебилды**, и класть их в основное дерево нельзя — при следующем `emerge --sync` они пропадут.

```bash
emerge -av sys-devel/crossdev
```

Заводим отдельный репозиторий. Через eselect:

```bash
emerge -av app-eselect/eselect-repository
eselect repository create crossdev
```

Либо руками:

```bash
mkdir -p /var/db/repos/crossdev/{profiles,metadata}
echo 'crossdev' > /var/db/repos/crossdev/profiles/repo_name
echo 'masters = gentoo' > /var/db/repos/crossdev/metadata/layout.conf
chown -R portage:portage /var/db/repos/crossdev
```

И подключаем:

```ini
# /etc/portage/repos.conf/crossdev.conf
[crossdev]
location = /var/db/repos/crossdev
priority = 10
masters = gentoo
auto-sync = no
```

`auto-sync = no` обязателен: синхронизировать этот репозиторий не с чем, его наполняет сам crossdev.

---

## 3. Синтаксис и стадии

```bash
crossdev [опции] --target ТРИПЛЕТ
```

| Флаг | Смысл |
| :--- | :--- |
| `-t`, `--target` | целевой триплет, например `aarch64-unknown-linux-gnu` |
| `--b`, `--binutils` | версия binutils |
| `--g`, `--gcc` | версия gcc |
| `--k`, `--kernel` | версия заголовков ядра |
| `--l`, `--libc` | версия libc |
| `-S`, `--stable` | брать стабильные версии |
| `--clean --target T` | снести тулчейн |
| `--ex-gcc` | дополнительные цели gcc |
| `--ex-gdb` | кросс-отладчик |
| `--ex-pkg PKG` | доставить произвольный пакет в тулчейн |

Сборка идёт стадиями, и это важно понимать при отладке — если упало, ясно, на чём:

| Стадия | Что собирается |
| :--- | :--- |
| `-s0` | только binutils |
| `-s1` | + «голый» компилятор C (без libc) |
| `-s2` | + заголовки ядра |
| `-s3` | + libc |
| `-s4` | полный компилятор — **по умолчанию** |

Курица и яйцо здесь разрешается именно так: чтобы собрать libc, нужен компилятор; чтобы собрать полноценный компилятор — нужна libc. Отсюда голый gcc на s1 и пересборка на s4.

Пример:

```bash
crossdev -S -t aarch64-unknown-linux-gnu
```

Времени это займёт прилично: собираются четыре крупных пакета, gcc дважды. На 8-ядерном VPS — порядка часа, на ноутбуке — несколько.

---

## 4. Что и куда ставится

| Что | Куда |
| :--- | :--- |
| Тулчейн | `/usr/<CTARGET>/` |
| Ебилды тулчейна | категория `cross-<CTARGET>/` в вашем crossdev-репозитории |
| Бинарники | `/usr/bin/<CTARGET>-gcc`, `-ld`, `-strip`, … |
| Обёртка Portage | `emerge-<CTARGET>` |

Сборка пакетов под цель:

```bash
emerge-aarch64-unknown-linux-gnu -av app-editors/nano
```

Обёртка сама расставляет `ROOT=/usr/<CTARGET>/`, `SYSROOT` и `PORTAGE_CONFIGROOT`, так что конфигурация цели живёт отдельно: `/usr/<CTARGET>/etc/portage/make.conf`. Там задаются **свои** `CFLAGS`, `USE`, `CHOST` — путать с хостовыми не надо.

Обновить сам тулчейн:

```bash
crossdev -t aarch64-unknown-linux-gnu     # повторный запуск обновит
crossdev --clean -t aarch64-unknown-linux-gnu
```

---

## 5. Триплеты

Формат: `АРХ-ПРОИЗВОДИТЕЛЬ-ОС-ABI`.

| Триплет | Для чего |
| :--- | :--- |
| `aarch64-unknown-linux-gnu` | 64-битный ARM: Raspberry Pi 4/5 в 64-бит, arm64-серверы |
| `armv7a-unknown-linux-gnueabihf` | 32-битный ARM, **hard-float** |
| `armv7a-unknown-linux-gnueabi` | 32-битный ARM, **soft-float** |
| `armv6j-unknown-linux-gnueabihf` | Raspberry Pi 1 / Zero |
| `arm-none-eabi` | микроконтроллеры, без ОС |
| `riscv64-unknown-linux-gnu` | RISC-V |
| `powerpc64le-unknown-linux-gnu` | POWER8+ |
| `i686-pc-linux-gnu` | 32-битный x86 |
| `x86_64-gentoo-linux-musl` | тот же x86-64, но с musl вместо glibc |

Разница `gnueabi` и `gnueabihf` — не косметическая: это разные ABI передачи вещественных чисел, бинарники несовместимы. Ошибка в этом месте даёт не понятную ошибку сборки, а неработающие бинарники на цели.

---

## 6. Связка с distcc

Ровно тот сценарий, ради которого в вики есть отдельная страница `Distcc/Cross-Compiling`: слабая машина одной архитектуры отдаёт компиляцию мощным машинам другой.

Ключевой принцип оттуда:

> *«as long as the networked boxes are all using the same toolchain built for the same processor architecture, no special distcc setup is required»*

Если архитектуры разные, на помощниках нужен crossdev с **точно теми же версиями**, что на цели. В вики есть скрипт, который прямо на целевой машине печатает готовую команду для помощников:

```bash
#!/bin/bash
BINUTILS_VER=$(qatom -F '%{PV}' $(qfile -v $(realpath /usr/bin/ld) | cut -d' ' -f1))
GCC_VER=$(qatom -F '%{PV}' $(qfile -v $(realpath /usr/bin/gcc) | cut -d' ' -f1))
KERNEL_VER=$(qatom -F '%{PV}' $(qlist -Ive sys-kernel/linux-headers))
LIBC_VER=$(qatom -F '%{PV}' $(qlist -Ive sys-libs/glibc))
echo "crossdev --b '~${BINUTILS_VER}' --g '~${GCC_VER}' --k '~${KERNEL_VER}' --l '~${LIBC_VER}' -t $(portageq envvar CHOST)"
```

Требует `app-portage/portage-utils` (`qatom`, `qfile`, `qlist`).

Отдельная тонкость на **клиенте**: многие сборочные системы зовут просто `gcc`, а не `armv7a-unknown-linux-gnueabihf-gcc`. Раньше приходилось руками класть обёртки в `/usr/lib/distcc/bin`. По замечанию вики, в distcc 3.2+ с соответствующей поддержкой это уже не нужно — distcc передаёт помощнику то имя, под которым его вызвали, и там подхватывается нужный кросс-компилятор.

---

## 7. Связка с binhost

Красивое сочетание: VPS на amd64 собирает пакеты **для arm64-машины** и раздаёт их как обычный binhost.

```bash
# на VPS
crossdev -S -t aarch64-unknown-linux-gnu
# в /usr/aarch64-unknown-linux-gnu/etc/portage/make.conf прописать
#   USE, CFLAGS и профиль ЦЕЛЕВОЙ машины, а также:
#   FEATURES="buildpkg"
#   PKGDIR="/srv/binpkgs-arm64"
emerge-aarch64-unknown-linux-gnu -uDN --buildpkg @world
```

Дальше `/srv/binpkgs-arm64` отдаётся по HTTP, а целевая машина подключает его через `binrepos.conf`. Получается, что arm64-устройство вообще ничего не компилирует — при том, что своим процессором оно собирало бы `@world` сутками.

Все требования к совпадению профиля, USE и CFLAGS из [заметки про binhost](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) действуют и здесь, только теперь их надо соблюдать между `/usr/<CTARGET>/etc/portage` и конфигурацией устройства.

---

## 8. Почему для роутера с Entware crossdev не подойдёт

Логичная мысль: раз есть ASUS RT-AX56U на armv7, соберём под него пакеты через crossdev. Не выйдет, и вот арифметика.

**Что нужно цели.** Разбор пакета `libc` из репозитория Entware `armv7sf-k3.2`:

```
Package: libc
Version: 2.27-12
Provides: libc-any
URL: http://www.gnu.org/software/libc/
```

То есть **glibc 2.27** (релиз февраля 2018). Плюс, судя по имени репозитория, `sf` — **soft-float** ABI, а ядро роутера, по исходникам прошивки, — **Linux 4.1**.

**Что может дать Gentoo сегодня.** В дереве 22 версии glibc, самая старая — **2.40**. Версии 2.27 там нет и уже не будет. Ядерные заголовки той же древности тоже давно вычищены.

| Что нужно Entware | Что есть в дереве Gentoo |
| :--- | :--- |
| glibc **2.27** (2018) | минимум **2.40** |
| ядро 4.1 | заголовки такой древности отсутствуют |
| soft-float armv7 | триплет есть, но без нужной libc бесполезен |

Даже если собрать тулчейн с glibc 2.40, полученные бинарники потребуют символов новее, чем есть в `/opt/lib/libc.so.6` роутера, и просто не запустятся.

> [!important] Правильный инструмент для Entware
> Пакеты `.ipk` собираются **OpenWrt/Entware SDK** — это собственный buildroot с зафиксированным тулчейном ровно той версии, под которую собран весь репозиторий. Он тянет свои binutils, gcc и glibc 2.27 и собирает в изолированном окружении.
>
> ```bash
> git clone https://github.com/Entware/Entware.git
> cd Entware
> make package/symlinks
> cp configs/armv7.config .config
> make -j8 toolchain/install
> make -j8 package/имя-пакета/compile V=s
> # результат: bin/packages/armv7-3.2/...ipk
> ```
>
> Это отдельная тема, но вывод простой: **crossdev — для Gentoo-целей, Entware SDK — для Entware-целей.** Не смешивать.

Впрочем, у crossdev остаётся законная роль в этой связке: если понадобится собрать что-то **не для Entware**, а для собственного chroot на USB-диске роутера с полноценным Gentoo armv7 — вот там он подойдёт целиком.

---

## 9. Грабли

| Проблема | Суть |
| :--- | :--- |
| **Ебилды в основном дереве** | Без отдельного репозитория всё сотрётся первым же `emerge --sync`. Раздел 2 |
| **Тождественный триплет** | `crossdev` откажется делать кросс-компилятор для собственной архитектуры. Для этого — chroot |
| **Падение на s3 (libc)** | Обычно несовместимость версий: старое ядро с новой glibc или наоборот. Пинить `--k` и `--l` явно |
| **Долго** | Четыре пакета, gcc дважды. Это не минуты |
| **`USE` от хоста подмешивается** | Конфигурация цели живёт в `/usr/<CTARGET>/etc/portage/`, а не в `/etc/portage/`. Частая путаница |
| **Обновление хостового gcc** | Кросс-тулчейн от него не зависит, но после крупных обновлений binutils его стоит пересобрать |
| **`~` в версиях** | В скрипте из вики версии пинятся через `'~X.Y.Z'` — кавычки обязательны, иначе bash съест тильду |
| **Не все пакеты кросс-собираются** | Пакеты, которым нужно запускать собранные бинарники в процессе сборки, ломаются. Их придётся собирать на цели или под qemu |

---

## 10. Альтернативы

**qemu-user + binfmt — эмуляция вместо кросс-компиляции.** Ставите chroot целевой архитектуры и запускаете в нём обычный `emerge`, а ядро через binfmt подсовывает эмулятор:

```bash
# USE="static-user" обязателен, иначе внутри chroot не хватит библиотек
QEMU_USER_TARGETS="aarch64 arm" emerge -av app-emulation/qemu
rc-update add qemu-binfmt default && rc-service qemu-binfmt start
cp /usr/bin/qemu-aarch64 /путь/к/chroot/usr/bin/
```

Файлы init-скрипта `qemu-binfmt.initd.head`/`.tail` есть в самом пакете `app-emulation/qemu` (в дереве версии до 10.2.2). Плюс подхода: **всё собирается «как родное»**, никаких проблем с пакетами, которые запускают свои бинарники в процессе сборки. Минус: медленно, эмуляция стоит в разы.

Разумная гибридная схема: qemu-chroot как основа плюс `distcc` с кросс-помощниками на хосте — тогда тяжёлая компиляция уходит нативному amd64-компилятору, а всё остальное честно эмулируется.

**Контейнер с целевой архитектурой.** То же самое, но через `systemd-nspawn` или Docker с `binfmt_misc` — удобнее в обслуживании.

**Готовые тулчейны.** Для не-Gentoo целей часто проще взять готовое: Linaro/ARM GNU Toolchain, musl.cc, SDK производителя. crossdev имеет смысл, когда цель — тоже Gentoo.

---

## 11. По системам

**Gentoo (хост сборки):** всё выше. Идеальное место для crossdev — тот самый VPS: 8 ядер соберут тулчейн за час, а дальше он просто лежит.

**Debian / Ubuntu:** аналог — штатные кросс-пакеты, ставятся без сборки:

```bash
dpkg --add-architecture arm64
apt update
apt install crossbuild-essential-arm64
aarch64-linux-gnu-gcc --version
```

Для сборки `.deb` под другую архитектуру — `sbuild --host=arm64` или `pbuilder` с `--architecture`.

**Arch (планируется с июня 2026):** в официальных репозиториях кросс-тулчейнов почти нет, всё в AUR:

```bash
paru -S aarch64-linux-gnu-gcc aarch64-linux-gnu-binutils aarch64-linux-gnu-glibc
# для голого металла: arm-none-eabi-gcc есть в extra
```

Сборка AUR-пакетов под другую архитектуру штатно не поддерживается — практикуется `qemu-user-static` плюс chroot.

**Entware / ASUS RT-AX56U:** цель, а не хост, и цель именно для **Entware SDK**, а не для crossdev — раздел 8. Сам роутер (armv7, 512 МБ ОЗУ) собирать тулчейн не может физически.

---

## 12. Кому стоит

| Ситуация | Вердикт |
| :--- | :--- |
| Есть arm64-устройство на Gentoo, собирать на нём больно | **Да**, crossdev + binhost — лучшая связка |
| Микроконтроллеры, `arm-none-eabi` | **Да** |
| Разнородный distcc-кластер | **Да**, иначе никак |
| Нужно собрать пакеты для роутера с Entware | **Нет**, нужен Entware SDK |
| Нужно ускорить сборку для своей же архитектуры | **Нет**, это chroot или [binhost](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) |
| Разовая сборка одной программы под ARM | Проще qemu-chroot или готовый тулчейн |
| Пакеты, которые запускают свои бинарники при сборке | Только qemu-эмуляция |

---

## Итог по всем четырём инструментам

| Инструмент | Что уносит с локальной машины | Требует совпадения | Когда нужен |
| :--- | :--- | :--- | :--- |
| [**binhost**](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) | всё: configure, компиляцию, линковку | профиль, USE, CFLAGS | основной путь |
| [**distcc**](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) | только компиляцию `.i` → `.o` | версию gcc и `-march` | когда нужна сборка «здесь и сейчас» |
| [**ccache**](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md) | ничего, но не повторяет работу | ничего | точечно, при пересборках одного и того же |
| **crossdev** | всё, для другой архитектуры | версии тулчейна с целью | когда цель — не x86-64 |

Для описанной связки «локальная Gentoo плюс VPS 7950X3D» порядок такой: **binhost как основа**, ccache на сборщике, distcc — по желанию, crossdev — только если появится ARM-устройство на Gentoo.

---

## Связанные заметки

- [binhost — свой сервер бинарных пакетов](binhost%20%E2%80%94%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D1%85%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Gentoo%20%D0%BD%D0%B0%20VPS%20%28binrepos.conf%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20PORTAGE_BINHOST%2C%20gpkg%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D0%B1%D1%8F%D0%B7%D0%B0%D0%BD%D0%BE%20%D1%81%D0%BE%D0%B2%D0%BF%D0%B0%D0%B4%D0%B0%D1%82%D1%8C%29.md) — куда складывать кросс-собранные пакеты
- [distcc — распределённая сборка на VPS](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) — кросс-помощники, раздел 6
- [ccache — кэш компилятора](ccache%20%E2%80%94%20%D0%BA%D1%8D%D1%88%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20Gentoo%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20%D0%B3%D0%BB%D0%BE%D0%B1%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BD%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%D0%B4%D1%83%D1%8E%D1%82%2C%20%D1%81%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20%D1%81%20distcc%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20CCACHE_PREFIX%2C%20%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0%20%D0%BA%D1%8D%D1%88%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%B4%D0%B0%D0%B5%D1%82%29.md) — работает и с кросс-тулчейном
- [OPKG](../Package-Manager/OPKG.md) — формат цели, под которую crossdev как раз не годится
- [Kernel — сборка или обновление ядра](../Gentoo/Kernel%20-%20%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%D0%BB%D0%B8%20%D0%9E%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%8F%D0%B4%D1%80%D0%B0.md) — кросс-сборка ядра тем же тулчейном

## Ссылки

- Gentoo Wiki, crossdev: https://wiki.gentoo.org/wiki/Crossdev
- Gentoo Wiki, distcc для разных архитектур: https://wiki.gentoo.org/wiki/Distcc/Cross-Compiling
- Gentoo Wiki, окружение кросс-сборки: https://wiki.gentoo.org/wiki/Cross_build_environment
- Репозиторий crossdev: https://gitweb.gentoo.org/proj/crossdev.git/
- Entware SDK (для роутера — вместо crossdev): https://github.com/Entware/Entware
- Пакеты Entware для armv7: https://bin.entware.net/armv7sf-k3.2/

#Gentoo #Portage #crossdev #Кросс_компиляция #ARM #Embedded #Сборка #Компиляция #Entware
