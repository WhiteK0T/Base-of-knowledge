---
создал заметку: 2026-06-19T15:20:00
author: WhiteK0T
tags:
  - AI
  - Claude_Code
  - Workflow
  - Loops
  - OpenAPI
  - API
Источник:
  - https://loops.elorm.xyz/loops/openapi-sync-until-valid
---

# 🧩🔁 OpenAPI Sync Until Valid — петля синхронизации OpenAPI-спеки

Петля из каталога [Loops!](Loops%20%E2%80%94%20обзор%20сайта%20и%20каталог%20петель.md): держит **`openapi.yaml`** валидным и **в соответствии с реальными роут-хендлерами** — линтит спеку и чинит расхождения (drift) на каждой итерации, пока линтер не вернёт 0 ошибок.

## ⚙️ Параметры

| Параметр | Значение |
| :--- | :--- |
| Триггер | ручной (только промпт) |
| Check-команда (между итерациями) | `npx @redocly/cli lint openapi.yaml` |
| Макс. итераций | **8** |
| Условие выхода | линт OpenAPI завершается с кодом **0** (нет ошибок) |
| Читает / пишет | читает `openapi.yaml`; правит `openapi.yaml` (и неявно — файлы хендлеров) |
| Совместимость | Claude Code, Cursor (`/loop`), Codex, любой кодинг-агент |

## 📋 Kickoff-промпт (вставить агенту как есть)

```text
Start the "OpenAPI Sync Until Valid" loop. Goal: openapi.yaml lints clean and
matches implemented routes. Max iterations: 8. Between iterations run:
npx @redocly/cli lint openapi.yaml. Exit when: OpenAPI lint exits 0.
Step 1: Lint openapi.yaml. Fix spec errors and handler drift until lint passes.
```

**По-русски, что он делает:** (1) прогнать линт спеки ([Redocly CLI](https://redocly.com/docs/cli)); (2) чинить ошибки спеки **и** расхождения с хендлерами (пути, схемы, статус-коды), пока линт не станет чистым. Выход — когда `lint` возвращает код 0 (макс. 8 кругов).

## 🚀 Как запустить

- **Claude Code:** вставь промпт; дай агенту право запускать `npx @redocly/cli lint`. Самоуправляемая `/loop`-задача (см. [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20гайд.md)).
- Нужны: файл спеки `openapi.yaml` и доступный `npx` (Node). Альтернатива линтеру — **Swagger CLI** (`swagger-cli validate`), тогда замени check-команду в промпте.

> [!tip] Подгони путь и линтер
> Если спека лежит иначе (`api/openapi.yaml`, `*.json`) — поправь путь в обеих строках промпта. Линтер можно сменить на `spectral lint openapi.yaml` (Stoplight Spectral) — главное, чтобы команда возвращала ненулевой код при ошибках.

## 🛡️ Anti-gaming (встроенные предохранители)

Петля запрещает менять check-команду или обходить критерий валидности ради «зелёного» линта. Цель — **реальная** валидная спека, синхронная с кодом, а не отключённые правила линтера.

## 💡 Когда использовать и ограничения

- Для проектов с **API-first / OpenAPI-контрактом**: после изменения роутов держать спеку валидной и актуальной.
- Хорошо рядом с петлёй **API Contract Until Match** (приводит реализацию к контракту) — см. [каталог](Loops%20%E2%80%94%20обзор%20сайта%20и%20каталог%20петель.md).
- **Неприменима к этому Obsidian-репозиторию** (нет API) — заметка как готовый рецепт под backend-проекты с OpenAPI.
- Линт ловит **формальную** валидность и часть drift'а; смысловую корректность контракта (правильные ли схемы по сути) всё равно проверяй сам.

## 🔗 Ссылки

- Страница петли: [loops.elorm.xyz/loops/openapi-sync-until-valid](https://loops.elorm.xyz/loops/openapi-sync-until-valid)
- Линтеры: [Redocly CLI](https://redocly.com/docs/cli) · [Spectral](https://stoplight.io/open-source/spectral)
- Связанные: [Каталог петель Loops!](Loops%20%E2%80%94%20обзор%20сайта%20и%20каталог%20петель.md) · [Claude Code — гайд](../Claude%20Code%20%E2%80%94%20гайд.md)

#AI #Claude_Code #Workflow #Loops #OpenAPI #API
