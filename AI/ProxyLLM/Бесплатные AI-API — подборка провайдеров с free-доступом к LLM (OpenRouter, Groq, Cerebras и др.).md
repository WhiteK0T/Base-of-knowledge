---
создал заметку: 2026-07-10T18:00:00
author: WhiteK0T
tags:
  - LLM
  - API
  - Free
  - Proxy
  - AI
Источник:
  - https://t.me/bugnotfeature/26319
---

# 🎁 Бесплатные AI-API — подборка провайдеров с free-доступом к LLM

Из канала «Не баг, а фича» — подборка сервисов, дающих **бесплатные токены** к разным моделям для своих ИИ-проектов. В отличие от браузер-хаков вроде [FreeQwenApi](FreeQwenApi%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20Qwen%20Chat.md)/[FreeDeepseekAPI](FreeDeepseekAPI%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20DeepSeek.md) — это **официальные** free-tier'ы, не нарушающие ToS. Почти все дают **OpenAI-совместимый** эндпоинт (`/v1`), так что подключаются одной заменой `base_url` в LiteLLM, Claude Code, OpenAI SDK.

> [!warning] Что такое «бесплатно» на самом деле
> Это **rate-limited eval/prototype-тиры**, а не бесплатный прод: жёсткие лимиты по запросам/токенам в минуту и в день. **Лимиты часто меняются** — цифры ниже сняты на **10.07.2026**, сверяйся с официальными страницами. На free-тирах провайдер нередко **использует твои запросы для улучшения моделей** — не слать чувствительное. Часть требует телефон/карту при регистрации и может **гео-блокировать РФ** (нужен способ доступа/регистрации).

## 📊 Провайдеры (снимок на 10.07.2026)

| Сервис | Что даёт | Free-лимит | OpenAI-`/v1` | Нюанс |
| :--- | :--- | :--- | :--- | :--- |
| **[OpenRouter](https://openrouter.ai/)** | Агрегатор 300+ моделей одним ключом; есть слоты `:free` (Llama, DeepSeek, Qwen и др.) | ~20 req/min; ~50 req/day (до ~1000/day при депозите $10) | ✅ | Единый ключ ко всему; удобно как «единая точка». См. [OpenRouter Fusion](OpenRouter%20Fusion%20%E2%80%94%20%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B5%D0%B9%20%2B%20%D1%81%D1%83%D0%B4%D1%8C%D1%8F%20%28%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D0%B8-LLM%20%D1%81%D0%B8%D0%BD%D1%82%D0%B5%D0%B7%29.md) |
| **[Cerebras](https://cloud.cerebras.ai/)** | Ультрабыстрый инференс (Llama, Qwen) ~2600 tok/s | **1 000 000 токенов/день**, без карты; 30 req/min, ~60k tok/min | ✅ `api.cerebras.ai/v1` | Самый щедрый по объёму; временный потолок контекста **8192** на free |
| **[Groq](https://console.groq.com/)** | Быстрый LPU-инференс (Llama и др.) | 30 req/min, 6 000 tok/min, ~1 000 req/day (у мелких моделей вроде Llama 3.1 8B — до 14 400/day) | ✅ `api.groq.com/openai/v1` | Отличная скорость; нужен телефон при регистрации |
| **[NVIDIA NIM](https://build.nvidia.com/)** | Каталог моделей (Llama, Nemotron, и др.) для оценки | Пробные кредиты/лимитированные запросы | ✅ `integrate.api.nvidia.com/v1` | Для evaluation; удобный playground |
| **[Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai)** | ~47 моделей на edge | **10 000 Neurons/день** (сброс 00:00 UTC) | ✅ (есть OpenAI-совм. эндпоинт) | «Neuron» — расчётная единица; удобно для Workers/edge |
| **[Mistral AI](https://console.mistral.ai/)** | Свои модели (Mistral, Codestral и др.) | Бесплатный экспериментальный тир La Plateforme, rate-limited | ✅ | Хорош для своих моделей Mistral |
| **[Hugging Face Inference Providers](https://huggingface.co/inference-api)** | Роутер к куче провайдеров/моделей | Небольшой месячный кредит для залогиненных | ✅ `router.huggingface.co/v1` | Единый роутер поверх многих бэкендов |
| **[GitHub Models](https://github.com/models)** | GPT-4o, Claude, Llama, Phi для прототипов | high-tier 50 req/day (10/min), mini 150/day; 8k in / 4k out | ✅ (Azure-эндпоинт) | ⚠️ **Закрывается 30.07.2026** — не строить на нём |

> [!caution] GitHub Models уходит 30 июля 2026
> Пост рекомендует GitHub Models, но сервис **полностью выключают 30.07.2026** (через считанные недели после этой заметки). Использовать как временный playground ещё можно, но **закладываться в проекты — нельзя**; мигрируй на другие пункты списка.

## 🧩 Как этим пользоваться в связке

- **Единый шлюз.** Не жонглируй ключами вручную — подними [LiteLLM](LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md): он объединяет все эти провайдеры за одним OpenAI-совместимым эндпоинтом, умеет фолбэк и балансировку между free-тирами (упёрся в лимит Groq → ушёл на Cerebras).
- **Claude Code / OpenAI SDK.** Большинство подключается заменой `base_url` + свой ключ; удобно гонять дешёвые задачи на free-моделях.
- **Дополняет локальный запуск.** Когда локальной [Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) не хватает мощности/скорости — free-API (Cerebras/Groq) дают быстрый доступ к крупным моделям, а приватные данные всё равно держишь на локальной.

## 🖥️ По системам

Это **облачные API** — ОС-агностичны, работают через `curl`/любой HTTP-клиент на Gentoo/Debian/Arch одинаково. На роутере **RT-AX56U** тоже можно дёргать (лёгкий `curl`-запрос), но осмысленно — как прокси/оркестрация, а не инференс.

## 🔗 Ссылки

- Провайдеры: [OpenRouter](https://openrouter.ai/) · [NVIDIA NIM](https://build.nvidia.com/) · [GitHub Models](https://github.com/models) · [Cerebras](https://cloud.cerebras.ai/) · [Groq](https://console.groq.com/) · [Mistral](https://console.mistral.ai/) · [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai) · [HF Inference](https://huggingface.co/inference-api)
- Курируемые списки: [awesome-free-llm-apis](https://github.com/amardeeplakshkar/awesome-free-llm-apis) · сравнение: [OpenRouter blog](https://openrouter.ai/blog/tutorials/free-llm-apis-compared/)
- Источник новости: [@bugnotfeature/26319](https://t.me/bugnotfeature/26319)
- Связанные: [LiteLLM (единый шлюз к 100+ LLM)](LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md) · [FreeQwenApi](FreeQwenApi%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20Qwen%20Chat.md) · [FreeDeepseekAPI](FreeDeepseekAPI%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20DeepSeek.md) · [92 AI-сервиса — шпаргалка по назначению](../92%20AI-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%B0%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BF%D0%BE%20%D0%BD%D0%B0%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8E%20%28%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%29.md)

#LLM #API #Free #Proxy #AI
