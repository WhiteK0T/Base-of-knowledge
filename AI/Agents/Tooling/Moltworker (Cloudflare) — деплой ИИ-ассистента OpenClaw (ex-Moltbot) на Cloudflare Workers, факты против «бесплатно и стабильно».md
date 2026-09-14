---
создал заметку: 2026-09-14T20:40:00
author: WhiteK0T
tags:
  - AI
  - Agents
  - Cloudflare
  - SelfHosted
  - OpenClaw
  - ClaudeAPI
  - Инструменты
Источник:
  - https://t.me/c/2675453029/1405
  - https://github.com/cloudflare/moltworker
---

# ☁️ Moltworker — деплой ИИ-ассистента OpenClaw на Cloudflare Workers

**Moltworker** ([github.com/cloudflare/moltworker](https://github.com/cloudflare/moltworker), **официальный проект Cloudflare**, Apache-2.0, TypeScript, ~10k★) — пакет, который разворачивает **OpenClaw** на **Cloudflare Workers Sandbox** (контейнеры). **OpenClaw** (это и есть «Moltbot» из поста — бывшие имена **Moltbot / Clawdbot**) — персональный ИИ-ассистент с gateway-архитектурой: подключается к чат-платформам (**Telegram, Discord, Slack**), с device-pairing аутентификацией и постоянной историей диалогов. Деплой — `npm run deploy` (через `wrangler`), опционально с веб-панелью управления.

> [!warning] Отделяем факты от рекламы поста
> | Заявление поста | Реально |
> | :--- | :--- |
> | «Moltbot» | имя устарело: теперь **OpenClaw** (ex-Moltbot, ex-Clawdbot). Ищи по «OpenClaw»/«moltworker» |
> | «стабилен» | ❌ репозиторий прямо помечен как **experimental / proof of concept**: «It is not officially supported and may break without notice». Это демо, не продакшн-решение |
> | «не нужно покупать железо» | формально да, но **не бесплатно**: нужен **Cloudflare Workers Paid ($5/мес)** для Sandbox-контейнеров **+ оплата LLM** (ключ Anthropic/Claude напрямую или через Cloudflare AI Gateway). Оценка 24/7 ≈ **$34.5/мес** |
> | «всегда доступен, без вмешательства» | контейнер можно усыпить (`SANDBOX_SLEEP_AFTER`) ради экономии — тогда «always-on» уже условный; за расходом надо следить |
> | «ИИ-ассистент» | ✅ верно, но это **чат-ассистент** (Telegram/Discord/Slack), а **не** кодинг-агент вроде Claude Code |

> [!danger] Безопасность: ты выставляешь ИИ-ассистента в интернет
> Это публичный эндпоинт с доступом к твоему LLM-ключу и историям. В комплекте есть защита, но её надо **включить и не слить**:
> - **Cloudflare Access** прикрывает админ-маршруты;
> - **Device Pairing** — каждое устройство одобряется вручную в админке до общения с ассистентом;
> - **gateway-токен** держать в секрете. Нюанс: **URL панели управления содержит токен в query-параметре** → он может утечь через логи/историю браузера/реферер. Обращайся с этой ссылкой как с паролем.

## 📦 Что нужно и как ставится

- **Cloudflare Workers Paid ($5/мес)** — обязателен для Sandbox-контейнеров.
- **LLM-ключ:** Anthropic (Claude) напрямую **или** Cloudflare AI Gateway с ключом апстрим-провайдера.
- **Опционально:** R2 (персистентность), Cloudflare Access (аутентификация).

```bash
# после настройки wrangler и секретов
npm run deploy      # = wrangler deploy: поднимает Linux-контейнер с OpenClaw + (опц.) web-UI
```

## 🖥️ Применимость на системах владельца

Сам деплой идёт **в облако Cloudflare** — локальная ОС нужна лишь для запуска `wrangler` (Node.js):

| Система | Роль |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ставишь Node + `wrangler`, деплоишь; всё исполняется у Cloudflare, не на твоём железе |
| **Entware / RT-AX56U** | ➖ роутер не при чём: вычисления в облаке, а `wrangler` удобнее с десктопа |

> [!tip] Альтернатива без облачных счетов
> Если цель — «свой ИИ-ассистент без мощного ПК», взвесь: Moltworker перекладывает железо на Cloudflare, но платишь **подписку + токены LLM**. Для приватного/бесплатного варианта на своём железе смотри локальный стек ([Ollama](../../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)) — там нет ежемесячной платы, но нужен свой GPU/CPU.

## 🔗 Связанные заметки

- Локальный LLM-бэкенд (альтернатива облачным счетам): [Ollama](../../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)
- Другое self-hosted пространство для людей и ИИ-агентов (тоже «сырое»): [BUZZ (Block)](BUZZ%20%28Block%29%20%E2%80%94%20self-hosted%20%D1%80%D0%B0%D0%B1%D0%BE%D1%87%D0%B5%D0%B5%20%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%81%D1%82%D0%B2%D0%BE%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9%20%D0%B8%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%BD%D0%B0%20Nostr%20%28%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B9%20%D1%81%20%D0%BC%D0%B0%D1%80%D1%82%D0%B0%2C%20README%20%D1%81%D0%B0%D0%BC%20%D0%BF%D0%B8%D1%88%D0%B5%D1%82%20%C2%ABnot%20finished%C2%BB%29.md)
- Кодинг-агенты (для сравнения — OpenClaw не про код): [Сводная таблица AI-агентов](../%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/cloudflare/moltworker](https://github.com/cloudflare/moltworker) (Apache-2.0, TypeScript) — «Run OpenClaw (formerly Moltbot, formerly Clawdbot) on Cloudflare Workers»
- Источник новости: [@CodeGuard](https://t.me/c/2675453029/1405)

#AI #Agents #Cloudflare #SelfHosted #OpenClaw #ClaudeAPI #Инструменты
