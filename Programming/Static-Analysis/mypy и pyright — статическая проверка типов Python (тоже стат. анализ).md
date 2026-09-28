---
создал заметку: 2026-09-28T15:25:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Python
  - TypeChecking
  - mypy
  - pyright
Источник:
  - https://github.com/python/mypy
  - https://github.com/microsoft/pyright
---

# 🔤 mypy и pyright — статическая проверка типов Python

Раз домен `Static-Analysis/` общий, сюда входят и **type-checkers** — они статически анализируют код по аннотациям типов, не запуская его. Это не security-инструменты, но ловят целый класс багов до рантайма (передал не тот тип, `None` там, где ожидался объект, опечатка в атрибуте).

- **[mypy](https://github.com/python/mypy)** (~20.6k★, MIT) — эталонный проверщик типов Python от команды языка. Медленнее, но «референсное» поведение.
- **[pyright](https://github.com/microsoft/pyright)** (Microsoft, ~15.7k★, MIT) — на TypeScript/Node, **быстрый**, движок за **Pylance** в VS Code. Сильный вывод типов, режим `strict`.

---

## 🔎 Зачем это в ИБ-контексте

Прямой security-пользы нет, но типобезопасность **убирает почву** под частью багов, которые перерастают в уязвимости: перепутанные `bytes`/`str`, `None`-разыменования, неверные сигнатуры в обработке ввода. Плюс аннотации типов делают код читаемее для последующего security-ревью и точнее для [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md).

```bash
pipx install mypy && mypy .            # проверка по аннотациям
mypy --strict src/                     # строгий режим (требует полной типизации)
pipx install pyright && pyright        # быстрый, strict через pyrightconfig.json
```

## 🆚 mypy vs pyright

| | mypy | pyright |
| :--- | :--- | :--- |
| Реализация | Python | TypeScript/Node (быстрее) |
| Роль | эталон поведения типов | движок Pylance (VS Code), сильный inference |
| Когда | CI, «как задумано в языке» | IDE-фидбэк на лету, строгие проекты |

На практике часто: **pyright в редакторе** (мгновенно) + **mypy в CI** (эталонная проверка). Есть и быстрый Rust-проверщик от Astral (**ty**, ранняя стадия) — стоит следить, но пока не замена.

---

## 🖥️ На системах владельца

| Система | Как |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | mypy: `pipx install mypy` / `dev-python/mypy` / `pacman -S mypy`; pyright: `pipx install pyright` (тянет Node) или npm |
| **Entware / RT-AX56U** | mypy (чистый Python) заведётся под `python3`; pyright требует Node — на роутере вряд ли оправдан |

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Скорость + линт + базовый security: [Ruff](Ruff%20%28astral-sh%29%20%E2%80%94%20%D1%81%D0%B2%D0%B5%D1%80%D1%85%D0%B1%D1%8B%D1%81%D1%82%D1%80%D1%8B%D0%B9%20%D0%BB%D0%B8%D0%BD%D1%82%D0%B5%D1%80%20Python%20%D0%BD%D0%B0%20Rust%20%28%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D1%8F%D0%B5%D1%82%20%D0%BF%D0%B0%D1%87%D0%BA%D1%83%20%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%29.md)

## 🔗 Ссылки

- [python/mypy](https://github.com/python/mypy) · [microsoft/pyright](https://github.com/microsoft/pyright)

#Programming #Static-Analysis #Python #TypeChecking #mypy #pyright
