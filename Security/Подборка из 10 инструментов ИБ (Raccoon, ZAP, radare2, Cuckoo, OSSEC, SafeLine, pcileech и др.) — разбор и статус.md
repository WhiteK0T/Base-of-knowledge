---
создал заметку: 2026-09-27T18:30:00
author: WhiteK0T
tags:
  - Security
  - Tools
  - BlueTeam
  - Pentest
  - ReverseEngineering
  - Подборка
Источник:
  - https://t.me/c/2675453029/1488
---

# 🧰 Подборка из 10 инструментов ИБ — разбор и статус

Пост из CodeGuard перечисляет 10 security-инструментов «просто подборкой». Список **разношёрстный**: тут и наступательные сканеры, и blue-team, и реверс, и песочница, и WAF, и DMA-железо. Проверил каждый по GitHub на 27.09.2026 — и это тот случай, где **проверка нужна**: один проект мёртв, ещё один давно не развивается, а пара описаний в посте неточны. Ниже — по группам, с реальным статусом.

> [!warning] Коротко, что важно знать до клонирования
> - 🪦 **Cuckoo Sandbox — архивирован** (последний коммит 05.2022). Живой преемник — **CAPEv2**.
> - 💤 **Raccoon** — реального развития нет: последний коммит (06.2025) это автоматический бамп зависимости. Ниша recon лучше закрыта другими.
> - 🔀 **Cutter** по ссылке из поста (`rizinorg/cutter`) работает на движке **Rizin** (форк r2), а **не на radare2 напрямую** — пара «radare2 + Cutter» из поста технически уже разошлась.
> - 🔌 **pcileech** без **специального железа (FPGA)** — это не «скачал и запустил».
> - 🛡️ **OSSEC** жив, но многие давно мигрировали на его форк **Wazuh**.

---

## 🔍 Наступление: recon и веб

| Инструмент | ★ | Статус | Разбор |
| :--- | :---: | :--- | :--- |
| **[Raccoon](https://github.com/evyatarmeged/Raccoon)** | ~4k · MIT | 💤 стагнация (с 2018, коммиты только dependabot) | всё-в-одном recon-CLI на Python: DNS, порты, веб-фингерпринт, поиск поддоменов. Идея хорошая, но **проект не развивается** — на реальном пентесте нишу лучше закрывает связка `nmap` + `amass`/`subfinder` + `httpx`, либо `reconFTW` |
| **[AutoRecon](https://github.com/Tib3rius/AutoRecon)** | активен | ✅ | не сканер сам по себе, а **оркестратор**: запускает цепочку известных инструментов (nmap, feroxbuster, gobuster…) и раскладывает результат по папкам. Требует, чтобы эти инструменты **уже стояли** (родная среда — Kali). Классика для OSCP-энумерации |
| **[ZAP](https://github.com/zaproxy/zaproxy)** | ~15.8k · Apache-2.0 | ✅ активен | прокси-сканер веб-приложений: пассивный + активный поиск уязвимостей, фаззинг, API для CI. Нюанс: с 2024 это **просто «ZAP», уже не «OWASP ZAP»** (проект ушёл из OWASP, спонсируется Checkmarx). Функционально — главная бесплатная альтернатива Burp |

## 🧬 Реверс-инжиниринг

| Инструмент | ★ | Статус | Разбор |
| :--- | :---: | :--- | :--- |
| **[radare2](https://github.com/radareorg/radare2)** | ~24.9k | ✅ очень активен | CLI-фреймворк для анализа бинарей и памяти: дизассемблер, отладчик, патчинг. Мощный, но крутая кривая обучения |
| **[Cutter](https://github.com/rizinorg/cutter)** | ~19.8k · GPL-3.0 | ✅ активен | GUI-фронтенд. ⚠️ **Важно:** современный Cutter построен на **Rizin** (форк radare2, 2020), а не на самом radare2. Пост подаёт их как одну связку — на деле это уже две ветки. Для r2-центричного GUI существует отдельный `iaito` |

## 🦠 Анализ malware (песочница)

| Инструмент | ★ | Статус | Разбор |
| :--- | :---: | :--- | :--- |
| **[Cuckoo Sandbox](https://github.com/cuckoosandbox/cuckoo)** | ~6k | 🪦 **архивирован (05.2022)** | автоматический запуск подозрительных образцов с записью поведения, трафика, артефактов. **Мёртв**: Python 2, не поддерживается. **Брать преемника — [CAPEv2](https://github.com/kevoreilly/CAPEv2)** (kevoreilly): активная разработка, распаковка/дамп конфигов malware, современные ОС |

## 🛡️ Защита / Blue Team

| Инструмент | ★ | Статус | Разбор |
| :--- | :---: | :--- | :--- |
| **[BlueTeam-Tools](https://github.com/A-poc/BlueTeam-Tools)** | ~4.5k | ✅ | awesome-список инструментов защиты: мониторинг, лог-анализ, форензика, DLP, сетевые сенсоры. Не софт, а **каталог** — точка входа, откуда выбирать |
| **[OSSEC](https://github.com/ossec/ossec-hids)** | ~5k · GPL-2.0 | ✅ жив, но… | хостовый IDS: анализ логов, контроль целостности ФС, rootkit-чекер, алерты по правилам. Работает, но большинство новых внедрений идут на его форк **[Wazuh](https://github.com/wazuh/wazuh)** (~17k★) — тот же корень + дашборд, агенты, интеграции. Для новой установки смотреть сначала Wazuh |
| **[SafeLine](https://github.com/chaitin/safeline)** | ~22.7k · GPL-3.0 | ✅ очень популярен | reverse-proxy со встроенным **WAF** от Chaitin: защита HTTP, правила, дашборд, простой деплой в Docker/K8s. Самый «звёздный» проект подборки; реальная бесплатная альтернатива коммерческим WAF для своего сайта |

## 📊 Аналитика

| Инструмент | ★ | Статус | Разбор |
| :--- | :---: | :--- | :--- |
| **[awesome-annual-security-reports](https://github.com/jacobdjwilson/awesome-annual-security-reports)** | ~1.2k · MIT | ✅ свежий | каталог **годовых отчётов** по угрозам/инцидентам/трендам от вендоров. Полезно для аналитики и обоснования решений, не инструмент |

## 🔌 Аппаратные атаки (DMA)

| Инструмент | ★ | Статус | Разбор |
| :--- | :---: | :--- | :--- |
| **[pcileech](https://github.com/ufrisk/pcileech)** | ~7.9k · AGPL-3.0 | ✅ активен | дамп/патч RAM через **PCIe/DMA**, обход экрана блокировки и т.п. ⚠️ Ключевое, чего в посте нет: для DMA-атак нужен **специальный аппарат** — FPGA-плата (Screamer/PCILeech-FPGA) или старый USB3380. Чисто софтом (без физического доступа и железа) это не работает. Смежный проект того же автора для анализа дампов памяти — **MemProcFS** |

---

## 🧭 Как это читать

Подборка полезна как «что вообще бывает», но это **микс из семи разных задач**, а не набор «поставь всё». По уму:

- **защита своих машин/сайта** → SafeLine (WAF), Wazuh/OSSEC (HIDS), BlueTeam-Tools (откуда брать остальное);
- **реверс** → radare2 + Cutter (помня про Rizin);
- **анализ malware** → CAPEv2, а не Cuckoo;
- **свой пентест/CTF** → AutoRecon (в Kali), ZAP по вебу; Raccoon — по желанию, но без иллюзий про поддержку;
- **аппаратная безопасность** → pcileech, если есть железо.

---

## 🖥️ На системах владельца

Почти всё — Linux-родное и часто заворачивается в Docker.

| Инструмент | Как ставить (Gentoo/Debian/Arch) |
| :--- | :--- |
| SafeLine / ZAP / CAPEv2 | Docker/Compose — самый простой путь; ZAP есть и как пакет/`zap.sh` |
| radare2 / Cutter | radare2: `emerge dev-util/radare2`, в Debian `apt install radare2`, Arch `pacman -S radare2`; Cutter — AppImage/`flatpak`/AUR |
| OSSEC / Wazuh | из исходников/официальных репозиториев; Wazuh — Docker или пакеты |
| AutoRecon / Raccoon | Python + `pipx`; AutoRecon тянет за собой кучу CLI-инструментов (проще в Kali/контейнере) |
| pcileech | софт собирается, но нужен **FPGA-девайс**; на роутере/десктопе владельца без него смысла нет |

> [!note] Entware / RT-AX56U
> Для роутера из этого списка практичен разве что смысловой уровень (понимать, что такое HIDS/WAF). Тяжёлые инструменты (ZAP, Cutter, CAPEv2) на armv7 с 512 МБ RAM не для роутера.

> [!warning] Право
> В подборке смешаны оборонительные и **наступательные** инструменты (Raccoon, AutoRecon, ZAP-active-scan, pcileech). Наступательные — только по своим/авторизованным целям (ст. 272 УК РФ). pcileech подразумевает **физический доступ** к машине — законен только к своей или по разрешению.

## 🔗 Связанные заметки

- Реверс через MCP поверх того же radare2: [Reversecore MCP](Reverse-Engineering/Reversecore%20MCP%20%E2%80%94%20MCP-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%B5%D0%B2%D0%B5%D1%80%D1%81-%D0%B8%D0%BD%D0%B6%D0%B8%D0%BD%D0%B8%D1%80%D0%B8%D0%BD%D0%B3%D0%B0%20%D0%B8%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%20malware%20%28Radare2-r2ghidra-YARA%29.md)
- Обезвреживание подозрительных документов (перед песочницей): [Dangerzone](Dangerzone%20%28Freedom%20of%20the%20Press%29%20%E2%80%94%20%D0%BE%D0%B1%D0%B5%D0%B7%D0%B2%D1%80%D0%B5%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D1%8B%D1%85%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B2%20%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D1%8B%D0%B9%20PDF%20%28CDR%2C%20%D0%BF%D0%B5%D1%81%D0%BE%D1%87%D0%BD%D0%B8%D1%86%D0%B0%29.md)
- Определить тип неизвестного образца до анализа: [TrID](Forensics/TrID%20%28Marco%20Pontello%29%20%E2%80%94%20%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%82%D0%B8%D0%BF%D0%B0%20%D1%84%D0%B0%D0%B9%D0%BB%D0%B0%20%D0%BF%D0%BE%20%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D0%BE%D0%B9%20%D1%81%D0%B8%D0%B3%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B5%20%28freeware%2C%2022k%20%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%BE%D0%B2%29.md)

## 🔗 Ссылки

- [Raccoon](https://github.com/evyatarmeged/Raccoon) · [BlueTeam-Tools](https://github.com/A-poc/BlueTeam-Tools) · [awesome-annual-security-reports](https://github.com/jacobdjwilson/awesome-annual-security-reports) · [OSSEC](https://github.com/ossec/ossec-hids) · [SafeLine](https://github.com/chaitin/safeline) · [ZAP](https://github.com/zaproxy/zaproxy) · [radare2](https://github.com/radareorg/radare2) · [Cutter](https://github.com/rizinorg/cutter) · [Cuckoo](https://github.com/cuckoosandbox/cuckoo) · [AutoRecon](https://github.com/Tib3rius/AutoRecon) · [pcileech](https://github.com/ufrisk/pcileech)
- Актуальные преемники: [CAPEv2](https://github.com/kevoreilly/CAPEv2) (вместо Cuckoo) · [Wazuh](https://github.com/wazuh/wazuh) (форк OSSEC)
- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Security #Tools #BlueTeam #Pentest #ReverseEngineering #Подборка
