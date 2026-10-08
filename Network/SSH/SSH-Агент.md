---
создал заметку: 2026-10-08T23:10:00
author: WhiteK0T
tags:
  - SSH
  - Linux
  - Security
  - Network
Источник:
  - https://man.openbsd.org/ssh-agent
  - https://man.openbsd.org/ssh-add
  - https://man.openbsd.org/ssh_config
  - https://www.openssh.com/releasenotes.html
---

# SSH-агент (`ssh-agent`, `ssh-add`) — ключи в памяти, автозапуск, проброс и безопасность

> [!info] Коротко
> `ssh-agent` — фоновый процесс, который **держит расшифрованные приватные ключи в памяти** и подписывает ими запросы аутентификации. Passphrase вы вводите один раз, при `ssh-add`, а дальше `ssh`, `scp`, `rsync`, `git` ходят по ключу без вопросов. Сам ключ агент **никому не отдаёт**: клиенты могут только попросить его что-то подписать.
>
> Всё ниже проверено на **OpenSSH 10.5p1** (Gentoo, 2026-10-08). Для версий старше 10.1 отличается путь к сокету (раздел 2).

Связанные заметки: [SSH-Ключи](SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md) (типы ключей, генерация, права), [SSH-Продвинутое руководство](SSH-%D0%9F%D1%80%D0%BE%D0%B4%D0%B2%D0%B8%D0%BD%D1%83%D1%82%D0%BE%D0%B5%20%D1%80%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE.md), [ssh-audit](ssh-audit%20%28jtesta%29%20%E2%80%94%20%D0%B0%D1%83%D0%B4%D0%B8%D1%82%20%D0%B8%20%D1%85%D0%B0%D1%80%D0%B4%D0%BD%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%20SSH-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%B0%20%D0%B8%20%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%B0%20%28%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D1%8B%2C%20CVE%2C%20policy-%D1%81%D0%BA%D0%B0%D0%BD%2C%20%D0%B3%D0%B0%D0%B9%D0%B4%D1%8B%29.md).

---

## 1. Зачем он нужен

Без агента есть два плохих варианта:
- ключ **без passphrase**: удобно, но украденный файл `~/.ssh/id_ed25519` сразу даёт доступ ко всем серверам;
- ключ **с passphrase**: безопасно, но её спрашивают при каждом `ssh`, `git pull` и в каждом скрипте.

Агент совмещает плюсы: на диске ключ зашифрован, а в рамках сессии вы вводите passphrase один раз. Дополнительно агент умеет:
- ограничивать **время жизни** ключа (`-t`);
- требовать **подтверждения** каждого использования (`-c`);
- разрешать ключ **только для определённых хостов** (`-h`, OpenSSH ≥ 8.9);
- **пробрасываться** на удалённый сервер (`ssh -A`), чтобы оттуда ходить дальше вашим ключом, не копируя его (с оговорками, раздел 6);
- работать с аппаратными ключами FIDO (`-K`) и PKCS#11-токенами (`-s`).

---

## 2. Как это устроено

```
ssh ──(UNIX-сокет $SSH_AUTH_SOCK)──► ssh-agent  [ключи в памяти]
 │        «подпиши вот это»          │
 │◄─────────── подпись ──────────────┘
 └──► сервер проверяет подпись по authorized_keys
```

- Агент слушает **UNIX-сокет**. Путь к нему клиенты берут из переменной **`SSH_AUTH_SOCK`**, а PID агента лежит в `SSH_AGENT_PID` (он нужен для `ssh-agent -k`).
- **Где сокет.** С **OpenSSH 10.1** (октябрь 2025) сокеты переехали из `/tmp/ssh-XXXX/agent.<pid>` в **`~/.ssh/agent/s.*`**. Так процессы, у которых есть доступ к `/tmp`, но нет доступа к домашнему каталогу, больше не получают ключи «по соседству». Старое поведение включается флагом `ssh-agent -T`. Проверено:
  ```
  SSH_AUTH_SOCK=/home/claude/.ssh/agent/s.sIuCk78wxV.agent.lEvgMCzyyM
  ```
- **Кто может пользоваться агентом.** Сокет доступен только владельцу (`0600`). Но **root и любой процесс под вашим же пользователем** могут к нему подключиться: так прямо сказано в `man ssh-agent`. Ключ они не вытащат, но **подписывать** им смогут, пока агент жив.
- Агент очищает все ключи по сигналу `SIGUSR1`: `pkill -USR1 ssh-agent`.

---

## 3. Быстрый старт

```bash
eval "$(ssh-agent -s)"          # запустить агент и экспортировать SSH_AUTH_SOCK/SSH_AGENT_PID
ssh-add                         # добавить ключи по умолчанию (~/.ssh/id_ed25519, id_rsa, id_ecdsa, *_sk …)
ssh-add ~/.ssh/work_ed25519     # добавить конкретный ключ
ssh-add -l                      # отпечатки загруженных ключей
ssh user@host                  # passphrase больше не спрашивается
```

> [!warning] Именно `eval "$(ssh-agent -s)"`, а не `ssh-agent`
> `ssh-agent` без `eval` запустится, но только **напечатает** команды `export`. Переменные не попадут в оболочку, и `ssh-add` ответит `Could not open a connection to your authentication agent`.

Флаг `-s` даёт синтаксис sh/bash/zsh, `-c` — csh/tcsh. Без флага агент выбирает синтаксис по `$SHELL`.

Есть и другой способ: **агент на время одной команды**. Агент живёт, пока работает дочерний процесс, и сам завершается после него:
```bash
ssh-agent bash                 # подоболочка со своим агентом
ssh-agent sh -c 'ssh-add ~/.ssh/deploy && rsync -a ./ host:/srv/'
```

### Коды возврата `ssh-add -l` (удобно в скриптах, проверено)

| Код | Значение | Сообщение |
| :---: | :--- | :--- |
| `0` | агент доступен, ключи есть | список отпечатков |
| `1` | агент доступен, ключей нет | `The agent has no identities.` |
| `2` | к агенту не подключиться | `Error connecting to agent: No such file or directory` / `Could not open a connection to your authentication agent` |

---

## 4. Шпаргалка

### `ssh-add`

| Команда | Что делает |
| :--- | :--- |
| `ssh-add [файл…]` | Добавить ключ(и). Без аргументов — `id_rsa`, `id_ecdsa`, `id_ecdsa_sk`, `id_ed25519`, `id_ed25519_sk`, `id_mldsa44_ed25519`. Рядом подхватывается сертификат `*-cert.pub` |
| `ssh-add -l` / `-L` | Список ключей: отпечатки / публичные ключи целиком (`-L` удобно вставлять в `authorized_keys`) |
| `ssh-add -t 8h ключ` | Ключ сам удалится из агента через 8 часов. Формат времени как в `sshd_config`: `90`, `30m`, `8h`, `1d` |
| `ssh-add -c ключ` | Каждое использование нужно подтвердить окном `ssh-askpass` |
| `ssh-add -d ключ` | Удалить один ключ (можно указать `.pub`) |
| `ssh-add -D` | Удалить все ключи |
| `ssh-add -x` / `-X` | Заблокировать / разблокировать агент паролем. Пока он заблокирован, ключи не используются |
| `ssh-add -T ключ.pub` | Проверить, что подходящий приватный ключ в агенте реально подписывает |
| `ssh-add -h host` | Ограничить ключ хостами назначения (раздел 6) |
| `ssh-add -K` | Загрузить резидентные ключи с FIDO-токена (YubiKey и т.п.) |
| `ssh-add -s /usr/lib64/…/opensc-pkcs11.so` | Ключи со смарт-карты или токена PKCS#11 (`-e` — выгрузить) |
| `ssh-add -Q` | Какие расширения протокола поддерживает агент |
| `ssh-add -v` | Отладка (до `-vvv`) |

`ssh-add` **отказывается** загружать ключ, если файл читают другие (`chmod 600`!).

### `ssh-agent`

| Флаг | Что делает |
| :--- | :--- |
| `-s` / `-c` | Вывод для sh / csh |
| `-t life` | Время жизни по умолчанию для всех добавляемых ключей (`ssh-add -t` его перекрывает). Без флага — вечно |
| `-a путь` | Слушать на заданном сокете (удобно для постоянного пути) |
| `-D` / `-d` | Не уходить в фон / отладка. Нужно для systemd и supervisor |
| `-k` | Убить агент из `$SSH_AGENT_PID`. С `eval "$(ssh-agent -k)"` переменные заодно снимутся |
| `-T` | Сокет в `$TMPDIR`, как до 10.1 |
| `-u` / `-U` | Только почистить «мёртвые» сокеты в `~/.ssh/agent/` и выйти / не чистить их при старте |
| `-P шаблон` | Какие библиотеки PKCS#11/FIDO разрешено подгружать (по умолчанию `/usr/lib*/*,/usr/local/lib*/*`) |
| `-O allow-remote-pkcs11` | Разрешить **проброшенным** клиентам грузить PKCS#11. Не включайте без нужды (см. CVE-2023-38408) |

---

## 5. Настройка в `~/.ssh/config`

```sshconfig
Host *
    AddKeysToAgent 8h        # первый ssh сам кладёт ключ в агент на 8 часов
    IdentitiesOnly yes       # предлагать серверу только ключи из IdentityFile
    ForwardAgent no          # по умолчанию и так no; явно — для ясности

Host github.com
    IdentityFile ~/.ssh/github_ed25519

Host prod-*
    IdentityFile ~/.ssh/prod_ed25519
    AddKeysToAgent confirm   # каждый вход на прод — через подтверждение
```

| Опция | Значения | Смысл |
| :--- | :--- | :--- |
| `AddKeysToAgent` | `no` (по умолч.), `yes`, `ask`, `confirm`, интервал (`8h`) | Ключ попадает в агент при первом использовании, отдельный `ssh-add` не нужен. `confirm` — как `ssh-add -c` |
| `IdentitiesOnly` | `yes`/`no` | Без него клиент предлагает серверу **все** ключи агента подряд. Когда ключей больше 5–6, сервер рвёт соединение: `Too many authentication failures` (лимит `MaxAuthTries`, по умолчанию 6) |
| `IdentityAgent` | путь, `SSH_AUTH_SOCK`, `$VAR`, `none` | Какой агент использовать для хоста: можно указать KeePassXC или gpg-agent для одних хостов и обычный агент для других. `none` — не использовать агент вовсе |
| `ForwardAgent` | `no` (по умолч.), `yes`, путь или `$VAR` | Пробрасывать агент на сервер (то же, что `ssh -A`). Можно пробросить **другой** агент, например с одним ограниченным ключом |
| `IdentityFile` | путь к ключу или к `.pub` | Можно указать **`.pub`**, если сам ключ живёт только в агенте или на токене |

---

## 6. Проброс агента (`ssh -A`): удобно, но опасно

**Зачем.** Вы на ноутбуке, заходите на `bastion`, оттуда на `db` или делаете `git pull` с GitHub, и всё это **вашим локальным ключом**, который на `bastion` никогда не копировался.

```bash
ssh -A user@bastion
bastion$ ssh-add -l          # видны ключи с ноутбука
bastion$ git pull            # работает вашим ключом
```

> [!danger] Главный риск
> На удалённой машине появляется сокет, ведущий к вашему агенту. **root на этом сервере** (или взломщик с правами root) может, пока вы подключены, выставить `SSH_AUTH_SOCK` на ваш сокет и **входить вашими ключами куда угодно**. Сами ключи он не получит, но для атаки это и не нужно. Это прямо написано в `man ssh` у флага `-A`.

### Что делать вместо этого

1. **Нужен только «прыжок» через сервер — используйте `ProxyJump`**, а не `-A`. Соединение с `db` шифруется сквозным туннелем от ноутбука, и агент на `bastion` не попадает:
   ```bash
   ssh -J user@bastion user@db
   ```
   ```sshconfig
   Host db
       HostName 10.0.0.5
       ProxyJump bastion
   ```
2. **Пробрасывайте точечно**: `ForwardAgent yes` только в блоке `Host` конкретного доверенного сервера, никогда в `Host *`.
3. **Подтверждение**: ключ, добавленный через `ssh-add -c` (или `AddKeysToAgent confirm`), на каждое использование, в том числе удалённое, вызывает окно на **вашем** экране. Неожиданное окно — повод насторожиться. Нужен `ssh-askpass` (раздел 7), иначе подпись просто отклоняется: `agent refused operation`.
4. **Ограничение по хостам (OpenSSH ≥ 8.9)**: ключ разрешено использовать только на заданном пути.
   ```bash
   # ключ годится только для входа с ноутбука на bastion,
   # а с bastion (через проброшенный агент) — только на git@github.com
   ssh-add -h bastion -h "bastion>git@github.com" ~/.ssh/id_ed25519
   ```
   Хосты сверяются по **ключам хостов** из `known_hosts`, поэтому все участники должны быть там. Ограничение работает, только если и клиенты, и серверы на пути поддерживают расширение `session-bind@openssh.com` (OpenSSH 8.9+; `ssh-add -Q` его показывает). По `man ssh-add`, root на промежуточном узле всё равно может использовать сокет, но **только для разрешённых** назначений.
5. **Отдельный агент для проброса**: `ForwardAgent ~/.ssh/agent-deploy.sock` пробрасывает агент, где лежит один ограниченный ключ.

**На сервере** (`/etc/ssh/sshd_config`): `AllowAgentForwarding no` запрещает проброс. Но, по `man sshd_config`, это **не повышает безопасность**, если у пользователя есть shell: проброс можно устроить своими средствами. В **OpenSSH 10.6** (2026-10-06) появилась опция `AgentSocketPath` — где sshd создаёт сокеты проброшенных агентов (по умолчанию `user:.ssh/agent`).

> [!warning] CVE-2023-38408 — обновите OpenSSH до ≥ 9.3p2
> Через **проброшенный** агент можно было заставить `ssh-agent` подгрузить системные PKCS#11-библиотеки и получить **RCE на вашей машине**. Это исправлено в 9.3p2/9.4: теперь удалённым клиентам загрузка PKCS#11 по умолчанию запрещена (`-O allow-remote-pkcs11` возвращает старое поведение — не надо).

---

## 7. Автозапуск по системам

Цель — **один агент на сессию** (а не по агенту на каждый терминал) и правильный `SSH_AUTH_SOCK` во всех программах.

### Gentoo (OpenRC) — нет systemd user units, поэтому через профиль

**Вариант 1 — `keychain`** (готовый «переиспользователь» агента, есть в дереве):
```bash
emerge --ask net-misc/keychain
```
```sh
# ~/.bash_profile (или ~/.zprofile)
eval "$(keychain --eval --quiet --timeout 480 id_ed25519)"
```
`keychain` находит уже запущенный агент или стартует новый, а passphrase спрашивает один раз после загрузки системы. `--timeout` задаётся в **минутах**.

**Вариант 2 — без пакетов** (POSIX sh; проверено в `sh` и `bash`: вторая оболочка подхватывает тот же агент, после `ssh-agent -k` поднимается новый):
```sh
# ~/.profile или ~/.bash_profile
agent_env="$HOME/.ssh/agent.env"
ssh-add -l >/dev/null 2>&1
if [ $? -eq 2 ]; then                          # 2 = к агенту не подключиться
  [ -r "$agent_env" ] && . "$agent_env" >/dev/null
  ssh-add -l >/dev/null 2>&1
  if [ $? -eq 2 ]; then
    (umask 077; ssh-agent -s -t 8h > "$agent_env")
    . "$agent_env" >/dev/null
  fi
fi
unset agent_env
```
Вместе с `AddKeysToAgent 8h` в `~/.ssh/config` получается удобно: агент живёт всегда, ключ попадает туда при первом `ssh`.

### Debian / Ubuntu (systemd)

Пакет `openssh-client` ставит **пользовательские юниты** `ssh-agent.socket` + `ssh-agent.service`. В графической сессии агент поднимается сам, а сокет — `$XDG_RUNTIME_DIR/openssh_agent` (юнит сам экспортирует `SSH_AUTH_SOCK` в окружение systemd). Для ssh/tty-сессий без графики:
```bash
systemctl --user enable --now ssh-agent.socket
echo 'export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/openssh_agent"' >> ~/.profile
```
Сервис запускается с `SSH_ASKPASS_REQUIRE=force`. Аргументы (например, `-t`) добавляются через `systemctl --user edit ssh-agent.service`:
```ini
[Service]
ExecStart=
ExecStart=/usr/bin/ssh-agent -D -t 8h
```
GNOME может подменять агент своим (`gcr-ssh-agent`, сокет `$XDG_RUNTIME_DIR/gcr/ssh`): проверяйте, куда указывает `echo $SSH_AUTH_SOCK`.

### Arch (systemd)

Пакет `openssh` даёт `ssh-agent.socket` с сокетом `%t/ssh-agent.socket`, но **переменную не экспортирует** — сделайте это сами:
```bash
systemctl --user enable --now ssh-agent.socket
echo 'export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"' >> ~/.bash_profile
```
Юниты имеют `ConditionEnvironment=!SSH_AGENT_PID`: если агент уже запущен иначе, они не стартуют. `keychain` тоже есть: `pacman -S keychain`.

### KDE Plasma (любой дистрибутив, в том числе Gentoo/OpenRC)

Скрипты из `~/.config/plasma-workspace/env/` выполняются **до** старта Plasma, и их переменные видят все программы сессии:
```sh
# ~/.config/plasma-workspace/env/ssh-agent.sh
[ -n "$SSH_AGENT_PID" ] || eval "$(ssh-agent -s -t 8h)"
export SSH_ASKPASS=/usr/bin/ksshaskpass SSH_ASKPASS_REQUIRE=prefer
```
```sh
# ~/.config/plasma-workspace/shutdown/ssh-agent-stop.sh  (chmod +x)
[ -z "$SSH_AGENT_PID" ] || eval "$(ssh-agent -k)"
```
`ksshaskpass` показывает графический запрос passphrase или подтверждения (`-c`) и умеет сохранять passphrase в KWallet. Установка: Gentoo `emerge kde-plasma/ksshaskpass`, Debian `apt install ksshaskpass`, Arch `pacman -S ksshaskpass`. Без KDE подойдёт `net-misc/x11-ssh-askpass` (Gentoo) / `ssh-askpass` (Debian) / `x11-ssh-askpass` (Arch).

### Entware (роутер)

Агент есть в пакете **`openssh-client-utils`** (содержит `ssh-agent`, `ssh-add`, `ssh-keyscan`, `ssh-keysign`; OpenSSH 10.2 для armv7):
```sh
opkg update && opkg install openssh-client openssh-client-utils openssh-keygen
eval "$(ssh-agent -s -t 1h)"; ssh-add /opt/root/.ssh/id_ed25519
```
С 10.1 сокет создаётся в `~/.ssh/agent/`. Если `$HOME` на роутере только для чтения или живёт в tmpfs, задайте путь явно: `ssh-agent -a /opt/tmp/agent.sock` (или `-T`). Штатный клиент **Dropbear** (`dbclient`) собственного агента не имеет, но использует агент из `SSH_AUTH_SOCK` и умеет его пробрасывать (`-A`). Держать ключи в агенте на роутере имеет смысл разве что для коротких скриптов (`ssh-agent sh -c '…'`). Для постоянной работы безопаснее ключ без агента с ограничением в `authorized_keys` на той стороне (`command=`, `from=`).

---

## 8. Альтернативные агенты

Любая программа, говорящая на протоколе агента, подключается через `SSH_AUTH_SOCK` или `IdentityAgent`:

| Агент | Чем хорош | Как подключить |
| :--- | :--- | :--- |
| **gpg-agent** | SSH-ключ на OpenPGP-смарткарте или YubiKey (OpenPGP-апплет), единый pinentry | `enable-ssh-support` в `~/.gnupg/gpg-agent.conf`, `export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)` |
| **KeePassXC** | Ключи лежат в базе паролей и попадают в агент при её открытии, а при блокировке базы убираются | «Настройки → SSH-агент» + вкладка «SSH Agent» у записи с вложенным ключом |
| **gnome-keyring / gcr-ssh-agent** | Встроен в GNOME, разблокируется паролем входа | обычно уже активен в GNOME |
| **FIDO-ключи (`ed25519-sk`)** | Приватный ключ вообще не покидает токен, каждая подпись требует касания | `ssh-keygen -t ed25519-sk -O resident`, затем `ssh-add -K` |

---

## 9. Диагностика

| Симптом | Причина | Решение |
| :--- | :--- | :--- |
| `Could not open a connection to your authentication agent` / `Error connecting to agent` | Нет `SSH_AUTH_SOCK` или сокет «мёртвый» | `eval "$(ssh-agent -s)"`, проверить `echo $SSH_AUTH_SOCK; ls -l "$SSH_AUTH_SOCK"` |
| `The agent has no identities` | Агент есть, ключей нет | `ssh-add`; или `AddKeysToAgent yes` |
| `Too many authentication failures` | Агент предложил серверу слишком много ключей | `IdentitiesOnly yes` + `IdentityFile` для хоста |
| `sign_and_send_pubkey: signing failed … agent refused operation` | Ключ с `-c`/`confirm`, а `ssh-askpass` не найден (или нет `DISPLAY`); агент заблокирован (`-x`); ключ ограничен `-h` для другого хоста | установить askpass / `ssh-add -X` / проверить ограничения |
| После `tmux attach` или `screen -r` ssh «забыл» ключи | В старой tmux-сессии остался `SSH_AUTH_SOCK` от прошлого SSH-входа | В `~/.ssh/rc` на сервере: `[ -S "$SSH_AUTH_SOCK" ] && ln -sf "$SSH_AUTH_SOCK" ~/.ssh/agent/current`, в `~/.tmux.conf`: `set-environment -g SSH_AUTH_SOCK ~/.ssh/agent/current` |
| `sudo git pull` не видит ключ | `sudo` чистит окружение | Не тянуть ключи под root; если очень нужно — `Defaults env_keep += "SSH_AUTH_SOCK"` в sudoers (root получит доступ к агенту) |
| Агентов десяток, `ps` полон `ssh-agent` | `eval "$(ssh-agent)"` в `~/.bashrc` — по агенту на каждый терминал | Переиспользование (раздел 7), `keychain` или systemd-сокет |
| После обновления до 10.1+ скрипт ищет сокет в `/tmp/ssh-*` | Сокеты переехали в `~/.ssh/agent/` | Брать путь только из `$SSH_AUTH_SOCK` или запускать агент с `-a`/`-T` |

> [!note] Про `~/.ssh/rc` из рецепта для tmux
> Если `~/.ssh/rc` существует, sshd запускает его **вместо** `xauth`: при X11-форвардинге скрипт должен сам передать cookie в `xauth` (пример в `man sshd`, раздел SSHRC). Писать в stdout ему нельзя, только в stderr. Без X11-форвардинга достаточно одной строки с `ln -sf`.

Что предлагает клиент серверу и откуда:
```bash
ssh -v user@host 2>&1 | grep -E 'Will attempt key|Offering|Server accepts|agent'
```
Строка `… agent` после имени ключа значит, что ключ взят из агента.

---

## 10. Чек-лист безопасности

- [ ] Ключи на диске **с passphrase**, агент снимает неудобство.
- [ ] У ключей в агенте **ограничено время жизни** (`-t`, `AddKeysToAgent 8h`), а не «навсегда».
- [ ] `ForwardAgent` **не** в `Host *`. Для прыжков через сервер используется `ProxyJump`.
- [ ] Для проброса на сомнительные серверы — `ssh-add -c` (подтверждение) и/или `-h` (ограничение хостов).
- [ ] `IdentitiesOnly yes`, чтобы сервер не видел все ваши публичные ключи (по ним можно отследить, что это один и тот же человек на разных сервисах).
- [ ] OpenSSH ≥ 9.3p2 (CVE-2023-38408), без `-O allow-remote-pkcs11`.
- [ ] Отошли от компьютера — `ssh-add -x` (блокировка) или `ssh-add -D`.
- [ ] Самое ценное — на FIDO-токене (`ed25519-sk`) или в KeePassXC с автоблокировкой.

## Ссылки

- `man ssh-agent`: https://man.openbsd.org/ssh-agent
- `man ssh-add`: https://man.openbsd.org/ssh-add
- `man ssh_config` (AddKeysToAgent, ForwardAgent, IdentityAgent): https://man.openbsd.org/ssh_config
- Release notes OpenSSH (10.1 — сокеты в `~/.ssh/agent`, 10.6 — `AgentSocketPath`): https://www.openssh.com/releasenotes.html
- Ограничения агента по хостам (Damien Miller): https://www.openssh.com/agent-restrict.html
- CVE-2023-38408 (Qualys): https://www.qualys.com/2023/07/19/cve-2023-38408/rce-openssh-forwarded-ssh-agent.txt
- keychain: https://www.funtoo.org/Funtoo:Keychain
- Arch Wiki — SSH keys / ssh-agent: https://wiki.archlinux.org/title/SSH_keys#SSH_agents

#SSH #Linux #Security #Network
