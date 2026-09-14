---
создал заметку: 2026-09-14T22:30:00
author: WhiteK0T
tags:
  - TeamViewer
  - RemoteAccess
  - Proprietary
  - Privacy
  - Инструменты
Источник:
  - https://www.teamviewer.com/
  - https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-remote/download-and-installation/linux/
---

# 🔵 TeamViewer — проприетарный удалённый доступ

**TeamViewer** ([teamviewer.com](https://www.teamviewer.com/), TeamViewer SE, Германия) — ветеран рынка удалённого доступа с огромной базой пользователей. Кроссплатформенный (Windows/macOS/Linux/Android/iOS/ChromeOS), текущая линейка **v15.x** (TeamViewer Remote / «Classic»). **Закрытый исходник, freemium**: бесплатно только для **личного некоммерческого** использования; платные тарифы для работы и команд. Соединение — по числовому **ID + паролю** (разовый или unattended), через облако TeamViewer или P2P.

> [!warning] Ключевые нюансы (важнее, чем в рекламе)
> - **Агрессивный детект коммерческого использования** — самый жёсткий на рынке. Если TeamViewer заподозрит «работу» (частые подключения, разные ID, домены), бесплатные сессии **обрезаются до нескольких секунд** и всплывает «commercial use suspected». Для регулярной работы free-тариф практически неюзабелен → нужна лицензия.
> - **Закрытый код + облачная маршрутизация** по умолчанию: доверие вендору, сессии идут через его инфраструктуру. Свой сервер — только платный **On-Premises / TeamViewer Tensor** (Enterprise-аплайнс), не для рядового пользователя.
> - **История безопасности:** в 2016 массовые компрометации аккаунтов (credential stuffing) → обязательно **2FA** и уникальный пароль, включай allowlist доверенных устройств.
> - **Вендор может ограничивать доступ** по гео/санкциям и банить аккаунты — вне твоего контроля (закрытый облачный сервис). Сверяйся с актуальными ToS.

## 🖥️ Установка на системах владельца

Закрытый GUI-бинарь + фоновый демон **`teamviewerd`**; **без сборки из исходников**:

### Debian / Ubuntu
```bash
# скачать .deb с сайта (full-клиент ИЛИ host — вместе не ставятся!)
sudo apt install ./teamviewer_15.x.xxxxx_amd64.deb
# демон:
sudo systemctl enable --now teamviewerd
```
> **`teamviewer` vs `teamviewer-host`:** полноценный клиент и «host» (только приём подключений, для unattended-серверов) **несовместимы бок о бок** — host ставится вместо full. Есть и официальный apt-репозиторий TeamViewer для автообновлений.

### Arch (AUR)
```bash
yay -S teamviewer          # или git clone https://aur.archlinux.org/teamviewer.git && makepkg -si
sudo systemctl enable --now teamviewerd
```

### Gentoo (основная) — нет в Portage
Официального `net-misc/teamviewer` в дереве **нет**. Варианты:
- ebuild из **стороннего/GURU-оверлея** → `emerge teamviewer`;
- вручную из **generic Linux tarball** (`teamviewer_*.tar.xz`) с сайта: распаковать, запустить `./tv-setup checklibs`, а `teamviewerd` обернуть в **OpenRC**-скрипт (аналог примера hbbs из заметки RustDesk — `command=/opt/teamviewer/tv_bin/teamviewerd`, `command_args="-f"`).
> [!note] Демон обязателен
> Без запущенного `teamviewerd` клиент не соединится. На Gentoo проверь автозапуск через `rc-update add teamviewerd default`.

### Entware / ASUS RT-AX56U
➖ **Неприменимо:** TeamViewer — GUI-клиент с захватом экрана, роутер без десктопа не подходит. Свой сервер тоже не поднять (On-Premises — тяжёлый Enterprise). Роутер ни при чём.

## 🛡️ Приватность и право

- **Доверие вендору:** закрытый код, облако по умолчанию. Для чувствительных сессий предпочтительнее self-hosted [RustDesk](RustDesk%20%E2%80%94%20self-hosted%20%D1%83%D0%B4%D0%B0%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%20%28%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%2B%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20hbbs-hbbr%2C%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%BD%D0%B0%20Gentoo-Debian-Arch-Entware%29.md).
- **2FA + уникальный пароль** обязательны (см. инцидент 2016). Unattended-пароль храни надёжно.
- **Фишинг «техподдержки»** через TeamViewer — классика мошенничества: никогда не давай ID/пароль незнакомцам «из банка/Microsoft».
- **Легально:** свои машины и помощь с согласия пользователя; для работы — покупка лицензии (иначе детект коммерции всё равно заблокирует).

## 🔗 Связанные заметки

- Открытая self-hosted альтернатива (свой сервер, исходники, без детекта коммерции): [RustDesk](RustDesk%20%E2%80%94%20self-hosted%20%D1%83%D0%B4%D0%B0%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%20%28%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%20%2B%20%D1%81%D0%B2%D0%BE%D0%B9%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20hbbs-hbbr%2C%20%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%20%D0%BD%D0%B0%20Gentoo-Debian-Arch-Entware%29.md)
- Второй проприетарный вариант (кодек DeskRT, чуть мягче детект): [AnyDesk](AnyDesk%20%E2%80%94%20%D0%BF%D1%80%D0%BE%D0%BF%D1%80%D0%B8%D0%B5%D1%82%D0%B0%D1%80%D0%BD%D1%8B%D0%B9%20%D1%83%D0%B4%D0%B0%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%20%28%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo-Debian-Arch%2C%20on-premises%20%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20Enterprise%29%2C%20%D0%BD%D1%8E%D0%B0%D0%BD%D1%81%D1%8B%20%D0%B8%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B0%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C.md)
- Ещё один remote-access: [ScreenConnect](ScreenConnect.md)

## 🔗 Ссылки

- Загрузки Linux: [teamviewer.com — Linux](https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-remote/download-and-installation/linux/) · AUR: [aur.archlinux.org/packages/teamviewer](https://aur.archlinux.org/packages/teamviewer)
- Enterprise self-host: **TeamViewer Tensor / On-Premises**

#TeamViewer #RemoteAccess #Proprietary #Privacy #Инструменты
