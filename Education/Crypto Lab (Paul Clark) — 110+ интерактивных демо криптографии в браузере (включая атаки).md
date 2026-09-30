---
создал заметку: 2026-09-30T11:40:00
author: WhiteK0T
tags:
  - Education
  - Security
  - Cryptography
  - PostQuantum
  - Обучение
Источник:
  - https://t.me/c/2675453029/1530
  - https://crypto-lab.systemslibrarian.dev/
  - https://github.com/systemslibrarian/crypto-lab
---

# 🔐 Crypto Lab — 110+ интерактивных демо криптографии в браузере

**Crypto Lab** ([crypto-lab.systemslibrarian.dev](https://crypto-lab.systemslibrarian.dev/), репозиторий [systemslibrarian/crypto-lab](https://github.com/systemslibrarian/crypto-lab), **MIT**) — набор из 110+ интерактивных демонстраций криптографии, работающих **прямо в браузере**: без установки, аккаунтов, API-ключей и телеметрии. Ценно тем, что показывает не только «как работает», но и «как ломается» — на реальных атаках. Автор — **Paul Clark** (ник `systemslibrarian`); проект разложен на ~200 отдельных репозиториев `crypto-lab-*` (каждое демо — свой репо).

> [!note] Это **один человек** и учебный проект, а не учебник
> Пост пишет «по глубине не уступает университетским курсам» — breadth впечатляет, но это **хобби-проект одного мейнтейнера**, не рецензируемый материал. Отлично для **интуиции** и «пощупать руками», но для строгости дополнять стандартными источниками (Katz–Lindell, курсы Cryptopals, NIST-документы). А награду «Gold Winner 2026 Cybersecurity Excellence Awards» стоит воспринимать как **заявление проекта** — не независимо проверенный факт.

---

## 📚 Что внутри

**Примитивы и протоколы:** симметричное/асимметричное шифрование, хеши, обмен ключами, цифровые подписи, **ZK-proofs** (SNARK/STARK/Bulletproofs), **гомоморфное шифрование** (TFHE, BGV/BFV, CKKS), **MPC** (secure multi-party computation), threshold-схемы.

**Пост-квантовый трек** (актуально — см. связанные заметки):
- lattice: **ML-KEM**, **ML-DSA**, **Falcon**;
- code-based: **Classic McEliece**, **BIKE**;
- hash-based: **SPHINCS+**;
- isogeny.

**Атаки (сильная часть) — рабочие, не анимации:**
- бэкдор **Dual_EC_DRBG** с предсказанием будущих выходов;
- **padding-oracle** Vaudenay — побайтовое восстановление открытого текста (AES-CBC + PKCS#7);
- **KyberSlash** — timing-утечка;
- восстановление ключа **ECDSA** через lattice-атаку на смещённый/повторный nonce.

**Learning Paths** — 4 готовых маршрута: **Developer** (от примитивов к протоколам), **Cryptanalyst** (от классики к PQ side-channel), **Post-Quantum** (KEM, подписи, гибриды, миграция), **Key Exchange** (от ECDH к гибридным PQ-рукопожатиям).

---

## ⚠️ Важная оговорка про «крипту в браузере»

Демо запускают **настоящие** алгоритмы, и это здорово для понимания. Но это **учебный** код: **не переносить его в прод**. Реальная криптография требует проверенных библиотек (constant-time реализации, аудит) — именно в таких деталях (как в демо KyberSlash) и живут side-channel-уязвимости. Crypto Lab учит *видеть* эти проблемы, а не поставляет боевые реализации.

---

## 🖥️ Применимость / на системах владельца

Это веб-сайт — ставить нечего, работает в любом браузере офлайн после загрузки. При желании — **self-host**: `git clone` (статический HTML) и открыть локально, без бэкенда. От ОС не зависит.

Тема владельцу близка: у него есть заметки по JCA и пост-квантовым подписям, PQ-шифроконтейнер и TLS-туннели — Crypto Lab хорошо «оживляет» эту теорию (ML-KEM, гибридные рукопожатия, подписи).

## 🔗 Связанные заметки

- Практика крипты в коде (Java): [Ключи в Java (JCA) — KeyFactory/KeyPairGenerator, ECC, постквант](../Programming/Java/Crypto/%D0%9A%D0%BB%D1%8E%D1%87%D0%B8%20%D0%B2%20Java%20%28JCA%29%20%E2%80%94%20%D1%87%D1%82%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyFactory%20%D0%B8%20%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20%D1%87%D0%B5%D1%80%D0%B5%D0%B7%20KeyPairGenerator%20%28SPI%2C%20KeySpec%2C%20PEM-DER%2C%20ECC%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%29.md)
- Пост-квант на практике (ML-KEM): [LUKSbox (PentHertz)](../Security/LUKSbox%20%28PentHertz%29%20%E2%80%94%20%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D1%88%D0%B8%D1%84%D1%80%D0%BE%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%20%D0%BD%D0%B0%20Rust%20%28FIDO2%2C%20TPM%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%BA%D0%B2%D0%B0%D0%BD%D1%82%20ML-KEM%29%2C%20%D1%87%D1%82%D0%BE%20%D1%8D%D1%82%D0%BE%20%D0%B8%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%20%C2%ABpre-1.0%C2%BB.md)

## 🔗 Ссылки

- Сайт: [crypto-lab.systemslibrarian.dev](https://crypto-lab.systemslibrarian.dev/) · репозиторий: [systemslibrarian/crypto-lab](https://github.com/systemslibrarian/crypto-lab)
- Источник новости: пост в закрытом канале CodeGuard: PySec Edition

#Education #Security #Cryptography #PostQuantum #Обучение
