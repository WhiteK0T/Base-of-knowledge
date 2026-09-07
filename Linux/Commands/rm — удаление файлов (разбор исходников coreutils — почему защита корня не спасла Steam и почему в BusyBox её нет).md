---
создал заметку: 2026-09-07T18:40:00
author: WhiteK0T
tags:
  - rm
  - Linux
  - Coreutils
  - Файловые_системы
  - Безопасность
  - Шпаргалка
Источник:
  - https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html
  - https://github.com/coreutils/coreutils/blob/v9.11/src/rm.c
  - https://github.com/coreutils/coreutils/blob/v9.11/src/remove.c
  - https://github.com/ValveSoftware/steam-for-linux/issues/3671
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/rm.html
---

# 🗑️ rm — удаление файлов: что он делает на самом деле

`rm` — команда из **GNU coreutils**, которая **отвязывает имя от файла** (`unlink`), а вовсе не «стирает данные». Из этого одного факта следует почти всё, что дальше: и почему удалённый файл может годами занимать место, и почему `rm` иногда спрашивает, а иногда молча удаляет, и почему знаменитая защита от `rm -rf /` не спасла тысячи пользователей Steam.

Заметка написана **по исходникам** `coreutils v9.11` (`src/rm.c`, `src/remove.c`) и проверена руками на Gentoo с `rm (GNU coreutils) 9.11`. Всё, что помечено «проверено», реально запускалось.

> [!info] Версии на момент написания (07.09.2026)
> | Где | Версия coreutils |
> | :--- | :--- |
> | **Gentoo** (проверялось здесь) | `9.11-r1` |
> | **Arch** | `9.11-2` |
> | **Debian** | forky/sid `9.10-1` · trixie `9.7-3` · bookworm `9.1-1` |
> | **Entware** (`armv7sf-k3.2`) | `coreutils-rm 9.9-2` |
> | **BusyBox** в прошивке роутера | `1.37.0` — **свой `rm`, не coreutils** |

## 📋 Опции — полный список (из `rm --help` 9.11)

| Опция | Что делает |
| :--- | :--- |
| `-f`, `--force` | игнорировать несуществующие файлы **и отсутствие операндов**, никогда не спрашивать |
| `-i` | спрашивать перед **каждым** удалением |
| `-I` | спросить **один раз**, если файлов больше трёх или задан `-r` |
| `--interactive[=WHEN]` | `never` / `once` (=`-I`) / `always` (=`-i`); без аргумента — `always` |
| `-r`, `-R`, `--recursive` | рекурсивно, вместе с содержимым |
| `-d`, `--dir` | удалить **пустой** каталог |
| `--one-file-system` | при рекурсии пропускать каталоги на **другой** ФС |
| `--preserve-root[=all]` | не удалять `/` (**по умолчанию**); с `all` — отвергать любой аргумент, который является точкой монтирования |
| `--no-preserve-root` | отключить защиту корня |
| `-v`, `--verbose` | печатать, что удаляется |

Никаких `-p`, `--trash`, `--undo` не существует. Корзины у `rm` нет.

## 🧬 Главное: `rm` удаляет **имя**, а не файл

В Unix у файла есть **счётчик жёстких ссылок**. `rm` вызывает `unlink()`, тот уменьшает счётчик на единицу и удаляет запись в каталоге. Сам файл (инод + данные) исчезает, только когда выполнены **оба** условия:

1. счётчик ссылок стал `0`;
2. файл никем не открыт (нет ни одного файлового дескриптора).

```bash
# проверено:
$ touch orig && ln orig hard && stat -c "%h" orig
2
$ rm orig && stat -c "%h" hard
1                      # файл жив, исчезло только имя orig
```

> [!warning] Отсюда классическая загадка «удалил лог на 200 ГБ, а место не вернулось»
> Пока процесс держит дескриптор, данные остаются на диске, хотя имени в ФС уже нет:
> ```bash
> # проверено на 200 МБ:
> $ df -h --output=avail .        #  152G   — до удаления
> $ exec 9<big && rm big
> $ df -h --output=avail .        #  152G   — файл удалён, место НЕ освободилось
> $ ls -l /proc/$$/fd/9
> lr-x------ ... /9 -> /.../big (deleted)
> $ exec 9<&- ; df -h --output=avail .
> #  153G   — освободилось только после закрытия дескриптора
> ```
> Ищут такие файлы через `lsof +L1` или по пометке **`(deleted)`** — подробности в заметке про [lsof](lsof%20%E2%80%94%20%D0%BA%D1%82%D0%BE%20%D1%87%D1%82%D0%BE%20%D0%B8%20%D0%BA%D1%83%D0%B4%D0%B0%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D0%BB%20%28%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5%20%D1%84%D0%B0%D0%B9%D0%BB%D1%8B%2C%20%D1%81%D0%BE%D0%BA%D0%B5%D1%82%D1%8B%2C%20%D0%BF%D0%BE%D1%80%D1%82%D1%8B%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%29.md). Не помогает и `rm` от root — помогает `> /proc/<pid>/fd/N` или перезапуск процесса.

## 🔐 Права: важен каталог, а не файл

Удаление — это **изменение каталога**, а не файла. Поэтому нужно право `w` на **каталог**, а права самого файла роли не играют:

```bash
# проверено:
$ chmod 444 dw/ro   && rm dw/ro      # exit=0 — файл 444 удалён без вопросов
$ chmod 555 dro     && rm -f dro/rw  # rm: cannot remove 'dro/rw': Permission denied
                                     # exit=1 — файл 666, но каталог не записываемый
```

> [!tip] Sticky bit — почему в `/tmp` нельзя удалять чужое
> На каталоге с битом `t` (`drwxrwxrwt`, как `/tmp`) удалять файл может только его владелец, владелец каталога или root — хотя право `w` есть у всех. Это единственное исключение из правила выше.

## 🛡️ Защита от `rm -rf /` — как она устроена и где не работает

Появилась в **coreutils 6.6** (22.11.2006): *«rm now rejects attempts to remove the root directory»*. Проверка сделана **не по строке** `/`, а по паре `st_dev`/`st_ino` реального корня — обойти её символической ссылкой или `//` нельзя.

```bash
# проверено:
$ rm -rf /
rm: it is dangerous to operate recursively on '/'
rm: use --no-preserve-root to override this failsafe
exit=1
```

Но в исходнике видны **три ограничения**, о которых обычно молчат.

### 1. Защита включается только вместе с `-r`

`src/rm.c`, конец `main()`:

```c
  if (x.recursive && preserve_root)
    {
      static struct dev_ino dev_ino_buf;
      x.root_dev_ino = get_root_dev_ino (&dev_ino_buf);
```

Без `-r` `root_dev_ino` вообще не вычисляется. На практике это безобидно (`rm /` и так упрётся в `EISDIR`), но означает, что «`rm` защищает корень» — утверждение только про рекурсивный режим.

### 2. Проверяются **только аргументы командной строки**

`src/remove.c`, функция `rm_fts()`:

```c
      /* Perform checks that can apply only for command-line arguments.  */
      if (ent->fts_level == FTS_ROOTLEVEL)
        {
          ...
          if (ROOT_DEV_INO_CHECK (x->root_dev_ino, ent->fts_statp))
            {
              ROOT_DEV_INO_WARN (ent->fts_path);
```

`FTS_ROOTLEVEL` — верхний уровень обхода, то есть ровно то, что перечислено в командной строке. **Именно здесь ломается вся защита**, см. следующий раздел.

### 3. `--no-preserve-root` нельзя сократить, а `--preserve-root=all` появился поздно

С **coreutils 8.26** (30.11.2016) отключение защиты требует полного написания опции — чтобы случайная `--no-preserve-roo` не проскочила:

```bash
# проверено:
$ rm -rf --no-preserve-roo /
rm: you may not abbreviate the --no-preserve-root option
```

А `--preserve-root=all` — это уже **8.30** (01.07.2018): *«reject any command line argument that is mounted to a separate file system»*. Реализован сравнением устройства аргумента с устройством его `..`:

```c
          if (x->preserve_all_root)
            {
              ...
              if (failed || fts->fts_dev != statbuf.st_dev)
                {
                  error (0, 0, _("skipping %s, since it's on a different device"), ...);
                  error (0, 0, _("and --preserve-root=all is in effect"));
```

Это **не** поведение по умолчанию. Обычный `rm -rf /mnt/backup` (отдельный диск) ничем не защищён.

## 💥 Почему защита не спасла Steam

Самый известный случай — **[ValveSoftware/steam-for-linux#3671](https://github.com/ValveSoftware/steam-for-linux/issues/3671)** от 14.01.2015: *«Moved ~/.local/share/steam. Ran steam. It deleted everything on system owned by user»*. Причину нашли в комментариях в тот же день:

> **Line 468:** `rm -rf "$STEAMROOT/"*`

Если `STEAMROOT` не задан, **`rm` никогда не увидит строку `/`**. Раскрытием занимается shell, и `rm` получает уже готовый список:

```bash
# проверено (безопасно, через echo):
$ STEAMROOT=""
$ echo rm -rf "$STEAMROOT/"*
rm -rf /bin /boot /dev /etc /home /lib /lib64 /lost+found /media /mnt /opt \
       /proc /root /run /sbin /srv /sys /tmp /usr /var
```

Ни один аргумент не равен `/` → проверка `FTS_ROOTLEVEL` не срабатывает ни для одного из них → защита молчит, и содержимое системы удаляется по одному каталогу. `--preserve-root=all` здесь бы помог (все эти пути — либо точки монтирования, либо нет, зависит от разметки), но он не по умолчанию и появился на три года позже инцидента.

> [!danger] Практический вывод
> `rm -rf "$VAR"/*` — **опасная конструкция**, а не защищённая. Единственная надёжная страховка — не дать shell раскрыть пустую переменную:
> ```bash
> set -euo pipefail                          # в начало скрипта
> rm -rf "${STEAMROOT:?переменная не задана}/"*
> ```
> ```bash
> # проверено:
> $ echo rm -rf "${NOTSET:?STEAMROOT не задан — прерываю}/"*
> bash: NOTSET: STEAMROOT не задан — прерываю     # команда не выполнилась
> ```
> `${VAR:?сообщение}` прерывает shell до вызова `rm`. `set -u` работает так же, но `:?` даёт внятный текст и действует даже без `set -u`.

## ❓ `-i` и `-I` — и ловушка с терминалом

Порог `-I` зашит константой прямо в `rm.c`:

```c
  if (prompt_once && (x.recursive || 3 < n_files))
```

То есть **ровно три файла проходят молча**, четвёртый включает запрос:

```bash
# проверено:
$ rm -I a b c   </dev/null   # exit=0, удалены без вопроса
$ rm -I a b c e </dev/null
rm: remove 4 arguments?      # запрос; EOF = «нет»
# exit=0, ничего не удалено
```

> [!caution] Отказ от удаления — это **успех**, а не ошибка
> В обоих случаях код возврата `0`. Скрипт вида `rm -I "$@" && echo "удалено"` напечатает «удалено», даже если пользователь ответил «нет». Проверять надо не `$?`, а факт отсутствия файла.

Вторая ловушка серьёзнее. `rm` без опций спрашивает про файлы, защищённые от записи, — но только если **stdin является терминалом**. В `remove.c`:

```c
  if (!x->ignore_missing_files
      && (x->interactive == RMI_ALWAYS || x->stdin_tty)
      && dirent_type != DT_LNK)
    write_protected = write_protected_non_symlink (fd_cwd, filename, sbuf);
```

```bash
# проверено:
$ touch p1 && chmod 000 p1
$ rm p1 </dev/null        # exit=0, файл удалён МОЛЧА — stdin не терминал

$ touch p2 && chmod 000 p2
$ echo n | rm ---presume-input-tty p2
rm: remove write-protected regular empty file 'p2'?   # ответ n → файл жив
```

Значит **в скриптах, cron и pipeline `rm` никогда не спросит** — привычка «он же переспросит» из интерактивной сессии туда не переносится. (`---presume-input-tty` — недокументированная опция для тестов coreutils; в `rm.c` она объявлена как `{"-presume-input-tty", ...}`, поэтому и пишется с тремя дефисами.)

## ➖ Файлы, начинающиеся с дефиса

`rm` разбирает опции через `getopt`, поэтому файл с именем `-rf` превращается в набор флагов:

```bash
# проверено:
$ touch -- -rf
$ rm -rf          # операндов нет, -f глушит ошибку
                  # exit=0, файл -rf на месте
$ rm -- -rf       # правильно
$ rm ./-rf        # тоже правильно
```

Отдельно обратите внимание на первый случай: **`rm -rf` без операндов молча возвращает 0**. `-f` включает `ignore_missing_files`, и `rm` даже не сообщает, что делать нечего. Это ещё одна причина, по которой ошибки в скриптах проходят незамеченными.

## 📦 Каталоги, ссылки и `-d`

```bash
# проверено:
$ rm -d empty                       # exit=0
$ rm -d full
rm: cannot remove 'full': Directory not empty     # exit=1 — -d только для пустых

$ ln -s target lnk && rm lnk        # удалена ссылка, каталог target цел
$ ln -s target lnk2 && rm -r lnk2/
rm: cannot remove 'lnk2/': Not a directory        # exit=1, target цел
```

Последнее — важное свойство безопасности GNU `rm`: **завершающий слеш на символической ссылке не заставляет его войти в цель**. Обход всегда физический (`FTS_PHYSICAL` в `remove.c`), поэтому `rm -r` не уходит по симлинкам за пределы дерева.

Каталог `.` и `..` отвергается по требованию POSIX:

```bash
# проверено:
$ cd d1 && rm -r .
rm: refusing to remove '.' or '..' directory: skipping '.'
```

Обходной путь, который действительно нужен, — `rm -rf ./* ./.[!.]*` или просто `rm -rf d1` снаружи.

## 🚀 Много файлов: `Argument list too long` и что быстрее

Список аргументов ограничен `ARG_MAX` (на моей машине `2 097 152` байт, `getconf ARG_MAX`):

```bash
# проверено на 200 000 файлов:
$ rm -f *
bash: /usr/bin/rm: Argument list too long
```

Замеры на тех же 200 000 пустых файлов (tmpfs, один прогон):

| Способ | Время |
| :--- | :--- |
| `rm -rf каталог` | **2,05 с** |
| `find каталог -type f -delete` | 2,20 с |
| `find каталог -type f -print0 \| xargs -0 rm -f` | 2,39 с |

> [!note] Расхожее «`find -delete` быстрее `rm`» на практике не подтвердилось
> Когда нужно снести **каталог целиком**, `rm -rf` оказался быстрее всех: он не строит список, а идёт по `fts` с `FTS_CWDFD` (относительные `unlinkat` вместо длинных путей). `find` нужен не ради скорости, а ради двух вещей: обхода `ARG_MAX` и **выборочного** удаления (`-mtime`, `-name`, `-size`). Разница в 15% на 200k файлов практического значения не имеет; на реальном диске всё упрётся в ФС, а не в утилиту.

Полезные варианты:

```bash
find /var/log/app -name '*.log' -mtime +30 -delete      # старше 30 дней
find /path -type f -print0 | xargs -0 -P4 rm -f         # в 4 потока
find /path -mindepth 1 -delete                          # очистить каталог, сам каталог оставить
```

## 💀 «Удалил не то» — что реально можно сделать

> [!danger] Порядок действий — по убыванию шансов
> 1. **Немедленно прекратить запись** на этот раздел. Каждая новая запись может занять освобождённые блоки. Если это системный раздел — размонтировать или перевести в read-only, если корень — выключить машину.
> 2. **Файл ещё открыт процессом?** Тогда он цел: `lsof +L1`, дальше `cp /proc/<pid>/fd/<N> /куда-нибудь`. Самый надёжный сценарий восстановления из всех.
> 3. **Снапшот Btrfs/ZFS** — если настроен, файл лежит в снапшоте нетронутым. См. [Btrfs — CoW-ФС (подтома, снапшоты, RAID)](../Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md).
> 4. **Файл был в git и закоммичен** — `git restore <файл>` или `git checkout HEAD -- <файл>`. Тонкости отличия от [`git rm`](../../VCS/Git/rm.md) — в отдельной заметке.
> 5. **Утилиты восстановления** — по ФС: `extundelete`/`ext4magic` (ext4), `btrfs restore` (Btrfs), `testdisk`/`photorec` (сигнатурный поиск, имена файлов теряются). На ext4 шансы низкие: журналируемая запись затирает указатели на экстенты.

Официальная формулировка GNU честнее большинства статей:

> *Warning: If you use `rm` to remove a file, it is usually **possible** to recover the contents of that file.*

То есть **`rm` не является средством уничтожения данных**. Обратная сторона того же факта: `rm` не годится, когда файл надо именно уничтожить.

> [!caution] `shred` — не универсальная замена
> `shred` перезаписывает файл на месте, и его собственный man честно предупреждает:
> > *CAUTION: shred assumes the file system and hardware overwrite data in place. Although this is common, many platforms operate otherwise.*
>
> «Many platforms» — это ровно ваш случай: **Btrfs, ZFS, любая CoW-ФС, journaled-режимы ext4, все SSD с wear leveling, RAID, снапшоты, бэкапы**. На них `shred` пишет новые блоки, а старые остаются. Для SSD правильный ответ — **шифрование всего раздела с самого начала** (LUKS) и уничтожение ключа, либо ATA Secure Erase. `shred` осмысленен на HDD с непосредственной записью.

## 🧯 Как защититься на практике

| Приём | Команда / настройка | Что даёт | Чего не даёт |
| :--- | :--- | :--- | :--- |
| **`-I` по умолчанию** | `alias rm='rm -I'` в `~/.bashrc` | один вопрос перед `-r` и перед >3 файлов | не действует в скриптах (алиасы неинтерактивны), приучает жать `y` не глядя |
| **`-i` по умолчанию** | `alias rm='rm -i'` | вопрос на каждый файл | быстро надоедает → рефлекс `rm -f`, который хуже исходного |
| **Корзина** | `emerge app-misc/trash-cli`, затем `alias rm=trash-put` | удалённое лежит в `~/.local/share/Trash`, восстановимо `trash-restore` | корзина **на том же разделе**; на другом диске нужна своя `.Trash-<uid>`; меняет семантику `rm` — скрипты, вызывающие `/bin/rm`, не затронуты |
| **Иммутабельный флаг** | `sudo chattr +i важный.conf` | `rm` вернёт `Operation not permitted` **даже от root** | только ext*/Btrfs/XFS; снимается тем же `chattr -i`; неудобно для часто редактируемых файлов |
| **`:?` в скриптах** | `rm -rf "${DIR:?}"/*` | обрывает выполнение на пустой переменной | не спасает от **неправильного** значения переменной |
| **`--one-file-system`** | `rm -rf --one-file-system /mnt/chroot` | не выйдет за пределы ФС аргумента (`FTS_XDEV`) | требует, чтобы опасное было именно на другой ФС |
| **Снапшоты** | Btrfs/ZFS + автоснапшоты по расписанию | **единственная защита, которая работает после факта** | занимают место; снапшот на том же диске не спасёт от отказа диска |

> [!tip] Что из этого стоит включить на Gentoo
> `alias rm='rm -I'` плюс регулярные снапшоты Btrfs. Первое ловит опечатки в интерактивной сессии, второе — всё остальное, включая ошибки в скриптах, где алиас бесполезен. `trash-cli` имеет смысл на десктопе (KDE и так кладёт в корзину через Dolphin), но привыкать к `alias rm=trash-put` рискованно: на чужой машине этого алиаса не будет.

## ✅ Проверка утверждений

| Утверждение | Вердикт | Пояснение |
| :--- | :--- | :--- |
| «`rm -rf /` уничтожит систему» | ⚠️ Не по умолчанию | С coreutils 6.6 отказ с `it is dangerous to operate recursively on '/'`. Обходится явным `--no-preserve-root` |
| «Значит, и `rm -rf /*` защищён» | ❌ **Нет** | Проверка только для аргументов уровня `FTS_ROOTLEVEL`; после раскрытия глоба ни один аргумент не равен `/`. Ровно так пострадали пользователи Steam |
| «Защиту можно случайно отключить опечаткой» | ❌ Нет | С 8.26: `you may not abbreviate the --no-preserve-root option` |
| «`--preserve-root` защищает и отдельные диски» | ❌ Только с `=all` | `--preserve-root=all` появился в 8.30 и не включён по умолчанию |
| «`rm` спрашивает про файлы без права записи» | ⚠️ Только в терминале | Условие `x->stdin_tty` в `remove.c`; в скрипте удалит молча |
| «`rm -I` защищает от массового удаления» | ⚠️ С порога в 4 файла | `3 < n_files` в `rm.c`; три файла уходят без вопроса |
| «Отказ на запрос `-I` вернёт ошибку» | ❌ Нет | `return EXIT_SUCCESS` — код возврата `0` |
| «`rm` стирает данные с диска» | ❌ Нет | Только `unlink()`. GNU: *«it is usually possible to recover the contents»* |
| «`shred` гарантированно уничтожит файл» | ❌ Не на современных ФС | Сам man: *«shred assumes the file system and hardware overwrite data in place»* — неверно для CoW, SSD, RAID, снапшотов |
| «`find -delete` быстрее, чем `rm -rf`» | ❌ У меня наоборот | 200 000 файлов: `rm -rf` 2,05 с против `find -delete` 2,20 с. `find` нужен ради `ARG_MAX` и фильтров, не ради скорости |
| «`rm -d` удалит каталог» | ⚠️ Только пустой | Иначе `Directory not empty` |
| «`rm -r ссылка/` вычистит цель» | ❌ Нет | `Not a directory`; обход физический (`FTS_PHYSICAL`) |
| «`rm -rf` без аргументов сообщит об ошибке» | ❌ Нет | `-f` включает `ignore_missing_files` → тихий `exit 0` |
| «На роутере `rm` такой же» | ❌ **Совсем нет** | BusyBox `rm` знает только `-f -i -R -r -v` и **не имеет защиты корня** — см. ниже |

## 💻 На твоих системах

`rm` входит в **coreutils** — базовый пакет, который есть везде и который нельзя удалить. На Gentoo он помечен в профиле как системный:

```bash
$ grep coreutils /var/db/repos/gentoo/profiles/base/packages
*sys-apps/coreutils          # звёздочка = набор @system, снос сломает систему
```

| Система | Что делать |
| :--- | :--- |
| **Gentoo** | Уже стоит (`sys-apps/coreutils`, у меня `9.11-r1`, часть `@system`). Из полезного рядом: `emerge app-misc/trash-cli` (стабилен на `amd64 x86`) для корзины, `sys-apps/e2fsprogs` даёт `chattr` для `+i`. **Не** ставьте `USE="multicall"` ради экономии — это сборка всех утилит одним бинарником, отладку она усложняет |
| **Debian / Ubuntu** | Уже стоит, пакет `coreutils` помечен `Essential: yes` — `apt remove` его не даст. Корзина: `sudo apt install trash-cli` |
| **Arch** | Уже стоит (`core/coreutils`, `9.11-2`). Корзина: `sudo pacman -S trash-cli` |
| **Entware / RT-AX56U** | ⚠️ **Здесь есть что делать.** По умолчанию `rm` — это апплет **BusyBox 1.37.0** из прошивки, а не coreutils. Ставится полноценный: `opkg install coreutils-rm` (версия `9.9-2`, 29 КБ в пакете / 70 КБ установленный) |

### ⚠️ BusyBox `rm` на роутере — защиты нет вообще

Разбор апплета `coreutils/rm.c` из BusyBox 1.37.0. Весь парсер опций — одна строка:

```c
	opt = getopt32(argv, "^" "fiRrv" "\0" "f-i:i-f");
```

Это **всё**: `-f`, `-i`, `-R`, `-r`, `-v` (последняя часть означает, что `-f` и `-i` взаимоисключающи). А единственная защита в теле функции — вот эта:

```c
			if (DOT_OR_DOTDOT(base)) {
				bb_simple_error_msg("can't remove '.' or '..'");
```

Итого, чего на роутере **нет**:

- **`--preserve-root` и защиты `/` в принципе** — `rm -rf /` на BusyBox начнёт удалять, ничего не спросив. Во flash-памяти большая часть смонтирована read-only, но `/opt` (USB-диск), `/tmp/mnt/*` и `/jffs` записываемы и будут вычищены;
- `-I` — массовое удаление без единого вопроса;
- `-d`, `--one-file-system`, `--interactive=WHEN`;
- **длинных опций вообще** — `rm --help` выдаст ошибку, а `--recursive` будет воспринято как имя файла.

```bash
# на роутере
opkg install coreutils-rm

# проверить, что подменилось (Alternatives: 300:/opt/bin/rm:/opt/libexec/rm-coreutils)
which rm          # ожидается /opt/bin/rm
rm --version      # rm (GNU coreutils) 9.9
```

> [!note] Подмена действует только на твою сессию
> `/opt/bin` стоит в `PATH` перед `/bin`, поэтому набранный вручную `rm` пойдёт в coreutils. Но **скрипты самой прошивки** вызывают `/bin/rm` по абсолютному пути и продолжат получать BusyBox. Заменять апплеты в прошивке не надо — сломается обновление. Про пакеты и `Alternatives` — в заметке про [OPKG](../Package-Manager/OPKG.md).

Полезная мелочь: если нужен только один-два GNU-инструмента, ставьте пофайлово (`coreutils-rm`, `coreutils-shred`, `findutils`), а не пакет `coreutils` целиком — на 256 МБ флеша это заметно. `findutils 4.10.0-1` даёт настоящие `find` и `xargs` с `-print0`/`-0`, чего в BusyBox тоже нет.

## 🔗 Ссылки

- Документация: [GNU coreutils — `rm` invocation](https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html) · [POSIX `rm`](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/rm.html) · локально `info '(coreutils) rm invocation'`
- Исходники: [`src/rm.c`](https://github.com/coreutils/coreutils/blob/v9.11/src/rm.c) · [`src/remove.c`](https://github.com/coreutils/coreutils/blob/v9.11/src/remove.c) · [`NEWS`](https://github.com/coreutils/coreutils/blob/v9.11/NEWS)
- Инцидент: [ValveSoftware/steam-for-linux#3671](https://github.com/ValveSoftware/steam-for-linux/issues/3671)
- Связанные: [lsof — кто держит удалённый файл](lsof%20%E2%80%94%20%D0%BA%D1%82%D0%BE%20%D1%87%D1%82%D0%BE%20%D0%B8%20%D0%BA%D1%83%D0%B4%D0%B0%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D0%BB%20%28%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B5%20%D1%84%D0%B0%D0%B9%D0%BB%D1%8B%2C%20%D1%81%D0%BE%D0%BA%D0%B5%D1%82%D1%8B%2C%20%D0%BF%D0%BE%D1%80%D1%82%D1%8B%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%29.md) · [strace — посмотреть, что `rm` реально вызывает](strace%20%E2%80%94%20%D1%82%D1%80%D0%B0%D1%81%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D1%85%20%D0%B2%D1%8B%D0%B7%D0%BE%D0%B2%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%B4%D0%B8%D0%B0%D0%B3%D0%BD%D0%BE%D1%81%D1%82%D0%B8%D0%BA%D0%B8%20%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B9%20%D0%B8%20100%25%20CPU%20%28%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%2C%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B%2C%20%D1%87%D0%B5%D0%BC%20%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C%20%D0%BD%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B5%29.md) · [sed](sed.md) · [git rm — совсем другая команда](../../VCS/Git/rm.md) · [Btrfs — снапшоты как страховка](../Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md) · [OPKG](../Package-Manager/OPKG.md)

#rm #Linux #Coreutils #Файловые_системы #Безопасность #Шпаргалка
