---
создал заметку: 2026-06-19T14:00:00
author: WhiteK0T
tags:
  - AI
  - ClaudeCode
  - Прокси
  - Инструменты
  - LLM
  - OpenRouter
Источник:
  - https://t.me/bugnotfeature/25921
  - https://github.com/kaitranntt/ccs
  - https://www.npmjs.com/package/@kaitranntt/ccs
---

# 🔀 CCS (Claude Code Switch) — переключатель провайдеров и аккаунтов для Claude Code

**CCS** (`kaitranntt/ccs`, MIT) — менеджер **профилей и провайдеров** для [Claude Code](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) и совместимых CLI. Он поднимает **локальный Anthropic-совместимый прокси** и позволяет одной командой переключать, **куда именно** Claude Code шлёт запросы: на разные аккаунты Claude, на Codex/Gemini/Copilot, на **OpenRouter** (300+ моделей), на GLM/Kimi или на **локальные модели** ([Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) / [llama.cpp](../Local-LLM/llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md)). Есть веб-дашборд (React, `localhost:3000`) с аналитикой и управлением профилями.

> [!warning] «Объединяем ВСЕ нейросети в один API» — что на самом деле
> Заголовок поста продаёт магию «один API ко всему». По факту:
> - Это **не универсальный API-сервис**, а **локальный прокси + менеджер профилей конкретно под Claude Code** (и Claude-совместимые CLI). Он подменяет *upstream* для уже установленного Claude Code, а не «склеивает все ИИ» в один публичный эндпоинт.
> - **«Не требует подписки Claude» — но не «бесплатно из воздуха».** Без подписки Claude ты всё равно платишь *куда-то*: API-ключи провайдеров, **кредиты OpenRouter**, либо своё железо под локальную модель. CCS лишь маршрутизирует — деньги/ресурсы за инференс берёт нижележащий провайдер.
> - **Маршрутизация по моделям** («подставить модель подешевле для простых задач») — полезная фича, но качество ответа тогда = качество **выбранной** модели, а не Claude. Дешёвая подстановка экономит, но может ронять результат на сложном.
> - Категория не уникальна: рядом — [LiteLLM](LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md), `claude-code-router`, `claude-code-proxy`. CCS выделяется **управлением аккаунтами/профилями** и дашбордом.

## 🧩 Что умеет (по README)

| Возможность | Детали |
| :--- | :--- |
| **Переключение провайдеров** | Claude, Codex, Gemini, GitHub Copilot, **OpenRouter (300+)**, GLM, Kimi, локальные модели |
| **Несколько аккаунтов/контекстов** | OAuth + API-ключи; изолированные профили (напр. work/personal), параллельный запуск в разных терминалах |
| **Локальный прокси** | встроенный **Anthropic-совместимый** CLIProxy → переводит Claude Code на OpenAI-совместимые бэкенды |
| **Маршрутизация** | `proxy.routing` по сценариям, селектор `profile:model` на лету, авто-подстановка модели |
| **Веб-дашборд** | React-панель: аналитика, мониторинг авторизаций, управление провайдерами (`:3000`) |
| **Локальные модели** | Ollama, llama.cpp и совместимые рантаймы |
| **Доп.** | WebSearch-интеграция, browser-automation, CCS Bar (menu-bar для macOS) |
| Стек / лицензия | **TypeScript** (Node.js, рантайм **Bun**), **MIT** |

## ⚠️ Риски и оговорки

> [!danger] Прокси видит все твои ключи и токены
> CCS — это **посредник между Claude Code и провайдерами**: через него проходят **API-ключи и OAuth-токены** (Claude, OpenRouter и т.д.). Запуская его, ты доверяешь стороннему коду свои секреты и трафик запросов.
> - Дашборд на `localhost:3000` — **не выставляй наружу** без аутентификации/файрвола; в Docker не публикуй порт в интернет.
> - Ставь конкретную версию и читай, что обновляется (цепочка поставок npm — см. [Atomic Arch](../../Security/Vulns/Linux/Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md) как пример рисков пакетных экосистем).

> [!caution] Подписочные OAuth-токены через прокси — серая зона ToS
> Гонять **подписку** Claude/Copilot/Codex (OAuth, а не оплачиваемый API) через сторонний прокси или **ротировать несколько аккаунтов** ради лимитов может нарушать условия использования провайдера и привести к бану. Для своих API-ключей и локальных моделей вопрос не стоит; с подписочными аккаунтами — на свой риск.

## 📦 Установка и запуск

Это **десктопный dev-инструмент** поверх Node.js — для рабочих дистрибутивов владельца; на роутере (Entware) смысла нет.

| Система | Установка |
| :--- | :--- |
| **Gentoo** | поставить Node: `emerge net-libs/nodejs`, затем `npm install -g @kaitranntt/ccs` |
| **Debian / Ubuntu** | `sudo apt install nodejs npm` (или nodesource), затем `npm install -g @kaitranntt/ccs` |
| **Arch** | `sudo pacman -S nodejs npm`, затем `npm install -g @kaitranntt/ccs` (или AUR-пакет, если появится) |
| **Docker** | готовые compose-файлы из репо; дашборд на `http://localhost:3000` |
| **Entware / RT-AX56U** | **N/A** — инструмент для рабочей станции с Claude Code, не для роутера |

```bash
# глобальная установка
npm install -g @kaitranntt/ccs

# дальше: создать профиль(и) провайдеров и переключаться между ними;
# CCS поднимает локальный Anthropic-совместимый прокси, на который смотрит Claude Code.
# Точные команды/имена профилей — по README (CLI активно развивается).
```

> [!note] Команды смотри в README
> Проект активно меняется; конкретный синтаксис команд (создание профиля, активация, routing) уточняй в [актуальном README](https://github.com/kaitranntt/ccs), а не по памяти.

## 💡 Когда полезно / кому

- **Полезно**, если ты много работаешь в **Claude Code** и хочешь: держать несколько изолированных профилей (work/personal), быстро гонять задачи через **OpenRouter/локальные модели**, экономить на простом, видеть аналитику в дашборде.
- **Альтернатива/дополнение:** если нужен **общий** шлюз к 100+ моделям для любых приложений (не только Claude Code) — смотри [LiteLLM](LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md). Бесплатные бэкенды — [FreeQwenApi](FreeQwenApi%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20Qwen%20Chat.md) / [FreeDeepseekAPI](FreeDeepseekAPI%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20DeepSeek.md).
- **Скептически:** не ждёшь «всё в одном API задаром» — платит/считает всё равно нижележащий провайдер; и не суёшь подписочные токены через прокси без оглядки на ToS.

## 🔗 Ссылки

- Репозиторий: [github.com/kaitranntt/ccs](https://github.com/kaitranntt/ccs) · npm: [@kaitranntt/ccs](https://www.npmjs.com/package/@kaitranntt/ccs)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/25921)
- Связанные: [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [LiteLLM — шлюз к 100+ LLM](LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md) · [FreeQwenApi](FreeQwenApi%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20Qwen%20Chat.md) · [FreeDeepseekAPI](FreeDeepseekAPI%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20DeepSeek.md) · [Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)

#AI #ClaudeCode #Прокси #Инструменты #LLM #OpenRouter
