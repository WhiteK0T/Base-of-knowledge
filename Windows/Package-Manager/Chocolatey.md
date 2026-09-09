---
создал заметку: 2026-09-09T12:40:00
author: WhiteK0T
tags:
  - Windows
  - Пакетный_Менеджер
  - Chocolatey
  - PowerShell
  - Автоматизация
---

# Chocolatey — шпаргалка

**Chocolatey** (`choco`) — старейший из живых менеджеров пакетов Windows, построен поверх формата NuGet. Пакет — это `.nupkg`, внутри которого лежит **PowerShell-скрипт** `chocolateyInstall.ps1`, выполняющийся с правами администратора.

Обзор и сравнение с другими — [Сравнение менеджеров пакетов Windows](%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Windows%20%E2%80%94%20Chocolatey%2C%20winget%2C%20Scoop.md).

Данные проверены на 09.09.2026 по исходникам `chocolatey/choco` (версия **2.7.4**).

#### Требования

- PowerShell **v3+** (в установщике есть отдельные ветки для версий младше 5);
- .NET Framework **4.8** (требование Chocolatey CLI 2.0+);
- **права администратора обязательны**.

## Установка самого Chocolatey

Из PowerShell **от администратора**:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = `
    [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco -v      # ожидается 2.7.4 или новее
```

Ставится в `C:\ProgramData\chocolatey`.

## Поиск и информация

```powershell
choco search vlc                 # поиск в удалённом репозитории
choco search vlc --exact
choco search vlc --detail        # подробный вывод (--detail = алиас --verbose)
choco search vlc --all-versions
choco info vlc                   # сведения о пакете
choco list                       # УСТАНОВЛЕННЫЕ пакеты
choco list --limit-output        # машиночитаемо: id|version
choco outdated                   # что можно обновить
```

> [!warning] `choco list --local-only` больше не работает
> В Chocolatey 2.x `list` по умолчанию показывает локальные пакеты, а старые флаги **удалены**. Из `ChocolateyListCommand.cs`:
>
> ```csharp
> private readonly string[] _unsupportedArguments = new[]
> {
>     "-l", "-lo", "--lo", "-local", "--local",
>     "-localonly", "--localonly", "-local-only", "--local-only",
>     "-a", "-all", "--all", "-allversions", "--allversions", ...
> };
> ```
>
> При обычном выводе выбрасывается `ApplicationException`. Нюанс: исключение бросается **только при `RegularOutput`**, поэтому `choco list --local-only --limit-output` неожиданно отработает — предупреждение уйдёт только в лог-файл. Полагаться на это не стоит.
>
> Правильно: просто `choco list`. Для поиска в репозитории — `choco search`.

## Установка пакетов

```powershell
choco install vlc -y
choco install vlc --version 3.0.20 -y
choco install git -y --params "/GitAndUnixToolsOnPath"    # параметры пакета
choco install foo -y --install-args "/DIR=D:\Foo"          # аргументы инсталлятору
choco install foo -y --ignore-dependencies
choco install foo -y --force                               # переустановить
choco install packages.config -y                           # массово из файла
```

#### Основные опции install / upgrade

| Опция | Что делает |
| :--- | :--- |
| `-y`, `--yes`, `--confirm` | не спрашивать подтверждений (обязательно для скриптов) |
| `--version` | конкретная версия |
| `--pre`, `--prerelease` | разрешить предрелизные версии |
| `--params`, `--package-parameters` | параметры **пакета** (обрабатывает его скрипт) |
| `--install-args`, `--ia` | аргументы **инсталлятору** |
| `--override`, `-o` | заменить стандартные аргументы инсталлятора, а не дополнить |
| `--params-global` / `--args-global` | применить их же ко всем зависимостям |
| `-i`, `--ignore-dependencies` | не ставить зависимости |
| `-x`, `--force-dependencies` | переустановить и зависимости |
| `-n`, `--skip-scripts` | **не выполнять** PowerShell-скрипты пакета |
| `--allow-downgrade` | разрешить установку версии ниже текущей |
| `--x86`, `--forcex86` | принудительно 32-битная сборка |
| `--not-silent` | показать интерфейс инсталлятора |
| `-s`, `--source` | конкретный источник |

Разница между `--params` и `--install-args` — частая путаница: первое читает **скрипт пакета**, второе передаётся **инсталлятору программы**.

## Обновление и удаление

```powershell
choco upgrade vlc -y
choco upgrade all -y                       # обновить всё
choco upgrade all -y --limit-output
choco upgrade all -y --except="vlc,git"    # кроме перечисленных

choco uninstall vlc -y
choco uninstall vlc -y --remove-dependencies
choco uninstall vlc -y --all-versions
```

## Закрепление версий

```powershell
choco pin list
choco pin add --name vlc                   # не обновлять при upgrade all
choco pin add --name vlc --version 3.0.20
choco pin remove --name vlc
```

## Массовая установка: packages.config

Главный формат для развёртывания рабочих станций.

```xml
<?xml version="1.0" encoding="utf-8"?>
<packages>
  <package id="git" />
  <package id="7zip" version="24.09" />
  <package id="vlc" installArguments="/S" />
  <package id="googlechrome" ignoreDependencies="true" />
</packages>
```

```powershell
choco install packages.config -y
choco export packages.config          # выгрузить текущее состояние в файл
```

`choco export` — быстрый способ снять слепок с настроенной машины.

## Источники

```powershell
choco source list
choco source add -n=internal -s="https://nuget.local/api/v2/" --priority=1
choco source add -n=internal -s="..." -u=user -p=pass      # с авторизацией
choco source disable -n=chocolatey                          # отключить публичный
choco source remove -n=internal
```

Для организаций правильная схема — **только внутренний источник**, публичный отключён. Наполняется через Package Internalizer (платная редакция), который скачивает бинарники внутрь пакетов, убирая зависимость от внешних ссылок.

## Настройки и функции

```powershell
choco config list
choco config set cacheLocation D:\choco-cache
choco config set commandExecutionTimeoutSeconds 14400
choco config set proxy http://proxy.local:3128

choco feature list
choco feature enable -n=useRememberedArgumentsForUpgrades
choco feature enable -n=allowGlobalConfirmation      # больше не писать -y
choco feature disable -n=showDownloadProgress
```

`allowGlobalConfirmation` — первое, что стоит включить, если Chocolatey используется постоянно.

## Глобальные опции

Работают с любой командой:

| Опция | Что делает |
| :--- | :--- |
| `-y`, `--confirm` | подтвердить всё |
| `-r`, `--limit-output` | машиночитаемый вывод (`id\|version`) |
| `-d`, `--debug` · `-v`, `--verbose` · `--trace` | уровни подробности |
| `--noop`, `--what-if` | показать, что было бы сделано, ничего не делая |
| `-f`, `--force` | принудительно |
| `--no-progress` | без прогресс-баров (для CI и логов) |
| `--no-color` | без цвета |
| `--timeout=`, `--execution-timeout=` | таймаут операции |
| `-c`, `--cache-location=` | папка кэша |
| `--log-file=` | писать лог в файл |
| `--proxy=`, `--proxy-user=`, `--proxy-password=` | прокси |
| `--fail-on-stderr` | считать вывод в stderr ошибкой |
| `--use-system-powershell` | системный PowerShell вместо встроенного |

## Создание своих пакетов

```powershell
choco new mypackage                  # скелет пакета
choco pack mypackage.nuspec          # собрать .nupkg
choco push mypackage.1.0.0.nupkg -s="https://nuget.local/" --api-key=KEY
choco apikey add -s="https://nuget.local/" -k=KEY
```

## Безопасность

Модель принципиально отличается от winget и требует внимания.

**Пакет — это произвольный PowerShell-скрипт, выполняемый от администратора.** Модерация публичного репозитория есть, но это код от произвольного участника сообщества.

Статусы модерации устроены контринтуитивно:

- **approved** — модератор посмотрел пакет и не нашёл замечаний;
- **trusted** — пакет **пропускает** ручную модерацию; статус выдаётся доверенному мейнтейнеру, а не конкретному релизу;
- **exempted** — исключён из автоматической проверки, причина на странице пакета.

То есть совет «ставьте только approved или trusted» вводит в заблуждение: **`trusted` означает, что живой человек этот релиз не смотрел**. Автоматика (VirusTotal, 50+ антивирусов) отрабатывает в любом случае.

Полезные приёмы:

```powershell
choco install foo -y --noop            # сначала посмотреть, что будет
choco install foo -y --skip-scripts    # поставить, не выполняя скрипты пакета
```

> [!caution] Публичный репозиторий — supply-chain-поверхность
> Механика та же, что в [атаке на AUR](../../Security/Vulns/Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md): произвольный скрипт от произвольного участника, выполняемый с максимальными правами. Для организаций единственная рабочая защита — внутренний репозиторий.

Что проверить после установки — [System Informer](../System%20Informer%20%E2%80%94%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%BE%D1%85%D0%BE%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%BC%D0%B0%D0%BB%D0%B2%D0%B0%D1%80%D1%8C%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20Process%20Hacker%29.md).

## Каталог

Точное число пакетов публичный API **не отдаёт**: `$count` возвращает `10000` на любой фильтр (включая заведомо пустые), а `$skip` больше 10 000 даёт `HTTP 406`. Защищаемая оценка — **не менее 10 000 пакетов**.

## Ссылки

- [Официальная документация](https://docs.chocolatey.org/)
- [chocolatey/choco](https://github.com/chocolatey/choco) — исходники (Apache 2.0)
- [Модерация пакетов](https://docs.chocolatey.org/en-us/community-repository/moderation/)
- [Сравнение менеджеров пакетов Windows](%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Windows%20%E2%80%94%20Chocolatey%2C%20winget%2C%20Scoop.md) · [winget](winget.md) · [Scoop](Scoop.md)

#Windows #Пакетный_Менеджер #Chocolatey #PowerShell #Автоматизация
