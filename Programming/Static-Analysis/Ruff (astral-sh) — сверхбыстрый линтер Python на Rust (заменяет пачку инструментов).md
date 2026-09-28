---
создал заметку: 2026-09-28T15:05:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Python
  - Linter
  - Ruff
  - Rust
Источник:
  - https://github.com/astral-sh/ruff
  - https://docs.astral.sh/ruff/
---

# ⚡ Ruff (astral-sh) — сверхбыстрый линтер Python на Rust

**Ruff** ([github.com/astral-sh/ruff](https://github.com/astral-sh/ruff), **MIT**, ~50k★, от Astral — авторов `uv`) — линтер и форматтер Python, написанный **на Rust**, отсюда главная фишка: он **в десятки-сотни раз быстрее** классических Python-инструментов. Заменяет собой сразу пачку: Flake8, isort, pyupgrade, pydocstyle, часть pylint, а также **flake8-bandit** — то есть частично **security-правила Bandit** (коды `S…`).

Для домена важно: Ruff — прежде всего **качество/стиль**, но с бонусом security-подмножества.

---

## 🔎 Что умеет и что с security

- 800+ правил из экосистемы flake8-плагинов под одним быстрым движком; выбор наборов по префиксам: `E/F` (pyflakes/pycodestyle), `I` (isort), `UP` (pyupgrade), `B` (bugbear), **`S` (flake8-bandit — security)** и др.
- Встроенный **форматтер** (замена Black), автофиксы (`--fix`).
- Конфиг в `pyproject.toml` (`[tool.ruff]`), интеграция pre-commit/CI/LSP.

```bash
pipx install ruff
ruff check .                 # линт
ruff check --select S .      # только security-правила (flake8-bandit)
ruff check --fix .           # автоисправления
ruff format .                # форматирование
```

> [!note] Ruff `S` ≠ полноценный Bandit
> Подмножество `S` покрывает **часть** проверок [Bandit](Bandit%20%28PyCQA%29%20%E2%80%94%20security-%D0%BB%D0%B8%D0%BD%D1%82%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Python%20%D0%B1%D0%B5%D0%B7%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28%D0%BF%D0%B0%D1%80%D0%B0%20%D0%BA%20Semgrep%29.md), но не весь набор и без его нюансов. Ruff отлично закрывает **скорость + качество + базовый security-линт** в одном проходе; для полноценного security-скана держать рядом Bandit/[Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md).

---

## 🖥️ На системах владельца

Ruff — **готовый бинарь на Rust** (ставится и через `pip`/`pipx` как wheel):

| Система | Как |
| :--- | :--- |
| **Gentoo** (основная) | `pipx install ruff` (wheel с бинарём) или `emerge dev-python/ruff`, если есть |
| **Debian / Ubuntu** | `pipx install ruff` (в репо бывает старый) |
| **Arch** | `pacman -S ruff` |
| **Entware / RT-AX56U** | ⚠️ зависит от готового колеса под `armv7`; если есть — `pip install ruff`, иначе собрать Rust на роутере нереально. Bandit тут надёжнее |

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Полноценный Python security-линтер: [Bandit](Bandit%20%28PyCQA%29%20%E2%80%94%20security-%D0%BB%D0%B8%D0%BD%D1%82%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Python%20%D0%B1%D0%B5%D0%B7%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28%D0%BF%D0%B0%D1%80%D0%B0%20%D0%BA%20Semgrep%29.md)

## 🔗 Ссылки

- [astral-sh/ruff](https://github.com/astral-sh/ruff) · [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)

#Programming #Static-Analysis #Python #Linter #Ruff #Rust
