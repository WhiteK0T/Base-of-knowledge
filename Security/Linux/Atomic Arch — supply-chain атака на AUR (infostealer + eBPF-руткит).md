---
создал заметку: 2026-06-17T21:40:00
author: WhiteK0T
tags:
  - Безопасность
  - SupplyChain
  - Arch
  - AUR
  - Malware
  - eBPF
Источник:
  - https://t.me/IzHmfluzM81OTAy/583
  - https://www.sonatype.com/blog/atomic-arch-npm-campaign-adds-malicious-dependency
  - https://www.phoronix.com/news/Arch-Linux-AUR-400-Compromised
  - https://thehackernews.com/2026/06/over-400-arch-linux-aur-packages.html
  - https://github.com/lenucksi/aur-malware-check
---

# 🦠 Atomic Arch — supply-chain атака на AUR (infostealer + eBPF-руткит)

> [!danger] TL;DR
> Июнь 2026: масштабная **атака на цепочку поставок Arch User Repository (AUR)**. Злоумышленники **«усыновляли» заброшенные (orphaned) пакеты** (и подделывали коммиты от имени мейнтейнера `arojas`), правили `PKGBUILD` и `.install`-хуки так, чтобы при установке тянулся вредоносный npm/bun-пакет (`atomic-lockfile` / `lockfile-js`, во 2-й волне — `js-digest`). Тот запускал **Rust-инфостилер** (ELF `deps`) и **eBPF-руткит** (`scales.bpf.c`). Затронуто **400 → 900 → 1500+** пакетов в нескольких волнах. Sonatype: `Sonatype-2026-003775`, CVSS **8.7**. 15.06.2026 AUR **отключил регистрацию новых аккаунтов**.
> **Вывод: AUR — это User Repository, а не Trusted Repository.** Любой `PKGBUILD` исполняет НЕдоверенный код у тебя на машине.

> [!warning] Тебе это прямо актуально
> Ты собираешься переходить на **Arch и пользоваться `yay`/`paru`** — а это и есть AUR. Эта заметка не «новость ради новости», а **чек-лист гигиены AUR** (ниже раздел «Как защититься»). [Платформы владельца](../../Linux/Package-Manager/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2.md).

## 🧬 Как работала атака

1. **Поиск заброшенного.** Атакующий находит **orphaned-пакет** (мейнтейнер бросил) и через штатную процедуру AUR **подаёт заявку на усыновление** — система отдаёт пакет без какой-либо криптографической «преемственности» (новый мейнтейнер ничем не связан с прежним). Плюс — **подделка коммитов** под легитимного `arojas`.
2. **Внедрение.** Правятся `PKGBUILD` и **`.install` / `.hook`** скрипты: туда дописывается `npm install atomic-lockfile` (или `lockfile-js`; во 2-й волне `bun install js-digest`).
3. **Срабатывание.** AUR-хелпер (`yay`/`paru`) собирает пакет, затем ставит его через `pacman`. **`.install`-хуки `pacman` исполняет от root** при установке → вредонос тянет и запускает полезную нагрузку с привилегиями.

> [!note] Почему это так опасно именно в AUR
> В AUR **нет централизованной проверки безопасности**: `PKGBUILD` — это просто bash-скрипт, который выполняется при сборке/установке. Модель «доверяй мейнтейнеру» ломается, как только пакет меняет владельца. Заброшенные пакеты как вектор были **предсказуемой** дырой.

## ☠️ Полезная нагрузка

| Компонент | Что делает |
| :--- | :--- |
| **Rust-инфостилер** (ELF `deps`) | крадёт: пароли/куки браузеров, данные Electron-приложений (**Slack, Teams, Discord**), **GitHub-токены**, npm, **HashiCorp Vault**, **Docker**, **SSH-ключи**, **VPN-данные**, историю shell и прочие локальные секреты → эксфильтрация |
| **eBPF-руткит** (`scales.bpf.c`, libbpf) | прячет PID'ы, имена процессов и socket inode от `ps`, `ss`, `netstat`, `/proc`, netlink-диагностики — то есть **маскирует своё присутствие** |

## 🌊 Волны, масштаб, ответ

- **1-я волна** (11.06.2026, нашёл Sonatype / Eyad Hasan): `npm`-цепочка `atomic-lockfile`/`lockfile-js`.
- **2-я волна** (~12–14.06): перешли на **Bun** (`bun install js-digest`) и **обфускацию** (склейка строк в post-install хуках), чтобы обойти простые сигнатурные сканеры. Phoronix: сложнее первой.
- **Масштаб:** оценки росли **400 → 900 → 1500+** пакетов.
- **Ответ:** 15.06.2026 мейнтейнеры AUR **отключили регистрацию новых аккаунтов**; сообщество сканирует git-зеркало AUR.

## 🛡️ Как защититься (чек-лист AUR)

> [!tip] Главное правило: всегда читай PKGBUILD и .install ПЕРЕД сборкой
> AUR-хелпер по умолчанию показывает дифф/файлы — **не проматывай их вслепую**.

- **Включи обязательный просмотр** в хелпере:
  - `paru`: в `/etc/paru.conf` — опции `Review` (или ставь с `paru --review`); смотри **diff** перед сборкой.
  - `yay`: `yay -S --editmenu --diffmenu=true <pkg>` (или `yay --save --editmenu`), чтобы перед сборкой открывались `PKGBUILD`/`.install`.
- **Что искать в `PKGBUILD`/`.install`:** строки `npm install` / `bun install` / `curl … | sh` / `wget … | bash`, странные зависимости, обфускацию (склейка строк, base64, `eval`), скачивание ELF, подозрительные `source=()`/`sha`-несоответствия.
- **Минимизируй AUR:** бери из **официальных репозиториев** (`pacman -S`) всё, что там есть; AUR — только когда реально нужно и от живого мейнтейнера.
- **Проверяй «здоровье» пакета:** дата последнего обновления, votes, **не orphaned ли**, кто текущий мейнтейнер, история коммитов AUR-git.
- **Не запускай `yay`/`paru` под root** и не добавляй им бездумного `sudo`-доверия; собирай в непривилегированном пользователе.
- **Детект-инструменты:** [lenucksi/aur-malware-check](https://github.com/lenucksi/aur-malware-check) — community-скрипты под эту кампанию.

## 🧯 Если ставил/обновлял AUR-пакеты 11–15 июня 2026

> [!danger] Считай секреты скомпрометированными
> Инфостилер метит ровно в то, что у тебя ценно: **SSH-ключи, GitHub-токены, VPN-данные, пароли браузера**.
> 1. **Найди следы** (IOC): пакеты/зависимости `atomic-lockfile`, `lockfile-js`, `js-digest`; ELF с именем `deps`; `npm/bun install` в `.install`/`.hook`; прогони [aur-malware-check](https://github.com/lenucksi/aur-malware-check).
> 2. **Руткит маскируется** — обычным `ps`/`ss` можно ничего не увидеть; проверяй с offline/живого носителя, смотри загруженные **eBPF-программы** (`bpftool prog list`).
> 3. **Ротация всего:** перевыпусти **SSH-ключи**, отзови **GitHub/npm/Vault/Docker-токены**, смени пароли (особенно браузерные/VPN), проверь сессии Slack/Discord/Teams.
> 4. При сомнениях в чистоте — **переустановка системы** надёжнее, чем «вычистить руткит».

## 🖥️ А другие дистрибутивы?

Сам инцидент — **только AUR/Arch**. Но урок общий: любой **пользовательский репозиторий со сборкой из исходников исполняет недоверенный код**.

| Система | Аналог риска |
| :--- | :--- |
| **Gentoo** | сторонние **оверлеи** (`eselect repository`) — `ebuild` это тоже скрипт;官 main tree модерируется, оверлеи — нет |
| **Debian / Ubuntu** | сторонние **PPA** и `curl \| bash`-инсталляторы вне репозиториев Debian |
| **Entware / RT-AX56U** | `opkg` тянет из своего фида; кастомные/сторонние фиды — на свой риск |

Официальные репозитории (`pacman -S`, Portage main tree, Debian main, базовый Entware) проходят модерацию — приоритет им; «пользовательские» источники — только осознанно и с просмотром.

## 🔗 Ссылки

- Разбор Sonatype: [Atomic Arch — npm campaign](https://www.sonatype.com/blog/atomic-arch-npm-campaign-adds-malicious-dependency) · [The Hacker News](https://thehackernews.com/2026/06/over-400-arch-linux-aur-packages.html) · [Phoronix](https://www.phoronix.com/news/Arch-Linux-AUR-400-Compromised)
- Детект: [github.com/lenucksi/aur-malware-check](https://github.com/lenucksi/aur-malware-check)
- Источник новости: [@Mr0x45xploit](https://t.me/IzHmfluzM81OTAy/583)
- Связанные: [CVE-2026-55200 — libssh2 (кража через SSH-стек)](CVE/CVE-2026-55200%20%E2%80%94%20libssh2%20pre-auth%20OOB-write%20%28%D0%A2%D0%BE%D0%BA%D1%81%D0%B8%D1%87%D0%BD%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%BF%D0%BE%D0%B6%D0%B0%D1%82%D0%B8%D0%B5%29.md) · [Сравнение менеджеров пакетов](../../Linux/Package-Manager/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BA%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%D0%BE%D0%B2%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2.md)

#Безопасность #SupplyChain #Arch #AUR #Malware #eBPF
