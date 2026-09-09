---
создал заметку: 2026-09-09T22:00:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Агенты
  - Видео
  - Anthropic
Источник:
  - https://t.me/bugnotfeature/27220
  - https://claude.com/blog/getting-started-with-loops
---

# 🎥 Гайд по настройке Claude Code с нуля — разбор поста

Разбор [поста «Не баг, а фича» от 21.08.2026](https://t.me/bugnotfeature/27220): «мощнейший гайд от инженера Anthropic по созданию полной конфигурации Claude Code с нуля».

Видео вложено прямо в Telegram, **без ссылки на первоисточник и без указания автора**. Проверил, что смог: одну фактическую ошибку нашёл сразу, а само видео опознать не удалось.

## ✅ Проверка утверждений

| Утверждение | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «От **инженера** Anthropic» | ❌ Неверно | Cat Wu — **product manager** и Head of Product для Claude Code, а не инженер |
| «Через **десять минут** готовая конфигурация» | ⚠️ Не подтвердил | Ближайшее официальное видео Anthropic с Cat Wu идёт **14:03**, подкаст — 40:36. Десятиминутного не нашёл |
| «Промптинг → Циклы → Агенты → Системы самоулучшения» | ✅ Реальная рамка | Совпадает с материалами Anthropic про **петли (loops)** |
| «Даже промптов не надо» | ✅ Смысл передан верно | Тезис команды Claude Code: не промптить Claude, а строить систему, которая промптит себя сама |
| «Сканирование кодовой базы, интеграция MCP» | ✅ Правдоподобно | Стандартный набор настройки: `CLAUDE.md`, MCP-серверы, скиллы, хуки, субагенты |
| «Курс стоил бы больше $1000» | ⚠️ Риторика | Проверить нельзя. Заодно: у Anthropic есть **бесплатная** академия с 24 курсами |
| Ссылка на источник | ❌ Отсутствует | Видео залито в канал без атрибуции |

## 👤 Про Cat Wu

Единственная проверяемая фактическая ошибка поста. **Cat Wu** — продакт-менеджер Claude Code в Anthropic, руководитель продукта. Не инженер. Основатели Claude Code — Boris Cherny и команда; Cat Wu отвечает за продуктовую часть и часто выступает публично.

## 🔍 Какое это видео — установить не удалось

Пост не даёт ни ссылки, ни названия. Проверил шесть публичных видео с Cat Wu, ни одно не совпало с описанием («пустой терминал → готовая конфигурация за 10 минут»):

| Видео | Канал | Длина | О чём |
| :--- | :--- | :--- | :--- |
| [Building and prototyping with Claude Code](https://www.youtube.com/watch?v=DAQJvGjlgVM) | **Anthropic** (офиц.) | 14:03 | Cat Wu и Alex Albert о прототипировании фич и практиках работы с SDK |
| [Inside How the Claude Code Team Ships at Lightning Speed](https://www.youtube.com/watch?v=jmHBMtpR36M) | Peter Yang | 40:36 | подкаст о том, как команда работает изнутри |
| [From Boris's Notebook to the Whole Company](https://www.youtube.com/watch?v=wo_CbgoyFLY) | O'Reilly | — | как Claude Code вырос из личного инструмента |
| [How Should Junior Engineers Use Claude Code?](https://www.youtube.com/watch?v=qnSuOFXkEH0) | O'Reilly | — | про junior-разработчиков |
| [My Claude Fixed My Bug Before I Did](https://www.youtube.com/watch?v=4h0i7YiS9io) | O'Reilly | — | из той же серии |
| [Claude Fable, Claude Tag и культура Anthropic](https://www.youtube.com/watch?v=uU5Gv2h8-9g) | AI Engineer | — | Cat Wu и Thariq Shihipar с Simon Willison |

> [!note] Честно о границах проверки
> Официальное видео Anthropic с Cat Wu ближе всего по формату, но оно про **прототипирование фич и SDK**, а не про «настроить конфиг с нуля». Возможно, в посте другое, более свежее видео, которого нет в поисковой выдаче. Утверждать, какое именно, я не могу.

## 🔁 Что за «Циклы» и «системы самоулучшения»

Эта часть поста опирается на реальную концепцию Anthropic — **петли (loops)**: агент повторяет цикл работы, пока не выполнится условие остановки. Отсюда и тезис «промптов не надо»: вместо ручного промпта строится система, которая формирует запросы себе сама.

Вторая половина — **самоулучшение**: каждая ошибка Claude превращается в переиспользуемую инструкцию в `CLAUDE.md` или в скилл. Так конфигурация со временем чинит сама себя.

В базе эта тема уже разобрана предметно и по первоисточникам:

- [Getting Started with Loops (Anthropic)](../Loops/Getting%20Started%20with%20Loops%20%28Anthropic%29%20%E2%80%94%204%20%D1%82%D0%B8%D0%BF%D0%B0%20%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28goal%2C%20loop%2C%20schedule%29.md) — четыре типа циклов;
- [Loops — обзор сайта и каталог петель](../Loops/Loops%20%E2%80%94%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20%D0%B8%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%BF%D0%B5%D1%82%D0%B5%D0%BB%D1%8C.md) — плюс шесть готовых петель рядом в той же папке.

## 🛠️ Из чего на самом деле состоит настройка

Пять слоёв, которые обычно и показывают в таких гайдах:

| Слой | Зачем |
| :--- | :--- |
| `CLAUDE.md` | правила проекта, память |
| **MCP-серверы** | доступ к БД, логам, GitHub, браузеру |
| **Скиллы** | повторяемые многошаговые процедуры |
| **Хуки** | детерминированная автоматизация и проверки |
| **Субагенты** | изолированный ресёрч и ревью |

Начинать со всего сразу не нужно: один хорошо написанный `CLAUDE.md` уже даёт заметный эффект. Практическая часть — в [шпаргалке](Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md), про MCP — в [отдельной заметке](Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md).

## 💡 Итог

- Тема настоящая и полезная, рамка «промптинг → циклы → агенты → самоулучшение» отражает реальный подход команды Claude Code.
- **Cat Wu — product manager, а не инженер.** Единственная проверяемая ошибка поста.
- **Ссылки на источник в посте нет**, видео опознать не удалось: ни одно из шести публичных выступлений Cat Wu не совпадает с описанием.
- «Курс стоил бы $1000» — риторика. У Anthropic есть [бесплатная академия](../../Education/Claude%20Academy%20%28Anthropic%29%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D1%8F%20%D0%BF%D0%BE%20Claude%20%2824%20%D0%BA%D1%83%D1%80%D1%81%D0%B0%20%D0%B8%20293%20%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B0%2C%20%D0%BD%D0%BE%20%D1%83%D1%80%D0%BE%D0%B2%D0%BD%D0%B5%D0%B9%20%D1%82%D1%80%D0%B8%2C%20%D0%B0%20%D0%BD%D0%B5%20%D1%88%D0%B5%D1%81%D1%82%D1%8C%3B%20%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D0%B2%20%D0%BF%D1%8F%D1%82%D1%8C%29.md) с 24 курсами, включая «Claude Code in Action» и большой курс по API.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/27220](https://t.me/bugnotfeature/27220) (21.08.2026)
- Официальное видео с Cat Wu: [Building and prototyping with Claude Code](https://www.youtube.com/watch?v=DAQJvGjlgVM) (Anthropic, 14:03)
- Про петли: [Loop engineering — Getting started with loops](https://claude.com/blog/getting-started-with-loops)
- Связанные: [Claude Code — гайд](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md) · [Claude Code — шпаргалка команд](Claude%20Code%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4.md) · [MCP — серверы Model Context Protocol](Tooling/MCP%20%E2%80%94%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D1%8B%20Model%20Context%20Protocol.md) · [Getting Started with Loops](../Loops/Getting%20Started%20with%20Loops%20%28Anthropic%29%20%E2%80%94%204%20%D1%82%D0%B8%D0%BF%D0%B0%20%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%28goal%2C%20loop%2C%20schedule%29.md) · [Claude Academy](../../Education/Claude%20Academy%20%28Anthropic%29%20%E2%80%94%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%B0%D1%8F%20%D0%B0%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D1%8F%20%D0%BF%D0%BE%20Claude%20%2824%20%D0%BA%D1%83%D1%80%D1%81%D0%B0%20%D0%B8%20293%20%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B0%2C%20%D0%BD%D0%BE%20%D1%83%D1%80%D0%BE%D0%B2%D0%BD%D0%B5%D0%B9%20%D1%82%D1%80%D0%B8%2C%20%D0%B0%20%D0%BD%D0%B5%20%D1%88%D0%B5%D1%81%D1%82%D1%8C%3B%20%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D0%B2%20%D0%BF%D1%8F%D1%82%D1%8C%29.md)

#AI #Claude_Code #Агенты #Видео #Anthropic
