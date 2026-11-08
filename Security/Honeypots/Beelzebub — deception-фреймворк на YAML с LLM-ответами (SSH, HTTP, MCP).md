---
создал заметку: 2026-11-09T12:25:00
author: WhiteK0T
tags:
  - Безопасность
  - Honeypot
  - Мониторинг
  - LLM
  - Go
Источник:
  - https://github.com/beelzebub-labs/beelzebub
  - https://docs.beelzebub.ai
---

# 🍯 Beelzebub — deception-фреймворк на YAML с LLM

[**Beelzebub**](https://github.com/beelzebub-labs/beelzebub) — современный low-code фреймворк приманок: вы описываете ложные сервисы и правила ответов в **YAML**, а при желании подключаете **LLM**, чтобы приманка динамически отвечала атакующему и удерживала сессию дольше, чем позволяет фиксированный набор заготовок. Написан на Go, разворачивается как бинарник, Docker Compose или в Kubernetes.

| | |
| :--- | :--- |
| Что это | deception-фреймворк, конфигурация на YAML |
| Язык/лицензия | Go, GPL-3.0; ~2,2 тыс. звёзд, активен |
| Версия | v3.10.0 (октябрь 2026) |
| Протоколы | SSH, HTTP, TCP, TELNET, **MCP** |

## Чем интересен

- **Статические или LLM-ответы.** Простые сценарии — заготовками; сложные — моделью (нужен настроенный провайдер). Есть 18 примеров конфигов (SSH, WordPress, MySQL, Redis, SMB, LDAP, MQTT и др.).
- **Приманки для ИИ-агентов (MCP).** Умеет выставлять ложные MCP-инструменты — «наживку», по обращению к которой видно попытки prompt-injection при тестировании агентов. Это не гарантия детекта, но фиксация подозрительных вызовов.
- **Интеграция.** Логи локально, события в RabbitMQ, метрики Prometheus (`core.prometheus.enabled: true`, по умолчанию выключено).

## Установка по платформам

| Система | Как ставить |
| :--- | :--- |
| Debian / Ubuntu | `./install.sh --docker` (нужен Docker Engine + Compose v2) |
| Gentoo | `go build` из исходников (`dev-lang/go`) или Docker |
| Arch | `sudo pacman -S go` и сборка бинарника, либо Docker |
| Entware | не рекомендуется: LLM-ответы и набор сервисов тяжелы для роутера |

```bash
git clone https://github.com/beelzebub-labs/beelzebub.git
cd beelzebub && ./install.sh --docker
curl -i http://localhost:8080/      # приманка ответит 401 Unauthorized
```

## Чтобы не подставиться

- Установщик поднимает **пачку сервисов, включая привилегированные порты**, и на Linux может включить host-networking (изоляции сети в этом режиме нет) — только на изолированном лабораторном хосте.
- Использовать синтетические учётки, не класть реальные секреты; перед выставлением наружу прочитать production-safety из документации.
- **Go-плагины исполняются в процессе приманки** — ставить только доверенные и с фиксированной версией.
- При LLM-ответах выставить лимиты на API провайдера (защита от «Denial of Wallet»).

## Связанные заметки

- [Honeypot — приманки: обзор и как выбрать](Honeypot%20%E2%80%94%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B8%3A%20%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%20%D0%B8%20%D0%BA%D0%B0%D0%BA%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C%20%28Cowrie%2C%20T-Pot%2C%20Dionaea%2C%20Conpot%2C%20OpenCanary%2C%20Canarytokens%2C%20Beelzebub%29.md) — Beelzebub среди LLM-приманок
- [Galah — веб-приманка на LLM](Galah%20%E2%80%94%20%D0%B2%D0%B5%D0%B1-%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B0%20%D0%BD%D0%B0%20LLM%2C%20%D0%BE%D1%82%D0%B2%D0%B5%D1%87%D0%B0%D0%B5%D1%82%20%D0%BD%D0%B0%20%D0%BB%D1%8E%D0%B1%D0%BE%D0%B9%20HTTP-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81.md) — похожая идея, но только для веба

## 🔗 Ссылки

- GitHub: https://github.com/beelzebub-labs/beelzebub
- Документация: https://docs.beelzebub.ai

#Безопасность #Honeypot #Мониторинг #LLM #Go
