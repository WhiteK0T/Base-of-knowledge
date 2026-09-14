---
создал заметку: 2026-09-14T16:30:00
author: WhiteK0T
tags:
  - Security
  - Privacy
  - Metadata
  - OSINT
  - AntiForensics
  - OpenSource
Источник:
  - https://t.me/c/2675453029/1387
  - https://0xacab.org/jvoisin/mat2
  - https://github.com/jvoisin/mat2
---

# 🕵️ MAT2 — очистка метаданных из файлов (что чистит и почему пост даёт мёртвую ссылку)

**MAT2** (Metadata Anonymisation Toolkit 2, автор **jvoisin**) — инструмент на **Python 3** для удаления метаданных из файлов: имя автора, устройство, GPS-геолокация, время создания, версия ПО, история правок, EXIF и т.п. Ядро — **библиотека** + CLI `mat2` + расширения для файловых менеджеров (Nautilus/Dolphin). Применяется в **OSINT-гигиене, журналистике, ИБ и приватности** — чтобы не «слить» себя через опубликованный файл.

> [!danger] Ссылка в посте ведёт на МЁРТВЫЙ проект
> Пост даёт [`github.com/jubalh/MAT`](https://github.com/jubalh/MAT) — это **зеркало оригинального MAT** (не MAT2!): **Python 2.7, GTK, hachoir**, копирайт Julien Voisin **2011–2015**, не развивается ~10 лет. Ставить его сегодня — боль с Python 2 и мёртвыми зависимостями.
> **Актуален MAT2** — переписанный на Python 3 преемник: дом [`0xacab.org/jvoisin/mat2`](https://0xacab.org/jvoisin/mat2), зеркало [`github.com/jvoisin/mat2`](https://github.com/jvoisin/mat2). Именно его ставит пакет `mat2` в дистрибутивах.

> [!warning] И сам MAT2 теперь заморожен (важно для ожиданий)
> Официальный репозиторий MAT2 помечен как **archived / read-only** — проект «стабилен и закончен», активной разработки нет. Он **рабочий и в репозиториях дистрибутивов**, но новых форматов/фиксов от апстрима ждать не стоит. Если нужен живой апстрим — есть форки (например [`github.com/atenart/mat2`](https://github.com/atenart/mat2)) и GUI **Metadata Cleaner** (Flatpak, обёртка над mat2).

## 🧬 Что умеет

- **Чистит копию, не портит оригинал:** `mat2 photo.jpg` создаёт `photo.cleaned.jpg`, исходник не трогает.
- **Форматы:** изображения (JPEG, PNG, TIFF, GIF, WEBP), **PDF**, офис (docx/xlsx/pptx, odt/ods/odp), аудио (MP3/FLAC/OGG/WAV), видео (MP4/AVI — ограниченно, через FFmpeg), torrent и др. Точный список — `mat2 -l`.
- **Показать метаданные без очистки:** `mat2 --show file.pdf` (`-s`).
- **Лёгкий режим:** `mat2 -L`/`--lightweight` — быстрая чистка без глубокой пересборки (когда полная ломает файл).

```bash
mat2 -l                     # какие форматы поддерживаются
mat2 --show doc.pdf         # что внутри (не меняя файл)
mat2 doc.pdf                # → doc.cleaned.pdf
mat2 -L video.mp4           # лёгкая чистка (видео — неполно, см. ниже)
```

## ⚠️ Чего MAT2 НЕ делает (факты против «без следов»)

> [!caution] «Очистка без следов» — с оговорками
> - **Метаданные ≠ анонимность.** MAT2 убирает *известные* контейнеры метаданных, но **содержимое файла** остаётся: лица и таблички на фото, стиль текста, водяные знаки, скрытые данные в незнакомых форматах. Плюс тебя выдаёт **имя файла** и сам факт «чистого» файла.
> - **Видео — неполно.** Поддержка MP4/AVI через FFmpeg частичная, апстрим сам это оговаривает; критичные ролики лучше проверять вручную (`--show`) и не полагаться слепо.
> - **Не все форматы одинаково.** Экзотику MAT2 может не знать целиком; всегда сверяйся `--show` до публикации.
> - **Проверяй результат.** После `.cleaned` прогони `mat2 --show` по копии — убедись, что метаданных не осталось.

## 🖥️ Установка на системах владельца

MAT2 — Python 3, нужен PyGObject + библиотеки под форматы (poppler для PDF, gdk-pixbuf; FFmpeg для видео):

| Система | Как поставить |
| :--- | :--- |
| **Gentoo (основная)** | проверь `app-misc/mat2` в Portage/оверлеях; либо `pipx install mat2` + системные `poppler`, `gdk-pixbuf`, по желанию `media-video/ffmpeg` |
| **Debian / Ubuntu** | `sudo apt install mat2` (в официальных репах; тянет `python3-gi`, `gir1.2-poppler`, `gir1.2-gdkpixbuf`) |
| **Arch** | `sudo pacman -S mat2` (extra) |
| **Entware / RT-AX56U** | ➖ **непрактично**: GTK/PyGObject-стек и poppler на armv7-роутере тяжелы и не нужны; чисти метаданные на десктопе, а не на роутере |

> [!tip] GUI, если не любишь CLI
> **Metadata Cleaner** (Flatpak `fr.romainvigier.MetadataCleaner`) — графическая обёртка над mat2: перетащил файлы → «Очистить». Под капотом та же библиотека, те же ограничения.

## 🔗 Связанные заметки

- Обратная сторона — **чем эти метаданные собирают** (self-OSINT): [Argus — сканер цифрового следа](../Pentest/Recon/Argus%20%28lachydotmcg%29%20%E2%80%94%20self-OSINT%20%D1%81%D0%BA%D0%B0%D0%BD%D0%B5%D1%80%20%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%BE%D0%B3%D0%BE%20%D1%81%D0%BB%D0%B5%D0%B4%D0%B0%20%28username%20%2B%20Gemini-%D0%B4%D0%BE%D1%80%D0%BA%D0%B8%2C%20%D1%80%D0%B8%D1%81%D0%BA-%D0%BE%D1%82%D1%87%D1%91%D1%82%29.md) · [Web Check — OSINT-досье на сайт](../Pentest/Recon/Web%20Check%20%E2%80%94%20OSINT-%D0%B4%D0%BE%D1%81%D1%8C%D0%B5%20%D0%BD%D0%B0%20%D1%81%D0%B0%D0%B9%D1%82%20%28DNS-SSL-%D0%B7%D0%B0%D0%B3%D0%BE%D0%BB%D0%BE%D0%B2%D0%BA%D0%B8-%D1%81%D1%82%D0%B5%D0%BA-%D0%BF%D0%BE%D1%80%D1%82%D1%8B%29.md)
- Соседний защитный CDR-инструмент (обезвредить, а не почистить): [Dangerzone](Dangerzone%20%28Freedom%20of%20the%20Press%29%20%E2%80%94%20%D0%BE%D0%B1%D0%B5%D0%B7%D0%B2%D1%80%D0%B5%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D1%8B%D1%85%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B2%20%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D1%8B%D0%B9%20PDF%20%28CDR%2C%20%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D0%B0%29.md)
- Приватность шире: [privacy.sexy](privacy.sexy%20%E2%80%94%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%20%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B2%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B0%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B8%20%D1%85%D0%B0%D1%80%D0%B4%D0%BD%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D0%B0%20%D0%B4%D0%BB%D1%8F%20Windows-macOS-Linux%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B%29.md) · [paranoiaprivacy.wiki — гайд для «параноидальных»](Privacy/Guides/paranoiaprivacy.wiki%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B0%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B4%D0%BB%D1%8F%20%C2%AB%D1%80%D0%B0%D0%B7%D1%83%D0%BC%D0%BD%D0%BE%20%D0%BF%D0%B0%D1%80%D0%B0%D0%BD%D0%BE%D0%B8%D0%B4%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%C2%BB%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2011%20%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D0%BE%D0%B2%2C%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D1%8B%20%D0%BF%D0%BE%D0%B4%204%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%2C%20%D0%A0%D0%A4-%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%29.md)

## 🔗 Ссылки

- MAT2 (актуальный): [0xacab.org/jvoisin/mat2](https://0xacab.org/jvoisin/mat2) · зеркало [github.com/jvoisin/mat2](https://github.com/jvoisin/mat2) · форк [atenart/mat2](https://github.com/atenart/mat2)
- GUI: **Metadata Cleaner** (Flatpak `fr.romainvigier.MetadataCleaner`)
- Оригинальный MAT (мёртв, из поста): [github.com/jubalh/MAT](https://github.com/jubalh/MAT)
- Источник новости: [@CodeGuard](https://t.me/c/2675453029/1387)

#Security #Privacy #Metadata #OSINT #AntiForensics #OpenSource
