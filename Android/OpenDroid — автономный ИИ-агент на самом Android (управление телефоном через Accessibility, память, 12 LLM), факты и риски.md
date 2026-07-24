---
создал заметку: 2026-07-24T18:00:00
author: WhiteK0T
tags:
  - Android
  - AI
  - Агенты
  - Автоматизация
  - Accessibility
  - Приватность
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/26509
  - https://github.com/yashab-cyber/opendroid
  - https://yashab-cyber.github.io/opendroid/
---

# 🤖 OpenDroid — автономный ИИ-агент прямо на Android

**OpenDroid** ([github.com/yashab-cyber/opendroid](https://github.com/yashab-cyber/opendroid)) — нативное Android-приложение (Kotlin/Jetpack Compose), которое превращает телефон в **автономного ИИ-агента**: понимает команду, **сам разбивает её на шаги, выполняет, проверяет результат и перепланирует** при сбое. Управляет телефоном через **Accessibility Service** (тапы, ввод текста, открытие приложений), помнит контекст между сессиями и работает с **12 LLM-провайдерами** (облако + локально). Apache-2.0, ~426★, автор — Yashab Alam (соло-разработчик); проект молодой (создан май 2026), но активно пилится, есть релиз **v1.0.1** с APK.

> [!info] Сверка поста с репозиторием — тут пост в основном честен
> | Заявление поста | Реально |
> | :--- | :--- |
> | «постоянная память между сессиями» | ✅ **4-уровневая память**: working / episodic (прошлые задачи) / semantic (факты и предпочтения) / procedural (макро-воркфлоу) |
> | «GPT, Claude, Gemini и локальные через Ollama» | ✅ и даже больше — **12 провайдеров** (Gemini, Claude, OpenAI, Groq, DeepSeek, Mistral, OpenRouter, Together, Cohere, Copilot, **Ollama**, любой OpenAI-совместимый) с авто-фолбэком |
> | «не падает на ошибках — сам обрабатывает и продолжает» | ✅ есть **ре-эвалюация/перепланирование** шагов + переключение на следующего провайдера, если текущий отвалился. Но «никогда не ошибается» ≠ «всегда делает правильно» (см. риски) |
> | «главная имба — управляет телефоном» | ✅ 60+ действий: система (WiFi/BT/яркость/скрин), связь (звонки/SMS/WhatsApp/почта), продуктивность (будильники/календарь), навигация (Maps/Uber), медиа, **финансы (UPI-платежи)**, умный дом |

> [!caution] Главное, о чём пост молчит: Accessibility + облако = серьёзные риски
> Механизм работы — **Accessibility Service**, самое мощное разрешение в Android: приложение **видит весь экран и действует за тебя**. Отсюда два риска:
> - **Приватность**: «глаза» агента — скриншоты экрана, которые уходят в **облачную LLM** (GPT/Claude/Gemini и т.д.). То есть содержимое твоих чатов/банка/почты может утекать стороннему провайдеру. Хочешь приватности — только **Ollama/on-device**, и то с оговорками.
> - **Действия с последствиями**: агент умеет **слать сообщения, платить по UPI, вызывать такси**. Ошибка планировщика/распознавания = отправленное не туда сообщение или лишний платёж. Давать такое автономно — на свой страх; тестируй на **не-основном аккаунте/устройстве**.

> [!warning] «Production-ready» — с поправкой
> В описании «production-ready», но по факту это **v1.0.1 от соло-разработчика**, ~426★, май 2026. Тот же автор (Yashab Alam / ZehraSec) сделал [awesome-osint-arsenal](../Security/OSINT/awesome-osint-arsenal%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20750%2B%20OSINT-recon-DFIR-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%20%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D0%BE%D1%81%D1%82%D0%B5%D1%80%D0%B5%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%29.md) — проект с донат-уклоном (UPI/донаты в README). Код открыт (Apache-2.0), но **жди шероховатостей** и не полагайся на него в критичных сценариях.

## 🧩 Что ещё внутри

- **Vision Engine**: скриншот через Accessibility → vision-LLM для анализа экрана; на старых устройствах откат на текстовый разбор accessibility-дерева.
- **On-device Model Manager (LiteRT-LM)**: докачка/импорт `.task`/`.litertlm`-моделей (SHA-256, проверка совместимости), Gemini Nano на устройстве — для офлайна.
- **Голос**: офлайновое wake-word «OpenDroid», распознавание речи, TTS (опц. премиум-голоса ElevenLabs).
- **Contact Disambiguation**: нечёткое сопоставление контактов («позвони папе»).

## 🛠️ Установка

Приложения **нет в Google Play** — ставится сайдлоадом:

- **Готовый APK**: из [Releases](https://github.com/yashab-cyber/opendroid/releases) (`app-release.apk`, сейчас v1.0.1).
- **Своя сборка**: JDK 21+, Android SDK 35 (Android 15) → `./gradlew assembleDebug`.
- На первом запуске выдаёшь: **Accessibility Service**, Write Settings, Record Audio, Notification Access, Post Notifications. В Settings добавляешь API-ключ провайдера (или адрес Ollama).

> [!tip] Приватный вариант — локальная модель на своём десктопе
> Чтобы не сливать экран в облако, укажи в OpenDroid **Ollama-эндпоинт своего ПК по LAN**. On-device модели телефона (Nano/LiteRT) слабоваты для сложного агентского планирования — надёжнее держать [Ollama](../AI/Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) на десктопе.

## 🖥️ Как ложится на системы владельца

Само приложение — **для Android-телефона** (нужен современный Android; целевой SDK 35). Десктопы владельца полезны рядом:

| Система | Роль |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ держать **Ollama-сервер** на десктопе и подключить к нему OpenDroid по LAN — приватный локальный «мозг» для агента |
| **Entware / RT-AX56U** | ❌ роутер не потянет LLM и не Android — только как сеть между телефоном и десктоп-Ollama |

## 🔗 Связанные заметки

- Управление телефоном **снаружи**, с десктопа (другой подход): [aya — GUI над ADB для Android](aya%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF%D0%BD%D1%8B%D0%B9%20GUI%20%D0%BD%D0%B0%D0%B4%20ADB%20%D0%B4%D0%BB%D1%8F%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20Android%20%28%D0%B7%D0%B5%D1%80%D0%BA%D0%B0%D0%BB%D0%BE%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%2C%20%D1%84%D0%B0%D0%B9%D0%BB%D1%8B%2C%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%2C%20%D0%BB%D0%BE%D0%B3%D0%B8%29.md)
- «Computer use» на десктопе: [Cua Driver — драйвер компьютерного управления для ИИ-агентов](../AI/Cua%20Driver%20%E2%80%94%20%D1%84%D0%BE%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D0%B5%D1%80%20%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%BE%D0%B3%D0%BE%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28computer%20use%2C%20MCP%29.md)
- Локальный «мозг»: [Ollama — менеджер и сервер локальных LLM](../AI/Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)

## 🔗 Ссылки

- Репозиторий: [github.com/yashab-cyber/opendroid](https://github.com/yashab-cyber/opendroid) · Сайт: [yashab-cyber.github.io/opendroid](https://yashab-cyber.github.io/opendroid/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26509)

#Android #AI #Агенты #Автоматизация #Accessibility #Приватность #Инструменты
