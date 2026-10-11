---
создал заметку: 2026-10-12T12:00:00
author: WhiteK0T
tags:
  - PostgreSQL
  - СУБД
  - Бэкап
  - PITR
  - Docker
  - Self-hosted
Источник:
  - https://t.me/bugnotfeature/28372
  - https://github.com/databasus/databasus
  - https://github.com/databasus/databasus/blob/main/assets/readme/README.ru.md
  - https://databasus.com
---

# 🗄️ Databasus — self-hosted бэкапы PostgreSQL с PITR и проверкой восстановления

**Databasus** ([github.com/databasus/databasus](https://github.com/databasus/databasus), **Apache-2.0**, 8.9k★, релиз **v3.61.0** от 2026-10-10) — бесплатная self-hosted система резервного копирования баз данных с веб-интерфейсом. Разворачивается одним Docker-контейнером, по расписанию снимает бэкапы, складывает их в выбранное хранилище, шифрует, чистит по политике хранения, шлёт уведомления и умеет **реально восстанавливать бэкап для проверки**. Автор — Ростислав Дугин ([@rostislav_dugin](https://t.me/rostislav_dugin)), есть русскоязычное сообщество [@databasus_community](https://t.me/databasus_community).

Главный фокус — PostgreSQL, но поддерживаются и **MySQL, MariaDB и MongoDB** (для них только логические бэкапы). На русский переведён README и документация на сайте; интерфейс и код — на английском.

Связанная заметка: [PostgreSQL — опорная заметка](PostgreSQL%20%E2%80%94%20%D0%BE%D0%BF%D0%BE%D1%80%D0%BD%D0%B0%D1%8F%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BA%D0%B0%20%28%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0%20MVCC-WAL%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D1%80%D0%BE%D0%BB%D0%B8%2C%20%D1%82%D0%B8%D0%BF%D1%8B%2C%20%D0%B8%D0%BD%D0%B4%D0%B5%D0%BA%D1%81%D1%8B%2C%20EXPLAIN%2C%20%D0%B1%D1%8D%D0%BA%D0%B0%D0%BF%2C%20%D1%80%D0%B5%D0%BF%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%29.md) — там разобраны WAL, `pg_dump` и репликация, на которых всё это построено.

---

## 1. Что умеет

| Возможность | Подробности |
| :--- | :--- |
| **Типы бэкапов** | **Логический** — `pg_dump` в родном сжатом формате (подходит для параллельного восстановления). **Физический** — копия всего кластера: полный, блочный инкрементальный и непрерывный поток WAL для PITR |
| **Расписание** | Каждый час / день / неделю / месяц или cron; можно задать точное время (например, 4:00 ночи) |
| **Сжатие** | В 4–8 раз при накладных расходах около 20% |
| **Хранилища** | Локальный диск, S3 и совместимые (Cloudflare R2, MinIO), Azure Blob, Google Drive, NAS, SFTP, FTP и Rclone (через него — Dropbox и десятки других облаков) |
| **Уведомления** | Email, Telegram, Slack, Discord, Teams, Mattermost, вебхуки — об успехе и сбоях |
| **Хранение** | По сроку (7 дней, 3 месяца, год), по количеству (последние 30), **GFS** (отдельно часовые, дневные, недельные, месячные, годовые) и лимиты по размеру |
| **Безопасность** | Шифрование бэкапов **AES-256-GCM** (можно хранить в чужом S3), шифрование паролей и секретов, по умолчанию бэкап идёт от **read-only пользователя**, 2FA по email, вход через Google/GitHub |
| **Команды** | Рабочие пространства, роли (viewer / member / admin / owner), журнал аудита, экспорт логов в OpenTelemetry |
| **Сеть** | Встроенный SSH-туннель — можно бэкапить базу, которая не открыта наружу |
| **Проверка восстановления** | Восстанавливает свежий бэкап во временный контейнер, сверяет размер, присылает отчёт с числом строк по каждой таблице (раздел 4) |

### Поддерживаемые СУБД

| СУБД | Версии | Бэкап |
| :--- | :--- | :--- |
| PostgreSQL | 14–18 | логический (`pg_dump`) |
| PostgreSQL | **17+** | физический, инкрементальный, PITR |
| MySQL | 5.7, 8.0, 8.4, 9, 26 | только логический |
| MariaDB | 5.5, 10, 11, 12, 13 | только логический |
| MongoDB | 4.2+ … 9 | только логический |

> [!note] Физические бэкапы — только с PostgreSQL 17
> В README в списке версий стоит «14–18 (physical and logical)», но FAQ на сайте уточняет: физические и PITR-бэкапы требуют **PostgreSQL 17 или новее**, на старых версиях работают только логические через `pg_dump`. Если нужен PITR на PG 14–16 — обновите сервер или берите pgBackRest / WAL-G (раздел 7).

---

## 2. Как устроены физические бэкапы и PITR

Databasus снимает физические бэкапы **удалённо со своего хоста** по стандартному протоколу репликации. На сервер с базой ничего ставить не нужно, поэтому это работает и с управляемыми базами (Amazon RDS, Google Cloud SQL), где протокол репликации открыт, а установка ПО запрещена.

Вся механика — родная, из PostgreSQL 17 (её разработали Robert Haas и David Steele, автор pgBackRest):

| Шаг | Чем делается |
| :--- | :--- |
| Полный бэкап | `pg_basebackup`, поток идёт прямо в Databasus |
| Инкремент | `pg_basebackup --incremental` — передаются только изменённые блоки; изменения отслеживают серверные WAL-сводки (`summarize_wal = on`) |
| Непрерывный WAL | `pg_receivewal` — цепочка восстановления между бэкапами остаётся полной |
| Восстановление | `pg_combinebackup` собирает каталог данных из полного бэкапа и цепочки инкрементов, затем PostgreSQL проигрывает WAL до выбранного момента и становится первичным |

Что подготовить на стороне PostgreSQL (по документации; точные команды интерфейс Databasus показывает уже с вашими значениями):

```ini
# postgresql.conf
wal_level = replica          # по умолчанию уже replica
summarize_wal = on           # нужно для блочных инкрементов
```
```sql
ALTER ROLE backup_user WITH REPLICATION;   -- pg_basebackup требует право репликации
```
```
# pg_hba.conf — доступ к протоколу репликации с адреса Databasus
host  replication  backup_user  <IP-хоста-Databasus>/32  scram-sha-256
```

Инкременты и поток WAL необязательны: можно снимать только полные бэкапы.

> [!info] Про «восстановите работу мгновенно»
> Восстановление на нужную секунду (PITR) — реальная сильная сторона: потеря данных близка к нулю, если поток WAL работал. Но само восстановление — это не кнопка «откатить базу на месте». Интерфейс выдаёт пошаговую инструкцию и скрипт `databasus-recovery.sh`, который на целевом сервере скачивает бандл, запускает `pg_combinebackup`, проигрывает WAL до `--target-time` и поднимает PostgreSQL. Время восстановления (RTO) зависит от размера базы и объёма WAL. Его стоит один раз замерить на тестовом стенде, чтобы знать реальную цифру.

```bash
# восстановление физического бэкапа на момент времени (команду с токеном даёт интерфейс)
sh databasus-recovery.sh --target-time '2026-10-12 14:30:00+00:00' '<URL-бандла-с-токеном>' /var/lib/postgresql/restore
```

Раньше для физических бэкапов был отдельный **агент** на хосте базы. В текущих версиях он объявлен устаревшим: авторы прямо пишут, что первая реализация давала долгий RTO, и перешли на удалённую схему выше.

---

## 3. Установка

Databasus — один Docker-контейнер с веб-интерфейсом на порту **4005**, данные — в каталоге `databasus-data`.

### Docker Compose (любой Linux)

```yaml
services:
  databasus:
    container_name: databasus
    image: databasus/databasus:latest       # то же есть в ghcr.io/databasus/databasus
    ports:
      - "127.0.0.1:4005:4005"               # только localhost — см. предупреждение ниже
    volumes:
      - ./databasus-data:/databasus-data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "databasus", "healthcheck"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 60s
```
```bash
docker compose up -d
```

> [!warning] Сначала создайте учётку, и не открывайте порт наружу
> **Первая зарегистрированная учётная запись становится администратором** всего инстанса. В примерах из README порт опубликован как `"4005:4005"`, то есть на всех адресах, а Docker обходит обычные правила `input` у nftables/iptables. На сервере с публичным IP привяжите порт к `127.0.0.1` (как выше) и заходите через SSH-туннель или reverse-proxy с HTTPS:
> ```bash
> ssh -L 4005:127.0.0.1:4005 user@<IP-сервера>   # затем http://localhost:4005
> ```
> Админскую учётку можно создать сразу из консоли, не открывая регистрацию в браузере:
> ```bash
> docker exec -it databasus ./main --create-user --email="ops@example.com" --password="..." --role=admin
> ```

### Подготовка Docker по системам

| Система | Команды |
| :--- | :--- |
| **Gentoo (OpenRC)** | `emerge --ask app-containers/docker app-containers/docker-cli app-containers/docker-compose` → `rc-update add docker default && rc-service docker start`. Скрипт-установщик **не подходит**: он рассчитан на `apt` |
| **Debian / Ubuntu** | Официальный скрипт ставит Docker из репозитория Docker и разворачивает Databasus в `/opt/databasus/` с автозапуском. Перед запуском прочитайте его — он выполняется от root: `curl -fsSL https://raw.githubusercontent.com/databasus/databasus/refs/heads/main/install-databasus.sh -o install-databasus.sh && less install-databasus.sh && sudo bash install-databasus.sh` |
| **Arch** | `pacman -S docker docker-compose` → `systemctl enable --now docker`, затем Compose выше |
| **Kubernetes** | Helm-чарт: `helm install databasus oci://ghcr.io/databasus/charts/databasus -n databasus --create-namespace` |
| **Entware (роутер)** | Сам Databasus на роутере не запустить (нужен Docker). Зато роутер с USB-диском можно сделать **хранилищем** для бэкапов по SFTP: `opkg install openssh-sftp-server` и указать его в Databasus как SFTP-хранилище. Бэкапы зашифрованы AES-256-GCM, так что лежать на роутере им безопасно |

### Первые шаги в интерфейсе

1. Откройте `http://localhost:4005` (или через туннель) и создайте **первую** учётку — она админская.
2. **New Database** → данные подключения (лучше отдельный пользователь только на чтение).
3. Расписание → хранилище → политика хранения → уведомления.
4. Сохранить: Databasus проверит настройки и запустит расписание.

> [!tip] Сохраните ключ шифрования
> Сразу после установки сделайте бэкап самого Databasus или хотя бы скопируйте **секретный ключ шифрования**. Без него зашифрованные бэкапы не восстановить, если сервер с Databasus потеряется.

Сброс пароля и список админов:
```bash
docker exec -it databasus ./main --list-admins
docker exec -it databasus ./main --new-password="NewPass123" --email="owner@example.com"
```

---

## 4. Проверка восстановления

Бэкап, который ни разу не восстанавливали, — это надежда, а не бэкап. Databasus проверяет его делом: берёт свежий бэкап, восстанавливает во временный контейнер нужной мажорной версии, сверяет с исходной базой и присылает отчёт с числом строк по каждой таблице. Запускать можно после каждого бэкапа или по расписанию, отчёт — в любой настроенный канал уведомлений.

Проверку выполняет отдельный **агент проверки** — небольшой Go-бинарник на любой машине со свободными ресурсами:
- нужен **Docker** на этой машине и исходящий доступ к Databasus по **HTTPS** (HTTP — только с флагом `--allow-insecure-http` для тестов);
- минимум **1 CPU и 512 МБ RAM** на каждую параллельную задачу;
- диск: размер бэкапа + размер базы без сжатия + запас до 5 ГБ на задачу. Лимиты задаются флагами `--max-cpu`, `--max-ram-mb`, `--max-disk-gb`, `--max-concurrent-jobs`.

---

## 5. Если Databasus недоступен

Бэкапы не заперты внутри Databasus: на сайте есть отдельная инструкция [how-to-recover-without-databasus](https://databasus.com/how-to-recover-without-databasus). Логические бэкапы — обычные дампы для `pg_restore`, физические собираются штатным `pg_combinebackup`. Понадобятся сами файлы из хранилища и **ключ шифрования**.

---

## 6. Когда подходит

| Задача | Databasus |
| :--- | :--- |
| Несколько баз (PostgreSQL, MySQL, MongoDB) на VPS, нужны расписание, S3 и уведомления в Telegram | ✅ основной сценарий, всё через веб-интерфейс |
| PITR для PostgreSQL 17+, в том числе управляемого (RDS, Cloud SQL) | ✅ удалённо, без установки на сервер базы |
| PITR для PostgreSQL 14–16 | ❌ только логические бэкапы — нужен pgBackRest или WAL-G |
| Команда с разграничением доступа и аудитом | ✅ рабочие пространства, роли, журнал |
| Одна маленькая база, хватает `pg_dump` по cron | Можно, но и cron-скрипта достаточно |

## 7. Альтернативы

| Инструмент | Чем отличается |
| :--- | :--- |
| **pgBackRest** | Зрелый стандарт для физических бэкапов и PITR, работает с PG старых версий, параллельность, проверка. Без веб-интерфейса, настройка через конфиги |
| **WAL-G** | Физические бэкапы и WAL прямо в облачные хранилища, поддерживает и другие СУБД. CLI |
| **Barman** | Решение для парка PostgreSQL-серверов от EDB. CLI |
| **pgBackWeb** | Веб-интерфейс над `pg_dump`: проще, но без физических бэкапов и PITR |
| `pg_dump` + cron | Минимум: логические дампы без PITR |

У Databasus на сайте есть подробные сравнения с каждым из них (`databasus-vs-pgbackrest`, `-vs-wal-g`, `-vs-barman`, `-vs-pgbackweb`). Учитывайте, что их писали авторы Databasus.

## 🔗 Ссылки

- Репозиторий: https://github.com/databasus/databasus
- README на русском: https://github.com/databasus/databasus/blob/main/assets/readme/README.ru.md
- Сайт и документация: https://databasus.com
- FAQ (как работают физические бэкапы и PITR): https://databasus.com/faq
- Восстановление без Databasus: https://databasus.com/how-to-recover-without-databasus
- PostgreSQL 17: непрерывное архивирование и PITR — https://www.postgresql.org/docs/17/continuous-archiving.html, `pg_combinebackup` — https://www.postgresql.org/docs/17/app-pgcombinebackup.html
- Сообщество в Telegram: https://t.me/databasus_community
- Исходный пост: https://t.me/bugnotfeature/28372

#PostgreSQL #СУБД #Бэкап #PITR #Docker #Self-hosted
