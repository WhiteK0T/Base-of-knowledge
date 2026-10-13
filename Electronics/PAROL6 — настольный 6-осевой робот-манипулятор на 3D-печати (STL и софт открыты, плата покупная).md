---
создал заметку: 2026-10-14T12:00:00
author: WhiteK0T
tags:
  - Electronics
  - Робототехника
  - Open_Hardware
  - 3D-печать
  - ROS2
Источник:
  - https://t.me/open_source_friend/5848
  - https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm
  - https://source-robotics.github.io/PAROL-docs/
  - https://github.com/Source-Robotics/PAROL-commander-software
  - https://source-robotics.com/
---

# 🦾 PAROL6 — настольный 6-осевой робот-манипулятор на 3D-печати

**[PAROL6](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm)** — настольный робот-манипулятор от хорватской **Source Robotics** (автор — Петар Црњак). Корпус печатается на 3D-принтере, а механика, управление и программы сделаны по образцу промышленных роботов: планетарные редукторы, конические роликоподшипники, кинематика, аварийный стоп, программирование командами. Подходит для обучения, исследований и экспериментов с ROS 2.

| | |
| :--- | :--- |
| Репозиторий | [Source-Robotics/PAROL6-Desktop-robot-arm](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm) (старый адрес `PCrnjak/…` перенаправляет) |
| Звёзды / форки | **3 370** · 403, с июля 2023, последний коммит 02.10.2026 (обновление BOM) |
| Лицензия | **GPL-3.0** — STL, код, инструкции и BOM |
| Документация | [source-robotics.github.io/PAROL-docs](https://source-robotics.github.io/PAROL-docs/) |

> [!info] Насколько он открытый
> Пост называет проект «полностью открытым» — это почти так, но с двумя оговорками:
> - **Плату управления** (STM32F446RE + драйверы TMC5160) нужно покупать у Source Robotics: схем и файлов печатной платы в открытом доступе нет. Исходники её прошивки при этом в репозитории есть. Программа управления Commander прямо требует эту плату.
> - **Бесплатны STL-файлы**, то есть готовые сетки для печати. Редактируемые CAD-модели в STEP **продаются** (около 27 в валюте магазина). Мелкие правки делать можно, а вот полноценно перепроектировать детали без STEP неудобно.

---

## 1. Характеристики (из документации)

| Параметр | Значение |
| :--- | :--- |
| Степени свободы | 6 |
| Грузоподъёмность | **1 кг** у основания, **0,5 кг** во всей рабочей зоне |
| Повторяемость | **0,1 мм** |
| Досягаемость | 400 мм со штатным захватом |
| Масса | 5,5 кг |
| Диапазоны суставов | J1 250°, J2 141°, J3 180°, J4 212°, J5 180°, J6 без ограничения |
| Приводы | шаговые двигатели NEMA 17 + планетарные редукторы и ремни HTD3 |
| Питание | 24 В, около 40 Вт |
| Связь | USB с компьютером, CAN, 2 изолированных выхода, вход аварийного стопа |

Повторяемость 0,1 мм — заявленная производителем. На самосборном роботе она зависит от качества печати, натяжения ремней и люфта редукторов.

---

## 2. Из чего состоит репозиторий

```
STL/                            детали для печати по узлам (база, плечо, локоть, запястье, захват, аварийный стоп)
STL/SMALL_PRINT_BED/            варианты деталей для принтеров с маленьким столом (от сообщества)
BOM/BOM.md                      список покупных компонентов со ссылками
Building instructions/          инструкция по сборке (PDF) и советы по печати PETG
PAROL6 control board main software/   прошивка платы (PlatformIO, AccelStepper)
PAROL6 control board test code/       тестовая прошивка
PAROL6_URDF/                    модель робота для симуляции (URDF)
Extras/LEAP motion control code       управление жестами через Leap Motion
```

Детали печатаются из **PETG** (советы — в `Building instructions/PETG_printing.md`).

### Главные покупные компоненты (BOM)

| Узел | Что | Кол-во |
| :--- | :--- | :--- |
| Двигатели | NEMA 17: 16 Н·см ×1, 45 Н·см ×3, 65 Н·см ×2 | 6 |
| Редукторы | планетарные NEMA 17, 20:1 ×2 и 10:1 ×1 (серия EG; дешевле — серия MG с бо́льшим люфтом) | 3 |
| Подшипники | конические NSK HR32906J ×5, HR32907J ×4, игольчатый упорный AXK3552, мелкие 3×8×4 и 3×10×4 для натяжения ремней | |
| Ремни | HTD3, ширина 6 мм, четыре длины | 4 |
| Электроника | плата PAROL, драйверы TMC5160 ×6 (если плата без них), блок питания 24 В 5 А | |

Часть ссылок в BOM партнёрские (AliExpress, StepperOnline). Крепёж, ремни и подшипники можно купить где угодно.

---

## 3. Сколько стоит (магазин Source Robotics, 14.10.2026)

| Вариант | Цена |
| :--- | ---: |
| Собранный робот | 3 570 |
| Полный набор для сборки | 2 379 |
| Частичный набор | 1 189 |
| Напечатанные детали | 476 |
| Плата управления без драйверов / с драйверами | 237 / 471 |
| Набор крепежа | 58 |
| Файлы STEP | 27 |
| Адаптивный захват SSG-48 | 714–774 |

Цены — в валюте магазина (компания в Хорватии, вероятнее всего евро). Самостоятельная сборка с покупной платой обычно выходит заметно дешевле набора, но основная часть суммы — двигатели, редукторы и подшипники.

---

## 4. Программы

| Программа | Что это | Лицензия |
| :--- | :--- | :--- |
| [PAROL Commander](https://github.com/Source-Robotics/PAROL-commander-software) | графическая программа: движение по осям и в декартовых координатах, программирование командами, симулятор, телеметрия, управление захватом | GPL-3.0 |
| [PAROL6 Python API](https://github.com/PCrnjak/PAROL6-python-API) | управление роботом из Python без графического интерфейса | GPL-3.0 |
| [PAROL6-ROS2-MOVEIT](https://github.com/Source-Robotics/PAROL6-ROS2-MOVEIT) | симуляция и планирование движений в ROS 2 / MoveIt | MIT |
| [PAROL-Web-Commander](https://github.com/Jepson2k/PAROL-Web-Commander) | веб-альтернатива Commander от сообщества | — |

Ещё проекты сообщества (интерфейсы, демо с компьютерным зрением и ИИ, доработки железа) — в [`community_projects.md`](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/community_projects.md).

### Установка Commander

Протестирован на **Python 3.10**. Авторы рекомендуют процессор не слабее 6-ядерного Intel i5 2017 года или аналогичного AMD; из ARM проверен Radxa ROCK 5B.

```bash
git clone https://github.com/Source-Robotics/PAROL-commander-software.git
cd PAROL-commander-software
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

Системные пакеты для графического интерфейса (Tk и Pillow):

| Система | Команда |
| :--- | :--- |
| **Gentoo** | `tkinter` — USE-флаг `tk` у `dev-lang/python` (в `/etc/portage/package.use/python`: `dev-lang/python tk`), затем `emerge --ask --newuse dev-lang/python dev-python/pillow` |
| **Debian / Ubuntu** | `sudo apt install python3-tk python3-pil python3-pil.imagetk` |
| **Arch** | `sudo pacman -S tk python-pillow` |
| **Entware** | не подходит: нужен настольный компьютер с графикой и достаточной мощностью |

Плата подключается по USB как последовательный порт. На Linux пользователю нужен доступ к нему: группа `dialout` на Debian/Ubuntu и Gentoo, `uucp` на Arch (`sudo usermod -aG dialout $USER` и перелогиниться).

Если проблемы с декартовым перемещением — у Commander есть ветка `experimental_kinematics`, но авторы предупреждают, что она может повредить робота. Основная ветка безопасна.

---

## 5. Безопасность

Авторы выделяют отдельный документ [SAFETY_WARNING_AND_DISCLAIMER](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/SAFETY_WARNING_AND_DISCLAIMER.md). Суть: робот может двигаться резко и неожиданно, защемить или ударить, а блок питания работает от сети 230 В. Практически:
- соберите и подключите **аварийный стоп** (детали есть в `STL/ESTOP`) до первого включения;
- первые запуски — на малых скоростях и с ограничениями суставов в программе;
- блок питания 24 В — готовый, в закрытом корпусе (в BOM — Mean Well на DIN-рейку);
- поведение в симуляторе и на реальном роботе может отличаться.

## 🔗 Ссылки

- Репозиторий: https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm
- Документация: https://source-robotics.github.io/PAROL-docs/
- Видео работы: https://youtu.be/bbrFn3aFLaA · уроки: https://youtube.com/playlist?list=PLSueoDrBt5MMTL9O8qAWZiJrNIf8-29Qz
- Магазин: https://source-robotics.com/
- Hackaday: https://hackaday.io/project/191860-parol6-desktop-robotic-arm
- Исходный пост: https://t.me/open_source_friend/5848

Похожие проекты в базе: [OpenAMR](OpenAMR%20%E2%80%94%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D0%B9%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BD%D0%BE%D0%BC%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%80%D0%BE%D0%B1%D0%BE%D1%82%20%28AMR%29%20%D0%B4%D0%BB%D1%8F%20%D1%81%D0%BA%D0%BB%D0%B0%D0%B4%D0%B0%20%D1%81%D0%B2%D0%BE%D0%B8%D0%BC%D0%B8%20%D1%80%D1%83%D0%BA%D0%B0%D0%BC%D0%B8%20%28ROS%202%2C%20LiDAR-SLAM%2C%20%D0%B4%D0%BE%20150%20%D0%BA%D0%B3%29.md), [DIY-CNC-machine](DIY-CNC-machine%20%28maxvfischer%29%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4%20%D0%BF%D0%BE%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B5%20%D0%A7%D0%9F%D0%A3-%D1%84%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B0%20%D1%81%20%D0%BD%D1%83%D0%BB%D1%8F%20%28BOM%2C%203D-%D0%B4%D0%B5%D1%82%D0%B0%D0%BB%D0%B8%2C%20GRBL%29%2C%20%D1%87%D1%82%D0%BE%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B8%20%D0%B8%20%D1%82%D1%80%D0%B5%D0%B7%D0%B2%D0%B0%D1%8F%20%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B0.md), [awesome-open-hardware](awesome-open-hardware%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D1%80%D0%B5%D1%81%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D0%BF%D0%BE%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D0%BE%D0%BC%D1%83%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D1%83%20%28open%20hardware%29.md).

#Electronics #Робототехника #Open_Hardware #3D-печать #ROS2
