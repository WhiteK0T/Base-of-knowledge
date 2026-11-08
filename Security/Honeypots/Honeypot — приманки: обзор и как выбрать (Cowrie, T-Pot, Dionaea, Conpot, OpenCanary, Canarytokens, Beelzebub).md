---
создал заметку: 2026-11-08T22:00:00
author: WhiteK0T
tags:
  - Безопасность
  - Honeypot
  - Мониторинг
  - Обзор
Источник:
  - https://github.com/telekom-security/tpotce
  - https://github.com/cowrie/cowrie
  - https://canarytokens.org/
---

# 🍯 Honeypot — приманки: обзор и как выбрать

**Honeypot** — намеренно уязвимый на вид сервис, единственная цель которого — быть атакованным, чтобы вы собрали данные об атакующих: IP, перебираемые пароли, команды, загружаемый вредонос. У honeypot нет легитимных пользователей, поэтому **любое обращение к нему подозрительно** — это и делает приманку отличным ранним детектором. Заметка-обзор: что брать под разные задачи.

## 1. Виды приманок

| Признак | Варианты |
| :--- | :--- |
| По интерактивности | **low** (отвечает по сценарию, минимум риска), **medium** (эмулирует оболочку/протокол), **high** (за приманкой настоящая система — больше данных, выше риск) |
| По месту | **сервис-приманка** (ждёт подключений на периметре/в сегменте) и **токен-приманка** (файл, ссылка, ключ, который срабатывает, когда его открыл чужой) |
| По цели | SSH/Telnet, веб, промышленные протоколы (ICS/SCADA), сбор вредоноса, «всё сразу» |

Главный плюс токенов и low-interaction: минимальная поверхность атаки, почти нет риска «подставиться».

## 2. Что брать

| Инструмент | Для чего | Интерактивность | Статус |
| :--- | :--- | :--- | :--- |
| [Cowrie](Cowrie%20%E2%80%94%20SSH-Telnet%20honeypot%20%28%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B0%29%3A%20%D1%87%D1%82%D0%BE%20%D0%BB%D0%BE%D0%B3%D0%B8%D1%80%D1%83%D0%B5%D1%82%2C%20medium%20vs%20proxy%2C%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%B2%20Docker%2C%20%D0%BA%D0%B0%D0%BA%20%D0%BD%D0%B5%20%D0%BF%D0%BE%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%D1%81%D1%8F.md) | **SSH/Telnet**, лучший старт: ловит брут-форс и команды | medium (или proxy) | активен, ★~6,7k |
| [T-Pot](T-Pot%20%E2%80%94%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%B8%D0%B7%2020%2B%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BE%D0%BA%20%D0%B2%20Docker%20%D1%81%20%D0%B4%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D0%B0%D0%BC%D0%B8%20Elastic%20%28Deutsche%20Telekom%29.md) (Deutsche Telekom) | **всё в одном**: 20+ приманок в Docker (Cowrie, Dionaea, Conpot, Galah и др.) + дашборды Kibana/Elastic | разная | активен, ★~9,7k — эталон «платформы» |
| [OpenCanary](OpenCanary%20%E2%80%94%20%D0%BB%D1%91%D0%B3%D0%BA%D0%B8%D0%B5%20%D1%81%D0%B5%D1%82%D0%B5%D0%B2%D1%8B%D0%B5%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B8-%D0%BB%D0%BE%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20%D0%B4%D0%BB%D1%8F%20%D0%B2%D0%BD%D1%83%D1%82%D1%80%D0%B5%D0%BD%D0%BD%D0%B5%D0%B9%20%D1%81%D0%B5%D1%82%D0%B8%20%28Thinkst%29.md) (Thinkst) | **лёгкие tripwire-сервисы** (SSH, SMB, HTTP, RDP…): один сработавший логин = тревога, почти нулевой риск | low | активен, ★~3,1k |
| [Canarytokens](Canarytokens%20%E2%80%94%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D1%8B-%D0%BB%D0%BE%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20%28%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%2C%20URL%2C%20AWS-%D0%BA%D0%BB%D1%8E%D1%87%29%20%D0%B8%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%28Thinkst%29.md) (Thinkst) | **токены-ловушки**: документ Word/PDF, URL, AWS-ключ, QR — срабатывают при открытии; бесплатный хостинг или self-hosted | — (токен) | активен, ★~2,2k |
| [Dionaea](Dionaea%20%E2%80%94%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%B7%D0%B0%D1%85%D0%B2%D0%B0%D1%82%D0%B0%20%D0%B2%D1%80%D0%B5%D0%B4%D0%BE%D0%BD%D0%BE%D1%81%D0%B0%20%D0%BF%D0%BE%20SMB%2C%20FTP%2C%20MSSQL%20%D0%B8%20%D0%B4%D1%80.md) | **сбор вредоноса** по SMB, FTP, HTTP, MSSQL и др. | low/medium | обновляется редко, но стандарт для захвата малвари (входит в T-Pot) |
| [Conpot](Conpot%20%E2%80%94%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%BC%D1%8B%D1%88%D0%BB%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D1%81%D0%B5%D1%82%D0%B5%D0%B9%20%28ICS-SCADA%2C%20Modbus%2C%20S7comm%29.md) | **ICS/SCADA**: Modbus, S7comm, BACnet — приманка для промышленных сетей | low | активен, ★~1,5k |
| [Beelzebub](https://github.com/beelzebub-labs/beelzebub) | современный low-code фреймворк, умеет **LLM-ответы** в эмулируемой оболочке | low/medium | активен, ★~2,2k |
| [Galah](https://github.com/0x4D31/galah) | **веб-honeypot на LLM**: модель на лету генерирует правдоподобные ответы сервера | medium | активен, ★~0,7k |
| [qeeqbox/honeypots](https://github.com/qeeqbox/honeypots) | **30 протоколов одним пакетом** Python (DNS, FTP, HTTP, Elastic, SMB…) — быстро «накидать» сенсоров | low | активен |

Рядом, но не совсем honeypot: [endlessh](https://github.com/skeeto/endlessh) — SSH-tarpit: не собирает данные, а бесконечно медленно шлёт баннер, подвешивая ботов. Хорош как «наказание» для сканеров на ложном порту.

## 3. Как выбрать

- **Просто посмотреть, кто ломится по SSH** → [Cowrie](Cowrie%20%E2%80%94%20SSH-Telnet%20honeypot%20%28%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B0%29%3A%20%D1%87%D1%82%D0%BE%20%D0%BB%D0%BE%D0%B3%D0%B8%D1%80%D1%83%D0%B5%D1%82%2C%20medium%20vs%20proxy%2C%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%B2%20Docker%2C%20%D0%BA%D0%B0%D0%BA%20%D0%BD%D0%B5%20%D0%BF%D0%BE%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%D1%81%D1%8F.md) в Docker.
- **Красивые дашборды и картина атак на весь периметр** → T-Pot (нужна отдельная ВМ, 8+ ГБ RAM).
- **Раннее обнаружение внутри своей сети, минимум возни** → OpenCanary или Canarytokens: сработало — значит, кто-то уже внутри.
- **Промышленная сеть** → Conpot.
- **Поэкспериментировать с LLM-приманками** → Beelzebub, Galah.

## 4. Общие правила (чтобы не подставиться)

- **Изоляция.** Приманку намеренно атакуют, поэтому она должна стоять в сегменте, из которого **нельзя дойти до продакшена**, без реальных секретов на борту.
- **Меньше интерактивности — меньше риск.** Для раннего обнаружения достаточно low-interaction и токенов. High-interaction (настоящая система за прокси) — только с жёсткой изоляцией.
- **Загруженные образцы = вредонос**: не запускать, хранить и разбирать в песочнице.
- **Право.** Логировать атакующих на своей инфраструктуре законно; ответные атаки (hack-back) — нет.

## Связанные заметки

- [Cowrie — SSH/Telnet honeypot](Cowrie%20%E2%80%94%20SSH-Telnet%20honeypot%20%28%D0%BF%D1%80%D0%B8%D0%BC%D0%B0%D0%BD%D0%BA%D0%B0%29%3A%20%D1%87%D1%82%D0%BE%20%D0%BB%D0%BE%D0%B3%D0%B8%D1%80%D1%83%D0%B5%D1%82%2C%20medium%20vs%20proxy%2C%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%B2%20Docker%2C%20%D0%BA%D0%B0%D0%BA%20%D0%BD%D0%B5%20%D0%BF%D0%BE%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D1%8C%D1%81%D1%8F.md) — подробный разбор лучшего стартового варианта
- [Fail2ban — защита сервисов от перебора](../../Network/Fail2ban/Fail2ban%20%E2%80%94%20%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B0%20%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BE%D0%B2%20%D0%BE%D1%82%20%D0%BF%D0%B5%D1%80%D0%B5%D0%B1%D0%BE%D1%80%D0%B0%20%28SSH%2C%20journald%2C%20%D1%84%D0%B0%D0%B9%D1%80%D0%B2%D0%BE%D0%BB%2C%20%D0%B4%D0%B8%D0%B0%D0%B3%D0%BD%D0%BE%D1%81%D1%82%D0%B8%D0%BA%D0%B0%29.md) — не приманка, а блокировка перебора по логам

## 🔗 Ссылки

- T-Pot: https://github.com/telekom-security/tpotce
- Cowrie: https://github.com/cowrie/cowrie
- OpenCanary: https://github.com/thinkst/opencanary
- Canarytokens: https://canarytokens.org/
- Dionaea: https://github.com/DinoTools/dionaea
- Conpot: https://github.com/mushorg/conpot
- Beelzebub: https://github.com/beelzebub-labs/beelzebub
- Galah: https://github.com/0x4D31/galah

#Безопасность #Honeypot #Мониторинг #Обзор
