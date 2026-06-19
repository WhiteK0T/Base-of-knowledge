---
создал заметку: 2026-06-19T20:35:00
author: WhiteK0T
tags:
  - FileManager
  - FAR
  - far3
  - Windows
  - TUI
Источник:
  - http://farmanager.com/
  - https://github.com/FarGroup/FarManager
  - https://en.wikipedia.org/wiki/Far_Manager
---

# 🪟 Far Manager 3 (far3) — ортодоксальный файловый менеджер для Windows

**Far Manager** (FAR = **F**ile and **AR**chive manager) — классический **ортодоксальный двухпанельный** файловый менеджер для **Windows**, клон Norton Commander. Создан **Евгением Рошалом** (автор RAR/WinRAR), развивается **Far Group** с 2000 года. **far3** — это ветка **3.0** (текущая, сборки ~3.0.6xxx). Работает в Win32-консоли, управление с клавиатуры, расширяется плагинами.

> [!info] Лицензия и открытость
> Unicode-ветки **2.0 и 3.0 — открытые**, под **BSD-3-Clause**. Исходники — у [FarGroup/FarManager](https://github.com/FarGroup/FarManager). (Старые не-Unicode версии 1.x были другими по лицензии — здесь речь про современный far3.)

> [!note] far3 — это Windows; на Linux нужен [far2l](far2l%20%E2%80%94%20%D0%BF%D0%BE%D1%80%D1%82%20FAR%20Manager%20%D0%BD%D0%B0%20Linux-macOS-BSD%20%28%D0%B4%D0%B2%D1%83%D1%85%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%29.md)
> Far Manager 3 — **нативно только под Windows** (Win32-консоль). На Linux/macOS его запускают через **Wine**, но «родной» путь — порт **[far2l](far2l%20%E2%80%94%20%D0%BF%D0%BE%D1%80%D1%82%20FAR%20Manager%20%D0%BD%D0%B0%20Linux-macOS-BSD%20%28%D0%B4%D0%B2%D1%83%D1%85%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%29.md)** (форк v2). Поскольку основная система владельца — Linux, **far3 актуален только для Windows-машин**, на Linux бери far2l.

## ✨ Возможности

- **Двухпанельный** интерфейс, одновременный просмотр двух каталогов; клавиатуро-ориентированное управление (плюс ограниченная мышь, drag-and-drop).
- **Встроенный редактор и вьювер** для быстрой правки/просмотра файлов.
- **Подсветка** типов файлов по цвету, **группы сортировки** для удобной навигации.
- **Многоязычный** интерфейс.
- **Плагины (DLL)** через Plugins API — именно ими реализованы: поддержка **архивов**, **FTP-клиент**, временные панели, сетевой браузер и многое другое (идут в стандартной поставке).
- В 3.0 — **макросы на Lua** (вместо старого языка макросов 1.x/2.x), улучшенный движок плагинов.

## 📦 Установка

| Система | Как |
| :--- | :--- |
| **Windows** | официальный установщик/портативный архив с [far-manager.com](https://www.farmanager.com/download.php?l=ru) (x86/x64); есть в **winget**: `winget install Far.Far`, и в Chocolatey/Scoop |
| **Linux / macOS** | нативно **нет**; либо **Wine** (с оговорками по консоли), либо — **рекомендуется** — нативный [far2l](far2l%20%E2%80%94%20%D0%BF%D0%BE%D1%80%D1%82%20FAR%20Manager%20%D0%BD%D0%B0%20Linux-macOS-BSD%20%28%D0%B4%D0%B2%D1%83%D1%85%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%29.md) |
| **Entware / RT-AX56U** | **N/A** (Windows-софт; на роутере — `mc`/`ls` по SSH) |

## 💡 Кому полезно

- Работаешь под **Windows** и любишь **ортодоксальные двухпанельники** (Norton/Volkov Commander) с мощным редактором, архивами и FTP «из коробки».
- Нужны **плагины** и Lua-макросы под автоматизацию рутинных файловых задач.
- На **Linux** этот воркфлоу даёт нативно [far2l](far2l%20%E2%80%94%20%D0%BF%D0%BE%D1%80%D1%82%20FAR%20Manager%20%D0%BD%D0%B0%20Linux-macOS-BSD%20%28%D0%B4%D0%B2%D1%83%D1%85%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%29.md); более «современный» TUI с превью-картинками — [elio](elio%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D1%81%20%D0%BF%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20%28Rust%29.md).

## 🔗 Ссылки

- Сайт: [farmanager.com](http://farmanager.com/) · исходники: [github.com/FarGroup/FarManager](https://github.com/FarGroup/FarManager)
- Связанные: [far2l (порт FAR на Linux/macOS)](far2l%20%E2%80%94%20%D0%BF%D0%BE%D1%80%D1%82%20FAR%20Manager%20%D0%BD%D0%B0%20Linux-macOS-BSD%20%28%D0%B4%D0%B2%D1%83%D1%85%D0%BF%D0%B0%D0%BD%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%29.md) · [elio (TUI-менеджер с превью)](elio%20%E2%80%94%20%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D1%81%20%D0%BF%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20%28Rust%29.md)

#FileManager #FAR #far3 #Windows #TUI
