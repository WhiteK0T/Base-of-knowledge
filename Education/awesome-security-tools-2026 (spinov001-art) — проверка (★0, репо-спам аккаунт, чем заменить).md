---
создал заметку: 2026-10-02T11:00:00
author: WhiteK0T
tags:
  - Education
  - Security
  - Подборка
  - Проверка
Источник:
  - https://t.me/c/2675453029/1535
---

# 📦 awesome-security-tools-2026 (spinov001-art) — проверка

Пост рекламирует репозиторий **[spinov001-art/awesome-security-tools-2026](https://github.com/spinov001-art/awesome-security-tools-2026)** как «150+ инструментов в 15 категориях». Проверил по GitHub на 02.10.2026 — **не стоит сохранять**: это пустой по авторитету репозиторий от аккаунта-репоспамера, и мы его **уже видели**.

> [!danger] Короткий вердикт
> **★0**, создан 03.2026, последний коммит **04.2026** (заброшен), **без лицензии**. Аккаунт `spinov001-art` — **297 репозиториев при 13 подписчиках**, штампует однотипные «awesome-*-2026». Это **тот же репозиторий**, который уже разбирался в [проверке подборки #1493](5%20GitHub-%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B5%D0%B2%20%D0%BF%D0%BE%20%D0%98%D0%91%20%D0%B8%D0%B7%20%D0%BF%D0%BE%D1%81%D1%82%D0%B0%20%E2%80%94%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%28%D0%BC%D1%83%D1%81%D0%BE%D1%80%D0%BD%D1%8B%D0%B9%20%231%2C%20%D0%B4%D1%83%D0%B1%D0%BB%D0%B8%2C%20%D0%B1%D0%B8%D1%82%D1%8B%D0%B5%20%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B8%2C%20%D1%87%D0%B5%D0%BC%20%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C%29.md) (там он всплывал как мислинк «security-tools» → `awesome-ai-tools-2026`).

---

## 🎭 Приём поста: чужими звёздами

Пост впечатляет числами — **Metasploit 34K★, sqlmap 32K★, Nuclei 21K★, Trivy 24K★…** Но это **звёзды самих инструментов**, а не репозитория-списка. У списка-обёртки — **0 звёзд**. Классическая подмена: авторитет известных тулзов приписывается пустому каталогу, который их просто перечисляет.

Сами инструменты из поста — реальные и хорошие (Metasploit, sqlmap, Nmap, Nuclei, Burp, ffuf, Hydra, Amass, Subfinder, httpx, Trivy, Grype, Semgrep, Bandit). Но чтобы их найти, **этот репозиторий не нужен** — половина уже с разборами в хранилище (ниже).

---

## ✅ Чем заменить (проверенные крупные списки)

| | Список |
| :--- | :--- |
| Гигантский каталог по темам | [Hack-with-Github/Awesome-Hacking](https://github.com/Hack-with-Github/Awesome-Hacking) (★121k) |
| Security-инструменты | [sbilly/awesome-security](https://github.com/sbilly/awesome-security) (★15k) |
| «Книга тайных знаний» (инструменты + команды) | [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) (★246k) |

А конкретные инструменты из поста уже разобраны в хранилище:
- [Metasploit](../Pentest/Frameworks/Metasploit%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%28msfconsole%2C%20%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D0%B8%2C%20msfvenom%2C%20meterpreter%2C%20%D0%BF%D0%B8%D0%B2%D0%BE%D1%82%D0%B8%D0%BD%D0%B3%29.md) · [sqlmap](../Pentest/Web/sqlmap%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BF%D0%BE%D0%B8%D1%81%D0%BA%D0%B0%20%D0%B8%20%D1%8D%D0%BA%D1%81%D0%BF%D0%BB%D1%83%D0%B0%D1%82%D0%B0%D1%86%D0%B8%D0%B8%20SQL-%D0%B8%D0%BD%D1%8A%D0%B5%D0%BA%D1%86%D0%B8%D0%B9%20%28%D1%87%D1%82%D0%BE%20%D1%83%D0%BC%D0%B5%D0%B5%D1%82%2C%20%D1%87%D0%B5%D0%B3%D0%BE%20%D0%9D%D0%95%20%D1%83%D0%BC%D0%B5%D0%B5%D1%82%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%20%D0%B8%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%29.md) · [Burp Suite](../Pentest/Web/Burp%20Suite%20%E2%80%94%20%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0%20%D0%BF%D0%B5%D1%80%D0%B5%D1%85%D0%B2%D0%B0%D1%82%D0%B0%20HTTPS%20%28%D1%81%20%D0%BF%D0%BE%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0%D0%BC%D0%B8%3A%20%D0%B2%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%2C%20%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%20%D0%B2%20Chrome%20%D0%BD%D0%B0%20Linux%2C%20%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C%29.md) · [Semgrep](../Programming/Static-Analysis/Semgrep%20%E2%80%94%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%D0%BC%20%28%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%2C%20%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%2C%20%D1%84%D0%BE%D1%80%D0%BA%20Opengrep%2C%20%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%BE%D1%82%D0%BE%D0%BB%D0%BE%D0%BA%29.md) · [Bandit](../Programming/Static-Analysis/Bandit%20%28PyCQA%29%20%E2%80%94%20security-%D0%BB%D0%B8%D0%BD%D1%82%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20Python%20%D0%B1%D0%B5%D0%B7%20%D1%82%D0%B5%D0%BB%D0%B5%D0%BC%D0%B5%D1%82%D1%80%D0%B8%D0%B8%20%28%D0%BF%D0%B0%D1%80%D0%B0%20%D0%BA%20Semgrep%29.md)

---

## 🧭 Паттерн для памяти

Это уже **вторая** заметка про аккаунт `spinov001-art` — устойчивый источник мусорных «awesome-*-2026». Признаки такого репоспама:
- **★0–единицы** при громком названии и «2026» в имени (SEO под свежесть);
- аккаунт с **сотнями** одинаковых awesome-репозиториев и горсткой подписчиков;
- в описании — **звёзды перечисляемых инструментов**, а не самого списка;
- нет лицензии, заброшен через пару недель после создания.

Правило прежнее: открыть ссылку, глянуть звёзды/дату/автора — и не сохранять.

## 🔗 Связанные заметки

- Первая встреча с этим аккаунтом: [проверка подборки #1493](5%20GitHub-%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B5%D0%B2%20%D0%BF%D0%BE%20%D0%98%D0%91%20%D0%B8%D0%B7%20%D0%BF%D0%BE%D1%81%D1%82%D0%B0%20%E2%80%94%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%28%D0%BC%D1%83%D1%81%D0%BE%D1%80%D0%BD%D1%8B%D0%B9%20%231%2C%20%D0%B4%D1%83%D0%B1%D0%BB%D0%B8%2C%20%D0%B1%D0%B8%D1%82%D1%8B%D0%B5%20%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B8%2C%20%D1%87%D0%B5%D0%BC%20%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C%29.md)

## 🔗 Ссылки

- Разбираемый репозиторий (не рекомендуется): [spinov001-art/awesome-security-tools-2026](https://github.com/spinov001-art/awesome-security-tools-2026)
- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Education #Security #Подборка #Проверка
