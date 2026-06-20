---
создал заметку: 2026-06-20T12:00:00
author: WhiteK0T
tags:
  - Btrfs
  - Linux
  - Файловая_Система
  - CoW
  - Снапшоты
  - RAID
Источник:
  - https://wiki.gentoo.org/wiki/Btrfs/ru
  - https://wiki.archlinux.org/title/Btrfs_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9)
  - https://www.funtoo.org/BTRFS_Fun
  - https://btrfs.readthedocs.io/
---

# 🧬 Btrfs — современная CoW-ФС (подтома, снапшоты, RAID): практика и устройство

**Btrfs** (B-tree FS, «баттер-эф-эс») — журналируемая файловая система Linux с **копированием-при-записи (Copy-on-Write, CoW)**. Главные фишки: **подтома (subvolumes)** и почти бесплатные **снапшоты**, **контрольные суммы** данных и метаданных с самовосстановлением, **встроенный RAID** без mdadm/LVM, **прозрачное сжатие**, онлайн-изменение размера, дефрагментация и проверка — всё на смонтированной ФС.

> [!warning] Факты против страшилок (актуальный статус, 2026)
> Старые гайды (включая **Funtoo BTRFS_Fun**) пишут «experimental», «не храните важные данные», «нет зрелого инструмента ремонта». Это **устарело**. Сегодня:
> - **Single-disk, RAID0, RAID1, RAID10** — стабильны, используются в проде (openSUSE/SUSE — Btrfs по умолчанию для корня, Fedora — с F33).
> - **RAID5/RAID6 — по-прежнему НЕ для важных данных**: известна «дыра записи» (write hole) и проблемы восстановления. Если нужен паритет — bcachefs/ZFS/mdadm+ФС или RAID1/RAID10.
> - Инструменты ремонта (`btrfs check`, `btrfs rescue`, `--repair`) есть, но `--repair` — **последнее средство**, может доломать. Реальная защита от сбоев — **снапшоты + бэкапы (`btrfs send`)**, а не починка.
> - Команда `btrfs-zero-log` из старых гайдов заменена на `btrfs rescue zero-log`.

---

## 🛠️ Практика

### 0. Ядро и утилиты

ФС живёт в ядре; userspace-команды — в пакете **btrfs-progs**. Нужен также CRC32c (для контрольных сумм).

**Конфиг ядра (актуально для Gentoo — собираешь сам):**

```text
# ядра < 6.14
File systems  --->
  <*> Btrfs filesystem support          # CONFIG_BTRFS_FS=y/m
Cryptographic API --->
  Accelerated Cryptographic Algorithms for CPU (x86) --->
    <*> CRC32c (SSE4.2/PCLMULQDQ)

# ядра >= 6.14 (CRC переехал)
File systems  --->
  <*> Btrfs filesystem support
Library routines --->
  [*] Enable optimized CRC implementations
```

В Debian/Ubuntu/Arch Btrfs уже встроен в стоковое ядро — донастраивать не нужно.

| Система | Установка `btrfs-progs` |
| :--- | :--- |
| **Gentoo** | `emerge --ask sys-fs/btrfs-progs` (+ нужный CONFIG в ядре). Сервисы обслуживания — `sys-fs/btrfsmaintenance` (OpenRC) |
| **Debian / Ubuntu** | `apt install btrfs-progs` (ядро уже с Btrfs). Авто-обслуживание — пакет `btrfsmaintenance` (systemd-таймеры) |
| **Arch** | `pacman -S btrfs-progs`. Снапшоты: `pacman -S snapper snap-pac` или `timeshift`; обслуживание `btrfsmaintenance` (AUR) |
| **Entware / RT-AX56U** | **N/A** — Btrfs это ФС уровня ядра; на стоковой прошивке роутера её нет (диск обычно ext4/exFAT). Не для armv7-роутера |

### 1. Создание ФС

```bash
mkfs.btrfs /dev/sdXN                 # простейший случай
mkfs.btrfs -L rootfs /dev/sda2       # с меткой (-L)
mkfs.btrfs -d raid1 -m raid1 /dev/sdb /dev/sdc   # сразу зеркало из 2 дисков
```

> [!tip] fsck не нужен — ставь `0` в 6-м поле fstab
> Btrfs не использует классический `fsck` при загрузке. В `/etc/fstab` последняя колонка (`pass`) для btrfs-разделов должна быть **`0`**.

### 2. Подтома (subvolumes) и раскладка

Подтом — независимо монтируемое «поддерево» внутри одной ФС со своим набором снапшотов. Рекомендуется **плоская раскладка** (flat layout): корень ФС держит подтома `@`, `@home`, …, а монтируются они в нужные точки. Так корневую систему можно откатывать снапшотом, не трогая `/home`.

```bash
# монтируем верхний уровень ФС (subvolid=5) во временную точку
mount /dev/sda2 /mnt

btrfs subvolume create /mnt/@          # будущий /
btrfs subvolume create /mnt/@home      # будущий /home
btrfs subvolume create /mnt/@snapshots # хранилище снапшотов
btrfs subvolume create /mnt/@log       # /var/log (его не откатывают вместе с /)
btrfs subvolume create /mnt/@swap      # под swapfile (без снапшотов)

btrfs subvolume list /mnt              # показать все подтома + их ID
btrfs subvolume delete /mnt/@log       # удалить подтом
```

Имена с `@` — конвенция **snapper/Arch**; Timeshift по умолчанию ждёт `@` и `@home`.

### 3. Монтирование и fstab

Опции монтирования (самые ходовые): `subvol=` / `subvolid=`, `compress=zstd`, `noatime`, `ssd`, `discard=async`, `space_cache=v2`.

```bash
mount -o subvol=@,compress=zstd:3,noatime,ssd,discard=async,space_cache=v2 /dev/sda2 /mnt
```

**Пример `/etc/fstab`** (один диск, SSD, сжатие):

```fstab
# <dev>                       <mnt>      <fs>   <options>                                                  <dump> <pass>
UUID=xxxx-...  /          btrfs  subvol=@,compress=zstd:3,noatime,ssd,discard=async,space_cache=v2  0 0
UUID=xxxx-...  /home      btrfs  subvol=@home,compress=zstd:3,noatime,ssd,discard=async             0 0
UUID=xxxx-...  /var/log   btrfs  subvol=@log,compress=zstd:3,noatime,ssd                            0 0
UUID=xxxx-...  /.snapshots btrfs subvol=@snapshots,noatime,ssd                                      0 0
```

> [!note] `discard=async` vs cron-trim
> `discard=async` (с ядра 5.6) — фоновый TRIM для SSD, рекомендуется. Альтернатива — периодический `fstrim.timer` (тогда `discard` в опциях не нужен). Старый синхронный `discard` без `async` тормозит — не используй.

### 4. Сжатие (compression)

```bash
# при монтировании: compress (сжимать если выгодно) или compress-force (всегда пытаться)
mount -o compress=zstd:3 /dev/sdXY /mnt
# применить к уже записанным файлам (рекурсивно перепаковать)
btrfs filesystem defragment -r -v -czstd /mnt
```

Алгоритмы: **zstd** (универсальный, уровни `:1`..`:15`, по умолчанию `:3`) · **zlib** (плотнее, медленнее) · **lzo** (быстрый, слабее). Уже сжатые файлы (видео, jpeg, архивы) почти не ужмутся — для них выигрыш близок к нулю.

> [!tip] Отключить CoW для нагруженных random-write файлов
> Образы ВМ, большие БД, swapfile плохо дружат с CoW (фрагментация). Отключай по-файлово/по-каталогу **до записи данных**:
> ```bash
> chattr +C /var/lib/libvirt/images      # NOCOW на каталог → новые файлы внутри без CoW
> ```
> `+C` действует только на пустые файлы/новые в каталоге; сжатие на NOCOW-файлах тоже отключается.

### 5. Снапшоты: создание, откат

Снапшот — это подтом, мгновенно фиксирующий состояние (за счёт CoW занимает почти 0 места, растёт по мере расхождения).

```bash
# писаемый снапшот
btrfs subvolume snapshot /mnt/@ /mnt/@snapshots/root-2026-06-20
# read-only снапшот (-r) — нужен для btrfs send и как «эталон» отката
btrfs subvolume snapshot -r /mnt/@ /mnt/@snapshots/root-2026-06-20-ro

btrfs subvolume delete /mnt/@snapshots/root-2026-06-20   # удалить снапшот
```

**Откат корня к снапшоту** (классическая схема с плоской раскладкой):

```bash
# смонтировать верхний уровень ФС
mount -o subvolid=5 /dev/sda2 /mnt
mv /mnt/@ /mnt/@broken                                  # отодвинуть сломанный корень
btrfs subvolume snapshot /mnt/@snapshots/root-good /mnt/@   # вернуть из снапшота
reboot                                                  # @ снова монтируется как /
btrfs subvolume delete /mnt/@broken                     # позже подчистить
```

Альтернатива — назначить снапшот загрузочным по умолчанию (если не используешь именованный `@`):

```bash
btrfs subvolume set-default <ID> /mnt   # ID из `btrfs subvolume list`
# или временно через загрузчик: rootflags=subvol=@snapshots/root-good
```

**Автоматизация снапшотов:**
- **snapper** (+`snap-pac`) — авто-снапшоты до/после каждой транзакции пакетного менеджера (openSUSE/Arch). `snapper -c root create-config /` → `snapper -c root list`.
- **Timeshift** — GUI/CLI «как System Restore», ждёт раскладку `@`/`@home`.
- **btrbk** — снапшоты + инкрементальный бэкап через `send/receive` на другой диск/по SSH.

### 6. Swapfile на Btrfs

Swap-файл **обязан** быть без CoW и без сжатия, на неснапшотируемом подтоме:

```bash
btrfs subvolume create /swap            # отдельный подтом (его не снапшотим)
btrfs filesystem mkswapfile --size 8g /swap/swapfile   # btrfs-progs >= 6.1 делает всё сам
# вручную (старый способ):
#   touch /swap/swapfile && chattr +C /swap/swapfile
#   btrfs property set /swap/swapfile compression none
#   fallocate -l 8G /swap/swapfile && chmod 600 /swap/swapfile && mkswap /swap/swapfile
swapon /swap/swapfile
echo '/swap/swapfile none swap defaults 0 0' >> /etc/fstab
```

### 7. RAID и управление устройствами

```bash
btrfs filesystem show                                   # все ФС и их устройства
btrfs device add /dev/sdd /mnt                          # добавить диск в ФС
btrfs device remove /dev/sdc /mnt                       # убрать (данные переедут сами)
btrfs replace start /dev/old /dev/new /mnt              # заменить диск (лучше, чем add+remove)

# сменить профиль RAID на лету (балансировкой)
btrfs balance start -dconvert=raid1 -mconvert=raid1 /mnt
```

> [!danger] Профили и предостережения
> - **raid1** = ровно 2 копии каждого блока (на любом числе дисков), переживает смерть 1 диска. **raid1c3/raid1c4** — 3/4 копии.
> - **raid0** — без избыточности, потеря 1 диска убивает ФС.
> - **raid5/raid6 — не для важных данных** (write hole; восстановление сырое). Допустимо: data=raid5, **metadata=raid1c3** — но всё равно с бэкапом.
> - **Не выдёргивай диск до конца операции** (`remove`/`replace`/`balance`) — потеряешь данные.
> - Деградированный монтаж: `mount -o degraded /dev/sdX /mnt` (работает для raid1/raid10).

### 8. Обслуживание: scrub, balance, defrag

```bash
# SCRUB — читает все данные, сверяет контрольные суммы, чинит из копии (raid1/10/dup)
btrfs scrub start /mnt
btrfs scrub status /mnt
# раз в 1–4 недели — через systemd-таймер (btrfsmaintenance) или cron/OpenRC

# BALANCE — перепаковывает чанки; лечит ENOSPC при «рассыпанном» свободном месте
btrfs balance start -dusage=20 -musage=20 /mnt   # трогать только блоки <20% занятости (быстро)
btrfs balance status /mnt

# DEFRAG — онлайн, но осторожно
btrfs filesystem defragment -r -v /mnt
```

> [!caution] Дефрагментация и снапшоты «разрывают» CoW-связи
> `defragment` переписывает экстенты и **может расцепить общие блоки между снапшотами** → расход места резко вырастет. На ФС со снапшотами дефраг применяй точечно и осознанно. На SSD дефраг обычно не нужен вовсе.

### 9. Свободное место (обычный `df` врёт)

Из-за чанковой аллокации и профилей RAID классический `df` показывает неправду. Правильно:

```bash
btrfs filesystem usage /mnt     # самое наглядное: Device/Data/Metadata/Unallocated
btrfs filesystem df /mnt        # разбивка Data/Metadata/System по профилям
btrfs filesystem du -s /path    # реальный размер с учётом общих блоков снапшотов
compsize /path                  # коэффициент сжатия (пакет compsize / btrfs-compsize)
```

> [!warning] ENOSPC при «свободном» месте
> Btrfs может выдать «нет места», хотя `df` показывает свободное: метаданные исчерпали свои чанки, а нераспределённого (Unallocated) места нет. Лечится **balance** (см. выше). Поэтому не доводи ФС до >90% и держи периодический balance.

### 10. send / receive (бэкап и репликация)

```bash
# read-only снапшот → поток → распаковка на другой ФС
btrfs subvolume snapshot -r /mnt/@home /mnt/@snapshots/home-ro
btrfs send /mnt/@snapshots/home-ro | btrfs receive /backup/
# инкрементально (только разница от прошлого -p эталона):
btrfs send -p /mnt/@snapshots/home-prev /mnt/@snapshots/home-ro | btrfs receive /backup/
# по сети:
btrfs send /mnt/@snapshots/home-ro | ssh host 'btrfs receive /backup/'
```

### 11. Конвертация из ext4, resize, проверка

```bash
# ext3/4 -> btrfs (без перезаписи; ext-данные остаются в снапшоте ext2_saved)
umount /dev/sdX
fsck.ext4 -f /dev/sdX
btrfs-convert /dev/sdX            # затем поправить тип в fstab; убедиться → удалить ext2_saved

# изменение размера ОНЛАЙН (сначала растягивают раздел, потом ФС; при сжатии — наоборот)
btrfs filesystem resize +50G /mnt
btrfs filesystem resize max /mnt
btrfs filesystem resize -10G /mnt

# проверка/ремонт (только на размонтированной ФС; --repair — крайняя мера!)
btrfs check /dev/sdX
btrfs check --repair /dev/sdX     # риск; делай бэкап образа раздела заранее
btrfs rescue zero-log /dev/sdX    # сбросить лог после краша (бывшая btrfs-zero-log)
```

---

## 🧠 Теория: принципы и устройство

### Copy-on-Write (CoW) — главный принцип

При изменении данных Btrfs **не перезаписывает блок на месте**, а пишет новую версию в свободное место и переключает указатели «снизу вверх» до корня дерева. Следствия:
- **Атомарность**: незавершённая запись не повреждает старые данные — на диске всегда консистентное состояние (поэтому не нужен offline-fsck).
- **Снапшоты почти бесплатны**: снапшот лишь разделяет указатели на те же блоки; место тратится только на расхождения.
- **Минус — фрагментация**: частые random-write поверх одного файла (БД, образы ВМ) плодят раскиданные экстенты → отсюда `chattr +C` и отдельные подтома.

### B-деревья (откуда «B-tree FS»)

Вся структура ФС — это **набор B-деревьев** (дерево корней, дерево экстентов, дерево файлов/подтомов, дерево контрольных сумм, дерево устройств…). B-дерево даёт **логарифмическую** глубину при росте → быстрый поиск/обход даже на больших объёмах. Фиксированных по расположению метаданных очень мало — это и позволяет конвертировать ext «на месте» и свободно двигать данные.

### Экстенты (extents)

Хранение не поблочно, а **экстентами** — непрерывными диапазонами блоков переменной длины. Эффективнее для больших файлов и для CoW. Нюанс: один маленький 4K-фрагмент может удерживать целый исходный экстент (например 128M), мешая освобождению места — отсюда часть случаев «фантомного» расхода и ENOSPC.

### Подтома и снапшоты

**Подтом** — это отдельное дерево файлов (POSIX-namespace) внутри той же ФС, со своей точкой монтирования и своей независимой историей снапшотов. Это **не каталог**: только подтом можно смонтировать в VFS. Корневой подтом (ID 5) неудаляем. **Снапшот** — частный случай подтома, стартующий как точная CoW-копия другого подтома.

### Контрольные суммы и самоисцеление

Btrfs считает **контрольную сумму (по умолчанию CRC32c; опц. xxhash/sha256/blake2)** для **данных и метаданных**. При чтении сумма сверяется; если есть избыточная копия (raid1/raid10/dup) — повреждённый блок **прозрачно чинится из здоровой копии**. `scrub` делает это превентивно по всей ФС. Это защита от «тихого» битрота, которой нет у ext4/xfs.

### Чанки и встроенный RAID

Пространство нарезается на **чанки (block groups)** трёх типов: **Data**, **Metadata**, **System**. У каждого типа — свой профиль размещения (`single`/`dup`/`raid0/1/10/5/6/1c3/1c4`). По умолчанию на одном диске метаданные идут как **dup** (две копии), данные — `single`. Поэтому RAID в Btrfs гибче mdadm: можно зеркалить метаданные и не зеркалить данные, менять профиль на лету балансировкой. `balance` — это и есть перераскладка чанков.

> [!info] Почему `df` обманывает
> Место сначала резервируется крупными **чанками** под Data/Metadata, и лишь потом заполняется. Свободное в одном типе чанков недоступно другому без `balance`. Плюс множители профилей (raid1 = ×2). Поэтому единственный честный показатель — `btrfs filesystem usage`.

---

## 💡 Кому и когда

- **Брать Btrfs**, если нужны: дешёвые снапшоты + откаты (snapper/Timeshift до апдейтов), защита от битрота контрольными суммами, прозрачное сжатие zstd, гибкий RAID1/RAID10 без LVM, send/receive-бэкапы. Идеален для рабочего ноута/десктопа и домашнего файлового сервера на зеркале.
- **Подумать дважды**, если: нужен паритетный RAID5/6 на важных данных (бери RAID1/10 или ZFS/mdadm); тяжёлый random-write по огромным файлам без возможности `+C`; экстремальная нагрузка БД (там xfs/ext4 предсказуемее).
- **Под систему владельца**: на Gentoo — собрать `CONFIG_BTRFS_FS` + `emerge btrfs-progs`, обслуживание через `btrfsmaintenance` (OpenRC-таймеры scrub/balance). На Debian/Ubuntu и (будущем) Arch — ФС готова из коробки, добавить снапшоты (snapper/Timeshift) и systemd-таймеры scrub. На роутере (Entware/RT-AX56U) — **неприменимо**.

## 🔗 Ссылки

- Gentoo Wiki (RU): [wiki.gentoo.org/wiki/Btrfs/ru](https://wiki.gentoo.org/wiki/Btrfs/ru)
- Arch Wiki (RU): [wiki.archlinux.org/title/Btrfs_(Русский)](https://wiki.archlinux.org/title/Btrfs_(%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9))
- Funtoo (архитектура и эксперименты): [funtoo.org/BTRFS_Fun](https://www.funtoo.org/BTRFS_Fun)
- Официальная документация: [btrfs.readthedocs.io](https://btrfs.readthedocs.io/)
- Связанные: [Сборка или обновление ядра (Gentoo)](../Gentoo/Kernel%20-%20%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%D0%BB%D0%B8%20%D0%9E%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%8F%D0%B4%D1%80%D0%B0.md) · [Настройка ядра Linux (Gentoo Wiki)](../Gentoo/Gentoo%20Wiki%20-%20%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D1%8F%D0%B4%D1%80%D0%B0%20Linux.md)

#Btrfs #Linux #Файловая_Система #CoW #Снапшоты #RAID
