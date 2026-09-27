---
создал заметку: 2026-09-27T19:10:00
author: WhiteK0T
tags:
  - Education
  - Security
  - Обучение
  - Подборка
  - Проверка
Источник:
  - https://t.me/c/2675453029/1493
---

# 📚 «5 GitHub-репозиториев по ИБ» из поста — проверка

Пост из CodeGuard обещает «5 репозиториев, которые заменят десяток курсов по ИБ, всё актуально на 2026». Проверил каждую ссылку по GitHub на 27.09.2026 — и подборка оказалась **небрежной**: одна ссылка ведёт вообще не туда, два пункта из пяти — это **один и тот же** репозиторий, один заявленный репозиторий не существует по указанному адресу, а «регулярно обновляется» местами неправда. Ниже — что там на самом деле и чем это заменить.

> [!danger] Короткий вердикт
> Из 5 пунктов **надёжен по сути один** (okhosting). Реально уникальных репозиториев в списке — **три**, а не пять. Пункт №1 — посторонний репозиторий на 2 звезды. Ссылки замусорены (яндекс-трекер `?ysclid=`, неверные имена/авторы).

---

## 🔎 Разбор по пунктам

### 1. «awesome-security-tools-2026» → на деле [`spinov001-art/awesome-ai-tools-2026`](https://github.com/spinov001-art/awesome-ai-tools-2026)
🚩 **Главный прокол.** В посте пункт назван *security-tools*, а ссылка ведёт на репозиторий про **AI-tools**. При этом репо **свежее и пустое по авторитету**: создан в марте 2026, **★ 2**. Ни о каких «150+ инструментов для пентеста, проверенных временем» речи нет — это не тот масштаб и не та тема. **Не использовать.**
Чем заменить (проверенные крупные списки): [enaqx/awesome-pentest](https://github.com/enaqx/awesome-pentest) (★27k), [sbilly/awesome-security](https://github.com/sbilly/awesome-security) (★15k), [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) (★246k).

### 2. [`okhosting/awesome-cyber-security`](https://github.com/okhosting/awesome-cyber-security) ✅
**Единственный пункт без нареканий.** ★ 757, живой (обновлялся 09.2026), с 2021. Инструменты + платформы для обучения, курсы, сообщества, сертификации. Как заявлено, так и есть.

### 3. «Cybersecurity_resources» → ссылка на [`vatsalgupta67/All-In-One-CyberSecurity-Resources`](https://github.com/vatsalgupta67/All-In-One-CyberSecurity-Resources) ⚠️
Репозиторий существует (★ 600, с 2022) — большая коллекция бесплатных книг (Python для пентеста, форензика, реверс). **Но:** в посте он подписан именем `Cybersecurity_resources`, а это **имя чужого репозитория** (см. п.5). И «регулярно обновляется» — **неправда**: последний коммит — **август 2024**, больше года тишины.

### 4. [`artroneee/Cyber-Security-Collection`](https://github.com/artroneee/Cyber-Security-Collection) ⚠️
Существует, но **маленький и малоизвестный**: ★ 11, создан в конце 2024. Материалы по анализу атак (артефакты Windows, IOC Linux, веб-уязвимости) — тематически для Blue Team полезно, но это **личная подборка одного автора**, а не проверенный сообществом ресурс. Оценивать критически.

### 5. «Cybersecurity-Resources (arceuzvx)» → ссылка снова на `vatsalgupta67/All-In-One…` (+ `?ysclid=…`) 🚩
Тройная ошибка в одном пункте:
- **это дубль п.3** — ссылка ведёт на тот же репозиторий vatsalgupta67;
- к ссылке прицеплен **яндексовый трекинг-параметр** `?ysclid=mu56u79yq2375567757` (мусор, стоит убирать);
- заявленный репозиторий **`arceuzvx/Cybersecurity-Resources` (через дефис) не существует — 404**.

Что автор, видимо, имел в виду: у пользователя `arceuzvx` действительно есть **[`Cybersecurity_resources`](https://github.com/arceuzvx/Cybersecurity_resources)** — **через подчёркивание**, ★ 122, коллекция бесплатных книг (в т.ч. «The Art of Memory Forensics»). Вот это — реальный отдельный репозиторий, который пост промахнулся указать.

---

## 🧩 Что реально есть (сводка)

| В посте | Реальный репозиторий | Статус | Вердикт |
| :--- | :--- | :--- | :--- |
| №1 security-tools | `spinov001-art/awesome-ai-tools-2026` | ★2, не по теме | ❌ мусор/мислинк |
| №2 awesome-cybersecurity | `okhosting/awesome-cyber-security` | ★757, живой | ✅ годно |
| №3 Cybersecurity_resources | `vatsalgupta67/All-In-One-CyberSecurity-Resources` | ★600, застыл 08.2024 | ⚠️ ок как архив книг |
| №4 Cyber-Security-Collection | `artroneee/Cyber-Security-Collection` | ★11, личное | ⚠️ на свой риск |
| №5 (arceuzvx) | заявленный **404**; реальный — `arceuzvx/Cybersecurity_resources` | ★122 | ⚠️ и это дубль книг |

Итого **уникальных** ресурса три: okhosting (списки/курсы), vatsalgupta67 (книги, но стоит), arceuzvx (книги). Плюс маленький artroneee для Blue Team.

---

## 🛡️ Практика: как относиться к таким «подборкам»

- **Проверять ссылку, а не подпись.** Здесь имя пункта и URL расходятся в 3 из 5 случаев — классический признак наспех собранного/сгенерированного поста.
- **Чистить трекеры.** `?ysclid=…` (Яндекс), `?utm_…`, `fbclid` — обрезать хвост после `?`.
- **Смотреть возраст и звёзды.** ★2 и создание месяц назад — не «проверено временем». Для awesome-списков ориентир — тысячи звёзд и свежие коммиты.
- **«Регулярно обновляется» — проверяемо.** Дата последнего коммита на странице репозитория. У vatsalgupta67 — август 2024.

> [!tip] Что скачать книги офлайн
> Списки книг (vatsalgupta67, arceuzvx) — это в основном ссылки на PDF. Для оффлайн-архива удобно `git clone` + пройтись по ссылкам; но помни про **легальность** — многие «бесплатные PDF» книг по ИБ нарушают копирайт. Легальные источники: No Starch/Packt-распродажи, Humble Bundle, официальные бесплатные издания (напр., у NIST, OWASP).

---

## 🖥️ На системах владельца

Ставить нечего — это контент. `git clone` работает откуда угодно; на роутере (Entware) смысла держать нет.

## 🔗 Связанные заметки

- Разобранная ранее подборка обучающих репозиториев (там всё оказалось по делу): [7 репозиториев для практики в ИБ](../Pentest/Web/7%20%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B5%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B8%20%D0%B2%20%D0%98%D0%91%20%28WebGoat%2C%20Juice%20Shop%2C%20DVWA%2C%20HackTricks%2C%20PayloadsAllTheThings%2C%20h4cker%2C%20bug%20bounty%29%20%E2%80%94%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80.md)
- Каталог курсов с сертификатами (тоже с проверкой заявленного): [awesome-certificates](awesome-certificates%20%28PanXProject%29%20%E2%80%94%20%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20200%2B%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D1%85%20%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2%20%D1%81%20%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%B0%D0%BC%D0%B8%20%28IT-CS-%D0%B4%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B.md)

## 🔗 Ссылки

- Годные: [okhosting/awesome-cyber-security](https://github.com/okhosting/awesome-cyber-security) · [vatsalgupta67/All-In-One-CyberSecurity-Resources](https://github.com/vatsalgupta67/All-In-One-CyberSecurity-Resources) · [arceuzvx/Cybersecurity_resources](https://github.com/arceuzvx/Cybersecurity_resources)
- Замена «пункту №1» (крупные проверенные списки): [enaqx/awesome-pentest](https://github.com/enaqx/awesome-pentest) · [sbilly/awesome-security](https://github.com/sbilly/awesome-security) · [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge)
- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Education #Security #Обучение #Подборка #Проверка
