---
создал заметку: 2026-09-09T12:30:00
author: WhiteK0T
tags:
  - Windows
  - Пакетный_Менеджер
  - winget
  - Автоматизация
---

# winget — шпаргалка

**Windows Package Manager** (`winget`) — официальный менеджер пакетов Microsoft. Предустановлен в Windows 11 и в Windows 10 начиная с 1809, обновляется через Microsoft Store вместе с «App Installer».

Обзор и сравнение с другими — [Сравнение менеджеров пакетов Windows](%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Windows%20%E2%80%94%20Chocolatey%2C%20winget%2C%20Scoop.md).

Данные проверены на 09.09.2026 по исходникам `microsoft/winget-cli` (v1.29.290) и документации Microsoft Learn.

#### Где работает

- **Windows 10 build 17763 (1809) и новее**, Windows 11 — штатно;
- **Windows Server 2025** — штатно, поставляется через Windows Update;
- **Windows Server 2019 / 2022** — только экспериментально, распаковкой `.msixbundle` вручную (официально не поддерживается);
- **Windows Server Core — не работает**, из-за жёсткой зависимости от MSIX и `IsWow64Process2`.

#### Проверка и первый запуск

```powershell
winget --version                 # ожидается v1.29.x
winget --info                    # пути, источники, политики, логи
winget source update             # обновить индекс источников
```

## Поиск и информация

```powershell
winget search firefox                    # поиск по имени, id, moniker, тегам
winget search --id Mozilla.Firefox -e    # точное совпадение по id
winget show --id Mozilla.Firefox         # описание, версия, лицензия, ссылки
winget show --id Mozilla.Firefox --versions   # все доступные версии
winget list                              # ВСЕ установленные программы, не только winget
winget list --upgrade-available          # что можно обновить
winget list --id Mozilla.Firefox         # проверить конкретную
```

> [!note] `winget list` показывает больше, чем ставил winget
> В отличие от `choco list` и `scoop list`, эта команда читает системный список «Установка и удаление программ». Поэтому в выводе будут и программы, поставленные вручную, и пакеты других менеджеров. Колонка `Source` показывает `winget`, если пакет из каталога, и пусто — если поставлен иначе.

## Установка

```powershell
winget install --id Mozilla.Firefox -e            # -e = точное совпадение id
winget install --id Git.Git -e --version 2.45.0   # конкретная версия
winget install --id 7zip.7zip -e --silent         # без окон инсталлятора
winget install --id VideoLAN.VLC -e --scope machine    # для всех пользователей
winget install --id Foo.Bar -e --location "D:\Apps\Bar"
winget install --id Foo.Bar -e --override "/S /D=D:\Bar"   # свои аргументы инсталлятору
```

Всегда указывайте `-e` (`--exact`) вместе с `--id`. Без него `winget install firefox` может выбрать не тот пакет, если совпадений несколько.

#### Основные опции установки

| Опция | Что делает |
| :--- | :--- |
| `-e`, `--exact` | точное совпадение, без нечёткого поиска |
| `-v`, `--version` | конкретная версия (по умолчанию последняя) |
| `--silent` | тихая установка |
| `--interactive` | наоборот, показать интерфейс инсталлятора |
| `--scope user\|machine` | для текущего пользователя или для всей машины |
| `--location <путь>` | куда ставить, если инсталлятор поддерживает |
| `--override <строка>` | заменить аргументы инсталлятора целиком |
| `--custom <строка>` | добавить аргументы к стандартным |
| `--architecture x64\|x86\|arm64` | выбрать архитектуру |
| `--installer-type` | выбрать тип инсталлятора, если их несколько |
| `--skip-dependencies` | не ставить зависимости и компоненты Windows |
| `--accept-package-agreements` | принять лицензии пакетов |
| `--accept-source-agreements` | принять соглашения источников |
| `--disable-interactivity` | запретить любые интерактивные запросы |
| `--allow-reboot` | разрешить перезагрузку, если требуется |
| `--ignore-security-hash` | **отключить проверку SHA256** — не использовать |

## Обновление

```powershell
winget upgrade                          # список доступных обновлений
winget upgrade --id Mozilla.Firefox -e  # обновить один пакет
winget upgrade --all --silent           # обновить всё тихо
winget upgrade --all --include-unknown  # включая те, у кого версия не определяется
winget upgrade --all --include-pinned   # включая закреплённые не-блокирующим пином
```

`--include-unknown` нужен чаще, чем кажется: у части программ winget не может прочитать текущую версию из реестра и по умолчанию их пропускает.

## Удаление

```powershell
winget uninstall --id Mozilla.Firefox -e
winget uninstall --id Foo.Bar -e --purge      # portable: снести и данные
winget uninstall --id Foo.Bar -e --preserve   # portable: оставить файлы
```

Удалять можно и то, что winget не ставил, — по имени из `winget list`.

## Закрепление версий (pin)

```powershell
winget pin list
winget pin add --id Mozilla.Firefox -e             # не обновлять
winget pin add --id Git.Git -e --version 2.45.*    # обновлять только внутри 2.45
winget pin remove --id Mozilla.Firefox -e
winget pin reset --force                            # снять все пины
```

## Экспорт и импорт набора программ

Самое полезное для переустановки системы.

```powershell
winget export -o packages.json --source winget      # выгрузить список
winget export -o all.json --include-versions        # с точными версиями

winget import -i packages.json `
  --accept-source-agreements --accept-package-agreements
```

> [!warning] Оба флага согласия обязательны
> Часто пишут только `--accept-source-agreements`. Этого мало: лицензии **самих пакетов** принимаются отдельным `--accept-package-agreements`, иначе импорт остановится на интерактивном запросе и автоматизация встанет.

Опции импорта: `--ignore-unavailable` (пропускать пакеты, которых больше нет в каталоге), `--ignore-versions` (ставить последнюю версию вместо зафиксированной).

## Декларативная настройка машины — winget configure

Аналог Ansible/DSC внутри winget: YAML описывает желаемое состояние, `winget` его применяет.

```powershell
winget configure -f state.dsc.yaml       # применить
winget configure test -f state.dsc.yaml  # проверить, соответствует ли система
winget configure show -f state.dsc.yaml  # показать, что будет сделано
winget configure validate -f state.dsc.yaml
winget configure export -f out.yaml      # выгрузить текущее состояние
winget configure list                    # история применённых конфигураций
```

Рядом лежит `winget dsc` — ресурсы DSC v3. Это прямой ответ на главный корпоративный аргумент в пользу Chocolatey.

## Остальные команды

```powershell
winget download --id Git.Git -e          # скачать инсталлятор, НЕ ставя
winget repair --id Foo.Bar -e            # починить установленный пакет
winget resume -g <id>                    # продолжить прерванную операцию
winget hash installer.exe                # SHA256 для манифеста
winget validate manifest.yaml            # проверить манифест перед PR
winget font list                         # установленные шрифты
winget error 0x8a150011                  # расшифровать код ошибки
winget mcp                               # сведения об интеграции Model Context Protocol
```

Всего в CLI **32 команды**.

## Источники (sources)

```powershell
winget source list
winget source update
winget source add -n mysrc -a https://repo.local/api --type Microsoft.Rest
winget source remove -n mysrc
winget source reset --force              # вернуть источники по умолчанию
winget source export
```

Штатно подключены два: `winget` (каталог сообщества, **14 756** пакетов) и `msstore` (Microsoft Store).

## Настройки

```powershell
winget settings              # открыть settings.json в редакторе
winget settings export       # показать текущие настройки
winget features              # статус экспериментальных возможностей

# административные настройки (нужен админ)
winget settings set LocalManifestFiles true
winget settings reset LocalManifestFiles
```

Файл лежит в `%LOCALAPPDATA%\Packages\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe\LocalState\settings.json`.

## Безопасность

Модель проще, чем у Chocolatey, и в этом её сила:

- **Манифест — декларативный YAML**, исполняемого кода в пакете нет. Из README `winget-pkgs`: *«Script-based installers are not currently supported»*. Допустимы только MSIX, MSI, APPX, MSIXBundle, APPXBundle, `.exe` и файлы шрифтов.
- Проверяется **SHA256** инсталлятора из манифеста. Не подпись издателя — именно хеш. Отключается флагом `--ignore-security-hash`.
- Подписи репозитория **нет** (в отличие от GPG у [APT](../../Linux/Package-Manager/APT.md)).
- `--ignore-local-archive-malware-scan` отключает антивирусную проверку архивных пакетов из локального манифеста.

Что проверить после установки незнакомого пакета — [System Informer](../System%20Informer%20%E2%80%94%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%BE%D1%85%D0%BE%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%BC%D0%B0%D0%BB%D0%B2%D0%B0%D1%80%D1%8C%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20Process%20Hacker%29.md).

## Рецепты

**Настройка новой машины одной командой:**

```powershell
winget import -i packages.json --accept-source-agreements --accept-package-agreements --ignore-unavailable
```

**Обновление всего по расписанию (задача в планировщике):**

```powershell
winget upgrade --all --silent --include-unknown --disable-interactivity --accept-package-agreements
```

**Посмотреть, что поставлено не через winget:**

```powershell
winget list | Where-Object { $_ -notmatch 'winget$' }
```

## Ссылки

- [Документация Microsoft Learn](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
- [microsoft/winget-cli](https://github.com/microsoft/winget-cli) — клиент (MIT)
- [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs) — манифесты каталога
- [Сравнение менеджеров пакетов Windows](%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%20Windows%20%E2%80%94%20Chocolatey%2C%20winget%2C%20Scoop.md) · [Chocolatey](Chocolatey.md) · [Scoop](Scoop.md)

#Windows #Пакетный_Менеджер #winget #Автоматизация
