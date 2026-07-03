---
создал заметку: 2026-06-25T15:00:00
author: WhiteK0T
tags:
  - OpenHardware
  - Electronics
  - Awesome
  - Reference
  - Catalog
Источник:
  - https://github.com/delftopenhardware/awesome-open-hardware
  - https://t.me/open_source_friend/5719
---

# 🛠️ awesome-open-hardware — подборка ресурсов по открытому железу (open hardware)

[**awesome-open-hardware**](https://github.com/delftopenhardware/awesome-open-hardware) — курируемый «awesome»-список ресурсов по **открытому аппаратному обеспечению** (open source hardware): проекты, доклады, научные статьи, конференции, площадки, подкасты, книги и обучающие программы — собрано в одном месте. Ведёт **[Delft Open Hardware](https://delftopenhardware.nl/)** (инициатива при **TU Delft**), лицензия **CC0-1.0** (общественное достояние), ~930★, обновляется (правки — сегодня).

> [!note] Что это и чего ждать
> Это **справочник-указатель ссылок**, а не туториал, рейтинг или магазин. Уклон **академический** (есть журналы и статьи: Journal of Open Hardware, HardwareX), но рядом и чисто практические проекты. Используй как **карту «что вообще есть»** в мире открытого железа; конкретный проект/плату проверяй отдельно (живость, лицензия, доступность компонентов).

## 📂 Что внутри (разделы)

| Раздел | О чём |
| :--- | :--- |
| **Projects** | открытые проекты железа: Arduino, RepRap, Prusa3D, OpenBCI, OpenFlexure, FarmBot, VORON Design, WikiHouse, Open Source Ecology, SafeCast |
| **Talks / Papers** | доклады и научные публикации по open hardware |
| **Conferences** | профильные конференции и события |
| **Platforms** | площадки для публикации проектов: Hackaday.io, Instructables, Thingiverse, Kitspace.org |
| **Podcasts** | подкасты по теме |
| **Books / Training programs** | книги и обучающие программы |
| **Further Readings / Related awesome** | смежное чтение и другие awesome-списки |

В сумме ~**100+ ссылок**; отдельно стоит упомянуть **OSHWA Certification** (сертификация «открытости» железа) — полезный ориентир, что считается настоящим open hardware.

> [!tip] Чем open hardware отличается от «просто доступной схемы»
> Открытое железо = опубликованы **исходники дизайна** (схемы, разводка платы/Gerber, BOM, CAD-модели, прошивка) под свободной лицензией, чтобы можно было **повторить, изменить и производить**. Юридические рамки задают **[CERN OHL](https://cern-ohl.web.cern.ch/)** (аналог GPL/MPL для железа) и определение **[OSHWA](https://www.oshwa.org/definition/)**. Просто выложенный PDF-схемы без права на производство — это ещё **не** open hardware.

## 🔑 С чего начать (открытый стек)

- **Платы/контроллеры:** [Arduino](https://www.arduino.cc/) (классика входа), а для Wi-Fi/BLE-проектов — [ESP32](ESP32%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D0%B8%20%D0%B2%D1%8B%D0%B1%D0%BE%D1%80%20%D0%B2%D0%B0%D1%80%D0%B8%D0%B0%D0%BD%D1%82%D0%B0%20%282026%29.md).
- **EDA (проектирование плат):** **KiCad** — открытый, кроссплатформенный редактор схем и печатных плат (в списке тема EDA затрагивается через проекты/площадки).
- **Площадки идей:** **Hackaday.io**, **Kitspace.org** (готовые открытые платы с BOM), [BoardRepo](BoardRepo%20%E2%80%94%20%D0%B2%D0%B5%D0%B1-%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D1%85%20KiCad-%D0%BF%D0%BB%D0%B0%D1%82%20%28%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%D0%BD%D1%8B%D0%B9%20%D0%BF%D1%80%D0%BE%D1%81%D0%BC%D0%BE%D1%82%D1%80%2C%20%D1%81%D0%BA%D0%B0%D1%87%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20GitHub-%D0%B8%D0%BC%D0%BF%D0%BE%D1%80%D1%82%29.md) (просмотр KiCad-плат в браузере), **Thingiverse/Printables** для механики.
- **3D-механика:** корпуса и детали печатаются на 3D-принтере — пересекается с [awesome-3d-printing](../3D-Printing/awesome-3d-printing%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D0%BF%D0%BE%203D-%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D0%B8.md).

> [!tip] Под Linux владельца
> Инструменты open-hardware-разработки ставятся на Gentoo/Debian/Arch штатно: **KiCad** (`sci-electronics/kicad` в Gentoo, `kicad` в Debian/Arch или Flatpak), **Arduino IDE** / **PlatformIO**, **FreeCAD/OpenSCAD** для механики, **Blender**. На роутере/Entware смысла нет — это десктоп-САПР. Сам репозиторий — просто список ссылок, ничего ставить не нужно.

## 🧩 Похожие подборки

- [awesome-3d-printing](../3D-Printing/awesome-3d-printing%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D0%BF%D0%BE%203D-%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D0%B8.md) — софт/железо для печати (механическая часть open-hardware-проектов).
- [awesome-drones](../Drones/awesome-drones%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D0%BF%D0%BE%20%D0%B4%D1%80%D0%BE%D0%BD%D0%B0%D0%BC.md) — многие открытые полётники/рамы тоже относятся к open hardware.

## 💡 Кому полезно

- **Инженерам/мейкерам:** найти готовый открытый проект-основу (датчик, прибор, станок), чтобы не изобретать с нуля.
- **Студентам/исследователям:** академический срез (статьи, журналы, сертификация OSHWA) для научных open-hardware-работ.
- **Не** замена документации конкретного проекта и **не** магазин — это отправная точка «куда смотреть».

## 🔗 Ссылки

- Репозиторий: [github.com/delftopenhardware/awesome-open-hardware](https://github.com/delftopenhardware/awesome-open-hardware)
- Стандарты: [OSHWA Definition](https://www.oshwa.org/definition/) · [CERN OHL](https://cern-ohl.web.cern.ch/)
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5719)
- Связанные: [ESP32 (обзор и выбор)](ESP32%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D0%B8%20%D0%B2%D1%8B%D0%B1%D0%BE%D1%80%20%D0%B2%D0%B0%D1%80%D0%B8%D0%B0%D0%BD%D1%82%D0%B0%20%282026%29.md) · [awesome-3d-printing](../3D-Printing/awesome-3d-printing%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D0%BF%D0%BE%203D-%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D0%B8.md) · [awesome-drones](../Drones/awesome-drones%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D0%BF%D0%BE%20%D0%B4%D1%80%D0%BE%D0%BD%D0%B0%D0%BC.md)

#OpenHardware #Electronics #Awesome #Reference #Catalog
