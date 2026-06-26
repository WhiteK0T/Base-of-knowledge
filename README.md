# 🧠 Base of knowledge

![Obsidian](https://img.shields.io/badge/Obsidian-483699?logo=obsidian&logoColor=white)
![Made with Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f?logo=markdown&logoColor=white)
![Язык: Русский](https://img.shields.io/badge/Язык-Русский-0088CC)
![Заметок](https://img.shields.io/badge/Заметок-180-success)
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
| [`Linux/`](Linux) | Пакетные менеджеры, Bash, Gentoo, файловые системы, безопасность и пр. |
| [`Programming/`](Programming) | Парадигмы, очереди сообщений, Java, алгоритмы |
| [`СУБД/`](СУБД) | Базы данных: PostgreSQL (обслуживание, производительность) |
| [`Health/`](Health) | Витамины и их приём, тренировка мозга |
| [`Education/`](Education) | Методики обучения |
| [`Windows/`](Windows) | WSL и прочее |
| [`Auto/`](Auto) | Автомобиль: сигнализации, электроника |
| [`Drones/`](Drones) | Дроны, БПЛА: подборки ресурсов |
| [`Electronics/`](Electronics) | Электроника и микроконтроллеры: ESP32, открытое железо |
| [`3D-Printing/`](3D-Printing) | 3D-печать: подборки ресурсов, софт, слайсеры |
| [`Terminal/`](Terminal) | Эмуляторы терминала и мультиплексоры: Rio, Alacritty, kitty, Konsole, tmux |
| [`File-Managers/`](File-Managers) | Файловые менеджеры (TUI/CLI): elio, far2l, Far Manager |
| [`Apps/`](Apps) | Заметки по приложениям и сервисам |
| [`Templates/`](Templates) | Шаблоны заметок для Obsidian |
| [`Cache/`](Cache) | Папка вложений (изображения и бинарные файлы) |

## 🗂️ Каталог заметок

### 🤖 AI

- **AI-агенты:** [Сводная таблица AI-агентов для программирования (июнь 2026)](AI/Сводная%20таблица%20AI-агентов%20для%20программирования%20%28июнь%202026%29.md) · [MiMo Code (терминальный агент с долгой памятью, Xiaomi)](AI/MiMo%20Code%20%E2%80%94%20терминальный%20AI-агент%20для%20кода%20с%20долгой%20памятью%20%28Xiaomi%29.md)
- **Claude Code:** [Гайд](AI/Claude%20Code%20%E2%80%94%20гайд.md) · [Шпаргалка команд](AI/Claude%20Code%20%E2%80%94%20шпаргалка%20команд.md) · [MCP — серверы Model Context Protocol](AI/MCP%20%E2%80%94%20серверы%20Model%20Context%20Protocol.md) · [workout-gate (хук: промпт за отжимания)](AI/workout-gate%20%E2%80%94%20плагин%20Claude%20Code%2C%20блокирующий%20промпт%20до%20отжиманий%20%28вебка%29.md)
- **Инструменты:** [Understand Anything (граф знаний по кодовой базе)](AI/Understand%20Anything%20%E2%80%94%20интерактивный%20граф%20знаний%20по%20кодовой%20базе.md) · [CodexPro (MCP-мост ChatGPT Dev Mode ↔ репо)](AI/CodexPro%20%E2%80%94%20MCP-мост%20между%20ChatGPT%20Developer%20Mode%20и%20локальным%20репо.md) · [Open Design (опенсорс-альтернатива Claude Design)](AI/Open%20Design%20%E2%80%94%20опенсорсная%20альтернатива%20Claude%20Design%20%28скиллы%20%2B%20дизайн-системы%29.md) · [OpenPencil (опенсорсный ИИ-редактор дизайна, альтернатива Figma, открывает .fig)](AI/OpenPencil%20%E2%80%94%20опенсорсный%20ИИ-редактор%20дизайна%20%28альтернатива%20Figma%2C%20открывает%20.fig%29.md) · [AI Website Cloner](AI/AI%20Website%20Cloner%20%E2%80%94%20клонирование%20сайтов%20в%20Next.js%20через%20AI-агентов.md) · [Cua Driver (фоновый драйвер computer-use для ИИ-агентов, MCP)](AI/Cua%20Driver%20%E2%80%94%20%D1%84%D0%BE%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D0%B5%D1%80%20%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28computer%20use%2C%20MCP%29.md) · [Unlimited-OCR (распознавание документа целиком за один проход, Baidu)](AI/Unlimited-OCR%20%E2%80%94%20%D1%80%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%20%D1%86%D0%B5%D0%BB%D0%B8%D0%BA%D0%BE%D0%BC%20%D0%B7%D0%B0%20%D0%BE%D0%B4%D0%B8%D0%BD%20%D0%BF%D1%80%D0%BE%D1%85%D0%BE%D0%B4%20%28Baidu%2C%20one-shot%20long-horizon%29.md) · [PixelRAG (RAG по скриншотам страниц вместо HTML, visual RAG)](AI/PixelRAG%20%E2%80%94%20RAG%20%D0%BF%D0%BE%20%D1%81%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D0%B0%D0%BC%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20HTML%20%28visual%20RAG%2C%20VLM-%D1%8D%D0%BC%D0%B1%D0%B5%D0%B4%D0%B4%D0%B8%D0%BD%D0%B3%D0%B8%2C%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20Claude%20Code%29.md) · [Heretic (abliteration)](AI/Heretic%20%E2%80%94%20снятие%20safety-ограничений%20с%20открытых%20LLM%20%28abliteration%29.md) · [abtop (htop для AI-агентов: мониторинг сессий Claude Code/Codex/OpenCode)](AI/abtop%20%E2%80%94%20htop%20%D0%B4%D0%BB%D1%8F%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D1%81%D0%B5%D1%81%D1%81%D0%B8%D0%B9%20Claude%20Code-Codex-OpenCode%29.md)
- **Прокси/шлюзы к LLM:** [LiteLLM (единый шлюз к 100+ LLM)](AI/ProxyLLM/LiteLLM%20%E2%80%94%20единый%20шлюз%20%28proxy%29%20к%20100%2B%20LLM.md) · [CCS (Claude Code Switch — переключатель провайдеров/аккаунтов)](AI/ProxyLLM/CCS%20%28Claude%20Code%20Switch%29%20%E2%80%94%20переключатель%20провайдеров%20и%20аккаунтов%20для%20Claude%20Code.md) · [FreeQwenApi (бесплатный API к Qwen Chat)](AI/ProxyLLM/FreeQwenApi%20%E2%80%94%20бесплатный%20OpenAI-совместимый%20API%20к%20Qwen%20Chat.md) · [FreeDeepseekAPI (бесплатный API к DeepSeek)](AI/ProxyLLM/FreeDeepseekAPI%20%E2%80%94%20бесплатный%20OpenAI-совместимый%20API%20к%20DeepSeek.md) · [OpenRouter Fusion (панель моделей + судья)](AI/ProxyLLM/OpenRouter%20Fusion%20%E2%80%94%20панель%20моделей%20%2B%20судья%20%28мульти-LLM%20синтез%29.md)
- **Skills:** [Ponytail (минимизация кода AI-агентов)](AI/Skills/Ponytail%20%E2%80%94%20скилл%20против%20%C2%ABграфомании%C2%BB%20AI-агентов%20в%20коде.md) · [Awesome-Journal-Skills (скиллы под научные журналы)](AI/Skills/Awesome-Journal-Skills%20%E2%80%94%20скиллы%20Claude%20Code%20под%20научные%20журналы.md) · [agent-skills (реестр проверенных скиллов + CLI-установка)](AI/Skills/agent-skills%20%E2%80%94%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28CLI-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20Claude%20Code-Cursor-Codex%29.md)
- **Модели:** [GLM 5.2 (открытая китайская LLM, Z.ai)](AI/GLM%205.2%20%E2%80%94%20открытая%20китайская%20LLM%20%28Z.ai%2C%20кодинг%29.md) · [Gemma 4 12B Coder (локальный GGUF-файнтюн на ризонинге Fable 5)](AI/Model/Gemma%204%2012B%20Coder%20%E2%80%94%20локальный%20файнтюн%20на%20ризонинге%20Fable%205%20%28GGUF%29.md) · [Huihui Gemma 4 12B Coder (abliterated, расцензуренная версия)](AI/Model/Huihui%20Gemma%204%2012B%20Coder%20%28abliterated%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20Gemma%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205.md) · [Qwythos-9B (расцензуренный файнтюн Qwen3.5-9B на трейсах Claude, 1M контекст)](AI/Model/Qwythos-9B-Claude-Mythos-5-1M%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20Qwen3.5-9B%20%D0%BD%D0%B0%20%D1%82%D1%80%D0%B5%D0%B9%D1%81%D0%B0%D1%85%20Claude%20%281M%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%29.md) · [North Mini Code 1.0 (открытая 30B-A3B для агентского кодинга, Cohere)](AI/Model/North%20Mini%20Code%201.0%20%E2%80%94%20открытая%2030B-A3B%20модель%20для%20агентского%20кодинга%20%28Cohere%29.md) · [LiveCodeBench v6 (бенчмарк кодинга без утечек, лидерборд)](AI/Model/LiveCodeBench%20v6%20%E2%80%94%20бенчмарк%20кодинга%20без%20утечек%20%28лидерборд%20llm-stats%29.md)
- **Локальный запуск:** [llama.cpp (движок инференса GGUF)](AI/Local-LLM/llama.cpp%20%E2%80%94%20движок%20локального%20инференса%20GGUF.md) · [Ollama (менеджер и сервер)](AI/Local-LLM/Ollama%20%E2%80%94%20менеджер%20и%20сервер%20локальных%20LLM.md) · [LM Studio (десктоп-GUI)](AI/Local-LLM/LM%20Studio%20%E2%80%94%20десктоп-GUI%20для%20локальных%20LLM.md) · [LocallyUncensored (AI-студия: чат/код/картинки/видео)](AI/Local-LLM/LocallyUncensored%20%E2%80%94%20локальная%20AI-студия%20%28чат%2C%20код%2C%20картинки%2C%20видео%29.md)
- **Петли (Loops, подробно):** [Autoloop TDD (red → green → refactor)](AI/Loops/Autoloop%20TDD%20%E2%80%94%20петля%20TDD%20%28red-green-refactor%29.md) · [PR Self-Review (ревью своего diff)](AI/Loops/PR%20Self-Review%20%E2%80%94%20петля%20самостоятельного%20ревью%20diff.md) · [Docs Sync After Edits (синхронизация доков)](AI/Loops/Docs%20Sync%20After%20Edits%20%E2%80%94%20петля%20синхронизации%20документации.md) · [Changelog Sync After Ship (обновление чейнджлога)](AI/Loops/Changelog%20Sync%20After%20Ship%20%E2%80%94%20петля%20обновления%20чейнджлога.md) · [OpenAPI Sync Until Valid (синхронизация OpenAPI)](AI/Loops/OpenAPI%20Sync%20Until%20Valid%20%E2%80%94%20петля%20синхронизации%20OpenAPI-спеки.md)
- **Ресурсы:** [Loops! (обзор сайта + каталог петель)](AI/Loops/Loops%20%E2%80%94%20обзор%20сайта%20и%20каталог%20петель.md) · [How to AI (сборник гайдов по Claude, Ruben Hassid)](AI/How%20to%20AI%20%28Ruben%20Hassid%29%20%E2%80%94%20сборник%20гайдов%20по%20Claude.md) · [92 AI-сервиса — шпаргалка по назначению](AI/92%20AI-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%B0%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BF%D0%BE%20%D0%BD%D0%B0%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8E%20%28%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%29.md) · [Yandex Open Source 2026 (гранты опенсорсу: AI Router, RAGU)](AI/Yandex%20Open%20Source%202026%20%E2%80%94%20%D0%B3%D1%80%D0%B0%D0%BD%D1%82%D1%8B%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D1%83%20%28%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20AI-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%29.md) · [In the Weights (помнит ли вас нейросеть «по памяти» — тест присутствия в весах LLM)](AI/In%20the%20Weights%20%E2%80%94%20%D0%BF%D0%BE%D0%BC%D0%BD%D0%B8%D1%82%20%D0%BB%D0%B8%20%D0%B2%D0%B0%D1%81%20%D0%BD%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%C2%AB%D0%BF%D0%BE%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%B8%C2%BB%20%28%D1%82%D0%B5%D1%81%D1%82%20%D0%BF%D1%80%D0%B8%D1%81%D1%83%D1%82%D1%81%D1%82%D0%B2%D0%B8%D1%8F%20%D0%B2%20%D0%B2%D0%B5%D1%81%D0%B0%D1%85%20LLM%29.md)
- **Промпты:** [План питания на неделю под бюджет (4 промпта: меню, покупки, готовка, упрощёнка)](AI/%D0%9F%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D1%8B%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D0%BB%D0%B0%D0%BD%D0%B0%20%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%BD%D0%B0%20%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8E%20%D0%BF%D0%BE%D0%B4%20%D0%B1%D1%8E%D0%B4%D0%B6%D0%B5%D1%82%20%284%20%D0%BF%D1%80%D0%BE%D0%BC%D0%BF%D1%82%D0%B0%3A%20%D0%BC%D0%B5%D0%BD%D1%8E%2C%20%D0%BF%D0%BE%D0%BA%D1%83%D0%BF%D0%BA%D0%B8%2C%20%D0%B3%D0%BE%D1%82%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D1%83%D0%BF%D1%80%D0%BE%D1%89%D1%91%D0%BD%D0%BA%D0%B0%29.md)

### 🔧 VCS

- **Git:** 🗺️ [Git — карта команд (шпаргалка)](VCS/Git/Git%20%E2%80%94%20карта%20команд%20%28шпаргалка%29.md) · [git status — состояние рабочего дерева](VCS/Git/status.md) · [git diff — просмотр изменений](VCS/Git/diff.md) · [git add — индексация изменений](VCS/Git/add.md) · [git commit — фиксация изменений](VCS/Git/commit.md) · [git log — история коммитов](VCS/Git/log.md) · [git reset — откат указателя и индекса](VCS/Git/reset.md) · [git restore — восстановление файлов](VCS/Git/restore.md) · [git switch — переключение веток](VCS/Git/switch.md) · [git branch — управление ветками](VCS/Git/branch.md) · [git remote — удалённые репозитории](VCS/Git/remote.md) · [git fetch — забрать с сервера](VCS/Git/fetch.md) · [git push — отправить коммиты](VCS/Git/push.md) · [git pull — забрать и влить](VCS/Git/pull.md) · [git merge — слияние веток](VCS/Git/merge.md) · [git rebase — перенос и переписывание коммитов](VCS/Git/rebase.md) · [git stash — временно спрятать правки](VCS/Git/stash.md) · [git clone — клонировать репозиторий](VCS/Git/clone.md) · [git revert — отменить коммит новым коммитом](VCS/Git/revert.md) · [git cherry-pick — перенести отдельный коммит](VCS/Git/cherry-pick.md) · [git tag — метки версий (релизы)](VCS/Git/tag.md) · [git init — создать репозиторий](VCS/Git/init.md) · [.gitignore — игнорирование файлов](VCS/Git/gitignore.md) · [git config — настройки Git](VCS/Git/config.md) · [git show — показать объект](VCS/Git/show.md) · [git blame — авторство строк](VCS/Git/blame.md) · [git rm — удалить отслеживаемый файл](VCS/Git/rm.md) · [git clean — удалить неотслеживаемые файлы](VCS/Git/clean.md) · [git mv — переместить/переименовать](VCS/Git/mv.md) · [git reflog — журнал и восстановление](VCS/Git/reflog.md) · [git bisect — двоичный поиск бага](VCS/Git/bisect.md) · [git submodule — вложенные репозитории](VCS/Git/submodule.md) · 🔐 [git-crypt — прозрачное шифрование файлов](VCS/Git/git-crypt%20%E2%80%94%20%D0%BF%D1%80%D0%BE%D0%B7%D1%80%D0%B0%D1%87%D0%BD%D0%BE%D0%B5%20%D1%88%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%20%D0%B2%20%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8.md)
- **GitHub:** [GitHub Actions — автосчётчик заметок в README](VCS/GitHub/GitHub%20Actions%20%E2%80%94%20автосчётчик%20заметок%20в%20README.md)

### 🌐 Network

- **Сеть:** [IPTables](Network/IPTables.md) · [Samba](Network/Samba.md) · [Netcat](Network/Net%20Cat.md) · [Reverse Shell](Network/Reverse%20Shell.md) · [NetWatch](Network/NetWatch.md)
- **DNS-фильтрация:** [1Hosts (DNS-блоклисты против рекламы/трекеров/malware, Lite/Xtra)](Network/1Hosts%20%E2%80%94%20DNS-%D0%B1%D0%BB%D0%BE%D0%BA%D0%BB%D0%B8%D1%81%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D1%8B%2C%20%D1%82%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D0%BE%D0%B2%20%D0%B8%20malware%20%28Lite-Xtra%2C%20Pi-hole-AdGuard%20Home%29.md)
- **Торренты:** [qBittorrent (настройка и headless-сервер)](Network/Torrents/qBittorrent%20%E2%80%94%20настройка%20и%20headless-сервер%20%28WebUI%29.md) · [emonoda (автообновление торрентов)](Network/Torrents/emonoda%20%E2%80%94%20автообновление%20торрентов%20%28qBittorrent%29.md) · [Флаги пиров qBittorrent](Network/Torrents/Torrent%20Flags.md)
- **SSH:** [Ключи](Network/SSH/SSH-Ключи.md) · [Базовое руководство](Network/SSH/SSH-Базовое%20руководство.md) · [Продвинутое руководство](Network/SSH/SSH-Продвинутое%20руководство.md) · [Визуальное руководство по туннелям](Network/SSH/SSH-Визуальное%20руководство%20по%20туннелям.md)

### 🛡️ Security

- **Базы и справочники:** [Базы уязвимостей для пентестера (CVE, ФСТЭК, НКЦКИ, MITRE ATT&CK, Exploit-DB)](Security/%D0%91%D0%B0%D0%B7%D1%8B%20%D1%83%D1%8F%D0%B7%D0%B2%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B5%D0%B9%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D0%B5%D0%BD%D1%82%D0%B5%D1%81%D1%82%D0%B5%D1%80%D0%B0%20%E2%80%94%20%D0%B3%D0%B4%D0%B5%20%D0%B8%D1%81%D0%BA%D0%B0%D1%82%D1%8C%20%28CVE%2C%20%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A%2C%20%D0%9D%D0%9A%D0%A6%D0%9A%D0%98%2C%20MITRE%20ATT%26CK%2C%20Exploit-DB%29.md)
- **Форензика / DFIR:** [AndroidForensics — извлечение данных с Android через ADB (триаж, разбор и право)](Security/Forensics/AndroidForensics%20%E2%80%94%20%D0%B8%D0%B7%D0%B2%D0%BB%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%20Android%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20ADB%20%28DFIR-%D1%82%D1%80%D0%B8%D0%B0%D0%B6%2C%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md)
- **Реверс-инжиниринг / RE:** [Reversecore MCP — MCP-сервер для реверса и анализа malware (Radare2/r2ghidra/YARA)](Security/Reverse-Engineering/Reversecore%20MCP%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D0%B8%D0%BD%D0%B6%D0%B8%D0%BD%D0%B8%D1%80%D0%B8%D0%BD%D0%B3%D0%B0%20%D0%B8%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%20malware%20%28Radare2-r2ghidra-YARA%29.md)
- **OSINT / разведка:** [Web Check — OSINT-досье на сайт (DNS/SSL/заголовки/стек/порты)](Security/OSINT/Web%20Check%20%E2%80%94%20OSINT-досье%20на%20сайт%20%28DNS-SSL-заголовки-стек-порты%29.md) · [awesome-osint-arsenal — установщик 750+ OSINT/recon/DFIR-инструментов (разбор + предостережения)](Security/OSINT/awesome-osint-arsenal%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20750%2B%20OSINT-recon-DFIR-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B5%D1%80%D0%B5%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%29.md) · [awesome-osint-chrome-extensions — браузерные расширения для OSINT (Chrome/Brave)](Security/OSINT/awesome-osint-chrome-extensions%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D1%8B%D1%85%20%D1%80%D0%B0%D1%81%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%B8%D0%B9%20%D0%B4%D0%BB%D1%8F%20OSINT%20%28Chrome-Brave%29.md)
- **Социнженерия / фишинг:** [Storm-Breaker — фишинг вебки/микрофона/геолокации (разбор и защита)](Security/Social-Engineering/Storm-Breaker%20%E2%80%94%20фишинг%20вебки-микрофона-геолокации%20%28разбор%20и%20защита%29.md)
- **Supply-chain:** [Atomic Arch — атака на AUR (infostealer + eBPF-руткит)](Security/Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md)
- **CVE / Linux:** [CVE-2026-55200 — libssh2 pre-auth OOB-write (Токсичное рукопожатие)](Security/Linux/CVE/CVE-2026-55200%20%E2%80%94%20libssh2%20pre-auth%20OOB-write%20%28%D0%A2%D0%BE%D0%BA%D1%81%D0%B8%D1%87%D0%BD%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%BF%D0%BE%D0%B6%D0%B0%D1%82%D0%B8%D0%B5%29.md) · [CVE-2026-46333 — ssh-keysign-pwn (ptrace exit-race)](Security/Linux/CVE/CVE-2026-46333%20%E2%80%94%20ssh-keysign-pwn%20%28ptrace%20exit-race%29.md) · [CVE-2026-31431 — Copy Fail (algif_aead AF_ALG LPE)](Security/Linux/CVE/CVE-2026-31431%20%E2%80%94%20Copy%20Fail%20%28algif_aead%20AF_ALG%20LPE%29.md) · [Dirty Frag (CVE-2026-43284 / CVE-2026-43500)](Security/Linux/CVE/Dirty%20Frag%20%28CVE-2026-43284%20xfrm-ESP%2C%20CVE-2026-43500%20RxRPC%29.md) · [Squidbleed (CVE-2026-47729 — Squid FTP heap OOB-read, утечка памяти)](Security/Linux/CVE/CVE-2026-47729%20%E2%80%94%20Squidbleed%20%28Squid%20FTP%20heap%20OOB-read%2C%20%D1%83%D1%82%D0%B5%D1%87%D0%BA%D0%B0%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%B8%29.md)

### 🐧 Linux

- **Пакетные менеджеры:** [APT](Linux/Package-Manager/APT.md) · [DPKG](Linux/Package-Manager/DPKG.md) · [Aptitude](Linux/Package-Manager/Aptitude.md) · [OPKG](Linux/Package-Manager/OPKG.md) · [Сравнение команд менеджеров пакетов](Linux/Package-Manager/Сравнение%20команд%20менеджеров%20пакетов.md)
- **Команды:** [SCP](Linux/Commands/SCP.md) · [cURL](Linux/Commands/cURL.md) · [sed (потоковый редактор текста)](Linux/Commands/sed.md)
- **Bash:** [for](Linux/Bash/for.md) · [sec](Linux/Bash/sec.md) · [Bench Циклов](Linux/Bash/Bench%20Циклов.md)
- **Debian / Ubuntu:** [Включить репозитории stable + sid](Linux/Debian-Ubuntu/Включить%20репозитории%20stable%20+%20sid.md) · [Настройка языка и региональных стандартов](Linux/Debian-Ubuntu/Настройка%20языка%20и%20региональных%20стандартов%20в%20Ubuntu%20Server-Debian.md)
- **Gentoo:** [Сборка или обновление ядра](Linux/Gentoo/Kernel%20-%20Сборка%20или%20Обновление%20ядра.md) · [Настройка ядра (Wiki)](Linux/Gentoo/Gentoo%20Wiki%20-%20Настройка%20ядра%20Linux.md) · [Обновление ядра (Wiki)](Linux/Gentoo/Gentoo%20Wiki%20-%20ЯдроОбновление.md)
- **Файловые системы:** [Btrfs — CoW-ФС (подтома, снапшоты, RAID): практика и устройство](Linux/Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md)
- **Безопасность:** [Как узнать пароль user-a по SSH](Linux/Security/Как%20узнать%20пароль%20user-a,%20который%20подключается%20к%20серверу%20по%20ssh.md)
- **Серверная:** [SysRq — привести в чувство «зависший» Linux](Linux/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BD%D0%B0%D1%8F%20%C2%BB%20SysRQ%20%D0%B8%D0%BB%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%81%D1%82%D0%B8%20%D0%B2%20%D1%87%D1%83%D0%B2%D1%81%D1%82%D0%B2%D0%BE%20%C2%AB%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D1%88%D0%B8%D0%B9%C2%BB%20Linux.md)
- **Совместимость (Windows на Linux):** [WinPodX (Windows-приложения как нативные окна Linux: контейнерная Windows-ВМ + RemoteApp)](Linux/WinPodX%20%E2%80%94%20Windows-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%B0%D0%BA%20%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0%20Linux%20%28%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%BD%D0%B0%D1%8F%20Windows-%D0%92%D0%9C%20%2B%20RemoteApp%29.md)
- **Linux на Android:** [linux-android (Linux-десктоп на Android через Termux без root: proot + Termux-X11)](Linux/linux-android%20%E2%80%94%20Linux-%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF%20%D0%BD%D0%B0%20Android%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20Termux%20%D0%B1%D0%B5%D0%B7%20root%20%28proot%20%2B%20Termux-X11%29.md)
- **Telegram:** [Шаринг файлов с серверов в Телеграм](Linux/Telegram/Шаринг%20файлов-папок%20с%20серверов%20прямо%20к%20себе%20в%20Телеграм.md)

### 💻 Programming

- **Парадигмы программирования:** [OOP](Programming/Парадигмы%20Программирования/OOP.md) · [Императивное](Programming/Парадигмы%20Программирования/Императивное%20программирование.md) · [Процедурное](Programming/Парадигмы%20Программирования/Процедурное%20программирование.md) · [Структурное](Programming/Парадигмы%20Программирования/Структурное%20программирование.md)
- **Очереди сообщений:** [Kafka vs RabbitMQ](Programming/Очереди%20сообщений/Kafka%20vs%20RabbitMQ.md) · [RabbitMQ](Programming/Очереди%20сообщений/RabbitMQ.md)
- **Java / JCF:** [PriorityQueue](Programming/Java/JCF/PriorityQueue.md)
- **Java / Hibernate:** [Hibernate выполняет SQL не в порядке кода (порядок action queue при flush)](Programming/Java/Hibernate/Hibernate%20%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D1%8F%D0%B5%D1%82%20SQL%20%D0%BD%D0%B5%20%D0%B2%20%D0%BF%D0%BE%D1%80%D1%8F%D0%B4%D0%BA%D0%B5%20%D0%B2%D0%B0%D1%88%D0%B5%D0%B3%D0%BE%20%D0%BA%D0%BE%D0%B4%D0%B0%20%28%D0%BF%D0%BE%D1%80%D1%8F%D0%B4%D0%BE%D0%BA%20action%20queue%20%D0%BF%D1%80%D0%B8%20flush%29.md)
- **Сериализация:** [Apache Fory](Programming/Serialization/Apache%20Fory%20%E2%80%94%20высокопроизводительная%20сериализация.md)
- **Алгоритмы:** [Repository and Sites](Programming/Algorithm/Repository%20and%20Sites.md)

### 🗄️ СУБД

- **PostgreSQL:** [VACUUM FULL — возврат места на диске (bloat, dead tuples, pg_repack)](%D0%A1%D0%A3%D0%91%D0%94/Postgres/VACUUM%20FULL%20%E2%80%94%20%D0%B2%D0%BE%D0%B7%D0%B2%D1%80%D0%B0%D1%82%20%D0%BC%D0%B5%D1%81%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%B4%D0%B8%D1%81%D0%BA%D0%B5%20%D0%B2%20PostgreSQL%20%28bloat%2C%20dead%20tuples%2C%20pg_repack%29.md)

### 🩺 Health

- [Витамины](Health/Витамины.md) · [Время приёма витаминов и минералов](Health/Время%20приёма%20витаминов%20и%20минералов.md) · [Бета-Каротин](Health/Бета-Каротин.md) · [Метод Кавашимы (тренировка мозга: счёт + чтение вслух)](Health/Метод%20Кавашимы%20%E2%80%94%20тренировка%20мозга%20%28быстрый%20устный%20счёт%20%2B%20чтение%20вслух%29.md)

### 🎓 Education

- [Методики как учиться](Education/Методики%20как%20учится.md) · [Изучение языка с ИИ — каркас из 6 промптов (вместо Duolingo)](Education/Изучение%20языка%20с%20ИИ%20%E2%80%94%20каркас%20из%206%20промптов%20%28вместо%20Duolingo%29.md) · [Open Culture — 1700+ бесплатных университетских курсов (+ книги, аудио, кино, языки)](Education/Open%20Culture%20%E2%80%94%201700%2B%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D1%85%20%D1%83%D0%BD%D0%B8%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%82%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D1%85%20%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%28%D0%B0%D0%B3%D1%80%D0%B5%D0%B3%D0%B0%D1%82%D0%BE%D1%80%20%D0%BA%D0%BD%D0%B8%D0%B3%2C%20%D0%B0%D1%83%D0%B4%D0%B8%D0%BE%2C%20%D0%BA%D0%B8%D0%BD%D0%BE%2C%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%B2%29.md)

### 🪟 Windows

- [Свежая Ubuntu 23/24 в WSL](Windows/Как%20на%20wsl%20хитро%20вкорячить%20свежую%20версию%20ubuntu%2023%20или%2024.md) · [System Informer (мониторинг процессов и охота на малварь, преемник Process Hacker)](Windows/System%20Informer%20%E2%80%94%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%BE%D1%85%D0%BE%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%BC%D0%B0%D0%BB%D0%B2%D0%B0%D1%80%D1%8C%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20Process%20Hacker%29.md)

### 🚗 Auto

- [StarLine A93 V2 — автосигнализация (настройка и управление)](Auto/StarLine%20A93%20V2%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%28%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%B8%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%29.md)

### 🚁 Drones

- [awesome-drones — подборка ресурсов по дронам](Drones/awesome-drones%20%E2%80%94%20подборка%20ресурсов%20по%20дронам.md)

### 🔌 Electronics

- [ESP32 — обзор и выбор варианта (2026)](Electronics/ESP32%20%E2%80%94%20обзор%20и%20выбор%20варианта%20%282026%29.md)
- [awesome-open-hardware — подборка ресурсов по открытому железу (open hardware)](Electronics/awesome-open-hardware%20%E2%80%94%20подборка%20ресурсов%20по%20открытому%20железу%20%28open%20hardware%29.md)

### 🖨️ 3D-Printing

- [awesome-3d-printing — подборка ресурсов по 3D-печати](3D-Printing/awesome-3d-printing%20%E2%80%94%20подборка%20ресурсов%20по%203D-печати.md)

### 💻 Terminal

- **Эмуляторы:** [Rio (WebGPU, вкладки/сплиты)](Terminal/Rio%20%E2%80%94%20быстрый%20терминал%20на%20WebGPU%20%28Rust%29.md) · [Alacritty (OpenGL, минимализм)](Terminal/Alacritty%20%E2%80%94%20GPU-терминал%20на%20OpenGL%20%28минимализм%29.md) · [kitty (kittens, графика)](Terminal/kitty%20%E2%80%94%20GPU-терминал%20с%20kittens%20и%20графикой%20%28OpenGL%29.md) · [Konsole (KDE, профили)](Terminal/Konsole%20%E2%80%94%20терминал%20KDE%20%28профили%2C%20split-view%2C%20Qt%29.md)
- **Мультиплексоры:** [tmux (сессии, окна, панели)](Terminal/tmux%20%E2%80%94%20терминальный%20мультиплексор%20%28сессии%2C%20окна%2C%20панели%29.md) · [Horizon (GPU «бесконечный холст» сессий, Rust)](Terminal/Horizon%20%E2%80%94%20терминальный%20%C2%AB%D0%B1%D0%B5%D1%81%D0%BA%D0%BE%D0%BD%D0%B5%D1%87%D0%BD%D1%8B%D0%B9%20%D1%85%D0%BE%D0%BB%D1%81%D1%82%C2%BB%20%D0%BD%D0%B0%20GPU%20%28Rust%29.md)

### 🗂️ File-Managers

- **Терминальные:** [elio (трёхпанельный, превью с картинками, Rust)](File-Managers/elio%20%E2%80%94%20терминальный%20файловый%20менеджер%20с%20превью%20%28Rust%29.md)
- **FAR-семейство:** [far2l (порт FAR на Linux/macOS/BSD)](File-Managers/far2l%20%E2%80%94%20порт%20FAR%20Manager%20на%20Linux-macOS-BSD%20%28двухпанельный%29.md) · [Far Manager 3 (far3, Windows-оригинал)](File-Managers/Far%20Manager%203%20%28far3%29%20%E2%80%94%20ортодоксальный%20файловый%20менеджер%20для%20Windows.md)

### 📱 Apps

- **Разное:** [SearXNG](Apps/SearXNG.md) · [ScreenConnect](Apps/ScreenConnect.md) · [Mutagen](Apps/Mutagen/Mutagen.md) · [Pi-hole (сетевой блокировщик рекламы по DNS)](Apps/Pi-hole%20%E2%80%94%20сетевой%20блокировщик%20рекламы%20и%20телеметрии%20%28DNS-sinkhole%29.md) · [web-to-app (сборка Android-APK из сайта прямо на телефоне)](Apps/web-to-app%20%E2%80%94%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20Android-APK%20%D0%B8%D0%B7%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%BF%D1%80%D1%8F%D0%BC%D0%BE%20%D0%BD%D0%B0%20%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%D0%B5%20%28%D0%BA%D0%B0%D1%80%D0%BC%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F%20APK-%D0%BC%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%81%D0%BA%D0%B0%D1%8F%29.md) · [Bookracy (теневая библиотека книг/манги — риски и легальные альтернативы)](Apps/Bookracy%20%E2%80%94%20%D1%82%D0%B5%D0%BD%D0%B5%D0%B2%D0%B0%D1%8F%20%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B0%20%D0%BA%D0%BD%D0%B8%D0%B3%20%D0%B8%20%D0%BC%D0%B0%D0%BD%D0%B3%D0%B8%20%28%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%2C%20%D1%80%D0%B8%D1%81%D0%BA%D0%B8%20%D0%B8%20%D0%BB%D0%B5%D0%B3%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D1%8B%29.md) · [Look4Sat (отслеживание спутников и прогноз пролётов на Android, ham-radio/TLE)](Apps/Look4Sat%20%E2%80%94%20%D0%BE%D1%82%D1%81%D0%BB%D0%B5%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%81%D0%BF%D1%83%D1%82%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%B8%20%D0%BF%D1%80%D0%BE%D0%B3%D0%BD%D0%BE%D0%B7%20%D0%BF%D1%80%D0%BE%D0%BB%D1%91%D1%82%D0%BE%D0%B2%20%D0%BD%D0%B0%20Android%20%28ham-radio%2C%20TLE%29.md) · [SigDigger (анализ и декодирование неизвестных радиосигналов, SDR)](Apps/SigDigger%20%E2%80%94%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%B8%20%D0%B4%D0%B5%D0%BA%D0%BE%D0%B4%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BD%D0%B5%D0%B8%D0%B7%D0%B2%D0%B5%D1%81%D1%82%D0%BD%D1%8B%D1%85%20%D1%80%D0%B0%D0%B4%D0%B8%D0%BE%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D0%BB%D0%BE%D0%B2%20%28SDR%2C%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81%20%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D0%BB%D0%BE%D0%B2%29.md)
- **Браузерные расширения:** [VOT (закадровый перевод и озвучка видео)](Apps/Browser-Extensions/VOT%20%E2%80%94%20закадровый%20перевод%20и%20озвучка%20видео%20%28Voice-Over-Translation%29.md) · [Tampermonkey (менеджер юзерскриптов)](Apps/Browser-Extensions/Tampermonkey%20%E2%80%94%20менеджер%20юзерскриптов.md)
- **Загрузчики:** [Какой выбрать](Apps/Downloaders/%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%D0%BE%D0%B9%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C.md) · [yt-dlp](Apps/Downloaders/yt-dlp.md) · [VidBee](Apps/Downloaders/VidBee.md) · [Open Video Downloader](Apps/Downloaders/Open%20Video%20Downloader.md) · [ytDownloader](Apps/Downloaders/ytDownloader.md) · [Tartube](Apps/Downloaders/Tartube.md) · [Seal](Apps/Downloaders/Seal.md)

## 🛠️ Как пользоваться

- **В Obsidian:** открыть корень репозитория как vault. Вложения хранятся в [`Cache/`](Cache) (настроено в `app.json`), внутренние ссылки и теги управляются плагинами `dataview` и `tag-wrangler`.
- **На GitHub:** заметки открываются как обычный Markdown; для навигации по длинной заметке используйте встроенное оглавление (значок ☰ у заголовка файла), в Obsidian — панель **Outline**.

## 📝 Соглашения и настройка

- [`CLAUDE.md`](CLAUDE.md) — соглашения репозитория (фронтматтер заметок, ссылки, теги, раскладка папок).
- [`Obsidian Base Settings.md`](Obsidian%20Base%20Settings.md) — рекомендуемый набор плагинов и приёмы работы.

## 📄 Лицензия

Контент репозитория распространяется по лицензии [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) — © 2026 WhiteK0T. Можно свободно делиться и адаптировать материалы, в том числе в коммерческих целях, при условии указания авторства.
