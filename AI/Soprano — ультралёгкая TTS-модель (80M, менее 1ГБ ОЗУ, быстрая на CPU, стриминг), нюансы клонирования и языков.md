---
создал заметку: 2026-07-24T22:40:00
author: WhiteK0T
tags:
  - AI
  - TTS
  - СинтезРечи
  - Локально
  - OpenSource
  - Инструменты
Источник:
  - https://t.me/bugnotfeature/26540
  - https://github.com/ekwek1/soprano
  - https://huggingface.co/ekwek/Soprano-1.1-80M
---

# 🗣️ Soprano — ультралёгкая TTS-модель (синтез речи на CPU)

**Soprano** ([github.com/ekwek1/soprano](https://github.com/ekwek1/soprano)) — компактная **модель синтеза речи (text-to-speech)** на **80 млн параметров**, которая работает **локально, на CPU и в <1 ГБ ОЗУ**, но при этом быстрая и с потоковой отдачей. Apache-2.0, ~1350★, Python. Модель, демо и веса — на Hugging Face ([Soprano-1.1-80M](https://huggingface.co/ekwek/Soprano-1.1-80M), [демо-Space](https://huggingface.co/spaces/ekwek/Soprano-TTS)).

> [!info] Сверка поста с репозиторием — цифры реальные
> | Заявление поста | Реально (README) |
> | :--- | :--- |
> | «до 20× быстрее реального времени на CPU, до 2000× на GPU» | ✅ так и заявлено. Но **2000×** — «при достаточно длинном входе» (амортизация/батчинг), не универсальный множитель на любую фразу |
> | «работает на 1 ГБ ОЗУ» | ✅ **<1 ГБ**, 80M-архитектура |
> | «потоковая озвучка с низкой задержкой» | ✅ стриминг **<250 мс на CPU**, **<15 мс на GPU** |
> | «32 кГц, выразительно» | ✅ 32 кГц (не студийные 48 кГц, но чисто) |
> | «длинные тексты без ограничений» | ✅ авто-разбиение текста, «infinite length» |
> | «Windows/Linux/macOS, CPU/CUDA/Apple Silicon» | ✅ CUDA/CPU/MPS; интерфейсы: WebUI, CLI, **OpenAI-совместимый эндпоинт**, ONNX, ComfyUI, Python API |

> [!caution] «Клонирование» — это дообучение, а не «10 секунд и готово»
> Пост подаёт «клонирование голоса». По факту в репо это **train/fine-tune** через **отдельный проект [soprano-factory](https://github.com/ekwek1/soprano-factory)**: ты **дообучаешь модель на своих записях или под новый язык**. Это **не zero-shot клонирование** (как у XTTS/ElevenLabs, где хватает пары секунд референса) — нужны **датасет, время и вычисления на тренировку**. Совсем другой уровень усилий.

> [!warning] Язык — английский; готового русского нет
> Модель и все примеры — **англоязычные**; 80M-модель обучена под английский. **Русского из коробки нет** — чтобы озвучивать РФ-тексты, придётся **самому обучать/дообучать** голос и язык через soprano-factory (датасет + тренировка). Для быстрого RU-TTS это не готовое решение.

> [!note] Не «свежак» — проект притормозил
> Несмотря на подачу «нашли новинку», последний релиз/коммит основного репо — **январь 2026** (Soprano-1.1-80M, 14.01.2026), дальше активность заглохла. Модель рабочая, но **актуальность обновлений проверяй** — полгода без движения.

## 🛠️ Установка и использование

```bash
pip install soprano-tts            # CPU / Apple Silicon (MPS)
pip install soprano-tts[lmdeploy]  # CUDA (быстрый backend)

soprano "Soprano is an extremely lightweight text to speech model."   # CLI
soprano-webui                      # WebUI на http://127.0.0.1:7860
uvicorn soprano.server:app --port 8000   # OpenAI-совместимый /v1/audio/speech
```

```python
from soprano import SopranoTTS
model = SopranoTTS(backend='auto', device='auto')
model.infer("Hello from Soprano.", "out.wav")
```

> На Windows+CUDA `pip` ставит CPU-сборку PyTorch — после установки переустанови torch с нужным CUDA-колесом (в README есть команда).

## 🖥️ Применимость на системах владельца

Локальная модель — крутится на CPU/GPU десктопа:

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ идеально: `pip install soprano-tts`; на CPU уже быстро, с NVIDIA — `[lmdeploy]`. OpenAI-совместимый эндпоинт удобно дёргать из своих скриптов |
| **Entware / RT-AX56U** | ❌ несмотря на «1 ГБ»: у роутера **512 МБ ОЗУ** и **armv7**, плюс Python/PyTorch-стек под него не рассчитан. Гоняй на десктопе/мини-ПК; роутер не потянет |

## 🔗 Связанные заметки

- Каталог всего для локального ИИ (там же раздел audio/TTS): [LLMs-local — awesome-каталог](Local-LLM/LLMs-local%20%E2%80%94%20awesome-%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%B2%D1%81%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0%20%D0%98%D0%98%20%28%D0%B4%D0%B2%D0%B8%D0%B6%D0%BA%D0%B8%2C%20UI%2C%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20RAG%2C%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%BE%2C%20%D0%B3%D0%B0%D0%B9%D0%B4%D1%8B%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/ekwek1/soprano](https://github.com/ekwek1/soprano) · Тренировка/файнтюн: [soprano-factory](https://github.com/ekwek1/soprano-factory) · Модель: [HF Soprano-1.1-80M](https://huggingface.co/ekwek/Soprano-1.1-80M) · [Демо](https://huggingface.co/spaces/ekwek/Soprano-TTS)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26540)

#AI #TTS #СинтезРечи #Локально #OpenSource #Инструменты
