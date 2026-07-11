---
создал заметку: 2026-07-11T00:10:00
author: WhiteK0T
tags:
  - Security
  - Docker
  - Containers
  - DevSecOps
  - Scanner
Источник:
  - https://t.me/open_source_friend/5761
  - https://github.com/cr0hn/dockerscan
---

# 🐳 DockerScan (cr0hn) — сканер безопасности Docker-образов (Go)

[**DockerScan v2.0**](https://github.com/cr0hn/dockerscan) (**Daniel Garcia / cr0hn**, **Go 1.21+**, ~1.7k★, актив­но пилится) — сканер безопасности Docker-образов и конфигураций: проверка по **CIS Benchmark**, поиск **захардкоженных секретов**, обнаружение известных **CVE** и небезопасных настроек рантайма. Пост подал это обобщённо («выявляет уязвимости в реальном времени, комплексная защита»), но пара важных уточнений ниже — включая **мутную лицензию**.

## 🔬 Что это на самом деле

- **Статический сканер образов/конфигов**, а не «защита в реальном времени». Он **анализирует Docker-образ/настройки** и выдаёт отчёт — это не рантайм-IDS и не «real-time protection», как звучит в посте. Место применения — **CI/CD и аудит образов** (есть интеграции GitHub Actions/GitLab, вывод в **SARIF**).
- **v2.0 — полностью переписан на Go** (v1.x был на **Python** и был скорее **наступательным** инструментом для Docker-реестров). Сейчас — один бинарь, быстрый, конкурентное сканирование.

## ✨ Что реально умеет (v2.0)

- **CIS Docker Benchmark v1.7.0** — 80+ автоматических проверок конфигурации.
- **Advanced Secrets Detection** — 40+ паттернов (ключи AWS/GCP/Azure, токены GitHub/GitLab, Docker registry) + **энтропия Шеннона** (>4.5) для неизвестных секретов.
- **CVE-сканирование** — конкретные Docker-CVE 2024-2025: `CVE-2024-21626` (побег из runc), BuildKit `CVE-2024-23651/23652/23653`, Docker Desktop RCE, `CVE-2025-9074` и др.
- **Runtime Security (конфиг)** — аудит опасных Linux-**capabilities** (`CAP_SYS_ADMIN` и т.п.), проверка **Seccomp**, **AppArmor/SELinux**.
- **Supply-Chain Detection** — эвристики на вредоносные образы/майнеры/бэкдоры (перекликается с [Atomic Arch](Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md)).
- **Реестры:** Docker Hub, GHCR, ECR, GCR, ACR, GitLab, self-hosted; аутентификация в приватные реестры.

> [!note] Наступательных функций сейчас нет
> «Троянизация образов», операции с реестром (push/pull/delete) и сетевое сканирование реестров — в README помечены **«coming soon в v2.1»**, т.е. в текущей v2.0 их **нет**. Старый Python-dockerscan этим славился; v2 пока чисто **оборонительный** сканер.

## ⚠️ Главный нюанс: лицензия неоднозначна

> [!caution] «open source» под вопросом — проверь LICENSE перед использованием
> README **сам себе противоречит**: вверху бейдж **`license-Proprietary`**, а ниже в тексте — *«Free & Open Source: BSD-3 license»*. GitHub при этом лицензию **не смог классифицировать** (`NOASSERTION`). Итого статус **непрозрачен**: возможно, часть проприетарна (например, коммерческие фичи/база CVE), часть под BSD-3. Для канала «open source friend» это важная оговорка — **прежде чем закладывать в пайплайн, открой файл `LICENSE`** и убедись в условиях (особенно для коммерческого использования).

> [!tip] Не единственный и не эталон
> Это **новый и не самый известный** сканер. Индустриальные стандарты — **Trivy** (Aqua), **Grype** (Anchore), **Docker Scout**, **Dockle**, **Hadolint** (линтер Dockerfile). DockerScan v2 интересен как «всё-в-одном» (CIS+секреты+CVE+рантайм) в одном Go-бинаре, но для критичных пайплайнов сверяйся с проверенными Trivy/Grype, а не полагайся на один инструмент.

## 🖥️ По системам

Go-бинарь под **Linux / macOS / Windows / FreeBSD** — ставится как один файл, зависимостей нет. Сканирует локальные образы (нужен доступ к Docker/сокету) и образы из реестров.

| Система | Применимость |
| :--- | :--- |
| **Gentoo** (основная) | ✅ Бинарь из релизов или `go install`; работает с локальным Docker/Podman и реестрами |
| **Debian / Ubuntu** | ✅ Бинарь; удобно вставить в CI (GitHub Actions/GitLab, SARIF-отчёт) |
| **Arch** (план с июня 2026) | ✅ Бинарь/`go install` |
| **Entware / RT-AX56U** | ⚠️ На роутере Docker обычно не крутится (armv7, 512 МБ) → сканировать нечего; держи DockerScan там, где реально собираешь/хостишь образы (десктоп/сервер/CI) |

## 🔗 Ссылки

- Репозиторий: [github.com/cr0hn/dockerscan](https://github.com/cr0hn/dockerscan) (⚠️ статус лицензии проверь в `LICENSE`) · автор: [cr0hn.com](https://cr0hn.com)
- Альтернативы: Trivy · Grype · Docker Scout · Dockle · Hadolint
- Источник новости: [@open_source_friend](https://t.me/open_source_friend/5761)
- Связанные: [Atomic Arch — supply-chain атака на AUR (infostealer + eBPF-руткит)](Atomic%20Arch%20%E2%80%94%20supply-chain%20%D0%B0%D1%82%D0%B0%D0%BA%D0%B0%20%D0%BD%D0%B0%20AUR%20%28infostealer%20%2B%20eBPF-%D1%80%D1%83%D1%82%D0%BA%D0%B8%D1%82%29.md)

#Security #Docker #Containers #DevSecOps #Scanner
