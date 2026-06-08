# 🧠 Base of knowledge

![Obsidian](https://img.shields.io/badge/Obsidian-483699?logo=obsidian&logoColor=white)
![Made with Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f?logo=markdown&logoColor=white)
![Язык: Русский](https://img.shields.io/badge/Язык-Русский-0088CC)
![Заметок](https://img.shields.io/badge/Заметок-54-success)
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
| [`VCS/`](VCS) | Системы контроля версий: GitHub, GitHub Actions |
| [`Network/`](Network) | Сеть и SSH: IPTables, Samba, Netcat, туннели (кроссплатформенное) |
| [`Linux/`](Linux) | Пакетные менеджеры, Bash, Gentoo, безопасность и пр. |
| [`Programming/`](Programming) | Парадигмы, очереди сообщений, Java, алгоритмы |
| [`Health/`](Health) | Витамины и их приём |
| [`Education/`](Education) | Методики обучения |
| [`Windows/`](Windows) | WSL и прочее |
| [`Drones/`](Drones) | Дроны, БПЛА: подборки ресурсов |
| [`Apps/`](Apps) | Заметки по приложениям и сервисам |
| [`Templates/`](Templates) | Шаблоны заметок для Obsidian |
| [`Cache/`](Cache) | Папка вложений (изображения и бинарные файлы) |

## 🗂️ Каталог заметок

### 🤖 AI

- **AI-агенты:** [Сводная таблица AI-агентов для программирования (июнь 2026)](AI/Сводная%20таблица%20AI-агентов%20для%20программирования%20%28июнь%202026%29.md)
- **Claude Code:** [Гайд](AI/Claude%20Code%20%E2%80%94%20гайд.md) · [Шпаргалка команд](AI/Claude%20Code%20%E2%80%94%20шпаргалка%20команд.md) · [MCP — серверы Model Context Protocol](AI/MCP%20%E2%80%94%20серверы%20Model%20Context%20Protocol.md)
- **Инструменты:** [AI Website Cloner](AI/AI%20Website%20Cloner%20%E2%80%94%20клонирование%20сайтов%20в%20Next.js%20через%20AI-агентов.md) · [Heretic (abliteration)](AI/Heretic%20%E2%80%94%20снятие%20safety-ограничений%20с%20открытых%20LLM%20%28abliteration%29.md)

### 🔧 VCS

- **GitHub:** [GitHub Actions — автосчётчик заметок в README](VCS/GitHub/GitHub%20Actions%20%E2%80%94%20автосчётчик%20заметок%20в%20README.md)

### 🌐 Network

- **Сеть:** [IPTables](Network/IPTables.md) · [Samba](Network/Samba.md) · [Netcat](Network/Net%20Cat.md) · [Reverse Shell](Network/Reverse%20Shell.md) · [Флаги пиров qBittorrent](Network/Torrent%20Flags.md) · [NetWatch](Network/NetWatch.md)
- **SSH:** [Ключи](Network/SSH/SSH-Ключи.md) · [Базовое руководство](Network/SSH/SSH-Базовое%20руководство.md) · [Продвинутое руководство](Network/SSH/SSH-Продвинутое%20руководство.md) · [Визуальное руководство по туннелям](Network/SSH/SSH-Визуальное%20руководство%20по%20туннелям.md)

### 🐧 Linux

- **Пакетные менеджеры:** [APT](Linux/Package-Manager/APT.md) · [DPKG](Linux/Package-Manager/DPKG.md) · [Aptitude](Linux/Package-Manager/Aptitude.md) · [OPKG](Linux/Package-Manager/OPKG.md) · [Сравнение команд менеджеров пакетов](Linux/Package-Manager/Сравнение%20команд%20менеджеров%20пакетов.md)
- **Команды:** [SCP](Linux/Commands/SCP.md) · [cURL](Linux/Commands/cURL.md)
- **Bash:** [for](Linux/Bash/for.md) · [sec](Linux/Bash/sec.md) · [Bench Циклов](Linux/Bash/Bench%20Циклов.md)
- **Debian / Ubuntu:** [Включить репозитории stable + sid](Linux/Debian-Ubuntu/Включить%20репозитории%20stable%20+%20sid.md) · [Настройка языка и региональных стандартов](Linux/Debian-Ubuntu/Настройка%20языка%20и%20региональных%20стандартов%20в%20Ubuntu%20Server-Debian.md)
- **Gentoo:** [Сборка или обновление ядра](Linux/Gentoo/Kernel%20-%20Сборка%20или%20Обновление%20ядра.md) · [Настройка ядра (Wiki)](Linux/Gentoo/Gentoo%20Wiki%20-%20Настройка%20ядра%20Linux.md) · [Обновление ядра (Wiki)](Linux/Gentoo/Gentoo%20Wiki%20-%20ЯдроОбновление.md)
- **Безопасность:** [Как узнать пароль user-a по SSH](Linux/Security/Как%20узнать%20пароль%20user-a,%20который%20подключается%20к%20серверу%20по%20ssh.md)
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

### 🚁 Drones

- [awesome-drones — подборка ресурсов по дронам](Drones/awesome-drones%20%E2%80%94%20подборка%20ресурсов%20по%20дронам.md)

### 📱 Apps

- [SearXNG](Apps/SearXNG.md) · [ScreenConnect](Apps/ScreenConnect.md) · [Mutagen](Apps/Mutagen/Mutagen.md)

## 🛠️ Как пользоваться

- **В Obsidian:** открыть корень репозитория как vault. Вложения хранятся в [`Cache/`](Cache) (настроено в `app.json`), внутренние ссылки и теги управляются плагинами `dataview` и `tag-wrangler`.
- **На GitHub:** заметки открываются как обычный Markdown; для навигации по длинной заметке используйте встроенное оглавление (значок ☰ у заголовка файла), в Obsidian — панель **Outline**.

## 📝 Соглашения и настройка

- [`CLAUDE.md`](CLAUDE.md) — соглашения репозитория (фронтматтер заметок, ссылки, теги, раскладка папок).
- [`Obsidian Base Settings.md`](Obsidian%20Base%20Settings.md) — рекомендуемый набор плагинов и приёмы работы.

## 📄 Лицензия

Контент репозитория распространяется по лицензии [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) — © 2026 WhiteK0T. Можно свободно делиться и адаптировать материалы, в том числе в коммерческих целях, при условии указания авторства.
