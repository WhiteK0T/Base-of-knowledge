---
создал заметку: 2026-07-12T12:00:00
author: WhiteK0T
tags:
  - Network
  - Security
  - Architecture
  - ZeroTrust
  - SASE
  - OT
  - BestPractice
Источник:
  - https://t.me/alukatsky/14966
  - https://t.me/alukatsky/14967
---

# 🏛️ Архитектура сетевой безопасности — референсные документы

Подборка **Алексея Лукацкого** ([@alukatsky](https://t.me/alukatsky/14966)) — 16 публичных источников, по которым можно понять, **что такое архитектура сетевой безопасности**: как раскладывать сеть на сегменты/зоны/модули, где и зачем ставить защитные меры, как увязывать бизнес-потоки с контролем. Это **не инструменты, а «карта местности»**: reference-архитектуры вендоров, нейтральные стандарты и отраслевые примеры.

> [!tip] С чего начать (если читать не всё подряд)
> 1. **Нейтральная база →** [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) (Zero Trust) + [ISO/IEC 27033](https://www.iso.org/standard/63461.html) (прямой стандарт про сетевую безопасность).
> 2. **Логика построения →** [Cisco SAFE](https://www.cisco.com/go/safe) (зоны/модули/потоки) — вендорский, но самый наглядный для «как думать».
> 3. **Твоя среда →** облако (AWS/Azure/GCP SRA), платёжка (PCI DSS) или **АСУ ТП/OT** (IEC 62443) — по профилю.
>
> Дальше — по интересу: SASE/SSE, микросегментация, распределённая ИБ.

## 📚 Источники по категориям

### 🧭 Zero Trust (концепция и внедрение)

| # | Источник | Чем полезно | Нейтральность |
| :-- | :--- | :--- | :--- |
| 1 | [**NIST SP 800-207** — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) | Базовый документ по ZT: сдвиг от «доверенной внутренней сети» к решениям вокруг пользователей, устройств, ресурсов, политик и контекста | 🟢 нейтральный |
| 2 | [**NSA ZT Guidance — Network & Environment Pillar**](https://www.nsa.gov/Cybersecurity/ZIG/Pillars/Network-and-Environment-Pillar/) | Именно **сетевая** часть ZT: сегментация, ограничение lateral movement, контроль потоков, мониторинг внутренних/внешних коммуникаций | 🟢 нейтральный |
| 3 | [**Palo Alto — Zero Trust Enterprise Design Guide**](https://www.paloaltonetworks.com/resources/guides/zero-trust-overview) | Как ZT раскладывается на пользователей, приложения и инфраструктуру | 🟡 вендорский уклон |
| 4 | [**Microsoft — Zero Trust Adoption Framework**](https://learn.microsoft.com/en-us/security/zero-trust/adopt/zero-trust-adoption-overview) | Разложить модернизацию ИБ по этапам (см. также его Cloud Security Benchmark ниже) | 🟡 Azure/Entra-центрично |

> [!info] Полезное дополнение к #1: NIST SP 800-207A (2023)
> К «классике» 800-207 есть спутник — [**NIST SP 800-207A**](https://csrc.nist.gov/pubs/sp/800/207/a/final) (сент. 2023): ZT-модель контроля доступа для **cloud-native / multi-cloud** приложений (микросервисы, API-gateway, sidecar-прокси, identity вроде **SPIFFE**). Если инфраструктура — это распределённые микросервисы, читать вместе с 800-207.

### 🌐 SASE / SSE (современный периметр «в облаке»)

| # | Источник | Чем полезно | Нейтральность |
| :-- | :--- | :--- | :--- |
| 5 | [**Cloudflare — SASE Reference Architecture**](https://developers.cloudflare.com/reference-architecture/) | Как совмещаются сетевой доступ, проверка пользователей, защита приложений, фильтрация трафика и **единая политика** для распределённой компании; есть диаграммы и сценарии эволюции к SASE | 🟡 вендорский, но структура применима |

### 🏢 Вендорские архитектуры сетевой безопасности

| # | Источник | Чем полезно | Нейтральность |
| :-- | :--- | :--- | :--- |
| 6 | [**Cisco Security Reference Architecture / SAFE**](https://www.cisco.com/go/safe) | **Лучшая точка входа в логику**: сегменты/модули/зоны, потоки, где и зачем защитные меры; десятки архитектур под разные задачи и участников | 🟡 вендор, но методология наглядна |
| 7 | [**Juniper Connected Security / Distributed Services Architecture**](https://www.juniper.net/documentation/product/us/en/connected-security-distributed-services/) | Идея **распределённой ИБ**: безопасность не только «на периметре», а на всех точках подключения. DSA = централизованно управляемый логический масштабируемый firewall (у других вендоров позже — **Mesh Firewall**) | 🟡 вендорский |
| 8 | [**Fortinet — Security Fabric for OT**](https://www.fortinet.com/content/dam/fortinet/assets/white-papers/wp-operational-technology-design-guide.pdf) | Пример модели «**security fabric**»: единая связанная защита сети, облаков, конечных точек и OT. **Читать критически** — это скорее концепция платформенной интеграции одного вендора, чем нейтральная архитектура | 🔴 вендорская концепция |

### 🧩 Микросегментация

| # | Источник | Чем полезно | Нейтральность |
| :-- | :--- | :--- | :--- |
| 9 | [**Akamai Guardicore — Segmentation / Microsegmentation**](https://www.akamai.com/products/akamai-guardicore-segmentation) | Борьба с **lateral movement**: картирование потоков, понимание зависимостей приложений, политики на основе **реального** взаимодействия workloads | 🟡 вендорский, но подход универсален |

### ☁️ Облачные Security Reference Architecture

| # | Источник | Чем полезно | Нейтральность |
| :-- | :--- | :--- | :--- |
| 10 | [**AWS Security Reference Architecture**](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/introduction.html) | Как облачный провайдер видит ИБ в многоаккаунтной среде: функциональные аккаунты, сервисы безопасности, типовая многоуровневая архитектура приложения | 🟢 для своей платформы — «канон» |
| 11 | [**Microsoft Cloud Security Benchmark**](https://learn.microsoft.com/en-us/security/benchmark/azure/) | Рекомендации по сетевой безопасности, identity, привилегированному доступу, защите данных, логированию и защите от угроз (Azure/M365/Entra ID) | 🟢 для своей платформы |
| 12 | [**Google Cloud — Enterprise Foundations Blueprint / Security Foundations Guide**](https://docs.cloud.google.com/architecture/blueprints/security-foundations) | То же для **GCP**: [PDF-гайд](https://services.google.com/fh/files/misc/google-cloud-security-foundations-guide.pdf) | 🟢 для своей платформы |

### 📋 Стандарты и compliance

| # | Источник | Чем полезно | Нейтральность |
| :-- | :--- | :--- | :--- |
| 13 | [**PCI DSS v4.0.1 + PCI SSC Scoping & Segmentation Guidance**](https://docs-prv.pcisecuritystandards.org/Guidance%20Document/PCI%20DSS%20General/PCI-DSS-Scoping-and-Segmentation-Guidance-for-Modern-Network-Architectures.pdf) | Главный пример для **платёжной** инфраструктуры: определить **CDE** (cardholder data environment), минимизировать область PCI DSS, **отделить CDE**, контролировать потоки, **тестировать эффективность сегментации** | 🟢 отраслевой стандарт |
| 14 | [**ISO/IEC 27033 — Network Security**](https://www.iso.org/standard/63461.html) | Пожалуй, **самый прямой международный стандарт про сетевую безопасность**: устройства, приложения, сервисы, коммуникации между сетями, шлюзы безопасности, VPN, беспроводной доступ | 🟢 нейтральный (платный) |

### 🏭 OT / АСУ ТП (промышленные сети)

| # | Источник | Чем полезно | Нейтральность |
| :-- | :--- | :--- | :--- |
| 15 | [**IEC 62443 / ISA-62443**](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) | Обязательный источник для АСУ ТП. Ключевая концепция — **зоны и каналы** (zones & conduits): группировать активы в зоны с едиными требованиями и контролировать связь между зонами через каналы | 🟢 нейтральный (платный) |
| 16 | [**NIST SP 800-82 Rev.3 — Guide to OT Security**](https://csrc.nist.gov/pubs/sp/800/82/r3/final) | Очень практичный документ по защите АСУ ТП с учётом требований к **производительности, надёжности и безопасности** техпроцессов | 🟢 нейтральный |
| — | [**ENISA — Zoning and Conduits for Railways**](https://www.enisa.europa.eu/sites/default/files/publications/Zoning%20and%20Conduits%20for%20Railways%20-%20Security%20Architecture.pdf) | Отраслевой **пример** применения модели зон/каналов, оценки рисков и целевой архитектуры (ЖД, но образец переносим на любую отрасль) | 🟢 нейтральный |

## ⚠️ Как читать эту подборку (факты против маркетинга)

> [!warning] Вендорские материалы = логика хорошая, продукт — опционально
> Половина списка (Cisco, Palo Alto, Fortinet, Juniper, Cloudflare, Akamai) — **маркетинг-архитектуры вендоров**. Ценность в них — **принципы** (сегментация, зоны, потоки, ZT, микросегментация), а не конкретный SKU. Бери **методологию**, а привязку «только наш Fabric/только наш firewall» отбрасывай. Для нейтрального взгляда сверяйся с **NIST 800-207/800-82, ISO/IEC 27033, IEC 62443**.

> [!note] «Zero Trust» ≠ галочка и ≠ продукт
> Как подчёркивает и сам Лукацкий, ценность 800-207 **не в том, что «все теперь ZT»**, а в **сдвиге мышления**: доверие не выдаётся по факту нахождения «внутри сети», а вычисляется динамически по пользователю/устройству/ресурсу/контексту. Купить «Zero Trust» как коробку нельзя — это принцип проектирования.

> [!info] Облачные SRA — «канон для своей платформы»
> AWS SRA / Microsoft CSB / Google Foundations описывают, как **сам провайдер** рекомендует раскладывать ИБ в его облаке. Это близко к обязательному чтению, если инфраструктура там живёт, но между провайдерами модели **не взаимозаменяемы**.

## 🇷🇺 Контекст РФ: чем это дополнить локально

> [!tip] Международные документы задают логику, но в РФ есть свои обязательные требования
> Эти источники хороши как **методология**, но для регуляторики в России держи рядом отечественные акты (полезно как «перевод» тех же идей сегментации/зонирования на язык требований ФСТЭК/ЦБ):
> - **КИИ / значимые объекты:** [187-ФЗ](http://www.kremlin.ru/acts/bank/42128) + **приказ ФСТЭК № 239** (аналог «зон и каналов» для критической инфраструктуры).
> - **АСУ ТП:** **приказ ФСТЭК № 31** — прямой аналог IEC 62443/NIST 800-82 для российских промышленных систем.
> - **ГИС / гос-ИС:** **приказ ФСТЭК № 17**; **ПДн:** **приказ ФСТЭК № 21** + **152-ФЗ**.
> - **Банки/финансы (аналог PCI DSS):** **ГОСТ Р 57580.1/.2** + требования ЦБ (Положения 683-П/747-П и др.).
> - **Реестры угроз/уязвимостей:** [БДУ ФСТЭК и НКЦКИ — см. заметку про базы уязвимостей](../Security/Vulns/%D0%91%D0%B0%D0%B7%D1%8B%20%D1%83%D1%8F%D0%B7%D0%B2%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B5%D0%B9%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D0%B5%D0%BD%D1%82%D0%B5%D1%81%D1%82%D0%B5%D1%80%D0%B0%20%E2%80%94%20%D0%B3%D0%B4%D0%B5%20%D0%B8%D1%81%D0%BA%D0%B0%D1%82%D1%8C%20%28CVE%2C%20%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A%2C%20%D0%9D%D0%9A%D0%A6%D0%9A%D0%98%2C%20MITRE%20ATT%26CK%2C%20Exploit-DB%29.md).

## 🔗 Ссылки

- Источник (пост 1/2): [@alukatsky #14966](https://t.me/alukatsky/14966) · [окончание #14967](https://t.me/alukatsky/14967) · теги `#архитектура #bestpractice`
- Связанные заметки: [Модель OSI («Сложно о простом»)](OSI/%D0%A1%D0%BB%D0%BE%D0%B6%D0%BD%D0%BE%20%D0%BE%20%D0%BF%D1%80%D0%BE%D1%81%D1%82%D0%BE%D0%BC.%20%D0%9C%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C%20OSI..md) · [IPTables (практическая сегментация на Linux)](IPTables.md) · [Базы уязвимостей (CVE/ФСТЭК/НКЦКИ)](../Security/Vulns/%D0%91%D0%B0%D0%B7%D1%8B%20%D1%83%D1%8F%D0%B7%D0%B2%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B5%D0%B9%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D0%B5%D0%BD%D1%82%D0%B5%D1%81%D1%82%D0%B5%D1%80%D0%B0%20%E2%80%94%20%D0%B3%D0%B4%D0%B5%20%D0%B8%D1%81%D0%BA%D0%B0%D1%82%D1%8C%20%28CVE%2C%20%D0%A4%D0%A1%D0%A2%D0%AD%D0%9A%2C%20%D0%9D%D0%9A%D0%A6%D0%9A%D0%98%2C%20MITRE%20ATT%26CK%2C%20Exploit-DB%29.md)

#Network #Security #Architecture #ZeroTrust #SASE #OT #BestPractice
