---
создал заметку: 2026-09-14T22:10:00
author: WhiteK0T
tags:
  - AnyDesk
  - RemoteAccess
  - Proprietary
  - Privacy
  - Инструменты
Источник:
  - https://anydesk.com/
  - https://deb.anydesk.com/
---

# 🟥 AnyDesk — проприетарный удалённый доступ

**AnyDesk** ([anydesk.com](https://anydesk.com/), AnyDesk Software GmbH, Германия) — популярный кроссплатформенный инструмент удалённого доступа. Ключевая фишка — собственный кодек **DeskRT**: очень низкая задержка и малый трафик даже на слабом канале. **Закрытый исходник, freemium**: бесплатно для личного некоммерческого использования, платные тарифы (Solo/Standard/Advanced) для работы и команд. Клиент — Windows/macOS/Linux/Android/iOS/FreeBSD/Raspberry Pi.

> [!warning] Главное отличие от [RustDesk](RustDesk%20%E2%80%94%20self-hosted%20%D1%83%D0%B4%D0%B0%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%20%28%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%2B%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20hbbs-hbbr%2C%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%BD%D0%B0%20Gentoo-Debian-Arch-Entware%29.md)
> - **Закрытый код** — нельзя проверить, что происходит с трафиком/сессией; доверие к вендору.
> - **Свой сервер только в Enterprise.** Есть **AnyDesk On-Premises** (аплайнс — своя VM с собственным namespace/relay), но это **платный Enterprise**, а не бесплатный self-host. По умолчанию соединения идут через **облако AnyDesk**.
> - **Детект коммерческого использования.** На бесплатном тарифе AnyDesk эвристиками ловит «похоже на работу» и начинает **ограничивать/навязывать** покупку лицензии — для регулярной работы free-тариф ненадёжен.
> - **Вендор может менять ToS/доступность** (гео-ограничения, блокировки аккаунтов) — у закрытого облачного сервиса это вне твоего контроля. Сверяйся с актуальными условиями.

## 🔒 Как устроено (кратко)

- **ID-based:** каждому клиенту выдаётся числовой AnyDesk-адрес; подключаешься по нему, подтверждаешь на удалённой стороне **или** ставишь **unattended-пароль** (неконтролируемый доступ).
- **Шифрование:** TLS 1.2+, обмен ключами RSA-2048, перебор сессии — end-to-end по заявлению вендора (проверить нельзя — код закрыт).
- **Демон + GUI:** на Linux работает системная служба `anydesk` (`anydesk.service`) + графический клиент; для полноценного управления нужен **desktop environment**.
- **P2P или через облако AnyDesk** — прямой коннект, иначе ретрансляция через инфраструктуру вендора.

## 🖥️ Установка на системах владельца

Это GUI-приложение (закрытый бинарь) — ставится из вендорского репозитория/пакета, **без сборки из исходников**:

### Debian / Ubuntu (официальный репозиторий)
```bash
curl -fsSL https://keys.anydesk.com/repos/DEB-GPG-KEY | sudo gpg --dearmor -o /etc/apt/keyrings/anydesk.gpg
echo "deb [signed-by=/etc/apt/keyrings/anydesk.gpg] http://deb.anydesk.com/ all main" | sudo tee /etc/apt/sources.list.d/anydesk.list
sudo apt update && sudo apt install anydesk
```

### Arch (AUR)
```bash
yay -S anydesk-bin      # или paru -S anydesk-bin
# служба:
sudo systemctl enable --now anydesk
```

### Gentoo (основная) — нет в Portage
Официального `net-misc/anydesk` в дереве **нет**. Варианты:
- ebuild из **GURU/стороннего оверлея** (проверь `eselect repository`), затем `emerge anydesk`;
- вручную — **бинарный tarball** с [anydesk.com/downloads](https://anydesk.com/en/downloads/linux) (generic Linux `.tar.gz`), распаковать и запускать `./anydesk`; демон — обернуть в **OpenRC**-скрипт (см. пример для hbbs в заметке RustDesk).
> [!note] Зависимости
> Generic-бинарь тянет системные GTK/glib, `libgtkglext`, X11-библиотеки. На чистом Wayland бывают нюансы с захватом экрана — держи Xwayland/поддержку PipeWire.

### Entware / ASUS RT-AX56U
➖ **Неприменимо:** AnyDesk — это GUI-клиент с захватом экрана, а роутер без десктопа/дисплея. Своего relay для self-host тоже не поставить (On-Premises — тяжёлый Enterprise-аплайнс). Роутер тут ни при чём.

## 🛡️ Приватность и право

- **Доверие вендору:** закрытый код + облачная маршрутизация по умолчанию = твои сессии проходят через чужую инфраструктуру. Для чувствительного доступа предпочтительнее self-hosted **RustDesk**.
- **Unattended-пароль** храни надёжно и включай список доверенных — иначе постоянный доступ к машине утечёт вместе с паролем.
- **Легально:** свои машины, помощь с согласия пользователя. Для регулярной работы — покупай лицензию (иначе детект коммерции). Фишинг «техподдержки» через AnyDesk — распространённое мошенничество: не давай доступ незнакомцам «из банка».

## 🔗 Связанные заметки

- Открытая self-hosted альтернатива (свой сервер, исходники): [RustDesk](RustDesk%20%E2%80%94%20self-hosted%20%D1%83%D0%B4%D0%B0%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%20%28%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%2B%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20hbbs-hbbr%2C%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%BD%D0%B0%20Gentoo-Debian-Arch-Entware%29.md)
- Ещё один remote-access (для сравнения тарифов/подхода): [ScreenConnect](ScreenConnect.md)

## 🔗 Ссылки

- Сайт/загрузки: [anydesk.com/downloads/linux](https://anydesk.com/en/downloads/linux) · репозиторий пакетов: [deb.anydesk.com](https://deb.anydesk.com/)
- On-Premises (Enterprise): [anydesk.com/en/on-premises](https://anydesk.com/en/on-premises)

#AnyDesk #RemoteAccess #Proprietary #Privacy #Инструменты
