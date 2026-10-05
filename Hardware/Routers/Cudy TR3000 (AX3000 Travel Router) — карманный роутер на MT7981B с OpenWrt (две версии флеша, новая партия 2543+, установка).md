---
создал заметку: 2026-10-05T12:00:00
author: WhiteK0T
tags:
  - Роутер
  - Cudy
  - OpenWrt
  - WiFi6
  - MediaTek
  - Железо
Источник:
  - https://www.cudy.com/en-us/products/tr3000-1-0
  - https://openwrt.org/toh/cudy/tr3000
  - https://techinfodepot.shoutwiki.com/wiki/Cudy_TR3000
  - https://www.cudy.com/en-us/blogs/faq/openwrt-software-download
  - https://forum.openwrt.org/t/cudy-started-using-a-new-flash-chip-in-their-ax3000-devices-its-currently-unsupported/243547
  - https://github.com/openwrt/openwrt/pull/19167
  - https://www.wildberries.ru/catalog/1266531412/detail.aspx
  - https://4pda.to/forum/index.php?showtopic=1099628
---

# 📡 Cudy TR3000 (AX3000 Travel Router) — карманный роутер с OpenWrt

**Cudy TR3000** — компактный Wi-Fi 6 роутер («travel router») на **MediaTek MT7981B (Filogic 820)**. Для своей цены у него сильные характеристики: 2.5-гигабитный WAN, 512 МБ RAM, USB 3.0, а главное — он **официально поддерживается в OpenWrt**. Минус один: всего **два Ethernet-порта** (WAN 2.5G + LAN 1G).

Заметка собрана по первоисточникам (Cudy, OpenWrt Table of Hardware, TechInfoDepot, форум OpenWrt). Ссылки на **4PDA** и **Wildberries** из запроса проверить не удалось: 4PDA отдал HTTP 403, WB — 498 (антибот). Поэтому цена и содержимое ветки 4PDA здесь **не проверялись**.

> [!danger] Главное, что надо знать до прошивки OpenWrt
> 1. **Две версии флеша — 128 МБ и 256 МБ — и образы у них разные.** Объём смотри на этикетке или коробке.
> 2. **Новая партия (серийный номер начинается с `2543` и выше, с ноября 2025)** получила другой чип флеша (`F50L1G41LC`). Старые образы OpenWrt и старые промежуточные прошивки на нём **не загрузятся** (кирпич). Нужен **OpenWrt 24.10.5 или новее**.
> 3. **Откат на старые версии OpenWrt на такой партии тоже ломает загрузку** (прямо предупреждает Cudy).

---

## ⚙️ Характеристики (сверено)

| Параметр | Значение |
| :--- | :--- |
| SoC | MediaTek **MT7981BA** (Filogic 820), 2× ARM Cortex-A53 @ 1.3 ГГц |
| RAM | **512 МБ** DDR3L |
| Флеш | SPI NAND, **128 МБ** (в спецификации Cudy) или **256 МБ** (отдельная версия, OpenWrt: `256mb-v1`) |
| Wi-Fi | Wi-Fi 6: 2.4 ГГц — до **574 Мбит/с** (2×2), 5 ГГц — до **2402 Мбит/с** (3×3); чип MT7976CN; 2 внешние + 1 внутренняя антенна |
| Ethernet | **1× 2.5 GbE (WAN)** + **1× 1 GbE (LAN)**; PHY Realtek RTL8221B |
| USB | **1× USB 3.0** (в вики OpenWrt указан 3.1) |
| Питание | USB-C, **5 В / 3 А** (с поддержкой PD); потребление до 11.5 Вт, в простое 4.2 Вт |
| Размер / вес | 118 × 80 × 27.5 мм, 160 г |
| Режимы (сток) | Router, AP, Range Extender, WISP, Client |
| VPN (сток) | WireGuard, OpenVPN, IPsec, ZeroTier, PPTP, L2TP (сервер и клиент) |
| Консоль | UART 3.3 В, 115200 8N1; загрузчик U-Boot |

Всё, что ты перечислил (Wi-Fi 6, 512 МБ RAM, 256 МБ флеш, 2 ядра, USB 3.0, WAN 2.5G + LAN 1G), совпадает. Только **256 МБ** — не базовая комплектация, а отдельная версия: на странице Cudy для TR3000 1.0 указано 128 МБ. Точный вариант проверяй на коробке.

---

## 🔍 Что проверить перед покупкой или прошивкой

| Что смотреть | Где | Зачем |
| :--- | :--- | :--- |
| **Объём флеша** (128 / 256 МБ) | этикетка, коробка | от этого зависит образ: `cudy_tr3000-v1` (128) или `cudy_tr3000-256mb-v1` (256) |
| **Серийный номер** | этикетка | начинается с `2543`+ → новый чип флеша, **только OpenWrt ≥ 24.10.5** |
| Заводская прошивка | веб-интерфейс Cudy | промежуточную прошивку ставят **только поверх стока** |
| Ревизия платы | внутри (TechInfoDepot отмечает Rev1.2) | у разных ревизий могут быть отличия |

---

## 🛠️ Установка OpenWrt (метод OEM, по вики OpenWrt)

Метод безопасный: **чужой образ роутер отвергает и не кирпичится**.

1. Определи объём флеша (этикетка/коробка).
2. Скачай **промежуточную прошивку** Cudy (раздел поддержки Cudy или ссылка из их FAQ; файлы подписаны Cudy).
3. Достань из архива `cudy_tr3000-v1-sysupgrade.bin` (128 МБ) или `cudy_tr3000-256mb-v1-sysupgrade.bin` (256 МБ).
4. Загрузи файл через **веб-интерфейс заводской прошивки** (`192.168.1.1`).
5. После перезагрузки открой **LuCI** по `192.168.1.1` (по Ethernet).
6. Скачай финальный образ **sysupgrade** из OpenWrt Firmware Selector (своя версия флеша!).
7. **System → Flash Firmware** в LuCI → залить.

> [!warning] Условия Cudy
> - Промежуточная прошивка ставится, **только когда роутер работает на заводской прошивке**. Если там уже OpenWrt — сначала вернись на официальную прошивку Cudy ([инструкция Cudy](https://www.cudy.com/en-us/blogs/faq/how-to-recovery-the-cudy-router-from-openwrt-firmware-to-cudy-official-firmware)).
> - **Не меняй загрузчик на OpenWrt U-Boot** — вики предупреждает о «soft brick».
> - Если роутер всё же не стартует: восстановление через **UART + TFTP** возможно только с **подписанной прошивкой Cudy**, и нужно разбирать корпус.

После установки сверь, что поставился нужный образ:
```bash
ssh root@192.168.1.1
cat /etc/openwrt_release
ubus call system board        # модель и board_name
cat /proc/mtd                 # раскладка флеша (для сверки 128/256 МБ)
```

---

## 📦 Пакеты: opkg или apk

- **OpenWrt ≤ 24.10** — менеджер **opkg** (см. [OPKG](../../Linux/Package-Manager/OPKG.md)).
- **OpenWrt ≥ 25.12** — менеджер **apk** (Alpine Package Keeper) вместо opkg; названия пакетов в основном те же, команды другие (у проекта есть шпаргалка «opkg → apk»).
- **Entware здесь не нужен**: у OpenWrt собственный репозиторий. Архитектура — `aarch64_cortex-a53` (target `mediatek/filogic`), это **64-бит ARM**, а не armv7, как у RT-AX56U.

---

## 🆚 Против ASUS RT-AX56U (текущий роутер)

| | **Cudy TR3000** | **ASUS RT-AX56U** |
| :--- | :--- | :--- |
| Wi-Fi | Wi-Fi 6, **AX3000** | Wi-Fi 6, AX1800 |
| SoC / арх. | MT7981B, **aarch64** | BCM6755, armv7 |
| RAM / флеш | 512 МБ / 128 или **256 МБ** | 512 МБ / 256 МБ |
| Порты | **2.5G WAN + 1× 1G LAN** | WAN + 4× 1G LAN |
| Прошивка | **OpenWrt** (живые релизы) | Asuswrt-Merlin, ветка 388 заморожена |
| Размер | карманный, питание от USB-C | настольный |

Вывод: TR3000 выигрывает по скорости Wi-Fi и «живой» прошивке, проигрывает по числу портов. На роль основного роутера с несколькими проводными устройствами без свитча он не годится, а как **второй**, дорожный или специализированный (VPN, прокси, точка доступа) — удобен. Что стало с прошивкой RT-AX56U — в [заметке про Merlin](../../Network/Routers/ASUS%20RT-AX56U%20%D0%B8%20Asuswrt-Merlin%20%E2%80%94%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%BE%D0%BD%D1%87%D0%B8%D0%BB%D0%B8%D1%81%D1%8C%20%D0%BD%D0%B0%203004.388.8_4%20%28%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%BF%D1%80%D0%B8%D1%87%D0%B8%D0%BD%D0%B0%2C%20Entware%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%2C%20%D1%81%D1%82%D0%BE%D0%BA%20ASUS%29.md).

---

## ⚖️ Плюсы и минусы

**Плюсы**
- Официальная поддержка **OpenWrt** (с 23.05.4; версия 256 МБ добавлена в июне 2025, бэкпорт в 24.10.3).
- 2.5G WAN, 512 МБ RAM, USB 3.0 (можно подключить накопитель или модем).
- Питание от USB-C (5 В / 3 А): работает от повербанка или адаптера.
- Для своих задач ресурсов достаточно: на нём собирают и прокси-решения (например, гайд по daed на TR3000 на [zhul.in](https://zhul.in/en/2025/02/28/cudy-tr3000-daed-install-record/)).

**Минусы**
- **Только 2 порта** (WAN + 1 LAN): для нескольких проводных клиентов нужен свитч.
- **Две версии флеша** и **риск кирпича на партиях 2543+** при неверном образе.
- Заводской путь прошивки сложнее обычного: через промежуточную прошивку Cudy, а при сбое нужны UART и разборка.
- Фиксированные антенны (две внешние и одна внутренняя) — менять нельзя.

---

## 🖥️ Прошивка с рабочих систем

Всё делается из браузера (веб-интерфейс сток → LuCI), отдельных программ не нужно. Для UART-консоли (аварийный случай, 115200 8N1) подойдёт `picocom`:

| Система | Установка |
| :--- | :--- |
| **Gentoo** | `emerge -av net-dialup/picocom` |
| **Debian / Ubuntu** | `apt install picocom` |
| **Arch** | `pacman -S picocom` |

```bash
picocom -b 115200 /dev/ttyUSB0
```

---

## 🔗 Связанные заметки

- Роутер ASUS RT-AX56U и судьба Merlin: [ASUS RT-AX56U и Asuswrt-Merlin](../../Network/Routers/ASUS%20RT-AX56U%20%D0%B8%20Asuswrt-Merlin%20%E2%80%94%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%BE%D0%BD%D1%87%D0%B8%D0%BB%D0%B8%D1%81%D1%8C%20%D0%BD%D0%B0%203004.388.8_4%20%28%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%BF%D1%80%D0%B8%D1%87%D0%B8%D0%BD%D0%B0%2C%20Entware%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%2C%20%D1%81%D1%82%D0%BE%D0%BA%20ASUS%29.md)
- Менеджер пакетов opkg: [OPKG](../../Linux/Package-Manager/OPKG.md)

## 🔗 Ссылки

- [Cudy TR3000 — страница производителя](https://www.cudy.com/en-us/products/tr3000-1-0) · [OpenWrt Table of Hardware](https://openwrt.org/toh/cudy/tr3000) · [TechInfoDepot](https://techinfodepot.shoutwiki.com/wiki/Cudy_TR3000)
- [Cudy: OpenWrt и промежуточная прошивка](https://www.cudy.com/en-us/blogs/faq/openwrt-software-download) · [Форум OpenWrt: новый чип флеша](https://forum.openwrt.org/t/cudy-started-using-a-new-flash-chip-in-their-ax3000-devices-its-currently-unsupported/243547) · [PR #19167 (версия 256 МБ)](https://github.com/openwrt/openwrt/pull/19167)
- Исходные ссылки (не открылись для проверки): [Wildberries](https://www.wildberries.ru/catalog/1266531412/detail.aspx) · [4PDA](https://4pda.to/forum/index.php?showtopic=1099628)

#Роутер #Cudy #OpenWrt #WiFi6 #MediaTek #Железо
