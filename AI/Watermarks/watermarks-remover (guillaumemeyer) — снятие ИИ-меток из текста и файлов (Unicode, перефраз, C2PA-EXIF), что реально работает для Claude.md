---
создал заметку: 2026-10-13T18:00:00
author: WhiteK0T
tags:
  - AI
  - Claude
  - Вотермарки
  - Приватность
  - Метаданные
  - C2PA
Источник:
  - https://t.me/black_triangle_tg/9315
  - https://t.me/black_triangle_tg/9291
  - https://github.com/guillaumemeyer/watermarks-remover
---

# 🧼 watermarks-remover — снятие ИИ-меток из текста и файлов

**[guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover)** — открытый (MIT) набор Python-скриптов, HTTP-сервис и скилл для ИИ-агентов, который ищет и снимает метки происхождения ИИ-контента: невидимые символы Unicode, статистические вотермарки в тексте, метаданные C2PA/EXIF/XMP в файлах. Заявлены метки Claude, Gemini (SynthID), OpenAI и открытых моделей.

На 13.10.2026: **24 008 звёзд**, 2 754 форка, создан 11.08.2026, последний релиз **v0.7.0**, коммиты идут (последний — 09.10.2026). Около 52 тыс. строк кода и документации, большой набор тестов.

Предыстория — пост канала о том, что Anthropic с 2 августа 2026 метит контент Claude: подробно это разобрано в заметке [Вотермарки Claude](%D0%92%D0%BE%D1%82%D0%B5%D1%80%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%20Claude%20%28C2PA%20%2B%20%D0%BD%D0%B5%D0%B2%D0%B8%D0%B4%D0%B8%D0%BC%D1%8B%D0%B9%20%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BE%D0%B2%D1%8B%D0%B9%29%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%20Anthropic%20%D0%BC%D0%B5%D1%82%D0%B8%D1%82%20AI-%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D1%82%2C%20%D1%87%D1%82%D0%BE%20%D0%BF%D1%83%D1%82%D0%B0%D0%B5%D1%82%20%D0%BF%D0%BE%D1%81%D1%82%20%D0%B8%20%D0%BD%D0%B0%D1%81%D0%BA%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20%D1%8D%D1%82%D0%BE%20%D1%81%D1%82%D0%BE%D0%B9%D0%BA%D0%BE.md). Похожий, но платный веб-сервис — в заметке [Claude Watermark Remover](Claude%20Watermark%20Remover%20%E2%80%94%20%C2%AB%D1%83%D0%B4%D0%B0%D0%BB%D1%8F%D1%82%D0%BE%D1%80%C2%BB%20%D0%B2%D0%BE%D1%82%D0%B5%D1%80%D0%BC%D0%B0%D1%80%D0%BA%D0%B0%20Claude%20%28%D1%81%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D1%85%20%D1%81%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB%D0%BE%D0%B2%20%D0%BD%D0%B5%D1%82%20%D0%B2%D0%BE%D0%B2%D1%81%D0%B5%2C%20%D1%87%D0%B8%D1%81%D1%82%D0%BA%D0%B0%20%D0%BD%D0%B5%20%D0%BF%D1%80%D0%BE%20%D0%B2%D0%BE%D1%82%D0%B5%D1%80%D0%BC%D0%B0%D1%80%D0%BA%2C%20%D1%81%D0%BD%D1%8F%D1%82%D0%B8%D0%B5%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%D0%B5%29.md).

> [!info] Коротко, что важно знать
> - **Для текста Claude** надёжно работает только чистка мусора копипаста. Метка Claude — это статистический сдвиг в выборе слов, невидимых символов в ней нет. Снять её можно лишь перефразом другой моделью, и **проверить результат нечем**: детектор Anthropic в закрытом превью, в инструменте для него стоит заглушка.
> - **Для файлов** (C2PA, EXIF, XMP, свойства документов) чистка детерминированная и проверяемая — это самая полезная часть.
> - Перефраз ухудшает текст. Автор сам пишет: если всё равно переписывать дешёвой моделью, проще сразу писать ею.

---

## 1. Три уровня

| Уровень | Что снимает | Как | Можно ли проверить |
| :--- | :--- | :--- | :--- |
| **A — Unicode** | пробелы нулевой ширины, bidi-символы, tag-символы, экзотические пробелы | детерминированные скрипты, только stdlib Python | да: отчёт со счётчиками |
| **B — статистический вотермарк** | метку в самом выборе токенов (SynthID-Text, Kirchenbauer, Aaronson) | **перефраз другой моделью** | только для схем с известным ключом (MarkLLM, Gumbel) — не для Claude |
| **Файлы** | C2PA, EXIF, XMP, свойства документов | разбор контейнеров: PNG, JPEG, WebP, AVIF, HEIC, BMP, GIF, TIFF, SVG, PDF, DOCX, XLSX, PPTX, EPUB, ODT, HTML, Markdown, MP4/MOV, WAV, MP3, FLAC | да |

### Что по каким вендорам (матрица из README)

| Канал | Claude | Gemini / SynthID | OpenAI | Открытые модели |
| :--- | :--- | :--- | :--- | :--- |
| Unicode в тексте | уровень A | уровень A | уровень A | уровень A |
| Статистическая метка в тексте | перефраз «по возможности»; проверки нет, пока Anthropic не откроет детектор | перефраз; Google закрыл свой API-детектор в августе 2026 | перефраз, если метка есть | перефраз + проверка MarkLLM |
| C2PA и метаданные файлов | да | да | да | да |
| Пиксельные метки в картинках | **вне рамок** | опционально: оценка SynthID и удаление через внешний CtrlRegen | вне рамок | опционально, внешние бэкенды |

---

## 2. Уточнения к посту

- **Удаление пиксельных вотермарков в проекте есть, но как внешний опциональный модуль.** С v0.4.0 подключается бэкенд **CtrlRegen** (регенерация картинки через Stable Diffusion 1.5 + ControlNet). Ему нужны около 10 ГБ моделей и желательно GPU. Он рассчитан на метки класса SynthID, StegaStamp, Tree-Ring и StableSignature. Для картинок Claude не нужен: их метка — это C2PA в метаданных. Вне рамок остаётся только «мягкая привязка» C2PA (soft binding): водяной знак в самих пикселях, по которому можно снова найти удалённый манифест.
- **Отбор «наиболее лексически удалённого» варианта — запасной режим.** По умолчанию генерируется **один** вариант за раунд. Если подключён детектор (MarkLLM для схем с известным ключом), перефраз повторяется, пока детектор не перестанет видеть метку. Сравнение по лексическому расстоянию включается, только когда детектора нет. С v0.7.0 сервис `/clean` по умолчанию применяет стратегию `paraphrase@0.8,mlm@0.2` и без настроенной модели для перефраза возвращает ошибку 400.
- **Для текста Claude уровень A почти ничего не даёт.** Невидимых символов в ответах Claude нет, их могут добавить только редакторы и копирование из веба.
- **Фраза про «честно гарантировать»** в README звучит так: *«Until vendors ship public detectors and keys, no tool can honestly certify “this fails the official check.”»*

---

## 3. Установка

Ядру нужен только **Python 3.10+** без зависимостей. Внешние утилиты необязательны, но с ними чистка файлов полнее:

| Система | Python + утилиты для файлов |
| :--- | :--- |
| **Gentoo** | `emerge --ask dev-lang/python media-libs/exiftool app-text/qpdf` |
| **Debian / Ubuntu** | `sudo apt install python3 libimage-exiftool-perl qpdf` |
| **Arch** | `sudo pacman -S python perl-image-exiftool qpdf` |
| **Entware** | `opkg install python3` — хватит для уровня A и метаданных простых форматов; тяжёлые модули (перефраз, CtrlRegen) на роутере не запустить |

- `qpdf` **обязателен для настоящей чистки PDF**: одного `exiftool` мало, старые версии метаданных остаются в инкрементальных обновлениях файла.
- `c2patool` (просмотр манифестов C2PA) ставится через `cargo install c2patool` или из релизов [contentauth/c2pa-rs](https://github.com/contentauth/c2pa-rs/releases).

```bash
git clone https://github.com/guillaumemeyer/watermarks-remover.git
cd watermarks-remover
S=service/scripts

python3 "$S/inspect_file.py" report.docx                    # что найдено
python3 "$S/clean_file.py" report.docx -o report.clean.docx # снять метаданные
python3 "$S/clean_file.py" shot.png -o shot.clean.png
python3 "$S/clean_text.py" draft.md -o draft.clean.md --stats   # только уровень A
```

### Как скилл для агента

```bash
# Claude Code — через маркетплейс плагинов
/plugin marketplace add guillaumemeyer/watermarks-remover
/plugin install watermarks-remover@watermarks-remover

# или скриптом: claude-code, claude-project, codex, cursor, cowork (zip для загрузки)
python3 install_skill.py --skill remove-ai-marks --target claude-code
make serve        # скиллу нужен локальный сервис на 127.0.0.1:8765
```

- `remove-ai-marks` — полный скилл, сам кода не содержит и обращается к сервису по HTTP.
- `clean-user-facing-text` — автономный, только текст, уровень A, сервис не нужен.
- Плагин ставит хук `PostToolUse` на запись файлов: по умолчанию режим `check` (только сообщает), `WATERMARKS_HOOK_MODE=clean` — чистит сразу. Ответ агента в чате хук изменить не может, только файлы.
- Сервис по умолчанию слушает только loopback. Если открываете его в сеть, задайте `WATERMARKS_SERVER_API_KEY`.

---

## 4. Когда это полезно

- **Убрать метаданные из своих файлов перед публикацией**: C2PA, EXIF, авторов и историю правок в DOCX/PDF. Это та же задача, что у MAT2, но с поддержкой C2PA и новых форматов (AVIF, HEIC, EPUB). Подробнее о MAT2 — в заметке [MAT2](../../Security/MAT2%20%28Metadata%20Anonymisation%20Toolkit%202%29%20%E2%80%94%20%D0%BE%D1%87%D0%B8%D1%81%D1%82%D0%BA%D0%B0%20%D0%BC%D0%B5%D1%82%D0%B0%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85%20%D0%B8%D0%B7%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%20%28%D1%87%D1%82%D0%BE%20%D1%87%D0%B8%D1%81%D1%82%D0%B8%D1%82%2C%20%D1%87%D1%82%D0%BE%20%D0%BE%D1%80%D0%B8%D0%B3%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20MAT%20%D0%BC%D1%91%D1%80%D1%82%D0%B2%2C%20%D1%87%D1%82%D0%BE%20MAT2%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md) (он уже в архиве).
- **Почистить текст от мусора копипаста**: невидимые символы, неразрывные и экзотические пробелы, которые ломают поиск, диффы и код. Есть pre-commit-хук для репозиториев.
- **Исследовать вотермарки**: генерация помеченного текста (`/watermark`), проверка стойкости схем с открытым ключом, бенчмарки.

Где не поможет:
- **Выдать текст Claude за свой.** Метка Claude после перефраза не проверяется ничем, а сам перефраз заметно портит стиль. Автор прямо пишет, что проект — для своего контента и приватности, а не для академического мошенничества.
- **Антиплагиат вроде Turnitin или GPTZero** вотермарк Anthropic не читает вообще. Они ищут другие признаки, так что инструмент не про них.

## 🔗 Ссылки

- Репозиторий: https://github.com/guillaumemeyer/watermarks-remover
- Проверка файлов на C2PA от Anthropic: https://claude.com/check-content
- Content Credentials verify: https://contentcredentials.org/verify
- Исходные посты: https://t.me/black_triangle_tg/9315 · https://t.me/black_triangle_tg/9291

#AI #Claude #Вотермарки #Приватность #Метаданные #C2PA
