---
создал заметку: 2026-06-16T18:10:00
author: WhiteK0T
tags:
  - BrowserExtension
  - Userscript
  - Tampermonkey
  - JavaScript
Источник:
  - https://www.tampermonkey.net
  - https://github.com/Tampermonkey/tampermonkey
---

# 🐒 Tampermonkey — менеджер юзерскриптов

**Tampermonkey** ([tampermonkey.net](https://www.tampermonkey.net)) — самый популярный **менеджер юзерскриптов**: расширение браузера, которое устанавливает, обновляет и запускает пользовательские JavaScript-скрипты, меняющие поведение сайтов (добавить кнопку, убрать элемент, автоматизировать действие). Бесплатное, но **проприетарное** (открытая альтернатива — Violentmonkey). Именно через него ставится, например, [VOT (закадровый перевод видео)](VOT%20%E2%80%94%20закадровый%20перевод%20и%20озвучка%20видео%20%28Voice-Over-Translation%29.md).

## 🧬 Что такое юзерскрипт

Это `.js`-файл с **метаблоком** `==UserScript==`, который говорит менеджеру, где и как запускаться:

```javascript
// ==UserScript==
// @name         Пример
// @namespace    http://example.com/
// @version      1.0
// @description  Что делает скрипт
// @match        https://*.youtube.com/*
// @grant        GM_addStyle
// @run-at       document-idle
// ==/UserScript==

(function () {
  'use strict';
  GM_addStyle('body { font-family: monospace; }');
})();
```

| Директива | Смысл |
| :--- | :--- |
| `@match` / `@include` | на каких URL запускать |
| `@grant` | какие `GM_*`-API разрешить (или `none`) |
| `@run-at` | момент запуска (`document-start`/`idle`/`end`) |
| `@require` | подключить внешнюю библиотеку (jQuery и т.п.) |
| `@version` | для автообновления |

## 🧰 Что умеет (GM-API)

| API | Назначение |
| :--- | :--- |
| `GM_setValue` / `GM_getValue` | постоянное хранилище скрипта |
| `GM_xmlhttpRequest` | **кросс-доменные** запросы (в обход CORS) |
| `GM_addStyle` | вставить CSS |
| `GM_registerMenuCommand` | свой пункт в меню Tampermonkey |
| `GM_setClipboard` / `GM_notification` | буфер обмена / уведомления |

Плюс встроенный редактор скриптов, автообновление по `@version`, синхронизация настроек (через облако/файл), импорт-экспорт.

## 📦 Установка

Работает на уровне **браузера**, от ОС не зависит (одинаково на Gentoo, Debian/Ubuntu, Arch, Windows). Ставится из магазина расширений браузера:

- **Chrome / Edge / Brave / Opera / Vivaldi** — Chrome Web Store.
- **Firefox** — addons.mozilla.org.
- **Safari** — App Store (отдельная сборка).

> [!warning] Chrome (Manifest V3): включи «Allow user scripts»
> С переходом Chrome на Manifest V3 юзерскрипты требуют явного разрешения. В **Chrome 138+** (Tampermonkey 5.3+): правый клик по иконке → «Управление расширением» → включить тумблер **«Allow User Scripts» (Разрешить пользовательские скрипты)**. На более старых версиях вместо этого нужно включить **режим разработчика** на `chrome://extensions`. Без одного из этих шагов скрипты молча не запускаются.

## 🛒 Где брать скрипты

- **[Greasy Fork](https://greasyfork.org)** — крупнейший каталог (open-source скрипты).
- **[OpenUserJS](https://openuserjs.org)** — ещё один репозиторий.
- GitHub-ссылки на `*.user.js` (Tampermonkey сам распознаёт и предлагает установку).

## ⚖️ Tampermonkey vs альтернативы

| | Tampermonkey | Violentmonkey | Greasemonkey |
| :--- | :--- | :--- | :--- |
| Лицензия | проприетарное (free) | **open-source (MIT)** | open-source |
| Браузеры | Chrome/FF/Edge/Safari/Opera/Brave/Vivaldi | Chrome/FF/Edge | **только Firefox** |
| GM-API | самый полный | хороший | базовый |
| Кому | максимум совместимости | нужен открытый код | олдскул на Firefox |

## ⚠️ Безопасность

> [!danger] Юзерскрипт = чужой код с правами на страницы
> Скрипт выполняется на сайтах, может читать содержимое страниц, а через `GM_xmlhttpRequest` — слать данные куда угодно в обход CORS. Ставь только из **доверенных** источников и проглядывай код (особенно `@match *://*/*` — работает на всех сайтах, и сетевые запросы). Вредоносный юзерскрипт способен красть сессии/данные.

## 💡 Кому полезно

- Кастомизируешь сайты, автоматизируешь рутину в браузере, ставишь готовые скрипты (перевод, SponsorBlock-подобное, фиксы UI).
- Нужен «движок» для расширений-юзерскриптов вроде [VOT](VOT%20%E2%80%94%20закадровый%20перевод%20и%20озвучка%20видео%20%28Voice-Over-Translation%29.md).
- Нужен **открытый код** — бери Violentmonkey (тот же формат скриптов).

## 🔗 Ссылки

- Сайт: [tampermonkey.net](https://www.tampermonkey.net) · репозиторий: [github.com/Tampermonkey/tampermonkey](https://github.com/Tampermonkey/tampermonkey)
- Каталоги скриптов: [Greasy Fork](https://greasyfork.org) · [OpenUserJS](https://openuserjs.org)
- Связанные: [VOT — закадровый перевод видео](VOT%20%E2%80%94%20закадровый%20перевод%20и%20озвучка%20видео%20%28Voice-Over-Translation%29.md)

#BrowserExtension #Userscript #Tampermonkey #JavaScript
