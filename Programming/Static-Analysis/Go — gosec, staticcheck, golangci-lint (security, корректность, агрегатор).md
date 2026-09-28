---
создал заметку: 2026-09-28T15:45:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Go
  - SAST
  - Linter
Источник:
  - https://github.com/securego/gosec
  - https://github.com/dominikh/go-tools
  - https://github.com/golangci/golangci-lint
---

# 🐹 Go — gosec, staticcheck, golangci-lint

Экосистема статического анализа Go делится на три роли: **security-скан**, **линтер корректности** и **агрегатор**, который гоняет всё разом. Плюс встроенный `go vet`.

| Инструмент | ★ | Лицензия | Роль |
| :--- | :---: | :--- | :--- |
| **[gosec](https://github.com/securego/gosec)** (securego) | ~9k | Apache-2.0 | **SAST-security**: инъекции, хардкод-креды, слабая крипта, права файлов, `math/rand` для секретов |
| **[staticcheck](https://github.com/dominikh/go-tools)** (dominikh) | ~6.9k | MIT | лучший **линтер корректности/упрощений**: баги, мёртвый код, неэффективности |
| **[golangci-lint](https://github.com/golangci/golangci-lint)** (~19.4k) | GPL-3.0 | **агрегатор**: запускает десятки линтеров (включая gosec, staticcheck, govet) параллельно и быстро |
| `go vet` | — | (в составе Go) | базовые проверки от команды Go |

---

## 🔎 Что чем

- **gosec** — то, что для Python делает Bandit: security-паттерны Go. Правила `Gxxx` (`G101` хардкод-креды, `G204` command injection, `G401/G501` слабая крипта…).
  ```bash
  go install github.com/securego/gosec/v2/cmd/gosec@latest
  gosec ./...                 # весь модуль
  gosec -fmt=sarif -out=out.sarif ./...
  ```
- **staticcheck** — про баги и качество (не security). Практически стандарт для Go.
  ```bash
  go install honnef.co/go/tools/cmd/staticcheck@latest
  staticcheck ./...
  ```
- **golangci-lint** — как это гоняют в реальных проектах: один конфиг `.golangci.yml`, включаешь нужные линтеры (в т.ч. `gosec`, `staticcheck`, `govet`, `errcheck`…), один быстрый прогон в CI.
  ```bash
  golangci-lint run
  ```

> [!tip] Практика
> В CI обычно достаточно **golangci-lint** с включёнными `staticcheck`+`gosec` — не нужно дёргать их порознь. Отдельно gosec берут, когда нужен именно security-отчёт (SARIF) без прочего шума.

---

## 🖥️ На системах владельца

Все три — **самодостаточные Go-бинарники** (`go install` или готовые релизы), кроссплатформенные:

| Система | Как |
| :--- | :--- |
| **Gentoo** (основная) | `go install …@latest` (нужен `dev-lang/go`); golangci-lint — из релизов/`emerge` |
| **Debian / Ubuntu** | `go install` или официальный установочный скрипт golangci-lint |
| **Arch** | `pacman -S golangci-lint go`; gosec/staticcheck — `go install` |
| **Entware / RT-AX56U** | ⚠️ теоретически: golangci-lint/gosec есть в релизах под `arm`, но собирать/гонять анализ Go на роутере смысла мало — на ПК/в CI |

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Аналог gosec для Python: [Bandit](Bandit%20%28PyCQA%29%20%E2%80%94%20security-%D0%BB%D0%B8%D0%BD%D1%82%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Python%20%D0%B1%D0%B5%D0%B7%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28%D0%BF%D0%B0%D1%80%D0%B0%20%D0%BA%20Semgrep%29.md)

## 🔗 Ссылки

- [securego/gosec](https://github.com/securego/gosec) · [dominikh/go-tools (staticcheck)](https://github.com/dominikh/go-tools) · [golangci/golangci-lint](https://github.com/golangci/golangci-lint)

#Programming #Static-Analysis #Go #SAST #Linter
