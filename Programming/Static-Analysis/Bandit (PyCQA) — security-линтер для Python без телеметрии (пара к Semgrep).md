---
создал заметку: 2026-09-28T14:45:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - SAST
  - Python
  - Bandit
  - Security
Источник:
  - https://github.com/PyCQA/bandit
  - https://bandit.readthedocs.io/
---

# 🐍 Bandit (PyCQA) — security-линтер для Python

**Bandit** ([github.com/PyCQA/bandit](https://github.com/PyCQA/bandit), **Apache-2.0**, ~8.3k★) — специализированный SAST **только для Python**: строит AST файла и проверяет его набором детекторов небезопасных конструкций. В отличие от [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md) — **чистый OSS, без телеметрии и облака**, встроенный набор правил из коробки. Это естественная **пара к Semgrep** для Python: Bandit как быстрый базовый security-проход, Semgrep — для кастомных правил и не-Python кода.

---

## 🔎 Что ловит (те самые паттерны из поста про Semgrep — но из коробки)

- `eval`/`exec`, `pickle.loads`, небезопасный `yaml.load`;
- `subprocess(..., shell=True)`, вызовы через shell;
- хардкод паролей/секретов;
- слабая криптография (`md5`, `sha1`), `random` вместо `secrets`;
- `requests(..., verify=False)` (отключённая проверка TLS);
- небезопасные временные файлы, `assert` в проде, SQL из конкатенации строк.

Каждая проверка — ID `Bxxx` (напр. `B602` shell injection), с **severity** и **confidence**.

```bash
pip install bandit          # или pipx
bandit -r .                 # рекурсивно по проекту
bandit -r . -ll -ii         # только severity/confidence не ниже medium
bandit -r . -f sarif -o out.sarif   # для CI
bandit -r . -s B101,B601    # пропустить конкретные тесты
```
Конфиг — в `pyproject.toml` (`[tool.bandit]`) или `.bandit`; интеграция в `pre-commit` и CI из коробки.

> [!note] Не заменяет ревью и Semgrep
> Bandit — паттерны без глубокого dataflow: даёт ложные срабатывания (частый пример — `assert`/`B101` в тестах) и не проследит инъекцию через несколько функций. Триаж находок нужен. В связке с Semgrep покрытие шире.

---

## 🖥️ На системах владельца

**Чистый Python** — заводится где угодно, включая роутер:

| Система | Как |
| :--- | :--- |
| **Gentoo** (основная) | `emerge dev-python/bandit` или `pipx install bandit` |
| **Debian / Ubuntu** | `apt install bandit` или pipx |
| **Arch** | `pacman -S bandit` |
| **Entware / RT-AX56U** | ✅ реально: `pip install bandit` под `python3` из Entware (в отличие от JVM-инструментов). Полезно, если правишь Python прямо на роутере |

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Пара по кастомным правилам и мультиязык: [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md)

## 🔗 Ссылки

- [PyCQA/bandit](https://github.com/PyCQA/bandit) · [док](https://bandit.readthedocs.io/)

#Programming #Static-Analysis #SAST #Python #Bandit #Security
