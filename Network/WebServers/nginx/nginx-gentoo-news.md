---
создал заметку: 2026-11-22T22:57:51
author: WhiteK0T
tags:
  - nginx
  - Gentoo
  - Portage
  - WebServer
Источник:
  - https://raw.githubusercontent.com/gentoo/gentoo-news/master/2022-05-26-apache-nginx-glep-81/2022-05-26-apache-nginx-glep-81.en.txt
  - https://www.gentoo.org/support/news-items/2025-07-05-nginx-packaging-changes.html
  - https://www.gentoo.org/glep/glep-0081.html
  - https://devmanual.gentoo.org/eclass-reference/acct-user.eclass/index.html
  - https://packages.gentoo.org/categories/www-nginx
  - https://devmanual.gentoo.org/eclass-reference/nginx-module.eclass/index.html
---

# nginx в Gentoo — системный пользователь, модули, USE-флаги и журналы

Две новости из `eselect news read` описывают разные миграции: **GLEP 81** меняет то, как Portage управляет учётной записью службы, а **переупаковка nginx** — то, как собираются и подключаются модули и где по умолчанию лежат журналы. Это архивные объявления Gentoo, а не новые требования для каждой установки. Если nginx уже обновлён и работает, не нужно повторять миграцию: проверь только те места, которые настраивал вручную.[1][2]

См. также [основную заметку по nginx](nginx%20%E2%80%94%20%D0%B2%D0%B5%D0%B1-%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%B8%20reverse-proxy%20%E2%80%94%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%2C%20%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%2C%20server-location%2C%20%D1%81%D1%82%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%2C%20%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%2C%20TLS%2C%20%D0%BA%D1%8D%D1%88%20%28%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%29.md).

## 2022: системные учётные записи по GLEP 81

Новость `2022-05-26-apache-nginx-glep-81` опубликована **20 мая 2022 года**, начало миграции было назначено **после 1 июля 2022 года**. Пользователей и группы `nginx` и `apache` вынесли в отдельные пакеты `acct-user/*` и `acct-group/*`. Это позволяет нескольким пакетам зависеть от одной учётной записи; её параметры больше не нужно описывать в каждом пакете службы.[1][3]

**Что это меняет на практике.** Если вручную добавлял `nginx` в группу, например для доступа к сокету бэкенда, перенеси это изменение в конфигурацию Portage: пакет учётной записи может вернуть значения по умолчанию. Если пользователь и группы не менялись, переопределения не нужны. Описание учётной записи в Portage не заменяет директиву `user` в `nginx.conf`: это разные настройки.[1][4]

Переменные можно задать глобально в `/etc/portage/make.conf`. Для точечной настройки в `/etc/portage/package.env` свяжи **`acct-user/nginx`**, а не `www-servers/nginx`, с отдельным файлом в `/etc/portage/env/`. Для Apache аналогично: `acct-user/apache` и префикс `ACCT_USER_APACHE_`.[1][4]

| Переменная для nginx | Что делает |
| :--- | :--- |
| `ACCT_USER_NGINX_GROUPS` | Заменяет список групп; первая группа становится основной |
| `ACCT_USER_NGINX_GROUPS_ADD` | Добавляет группы, не заменяя стандартные; для дополнительных прав обычно нужен этот вариант |
| `ACCT_USER_NGINX_HOME` | Меняет путь домашнего каталога |
| `ACCT_USER_NGINX_HOME_OWNER` | Меняет владельца домашнего каталога |
| `ACCT_USER_NGINX_HOME_PERMS` | Меняет права домашнего каталога |
| `ACCT_USER_NGINX_SHELL` | Меняет оболочку; интерактивная оболочка для обычного nginx не нужна |

Список групп задаётся через пробелы. Прежде чем добавлять группу, проверь, что она существует и что службе действительно нужен доступ ко всем ресурсам, защищённым этой группой.[4]

<details>
<summary>Пример: сохранить дополнительную группу только для nginx</summary>

Строка в `/etc/portage/package.env` (или файле в этом каталоге, если используется раздельная конфигурация):

```text
acct-user/nginx nginx-account.conf
```

Содержимое `/etc/portage/env/nginx-account.conf`; замени `backend-socket` на имя существующей группы:

```bash
ACCT_USER_NGINX_GROUPS_ADD="backend-socket"
```

Посмотреть текущую запись и группы, затем проверить, что Portage видит пакет:

```bash
getent passwd nginx
id nginx
emerge --pretend --verbose acct-user/nginx
```

`--pretend` не применяет настройки. При переносе старой ручной настройки задай переменные до обновления пакета учётной записи, а после его установки проверь группы через `id nginx`. Если менялось членство в группах, проверь доступ уже у новых рабочих процессов после перезапуска службы в удобное окно.

</details>

## 2025: изменение упаковки nginx

Изменения вошли в Gentoo mainline начиная с **1.29.0**. Для стабильной ветки в объявлении названа дата **5 сентября 2025 года**. Это изменения пакетов Gentoo, а не универсальная инструкция для Debian, Arch или Entware.[2]

### Сторонние модули

Lua, Brotli, headers-more и upload-progress теперь устанавливаются отдельными пакетами из `www-nginx/`, а не включаются флагом основного пакета. Например, вместо старого `nginx_modules_http_lua` используется `www-nginx/ngx-lua-module`. Установка пакета не гарантирует загрузку модуля: следуй сообщению Portage — в зависимости от пакета это `load_module` в главном контексте или ссылка из `modules-enabled/` на конфиг в `modules-available/`. При старом `nginx.conf` проверь наличие `include modules-enabled/*.conf;` в главном контексте и не загружай один модуль обоими способами.[2][5][6]

При первоначальной переупаковке не перенесли `cache_purge`, `slowfs_cache`, `auth_pam`, `upstream_check`, `ngx_metrics`, Naxsi, RTMP, push-stream, sticky, MogileFS и auth-ldap. **Это исторический список, а не перечень того, чего сейчас нет:** в каталоге уже есть, например, `www-nginx/ngx-cache-purge`, `www-nginx/ngx-authpam`, `www-nginx/ngx-naxsi`, `www-nginx/ngx-rtmp`, `www-nginx/ngx-push-stream` и `www-nginx/ngx-auth-ldap`. Наличие в дереве ещё не означает доступность для твоей архитектуры и ключевых слов; окончательный ответ даёт `emerge --pretend` для конкретного пакета.[2][5]

<details>
<summary>Посмотреть модули в дереве, установленные модули и план установки Lua</summary>

```bash
emerge --search @www-nginx
qlist --installed www-nginx/
emerge --pretend --verbose www-nginx/ngx-lua-module
```

У `qlist` флаг `--tree` переключает источник на дерево доступных пакетов. Для списка **установленных** модулей его не добавляй; для списка пакетов **в дереве** подходит `qlist --installed --tree www-nginx/` (здесь `--installed` задаёт вывод имён вместо файлов).

</details>

### USE-флаги

| Было | Стало |
| :--- | :--- |
| `http2`, `http3` | `nginx_modules_http_v2`, `nginx_modules_http_v3`, или `NGINX_MODULES_HTTP: v2 v3` в `package.use` |
| Общий `ssl` | Отдельные `ssl` в `NGINX_MODULES_HTTP`, `NGINX_MODULES_STREAM`, `NGINX_MODULES_MAIL`; модули TLS по умолчанию включены |
| `threads` | Поддержка пулов потоков компилируется всегда; это не означает, что конкретная директива автоматически начинает ими пользоваться |
| `http-cache`, `ktls`, `pcre`, `pcre-jit` | Старые флаги удалены; их не нужно переносить как есть |
| `app-vim/nginx-syntax` | Синтаксис Vim теперь поставляет `www-servers/nginx` |

Изменения относятся к сборке. Например, `v3` добавляет поддержку HTTP/3 в бинарник, но сам по себе не включает QUIC на сервере: это настраивается в `nginx.conf` и требует доступа по UDP на выбранный порт.[2]

<details>
<summary>Пример package.use: HTTP/2 и HTTP/3</summary>

Открой `/etc/portage/package.use/nginx.use` (если `package.use` — каталог) или сам `/etc/portage/package.use` (если это файл). Обнови существующую запись вместо многократного добавления новых строк:

```text
www-servers/nginx NGINX_MODULES_HTTP: v2 v3
```

Для одного протокола оставь только `v2` или `v3`. Не отключай `ssl` ради миграции: если политика сборки действительно требует убрать TLS из всех трёх подсистем, в той же записи используются `NGINX_MODULES_HTTP: -ssl NGINX_MODULES_STREAM: -ssl NGINX_MODULES_MAIL: -ssl`.[2]

</details>

### Журналы и порядок обновления

По умолчанию `/var/log/nginx/error_log` и `access_log` стали `/var/log/nginx/error.log` и `access.log`. Пакетный конфиг `logrotate` обновлён; при явных `error_log` или `access_log` в собственном конфиге nginx продолжит использовать заданные там пути. Проверь, что с фактическими путями совпадают настройки ротации, сборщика логов, агента мониторинга и скриптов.[2]

1. Сохрани копию `/etc/nginx` и затронутых настроек Portage и ротации. Проверь нужные USE-флаги и список сторонних модулей до обновления; заранее реши, что делать с директивами модуля, для которого нет доступного пакета.[2][5]
2. Посмотри план Portage. Убери `app-vim/nginx-syntax` из `world` только если его добавляли явно: `--deselect` не удаляет установленный пакет. Установи нужные модули, объедини защищённые обновления конфигов (например, через `dispatch-conf`) и проверь, как подключаются новые модули.[2][6]
3. Запусти `nginx -t` до любого reload/restart. Если менялись бинарник, динамические модули вместе с ним или группы службы, запланируй перезапуск OpenRC; reload перечитывает конфиг, но его не стоит считать заменой перезапуска после обновления бинарника. После проверь ответ сайта и появление записей в ожидаемых журналах.

<details>
<summary>Команды обновления: предпросмотр отдельно от применения</summary>

Предпросмотр не меняет установленные пакеты:

```bash
emerge --pretend --verbose --update --deep www-servers/nginx
```

Команды ниже требуют прав администратора и меняют систему. Первую строку выполни только если `app-vim/nginx-syntax` был явно выбран, третью — только если нужен Lua:

```bash
emerge --deselect app-vim/nginx-syntax
emerge --oneshot --update --deep www-servers/nginx
emerge www-nginx/ngx-lua-module
```

После объединения конфигов проверь их; команда справа выполняется только после успешного теста. Перезапуск может прервать соединения:

```bash
nginx -t && rc-service nginx restart
```

</details>

## Sources

[1] https://raw.githubusercontent.com/gentoo/gentoo-news/master/2022-05-26-apache-nginx-glep-81/2022-05-26-apache-nginx-glep-81.en.txt
[2] https://www.gentoo.org/support/news-items/2025-07-05-nginx-packaging-changes.html
[3] https://www.gentoo.org/glep/glep-0081.html
[4] https://devmanual.gentoo.org/eclass-reference/acct-user.eclass/index.html
[5] https://packages.gentoo.org/categories/www-nginx
[6] https://devmanual.gentoo.org/eclass-reference/nginx-module.eclass/index.html

#nginx #Gentoo #Portage #WebServer
