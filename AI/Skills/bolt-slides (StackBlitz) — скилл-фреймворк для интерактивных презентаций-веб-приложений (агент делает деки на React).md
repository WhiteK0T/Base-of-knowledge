---
создал заметку: 2026-07-24T21:20:00
author: WhiteK0T
tags:
  - AI
  - Skills
  - Презентации
  - Frontend
  - ClaudeCode
  - Ресурсы
Источник:
  - https://t.me/bugnotfeature/26533
  - https://github.com/stackblitz/bolt-slides
---

# 🖥️ bolt-slides — презентации, которые являются веб-приложениями

**bolt-slides** ([github.com/stackblitz/bolt-slides](https://github.com/stackblitz/bolt-slides)) — от **StackBlitz** (создатели [Bolt.new](https://bolt.new)): это **React/Vite-фреймворк для слайдов + встроенный скилл** (`.bolt/skills/slides/SKILL.md`), который учит ИИ-агента ([Claude Code](../Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md), Codex, Cursor, Bolt) собирать **интерактивную презентацию по одному промпту**. Каждый слайд — обычный **React-компонент**: живые данные, графики, 3D, анимации, рабочие кнопки/формы. Движок — в стиле Slidev (сайдбар, grid, click-builds, аннотации, presenter mode). MIT, TypeScript, свежий (создан 14.07.2026, ~630★).

> [!info] Отделяем факты от рекламы поста
> | Заявление поста | Реально |
> | :--- | :--- |
> | «из коробки генерирует красивые HTML-презентации» | почти: это **React/Vite-проект**, а не один статический `.html`. Запускаешь (`npm run dev`) или открываешь в Bolt/StackBlitz; на выходе — **веб-приложение**, а не файл слайдов |
> | «по одному текстовому запросу» | ✅ но работу делает **твой агент** по встроенному `SKILL.md` — это его токены/подписка; качество зависит от модели |
> | «слайды интерактивны: кнопки, формы, графики, 3D, данные по API, адаптив» | ✅ всё правда — слайды это React + библиотека компонентов (Charts, StatGrid, Globe, TiltCard…), можно `fetch` живых данных |
> | «работает с Claude Code, Codex, Cursor, Bolt» | ✅ скилл агент-независимый |
> | «делиться по ссылке без экспорта» | ✅ но «ссылка» = **где-то захостить** веб-апп (Bolt/StackBlitz или свой деплой). Не «магия без хостинга», а обычный деплой SPA |

> [!caution] Чего он НЕ делает — и когда не брать
> - **Это не PowerPoint/PDF-генератор.** На выходе — **кодовая база (React)**, а не `.pptx`/`.pdf`. Нужен статичный дек для отправки/печати — это не сюда (максимум print-to-PDF из браузера).
> - **Нужен фронтенд-тулчейн**: Node/npm, React/Vite и агент. Для «быстро набросать 5 слайдов текстом» проще Marp/Slidev/обычный редактор — bolt-slides это **оверкилл** для простого.
> - **Воронка StackBlitz**: кнопки «Open in Bolt» ведут в их хостинг/продукт. Само по себе MIT и локально работает, но «поделиться ссылкой» удобнее всего именно через их платформу.
> - **Очень молодой** (пара дней коммитов на момент заметки) — API компонентов может меняться.

> [!tip] Зачем он вообще — борьба со «слоп-слайдами»
> Мотивация авторов прямая: *«AI-презентации обычно слоп — генеричные макеты, простыни буллетов»*. bolt-slides даёт агенту **строительные блоки с вкусом** (типографика, макеты, анимации, 9 готовых тем в `tokens.css`), чтобы дек был не стыдным. Это тот же анти-слоп посыл, что у [epstein.md](../Prompts/epstein.md%20%28Shipper%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B3%D0%B0%D0%BD%D1%82%D1%81%D0%BA%D0%B8%D0%B9%20.md-%D1%84%D0%B0%D0%B9%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%ABAI-%D1%81%D0%BB%D0%BE%D0%BF%D0%B0%C2%BB%20%D0%B2%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B5%20%28%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D1%82%D0%B5%D0%BD%D0%B8%2C%20%D1%8D%D0%BC%D0%BE%D0%B4%D0%B7%D0%B8%2C%20~350%20%D0%98%D0%98-%D1%81%D0%BB%D0%BE%D0%B2%29.md) и [apple-design](apple-design%20%28Emil%20Kowalski%29%20%E2%80%94%2017%20%D0%BF%D1%80%D0%B8%D0%BD%D1%86%D0%B8%D0%BF%D0%BE%D0%B2%20Apple-%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B0%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81%D0%BE%D0%B2%20%D1%81%20%D0%BA%D0%BE%D0%B4%D0%BE%D0%BC%20%28WWDC%20Designing%20Fluid%20Interfaces%29.md), только для презентаций.

## 🧩 Что внутри

- **Авторинг**: каждый ребёнок `<Deck>` — слайд; `<Build at={n}>` — пошаговое раскрытие по кликам; `notes="…"` — заметки докладчика.
- **Библиотека компонентов**: `Cover`/`Agenda`/`Split`/`Bento`; данные — `Charts` (bar/line/donut), `Table`, `StatGrid`, `BigNumber`, `CountUp`; сторителлинг — `Quote`/`Timeline`/`Steps`; продукт — `CodeWindow`/`BrowserFrame`/`Pricing`; «флэр» — `Globe`/`TiltCard`/`Marquee`. Все адаптивны.
- **Презентер**: сайдбар (`S`), grid всех слайдов (`G`), аннотации пером (`A`), presenter mode во второй вкладке с таймером и синком через `BroadcastChannel` (`P`), deep-link на слайд (`/#7`).
- **Темизация**: все цвета/шрифты/радиусы в `:root` (`src/styles/tokens.css`) — поменял `--primary`, перекрасился весь дек.

## 🛠️ Как начать

```bash
git clone https://github.com/stackblitz/bolt-slides
cd bolt-slides && npm install && npm run dev
# откроется демо на 26 слайдов; удали демо в src/App.tsx и пиши свои
```

Либо открыть репо в **Bolt** и дать промпт вида «*собери дек, питчащий X для Y*» — встроенный `SKILL.md` подхватит тему, макеты и текст.

## 🖥️ Применимость на системах владельца

| Система | Как использовать |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | ✅ Node/npm + агент на десктопе; собираешь и показываешь дек в браузере, деплоишь куда угодно (свой сервер/Netlify/Vercel/GitHub Pages) |
| **Entware / RT-AX56U** | ➖ сборка/агент — на десктопе. Роутер разве что как **статический хостинг** готового билда по LAN, не более |

## 🔗 Связанные заметки

- Дизайн-системы «с вкусом» для агентов: [Open Design — альтернатива Claude Design](../Open%20Design%20%E2%80%94%20%D0%BE%D0%BF%D0%B5%D0%BD%D1%81%D0%BE%D1%80%D1%81%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BB%D1%8C%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%B0%20Claude%20Design%20%28%D1%81%D0%BA%D0%B8%D0%BB%D0%BB%D1%8B%20%2B%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B%29.md)
- Анти-слоп для интерфейсов/дизайна: [apple-design (17 принципов)](apple-design%20%28Emil%20Kowalski%29%20%E2%80%94%2017%20%D0%BF%D1%80%D0%B8%D0%BD%D1%86%D0%B8%D0%BF%D0%BE%D0%B2%20Apple-%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B0%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81%D0%BE%D0%B2%20%D1%81%20%D0%BA%D0%BE%D0%B4%D0%BE%D0%BC%20%28WWDC%20Designing%20Fluid%20Interfaces%29.md) · [epstein.md (против AI-слопа в дизайне)](../Prompts/epstein.md%20%28Shipper%29%20%E2%80%94%20%D0%B3%D0%B8%D0%B3%D0%B0%D0%BD%D1%82%D1%81%D0%BA%D0%B8%D0%B9%20.md-%D1%84%D0%B0%D0%B9%D0%BB%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%C2%ABAI-%D1%81%D0%BB%D0%BE%D0%BF%D0%B0%C2%BB%20%D0%B2%20%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD%D0%B5%20%28%D0%B3%D1%80%D0%B0%D0%B4%D0%B8%D0%B5%D0%BD%D1%82%D1%8B%2C%20%D1%82%D0%B5%D0%BD%D0%B8%2C%20%D1%8D%D0%BC%D0%BE%D0%B4%D0%B7%D0%B8%2C%20~350%20%D0%98%D0%98-%D1%81%D0%BB%D0%BE%D0%B2%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/stackblitz/bolt-slides](https://github.com/stackblitz/bolt-slides) · Скилл: [.bolt/skills/slides/SKILL.md](https://github.com/stackblitz/bolt-slides/blob/main/.bolt/skills/slides/SKILL.md) · Открыть в [Bolt](https://bolt.new/github.com/stackblitz/bolt-slides)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/26533)

#AI #Skills #Презентации #Frontend #ClaudeCode #Ресурсы
