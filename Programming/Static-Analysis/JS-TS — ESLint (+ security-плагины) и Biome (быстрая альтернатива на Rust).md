---
создал заметку: 2026-09-28T16:05:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - JavaScript
  - TypeScript
  - ESLint
  - Biome
Источник:
  - https://github.com/eslint/eslint
  - https://github.com/biomejs/biome
---

# 🟨 JS/TS — ESLint (+ security-плагины) и Biome

Для JavaScript/TypeScript статический анализ строится вокруг двух подходов: **ESLint** с богатой экосистемой плагинов и **Biome** — быстрая всё-в-одном альтернатива на Rust.

| | [ESLint](https://github.com/eslint/eslint) | [Biome](https://github.com/biomejs/biome) |
| :--- | :--- | :--- |
| ★ / лицензия | ~27.5k · MIT | ~25.9k · Apache-2.0 |
| Реализация | Node.js | **Rust (быстрый)** |
| Роль | линтер с плагинами | линтер + форматтер в одном |
| Экосистема | огромная (тысячи правил/плагинов) | своя, компактнее; плагинов почти нет |
| Security | через плагины (см. ниже) | базово, security-правил мало |

---

## 🔒 Security в ESLint — через плагины

Сам ESLint — про качество/стиль; security добавляют плагины:
- **eslint-plugin-security** — небезопасные паттерны Node (детект `child_process`, `eval`, небезопасные regex/ReDoS, `Buffer`…);
- **eslint-plugin-no-unsanitized** — XSS-опасные присваивания в DOM (`innerHTML` и т.п.);
- **@typescript-eslint** — типо-осведомлённые правила для TS.

```bash
npm i -D eslint eslint-plugin-security
# eslint.config.js (flat config) — подключить plugin:security/recommended
npx eslint .
```

> [!note] Для серьёзного security JS честнее Semgrep
> ESLint-плагины ловят частые паттерны, но для dataflow/инъекций по JS сильнее [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md) (у него сильные JS/TS-правила) или CodeQL для OSS.

## ⚡ Biome — когда важна скорость

Biome (наследник Rome) — **линтер + форматтер** на Rust, в разы быстрее ESLint+Prettier, один инструмент и конфиг:
```bash
npm i -D @biomejs/biome
npx biome check --write .     # линт + формат + автофикс
```
Минус: **набор правил и плагинов меньше**, чем у ESLint; security-правил почти нет. Berёт скоростью и «всё в одном» для форматирования/базового линта, а глубокий security оставляют Semgrep/ESLint-плагинам.

---

## 🖥️ На системах владельца

Обоим нужен **Node.js** (`nodejs`/`npm` в Portage/apt/pacman); Biome ставится как npm-пакет с Rust-бинарём под платформу.

| Система | Как |
| :--- | :--- |
| **Gentoo / Debian-Ubuntu / Arch** | Node из репозитория, дальше `npm i -D eslint`/`@biomejs/biome` |
| **Entware / RT-AX56U** | ➖ Node-тулчейн на роутере обычно не держат; анализ JS — на ПК/в CI |

## 🔗 Связанные заметки

- Терминология домена: [SAST vs DAST vs SCA](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md)
- Сильные JS/TS-правила для security: [Semgrep](Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md)

## 🔗 Ссылки

- [eslint/eslint](https://github.com/eslint/eslint) · [biomejs/biome](https://github.com/biomejs/biome)

#Programming #Static-Analysis #JavaScript #TypeScript #ESLint #Biome
