---
создал заметку: 2026-06-22T17:00:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - Qwen
  - LocalLLM
  - Uncensored
  - GGUF
Источник:
  - https://t.me/bugnotfeature/26008
  - https://huggingface.co/empero-ai/Qwythos-9B-Claude-Mythos-5-1M
---

# 🐉 Qwythos-9B-Claude-Mythos-5-1M — расцензуренный файнтюн Qwen3.5-9B на трейсах Claude (1M контекст)

**Qwythos-9B-Claude-Mythos-5-1M** (`empero-ai` на Hugging Face) — **полнопараметрический файнтюн `Qwen/Qwen3.5-9B`**, дообученный на **500M+ токенов** «трейсов Claude Mythos и Claude Fable» + собственного chain-of-thought (инструмент `rethink` от Empero). Заявлен **расцензуренным**, с **контекстом до 1M токенов** (через YaRN-масштабирование), в **safetensors** + 11 квантизаций (GGUF и др.). Лицензия — **Apache-2.0** (унаследована от базового Qwen3.5-9B). По сути — близкий родственник заметок про [Gemma 4 12B Coder](Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md) и её [abliterated-версию](Huihui%20Gemma%204%2012B%20Coder%20%28abliterated%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20Gemma%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205.md), только на базе Qwen.

> [!warning] Факты против хайпа: это Qwen3.5-9B, а не «китайский Claude/Mythos»
> Пост: «китайцы дропнули свой Mythos… обучили на Claude Mythos и Claude Fable… без цензуры… сделает ЛЮБУЮ задачу». Разбираем:
> - Скачивается **Qwen3.5-9B** от Alibaba, дообученный на **синтетических трейсах** Claude-семейства — это **не веса Claude** и не его качество. Та же подмена понятий, что в [базовой Gemma-заметке](Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md): 9B-модель *переняла стиль*, но не уровень флагмана.
> - «Сделает ЛЮБУЮ задачу» — маркетинг расцензуривания: снятие отказов **не добавляет знаний и не повышает потолок** 9B-модели.

> [!caution] Бенчмарки самозаявленные — и базовый baseline выглядит аномально
> Карточка хвалит «+34.3 MMLU (0.232 → 0.575)» и «+30 GSM8K». Но **MMLU базового Qwen3.5-9B = 0.232** — это **уровень случайного угадывания** (~0.25 на 4 вариантах). Настоящий Qwen такого класса даёт 0.6+. Значит, «базу» мерили в сломанном/без-форматном режиме, и гигантский «прирост» — скорее **артефакт методики замера**, чем реальный скачок. Воспринимай цифры скептически, проверяй на своих задачах.

## 🧬 Что это по фактам

| Параметр | Значение |
| :--- | :--- |
| Базовая модель | **Qwen/Qwen3.5-9B** (Alibaba) |
| Кто сделал | **Empero AI** (`empero-ai`) |
| Метод | **полный SFT** (TRL, assistant-only loss: промпт маскируется, считается только ответ) |
| Данные | **500M+ токенов** трейсов «Claude Mythos / Claude Fable» + свой CoT (`rethink`), нормализовано в chat-формат Qwen3.5 |
| Контекст | **1 048 576 (1M)** — но через **YaRN rope-scaling ×4** поверх нативных **262k** (не «настоящий» 1M) |
| Формат | **safetensors** + **11 квантов** (GGUF и пр.) |
| Лицензия | **Apache-2.0** (от базы Qwen3.5-9B) |
| Скачиваний | **~1.86k / месяц** (на 22.06.2026) |

> [!note] Про «1M контекст»
> 1M включён **экстраполяцией** (YaRN ×4) от нативных 262k — без дообучения на такой длине. На сверхдлинном контексте качество обычно **деградирует**, а KV-кэш на 1M токенов требует **колоссум RAM/VRAM**. Реально рассчитывай на разумные десятки-сотни тысяч токенов, а не на честный миллион.

## 🚀 Как запустить

Движки и кванты — те же, что для других GGUF-моделей; подробности в [Gemma 4 12B Coder](Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md) (Gentoo/Debian/Ubuntu/Arch; Entware/RT-AX56U — **N/A**, 9B на роутер не влезет). 9B заметно **легче** 12B Gemma — комфортно идёт на десктопе.

```bash
# llama.cpp — взять GGUF-квант с HF (ищи репозиторий empero-ai с -GGUF)
llama-cli  -hf empero-ai/Qwythos-9B-Claude-Mythos-5-1M-GGUF:Q4_K_M
llama-server -hf empero-ai/Qwythos-9B-Claude-Mythos-5-1M-GGUF:Q4_K_M --ctx-size 8192 --port 8080

# Ollama
ollama run hf.co/empero-ai/Qwythos-9B-Claude-Mythos-5-1M-GGUF:Q4_K_M
```

> [!tip] Квант и контекст
> Для 9B на десктопе **Q4_K_M** — золотая середина (~5–6 ГБ). Контекст ставь по памяти: 1M в `--ctx-size` съест неадекватно много KV-кэша; начни с 8–32k.

## 🛡️ Безопасность и право

> [!danger] Намеренно расцензурена — guardrails на тебе
> Карточка прямо заявляет: модель **специально без цензуры**, «предметно отвечает» по кибербезопасности, фармакологии и клинической медицине вместо отказа. Как и [Heretic](../Heretic%20%E2%80%94%20%D1%81%D0%BD%D1%8F%D1%82%D0%B8%D0%B5%20safety-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D1%81%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D1%85%20LLM%20%28abliteration%29.md)/[Huihui-Gemma](Huihui%20Gemma%204%2012B%20Coder%20%28abliterated%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20Gemma%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205.md), это **dual-use**: годится для red-team/исследований, но в продакшн/публичные сценарии — только со своим слоем модерации. Карточка же отмечает, что модель «**может слишком уверенно называть конкретные идентификаторы**» — в критичных задачах **перепроверяй факты**.

> [!warning] Лицензия чище, чем у Gemma, но дистилляция — серая зона
> База Qwen3.5-9B действительно **Apache-2.0** (в отличие от Gemma Terms). Но обучение на **трейсах Claude-семейства** — спорный момент: условия многих провайдеров **запрещают тренировать конкурирующие модели на их выводах**. Для личных экспериментов — ок, для продукта оценивай риски (как в [базовой Gemma-заметке](Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md)).

## 💡 Стоит ли смотреть

- **Да**, если нужен **лёгкий локальный** (9B) ассистент без лишних отказов и ты сам ставишь guardrails; Qwen-база — хорошая основа.
- **Скептически** к «это Claude/Mythos», к «1M контексту» (экстраполяция) и к самозаявленным бенчмаркам (странный baseline).
- Хочешь **расцензуривание поаккуратнее** — [Heretic](../Heretic%20%E2%80%94%20%D1%81%D0%BD%D1%8F%D1%82%D0%B8%D0%B5%20safety-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D1%81%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D1%85%20LLM%20%28abliteration%29.md); другую расцензуренную модель — [Huihui Gemma](Huihui%20Gemma%204%2012B%20Coder%20%28abliterated%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20Gemma%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205.md); готовую студию с GUI — [LocallyUncensored](../Local-LLM/LocallyUncensored%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20AI-%D1%81%D1%82%D1%83%D0%B4%D0%B8%D1%8F%20%28%D1%87%D0%B0%D1%82%2C%20%D0%BA%D0%BE%D0%B4%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%29.md).

## 🔗 Ссылки

- Модель: [huggingface.co/empero-ai/Qwythos-9B-Claude-Mythos-5-1M](https://huggingface.co/empero-ai/Qwythos-9B-Claude-Mythos-5-1M)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26008)
- Связанные: [Gemma 4 12B Coder (база)](Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md) · [Huihui Gemma (abliterated)](Huihui%20Gemma%204%2012B%20Coder%20%28abliterated%29%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20Gemma%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205.md) · [Heretic — abliteration](../Heretic%20%E2%80%94%20%D1%81%D0%BD%D1%8F%D1%82%D0%B8%D0%B5%20safety-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D1%81%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D1%85%20LLM%20%28abliteration%29.md) · [FreeQwenApi — бесплатный API к Qwen](../ProxyLLM/FreeQwenApi%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20OpenAI-%D1%81%D0%BE%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B8%D0%BC%D1%8B%D0%B9%20API%20%D0%BA%20Qwen%20Chat.md) · [LocallyUncensored](../Local-LLM/LocallyUncensored%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20AI-%D1%81%D1%82%D1%83%D0%B4%D0%B8%D1%8F%20%28%D1%87%D0%B0%D1%82%2C%20%D0%BA%D0%BE%D0%B4%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%29.md)

#AI #LLM #Qwen #LocalLLM #Uncensored #GGUF
