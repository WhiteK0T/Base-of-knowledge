---
создал заметку: 2026-09-09T12:50:00
author: WhiteK0T
tags:
  - Windows
  - Пакетный_Менеджер
  - Scoop
  - PowerShell
---

# Scoop — шпаргалка

**Scoop** — менеджер пакетов Windows для командной строки, работающий **без прав администратора**. Всё ставится в пользовательскую папку `~\scoop\`, программы подключаются через «шимы» в `~\scoop\shims`, которая добавляется в `PATH`.

Обзор и сравнение с другими — [Сравнение менеджеров пакетов Windows](%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Windows%20%E2%80%94%20Chocolatey%2C%20winget%2C%20Scoop.md).

Данные проверены на 09.09.2026 по исходникам `ScoopInstaller/Scoop` (версия **v0.5.3**).

> [!warning] Ядро проекта заморожено
> Последний коммит в `ScoopInstaller/Scoop` — **12.08.2025**, оттуда же последний релиз. На 09.09.2026 это больше года без изменений при **527 открытых issue и PR**. Репозиторий не архивирован.
>
> Работать это не мешает: манифесты в бакетах обновляются **ежедневно**, а сам Scoop — набор PowerShell-скриптов, который свою задачу выполняет. Но багфиксов и новых возможностей ждать не стоит.

#### Требования

- PowerShell **v5+** (`Deny-Install` при более старой версии);
- .NET Framework **4.5+** — нужен для TLS 1.2;
- `C:\Windows\System32\Robocopy.exe` в `PATH`;
- политика выполнения не `Restricted`;
- **права администратора запрещены** — установщик отказывается работать от админа: `Deny-Install 'Running the installer as administrator is disabled by default'`. Обойти можно только явным `-RunAsAdmin`.

## Установка

Из **обычного**, не административного PowerShell:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
irm get.scoop.sh | iex
```

Установка в другую папку:

```powershell
irm get.scoop.sh -outfile 'install.ps1'
.\install.ps1 -ScoopDir 'D:\Scoop' -ScoopGlobalDir 'D:\ScoopGlobal'
```

Проверка:

```powershell
scoop checkup      # диагностика: чего не хватает, что настроено не так
```

`scoop checkup` стоит запускать сразу — он подскажет про отсутствующий 7-Zip, выключенный режим разработчика и незакрытые исключения антивируса.

## Бакеты — источники пакетов

Scoop хранит манифесты в «бакетах» — отдельных git-репозиториях. По умолчанию подключён только `main`.

```powershell
scoop bucket known         # список официальных
scoop bucket list          # подключённые
scoop bucket add extras
scoop bucket add versions
scoop bucket add java
scoop bucket add nerd-fonts
scoop bucket rm games
scoop bucket add mybucket https://github.com/user/repo    # сторонний
```

Официальных бакетов **десять**, суммарно **6 641 манифест**:

| Бакет | Манифестов | Зачем |
| :--- | ---: | :--- |
| `extras` | 2 383 | GUI-программы, всё, что не проходит в `main` |
| `main` | 1 643 | консольные утилиты, подключён сразу |
| `versions` | 604 | старые и preview-версии |
| `games` | 419 | игры и движки |
| `php` | 391 | сборки PHP |
| `nerd-fonts` | 367 | шрифты для терминала |
| `java` | 336 | JDK разных вендоров |
| `nirsoft` | 291 | утилиты NirSoft |
| `nonportable` | 132 | софт, который иначе не ставится |
| `sysinternals` | 75 | Sysinternals Suite |

Три бакета (`games`, `nerd-fonts`, `sysinternals`) живут у сторонних мейнтейнеров, но считаются официальными.

## Поиск и информация

```powershell
scoop search python
scoop info python           # версия, описание, бинарники, зависимости
scoop cat python            # ПОКАЗАТЬ МАНИФЕСТ целиком — до установки
scoop home python           # открыть сайт программы
scoop list                  # установленные
scoop list python           # с фильтром
scoop status                # что устарело и что сломано
scoop which python          # где лежит реальный бинарник за шимом
scoop prefix python         # путь к папке приложения
scoop depends python        # зависимости в порядке установки
```

`scoop cat` — важная привычка: манифест это обычный JSON, в нём видно, откуда качается файл, какой у него хеш и что выполняется после установки.

## Установка

```powershell
scoop install git
scoop install python nodejs go           # несколько сразу
scoop install gh@2.7.0                   # конкретная версия
scoop install https://raw.githubusercontent.com/ScoopInstaller/Main/master/bucket/runat.json
scoop install .\path\to\app.json         # из локального манифеста
```

#### Опции install

| Опция | Что делает |
| :--- | :--- |
| `-g`, `--global` | глобально, для всех пользователей (**требует админа**) |
| `-i`, `--independent` | не ставить зависимости |
| `-k`, `--no-cache` | не использовать кэш загрузок |
| `-s`, `--skip-hash-check` | пропустить проверку хеша — **не использовать** |
| `-u`, `--no-update-scoop` | не обновлять Scoop перед установкой |
| `-a`, `--arch 32bit\|64bit\|arm64` | архитектура, если поддерживается |

## Обновление

```powershell
scoop update                  # обновить сам Scoop и манифесты бакетов
scoop update python           # обновить одну программу
scoop update *                # обновить всё
scoop update --all            # то же самое
scoop update * -k             # без кэша
```

Обратите внимание: `scoop update` **без аргументов** обновляет не программы, а сам Scoop и списки манифестов. Это отличается от `apt update` только формально, а от `choco upgrade all` — принципиально.

## Удаление и уборка

```powershell
scoop uninstall python
scoop uninstall python --purge     # вместе с данными в persist
scoop cleanup python               # удалить старые версии
scoop cleanup * --cache            # всё + устаревший кэш
scoop cache show
scoop cache rm python
scoop cache rm *
```

Scoop — единственный из трёх, который **удаляет начисто**: приложение живёт в своей папке, снос папки убирает всё.

## Параллельные версии — главная фича

```powershell
scoop bucket add versions
scoop install python311 python312
scoop reset python311        # сделать активной 3.11
scoop reset python312        # переключиться на 3.12
```

`scoop reset` переписывает шимы и ярлыки на выбранную версию. Это то, ради чего Scoop чаще всего и ставят рядом с winget.

## Заморозка версий

```powershell
scoop hold python            # не обновлять
scoop unhold python
```

## Экспорт и импорт

```powershell
scoop export > scoopfile.json          # приложения, бакеты и (опционально) конфиг
scoop import scoopfile.json
scoop import https://example.com/scoopfile.json
```

## Шимы

```powershell
scoop shim list
scoop shim info python
scoop shim add mytool 'D:\tools\mytool.exe' --args
scoop shim rm mytool
scoop shim alter python                # выбрать, какой шим главный при конфликте
```

> [!note] Шимы — не симлинки
> Распространённое заблуждение. Scoop **копирует** готовый бинарный `.exe`-шим и кладёт рядом текстовый `.shim` с путём к цели (`lib/core.ps1`):
>
> ```powershell
> Copy-Item (get_shim_path) "$shim.exe" -Force
> Write-Output "path = `"$resolved_path`"" | Out-UTF8File "$shim.shim"
> ```
>
> Практическая причина: символическая ссылка в Windows требует прав администратора либо включённого режима разработчика. Scoop сознательно обходится без них.

## Настройки

Конфиг в `~\.config\scoop\config.json`.

```powershell
scoop config                          # все настройки
scoop config <имя>                    # одну
scoop config <имя> <значение>
scoop config rm <имя>
```

Полезные ключи:

| Ключ | Что делает |
| :--- | :--- |
| `use_external_7zip` | распаковка внешним 7-Zip из `PATH` |
| `use_lessmsi` | lessmsi вместо `msiexec` для MSI |
| `use_sqlite_cache` | SQLite-кэш — заметно ускоряет `scoop search` и `scoop shim` |
| `no_junction` | не использовать алиас `current`, ссылаться на конкретную версию |
| `scoop_repo` / `scoop_branch` | свой форк или ветка `develop` |
| `aria2-enabled` | многопоточная загрузка через aria2 |

`use_sqlite_cache` стоит включить сразу — поиск по 6 641 манифесту без него медленный.

## Безопасность

- Проверяется **SHA256** из манифеста. Отключается флагом `-s`/`--skip-hash-check` — не надо.
- Подписи репозитория **нет** (в отличие от GPG у [APT](../../Linux/Package-Manager/APT.md)).
- **Прав администратора не требуется** — это главное преимущество модели: скомпрометированный манифест не получает системных прав.
- `scoop cat <app>` показывает манифест до установки — пользуйтесь.
- `scoop virustotal <app>` проверяет хеш или URL по базе VirusTotal (нужен API-ключ).

```powershell
scoop config virustotal_api_key <ключ>
scoop virustotal python
scoop virustotal *              # проверить всё установленное
```

## Прочее

```powershell
scoop alias add ls 'scoop list' 'Список программ'
scoop alias list
scoop create https://example.com/tool.zip     # заготовка своего манифеста
scoop download python                          # скачать в кэш, не устанавливая
scoop help update
```

Всего в CLI **28 команд**.

## Ссылки

- [scoop.sh](https://scoop.sh) — сайт и поиск по пакетам
- [ScoopInstaller/Scoop](https://github.com/ScoopInstaller/Scoop) — исходники (Unlicense)
- [buckets.json](https://github.com/ScoopInstaller/Scoop/blob/master/buckets.json) — список официальных бакетов
- [ScoopInstaller/Install](https://github.com/ScoopInstaller/Install) — установщик
- [Сравнение менеджеров пакетов Windows](%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Windows%20%E2%80%94%20Chocolatey%2C%20winget%2C%20Scoop.md) · [winget](winget.md) · [Chocolatey](Chocolatey.md)

#Windows #Пакетный_Менеджер #Scoop #PowerShell
