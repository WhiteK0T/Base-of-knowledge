---
создал заметку: 2026-06-19T13:00:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - Кодинг
  - Cohere
  - LocalLLM
  - OpenSource
  - MoE
Источник:
  - https://t.me/johenews/2129
  - https://huggingface.co/CohereLabs/North-Mini-Code-1.0
  - https://cohere.com/blog/north-mini-code
  - https://huggingface.co/blog/CohereLabs/introducing-north-mini-code
---

# 🧭 North Mini Code 1.0 — открытая 30B-A3B модель для агентского кодинга (Cohere)

**Cohere** (через [Cohere Labs / C4AI](https://huggingface.co/CohereLabs/North-Mini-Code-1.0)) выпустила (9 июня 2026) **North Mini Code 1.0** — открытую модель **специально под программирование**: написание кода, **агентскую инженерию** (agentic software engineering) и задачи в терминале. Это первая модель новой линейки **North** и первая «для разработчиков» у Cohere. Архитектура — **sparse MoE 30B с ~3B активных** (30B-A3B), под **Apache 2.0**, влезает на **один H100 в FP8**. Повод для заметки — пост [@johenews](https://t.me/johenews/2129), который честно отмечает: на [LiveCodeBench v6](LiveCodeBench%20v6%20%E2%80%94%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D1%83%D1%82%D0%B5%D1%87%D0%B5%D0%BA%20%28%D0%BB%D0%B8%D0%B4%D0%B5%D1%80%D0%B1%D0%BE%D1%80%D0%B4%20llm-stats%29.md) она набирает скромные **0.703**.

> [!warning] Отделяем факты от хайпа — главное противоречие
> Пост видит «парадокс»: North Mini Code на **LiveCodeBench v6 = 0.703** проигрывает даже куда меньшей по «ощущению» Qwen3.6-27B (**0.839**) и Qwen3.6-35B-A3B (**0.804**). Но Cohere в карточке хвалит её **сильными** числами — **SWE-Bench Verified 67.6**, SWE-Bench Pro 40.2, Terminal-Bench v2 36.
> **Это не противоречие, а разные бенчмарки про разное:**
> - **LiveCodeBench v6** — *соревновательные одиночные задачки* (LeetCode/AtCoder/CF), чистый алгоритмический reasoning «в один проход».
> - **SWE-Bench / Terminal-Bench** — *агентская работа в реальном репозитории*: много шагов, инструменты, правка файлов, прогон тестов.
> North Mini Code **затачивали под второе** (она прямо позиционируется как **кодинг-субагент** под оркестратором, а не как чемпион олимпиад). Поэтому «слабый LiveCodeBench» ≠ «плохая модель» — он просто меряет не её сильную сторону. Вывод поста «вряд ли буду использовать» справедлив, **если тебе нужен именно competitive-coding**; для agentic-сценария метрика другая.

> [!info] Про «количество параметров не значит ничего» — поправка
> В посте верная мысль: **число параметров само по себе не предсказывает качество** (Qwen3.5-122B-A10B 0.789 хуже Qwen3.6-27B 0.839 — новее поколение + лучше данные/обучение бьют размер). Но не «параметры неважны вообще»: при **прочих равных** (то же поколение, те же данные) больше параметров обычно лучше. Важно сравнивать **в рамках одного поколения** и помнить, что **A3B активных** даёт скорость инференса уровня ~3B-модели при «знаниях» ближе к 30B.

## 🧬 Что это по фактам

| Параметр | Значение |
| :--- | :--- |
| Полное имя | **CohereLabs/North-Mini-Code-1.0** |
| Разработчик | **Cohere / Cohere Labs (C4AI)**, Канада |
| Архитектура | decoder-only **sparse MoE**, 128 экспертов (8 активны/токен), SwiGLU, interleaved sliding-window + global attention (3:1) |
| Параметров | **30B всего / ~3B активных** (30B-A3B) |
| Контекст | **256K вход / 64K выход** |
| Лицензия | **Apache 2.0** ✅ (свободная, коммерчески пригодная) |
| Фокус | кодинг, **агентская инженерия**, терминал, tool use, interleaved thinking |
| Обучение | каскадный SFT в 2 стадии + **RLVR** (RL с проверяемыми наградами) |
| Железо | **1× H100 в FP8**; есть **GGUF-кванты** (llama.cpp, LM Studio, Jan, Ollama) |

> [!tip] Apache 2.0 — это для Cohere заметный сдвиг
> Исторически Cohere отдавала открытые веса (линейка **Command/Aya**) под **некоммерческой** CC-BY-NC research-лицензией. North Mini Code под **Apache 2.0** — то есть можно использовать коммерчески и встраивать без NC-ограничений. Это редкость для Cohere и плюс к её привлекательности.

## 📊 Бенчмарки (как читать)

| Бенчмарк | Балл | Что меряет |
| :--- | :--- | :--- |
| **SWE-Bench Verified** | **67.6** (pass@1, SWE-Agent harness) | агентская правка реальных репозиториев — **сильная сторона** |
| **SWE-Bench Pro** | 40.2 | более сложный агентский набор |
| **Terminal-Bench v2** | 36 | задачи в терминале/окружении |
| **LiveCodeBench v6** | **0.703** | соревновательный одиночный кодинг — **слабее**, чем у топ-Qwen/GLM |

> [!note] Заявленные числа — от вендора
> SWE/Terminal-числа — из карточки Cohere (self-reported), как и почти везде. Cohere также заявляет **×2.8 throughput** и **~30% ниже latency** против Devstral Small 2 на том же железе. Проверяй на своей задаче, а не по одной строке. Подробнее про оговорки лидербордов — в заметке про [LiveCodeBench v6](LiveCodeBench%20v6%20%E2%80%94%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D1%83%D1%82%D0%B5%D1%87%D0%B5%D0%BA%20%28%D0%BB%D0%B8%D0%B4%D0%B5%D1%80%D0%B1%D0%BE%D1%80%D0%B4%20llm-stats%29.md).

## 🚀 Запуск локально

**A3B активных** = инференс быстрый (как у ~3B), но в память нужно поднять **все 30B весов**. В GGUF это реально на десктопе с достаточным RAM/VRAM; на сервере — 1× H100 FP8. Движки и подробности — в отдельных заметках: [llama.cpp](../Local-LLM/llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) · [Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) · [LM Studio](../Local-LLM/LM%20Studio%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF-GUI%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md).

```bash
# llama.cpp — взять community-GGUF прямо с HF (подставь нужный квант, напр. Q4_K_M)
llama-server -hf bartowski/CohereLabs_North-Mini-Code-1.0-GGUF:Q4_K_M \
  --ctx-size 16384 --port 8080         # OpenAI-совместимый сервер на :8080

# Ollama
ollama run hf.co/<репозиторий-с-GGUF>:Q4_K_M
```

> [!caution] Имя GGUF-репозитория уточни
> Квантизации выкладывает сообщество (на момент новости упоминается ~31 сборка). Точное имя репозитория (bartowski / unsloth / сам CohereLabs) проверь поиском по HF — оно могло отличаться. К размеру файла добавляй запас RAM на KV-кэш под нужный контекст.

Полученный OpenAI-совместимый эндпоинт можно завести в общий стек через [LiteLLM](../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md) и дёргать из агентов/Claude-Code-совместимых клиентов.

## 💡 Кому стоит смотреть

- **Да**, если нужен **открытый (Apache 2.0) локальный кодинг-субагент** под agentic-сценарий (правка репо, терминал) на дешёвом фиксированном железе — её под это и делали.
- **Скептически**, если задача — **соревновательный/алгоритмический** кодинг «в один проход»: тут открытые Qwen3.6-27B/35B-A3B и GLM по LiveCodeBench v6 сейчас впереди.
- **Плюс экосистеме:** хорошо, что сильные открытые кодинг-модели делает не только Alibaba/Google, но и Cohere — и сразу под свободной лицензией.
- Для сравнения с другими открытыми кодинг-LLM — [GLM 5.2](../GLM%205.2%20%E2%80%94%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%B0%D1%8F%20%D0%BA%D0%B8%D1%82%D0%B0%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20LLM%20%28Z.ai%2C%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3%29.md), [Gemma 4 12B Coder](Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md) и [сводная таблица AI-агентов](../%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B8%D1%8E%D0%BD%D1%8C%202026%29.md).

## 🔗 Ссылки

- Модель: [huggingface.co/CohereLabs/North-Mini-Code-1.0](https://huggingface.co/CohereLabs/North-Mini-Code-1.0)
- Анонс: [cohere.com/blog/north-mini-code](https://cohere.com/blog/north-mini-code) · [HF-блог](https://huggingface.co/blog/CohereLabs/introducing-north-mini-code)
- Источник новости: [@johenews](https://t.me/johenews/2129)
- Связанные: [LiveCodeBench v6 (бенчмарк + лидерборд)](LiveCodeBench%20v6%20%E2%80%94%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3%D0%B0%20%D0%B1%D0%B5%D0%B7%20%D1%83%D1%82%D0%B5%D1%87%D0%B5%D0%BA%20%28%D0%BB%D0%B8%D0%B4%D0%B5%D1%80%D0%B1%D0%BE%D1%80%D0%B4%20llm-stats%29.md) · [GLM 5.2](../GLM%205.2%20%E2%80%94%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%B0%D1%8F%20%D0%BA%D0%B8%D1%82%D0%B0%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20LLM%20%28Z.ai%2C%20%D0%BA%D0%BE%D0%B4%D0%B8%D0%BD%D0%B3%29.md) · [Gemma 4 12B Coder (GGUF)](Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md) · [Сводная таблица AI-агентов](../%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B8%D1%8E%D0%BD%D1%8C%202026%29.md) · [LiteLLM (шлюз к LLM)](../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md)

#AI #LLM #Кодинг #Cohere #LocalLLM #OpenSource #MoE
