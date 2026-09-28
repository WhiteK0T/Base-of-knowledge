---
создал заметку: 2026-09-28T19:10:00
author: WhiteK0T
tags:
  - Education
  - Security
  - Обучение
  - Подборка
  - Проверка
Источник:
  - https://t.me/c/2675453029/1515
---

# 📚 «5 GitHub-репозиториев для прокачки в ИБ» (подборка №2) — проверка

Второй по счёту пост из CodeGuard с обещанием «5 репозиториев заменят десяток платных курсов». Проверил все ссылки по GitHub на 28.09.2026 — и на этот раз подборка **ещё слабее** [первой](5%20GitHub-%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B5%D0%B2%20%D0%BF%D0%BE%20%D0%98%D0%91%20%D0%B8%D0%B7%20%D0%BF%D0%BE%D1%81%D1%82%D0%B0%20%E2%80%94%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%28%D0%BC%D1%83%D1%81%D0%BE%D1%80%D0%BD%D1%8B%D0%B9%20%231%2C%20%D0%B4%D1%83%D0%B1%D0%BB%D0%B8%2C%20%D0%B1%D0%B8%D1%82%D1%8B%D0%B5%20%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B8%2C%20%D1%87%D0%B5%D0%BC%20%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C%29.md): **ни одного авторитетного репозитория, все — крошечные личные списки**, несколько созданы «за один день» и больше не трогались. Плюс те же болезни: пропущенная ссылка и несовпадение названия с URL.

> [!danger] Короткий вердикт
> Из 5 пунктов **брать всерьёз нечего**: максимум 30★, часть — репозитории одного дня. Реальная польза, на которую они лишь ссылаются (TryHackMe, HackTheBox, Cybrary), — это **сами платформы**, куда надо идти напрямую. Ниже — что не так и чем заменить.

---

## 🔎 Разбор по пунктам

| В посте | Реальный репозиторий | Статус | Вердикт |
| :--- | :--- | :--- | :--- |
| 1. awesome-cybersecurity-tools | [`eudk/awesome-cybersecurity-tools`](https://github.com/eudk/awesome-cybersecurity-tools) | ★30, создан 09.2025 | ⚠️ маленький личный список |
| 2. ctf-free-rooms | [`blacks1ph0n/ctf-free-rooms`](https://github.com/blacks1ph0n/ctf-free-rooms) | ★18, застыл 09.2025 | ⚠️ мелкий, «обновляемость» под вопросом |
| 3. Awesome-Underrated-Cybersecurity-Resources | **ссылки в посте нет** (только название) | — | 🚩 без ссылки; совпадает с п.4 |
| 4. «Ultimate Cybersecurity Roadmap 2025» | ссылка ведёт на [`rahulsz/Awesome-Underrated-Cybersecurity-Resources`](https://github.com/rahulsz/Awesome-Underrated-Cybersecurity-Resources) | ★2, репо одного дня (06.2025) | 🚩 **название ≠ URL**: это не роадмап, а тот самый репо из п.3 |
| 5. Cyber-Security-Tools | [`DafniB/Cyber-Security-Tools`](https://github.com/DafniB/Cyber-Security-Tools) | ★6, репо одного дня (05.2025) | ⚠️ мельчайший |

**Итого:** уникальных ссылок 4 (п.3 и п.4 — один репозиторий), и все — второсортные. «Роадмап от новичка до мидла» по факту ведёт на список недооценённых ресурсов на 2 звезды.

---

## ✅ Чем заменить (проверенные, крупные)

| Задача | Достойная замена |
| :--- | :--- |
| Гигантский каталог инструментов/тем | [Hack-with-Github/Awesome-Hacking](https://github.com/Hack-with-Github/Awesome-Hacking) (★121k) · [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) (★246k) |
| CTF-практика | напрямую **[TryHackMe](https://tryhackme.com)**, **[HackTheBox](https://hackthebox.com)**, **[picoCTF](https://picoctf.org)**, **[OverTheWire](https://overthewire.org)**; список — [apsdehal/awesome-ctf](https://github.com/apsdehal/awesome-ctf) (★12k) |
| Роадмап входа в ИБ | [roadmap.sh/cyber-security](https://roadmap.sh/cyber-security) · [sundowndev/hacker-roadmap](https://github.com/sundowndev/hacker-roadmap) (★15k) |
| Практические стенды локально | [7 репозиториев для практики в ИБ](../Pentest/Web/7%20%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B5%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B8%20%D0%B2%20%D0%98%D0%91%20%28WebGoat%2C%20Juice%20Shop%2C%20DVWA%2C%20HackTricks%2C%20PayloadsAllTheThings%2C%20h4cker%2C%20bug%20bounty%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md) |

---

## 🧭 Урок (повтор из первой проверки — паттерн устойчивый)

Такие посты собираются наспех/генератором: **название пункта не совпадает с URL**, ссылки пропущены или дублируются, а «звёздность» не проверяется. Признаки мусорной подборки:
- звёзд **единицы-десятки** и репозиторий создан пару месяцев назад → не «проверено временем»;
- «список ресурсов», который сам лишь ссылается на **известные платформы** — проще идти на платформу напрямую;
- совпадающие/битые ссылки, трекеры в URL.

Быстрая проверка перед сохранением: открыть ссылку (а не верить подписи), глянуть звёзды и дату последнего коммита.

## 🔗 Связанные заметки

- Первая такая же проверка (там был хотя бы один годный — okhosting): [5 GitHub-репозиториев по ИБ — проверка](5%20GitHub-%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B5%D0%B2%20%D0%BF%D0%BE%20%D0%98%D0%91%20%D0%B8%D0%B7%20%D0%BF%D0%BE%D1%81%D1%82%D0%B0%20%E2%80%94%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%28%D0%BC%D1%83%D1%81%D0%BE%D1%80%D0%BD%D1%8B%D0%B9%20%231%2C%20%D0%B4%D1%83%D0%B1%D0%BB%D0%B8%2C%20%D0%B1%D0%B8%D1%82%D1%8B%D0%B5%20%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B8%2C%20%D1%87%D0%B5%D0%BC%20%D0%B7%D0%B0%D0%BC%D0%B5%D0%BD%D0%B8%D1%82%D1%8C%29.md)
- Легальные стенды для практики: [7 репозиториев для практики в ИБ](../Pentest/Web/7%20%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B5%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B8%20%D0%B2%20%D0%98%D0%91%20%28WebGoat%2C%20Juice%20Shop%2C%20DVWA%2C%20HackTricks%2C%20PayloadsAllTheThings%2C%20h4cker%2C%20bug%20bounty%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md)

## 🔗 Ссылки

- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Education #Security #Обучение #Подборка #Проверка
