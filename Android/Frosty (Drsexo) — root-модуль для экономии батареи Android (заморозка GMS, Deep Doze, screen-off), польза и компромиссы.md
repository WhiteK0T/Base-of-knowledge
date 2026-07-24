---
создал заметку: 2026-07-25T05:25:00
author: WhiteK0T
tags:
  - Android
  - Root
  - Magisk
  - KernelSU
  - Батарея
  - GMS
  - Приватность
  - Инструменты
Источник:
  - https://t.me/open_source_friend/5795
  - https://github.com/Drsexo/Frosty
---

# 🧊 Frosty — root-модуль экономии батареи (заморозка GMS + Doze)

**Frosty** ([github.com/Drsexo/Frosty](https://github.com/Drsexo/Frosty)) — **модуль для Magisk / KernelSU / APatch** (то есть только для **рутованного** Android), который экономит батарею: замораживает сервисы **Google Mobile Services (GMS)**, усиливает Doze, оптимизирует поведение при выключенном экране. Всё настраивается через **WebUI**. GPL-3.0, Shell, ~183★, активный (релиз 4.3). Требует **Android 9+**, root-менеджер и установленные Google Play Services.

> [!info] Пост занижает: это не только «заморозка GMS», а целый набор
> Заморозка GMS — лишь одна функция. По README модуль умеет:
> - **App Doze / Deep Doze** (Moderate/Maximum) — агрессивные фоновые ограничения, форс IDLE при выключенном экране, убийца wakelock'ов.
> - **Screen Off Optimization** — по таймеру гасить Wi-Fi/BT/данные/локацию при выключенном экране, чистить RAM, восстанавливать при разблокировке.
> - **Kill Google Tracking** — вырубить аналитику/Clearcut/Phenotype/рекламный трекинг GMS (это и **приватность**).
> - **RAM Optimizer** (ZRAM/LMK/LMKD/PSI), **Kernel Tweaks**, **System Props**, **Log Killing**, **Battery Saver Tuner**.
> - **По умолчанию всё выключено** — включаешь только нужное (хороший безопасный дефолт).

> [!warning] Главное: заморозка GMS — это КОМПРОМИСС «батарея против функций»
> README честно даёт таблицу последствий. Категории GMS:
> | Категория | Что ломается при заморозке |
> | :--- | :--- |
> | 📊 **Telemetry** | ✅ ничего — глушит рекламу/аналитику/трекинг (безопасно, даже полезно) |
> | 🔄 **Background** | ⚠️ автообновления могут задерживаться |
> | 📍 **Location** | Maps, навигация, **Find My Device**, шаринг локации |
> | 📡 **Connectivity** | Chromecast, Quick Share, Fast Pair |
> | ☁️ **Cloud** | **вход в Google**, автозаполнение, пароли, бэкап |
> | 💳 **Payments** | **Google Pay, NFC-оплата** |
> | ⌚ **Wearables** | Wear OS, Google Fit |
> | 🎮 **Games** | достижения/лидерборды/облачные сейвы Play Games |
>
> Классический побочный эффект — **задержка уведомлений** (из-за Doze): мессенджеры надо добавлять в **whitelist Deep Doze**. То есть это ручка, которую крутишь под себя, а не «включил и стало лучше без последствий».

> [!caution] Риски и оговорки
> - **Нужен root** (Magisk 20.4+/KernelSU/APatch) — сам по себе меняет модель безопасности телефона; для многих это стоп-фактор. Magisk-юзерам для доступа к WebUI нужен **WebUI-X**.
> - **Агрессивные режимы** (Deep Doze Maximum, RAM Optimizer Maximum, kernel-твики) могут давать нестабильность/странное поведение приложений — это **power-user-территория**, вводи по одному и проверяй.
> - Проект **небольшой и молодой** (~183★, с фев 2026), но живой; собран на идеях известных модулей (GhostGMS, Universal GMS Doze, DeepDoze Enforcer, SaverTuner — в credits).
> - GPL-3.0; имя «Frosty» зарезервировано за офиц. релизами, форки обязаны переименоваться; автор снимает ответственность за ущерб.

> [!tip] Если хочется приватности/экономии без всего пакета
> Даже без заморозки критичного: категория **Telemetry** + **Kill Google Tracking** дают приватностный выигрыш почти без потерь функций. А **Kernel Tweaks / RAM Optimizer / Deep Doze / Log Killing работают и вовсе без GMS** (для телефонов без Google-сервисов).

## 🖥️ Применимость (это Android-модуль, а не десктоп-софт)

| Где | Как |
| :--- | :--- |
| **Android-телефон с root** (Magisk/KernelSU/APatch), Android 9+ | ✅ целевая среда: поставить через root-менеджер, ребут, включить нужное в WebUI. Прямо по твоему root-профилю |
| **Твои Gentoo/Debian/Arch/Windows и RT-AX56U** | ➖ неактуально — модуль живёт на самом телефоне, к десктопам/роутеру отношения не имеет |

## 🔗 Связанные заметки

- Что такое Magisk/KernelSU/APatch и весь мир рутинга: [awesome-android-root — каталог рутинга (Magisk/KernelSU/APatch)](awesome-android-root%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D1%80%D1%83%D1%82%D0%B8%D0%BD%D0%B3%D0%B0%20Android%20%28Magisk-KernelSU-APatch%2C%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D0%B8%2C%20%D0%B3%D0%B0%D0%B9%D0%B4%D1%8B%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/Drsexo/Frosty](https://github.com/Drsexo/Frosty)
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5795)

#Android #Root #Magisk #KernelSU #Батарея #GMS #Приватность #Инструменты
