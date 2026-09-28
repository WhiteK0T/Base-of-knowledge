---
создал заметку: 2026-09-28T20:10:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - SAST
  - SCA
  - Secrets
  - Python
Источник:
  - https://t.me/c/2675453029/1524
  - https://github.com/PramanKasliwal/maunprekshak
  - https://pypi.org/project/maunprekshak/
---

# 🔍 MaunPrekshak — всё-в-одном security-сканер Python (концепт против зрелости)

**MaunPrekshak** ([github.com/PramanKasliwal/maunprekshak](https://github.com/PramanKasliwal/maunprekshak), Apache-2.0, Python ≥3.11) — новый инструмент, объединяющий в одной команде три класса проверок для Python: **SCA** (уязвимые зависимости), **secret-scanning** и **SAST**. Название с санскрита — «тихий наблюдатель». Идея хорошая: [SAST vs DAST vs SCA vs secrets](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md) — все четыре класса обычно гоняют разными тулзами, а тут один прогон.

> [!danger] Трезвый статус: инструменту 2 недели, ★0, версия pre-1.0
> Пост читается как **промо**. Факты на 28.09.2026: репозиторий **создан 12.09.2026** (≈2 недели), **★0**, форков 0, версия **v0.10.2** (быстрые релизы одного автора, всё ещё **до 1.0**). Это **не** проверенный временем инструмент — ни аудита, ни сообщества, ни репутации. Заявление поста **«ноль ложных срабатываний»** — типичный маркетинг: у SAST/secret-сканеров FP есть всегда, «ноль» не бывает.

---

## 📋 Что заявлено (по посту и репозиторию)

| Модуль | Заявка |
| :--- | :--- |
| **SCA** | зависимости через **[OSV.dev](https://osv.dev/)**, транзитивно; Python (`requirements.txt`, `poetry.lock`, `uv.lock`, `Pipfile`), а также JS/Node, Go, Rust |
| **Secrets** | 40+ regex-детекторов (ключи OpenAI `sk-proj-`, Anthropic `sk-ant-`, HF `hf_`, GitHub PAT, AWS, Stripe…) + Shannon-энтропия для беспрефиксных |
| **SAST** | 30 AST-правил (MP001–MP030): `eval`/`exec`, SQLi, отключённый TLS, `0.0.0.0`, небезопасная десериализация, `shell=True`, SSTI (Jinja2/Mako), ECB, Zip Slip |
| **Режимы** | `--staged` (pre-commit), `--diff` (против git-рефа), `--baseline` (подавить старое), `--ci --fail-on high` |
| **Экспорт** | SARIF 2.1.0, CycloneDX SBOM, SPDX, JSON, Markdown |
| **--fix** | автопатч безопасных анти-паттернов: `yaml.load→safe_load`, `tar.extractall(filter='data')`, `mktemp→NamedTemporaryFile` |
| **AI (опц.)** | с ключом Gemini/OpenAI/Anthropic или локальной Ollama — executive summary + план remediation; без ключа офлайн |

```bash
pip install maunprekshak
mp scan .
```

---

## ⚖️ Оценка: стоит ли брать

**Плюсы концепта:** один прогон вместо четырёх инструментов; privacy-first (локально, без ключей для базового скана); современный экспорт (SARIF/SBOM); разумные автофиксы. Для соло-разработчика «поставил и глянул риск-скор» — удобно.

**Против (существенно):**
- **Незрелость.** 2 недели, ★0, pre-1.0 — ставить его **гейткипером в CI** (`--fail-on high`) рано: неизвестны надёжность и полнота.
- **Каждый модуль по отдельности уже закрыт зрелыми тулзами**, и лучше:
  - SCA → **osv-scanner** (тот же OSV.dev, от Google) или **pip-audit**, **Trivy**;
  - secrets → [gitleaks / trufflehog](gitleaks%20%D0%B8%20trufflehog%20%E2%80%94%20%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%20%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D0%BE%D0%B2%20%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B5%20%D0%B8%20%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8%20git%20%28%D0%BF%D0%B0%D1%82%D1%82%D0%B5%D1%80%D0%BD%D1%8B%20vs%20%D0%B2%D0%B5%D1%80%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%29.md) (trufflehog ещё и **верифицирует** ключи вживую);
  - SAST → [Bandit](Bandit%20%28PyCQA%29%20%E2%80%94%20security-%D0%BB%D0%B8%D0%BD%D1%82%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Python%20%D0%B1%D0%B5%D0%B7%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28%D0%BF%D0%B0%D1%80%D0%B0%20%D0%BA%20Semgrep%29.md) / [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md).
- **Доверие к коду.** Это пакет, который читает **весь твой код** (и опц. шлёт в AI). Ставить свежий пакет от неизвестного автора без аудита — сам по себе supply-chain-риск: как минимум глянуть исходники перед прогоном на чувствительном проекте.
- Пост пинит GitHub Action `@v0.8.0`, тогда как актуальна уже v0.10.2 — темп изменений высокий, API нестабилен.

**Вердикт:** любопытный проект «на посмотреть» и последить за развитием. Для реальной работы сейчас — проверенная связка **osv-scanner/pip-audit + gitleaks + Bandit/Semgrep**. Пересмотреть, если MaunPrekshak наберёт аудиторию, дойдёт до 1.0 и покажет качество на практике.

---

## 🖥️ На системах владельца

Чистый Python (нужен **Python ≥3.11**):

| Система | Как |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | `pipx install maunprekshak` (изолировать!); проверить, что Python ≥3.11 |
| **Entware / RT-AX56U** | ⚠️ теоретически (чистый Python), но версия/зависимости и незрелость — гонять на ПК |

## 🔗 Связанные заметки

- Что за классы он объединяет: [SAST vs DAST vs SCA vs secrets](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Зрелые аналоги по модулям: [Bandit](Bandit%20%28PyCQA%29%20%E2%80%94%20security-%D0%BB%D0%B8%D0%BD%D1%82%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Python%20%D0%B1%D0%B5%D0%B7%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28%D0%BF%D0%B0%D1%80%D0%B0%20%D0%BA%20Semgrep%29.md) · [gitleaks / trufflehog](gitleaks%20%D0%B8%20trufflehog%20%E2%80%94%20%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%20%D1%81%D0%B5%D0%BA%D1%80%D0%B5%D1%82%D0%BE%D0%B2%20%D0%B2%20%D0%BA%D0%BE%D0%B4%D0%B5%20%D0%B8%20%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8%20git%20%28%D0%BF%D0%B0%D1%82%D1%82%D0%B5%D1%80%D0%BD%D1%8B%20vs%20%D0%B2%D0%B5%D1%80%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%29.md)

## 🔗 Ссылки

- [PramanKasliwal/maunprekshak](https://github.com/PramanKasliwal/maunprekshak) · [PyPI](https://pypi.org/project/maunprekshak/) · [OSV.dev](https://osv.dev/)
- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Programming #Static-Analysis #SAST #SCA #Secrets #Python
