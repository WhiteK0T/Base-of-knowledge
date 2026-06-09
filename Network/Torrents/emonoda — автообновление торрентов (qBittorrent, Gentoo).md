---
создал заметку: 2026-06-09T16:00:00
author: WhiteK0T
tags:
  - emonoda
  - Torrents
  - qBittorrent
  - Gentoo
  - Automation
  - Linux
Источник:
  - https://github.com/mdevaev/emonoda
  - https://mdevaev.github.io/emonoda/
---

# 🔄 emonoda — автообновление торрентов (qBittorrent, Gentoo)

[**emonoda**](https://github.com/mdevaev/emonoda) — набор консольных утилит в духе UNIX для управления коллекцией торрентов. Главная задача — **автоматически обновлять торрент-файлы прямо с трекеров**: когда раздача перезалита (новая серия, новый рип, исправленные файлы), emonoda сам скачивает свежий `.torrent`, подменяет его в клиенте и докачивает только изменённое — **в ту же папку, где лежали старые данные**.

Поддерживает трекеры: **rutracker.org**, nnm-club.me, rutor.info, tfile.cc, pravtor.ru, tr.anidub.com, pornolab.net, booktracker.org, trec.to. Клиенты: rtorrent, ktorrent, transmission и **qBittorrent**.

> [!info] Под какую конфигурацию написан гайд
> - ОС: **Gentoo**
> - Клиент: **qBittorrent** (с включённым WebUI)
> - Хранилище `.torrent`-файлов: **`/mnt/dat1T/Torrents/`**
> - Сами данные раздач разбросаны по **`/mnt/dat1T/`**, который используется **не только под торренты** (это важно для `emfind` — см. ниже).

## 🧰 Утилиты пакета

| Команда | Назначение |
| :--- | :--- |
| **emupdate** | Главная: проверяет раздачи на трекерах и обновляет `.torrent`-файлы + подменяет их в клиенте |
| **emload** | Добавить торрент в клиент с раскладкой данных по «ссылочной» схеме (symlink) |
| **emrm** | Удалить торрент(ы) из клиента |
| **emfind** | Сервисные запросы по коллекции: `orphans`, `not-in-client`, `missing-torrents`, `duplicate-torrents` |
| **emfile** | Показать метаданные `.torrent` (человеко- или скрипто-читаемо) |
| **emdiff** | Diff между двумя `.torrent`-файлами |
| **emconfetti-demo / -tghi** | Тест уведомлений / помощник настройки Telegram-бота |

## 🧭 Как это ложится на твою схему

```
            ┌─────────────────────────────┐
            │  /mnt/dat1T/Torrents/*.torrent  │  ← каноническое хранилище .torrent
            └──────────────┬──────────────┘
                           │  emupdate сканирует эту папку
                           ▼
   трекер (rutracker и т.п.) ──проверка обновления──► качает новый .torrent
                           │  (старый → в backup_dir)
                           ▼
            qBittorrent WebUI (http://localhost:8080)
                           │  снять старый торрент (данные сохранить),
                           │  добавить новый на ТОТ ЖЕ save path
                           ▼
        данные раздачи где-то в /mnt/dat1T/...  ← путь берётся из клиента,
                                                   emupdate его НЕ задаёт сам
```

Ключевая мысль: **`emupdate` берёт путь к данным из самого qBittorrent** (save path каждого торрента). Поэтому ему **не нужно** знать, где именно на `/mnt/dat1T/` лежит контент, и его не смущает, что диск используется ещё и под другое. Достаточно, чтобы `.torrent` лежал в `torrents_dir` **и** был загружен в qBittorrent.

## 🛠️ Установка

emonoda — Python-пакет из PyPI (собирает Cython-расширение, нужен **Python 3.6+** и компилятор C). В дистрибутивных репозиториях его обычно нет. Запускать его логично на **полноценной машине** (Gentoo/Debian/Arch), где лежит `torrents_dir` и откуда виден WebUI клиента, — **не на роутере** (см. Entware ниже).

Самый переносимый способ на любой системе (и без проблем с PEP 668) — **pipx**: изолированное окружение, команды кладутся в `~/.local/bin`.

```bash
pipx install emonoda
pipx upgrade emonoda    # обновление
```

Дальше — как поставить сам pipx и зависимости сборки на каждой системе.

### Gentoo

```bash
sudo emerge -an dev-python/pipx     # компилятор в системе уже есть
pipx install emonoda
```

Без pipx — вручную в venv (системный pip помечен *externally-managed*, PEP 668 → не `pip install --user`):

```bash
python3 -m venv ~/emonoda-venv
~/emonoda-venv/bin/pip install --upgrade pip emonoda
ln -sf ~/emonoda-venv/bin/em* ~/.local/bin/   # прокинуть команды в PATH
```

### Debian / Ubuntu

```bash
sudo apt install pipx python3-venv build-essential
pipx install emonoda
```

`build-essential` нужен для сборки Cython-расширения; на свежих Debian/Ubuntu системный pip тоже *externally-managed* → ставим через pipx/venv.

### Arch

Нативно — из **AUR**: пакет `emonoda` ведёт **сам автор проекта** (`mdevaev`), пакет актуальный.

```bash
yay -S emonoda      # или paru -S emonoda
```

Альтернатива (без AUR-хелпера) — тот же pipx:

```bash
sudo pacman -S python-pipx base-devel
pipx install emonoda
```

### Entware (роутер) — не нужно

> [!note] emonoda на роутере смысла не имеет
> В Entware есть `python3`/`python3-pip`, но emonoda собирает Cython-расширение (нужны gcc и заголовки — на роутере тяжело и не предусмотрено) и должен видеть и `torrents_dir`, и клиент. Правильно: держать emonoda на **полноценной машине** и натравливать его на нужный клиент по сети — в том числе на `transmission`, крутящийся на роутере, если раздачи там. Сам роутер ради emonoda трогать не надо.

### Проверка

```bash
emupdate --help
emfile /mnt/dat1T/Torrents/любой.torrent   # покажет метаданные
```

## ⚙️ Подготовка qBittorrent

1. **Включить WebUI:** *Настройки → Веб-интерфейс* → поставить галку, задать порт (по умолчанию **8080**), логин и пароль.
   - Если qBittorrent и emonoda на одной машине, удобно включить **«Обходить аутентификацию для клиентов на localhost»** — тогда `user`/`passwd` в конфиге можно оставить пустыми.
2. **Авто-складывание `.torrent` в хранилище:** *Настройки → Загрузки → «Сохранять копию .torrent файлов в:»* → указать **`/mnt/dat1T/Torrents/`**. Тогда каждый добавленный торрент **сам** попадает в каноническую папку, и `emupdate` его подхватит без ручного копирования.

> [!warning] qBittorrent не хранит «кастомы»
> Плагин qBittorrent в emonoda **не поддерживает custom-поля**. Это значит, что при обновлении торрента emonoda **не переносит автоматически категорию/метку (label)** на новый торрент — после апдейта может понадобиться вручную вернуть категорию. Опции `save_customs`/`set_customs` для qBittorrent неактуальны (работают у rtorrent/ktorrent).

## 📄 Рабочий конфиг (`~/.config/emonoda.yaml`)

Конфиг — YAML, лежит в `~/.config/emonoda.yaml`. Секции: `core`, `client` (**в единственном числе** — параметры выбранного в `core.client` клиента), `trackers`, плюс по-командные `emupdate`/`emfind`/… и `confetti` (уведомления).

```yaml
core:
    client: qbittorrent
    # каноническое хранилище .torrent-файлов:
    torrents_dir: /mnt/dat1T/Torrents

    # data_root_dir нужен ТОЛЬКО для `emfind orphans`.
    # Так как /mnt/dat1T используется не только под торренты — НЕ указывай сюда
    # весь диск, иначе emfind пометит твои НЕ-торрент-файлы как «мусор».
    # Либо оставь закомментированным (emupdate он не нужен), либо укажи
    # только подкаталоги, где лежат ИСКЛЮЧИТЕЛЬНО торрент-данные:
    # data_root_dir: /mnt/dat1T/Torrents/data
    # another_data_root_dirs:
    #     - /mnt/dat1T/Media/Torrents
    #     - /mnt/dat1T/Books/Torrents

# Параметры клиента (плагин qbittorrent → подключение по WebUI API)
client:
    url: http://localhost:8080
    user: admin           # пусто, если включён обход аутентификации на localhost
    passwd: ПАРОЛЬ_WEBUI   # пусто при обходе аутентификации
    timeout: 10.0

# Учётки трекеров. Пароли — в открытом виде, поэтому chmod 600 на файл!
trackers:
    rutracker.org:
        user: ЛОГИН_НА_РУТРЕКЕРЕ
        passwd: ПАРОЛЬ
        # proxy_url: socks5://127.0.0.1:9050   # если трекер заблокирован
    # nnm-club.me:
    #     user: ...
    #     passwd: ...

# Поведение обновлятора
emupdate:
    name_filter: "*.torrent"                # какие файлы проверять
    backup_dir: /mnt/dat1T/Torrents/.backup # старые .torrent складываются сюда
    backup_suffix: ".%Y.%m.%d-%H.%M.%S.bak" # с временной меткой
    show_unknown: false   # не ругаться на .torrent с неизвестных трекеров
    show_passed: false    # не показывать раздачи без изменений (тише лог)
    show_diff: true       # показывать, какие файлы изменились
```

> [!important] Права на файл
> В конфиге лежат пароли трекеров и WebUI в открытом виде:
> ```bash
> mkdir -p ~/.config && chmod 700 ~/.config
> chmod 600 ~/.config/emonoda.yaml
> mkdir -p /mnt/dat1T/Torrents/.backup
> ```

## ▶️ Первый запуск

```bash
# проверить обновления и применить их к клиенту (интерактивно)
emupdate

# только посмотреть, что обновилось бы, ничего не трогая в клиенте:
emupdate --dump-diff -            # покажет diff
# проверить конкретную раздачу по имени файла:
emupdate --name-filter "Severance*.torrent"
```

`emupdate` для каждого `.torrent` из `torrents_dir`:
1. читает URL раздачи из комментария `.torrent` → понимает, какой плагин трекера применить;
2. логинится на трекер, сверяет fingerprint сайта, проверяет наличие обновления;
3. если есть — качает новый `.torrent`, старый кладёт в `backup_dir`;
4. снимает старый торрент в qBittorrent (данные оставляет), добавляет новый на тот же save path;
5. qBittorrent делает re-check и **докачивает только изменённые файлы**.

## ⏱️ Автоматизация (cron)

Скрипт-обёртка `~/bin/run-emupdate.sh` (логирование + не зависать на капче):

```bash
#!/bin/bash
# тихий запуск emupdate для cron
# при pipx путь — ~/.local/bin/emupdate; при ручном venv — ~/emonoda-venv/bin/emupdate
exec ~/.local/bin/emupdate \
    --fail-on-captcha \
    >> /var/log/emonoda.log 2>&1
```

```bash
chmod +x ~/bin/run-emupdate.sh
```

Запись в crontab. Сам cron-демон по системам:

| Система | Cron |
| :--- | :--- |
| **Debian / Ubuntu** | стоит и запущен **из коробки** — просто `crontab -e` |
| **Gentoo** | по умолчанию нет: `emerge sys-process/cronie && rc-update add cronie default` |
| **Arch** | по умолчанию нет (там systemd-таймеры): `pacman -S cronie && systemctl enable --now cronie` |

```cron
# раз в день в 05:30 проверять обновления раздач
30 5 * * * /home/ПОЛЬЗОВАТЕЛЬ/bin/run-emupdate.sh
```

- `--fail-on-captcha` — не зависать в ожидании ввода капчи при автозапуске (раздача просто пропускается, ошибка — в лог).
- Раздачу всех логов смотри `tail -f /var/log/emonoda.log`.

## 🧹 emfind — обслуживание коллекции (осторожно с /mnt/dat1T)

`emfind` помогает искать рассинхрон между клиентом и `.torrent`-файлами:

```bash
emfind not-in-client       # .torrent есть в torrents_dir, но не загружен в qB
emfind missing-torrents    # торрент в qB есть, а .torrent-файла нет
emfind duplicate-torrents  # дубли по содержимому
emfind orphans             # «осиротевшие» файлы данных (требует data_root_dir!)
```

> [!danger] `emfind orphans` и смешанный диск
> `orphans` сканирует `data_root_dir` и считает мусором всё, что **не принадлежит ни одной раздаче**. Поскольку `/mnt/dat1T/` содержит и НЕ-торрент-данные — **никогда не указывай туда весь диск**, иначе твои личные файлы попадут в список «на удаление». Безопасные варианты:
> - вообще не задавать `data_root_dir` и не пользоваться `orphans`;
> - указать только подпапки, где лежат **исключительно** торрент-данные;
> - подстраховаться `emfind/ignore_orphans: [...]` для файлов-исключений.
>
> Команды `not-in-client` / `missing-torrents` безопасны — они смотрят только список торрентов в клиенте и `.torrent`-файлы, диск с данными не трогают.

## 🔔 Уведомления (опционально)

Секция `confetti` умеет слать сводку об обновлениях в e-mail, **Telegram**, Pushover или Atom-фид. Пример для Telegram:

```yaml
confetti:
    telegram:
        token: 1234567:ABC...        # токен бота от @BotFather
        to: ["123456789"]            # твой chat_id
```

Получить `chat_id` помогает `emconfetti-tghi`, проверить отправку — `emconfetti-demo`.

## 🔐 Fingerprint трекера (проверка подлинности сайта)

Перед отправкой логина/пароля emonoda проверяет, что перед ней **настоящий сайт трекера**: качает контрольную страницу и ищет на ней зашитый в плагин текст-маркер. Не совпало — логин не отправляется (защита от MITM/DNS-спуфинга/подменного зеркала).

Для `rutracker.org`: страница `forum/index.php`, маркер — ссылка на `static.rutracker.cc/opensearch.xml`, кодировка `cp1251`.

> [!warning] Блокировка провайдера ломает fingerprint
> Если rutracker заблокирован у провайдера, вместо сайта приходит заглушка → fingerprint не сходится и emonoda не логинится **ещё до проверки обновлений**. Лечится прокси для конкретного трекера:
> ```yaml
> trackers:
>     rutracker.org:
>         user: ...
>         passwd: ...
>         proxy_url: socks5://127.0.0.1:9050   # напр. Tor/VPN-сокс
> ```
> Капчу на входе плагин rutracker умеет разбирать сам; для cron добавляй `--fail-on-captcha`, чтобы не зависать на ней.

## 🩺 Если не работает

- **`emupdate` не видит торрент в клиенте** — проверь, что этот же `.torrent` реально загружен в qBittorrent (совпадение по infohash) и что WebUI доступен: `curl http://localhost:8080`.
- **Ошибка авторизации в qB** — неверные `user`/`passwd`, либо не включён WebUI, либо нужен обход аутентификации для localhost.
- **`unknown tracker` / раздача пропущена** — `.torrent` без распознаваемого комментария трекера или трекер не из списка поддерживаемых; `show_unknown: true` покажет такие.
- **Капча на rutracker** — без `--fail-on-captcha` придётся ввести вручную; при cron она логируется и раздача пропускается до следующего раза.
- **PEP 668 / `externally-managed-environment`** при `pip install` — ставь в venv/pipx, как выше, не через системный pip.

## 🔗 См. также

- [Флаги пиров qBittorrent](Torrent%20Flags.md)
- [Загрузчики видео — какой выбрать](../../Apps/Downloaders/%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%20%E2%80%94%20%D0%BA%D0%B0%D0%BA%D0%BE%D0%B9%20%D0%B2%D1%8B%D0%B1%D1%80%D0%B0%D1%82%D1%8C.md)
- Документация: <https://mdevaev.github.io/emonoda/> · GitHub: <https://github.com/mdevaev/emonoda>

#emonoda #Torrents #qBittorrent #Gentoo #Automation #Linux
