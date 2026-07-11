---
создал заметку: 2026-07-11T06:10:00
author: WhiteK0T
tags:
  - Windows
  - Firewall
  - Network
  - Security
  - Privacy
  - OpenSource
Источник:
  - https://t.me/open_source_friend/5771
  - https://github.com/tnodir/fort
---

# 🧱 Fort Firewall (tnodir) — опенсорсный брандмауэр Windows

[**Fort Firewall**](https://github.com/tnodir/fort) (автор **tnodir**, **C++/Qt**, лицензия **GPL-3.0**, ~3.17k★, живёт с 2014 г., v3.19.9, активно пилится) — бесплатный **брандмауэр для Windows** с фильтрацией трафика **по приложениям**: разрешай/блокируй сеть каждой программе, лимитируй скорость, смотри соединения и графики трафика в реальном времени. По духу — «Little Snitch для Windows» с открытым кодом. Работает на **Windows 7+** (x86), для **Windows 10 1809+** — x86_64 (есть и ARM64).

## ✨ Что умеет

- **Правила по приложениям** с шаблонами путей (**wildcard**), правила по **родительскому процессу**, фильтрация служб внутри `svchost.exe` **по имени сервиса**.
- **Группы приложений** с **лимитом скорости/полосы** (bandwidth limiting) — можно резать скорость отдельным категориям.
- **Blocklist-зоны** — подгружаемые списки для блокировки диапазонов/адресов.
- **Мониторинг в реальном времени:** статистика по соединениям + **графики полосы** пропускания.
- **Режимы фильтрации**, расписания, логирование. **Без телеметрии**, GPL — код открыт.

## ⚠️ Что важно понимать (факты против хайпа)

> [!caution] Главный нюанс: Fort несовместим с HVCI (Core Isolation) — придётся отключить hardening
> Fort ставит **собственный kernel-драйвер** (на базе **WFP**, Windows Filtering Platform — как у NetLimiter/Portmaster). Проблема: этот драйвер **динамически исполняет код в executable-страницах памяти** (чтобы обойти ограничения EV-сертификата), а это **конфликтует с HVCI** (Hypervisor-protected Code Integrity, он же **Целостность памяти / Core Isolation**). Итог — чтобы установить Fort, нужно **выключить «Целостность памяти» (Core Isolation → Memory Integrity)**.
> Это **честный минус**: ради инструмента безопасности ты **отключаешь заметную функцию защиты ядра Windows**. Плюс само поведение драйвера (runtime-исполнение кода, W^X-нарушение) — техника, пограничная с тем, что делают руткиты. Не значит «вредонос», но **взвесь tradeoff** и решай по своей модели угроз.

> [!warning] Свой драйвер = мощнее, но и риск/совместимость
> Собственный callout-драйвер даёт **гибкую фильтрацию и лимиты скорости** (чего WFP-провайдеры не всегда могут), но исторически бывали **BSOD при апгрейдах Windows** (напр. на ранних 22H2). Обновляй Fort под свежую Windows, держи точку отката. На чувствительных/рабочих машинах сначала протестируй.

> [!tip] Если отключать HVCI не хочется — есть HVCI-совместимые альтернативы
> **simplewall** и **TinyWall** используют **WFP-провайдер без своего драйвера** → **работают с включённым Core Isolation** (но и без bandwidth-лимитов Fort). Ещё в нише: **Portmaster** (opensource, свой драйвер, DNS-фильтрация), **GlassWire**, **NetLimiter** (платный), а также штатный **Windows Defender Firewall** + фронтенд **Windows Firewall Control**. Fort выбирают за **per-app + лимиты скорости + открытость**; simplewall — за **лёгкость и совместимость с hardening**.

## 🔧 Установка (Windows)

- Скачай инсталлятор с [GitHub Releases](https://github.com/tnodir/fort/releases) (x86_64 для Win10 1809+, x86 для Win7+).
- Нужен свежий **Visual C++ Redistributable** (x64/x86/ARM64).
- Если инсталлятор ругается на HVCI — отключи **«Целостность памяти»** в *Безопасность Windows → Безопасность устройства → Ядро → Изоляция ядра*, перезагрузись.
- Портативной версии официально нет (ставится как служба + драйвер).

## 🖥️ По системам

| Система | Применимость |
| :--- | :--- |
| **Windows 7+ / 10 1809+ / 11** | ✅ Целевая ОС (x86 / x86_64 / ARM64). Учитывай нюанс HVCI выше |
| **Gentoo** (основная) | **N/A** — это Windows-фаервол. На Linux ту же задачу решают **nftables/iptables**, а «per-app GUI как Fort/Little Snitch» — это **OpenSnitch** (аналог: спрашивает по каждому исходящему соединению приложения) |
| **Debian / Ubuntu / Arch** | **N/A** — см. выше: nftables + OpenSnitch/Douane для per-app |
| **Entware / RT-AX56U** | **N/A** — на роутере фильтрация делается его прошивкой/iptables; Fort тут ни при чём. Сетевую блокировку рекламы/телеметрии на уровне сети закрывает [Pi-hole](../Apps/Pi-hole%20%E2%80%94%20%D1%81%D0%B5%D1%82%D0%B5%D0%B2%D0%BE%D0%B9%20%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D1%8B%20%D0%B8%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28DNS-sinkhole%29.md) |

## 🔗 Ссылки

- Репозиторий: [github.com/tnodir/fort](https://github.com/tnodir/fort) (GPL-3.0) · [Wiki/FAQ](https://github.com/tnodir/fort/wiki) · [заметка про HVCI](https://github.com/tnodir/fort/wiki/HVCI)
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5771)
- Связанные: [GTweak — твикер-деблоатер Windows](GTweak%20%E2%80%94%20%D0%BF%D0%BE%D1%80%D1%82%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9%20%D1%82%D0%B2%D0%B8%D0%BA%D0%B5%D1%80-%D0%B4%D0%B5%D0%B1%D0%BB%D0%BE%D0%B0%D1%82%D0%B5%D1%80%20Windows%20%28%D0%BF%D1%80%D0%B8%D0%B2%D0%B0%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C%2C%20%D1%81%D0%BB%D1%83%D0%B6%D0%B1%D1%8B%2C%20%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%B0%D1%86%D0%B8%D1%8F%20HWID-KMS%29.md) · [System Informer — мониторинг процессов](System%20Informer%20%E2%80%94%20%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3%20%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%BE%D1%85%D0%BE%D1%82%D0%B0%20%D0%BD%D0%B0%20%D0%BC%D0%B0%D0%BB%D0%B2%D0%B0%D1%80%D1%8C%20%28%D0%BF%D1%80%D0%B5%D0%B5%D0%BC%D0%BD%D0%B8%D0%BA%20Process%20Hacker%29.md) · [AutoSettingsPS — твикер приватности на PowerShell](AutoSettingsPS%20%28westlife%29%20%E2%80%94%20portable-%D1%82%D0%B2%D0%B8%D0%BA%D0%B5%D1%80%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B0%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B8%20%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20Windows%20%D0%BD%D0%B0%20PowerShell%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D1%80%D0%B8%D1%81%D0%BA%20%D1%81%D0%B1%D0%BE%D1%80%D0%BE%D0%BA%29.md) · [privacy-settings — настройки приватности сервисов/ОС](../Security/privacy-settings%20%28StellarSand%29%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4%20%D0%BF%D0%BE%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%D0%BC%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B0%D1%82%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B4%D0%BB%D1%8F%2060%2B%20%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9%2C%20%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BE%D0%B2%20%D0%B8%20%D0%9E%D0%A1.md)

#Windows #Firewall #Network #Security #Privacy #OpenSource
