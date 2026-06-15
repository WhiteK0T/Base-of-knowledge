# 🧠 Base of knowledge

![Obsidian](https://img.shields.io/badge/Obsidian-483699?logo=obsidian&logoColor=white)
![Made with Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f?logo=markdown&logoColor=white)
![Язык: Русский](https://img.shields.io/badge/Язык-Русский-0088CC)
![Заметок](https://img.shields.io/badge/Заметок-95-success)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green)](LICENSE)
![Last commit](https://img.shields.io/github/last-commit/WhiteK0T/Base-of-knowledge)
![Repo size](https://img.shields.io/github/repo-size/WhiteK0T/Base-of-knowledge)

> Личный «второй мозг»: конспекты, шпаргалки и руководства, которые проще держать в одном месте и переиспользовать.

## ✨ О репозитории

- **Что это.** Личная база знаний в виде заметок [Obsidian](https://obsidian.md/) — конспекты по Linux, программированию, здоровью и другим темам.
- **Не софт-проект.** Здесь нет сборки, тестов и зависимостей — только Markdown-файлы. Obsidian читает каталог напрямую, а на GitHub репозиторий служит каталогом-витриной.
- **Язык.** Контент преимущественно на русском; команды и код — как есть.
- **Навигация.** Полный каталог заметок — в разделе «Каталог заметок» ниже; по длинной заметке удобно прыгать через встроенное оглавление (☰ на GitHub / Outline в Obsidian).

## 📂 Структура

Заметки сгруппированы по доменам верхнего уровня и далее по темам:

| Папка | О чём |
|-------|-------|
| [`AI/`](AI) | AI-агенты для кода, Claude Code, MCP, инструменты вокруг LLM |
| [`VCS/`](VCS) | Системы контроля версий: Git, GitHub, GitHub Actions |
| [`Network/`](Network) | Сеть и SSH: IPTables, Samba, Netcat, туннели, торренты (кроссплатформенное) |
| [`Security/`](Security) | Информационная безопасность: уязвимости (CVE), эксплуатация, защита |
| [`Linux/`](Linux) | Пакетные менеджеры, Bash, Gentoo, безопасность и пр. |
| [`Programming/`](Programming) | Парадигмы, очереди сообщений, Java, алгоритмы |
| [`Health/`](Health) | Витамины и их приём |
| [`Education/`](Education) | Методики обучения |
| [`Windows/`](Windows) | WSL и прочее |
| [`Auto/`](Auto) | Автомобиль: сигнализации, электроника |
| [`Drones/`](Drones) | Дроны, БПЛА: подборки ресурсов |
| [`Electronics/`](Electronics) | Электроника и микроконтроллеры: ESP32 |
| [`Apps/`](Apps) | Заметки по приложениям и сервисам |
| [`Templates/`](Templates) | Шаблоны заметок для Obsidian |
| [`Cache/`](Cache) | Папка вложений (изображения и бинарные файлы) |

## 🗂️ Каталог заметок

### 🤖 AI

- **AI-агенты:** [Сводная таблица AI-агентов для программирования (июнь 2026)](AI/Сводная%20таблица%20AI-агентов%20для%20программирования%20%28июнь%202026%29.md)
- **Claude Code:** [Гайд](AI/Claude%20Code%20%E2%80%94%20гайд.md) · [Шпаргалка команд](AI/Claude%20Code%20%E2%80%94%20шпаргалка%20команд.md) · [MCP — серверы Model Context Protocol](AI/MCP%20%E2%80%94%20серверы%20Model%20Context%20Protocol.md)
- **Инструменты:** [AI Website Cloner](AI/AI%20Website%20Cloner%20%E2%80%94%20клонирование%20сайтов%20в%20Next.js%20через%20AI-агентов.md) · [Heretic (abliteration)](AI/Heretic%20%E2%80%94%20снятие%20safety-ограничений%20с%20открытых%20LLM%20%28abliteration%29.md) · [LiteLLM (шлюз к 100+ LLM)](AI/LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md) · [FreeQwenApi (бесплатный API к Qwen Chat)](AI/FreeQwenApi%20%E2%80%94%20бесплатный%20OpenAI-совместимый%20API%20к%20Qwen%20Chat.md) · [FreeDeepseekAPI (бесплатный API к DeepSeek)](AI/FreeDeepseekAPI%20%E2%80%94%20бесплатный%20OpenAI-совместимый%20API%20к%20DeepSeek.md)

### 🔧 VCS

- **Git:** [git status — состояние рабочего дерева](VCS/Git/status.md) · [git diff — просмотр изменений](VCS/Git/diff.md) · [git add — индексация изменений](VCS/Git/add.md) · [git commit — фиксация изменений](VCS/Git/commit.md) · [git log — история коммитов](VCS/Git/log.md) · [git reset — откат указателя и индекса](VCS/Git/reset.md) · [git restore — восстановление файлов](VCS/Git/restore.md) · [git switch — переключение веток](VCS/Git/switch.md) · [git branch — управление ветками](VCS/Git/branch.md) · [git remote — удалённые репозитории](VCS/Git/remote.md) · [git fetch — забрать с сервера](VCS/Git/fetch.md) · [git push — отправить коммиты](VCS/Git/push.md) · [git pull — забрать и влить](VCS/Git/pull.md) · [git merge — слияние веток](VCS/Git/merge.md) · [git rebase — перенос и переписывание коммитов](VCS/Git/rebase.md) · [git stash — временно спрятать правки](VCS/Git/stash.md) · [git clone — клонировать репозиторий](VCS/Git/clone.md) · [git revert — отменить коммит новым коммитом](VCS/Git/revert.md) · [git cherry-pick — перенести отдельный коммит](VCS/Git/cherry-pick.md) · [git tag — метки версий (релизы)](VCS/Git/tag.md) · [git init — создать репозиторий](VCS/Git/init.md) · [.gitignore — игнорирование файлов](VCS/Git/gitignore.md)
- **GitHub:** [GitHub Actions — автосчётчик заметок в README](VCS/GitHub/GitHub%20Actions%20%E2%80%94%20автосчётчик%20заметок%20в%20README.md)

### 🌐 Network

- **Сеть:** [IPTables](Network/IPTables.md) · [Samba](Network/Samba.md) · [Netcat](Network/Net%20Cat.md) · [Reverse Shell](Network/Reverse%20Shell.md) · [NetWatch](Network/NetWatch.md)
- **Торренты:** [qBittorrent (настройка и headless-сервер)](Network/Torrents/qBittorrent%20%E2%80%94%20настройка%20и%20headless-сервер%20%28WebUI%29.md) · [emonoda (автообновление торрентов)](Network/Torrents/emonoda%20%E2%80%94%20автообновление%20торрентов%20%28qBittorrent%29.md) · [Флаги пиров qBittorrent](Network/Torrents/Torrent%20Flags.md)
- **SSH:** [Ключи](Network/SSH/SSH-Ключи.md) · [Базовое руководство](Network/SSH/SSH-Базовое%20руководство.md) · [Продвинутое руководство](Network/SSH/SSH-Продвинутое%20руководство.md) · [Визуальное руководство по туннелям](Network/SSH/SSH-Визуальное%20руководство%20по%20туннелям.md)

### 🛡️ Security

- **CVE / Linux:** [CVE-2026-46333 — ssh-keysign-pwn (ptrace exit-race)](Security/Linux/CVE/CVE-2026-46333%20%E2%80%94%20ssh-keysign-pwn%20%28ptrace%20exit-race%29.md) · [CVE-2026-31431 — Copy Fail (algif_aead AF_ALG LPE)](Security/Linux/CVE/CVE-2026-31431%20%E2%80%94%20Copy%20Fail%20%28algif_aead%20AF_ALG%20LPE%29.md) · [Dirty Frag (CVE-2026-43284 / CVE-2026-43500)](Security/Linux/CVE/Dirty%20Frag%20%28CVE-2026-43284%20xfrm-ESP%2C%20CVE-2026-43500%20RxRPC%29.md)

### 🐧 Linux

- **Пакетные менеджеры:** [APT](Linux/Package-Manager/APT.md) · [DPKG](Linux/Package-Manager/DPKG.md) · [Aptitude](Linux/Package-Manager/Aptitude.md) · [OPKG](Linux/Package-Manager/OPKG.md) · [Сравнение команд менеджеров пакетов](Linux/Package-Manager/Сравнение%20команд%20менеджеров%20пакетов.md)
- **Команды:** [SCP](Linux/Commands/SCP.md) · [cURL](Linux/Commands/cURL.md)
- **Bash:** [for](Linux/Bash/for.md) · [sec](Linux/Bash/sec.md) · [Bench Циклов](Linux/Bash/Bench%20Циклов.md)
- **Debian / Ubuntu:** [Включить репозитории stable + sid](Linux/Debian-Ubuntu/Включить%20репозитории%20stable%20+%20sid.md) · [Настройка языка и региональных стандартов](Linux/Debian-Ubuntu/Настройка%20языка%20и%20региональных%20стандартов%20в%20Ubuntu%20Server-Debian.md)
- **Gentoo:** [Сборка или обновление ядра](Linux/Gentoo/Kernel%20-%20Сборка%20или%20Обновление%20ядра.md) · [Настройка ядра (Wiki)](Linux/Gentoo/Gentoo%20Wiki%20-%20Настройка%20ядра%20Linux.md) · [Обновление ядра (Wiki)](Linux/Gentoo/Gentoo%20Wiki%20-%20ЯдроОбновление.md)
- **Безопасность:** [Как узнать пароль user-a по SSH](Linux/Security/Как%20узнать%20пароль%20user-a,%20который%20подключается%20к%20серверу%20по%20ssh.md)
- **Серверная:** [SysRq — привести в чувство «зависший» Linux](Linux/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BD%D0%B0%D1%8F%20%C2%BB%20SysRQ%20%D0%B8%D0%BB%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%81%D1%82%D0%B8%20%D0%B2%20%D1%87%D1%83%D0%B2%D1%81%D1%82%D0%B2%D0%BE%20%C2%AB%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D1%88%D0%B8%D0%B9%C2%BB%20Linux.md)
- **Telegram:** [Шаринг файлов с серверов в Телеграм](Linux/Telegram/Шаринг%20файлов-папок%20с%20серверов%20прямо%20к%20себе%20в%20Телеграм.md)

### 💻 Programming

- **Парадигмы программирования:** [OOP](Programming/Парадигмы%20Программирования/OOP.md) · [Императивное](Programming/Парадигмы%20Программирования/Императивное%20программирование.md) · [Процедурное](Programming/Парадигмы%20Программирования/Процедурное%20программирование.md) · [Структурное](Programming/Парадигмы%20Программирования/Структурное%20программирование.md)
- **Очереди сообщений:** [Kafka vs RabbitMQ](Programming/Очереди%20сообщений/Kafka%20vs%20RabbitMQ.md) · [RabbitMQ](Programming/Очереди%20сообщений/RabbitMQ.md)
- **Java / JCF:** [PriorityQueue](Programming/Java/JCF/PriorityQueue.md)
- **Сериализация:** [Apache Fory](Programming/Serialization/Apache%20Fory%20%E2%80%94%20высокопроизводительная%20сериализация.md)
- **Алгоритмы:** [Repository and Sites](Programming/Algorithm/Repository%20and%20Sites.md)

### 🩺 Health

- [Витамины](Health/Витамины.md) · [Время приёма витаминов и минералов](Health/Время%20приёма%20витаминов%20и%20минералов.md) · [Бета-Каротин](Health/Бета-Каротин.md)

### 🎓 Education

- [Методики как учиться](Education/Методики%20как%20учится.md)

### 🪟 Windows

- [Свежая Ubuntu 23/24 в WSL](Windows/Как%20на%20wsl%20хитро%20вкорячить%20свежую%20версию%20ubuntu%2023%20или%2024.md)

### 🚗 Auto

- [StarLine A93 V2 — автосигнализация (настройка и управление)](Auto/StarLine%20A93%20V2%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%28%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%B8%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md)

### 🚁 Drones

- [awesome-drones — подборка ресурсов по дронам](Drones/awesome-drones%20%E2%80%94%20подборка%20ресурсов%20по%20дронам.md)

### 🔌 Electronics

- [ESP32 — обзор и выбор варианта (2026)](Electronics/ESP32%20%E2%80%94%20обзор%20и%20выбор%20варианта%20%282026%29.md)

### 📱 Apps

- **Разное:** [SearXNG](Apps/SearXNG.md) · [ScreenConnect](Apps/ScreenConnect.md) · [Mutagen](Apps/Mutagen/Mutagen.md)
- **Загрузчики:** [Какой выбрать](Apps/Downloaders/%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%D0%BE%D0%B9%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C.md) · [yt-dlp](Apps/Downloaders/yt-dlp.md) · [VidBee](Apps/Downloaders/VidBee.md) · [Open Video Downloader](Apps/Downloaders/Open%20Video%20Downloader.md) · [ytDownloader](Apps/Downloaders/ytDownloader.md) · [Tartube](Apps/Downloaders/Tartube.md) · [Seal](Apps/Downloaders/Seal.md)

## 🛠️ Как пользоваться

- **В Obsidian:** открыть корень репозитория как vault. Вложения хранятся в [`Cache/`](Cache) (настроено в `app.json`), внутренние ссылки и теги управляются плагинами `dataview` и `tag-wrangler`.
- **На GitHub:** заметки открываются как обычный Markdown; для навигации по длинной заметке используйте встроенное оглавление (значок ☰ у заголовка файла), в Obsidian — панель **Outline**.

## 📝 Соглашения и настройка

- [`CLAUDE.md`](CLAUDE.md) — соглашения репозитория (фронтматтер заметок, ссылки, теги, раскладка папок).
- [`Obsidian Base Settings.md`](Obsidian%20Base%20Settings.md) — рекомендуемый набор плагинов и приёмы работы.

## 📄 Лицензия

Контент репозитория распространяется по лицензии [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) — © 2026 WhiteK0T. Можно свободно делиться и адаптировать материалы, в том числе в коммерческих целях, при условии указания авторства.
