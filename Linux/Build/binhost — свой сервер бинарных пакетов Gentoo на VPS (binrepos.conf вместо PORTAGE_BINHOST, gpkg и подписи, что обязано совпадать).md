---
создал заметку: 2026-09-07T01:15:00
author: WhiteK0T
tags:
  - Gentoo
  - Portage
  - Сборка
  - binhost
  - VPS
  - GPG
  - Оптимизация
Источник:
  - https://wiki.gentoo.org/wiki/Binary_package_guide
  - https://wiki.gentoo.org/wiki/Binary_package_guide/Settingup
  - https://wiki.gentoo.org/wiki/Gentoo_Binary_Host_Quickstart
  - https://github.com/gentoo/portage/blob/master/man/portage.5
  - https://github.com/gentoo/portage/blob/master/man/make.conf.5
---

# binhost — свой сервер бинарных пакетов Gentoo

> [!info] Задача
> Локальная машина на Gentoo, компилировать на ней долго. Есть VPS с **Ryzen 9 7950X3D (8 ядер, 16 ГБ)**. Идея: VPS собирает пакеты целиком и раздаёт готовые, локальная машина их просто ставит — как Debian, только со своими USE-флагами.
>
> В отличие от [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) сюда уезжает **вся** работа: `./configure`, компиляция, линковка, Rust, Go, ядро. Локальная машина не компилирует ничего.
>
> Две вещи, которые надо усвоить до старта: `PORTAGE_BINHOST` **объявлен устаревшим** в пользу `/etc/portage/binrepos.conf`, а весь риск проекта — в том, что **Portage не проверяет совместимость** сервера и клиента. Это целиком на вас.

---

## 1. Как это работает

```
   VPS (сборщик)                                 Локальная машина (клиент)
   ┌──────────────────────────┐                  ┌────────────────────────┐
   │ chroot с ВАШИМ            │                 │ emerge -avuDN @world   │
   │ /etc/portage              │                 │   ├─ читает Packages   │
   │   emerge @world           │   HTTPS         │   ├─ качает .gpkg.tar  │
   │   FEATURES="buildpkg"     │ ───────────────→│   ├─ проверяет подпись │
   │        ↓                  │                 │   └─ распаковывает     │
   │ /var/cache/binpkgs/       │                 │                        │
   │   Packages  (индекс)      │                 │ компиляции НЕТ         │
   │   cat/pkg-ver.gpkg.tar    │                 └────────────────────────┘
   │        ↓ nginx            │
   └──────────────────────────┘
```

Ключевой файл — **`Packages`** в корне `PKGDIR`. Это текстовый индекс с метаданными всех пакетов: версии, USE-флаги, зависимости, хеши. Клиент сначала скачивает его, а потом решает, что тянуть.

---

## 2. Что обязано совпадать — читать до начала

Из руководства Gentoo, дословно про ответственность:

> *«Portage can not validate if these requirements match»*

То есть если вы соберёте пакеты не с теми флагами, Portage их спокойно поставит, а сломается всё потом и непонятно где.

| Параметр | Насколько строго | Как сверить |
| :--- | :--- | :--- |
| **Архитектура и `CHOST`** | обязано совпадать точно | `portageq envvar CHOST` → `x86_64-pc-linux-gnu` |
| **Профиль** | обязан совпадать | `eselect profile show` |
| **`CFLAGS` / `CXXFLAGS`** | должны быть совместимы, то есть код обязан исполняться на клиенте | см. ниже |
| **`USE`** | глобальные и по пакетам | `portageq envvar USE`, `/etc/portage/package.use` |
| **`CPU_FLAGS_X86`** | обязано совпадать | `cpuid2cpuflags` на **клиенте** |
| **`VIDEO_CARDS`, `INPUT_DEVICES`, `L10N`** | должны совпадать | иначе получите пакеты не с тем набором драйверов |
| **`ACCEPT_KEYWORDS`** | желательно | иначе версии разойдутся |
| **Срез дерева Portage** | желательно | иначе клиент захочет версии, которых на сервере нет |

### Про `CFLAGS` и `-march`

Та же ловушка, что и с distcc, только страшнее: там ошибку ловит компилятор, здесь — процессор в рантайме.

VPS на Zen 4 умеет AVX-512. Если собрать пакеты с `-march=native` на VPS, а поставить на машину постарше — получите `SIGILL` в произвольный момент, возможно через месяц, в редко вызываемой ветке кода.

```bash
# на КЛИЕНТЕ выясняем, что он вообще умеет
emerge -av app-misc/resolve-march-native app-portage/cpuid2cpuflags
resolve-march-native
cpuid2cpuflags-x86        # выдаст строку CPU_FLAGS_X86="..."
```

Дальше в `make.conf` (одинаковый на обеих сторонах):

```bash
COMMON_FLAGS="-O2 -pipe -march=x86-64-v3 -mtune=generic"
CFLAGS="${COMMON_FLAGS}"
CXXFLAGS="${COMMON_FLAGS}"
CPU_FLAGS_X86="aes avx avx2 f16c fma3 mmx mmxext pclmul popcnt rdrand sha sse sse2 sse3 sse4_1 sse4_2 ssse3"
```

`CPU_FLAGS_X86` берите **с клиента**, а не с VPS: это USE-флаги, они определяют, какие ассемблерные ветки будут вкомпилированы в ffmpeg, openssl и прочие.

> [!tip] Простое правило
> Всё, что описывает **железо клиента**, берётся с клиента. VPS только выполняет работу, его собственный процессор в конфигурации не должен фигурировать нигде.

---

## 3. Форматы и умолчания

Проверено по `cnf/make.globals` в исходниках Portage (версии в дереве: стабильная `3.0.81.3`, в тестировании до `3.0.82.2`):

| Переменная | Значение по умолчанию | Комментарий |
| :--- | :--- | :--- |
| `PKGDIR` | `/var/cache/binpkgs` | где лежат пакеты |
| **`BINPKG_FORMAT`** | **`gpkg`** | современный формат, файлы `.gpkg.tar`; подписи работают **только** с ним |
| `BINPKG_COMPRESS` | **`zstd`** | ещё поддерживаются bzip2, gzip, lz4, lzip, lzop, xz |
| `BINPKG_COMPRESS_FLAGS` | пусто | например `-9` для сильнее/медленнее |
| `BINPKG_GPG_VERIFY_GPG_HOME` | `/etc/portage/gnupg` | связка ключей для проверки |
| `BINPKG_GPG_SIGNING_DIGEST` | `SHA512` | |

Старый формат `xpak` (файлы `.tbz2`) остаётся для совместимости, но подписывать его нельзя — брать не надо.

### FEATURES, включённые по умолчанию

Из того же `make.globals`, относящееся к бинарным пакетам:

```
binpkg-docompress  binpkg-dostrip  binpkg-logs  binpkg-multi-instance
buildpkg-live  compress-index  pkgdir-index-trusted
```

Обратите внимание на два:

- **`binpkg-multi-instance`** включён по умолчанию с portage-3.0.15. Хранит **несколько сборок одного пакета** с разными USE, раскладывая их по подкаталогам с BUILD_ID. Удобно, но `PKGDIR` пухнет — чистить придётся (раздел 8).
- **`pkgdir-index-trusted`** включён по умолчанию с portage-3.0.52. Portage доверяет файлу `Packages` и не сканирует каталог. Если вы руками удалили или положили пакет — индекс станет врать, пока не сделаете `emaint binhost --fix`.

---

## 4. `binrepos.conf`, а не `PORTAGE_BINHOST`

Дословно из `make.conf(5)`:

> *«The PORTAGE_BINHOST variable is deprecated in favor of the binrepos.conf configuration file (see portage(5)).»*

И из `portage(5)`:

> *«binrepos.conf — Specifies remote binary package repository configuration information. This is intended to be used as a replacement for the make.conf(5) PORTAGE_BINHOST variable.»*

Старая переменная пока работает, но новых конфигов на ней писать не стоит: в `binrepos.conf` есть приоритеты, отдельные каталоги под каждый источник и попакетная проверка подписи.

### Синтаксис

Файл `/etc/portage/binrepos.conf` или каталог `/etc/portage/binrepos.conf/*.conf`. Пример из комментариев самого Portage:

```ini
[example-binhost]
# repos with higher priorities are preferred when packages with equal
# versions are found in multiple repos
priority = 9999
# packages are fetched from here
sync-uri = https://example.com/binhost

# Introduced in portage-3.0.74 for per-repo verification choices
verify-signature = true

# Defaults to /var/cache/binhost/$NAME with >=portage-3.0.77
#location = /var/cache/binhost/example-binhost
```

Атрибуты секции `[DEFAULT]`, которые пригодятся:

| Атрибут | Смысл |
| :--- | :--- |
| `frozen = yes` | не обновлять индекс, брать закешированный. *«This should only be set temporarily in order to guarantee consistent and reproducible dependency calculations»* |
| `fetchcommand` / `resumecommand` | свои команды скачивания вместо тех, что в `make.conf` |

Дефолтный `binrepos.conf` из пакета portage состоит ровно из двух строк:

```ini
[DEFAULT]
verify-signature = true
```

То есть проверка подписи **включена изначально** — и это правильно, но означает, что свой неподписанный binhost из коробки не заработает. Либо подписывайте (раздел 7), либо явно ставьте `verify-signature = false` для своей секции.

---

## 5. Официальный binhost Gentoo — и почему он вас не спасёт

С 2023 года Gentoo публикует собственные бинарные пакеты. Для amd64 обновляются ежедневно:

```ini
# /etc/portage/binrepos.conf/gentoo.conf
[gentoo]
priority = 9999
sync-uri = https://distfiles.gentoo.org/releases/amd64/binpackages/23.0/x86-64/
verify-signature = true
location = /var/cache/binhost/gentoo
```

Есть вариант, собранный под `x86-64-v3`, если процессор его тянет. Для arm64 тоже ежедневно, для остальных архитектур — раз в неделю и только основные пакеты.

**Но:** официальные пакеты собраны с **дефолтными USE профиля**. Любой ваш `USE="-systemd wayland pipewire ..."` означает, что подойдёт лишь малая часть. Официальный binhost хорош как подложка: поставить его с низким приоритетом, свой — с высоким, и тогда своё собирается только то, что реально отличается по USE.

Проверку подписи для официального включает `getuto`:

```bash
FEATURES="binpkg-request-signature"   # в make.conf
getuto                                # разложит доверенные ключи Gentoo
# если ругается на существующий каталог:
mv /etc/portage/gnupg /etc/portage/gnupg.bak && getuto
```

---

## 6. Сервер: собираем на VPS

### Почему chroot, а не «просто поставить Gentoo»

VPS должен собирать пакеты **для вашей машины**, а не для себя. Значит нужна среда с вашим профилем, вашим `make.conf` и вашим `/etc/portage`. Самое надёжное — chroot, куда эти файлы просто копируются с клиента.

```bash
# --- на VPS ---
mkdir -p /srv/gentoo-build && cd /srv/gentoo-build
# взять stage3 под ваш профиль с зеркала Gentoo
wget https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-openrc/stage3-amd64-openrc-*.tar.xz
tar xpf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner

mount --types proc /proc proc
mount --rbind /sys sys && mount --make-rslave sys
mount --rbind /dev dev && mount --make-rslave dev
cp --dereference /etc/resolv.conf etc/
```

Теперь перенос конфигурации **с клиента**:

```bash
# --- на клиенте ---
rsync -av /etc/portage/ vps:/srv/gentoo-build/etc/portage/
# и список установленного, чтобы собрать ровно то же
emerge -pq --emptytree @world > /tmp/worldlist
scp /var/lib/portage/world vps:/srv/gentoo-build/var/lib/portage/world
```

Внутри chroot дописать в `make.conf` сборку пакетов:

```bash
FEATURES="${FEATURES} buildpkg"
# альтернатива: не ставить пакеты в chroot вообще, только собирать
# emerge -B ...
MAKEOPTS="-j16 -l8"          # 8 ядер / 16 потоков VPS — здесь можно не стесняться
```

### Сама сборка

```bash
chroot /srv/gentoo-build /bin/bash
source /etc/profile
emerge-webrsync                     # или emerge --sync
emerge -avuDN --with-bdeps=y @world # первый прогон — долгий
```

Дальше по расписанию:

```bash
emerge --sync && emerge -uDN --buildpkg --usepkg @world
```

> [!tip] Затравка через `quickpkg`
> Если система клиента уже собрана, не обязательно начинать с нуля. На **клиенте**:
> ```bash
> emerge -av app-portage/gentoolkit
> quickpkg --include-config=y --include-unmodified-config=y "*/*"
> ```
> Это упакует **уже установленные** пакеты в `PKGDIR` как есть. Полученное можно залить на VPS и начать не с пустого места. Осторожно с `--include-config`: в конфиги могут попасть пароли и ключи.

### Сколько это займёт места

Полная `@world` десктопной системы — обычно 5–15 ГБ бинарных пакетов, с `binpkg-multi-instance` растёт быстрее. На 16 ГБ ОЗУ VPS собираться будет всё, кроме, возможно, LTO-линковки chromium и rust — для них может понадобиться swap.

---

## 7. Раздача по HTTP

Отдавать надо **весь `PKGDIR` целиком**, включая файл `Packages`. Никакой специальной серверной части нет — это просто статика.

Пример nginx из руководства Gentoo:

```nginx
server {
    listen 0.0.0.0;
    server_name _;
    root /path/to/binhost/var/cache/binpkgs;
    autoindex on;
}
```

Для реального применения — с TLS и ограничением доступа:

```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name binhost.example.com;

    ssl_certificate     /etc/letsencrypt/live/binhost.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/binhost.example.com/privkey.pem;

    root /srv/gentoo-build/var/cache/binpkgs;
    autoindex on;

    # binhost — не публичный ресурс
    auth_basic           "binhost";
    auth_basic_user_file /etc/nginx/binhost.htpasswd;

    # .gpkg.tar уже сжаты zstd, повторно не жать
    gzip off;
}
```

Подробности по конфигу — [заметка про nginx](../../Network/WebServers/nginx/nginx%20%E2%80%94%20%D0%B2%D0%B5%D0%B1-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B8%20reverse-proxy%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%2C%20server-location%2C%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%2C%20%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20TLS%2C%20%D0%BA%D1%8D%D1%88%20%28%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%29.md), по сертификату — [Let's Encrypt](../../Network/WebServers/Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md).

Поддерживаются также FTP, FTPS, SSH/SFTP и NFS. Вариант без веб-сервера вообще — раздавать по SSH тем же ключом, что и для управления VPS:

```ini
[myhost]
sync-uri = ssh://build@vps.example.com/srv/gentoo-build/var/cache/binpkgs
priority = 9999
verify-signature = false
```

---

## 8. Подписи GPG

Раз пакеты едут через интернет и ставятся от root — подписывать стоит. Работает только с `gpkg`.

### На сервере (VPS)

```bash
# ключ отдельный, не тот, которым подписываете коммиты
gpg --homedir /root/.gnupg --full-generate-key   # ed25519, без срока или на год
gpg --homedir /root/.gnupg --list-secret-keys --keyid-format=long
```

В `make.conf` chroot'а:

```bash
FEATURES="${FEATURES} buildpkg binpkg-signing gpg-keepalive"
BINPKG_FORMAT="gpkg"
BINPKG_GPG_SIGNING_GPG_HOME="/root/.gnupg"
BINPKG_GPG_SIGNING_KEY="0xВАШОТПЕЧАТОК!"
```

Восклицательный знак в конце отпечатка обязателен — он означает «именно этот подключ, не выбирать автоматически».

`gpg-keepalive` нужен, чтобы агент не забыл парольную фразу посреди многочасового `emerge` и подписывание не отвалилось на середине.

### На клиенте

```bash
gpg --homedir /etc/portage/gnupg --import binhost-pubkey.asc
gpg --homedir /etc/portage/gnupg --edit-key 0xВАШОТПЕЧАТОК
  # trust → 5 (ultimate) → quit
gpg --homedir /etc/portage/gnupg --check-trustdb
```

И в `make.conf`:

```bash
FEATURES="${FEATURES} getbinpkg binpkg-request-signature"
```

`binpkg-request-signature` — по формулировке руководства: *«assumes that all packages should be signed and rejects any unsigned package»*. Жёстко, но правильно.

> [!warning] Если подписывать не хочется
> Тогда **обязательно** TLS плюс `auth_basic`, а в секции binrepos.conf — `verify-signature = false`. Без подписи и без TLS вы ставите от root бинарники, полученные по открытому каналу.

---

## 9. Клиент: настройка и запуск

```ini
# /etc/portage/binrepos.conf/myvps.conf
[myvps]
priority = 9999
sync-uri = https://binhost.example.com/
verify-signature = true
location = /var/cache/binhost/myvps
```

Если стоит `auth_basic`, логин с паролем задаётся через `fetchcommand` или, проще, в самом URL — но тогда пароль окажется в конфиге, лучше `~/.netrc` и `fetchcommand` с `--netrc`.

В `make.conf`:

```bash
FEATURES="${FEATURES} getbinpkg binpkg-request-signature"
```

Флаги `emerge`, которые понадобятся:

| Флаг | Что делает |
| :--- | :--- |
| `-k`, `--usepkg` | взять бинарник, если есть; иначе собрать из исходников |
| `-K`, `--usepkgonly` | **только** бинарники, при отсутствии — ошибка |
| `-g`, `--getbinpkg` | качать с удалённого хоста, иначе собрать |
| `-G`, `--getbinpkgonly` | только удалённые бинарники |
| `--rebuilt-binaries` | переставить пакеты, пересобранные на сервере после установки |
| `--usepkg-exclude ATOM` | не брать бинарник для конкретного пакета |

Обычное обновление:

```bash
emerge -avuDNg @world          # с бинарниками, откат на исходники разрешён
emerge -avuDNG @world          # строго только бинарники — покажет, чего не хватает
```

Полезная привычка: сначала прогнать с `-G`, посмотреть, что сервер не собрал, добрать это на сервере, и только потом ставить.

---

## 10. Обслуживание

**Чистка старых пакетов.** С `binpkg-multi-instance` каталог растёт постоянно:

```bash
emerge -av app-portage/gentoolkit
eclean-pkg --deep                 # удалить всё, что не соответствует дереву
eclean-pkg --deep --time-limit=30d
```

**Починка индекса** после ручных манипуляций с файлами:

```bash
emaint binhost --fix
```

Из документации: *«As of portage-3.0.52, Portage defaults to FEATURES=pkgdir-index-trusted for performance, which requires an accurate Packages index»* — то есть без этой команды клиент будет видеть несуществующие пакеты.

**Синхронизация конфигов.** Самая частая причина расхождений — поправили `package.use` на клиенте и забыли на сервере. Стоит завести один источник правды: держать `/etc/portage` в git и тянуть на обе стороны.

```bash
# на клиенте
cd /etc/portage && git add -A && git commit -m "use: ..." && git push
# на VPS в chroot
cd /etc/portage && git pull && emerge -uDN --buildpkg @world
```

---

## 11. Как убедиться, что работает

```bash
# что клиент видит на сервере
emerge -pv --getbinpkg app-editors/nano
# в выводе должно быть [binary] вместо [ebuild]

# индекс скачался?
ls -la /var/cache/binhost/myvps/Packages

# сколько пакетов на сервере
grep -c '^CPV:' /srv/gentoo-build/var/cache/binpkgs/Packages

# проверить подпись конкретного пакета руками
gpg --homedir /etc/portage/gnupg --verify \
    /var/cache/binhost/myvps/app-editors/nano-*.gpkg.tar
```

Признак `[binary]` в выводе `emerge -pv` — главный индикатор. Если там `[ebuild]`, значит либо пакета нет на сервере, либо не совпали USE, и Portage молча решил собирать из исходников.

Посмотреть, **почему** не подошёл бинарник:

```bash
emerge -pv --getbinpkg --verbose-conflicts app-editors/nano
emerge --info | diff - <(ssh vps 'chroot /srv/gentoo-build emerge --info')
```

Второй командой сравниваются полные окружения двух систем — самый быстрый способ найти разъехавшийся флаг.

---

## 12. Подводные камни

| Проблема | Суть |
| :--- | :--- |
| **Portage ничего не валидирует** | Несовпадение CFLAGS не будет замечено ни при сборке, ни при установке. Только `SIGILL` в рантайме |
| **USE разъезжаются незаметно** | Изменили `package.use` на клиенте — бинарники молча перестают подходить, всё собирается локально, а вы удивляетесь, почему binhost «не работает» |
| **`verify-signature = true` по умолчанию** | Свой неподписанный binhost из коробки не заработает — и сообщение об этом не очень внятное |
| **`pkgdir-index-trusted`** | Руками удалили файл — клиент будет пытаться его скачать, пока не сделаете `emaint binhost --fix` |
| **Место на VPS** | `binpkg-multi-instance` копит сборки; без `eclean-pkg` диск кончится |
| **Разные срезы дерева** | Клиент синхронизировался, сервер нет — клиент хочет версии, которых на сервере нет, и собирает сам |
| **Конфиги в `quickpkg`** | `--include-config=y` может утащить в пакет пароли из `/etc` |
| **Пакеты с `RESTRICT="bindist"`** | Некоторые нельзя распространять в бинарном виде по лицензии. Для личного binhost юридически это ваше дело, но флаг существует не просто так |

---

## 13. binhost против distcc

| Критерий | binhost | [distcc](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) |
| :--- | :--- | :--- |
| `./configure` | на сервере | локально |
| Компиляция | на сервере | на сервере |
| Линковка | на сервере | **локально** |
| Rust, Go, ядро | ускоряет | не трогает |
| Нагрузка на клиент | почти нулевая | заметная |
| Совпадение версий gcc | не нужно | обязательно |
| Сеть | один раз на пакет | на каждый файл |
| Задержка канала | не критична | критична |
| Работает офлайн | да, если пакет скачан | нет |
| Требует одинаковых USE и профиля | **да, жёстко** | нет |
| Сложность настройки | выше | ниже |
| Что ломается при ошибке | несовпадение ABI → `SIGILL` | ошибка компиляции сразу |

**Вывод для описанной задачи:** binhost выигрывает почти по всем пунктам, кроме одного — он требует дисциплины в синхронизации конфигов. Зато взамен вы получаете локальную машину, которая вообще не компилирует.

Их можно совмещать: binhost как основной путь, distcc — на те пакеты, которых на сервере не оказалось (`emerge -g` с откатом на исходники, а исходники уже через distcc).

---

## 14. По системам

**Gentoo (клиент и сборщик)** — всё выше.

**Debian / Ubuntu.** Прямого аналога не нужно: там и так бинарные пакеты. Аналог «своего binhost» — локальный репозиторий:

```bash
apt install reprepro          # или aptly
# reprepro -b /srv/repo includedeb stable ./mypackage.deb
# клиент: deb [signed-by=/etc/apt/keyrings/my.gpg] https://repo.example.com stable main
```

Если VPS нужен как сборочная машина для своих `.deb` — это `sbuild` или `pbuilder` в chroot, схема ровно та же: chroot с целевым релизом, сборка, подпись, раздача статикой.

**Arch (планируется с июня 2026).** Свой репозиторий делается штатно:

```bash
repo-add /srv/repo/x86_64/myrepo.db.tar.zst /srv/repo/x86_64/*.pkg.tar.zst
# /etc/pacman.conf на клиенте:
# [myrepo]
# SigLevel = Required DatabaseOptional
# Server = https://repo.example.com/$arch
```

Сборка AUR-пакетов на VPS через `makechrootpkg` — самый близкий по духу аналог binhost, и он же снимает боль с долгой сборкой тяжёлых AUR-пакетов.

**Entware / ASUS RT-AX56U.** Идея переносится один в один: `opkg` умеет свои фиды. Собираете `.ipk` кросс-компиляцией под armv7 на VPS, кладёте рядом `Packages.gz`, и на роутере:

```sh
echo "src/gz myfeed https://binhost.example.com/entware/armv7sf-k3.2" >> /opt/etc/opkg.conf
opkg update
```

Формат индекса у opkg тот же по духу, что у Portage, — текстовый `Packages`. Подробнее про сам менеджер — [OPKG](../Package-Manager/OPKG.md).

---

## 15. Кому стоит

| Ситуация | Вердикт |
| :--- | :--- |
| Одна машина на Gentoo + один мощный сервер | **Да, это основной сценарий.** Ради него всё и делается |
| Несколько машин с одинаковым профилем | **Да, тем более** — сборка один раз, установка всюду |
| Ноутбук, который жалко греть | **Да.** Компиляции на нём не будет вообще |
| USE-флаги меняются каждую неделю | Осторожно: придётся пересобирать и держать конфиги в синхроне |
| Разные машины с разными профилями | Придётся поднимать по chroot на каждый профиль |
| Стоковый десктоп с дефолтными USE | Возможно, хватит **официального binhost** Gentoo, свой не нужен |
| Нужен результат «прямо сейчас, один пакет» | Проще собрать на VPS и `scp` бинарь |

**Порядок внедрения, который я бы советовал:** сначала подключить официальный binhost Gentoo и посмотреть, сколько пакетов он закроет. Потом поднять свой chroot на VPS для остального. `binpkg-request-signature` и подписи включать сразу — потом переделывать больнее.

---

## Связанные заметки

- [distcc — распределённая сборка на VPS](distcc%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Gentoo%20%D0%BD%D0%B0%20%D0%BC%D0%BE%D1%89%D0%BD%D1%8B%D0%B9%20VPS%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20SSH%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20pump%20%D0%B2%D1%8B%D1%80%D0%B5%D0%B7%D0%B0%D0%BD%2C%20%D1%81%D0%B5%D1%80%D1%8B%D0%B9%20IP%20%D0%BD%D0%B5%20%D0%BC%D0%B5%D1%88%D0%B0%D0%B5%D1%82%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D1%82%D1%83%D0%BD%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BD%D0%B5%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%29.md) — альтернативный подход, сравнение в разделе 13
- [nginx — подробный разбор](../../Network/WebServers/nginx/nginx%20%E2%80%94%20%D0%B2%D0%B5%D0%B1-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B8%20reverse-proxy%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%2C%20server-location%2C%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%2C%20%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20TLS%2C%20%D0%BA%D1%8D%D1%88%20%28%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%29.md) — раздача PKGDIR
- [Let's Encrypt](../../Network/WebServers/Let%27s%20Encrypt%20%E2%80%94%20%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%20TLS-%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%20%D0%B8%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%20nginx%20%D0%B8%20Apache%20%28certbot%2C%20acme.sh%2C%20HTTP-01-DNS-01%2C%20wildcard%2C%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BF%D1%80%D0%BE%D0%B4%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md) — сертификат для binhost
- [SSH-Ключи](../../Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md) — если раздавать по `ssh://` вместо HTTPS
- [Kernel — сборка или обновление ядра](../Gentoo/Kernel%20-%20%D0%A1%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%D0%BB%D0%B8%20%D0%9E%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%8F%D0%B4%D1%80%D0%B0.md) — ядро binhost как раз закрывает, в отличие от distcc
- [OPKG](../Package-Manager/OPKG.md) — та же идея своего фида для роутера

## Ссылки

- Руководство по бинарным пакетам: https://wiki.gentoo.org/wiki/Binary_package_guide
- Поднятие своего binhost: https://wiki.gentoo.org/wiki/Binary_package_guide/Settingup
- Официальный binhost Gentoo: https://wiki.gentoo.org/wiki/Gentoo_Binary_Host_Quickstart
- `portage(5)`, секция binrepos.conf: https://github.com/gentoo/portage/blob/master/man/portage.5
- `make.conf(5)`: https://github.com/gentoo/portage/blob/master/man/make.conf.5
- Умолчания Portage (`make.globals`): https://github.com/gentoo/portage/blob/master/cnf/make.globals
- Дефолтный `binrepos.conf`: https://github.com/gentoo/portage/blob/master/cnf/binrepos.conf
- Официальные пакеты amd64: https://distfiles.gentoo.org/releases/amd64/binpackages/23.0/x86-64/

#Gentoo #Portage #binhost #Сборка #Компиляция #GPG #VPS #nginx #Оптимизация
