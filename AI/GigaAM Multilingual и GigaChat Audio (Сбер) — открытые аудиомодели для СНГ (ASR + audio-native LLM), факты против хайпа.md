---
создал заметку: 2026-07-25T03:05:00
author: WhiteK0T
tags:
  - AI
  - Аудио
  - ASR
  - РаспознаваниеРечи
  - Sber
  - GigaChat
  - OpenSource
  - Модель
Источник:
  - https://t.me/black_triangle_tg/9164
  - https://huggingface.co/ai-sage/GigaAM-Multilingual
  - https://github.com/salute-developers/GigaAM
  - https://arxiv.org/abs/2607.10371
---

# 🎙️ GigaAM Multilingual и GigaChat Audio — открытые аудиомодели Сбера

Сбер (команда **ai-sage / salute-developers**) выложил в опенсорс **две аудиомодели** под **MIT** на Hugging Face и GitHub:
- **GigaAM Multilingual** — мультиязычная модель **распознавания речи (ASR)** с фокусом на языки СНГ.
- **GigaChat Audio** — **audio-native LLM** (понимает аудио напрямую, без предварительной транскрибации).

Это реально заметный релиз для русского/СНГ-сегмента: открыто, MIT (можно коммерчески), с научной статьёй ([arXiv 2607.10371](https://arxiv.org/abs/2607.10371)). Репозиторий [salute-developers/GigaAM](https://github.com/salute-developers/GigaAM) — MIT, Python, ~700★.

> [!warning] Пост местами преувеличивает и путает цифры — что реально по карточкам моделей
> | Заявление поста | Реально (Hugging Face / arXiv) |
> | :--- | :--- |
> | «компактная версия на **240 млн** параметров» | ❌ **220M** (и Large — **600M**). 240 — округление мимо. Варианты: `ssl`/`ctc` 220M, `large_ssl`/`large_ctc` 600M |
> | «обгоняет **Whisper Large v3 и Omnilingual 1B**» | ⚠️ **только на языках СНГ** (русский, казахский, киргизский, узбекский) — там разгром. Но **на английском — нет**: карточка прямо пишет «moderate quality on English», Whisper/Seamless по English впереди. Это **чемпион для СНГ-языков, а не универсальный** |
> | «ошибок в **1,5–2 раза меньше**, чем у аналогов» | 🟡 по СНГ-языкам правдоподобно (см. таблицу WER), но это **заявление Сбера**; на русском/казахском/киргизском/узбекском отрыв большой, на английском обратная картина |
> | «поддерживает русский, английский, казахский, киргизский, узбекский» | ✅ да — **5 языков** для ASR. «70+ языков» — это только **предобучение энкодера** (2 млн ч), а не поддерживаемый вывод |
> | ссылка на статью в посте `arxiv 2607.10387` | ⚠️ у поста **битая/неточная**; корректная статья — **2607.10371** |

> [!info] GigaChat Audio — сильные заявления, но бенчмарки в основном ВНУТРЕННИЕ
> Пост: «эмоции с точностью 80% (Qwen3-Omni-30B — 70%, Kimi-Audio — 62%)», «Arena Hard Audio 75% побед, опередив Gemini 2.5 Pro (62%)», «до 3 часов», «диаризация», «поиск по аудио с таймкодами».
> - **Диаризация, длинное аудио, temporal grounding (таймкоды), эмоции** — реальные заявленные способности (модель `GigaChat3.1-Audio-10B-A1.8B`, MoE поверх GigaChat 3.1 Lightning; датасет TimeGround-1M).
> - **НО**: «Arena Hard Audio» и большая часть цифр — **собственные/внутренние тесты Сбера** («по внутренним тестам» — это и в посте). На **публичных** бенчмарках картина скромнее: по карточке на MMAU (62.2) и MMLU-speech (50.3) модель **уступает Qwen3-Omni-30B** (74.7 / 72.2). Её сила — **русский (RuBQ), эмоции на русских датасетах (Dusha) и temporal localization**, а не универсальное превосходство. Независимой проверки пока нет — относись как к вендорским цифрам.

## 📊 Что реально показывает таблица WER (GigaAM Multilingual)

По карточке (WER %, меньше — лучше; Common Voice / FLEURS / внутренний):
- **Русский, казахский, киргизский, узбекский** — GigaAM (и особенно Large 600M) **уверенно лучше** Whisper Large v3, Omnilingual 1B, Seamless M4T v2. На казахском/киргизском/узбекском Whisper вообще разваливается (WER 60–120%).
- **Английский** — GigaAM **проигрывает**: на FLEURS 12.2 против 3.9 у Whisper. Английский у модели «средний».

Вывод: **это лучший открытый ASR для русского и языков СНГ** под MIT — но не «убийца Whisper» вообще; для английского Whisper/Seamless остаются сильнее.

## 🧩 Линейка и как запускать

| Модель | Что это | Размер |
| :--- | :--- | :--- |
| **GigaAM-Multilingual** (`ctc`) | ASR, компактный | **220M** |
| **GigaAM-Multilingual Large** (`large_ctc`) | ASR, точнее | **600M** |
| **GigaChat3.1-Audio-10B-A1.8B** | облегчённая audio-native LLM (MoE, активны ~1.8B) | 10B (A1.8B) |

```python
from transformers import AutoModel
model = AutoModel.from_pretrained(
    "ai-sage/GigaAM-Multilingual", revision="ctc", trust_remote_code=True)
print(model.transcribe("example.wav"))
```
Нужны `torch 2.10.*`, `torchaudio`, `transformers 5.*`. Есть [пример в colab](https://github.com/salute-developers/GigaAM) и гайд по дообучению энкодера на новый язык.

## 🖥️ Применимость на системах владельца

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ Python + PyTorch. **GigaAM 220M** — лёгкий, реально гонять и на CPU/скромной GPU для локальной транскрибации русского. **600M** — комфортнее с GPU. **GigaChat Audio 10B** (MoE) — уже нужна GPU/много RAM |
| **Entware / RT-AX56U** | ❌ PyTorch-модели на роутере (armv7, 512 МБ) не запустить — только как файловое хранилище/оркестрация к десктопу |

> [!tip] Тебе это практически полезно
> MIT-лицензия = можно использовать локально без облака и легально. Для **офлайн-транскрибации русской речи** (заметки, встречи, субтитры) GigaAM 220M — сильный локальный вариант, точнее Whisper на русском/СНГ и без отправки аудио на чужой сервер. Пара к твоей заметке про **синтез** речи (Soprano) — теперь есть и распознавание.

## 🔗 Связанные заметки

- Обратная задача — синтез речи (TTS): [Soprano — ультралёгкая TTS-модель](Soprano%20%E2%80%94%20%D1%83%D0%BB%D1%8C%D1%82%D1%80%D0%B0%D0%BB%D1%91%D0%B3%D0%BA%D0%B0%D1%8F%20TTS-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C%20%2880M%2C%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B5%201%D0%93%D0%91%20%D0%9E%D0%97%D0%A3%2C%20%D0%B1%D1%8B%D1%81%D1%82%D1%80%D0%B0%D1%8F%20%D0%BD%D0%B0%20CPU%2C%20%D1%81%D1%82%D1%80%D0%B8%D0%BC%D0%B8%D0%BD%D0%B3%29%2C%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B%20%D0%BA%D0%BB%D0%BE%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%B8%20%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%B2.md)
- Другая открытая модель Сбера в базе: [GFusion (диффузионная LLM Сбера)](Model/GFusion%20%E2%80%94%20%D0%BF%D0%B5%D1%80%D0%B2%D0%B0%D1%8F%20%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%B4%D0%B8%D1%84%D1%84%D1%83%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20LLM%20%28%D0%B1%D0%BB%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%B4%D0%B8%D1%84%D1%84%D1%83%D0%B7%D0%B8%D1%8F%20%D0%BD%D0%B0%20%D0%B1%D0%B0%D0%B7%D0%B5%20GigaChat3%2C%20Sber%29.md)

## 🔗 Ссылки

- ASR-модель: [huggingface.co/ai-sage/GigaAM-Multilingual](https://huggingface.co/ai-sage/GigaAM-Multilingual) · Audio-LLM: [GigaChat3.1-Audio-10B-A1.8B](https://huggingface.co/ai-sage/GigaChat3.1-Audio-10B-A1.8B)
- Код: [github.com/salute-developers/GigaAM](https://github.com/salute-developers/GigaAM) · Статья: [arXiv 2607.10371](https://arxiv.org/abs/2607.10371)
- Источник новости: [@black_triangle_tg](https://t.me/black_triangle_tg/9164)

#AI #Аудио #ASR #РаспознаваниеРечи #Sber #GigaChat #OpenSource #Модель
