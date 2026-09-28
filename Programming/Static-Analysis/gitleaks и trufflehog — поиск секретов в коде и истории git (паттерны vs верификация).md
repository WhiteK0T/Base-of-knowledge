---
создал заметку: 2026-09-28T17:05:00
author: WhiteK0T
tags:
  - Programming
  - Static-Analysis
  - Secrets
  - Git
  - Security
  - gitleaks
  - trufflehog
Источник:
  - https://github.com/gitleaks/gitleaks
  - https://github.com/trufflesecurity/trufflehog
---

# 🔑 gitleaks и trufflehog — поиск секретов в коде и истории git

Отдельный класс из [терминологии домена](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md) — **secret-scanning**: не «уязвимость кода», а утёкший ключ/токен/пароль. Важно: искать надо **по всей истории git**, а не только в текущем коммите — секрет, удалённый следующим коммитом, остаётся в истории навсегда.

| Инструмент | ★ | Лицензия | Подход |
| :--- | :---: | :--- | :--- |
| **[gitleaks](https://github.com/gitleaks/gitleaks)** | ~29.5k | MIT | **паттерны + энтропия**: быстрый скан по regex-правилам и «случайности» строк |
| **[trufflehog](https://github.com/trufflesecurity/trufflehog)** (trufflesecurity) | ~28k | **AGPL-3.0** | **верификация**: найденный ключ **проверяется на живом сервисе** — работает ли он ещё |

---

## 🔎 Ключевое различие: паттерн vs проверка «вживую»

- **gitleaks** — быстрый регэксп/энтропийный скан. Много находок, но и ложных: «похоже на ключ» ≠ «ключ рабочий».
  ```bash
  gitleaks detect --source . -v          # скан рабочего дерева + история git
  gitleaks protect --staged              # pre-commit: блокировать до коммита
  gitleaks detect --report-format sarif -r out.sarif
  ```
- **trufflehog** — 800+ детекторов и главная фишка: **верификация** — берёт найденный AWS/GitHub/Slack-токен и **дёргает API**, проверяя, действителен ли он. Резко снижает шум и сразу показывает **реально опасные** утечки.
  ```bash
  trufflehog git file://. --only-verified   # только подтверждённые живые секреты
  trufflehog github --org=myorg --only-verified
  ```

**Практика:** gitleaks — в pre-commit/CI как быстрый барьер; trufflehog — для приоритизации (что из найденного действительно живое и требует ротации). Дополняют друг друга.

> [!caution] AGPL у trufflehog
> Лицензия trufflehog — **AGPL-3.0**: для встраивания в свой продукт/сервис имеет значение (обязательства AGPL). Для локального запуска и CI — не проблема. gitleaks (MIT) в этом плане свободнее.

---

## 🖥️ На системах владельца

Оба — **Go-бинарники**, ставятся легко:

| Система | Как |
| :--- | :--- |
| **Gentoo** (основная) | релизные бинарники/`go install`; gitleaks бывает в оверлеях |
| **Debian / Ubuntu** | бинарники из релизов; или `go install` |
| **Arch** | `pacman -S gitleaks` / AUR `trufflehog` |
| **Entware / RT-AX56U** | ⚠️ есть arm-релизы, но сканировать репозитории удобнее на ПК/в CI |

> [!tip] Для этого хранилища
> Полезно прогнать gitleaks по vault перед публикацией. Учитывать: папка `Network/Tunnels/**` под **git-crypt** — сканер увидит там **шифртекст**, а не секреты (это ожидаемо). Проверять стоит именно, что чувствительное **не попало мимо** git-crypt в открытом виде.

---

## 📍 О размещении заметки

Secret-scanning — пограничный класс: инструменты про **git-историю** (ближе к `VCS/`) и про **безопасность** (`Security/`). Пока положил в `Static-Analysis/` для целостности домена и связи с [обзорной заметкой](SAST%20vs%20DAST%20vs%20SCA%20vs%20secret-scanning%20%E2%80%94%20%D1%87%D1%82%D0%BE%20%D0%B5%D1%81%D1%82%D1%8C%20%D1%87%D1%82%D0%BE%20%28%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29.md). При желании легко перенести в `VCS/` или `Security/`.

## 🔗 Ссылки

- [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) · [trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog)

#Programming #Static-Analysis #Secrets #Git #Security #gitleaks #trufflehog
