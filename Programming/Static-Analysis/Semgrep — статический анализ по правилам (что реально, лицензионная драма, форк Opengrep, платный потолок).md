---
создал заметку: 2026-09-28T11:40:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - SAST
  - Security
  - Python
  - Semgrep
Источник:
  - https://t.me/c/2675453029/1500
  - https://semgrep.dev/docs/
  - https://github.com/semgrep/semgrep
---

# 🔎 Semgrep — статический анализ по правилам

**Semgrep** ([github.com/semgrep/semgrep](https://github.com/semgrep/semgrep), Semgrep Inc. / бывш. r2c, **LGPL-2.1**, ~16.8k★, CLI) — быстрый статический анализатор (SAST) для 30+ языков. Главная фишка — **синтаксис правил, похожий на сам код**: паттерн `eval(...)` матчит вызовы `eval` по структуре AST, а не регэкспом. За минуты пишется правило под свой проект. Пост про Python верен по сути, но продаёт инструмент глаже, чем он есть.

> [!tip] Вердикт (кратко)
> **Брать стоит** — для локального аудита и особенно **CI** это одна из лучших бесплатных SAST-опций. Но с поправкой на 4 вещи, которых нет в посте: облачная телеметрия `--config=auto`, платный потолок (межфайловый анализ — Pro), запутанная лицензионная история и наличие полностью открытого форка **Opengrep**. Для Python разумно в связке с **Bandit**.

---

## ✅ Что реально хорошо

- **Паттерн-матчинг по AST, а не текст.** Ловит `eval`, `exec`, `pickle.loads`, `subprocess(..., shell=True)`, хардкод секретов, небезопасные вызовы — устойчиво к форматированию/переносам.
- **Свои правила на простом YAML.** `pattern:`, `pattern-not:`, `metavariable`, `pattern-either` — порог входа низкий, кастомизация под кодовую базу быстрая.
- **Мультиязычность:** Python, JS/TS, Go, Java, Ruby, C/C++, PHP и др. — один инструмент на монорепо.
- **Интеграции:** CI (GitHub Actions/GitLab), `pre-commit`, VS Code, вывод в **SARIF/JSON** для дашбордов.
- **Готовые наборы правил:** OWASP Top 10, CWE, поиск секретов — через реестр (`p/python`, `p/owasp-top-ten`, `p/secrets`).

## ⚠️ Что пост умалчивает (4 подводных камня)

### 1. Лицензионная драма → форк Opengrep
В декабре 2024 Semgrep ужесточил условия реестра community-правил, и индустрия форкнула проект — **[Opengrep](https://github.com/opengrep/opengrep)** (LGPL-2.1, ~3.1k★, создан 14.12.2024 консорциумом Aikido, Endor Labs и др.). Сам движок Semgrep OSS остаётся открытым, но если важна «чистая» открытость правил без вендор-замка — смотреть в сторону Opengrep. Пост подаёт «открытый и бесплатный» без этого контекста.

### 2. Бесплатная версия ≠ полная мощь
Semgrep **OSS анализирует в пределах одного файла** (intraprocedural). Глубокий **межфайловый/межпроцедурный taint-анализ** (как грязные данные текут от входа к SQL-стоку через несколько функций/файлов) — это **Semgrep Pro Engine, закрытый и платный**. «Ловит SQL-инъекции» — да, простые; сложные цепочки бесплатная версия часто пропускает.

### 3. `--config=auto` ходит в сеть и шлёт телеметрию
`auto` тянет правила из облачного реестра и отправляет метрики о проекте. Для приватного/чувствительного кода так не стоит. Локально и без утечек:
```bash
semgrep scan --config p/python --config ./rules/ --metrics=off
```
(пиновать конкретные наборы/локальные правила + `--metrics=off`).

### 4. Это помощник, а не замена ревью
Паттерн-матчинг даёт ложные срабатывания — находки надо триажить. «Не нужно быть безопасником, чтобы начать» — наполовину правда: запустить легко, отсеять шум и писать хорошие правила — уже навык.

---

## 🐍 Для Python: Semgrep + Bandit

| | Semgrep | [Bandit](https://github.com/PyCQA/bandit) (PyCQA) |
| :--- | :--- | :--- |
| Лицензия | LGPL-2.1 (но реестр правил — см. выше) | **Apache-2.0, чистый OSS** |
| Языки | 30+ | только Python |
| Телеметрия | есть (`--config=auto`) | **нет** |
| Правила | свой YAML, реестр | встроенный набор + плагины |
| Сила | кастомные правила, мультиязык | быстрый базовый security-скан AST Python |

**Практика:** Bandit — как быстрый базовый проход (`bandit -r .`), Semgrep — для кастомных правил и не-Python кода. Дополняют друг друга. Рядом стоит держать в уме **Ruff** (astral-sh) — он умеет часть bandit-правил (`S`-коды flake8-bandit) на огромной скорости, и **CodeQL** (мощнее по dataflow, но бесплатен только для OSS, лицензия ограничивает приватное коммерческое использование).

---

## ⚙️ Установка/запуск по системам владельца

```bash
pipx install semgrep      # рекомендуемо (изолировано); либо pip install semgrep
semgrep scan --config p/python .     # скан по готовому набору
semgrep scan --config ./my-rules.yml --metrics=off .   # свои правила, без телеметрии
semgrep --sarif -o out.sarif --config auto .           # для дашбордов
```

| Система | Установка | Нюанс |
| :--- | :--- | :--- |
| **Gentoo** (основная) | `pipx install semgrep` (в venv); Bandit — `emerge dev-python/bandit` или pipx | Semgrep тащит платформенный OCaml-бинарь ядра; в pipx-окружении чисто |
| **Debian / Ubuntu** | `pipx install semgrep`; на новых системах системный pip заблокирован (PEP 668) → pipx/venv | Bandit — `apt install bandit` |
| **Arch** | AUR: `semgrep`/`semgrep-bin`; либо pipx. Bandit — `pacman -S bandit` | AUR-версия может отставать |
| **Entware / RT-AX56U** (armv7) | ➖ Semgrep — вряд ли: ядро на OCaml, готового бинаря под armv7 обычно нет. **Bandit** (чистый Python) — заведётся под `python3` из Entware | анализ кода логичнее гонять на ПК/в CI, а не на роутере |

> [!note] CI и pre-commit
> Наибольшая польза — в конвейере: `pre-commit` хук блокирует небезопасные паттерны до коммита, а в CI Semgrep гоняется на PR. Именно там окупается скорость и SARIF-вывод.

---

## 🔗 Связанные заметки

*(домен `Programming/Static-Analysis/` только заведён — сюда лягут Bandit, Ruff, mypy, CodeQL и др.)*

## 🔗 Ссылки

- Документация: [semgrep.dev/docs](https://semgrep.dev/docs/) · репозиторий: [semgrep/semgrep](https://github.com/semgrep/semgrep)
- Открытый форк: [opengrep/opengrep](https://github.com/opengrep/opengrep)
- Python-альтернатива без телеметрии: [PyCQA/bandit](https://github.com/PyCQA/bandit)
- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Programming #Static-Analysis #SAST #Security #Python #Semgrep
