---
создал заметку: 2026-07-10T14:00:00
author: WhiteK0T
tags:
  - Prompt
  - ChatGPT
  - ImageGeneration
  - PhotoRestoration
  - Privacy
Источник:
  - https://t.me/bugnotfeature/26283
---

# 🖼️ Промпт для реставрации и колоризации старых фото (ChatGPT)

Из канала «Не баг, а фича» разошёлся «ультимативный промпт для апскейла»: якобы в **ChatGPT** он повышает качество фото «вплоть до 4К» — убирает царапины, реставрирует и раскрашивает старые снимки. Промпт рабочий и даёт красивый результат, но формулировка «апскейл до 4К» вводит в заблуждение — разберём ниже, что происходит на самом деле.

## 📋 Промпт (копипаст)

Прикрепи фото в чат и вставь этот текст (на английском модель понимает точнее):

```text
Restore and enhance an old damaged photo. Remove scratches, stains, and noise.
Reconstruct faded or torn areas while preserving original details. Slightly sharpen
the image for better clarity, but keep it realistic. Apply natural and era-appropriate
colors to skin, hair, and clothing. Use a soft, balanced background color without being
too striking. The final result should look like an old photo that has been realistically
restored and colorized, while respecting its original appearance
```

**Что просим по пунктам:** убрать царапины/пятна/шум → восстановить выцветшие и порванные участки, **сохранив исходные детали** → аккуратно поднять резкость, но реалистично → наложить естественные, «по эпохе» цвета на кожу/волосы/одежду → мягкий сбалансированный фон → итог должен выглядеть как **реалистично отреставрированное** старое фото, уважающее оригинал.

## 🧪 Факты против хайпа

> [!warning] Это не «апскейл» и не «4К»
> ChatGPT не увеличивает разрешение существующих пикселей, как это делает upscaler. Модель генерации изображений (`gpt-image-1`) **создаёт новую картинку заново** по мотивам исходной. Отсюда следствия:
> - **Детали додумываются.** Мелочи (черты лица, надписи, узоры), которых не видно на оригинале, модель **дорисовывает по своим представлениям** — они могут не соответствовать реальности. Лицо человека может слегка «поплыть» и потерять сходство.
> - **Разрешение ограничено.** На выходе обычно ~1024 px по стороне (квадрат/портрет/альбом), а не 4К. «4К» — маркетинг поста.
> - **Не для документальной точности.** Для семейного архива «покрасивее» — отлично; для реставрации, где важна достоверность (лица, документы, улики), — нет.

> [!tip] Как повысить шанс на хороший результат
> - Добавь в промпт **«preserve the exact facial identity and features, do not alter the face»** — снижает «переизобретение» лица.
> - Работай **итеративно**: получил результат → «keep everything, but fix the left eye / make colors less saturated».
> - Грузи максимально **качественный скан** оригинала — чем больше исходных деталей, тем меньше модель выдумывает.

## 🔒 Приватность

> [!caution] Личные фото уходят в OpenAI
> Загружая семейные/личные снимки в ChatGPT, ты **отправляешь их на серверы OpenAI** (могут использоваться по их политике, если не отключён тренинг на данных). Для чувствительных фото лучше **локальные инструменты** ниже — они не отправляют ничего в облако и реально увеличивают разрешение.

## 🛠️ Настоящие инструменты (локально, без облака)

Если нужен **честный апскейл** и реставрация без «додумывания на чужом сервере»:

- **[Upscayl](https://github.com/upscayl/upscayl)** — open-source GUI-апскейлер (движок **Real-ESRGAN**), реально повышает разрешение ×2–×4. Кроссплатформенный.
- **Real-ESRGAN / GFPGAN** — CLI/модели: ESRGAN для общего апскейла, **GFPGAN**/**CodeFormer** — восстановление лиц.
- **[DeOldify](https://github.com/jantic/DeOldify)** — колоризация ч/б фото (то, что промпт делает «на глаз», но локально и управляемо).
- **chaiNNer**, **waifu2x** — узловой пайплайн / лёгкий апскейл аниме-графики и фото.

| Система | Как поставить локальный апскейлер |
| :--- | :--- |
| **Gentoo** (основная) | Upscayl — **AppImage** из релизов (в Portage пакета нет); Real-ESRGAN/GFPGAN — через `python` + `pip`/venv (`media-libs/…` для CUDA/ROCm по железу) |
| **Debian / Ubuntu** | Upscayl — **AppImage**/`.deb` из релизов; или `pipx install realesrgan` |
| **Arch** (план с июня 2026) | AUR: `upscayl-bin`; `python-pytorch` + Real-ESRGAN из pip |
| **Entware / RT-AX56U** | **N/A** — апскейл нейросетью требует GPU/десктоп; на роутере (armv7, 512 МБ) не запустить. Реставрируй на десктопе |

## 🔗 Ссылки

- Источник промпта: [@bugnotfeature/26283](https://t.me/bugnotfeature/26283)
- Локальные инструменты: [Upscayl](https://github.com/upscayl/upscayl) · [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) · [GFPGAN](https://github.com/TencentARC/GFPGAN) · [DeOldify](https://github.com/jantic/DeOldify)

#Prompt #ChatGPT #ImageGeneration #PhotoRestoration #Privacy
