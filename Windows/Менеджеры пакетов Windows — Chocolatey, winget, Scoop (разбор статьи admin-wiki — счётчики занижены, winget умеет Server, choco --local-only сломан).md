---
создал заметку: 2026-09-08T17:20:00
author: WhiteK0T
tags:
  - Windows
  - Пакетный_Менеджер
  - Chocolatey
  - winget
  - Scoop
  - PowerShell
  - Автоматизация
Источник:
  - https://admin-wiki.ru/article/menedzheryi-paketov-v-windows-2026-sravnenie-chocolatey-winget-i-scoop-dlya-avtomatizatsii/
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/
  - https://github.com/microsoft/winget-pkgs
  - https://github.com/chocolatey/choco
  - https://github.com/ScoopInstaller/Scoop
---

# 📦 Менеджеры пакетов Windows: Chocolatey, winget, Scoop — разбор статьи admin-wiki

Разбор статьи [«Менеджеры пакетов в Windows 2026: сравнение Chocolatey, winget и Scoop для автоматизации»](https://admin-wiki.ru/article/menedzheryi-paketov-v-windows-2026-sravnenie-chocolatey-winget-i-scoop-dlya-avtomatizatsii/). Структура у неё разумная, но данные сильно устарели, а часть команд просто **не выполнится** на тех версиях, которые ставятся по её же инструкциям.

Всё ниже проверено 08.09.2026 по первоисточникам: официальный индекс winget (`source.msix` от Microsoft), исходники `chocolatey/choco` и `ScoopInstaller/Scoop`, GitHub API, документация Microsoft Learn.

> [!warning] Главный вывод
> Статья датирована июлем 2026, но опирается на данные 2024 года. Три числа из её сравнительной таблицы занижены — одно почти втрое, одно втрое с лишним. Одно из ключевых утверждений («winget не поддерживает Windows Server») противоречит официальной документации Microsoft. И две команды из раздела автоматизации падают с ошибкой.

## ✅ Проверка утверждений

| Утверждение статьи | Вердикт | Что на самом деле |
| :--- | :--- | :--- |
| Репозиторий winget — «свыше 5000 уникальных приложений» | ❌ Занижено в **~3 раза** | **14 752** уникальных идентификатора в официальном индексе Microsoft |
| Scoop — «около 2000+» пакетов, 4 бакета | ❌ Занижено в **~3 раза** | **6 640** манифестов в **10** официальных бакетах |
| Chocolatey — «более 9000 пакетов» | ⚠️ Правдоподобно, но как нижняя граница | OData-API упирается в потолок 10 000, точное число получить нельзя |
| «winget не поддерживает Windows Server» | ❌ **Неверно** | Microsoft: winget работает на «Windows 10, Windows 11, **and Windows Server 2025**» и поставляется там через Windows Update |
| `choco list --local-only` | ❌ **Команда падает** | В Chocolatey 2.x аргумент удалён, выбрасывается `ApplicationException` |
| «Ожидается интеграция с WinGet Configuration» | ❌ Уже давно есть | Команда `winget configure` документирована, рядом `download`, `repair`, `pin`, `dscv3` |
| «Версия winget 1.8 добавила поддержку ARM64» | ❌ Это новость 2024 года | 1.8 — июнь–июль 2024. Актуальный стабильный — **v1.29.290** (24.08.2026) |
| «Ожидаемый вывод `choco -v`: 2.4.0 или новее» | ⚠️ Формально верно, фактически устарело | Актуальная — **2.7.4** (19.08.2026) |
| «Chocolatey for Business версии 6.0» | ❌ Такого продукта нет | Версионируются компоненты: Licensed Extension 8.1.0, Agent 4.1.0, Central Management 0.17.0, GUI 3.2.0 |
| «winget проверяет цифровую подпись, без неё установка блокируется» | ❌ **Неверно** | Проверяется **SHA256-хеш** из манифеста (`--ignore-security-hash`). Требования подписи нет |
| «Scoop требует .NET Framework 4.8» | ❌ Неверно | Установщик требует **4.5+** (нужен TLS 1.2) |
| «Chocolatey требует PowerShell 5.1+» | ⚠️ Завышено | Минимум — **PowerShell v3**; в установщике есть отдельные ветки для версий младше 5 |
| «В `~/scoop/shims` создаются символические ссылки» | ❌ Неверно | Копируется бинарный `.exe`-шим плюс текстовый `.shim` с путём к цели |
| «Устанавливайте пакеты только со статусом approved или **trusted**» | ⚠️ Смысл перевёрнут | `trusted` означает, что пакет **пропускает** ручную модерацию, а не проходит более строгую |
| «IIS, SQL Server доступны только в Chocolatey» | ❌ Неверно | В winget есть `Microsoft.SQLServer.2025.Developer`, `.2022.Developer` и ещё 462 пакета `Microsoft.*`. IIS — роль Windows, ставится через DISM, а не пакетным менеджером |
| Chocolatey — PowerShell-скрипты поверх NuGet, требует админа | ✅ Верно | |
| Scoop ставится без прав администратора в пользовательскую папку | ✅ Верно | Более того, запуск установщика от админа **запрещён** по умолчанию |
| `scoop update *`, `winget export/import`, `packages.config` | ✅ Верно | Синтаксис подтверждён по исходникам и документации |
| Статусы модерации approved / trusted / exempted, скан VirusTotal | ✅ Верно | VirusTotal прогоняет через 50+ антивирусов |

## 🔢 Откуда взяты цифры

### winget — 14 752 пакета, а не 5000

Microsoft публикует индекс источника как MSIX-архив с базой SQLite внутри. Это первоисточник, тот самый файл, который скачивает клиент:

```bash
curl -sL "https://cdn.winget.microsoft.com/cache/source.msix" -o src.msix
unzip -o src.msix           # внутри Public/index.db
```

```python
import sqlite3
c = sqlite3.connect('Public/index.db')
c.execute("SELECT COUNT(*) FROM ids").fetchone()               # 14752
c.execute("SELECT COUNT(DISTINCT id) FROM manifest").fetchone()# 14752
c.execute("SELECT COUNT(*) FROM manifest").fetchone()          # 169630
c.execute("SELECT COUNT(*) FROM versions").fetchone()          # 63773
```

| Показатель | Значение |
| :--- | :--- |
| Уникальных идентификаторов пакетов | **14 752** |
| Записей «пакет + версия» | 169 630 |
| Различных строк версий | 63 773 |
| Пакетов `Microsoft.*` | 462 |
| Дата сборки индекса | 08.09.2026 |

### Scoop — 6 640 манифестов в 10 бакетах, а не «2000+ в четырёх»

Список официальных бакетов лежит в самом репозитории Scoop — [`buckets.json`](https://github.com/ScoopInstaller/Scoop/blob/master/buckets.json). Их **десять**, а не четыре:

| Бакет | Репозиторий | Манифестов |
| :--- | :--- | ---: |
| `extras` | ScoopInstaller/Extras | 2 383 |
| `main` | ScoopInstaller/Main | 1 642 |
| `versions` | ScoopInstaller/Versions | 604 |
| `games` | **Calinou/scoop-games** | 419 |
| `php` | ScoopInstaller/PHP | 391 |
| `nerd-fonts` | matthewjberger/scoop-nerd-fonts | 367 |
| `java` | ScoopInstaller/Java | 336 |
| `nirsoft` | ScoopInstaller/Nirsoft | 291 |
| `nonportable` | ScoopInstaller/Nonportable | 132 |
| `sysinternals` | niheaven/scoop-sysinternals | 75 |
| **Итого** | | **6 640** |

Одни только `main` + `extras` дают 4 025 — уже вдвое больше заявленного в статье. Обратите внимание: `games` живёт не в организации ScoopInstaller, а у стороннего мейнтейнера `Calinou` — при этом бакет считается официальным.

Статья не упоминает `java` (важен, если нужны параллельные JDK), `php` и `nerd-fonts` (шрифты для терминала — как раз то, ради чего Scoop часто и ставят).

### Chocolatey — точное число получить не удалось

Честно: **не смог**. OData-эндпоинт репозитория отдаёт `10000` на любой запрос `$count`, включая заведомо узкие фильтры, а постраничный обход упирается в тот же потолок:

```bash
curl -s "https://community.chocolatey.org/api/v2/Packages/\$count?\$filter=IsLatestVersion"
# 10000  — и ровно столько же для startswith(Id,'a'), startswith(Id,'z') и т.д.
```

Так что «более 9000» из статьи — корректная **нижняя** граница, но, судя по потолку API, реальное число не меньше 10 000. Заявленное первенство Chocolatey по размеру репозитория при этом **сомнительно**: 14 752 у winget против ~10 000 у Chocolatey.

## 💥 Команды из статьи, которые не работают

### `choco list --local-only` выбрасывает исключение

В Chocolatey 2.x поведение `choco list` изменилось: теперь он по умолчанию показывает локальные пакеты, а старые флаги удалены. Из `ChocolateyListCommand.cs`:

```csharp
[Obsolete("Remove unsupported argument in V3!")]
private readonly string[] _unsupportedArguments = new[]
{
    "-l", "-lo", "--lo", "-local", "--local",
    "-localonly", "--localonly", "-local-only", "--local-only",
    "-a", "-all", "--all", "-allversions", "--allversions",
    "-all-versions", "--all-versions",
    "-order-by-popularity", "--order-by-popularity"
};
```

```csharp
if (isUnsupportedArgument || isUnsupportedRegistryProgramsArgument)
{
    if (configuration.RegularOutput)
    {
        throw new ApplicationException("Invalid argument {0}. This argument has been removed from the list command and cannot be used.".FormatWith(argument));
    }
    ...
    this.Log().Warn(ChocolateyLoggers.LogFileOnly, "Ignoring the argument {0}. ...");
}
```

> [!tip] Забавный нюанс: одна команда статьи падает, вторая работает случайно
> Бросок исключения происходит **только при `RegularOutput`**. Флаг `--limit-output` его выключает. Поэтому:
> - `choco list --local-only` → **падает с ошибкой**;
> - `choco list --local-only --limit-output > installed.csv` → **работает**, потому что предупреждение уходит только в лог-файл.
>
> То есть команда аудита из статьи выполнится, а команда прямо перед ней — нет. Автор явно не запускал ни ту, ни другую.

**Как правильно в Chocolatey 2.x:**

```powershell
choco list                       # локально установленные (поведение по умолчанию)
choco list --limit-output        # машиночитаемо: id|version
choco search vlc                 # поиск в удалённом репозитории
choco search vlc --detail        # подробности (--detail = алиас для --verbose)
choco outdated                   # что можно обновить
```

### Ещё раз про `--detail`

Флаг существует и объявлен как `.Add("detail|detailed", "Detailed - Alias for verbose.")`. Но статья обещает, что он «покажет статус модерации», — это просто подробный вывод, отдельного поля со статусом там нет. Статус смотрят на странице пакета на сайте.

## 🔐 Модель безопасности — статья описывает её неправильно

Это самая проблемная часть исходного текста, потому что из неверного описания следуют неверные решения.

### winget: хеш, а не подпись

Статья: *«Winget проверяет цифровую подпись каждого загружаемого инсталлятора. Если подпись отсутствует или недействительна, установка блокируется»*.

В документации `winget install` нет ни одной опции, связанной с подписью. Есть ровно две про безопасность:

| Опция | Описание из документации |
| :--- | :--- |
| `--ignore-security-hash` | *«Ignore the installer **hash** check failure. Not recommended.»* |
| `--ignore-local-archive-malware-scan` | *«Ignore the malware scan performed as part of installing an **archive type package from local manifest**.»* |

То есть механизм тот же самый, что у Scoop: **SHA256 из манифеста сверяется с загруженным файлом**. Антивирусное сканирование при установке применяется лишь к архивным пакетам из локального манифеста.

Настоящее преимущество winget в другом, и статья его не называет. Из README репозитория `winget-pkgs`:

> *At this time installers must be MSIX, MSI, APPX, MSIXBundle, APPXBundle, or .exe application installers. Font files ... are also supported. **Script-based installers are not currently supported.***

**Манифест winget — декларативный YAML без исполняемого кода.** Пакет Chocolatey — это PowerShell-скрипт, то есть произвольный код, выполняемый с правами администратора. Вот это и есть принципиальная разница в модели угроз, а не мифическая проверка подписи.

### Chocolatey: `trusted` — это меньше проверок, а не больше

Статья советует: *«Устанавливайте пакеты только со статусом approved или trusted»*, подавая `trusted` как «проверен и активно поддерживается». По документации Chocolatey всё наоборот:

- **approved** — модератор посмотрел пакет и не нашёл замечаний;
- **trusted** — пакет **пропускает человеческую модерацию** и идёт сразу дальше; статус выставляется модератором вручную для доверенных мейнтейнеров;
- **exempted** — исключён из автоматической проверки, причина указывается на странице пакета.

Автоматика (VirusTotal, 50+ антивирусов) отрабатывает в любом случае. Но `trusted` означает, что **живой человек этот конкретный релиз не смотрел**. Для оценки риска это ровно противоположный сигнал тому, что предлагает статья.

> [!caution] Публичный репозиторий сообщества — это supply-chain-поверхность
> Механика та же, что в [атаке на AUR](../Security/Vulns/Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md): пакет с произвольным скриптом от произвольного участника. Совет статьи про внутренний репозиторий для организаций — правильный, и он единственный по-настоящему рабочий.

### Scoop: изоляция реальнее, чем кажется, но шимы — не симлинки

Хеш SHA256 в манифесте — верно. Отсутствие прав администратора — верно, причём сильнее, чем написано: установщик **отказывается** работать от админа:

```powershell
# lib install.ps1, проверка перед установкой
Deny-Install 'Running the installer as administrator is disabled by default, ...'
```

А вот про шимы неточность. `scoop` не создаёт символических ссылок — он копирует готовый бинарный шим и кладёт рядом текстовый файл с целью (`lib/core.ps1`):

```powershell
Copy-Item (get_shim_path) "$shim.exe" -Force
Write-Output "path = `"$resolved_path`"" | Out-UTF8File "$shim.shim"
```

Практическая разница есть: симлинк требует либо прав администратора, либо включённого режима разработчика в Windows — именно поэтому Scoop их и не использует.

## ⚙️ Требования: что проверяют сами установщики

Взято не из документации, а из кода установочных скриптов.

| | Chocolatey | Scoop |
| :--- | :--- | :--- |
| PowerShell | **v3+** (в скрипте есть ветки для `Major -lt 5`) | **v5+** (`if (($PSVersionTable.PSVersion.Major) -lt 5) { Deny-Install ... }`) |
| .NET Framework | **4.8** (требование Chocolatey CLI 2.0+) | **4.5+** — нужен TLS 1.2: *«Scoop requires .NET Framework 4.5+ to work»* |
| Права администратора | требуются | **запрещены** по умолчанию, нужен явный `-RunAsAdmin` |
| Прочее | — | `C:\Windows\System32\Robocopy.exe` должен быть в `PATH`; политика выполнения не `Restricted` |

Статья приписывает Scoop требование .NET 4.8 и Chocolatey — PowerShell 5.1. Оба утверждения строже реальных: на старой машине по её тексту вы решите, что установка невозможна, хотя она пройдёт.

## 🛠️ Исправленная шпаргалка

```powershell
# ── Chocolatey (админский PowerShell) ──────────────────────────
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = `
    [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco -v                       # ожидается 2.7.4 или новее

choco install vlc -y
choco list                     # БЕЗ --local-only
choco list --limit-output      # для скриптов и CSV
choco outdated
choco upgrade all -y --limit-output
choco config set cacheLocation D:\choco-cache

# массовая установка
choco install packages.config -y

# ── winget (встроен; Win10 1809+, Win11, Windows Server 2025) ──
winget --version               # ожидается v1.29.x
winget search firefox
winget install --id Mozilla.Firefox -e

winget export -o config.json --source winget
winget import -i config.json --accept-source-agreements --accept-package-agreements
winget upgrade --all --silent

winget configure -f state.dsc.yaml   # декларативное состояние — УЖЕ существует
winget download --id Git.Git         # скачать инсталлятор, не ставя
winget pin add --id Foo.Bar          # закрепить версию

# ── Scoop (обычный, НЕ админский PowerShell) ──────────────────
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
irm get.scoop.sh | iex

scoop bucket add extras
scoop bucket add versions
scoop bucket add java           # статья про этот бакет молчит
scoop bucket add nerd-fonts

scoop update *                  # или scoop update --all
scoop export > scoopfile.json
scoop import scoopfile.json
scoop cat <пакет>               # посмотреть манифест ДО установки
scoop reset python311           # переключить активную версию
```

> [!note] Про `--accept-package-agreements`
> Статья приводит `winget import` только с `--accept-source-agreements`. Этого мало для полностью автоматического сценария: лицензии **самих пакетов** принимаются отдельным флагом `--accept-package-agreements`, иначе импорт остановится на интерактивном запросе.

## 🎯 Что статья говорит верно

Не всё плохо, и основной вывод у неё правильный:

- **Архитектурное разделение описано корректно:** Chocolatey — системная установка с правами админа, winget — клиент к репозиторию манифестов, Scoop — изоляция в пользовательской папке.
- **Три менеджера не конфликтуют** и осмысленно сочетаются: разные каталоги, разные реестры установленного.
- **Сценарии подобраны разумно:** winget для быстрой настройки рабочей станции, Chocolatey для корпоративной среды с внутренним репозиторием, Scoop для dev-окружения с параллельными версиями языков.
- **Совет про внутренний репозиторий** в Chocolatey for Business — единственная по-настоящему работающая защита от рисков публичного репозитория (реализуется через Package Internalizer, а не через мифическую «версию 6.0»).
- **Синтаксис автоматизации** (`packages.config`, `winget export/import`, `scoopfile.json`, `scoop update *`) приведён правильно.

## 🐧 Для сравнения — как это выглядит в Linux

Аналогия из статьи («Chocolatey эмулирует классический подход Linux-пакетных менеджеров») верна лишь отчасти. Ключевое отличие Windows-менеджеров: они **скачивают и запускают чужие инсталляторы**, а не распаковывают собственные архивы с зависимостями.

| | [APT](../Linux/Package-Manager/APT.md) / dpkg | [OPKG](../Linux/Package-Manager/OPKG.md) | Chocolatey | winget | Scoop |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Что в пакете | сам софт | сам софт | **скрипт**, качающий инсталлятор | **манифест** со ссылкой и хешем | манифест со ссылкой и хешем |
| Зависимости | полноценные | полноценные | есть | ограниченно | минимально |
| Подпись репозитория | GPG | подписи Entware | нет (хеш + VirusTotal) | нет (хеш) | нет (хеш) |
| Удаление начисто | да | да | зависит от инсталлятора | зависит от инсталлятора | да (папка) |

Сводная таблица команд по разным менеджерам — в заметке [Сравнение команд менеджеров пакетов](../Linux/Package-Manager/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2.md).

## 💡 Практический вывод

Комбинировать — правильный совет, но приоритеты стоит расставить иначе, чем в статье:

1. **winget как основной.** Встроен, репозиторий крупнейший (14 752 против ~10 000), манифесты декларативные — без произвольного кода в пакете. Умеет `configure` для декларативного состояния машины.
2. **Scoop для dev-окружения.** Без админа, параллельные версии, `scoop cat` для инспекции манифеста перед установкой. Не забыть бакеты `java`, `php`, `nerd-fonts`.
3. **Chocolatey — когда нужен именно он:** пакет есть только там, либо нужны внутренний репозиторий и групповые политики. Помнить, что пакет = PowerShell-скрипт с правами админа, а статус `trusted` означает отсутствие ручной проверки.

## 🔗 Ссылки

- Разбираемая статья: [admin-wiki.ru](https://admin-wiki.ru/article/menedzheryi-paketov-v-windows-2026-sravnenie-chocolatey-winget-i-scoop-dlya-avtomatizatsii/)
- winget: [документация Microsoft Learn](https://learn.microsoft.com/en-us/windows/package-manager/winget/) · [winget-cli](https://github.com/microsoft/winget-cli) · [winget-pkgs](https://github.com/microsoft/winget-pkgs)
- Chocolatey: [chocolatey/choco](https://github.com/chocolatey/choco) · [документация](https://docs.chocolatey.org/) · [модерация](https://docs.chocolatey.org/en-us/community-repository/moderation/)
- Scoop: [ScoopInstaller/Scoop](https://github.com/ScoopInstaller/Scoop) · [buckets.json](https://github.com/ScoopInstaller/Scoop/blob/master/buckets.json) · [установщик](https://github.com/ScoopInstaller/Install)
- Связанные: [Сравнение команд менеджеров пакетов](../Linux/Package-Manager/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2.md) · [APT](../Linux/Package-Manager/APT.md) · [OPKG](../Linux/Package-Manager/OPKG.md) · [Atomic Arch — supply-chain-атака на AUR](../Security/Vulns/Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md) · [System Informer — что реально запустилось после установки](System%20Informer%20%E2%80%94%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%BE%D1%85%D0%BE%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%BC%D0%B0%D0%BB%D0%B2%D0%B0%D1%80%D1%8C%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20Process%20Hacker%29.md)

#Windows #Пакетный_Менеджер #Chocolatey #winget #Scoop #PowerShell #Автоматизация
