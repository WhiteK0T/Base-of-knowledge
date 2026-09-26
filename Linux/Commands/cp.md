---
создал заметку: 2026-09-26T22:00:00
author: WhiteK0T
tags:
  - cp
  - Linux
  - Coreutils
  - Файловые_системы
  - Шпаргалка
Источник:
  - https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html
  - https://github.com/coreutils/coreutils/blob/v9.11/src/cp.c
  - https://github.com/coreutils/coreutils/blob/v9.11/src/copy.c
  - https://github.com/coreutils/coreutils/blob/v9.11/NEWS
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cp.html
---

# 📄 cp — копирование файлов: что он делает на самом деле

`cp` из **GNU coreutils** выглядит самой простой командой из трёх (`cp`, [mv](mv.md), [rm](rm.md)), но у него есть свойство, которое удивляет почти всех: **существующий файл назначения `cp` не заменяет, а перезаписывает на месте**. Он открывает его с `O_TRUNC`, обнуляет и пишет новые данные в **тот же инод**. Отсюда:

- все, кто держит этот файл открытым, видят его обнулённым и недописанным;
- все жёсткие ссылки на файл назначения меняются вместе с ним;
- если назначение — символическая ссылка, `cp` пишет **в её цель**;
- запущенный бинарник так заменить нельзя (`Text file busy`);
- при нехватке места старое содержимое уже уничтожено, а новое недописано.

У `mv` поверх файла в той же ФС всё наоборот: атомарная подмена имени. Эта разница — главное, что нужно знать про `cp`.

Заметка написана **по исходникам** `coreutils v9.11` (`src/cp.c`, `src/copy.c`) и проверена руками на Gentoo с `cp (GNU coreutils) 9.11`. Для сравнения на тех же тестах прогнаны **BusyBox 1.37.0** (собран из исходников, `defconfig`) и **uutils 0.10.0** (Ubuntu 26.04). Всё, что помечено «проверено», реально запускалось.

> [!info] Версии на момент написания (26.09.2026)
> | Где | Что за `cp` |
> | :--- | :--- |
> | **Gentoo** (проверялось здесь) | GNU coreutils `9.11-r1` |
> | **Arch** | GNU coreutils `9.11-2` |
> | **Debian** | GNU: forky/sid `9.10-1` · trixie `9.7-3` · bookworm `9.1-1` |
> | **Ubuntu** | 24.04 noble — GNU `9.4` · **25.10 и 26.04 — по умолчанию uutils** (`rust-coreutils`, в 26.04 `0.10.0`) |
> | **Entware** (`armv7sf-k3.2`) | `coreutils-cp 9.9-2` |
> | **BusyBox** в прошивке роутера | `1.37.0` — **свой `cp`, не coreutils** |

## 📋 Опции — полный список (из `cp --help` 9.11)

| Опция | Что делает |
| :--- | :--- |
| `-r`, `-R`, `--recursive` | копировать каталоги рекурсивно |
| `-a`, `--archive` | `-dR --preserve=all`: рекурсивно, ссылки как ссылки, все атрибуты |
| `-p` | `--preserve=mode,ownership,timestamps` |
| `--preserve[=СПИСОК]` / `--no-preserve=СПИСОК` | `mode`, `ownership`, `timestamps`, `links`, `context`, `xattr`, `all` |
| `-d` | `--no-dereference --preserve=links` |
| `-P`, `--no-dereference` | никогда не разыменовывать ссылки в источнике |
| `-L`, `--dereference` | всегда разыменовывать ссылки |
| `-H` | разыменовывать только ссылки из командной строки |
| `--keep-directory-symlink` | идти по существующим ссылкам на каталоги в назначении |
| `-f`, `--force` | если файл назначения **не открывается** — удалить его и повторить |
| `--remove-destination` | удалять файл назначения **до** открытия (сравните с `-f`) |
| `-i`, `--interactive` | спрашивать перед перезаписью |
| `-n`, `--no-clobber` | (устарела) молча пропускать существующие файлы |
| `--update[=UPDATE]` | `all` / `none` / `none-fail` / `older` (= `-u`) — как у `mv` |
| `-u` | копировать, только если назначение старше |
| `-b`, `--backup[=CONTROL]`, `-S` | резервные копии заменяемых файлов, как у `mv` |
| `-l`, `--link` | делать **жёсткие ссылки** вместо копий |
| `-s`, `--symbolic-link` | делать символические ссылки |
| `--reflink[=WHEN]` | CoW-клоны: `auto` (**по умолчанию** с 9.0) / `always` / `never` |
| `--sparse=WHEN` | разреженные файлы: `auto` (по умолчанию) / `always` / `never` |
| `--attributes-only` | скопировать только атрибуты, без данных |
| `--copy-contents` | при рекурсии читать **содержимое** спецфайлов (FIFO, устройств) |
| `--parents` | воссоздать путь источника внутри каталога назначения |
| `-x`, `--one-file-system` | не выходить за пределы ФС |
| `-t`, `-T`, `--strip-trailing-slashes` | как у `mv` |
| `--debug` | объяснить, как копировался файл (включает `-v`) |
| `-v`, `--verbose` | печатать, что делается |
| `-Z`, `--context[=CTX]` | SELinux/SMACK-контекст |

## 🧬 Главное: перезапись **на месте**, а не замена

В `copy.c`, функция `copy_reg()`:

```c
  /* The semantics of the following open calls are mandated
     by the specs for both cp and mv.  */
  if (! *new_dst)
    {
      int open_flags =
        O_WRONLY | O_BINARY | (data_copy_required ? O_TRUNC : 0);
      dest_desc = openat (dst_dirfd, dst_relname, open_flags);
```

Существующий файл открывается на запись с обнулением. Нового инода не появляется, и всё, что привязано к старому, видит изменения:

```bash
# проверено:
$ stat -c %i d; cp s d; stat -c %i d
4593619
4593619                           # тот же инод — файл переписан на месте

$ echo orig > h1; ln h1 h2; cp s2 h1; cat h2
NEW                               # жёсткая ссылка h2 изменилась вместе с h1

$ echo secret > target; ln -s target lnk; cp s3 lnk; cat target
PWN                               # cp записал В ЦЕЛЬ ссылки; lnk осталась ссылкой

$ chmod 600 m2; cp m1 m2; stat -c %a m2
600                               # права существующего файла сохраняются (у m1 было 755)
```

Последний пункт часто упускают: без `-p` при перезаписи **права, владелец и ACL остаются от старого файла**, а не от источника. У нового файла права берутся от источника с учётом `umask`, а биты setuid/setgid снимаются:

```bash
# проверено:
$ stat -c %A /usr/bin/passwd;  cp /usr/bin/passwd pw; stat -c %A pw
-rwsr-xr-x
-rwxr-xr-x                        # setuid снят
```

### Кто видит недописанный файл

```bash
# проверено: 200 МБ поверх уже существующей копии
$ cp big bigdst & sleep 0.02; stat -c %s bigdst
24379392                          # читатель видит 23 МБ из 200
```

Пока `cp` работает, любой процесс, читающий файл назначения (веб-сервер, демон, перечитывающий конфиг, `tail`), получает обрезок. Для конфигов и всего, что читается «на лету», это прямой путь к сбою.

### Запущенный бинарник

```bash
# проверено:
$ ./ms 20 &
$ cp /bin/true ms
cp: cannot create regular file 'ms': Text file busy       # exit=1
$ cp -f /bin/true ms                                       # exit=0
$ cp --remove-destination /bin/true ms                     # exit=0
```

Ядро не даёт писать в исполняемый файл запущенного процесса (`ETXTBSY`). `-f` обходит это так: открыть не удалось → удалить → создать заново. `--remove-destination` удаляет **сразу**, не пытаясь открыть. В обоих случаях появляется новый инод, а работающий процесс остаётся со старым (в `lsof` он будет `(deleted)`).

> [!tip] Как заменять файлы правильно
> | Задача | Команда | Почему |
> | :--- | :--- | :--- |
> | Атомарно подменить конфиг или бинарник | `cp new f.tmp && mv -f f.tmp f` | `mv` в той же ФС — атомарный `rename()`, читатели видят старое или новое целиком. Подробности в [mv](mv.md) |
> | Установить файл с нужными правами | `install -m 0644 -o root new /etc/app.conf` | `install` удаляет старый файл и создаёт новый (жёсткие ссылки и цель симлинка не трогает, проверено), права задаются явно |
> | Не писать через ссылку и в жёсткие ссылки | `cp --remove-destination src dst` | удаляет имя, создаёт новый файл, сторонние ссылки не трогает |
> | Скопировать **с** атрибутами источника | `cp -p` или `cp -a` | иначе права останутся от старого файла назначения |

## 💥 Нехватка места: старое содержимое уничтожено сразу

Раз файл обнуляется при открытии, любая ошибка записи оставляет **обрезок** вместо старой версии. Причём это происходит в той же ФС, а не только при переносе между ФС, как у `mv`:

```bash
# проверено: файл 3 МБ копируется поверх важного файла на tmpfs размером 2 МБ
$ cat mnt/big
OLD IMPORTANT
$ cp big mnt/big
cp: error writing 'mnt/big': No space left on device
exit=1
$ ls -il mnt/big
2 -rw-r--r-- 1 root root 2097152 mnt/big      # тот же инод, OLD IMPORTANT потерян
```

`cp` не делает резервную копию сам. Если старая версия важна, используйте `cp -b` / `--backup=numbered` или копируйте во временный файл и переименовывайте через `mv`.

## ⚙️ Как `cp` копирует данные: reflink, `copy_file_range`, sparse

`cp` не просто читает и пишет буфер. В порядке приоритета:

1. **Reflink (CoW-клон)** через `ioctl(FICLONE)`: с **coreutils 9.0** это поведение по умолчанию (`--reflink=auto`). На Btrfs, XFS (с `reflink=1`) и bcachefs копия создаётся **мгновенно** и не занимает места, пока одна из копий не изменится.
2. **`copy_file_range()`** — копирование внутри ядра без передачи данных в пользовательское пространство. На NFS 4.2 и SMB копирование делает сам сервер.
3. Обычные `read()`/`write()`, с обнаружением «дыр» через `SEEK_HOLE`.

`--debug` показывает, что сработало:

```bash
# проверено (ext4 → ext4 и ext4 → tmpfs):
$ cp --debug b1 b2
'b1' -> 'b2'
copy offload: yes, reflink: unsupported, sparse detection: no
$ cp --debug b1 /dev/shm/b2
'b1' -> '/dev/shm/b2'
copy offload: unsupported, reflink: unsupported, sparse detection: no
```

> [!warning] Reflink на Btrfs — копия не является резервной
> После `cp` на Btrfs оба файла указывают на **одни и те же физические блоки**. Если эти блоки повредятся (сбой диска, битый сектор), испортятся обе «копии». Для настоящей резервной копии на том же Btrfs используйте `cp --reflink=never` или, лучше, копию на другой диск. Подробнее — в [Btrfs](../Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md).

### Разреженные файлы

```bash
# проверено: 1 ГБ «дыры» (образ диска, файл БД, swap-файл)
$ truncate -s 1G sp
$ cp sp sp2;      du -h sp2        # 0      — дыры сохранены
$ cat sp > sp3;   du -h sp3        # 1.0G   — cat записал гигабайт нулей
$ busybox cp sp sp4; du -h sp4     # 1.0G   — BusyBox тоже!
```

Для образов виртуальных машин и дисков это разница между «мгновенно и 0 байт» и «гигабайты на диске». На роутере с USB-флешкой и BusyBox по умолчанию — вторая ситуация.

## 📁 Каталоги: `-r` против `-a` и ловушка повторного запуска

| Что | `cp -r` | `cp -a` |
| :--- | :--- | :--- |
| Время изменения | **текущее** | сохраняется |
| Права | от источника с `umask`, без setuid | сохраняются |
| Владелец | тот, кто копирует | сохраняется (только root) |
| Жёсткие ссылки внутри дерева | **размножаются** в отдельные файлы | сохраняются |
| Символические ссылки | копируются как ссылки | копируются как ссылки |
| xattr, ACL, SELinux | нет | да |

```bash
# проверено:
$ touch -d 2020-01-01 src/x/f
$ cp -r src r1; cp -a src a1; stat -c %y r1/x/f a1/x/f
2026-09-26 21:49:09               # -r: дата копирования
2020-01-01 00:00:00               # -a: исходная

$ ln hl/a hl/b; cp -r hl hlr; cp -a hl hla; stat -c %h hlr/a hla/a
1                                 # -r: две независимые копии
2                                 # -a: связь сохранена
```

> [!caution] `cp -a` и `cp -p` от обычного пользователя молча теряют владельца и setuid
> `cp -a /usr/bin/passwd pw` (и `cp -p`, и даже `--preserve=ownership`) завершается с `exit 0` без единого сообщения, но `pw` принадлежит вам и без `s` (проверено). Ошибку «не удалось сменить владельца» от обычного пользователя `cp` не показывает. Для резервных копий системных файлов нужен root (или `tar`/`rsync` от root).

### Повторный запуск кладёт копию внутрь

Результат `cp -r src dst` зависит от того, **существует ли уже `dst`**:

```bash
# проверено:
$ cp -r src dst     # dst нет → dst/x/f          (dst — копия src)
$ cp -r src dst     # dst есть → dst/src/x/f     (src скопирован ВНУТРЬ dst)
```

Скрипт синхронизации, запущенный второй раз, создаёт вложенную копию. Чтобы поведение не зависело от этого, укажите явно:

```bash
cp -rT src dst       # всегда «dst — это копия src», даже если dst есть (проверено)
cp -r src/. dst      # скопировать СОДЕРЖИМОЕ src в dst, включая скрытые (проверено)
```

В отличие от `rsync`, у `cp` завершающий слеш у источника **ничего не меняет**: `cp -r src/ dst` ведёт себя как `cp -r src dst`. Содержимое без самого каталога копирует только `src/.`.

### Символические ссылки: с `-r` и без

Правило из `cp.c`:

```c
  if (x.dereference == DEREF_UNDEFINED)
    {
      if (x.recursive && ! x.hard_link)
        /* This is compatible with FreeBSD.  */
        x.dereference = DEREF_NEVER;
      else
        x.dereference = DEREF_ALWAYS;
    }
```

- `cp ссылка куда` (без `-r`) копирует **файл, на который указывает ссылка**;
- `cp -r` копирует **сами ссылки**. Относительная ссылка `../tt` после копирования в другое место может стать битой;
- `cp -rL` разыменовывает всё: вместо ссылок получаются копии файлов.

### FIFO и устройства: `cp` может зависнуть

```bash
# проверено:
$ mkfifo ff; timeout 2 cp ff ffc; echo $?
124                               # завис: cp ждёт данных из канала
$ cp -r fd fd2                    # внутри fd/ есть FIFO — создаётся новый FIFO, без зависания
```

Без `-r` `cp` **читает** спецфайл как обычный. С `-r` он создаёт такой же узел через `mknod` (`--copy-contents` возвращает чтение). Поэтому `cp /dev/sda disk.img` работает как `dd`, а `cp -r` на каталог с устройствами создаёт новые узлы устройств (для этого нужен root).

Файлы в `/proc` и `/sys` с размером `0` копируются нормально: `cp /proc/cpuinfo ci` даёт 12 КБ (проверено). `cp` читает до конца файла, а не до `st_size`.

### Каталог в самого себя

```bash
# проверено:
$ cp -r q q/sub
cp: cannot copy a directory, 'q', into itself, 'q/sub'
exit=1
$ find q
q  q/sub  q/1  q/sub/1            # но ЧАСТИЧНАЯ копия осталась
```

GNU `cp` обнаруживает рекурсию, уже начав копировать, и не убирает за собой. Типичный источник — `cp -r * backup/`, когда `backup` лежит в том же каталоге.

### `--parents` и `-x`

```bash
# проверено:
$ cp --parents a/b/c/f bk/        # → bk/a/b/c/f — удобно для выборочного бэкапа
$ cp -ax / /mnt/newroot/          # перенос корня без /proc, /sys, /dev и других смонтированных ФС
```

## ❓ `-i`, `-n`, `-u`, `-f` и коды возврата

Коды возврата такие же, как у `mv` (с той же историей `-n`, см. таблицу версий в [mv](mv.md)):

```bash
# проверено на 9.11:
$ cp -n s d;                  echo $?   # 0 — пропущен молча
$ cp --update=none-fail s d;  echo $?   # cp: not replacing 'd' → 1
$ echo n | cp -i s d;         echo $?   # 1
$ cp -u s d;                  echo $?   # 0 — назначение новее, пропущен молча
$ cp s s;                     echo $?   # cp: 's' and 's' are the same file → 1
```

А вот с защищённым от записи файлом назначения `cp` ведёт себя **не как `mv`**:

```bash
# проверено:
$ chmod 444 ro
$ cp s ro                    # даже в терминале — вопроса нет:
cp: cannot create regular file 'ro': Permission denied      # exit=1
$ cp -f s ro                 # exit=0: удалил и создал заново, права стали 644
```

`mv` в терминале спросит `replace 'ro', overriding mode 0444?`, а `cp` сразу завершится ошибкой. `-f` у `cp` означает не «не спрашивать», а «**удалить, если не открывается**». `cp -f` поверх read-only файла возвращает `exit 0`, а файл получает новые права.

Одна особенность из `cp --help`: при `-f` вместе с `-b` и одинаковых источнике и назначении `cp` делает резервную копию **источника** (`cp -f --backup s s` → `s~`, проверено).

## ⚠️ Ловушки, общие с `mv` и `rm`

- **Имена с дефисом в глобе.** `cp * dir/` с файлом `-n` в каталоге молча превращается в `cp -n ...`. Пишите `cp -- * dir/` или `cp ./* dir/`.
- **Скрытые файлы.** `cp -r src/* dst/` пропускает `.hidden`, а `cp -r src/. dst/` копирует их.
- **Несуществующий каталог назначения.** `cp f newdir` создаст **файл** `newdir`. Используйте `cp f newdir/` (ошибка `Not a directory`) или `-t newdir`.
- **`cp` не делает `fsync`.** После `cp` на USB-флешку данные могут ещё висеть в кэше. Перед извлечением: `sync` (или `sync -f /mnt/usb`).

## ✅ Проверка утверждений

| Утверждение | Вердикт | Пояснение |
| :--- | :--- | :--- |
| «`cp` поверх файла создаёт новый файл» | ❌ **Нет** | `O_TRUNC` на существующий инод; проверено: инод тот же |
| «Жёсткие ссылки на назначение не затронет» | ❌ Нет | Меняются все, это один инод. BusyBox — наоборот, см. ниже |
| «`cp` поверх симлинка заменит симлинк» | ❌ Нет | GNU и uutils пишут в **цель**; помогает `--remove-destination` |
| «Права у файла будут как у источника» | ⚠️ Только у нового файла | У перезаписанного остаются старые, пока нет `-p`/`-a` |
| «Замена конфига через `cp` безопасна» | ❌ Нет | Читатель видит обрезок (проверено: 23 МБ из 200); атомарно — только `cp` во временный файл + `mv` |
| «Если `cp` упал, старый файл цел» | ❌ Нет | Обнулён при открытии; при `ENOSPC` остаётся обрезок |
| «`cp -f` — это «не спрашивать»» | ❌ Нет | Это «удалить, если не открывается». Без `-f` `cp` не спрашивает, а падает |
| «`cp -r` и `cp -a` почти одинаковы» | ❌ Нет | `-r` сбрасывает даты, размножает жёсткие ссылки, не переносит xattr/ACL |
| «`cp -a` сохранит владельца» | ⚠️ Только root | От пользователя — молча `exit 0` без владельца и setuid (так же `-p`) |
| «`cp -r src dst` идемпотентен» | ❌ Нет | Второй запуск → `dst/src`; используйте `-T` или `src/.` |
| «Слеш в конце `src/` меняет поведение, как в rsync» | ❌ Нет | Для `cp` `src/` = `src`; содержимое — `src/.` |
| «Копия на Btrfs независима от оригинала» | ⚠️ Логически да, физически нет | С 9.0 по умолчанию reflink: общие блоки |
| «`cp` сохраняет разреженность» | ✅ GNU и uutils — да | BusyBox — **нет** (1 ГБ нулей, проверено) |
| «`cp` безопасен для FIFO» | ❌ Без `-r` зависает | Читает канал; с `-r` создаёт новый FIFO |
| «`cp -r dir dir/sub` ничего не сделает» | ❌ Нет | Ошибка, но частичная копия остаётся (GNU и BusyBox) |

## 💻 На твоих системах

| Система | Что делать |
| :--- | :--- |
| **Gentoo** | Уже стоит (`sys-apps/coreutils`, у меня `9.11-r1`, часть `@system`). Для больших и повторяемых копий — `net-misc/rsync` (докачка, проверка, `--link-dest`). Для reflink-копий на Btrfs ничего ставить не нужно, это поведение по умолчанию |
| **Debian / Ubuntu** | Уже стоит (`Essential: yes`). **Проверьте реализацию**: `cp --version`. На Ubuntu 25.10/26.04 по умолчанию uutils; вернуть GNU — `sudo apt install coreutils-from-gnu`. `rsync`: `sudo apt install rsync` |
| **Arch** | Уже стоит (`core/coreutils`, `9.11-2`). `rsync`: `sudo pacman -S rsync` |
| **Entware / RT-AX56U** | ⚠️ По умолчанию `cp` — апплет **BusyBox 1.37.0**. Полноценный: `opkg install coreutils-cp` (версия `9.9-2`, 49 КБ в пакете / 110 КБ установленный; тянет `coreutils` и `libacl`). Для копирования на USB-диск с проверкой и докачкой — `opkg install rsync` (`3.4.1-3`) |

### ⚠️ BusyBox `cp` на роутере — другой алгоритм перезаписи

Опции (при `FEATURE_CP_LONG_OPTIONS` и `FEATURE_CP_REFLINK`, в `defconfig` обе включены): `-a -r/-R -d/-P -L -H -p -f -i -n -l -s -T -t -u -v`, длинные `--remove-destination`, `--parents`, `--reflink`. **Нет** `-x`, `-b`/`--backup`, `--preserve=...`, `--sparse`, `--update=...`, `--debug`.

Главное отличие — в `libbb/copy_file.c` при включённом `CONFIG_FEATURE_NON_POSIX_CP` (в `defconfig` — `y`):

```c
		if (ENABLE_FEATURE_NON_POSIX_CP || (flags & FILEUTILS_INTERACTIVE)) {
			/*
			 * O_CREAT|O_EXCL: require that file did not exist before creation
			 */
			dst_fd = open(dest, O_WRONLY|O_CREAT|O_EXCL, new_mode);
```

Существующий файл **не перезаписывается**: `open` с `O_EXCL` падает, файл удаляется (`unlink`) и создаётся заново. Комментарий авторов о поведении по POSIX: *«This is strange, but POSIX-correct»*. На практике:

```bash
# проверено на BusyBox 1.37.0 (defconfig):
$ echo orig > h1; ln h1 h2; busybox cp s9 h1; cat h2
orig                        # жёсткая ссылка НЕ изменилась (у GNU — изменилась бы)
$ ln -s tg lk; busybox cp s lk; cat tg
sec                         # цель ссылки цела, lk стал обычным файлом
$ chmod 444 ro; busybox cp s ro; echo $?
0                           # read-only файл молча заменён (GNU — Permission denied)
$ ./ms 20 & busybox cp /bin/true ms; echo $?
0                           # запущенный бинарник заменён без Text file busy
$ echo n | busybox cp -i s d; echo $?
0                           # отказ = успех (у GNU — 1)
$ busybox cp sp sp4; du -h sp4
1.0G                        # разреженность НЕ сохраняется
$ busybox cp big mnt/big    # переполнение
cp: write error: No space left on device    # старый файл уже удалён
```

Итого на роутере `cp` ведёт себя **как GNU `cp --remove-destination` всегда**. Это безопаснее для ссылок, но **read-only файлы и работающие бинарники заменяются молча**, а образы с дырами раздуваются до полного размера. Какие именно опции собраны в прошивке ASUS, зависит от её конфигурации: проверьте `busybox cp --help`.

```bash
# на роутере
opkg install coreutils-cp
which cp          # ожидается /opt/bin/cp (Alternatives: 300:/opt/bin/cp:/opt/libexec/cp-coreutils)
cp --version      # cp (GNU coreutils) 9.9
```

> [!note] Как и с `mv` и `rm`, подмена действует только на твою сессию
> Скрипты прошивки вызывают `/bin/cp` и получают BusyBox. Про `Alternatives` — в [OPKG](../Package-Manager/OPKG.md).

### uutils (Ubuntu 25.10+) — совместим с GNU

Проверено на `cp (uutils coreutils) 0.10.0`: перезапись на месте (жёсткая ссылка и цель симлинка меняются, как у GNU), `-n` → 0, отказ на `-i` → 1, read-only назначение → `Permission denied`, разреженность сохраняется, `-a` сохраняет жёсткие ссылки, FIFO без `-r` так же зависает. Отличия мелкие:

- `cp -r q q/sub` **не оставляет** частичной копии (чище, чем GNU), но в сообщении странный путь `'q/sub/q'`;
- при нехватке места сообщение другого формата: `cp: 'big' -> 'mnt/big': No space left on device`. Старое содержимое теряется так же.

## 🔗 Ссылки

- Документация: [GNU coreutils — `cp` invocation](https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html) · [POSIX `cp`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cp.html) · локально `info '(coreutils) cp invocation'`
- Исходники: [`src/cp.c`](https://github.com/coreutils/coreutils/blob/v9.11/src/cp.c) · [`src/copy.c`](https://github.com/coreutils/coreutils/blob/v9.11/src/copy.c) · [`NEWS`](https://github.com/coreutils/coreutils/blob/v9.11/NEWS) · BusyBox [`coreutils/cp.c`](https://git.busybox.net/busybox/tree/coreutils/cp.c?h=1_37_stable), [`libbb/copy_file.c`](https://git.busybox.net/busybox/tree/libbb/copy_file.c?h=1_37_stable)
- Связанные: [mv — атомарная замена и перенос между ФС](mv.md) · [rm — удаление](rm.md) · [scp — копирование по SSH](scp.md) · [lsof — кто держит старый инод](lsof.md) · [strace — увидеть `FICLONE` / `copy_file_range`](strace.md) · [Btrfs — reflink и снапшоты](../Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md) · [OPKG](../Package-Manager/OPKG.md)

#cp #Linux #Coreutils #Файловые_системы #Шпаргалка
