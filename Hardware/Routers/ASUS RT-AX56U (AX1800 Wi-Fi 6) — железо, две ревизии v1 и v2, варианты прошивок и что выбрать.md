---
создал заметку: 2026-10-05T13:00:00
author: WhiteK0T
tags:
  - Роутер
  - ASUS
  - Broadcom
  - WiFi6
  - Железо
  - Merlin
Источник:
  - https://www.asus.com/networking-iot-servers/wifi-routers/asus-wifi-routers/rt-ax56u/techspec/
  - https://techinfodepot.shoutwiki.com/wiki/ASUS_RT-AX56U
  - https://github.com/RMerl/asuswrt-merlin.ng/wiki/Supported-Devices
  - https://www.snbforums.com/threads/asus-merlin-support-ax56u-model-can-support-ax56u-v2-same-firmware.83298/
  - https://www.snbforums.com/threads/cannot-flash-merlin-on-rt-ax56u-v2.68383/
---

# 📡 ASUS RT-AX56U (AX1800 Wi-Fi 6) — железо, две ревизии, прошивки

**ASUS RT-AX56U** — недорогой Wi-Fi 6 роутер класса **AX1800** на **Broadcom BCM6755** (4× ARM Cortex-A7). Классический «настольный» роутер: **WAN + 4 LAN по 1 Гбит/с**, два USB-порта (один USB 3.x), 512 МБ RAM. Главное его достоинство по сравнению с современными карманными моделями — **четыре проводных порта и штатная поддержка Entware/Merlin**. Главная проблема — **прошивка заморожена**, а OpenWrt на этот SoC не ставится.

Это вторая заметка по модели. Про прошивку и причины остановки обновлений подробно: [RT-AX56U и Asuswrt-Merlin](ASUS%20RT-AX56U%20%D0%B8%20Asuswrt-Merlin%20%E2%80%94%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%BE%D0%BD%D1%87%D0%B8%D0%BB%D0%B8%D1%81%D1%8C%20%D0%BD%D0%B0%203004.388.8_4%20%28%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%BF%D1%80%D0%B8%D1%87%D0%B8%D0%BD%D0%B0%2C%20Entware%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%2C%20%D1%81%D1%82%D0%BE%D0%BA%20ASUS%29.md). Здесь только железо, ревизии и выбор.

> [!danger] Главное, что надо знать
> 1. **Под названием RT-AX56U продаются две разные модели: v1 и v2.** Железо у них разное, а **Asuswrt-Merlin поддерживает только v1** (v2, китайский вариант, разработчик поддерживать не планирует). Проверь этикетку до любых прошивок.
> 2. **Merlin относит RT-AX56U к «No longer supported»**: последняя сборка `3004.388.8_4`, дальше обновлений нет.
> 3. **OpenWrt для RT-AX56U не существует**: на странице модели в OpenWrt Table of Hardware пусто (статьи нет), а Broadcom HND/BCM6755 с закрытым стеком в OpenWrt не поддерживается.

---

## ⚙️ Характеристики (сверено)

| Параметр | Значение |
| :--- | :--- |
| SoC | Broadcom **BCM6755**, 4 ядра ARM Cortex-A7, **1.5 ГГц** (платформа HND/`675x`, SDK 5.02) |
| RAM | **512 МБ** (чип Nanya NT5CC256M16ER-EK) |
| Флеш | **256 МБ** NAND (Macronix MX30LF2G189C-TI) |
| Wi-Fi | Wi-Fi 6: 2.4 ГГц до **574 Мбит/с** (2×2), 5 ГГц до **1201 Мбит/с** (2×2); радиочасть встроена в SoC |
| Антенны | 2 внешние |
| Ethernet | **1× WAN + 4× LAN**, 1 Гбит/с; коммутатор встроен в BCM6755 |
| USB | **1× USB 3.2 Gen 1** (он же 3.1 Gen 1) + **1× USB 2.0** |
| Питание | 12 В / 2 А, блок питания 110–240 В (круглый разъём) |
| Размер / вес | 223.5 × 129.3 × 47.5 мм, 456 г |
| Режимы | Router, Access Point, Repeater, Media Bridge, **AiMesh node** |
| VPN (сток) | сервер: IPSec, OpenVPN, PPTP; клиент: L2TP, OpenVPN, PPTP |
| Идентификаторы | FCC ID **MSQ-RTAXHY00** (v1), ревизия платы A1 (1.20) |

> [!note] Про номера из других источников
> Данные по этой модели у ASUS, TechInfoDepot и в вики Merlin согласуются. Не путай с **v2**: у неё другое железо (см. ниже), и числа из этой таблицы на неё переносить нельзя.

---

## 🔍 v1 против v2 — что проверить на этикетке

| | **RT-AX56U (v1)** | **RT-AX56U v2** |
| :--- | :--- | :--- |
| Рынок | основной (мировой) | в источниках описывается как китайский вариант |
| Merlin | **поддерживался**, последняя `3004.388.8_4` | **не поддерживается**, разработчик не планирует |
| FCC ID | `MSQ-RTAXHY00` | по SNBForums другой (`MSQ-RTAX8A00`) |

Что здесь **не удалось проверить**: страницы SNBForums отдали 403, поэтому факт «v2 ≠ v1 и Merlin её не берёт» взят из выдержек и заголовков тем («Cannot flash Merlin on RT-AX56U V2», «Install Merlin on Chinese asus AX56U»). Подробное железо v2 в источниках **противоречит само себе** (WikiDevi даёт для неё 256 МБ RAM, 128 МБ флеша и FCC ID v1), поэтому я его не привожу. Если у тебя китайская модель, перед прошивкой сверь этикетку, FCC ID и поддержку именно своей ревизии.

Проверка с самого роутера (подробнее — в разделе 11 заметки про Merlin):
```sh
nvram get productid     # модель
nvram get odmpid        # вариант/регион
nvram get buildno       # номер сборки прошивки
```

---

## 🧰 Прошивки: что реально доступно

| Вариант | Статус | Комментарий |
| :--- | :--- | :--- |
| **Сток ASUS** | жив, ветка 386 (ASUS модель на 388 не переводила) | вендорские фиксы, но функции урезаны |
| **Asuswrt-Merlin** | **No longer supported**, последняя `3004.388.8_4` | только v1; ядро 4.1 |
| **Самосборка 3004.388.12_2** | профиль модели в дереве есть | на свой риск (TFTP/UART нужны для отката) |
| **Entware поверх Merlin/стока** | рабочий и разумный путь | свежий OpenSSH/curl/OpenSSL на USB-диске |
| **OpenWrt** | **нет** | поддержки BCM6755 нет, и не ожидается |

Подробные причины (ядро 4.1, SDK 5.02, закрытые блобы), рецепты Entware и самосборки — в [заметке про Merlin](ASUS%20RT-AX56U%20%D0%B8%20Asuswrt-Merlin%20%E2%80%94%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%BE%D0%BD%D1%87%D0%B8%D0%BB%D0%B8%D1%81%D1%8C%20%D0%BD%D0%B0%203004.388.8_4%20%28%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%BF%D1%80%D0%B8%D1%87%D0%B8%D0%BD%D0%B0%2C%20Entware%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%2C%20%D1%81%D1%82%D0%BE%D0%BA%20ASUS%29.md).

> [!tip] Про пометку «Support: Yes» в вики naiveproxy
> В выдаче поиска встречается строка вида «RT-AX56U — Yes, ipq40xx/arm_cortex-a7». Это **не** про установку OpenWrt: страница описывает, **какой готовый бинарник naiveproxy** подойдёт по архитектуре (ARM Cortex-A7). Роутер при этом остаётся на ASUS/Merlin.

---

## 📦 Пакеты и архитектура

- Архитектура — **armv7 (32 бита)**. Для Entware это репозиторий `armv7sf-k3.2` (см. [OPKG](../../Linux/Package-Manager/OPKG.md)).
- Предел пакетов задаёт ядро **4.1** и закрытые блобы Broadcom: Entware закрывает userspace (SSH, curl, DNS), но не ядро и не веб-интерфейс.
- У владельца хранилища на этом роутере Entware стоит на USB-диске.

---

## 🆚 Против Cudy TR3000

Сравнительная таблица — в заметке про [Cudy TR3000](Cudy%20TR3000%20%28AX3000%20Travel%20Router%29%20%E2%80%94%20%D0%BA%D0%B0%D1%80%D0%BC%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%20%D1%80%D0%BE%D1%83%D1%82%D0%B5%D1%80%20%D0%BD%D0%B0%20MT7981B%20%D1%81%20OpenWrt%20%28%D0%B4%D0%B2%D0%B5%20%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8%20%D1%84%D0%BB%D0%B5%D1%88%D0%B0%2C%20%D0%BD%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%B0%D1%80%D1%82%D0%B8%D1%8F%202543%2B%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%29.md). Коротко, **когда что**:

| Задача | Выбор |
| :--- | :--- |
| Основной роутер дома, несколько проводных клиентов | **RT-AX56U** (4 LAN) |
| Вторая точка, дорожный роутер, прокси/VPN-шлюз | **TR3000** |
| Нужна «живая» прошивка с обновлениями | **TR3000** (OpenWrt) |
| Нужны свежие security-фиксы прошивки | не RT-AX56U (заморожена) |

---

## ⚖️ Плюсы и минусы

**Плюсы**
- 4 LAN-порта 1 Гбит/с, не нужен отдельный свитч.
- Два USB (один 3.x): диск, принтер, Entware.
- 512 МБ RAM и 256 МБ флеша достаточно для Entware.
- Сток и Merlin знакомы и хорошо задокументированы.

**Минусы**
- **Прошивка заморожена**: у Merlin конец на `3004.388.8_4`, у стока ветка 386.
- **Ядро 4.1** и закрытые блобы Broadcom: часть уязвимостей не закрыть.
- **OpenWrt нет и не будет.**
- Путаница v1/v2: Merlin работает только на v1.
- Нет 2.5G порта, Wi-Fi AX1800 (против AX3000 у TR3000).

---

## 🖥️ Доступ с рабочих систем

Настройка из браузера (`router.asus.com` или адрес роутера в LAN), отдельных программ не нужно. SSH включается в веб-интерфейсе (Merlin: Administration → System). Дальше с любой системы:

| Система | Что нужно |
| :--- | :--- |
| **Gentoo / Debian / Ubuntu / Arch** | обычный `ssh` (OpenSSH уже есть) |
| **Entware на самом роутере** | `opkg`, ставится на USB-диск (см. заметку про Merlin) |

```bash
ssh admin@<адрес-роутера>        # имя — логин веб-интерфейса
```

---

## 🔗 Связанные заметки

- Прошивка, EOL и Entware: [ASUS RT-AX56U и Asuswrt-Merlin](ASUS%20RT-AX56U%20%D0%B8%20Asuswrt-Merlin%20%E2%80%94%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%BE%D0%BD%D1%87%D0%B8%D0%BB%D0%B8%D1%81%D1%8C%20%D0%BD%D0%B0%203004.388.8_4%20%28%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%BF%D1%80%D0%B8%D1%87%D0%B8%D0%BD%D0%B0%2C%20Entware%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%2C%20%D1%81%D1%82%D0%BE%D0%BA%20ASUS%29.md)
- Альтернатива с OpenWrt: [Cudy TR3000](Cudy%20TR3000%20%28AX3000%20Travel%20Router%29%20%E2%80%94%20%D0%BA%D0%B0%D1%80%D0%BC%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%20%D1%80%D0%BE%D1%83%D1%82%D0%B5%D1%80%20%D0%BD%D0%B0%20MT7981B%20%D1%81%20OpenWrt%20%28%D0%B4%D0%B2%D0%B5%20%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8%20%D1%84%D0%BB%D0%B5%D1%88%D0%B0%2C%20%D0%BD%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%B0%D1%80%D1%82%D0%B8%D1%8F%202543%2B%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%29.md)
- Менеджер пакетов Entware: [OPKG](../../Linux/Package-Manager/OPKG.md)

## 🔗 Ссылки

- [ASUS: технические характеристики RT-AX56U](https://www.asus.com/networking-iot-servers/wifi-routers/asus-wifi-routers/rt-ax56u/techspec/) · [TechInfoDepot](https://techinfodepot.shoutwiki.com/wiki/ASUS_RT-AX56U) · [Merlin: Supported Devices](https://github.com/RMerl/asuswrt-merlin.ng/wiki/Supported-Devices)
- v1/v2 (страницы не открылись, 403): [SNBForums: поддержка v2](https://www.snbforums.com/threads/asus-merlin-support-ax56u-model-can-support-ax56u-v2-same-firmware.83298/) · [SNBForums: прошивка Merlin на v2](https://www.snbforums.com/threads/cannot-flash-merlin-on-rt-ax56u-v2.68383/)

#Роутер #ASUS #Broadcom #WiFi6 #Железо #Merlin
