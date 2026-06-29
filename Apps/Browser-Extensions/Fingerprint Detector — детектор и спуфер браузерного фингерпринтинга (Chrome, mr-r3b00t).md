---
создал заметку: 2026-06-29T17:00:00
author: WhiteK0T
tags:
  - BrowserExtension
  - Приватность
  - Fingerprinting
  - AntiTracking
  - Chrome
  - JavaScript
Источник:
  - https://t.me/bugnotfeature/26146
  - https://github.com/mr-r3b00t/fingerprintdetector
---

# 🕵️ Fingerprint Detector — детектор и спуфер браузерного фингерпринтинга

[**Fingerprint Detector**](https://github.com/mr-r3b00t/fingerprintdetector) (*mr-r3b00t* — Daniel Card / **Xservus Ltd**, **JavaScript**, ~**118★**) — расширение для **Chrome**, которое в реальном времени **перехватывает вызовы fingerprinting-API** и показывает, кто и как тебя «снимает» по цифровому отпечатку (без cookie). Покрывает 12+ векторов: **Canvas, WebGL, Audio, шрифты, плагины, железо, экран, WebRTC, Battery, User-Agent, хранилище, сеть**. Три режима работы:

> [!info] Три режима
> - **Detect** — пассивный мониторинг: только показывает, что именно сайт пытается собрать, ничего не меняя.
> - **Ghost** — отдаёт **самые распространённые** значения, чтобы «слиться с миллионами Chrome», + блокирует извлечение пикселей canvas, audio-фингерпринт и **утечку IP через WebRTC**.
> - **Spoof** — подставляет **фиксированную фейковую личность** (Chrome 120 на Windows 10 с графикой Intel UHD 630).

## 🧪 Факты против хайпа

> [!warning] «Уничтожаем ВСЮ слежку» — сильное преувеличение
> Фингерпринтинг — лишь **один** из векторов слежки. Расширение **не закрывает**: cookie и трекеры (нужен uBlock Origin/Pi-hole), вход по аккаунту (login-based tracking), **IP-адрес**, серверные и сетевые отпечатки (**TLS/JA3-JA4**, HTTP/2). «Вся слежка» так не выключается.

> [!caution] Спуфинг может сделать тебя **заметнее**, а не незаметнее
> Это фундаментальный парадокс анти-фингерпринтинга:
> - **редкие/несогласованные** значения выделяют. Фиксированный «Chrome 120 / Win10 / UHD 630», который **не совпадает** с твоим реальным часовым поясом, языком, экраном, шрифтами и поведением WebGL, даёт **противоречивый** отпечаток → ты уникальнее.
> - сам факт «здесь стоит анти-фингерпринт» — **отдельный сигнал**: продвинутые трекеры детектят перехват canvas/audio (тайминги, `toString` переопределённых функций, проверки «нативности»).
> - JS-перехват **обходим** и не покрывает то, что считается **вне** JS (TLS/сетевой отпечаток, IP).
> Зрелые подходы строят на **единообразии** (Tor Browser — все пользователи выглядят одинаково) или контролируемой рандомизации (**Brave** farbling, Firefox **RFP**), а не на статичной подмене в одиночном браузере.

> [!danger] Статус проекта и лицензия — читай до установки
> - **Не open-source.** Лицензия **проприетарная**: *«Copyright Xservus Limited. All rights reserved. This software is proprietary. No license is granted for redistribution, modification, or commercial use»*. Исходники видны на GitHub, но это **не** свободная лицензия (GitHub поле license — пусто).
> - **Ранний тест-билд.** Сам автор: *«A very in development/test… use at own risk»*, в README — *«This is a test version… no warranty, no support, no guarantee of functionality»*. Последний коммит — **8 апреля 2026** (репо создан в тот же день): по сути **заброшенный** прототип, без обновлений.
> - **Только Chrome, ставится распакованным** (developer mode «Load unpacked») — **нет** авто-обновлений и проверки Web Store; ты загружаешь сырой код. Перед установкой просмотри код/сделай аудит сам.

> [!tip] Реальная польза — режим Detect
> Самое ценное здесь — **образовательный** Detect: наглядно видеть, **кто и какие API** дёргает для отпечатка на конкретном сайте. Как учебный «рентген» фингерпринтинга — отлично. Как «щит от всей слежки» — нет: для защиты надёжнее **Tor Browser** (анонимность), **Brave**/**Firefox RFP** (повседневно) + **uBlock Origin** и [Pi-hole](../Pi-hole%20%E2%80%94%20%D1%81%D0%B5%D1%82%D0%B5%D0%B2%D0%BE%D0%B9%20%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D1%8B%20%D0%B8%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28DNS-sinkhole%29.md).

## 💻 Как это ложится на твои системы

Это расширение **Chrome/Chromium** — кроссплатформенно на любом десктопе с Chromium, грузится распакованным из папки репозитория.

| Система | Применимость |
| :--- | :--- |
| **Gentoo** (основная) | `emerge www-client/chromium` (или `google-chrome`), затем `chrome://extensions` → Developer mode → Load unpacked → папка репо |
| **Debian / Ubuntu** | `sudo apt install chromium` (или установить Chrome), далее так же через `chrome://extensions` |
| **Arch** | `sudo pacman -S chromium`, далее так же |
| **Firefox** | **Не поддерживается** (расширение под Chrome MV; на Firefox нативно лучше **RFP** `privacy.resistFingerprinting`) |
| **Entware / RT-AX56U** | **N/A** — на роутере нет браузера; сетевой уровень приватности там закрывает не это, а DNS-sinkhole/блокировки |

## 💡 Кому полезно

- **Тем, кто хочет понять фингерпринтинг** — Detect-режим как наглядный анализатор того, что собирают сайты.
- **Пентестерам/исследователям приватности** — быстро увидеть набор векторов на странице.
- **Не** тем, кто ищет «поставил и невидим»: для реальной защиты — Tor/Brave/Firefox RFP + блокировщики, а не одиночный спуфер (который может повысить уникальность).

## 🔗 Ссылки

- Репозиторий: [github.com/mr-r3b00t/fingerprintdetector](https://github.com/mr-r3b00t/fingerprintdetector) (проприетарный, тест-билд)
- Проверить свой отпечаток: [coveryourtracks.eff.org](https://coveryourtracks.eff.org/) (бывш. Panopticlick) · [amiunique.org](https://amiunique.org/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26146)
- Связанные: [Pi-hole (сетевой блокировщик рекламы и телеметрии)](../Pi-hole%20%E2%80%94%20%D1%81%D0%B5%D1%82%D0%B5%D0%B2%D0%BE%D0%B9%20%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D1%89%D0%B8%D0%BA%20%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D1%8B%20%D0%B8%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28DNS-sinkhole%29.md) · [Tampermonkey (менеджер юзерскриптов)](Tampermonkey%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D1%8E%D0%B7%D0%B5%D1%80%D1%81%D0%BA%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B2.md)

#BrowserExtension #Приватность #Fingerprinting #AntiTracking #Chrome #JavaScript
