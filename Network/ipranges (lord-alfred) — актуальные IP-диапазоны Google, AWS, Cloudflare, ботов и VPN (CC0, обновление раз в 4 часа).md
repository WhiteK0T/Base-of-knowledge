---
создал заметку: 2026-09-21T01:05:00
author: WhiteK0T
tags:
  - Network
  - Firewall
  - Iptables
  - Nftables
  - Ipset
  - Bots
  - OpenSource
Источник:
  - https://t.me/open_source_friend/5825
  - https://github.com/lord-alfred/ipranges
---

# 🌐 ipranges — готовые списки IP-диапазонов Google, AWS, Cloudflare, ботов и VPN

**ipranges** ([github.com/lord-alfred/ipranges](https://github.com/lord-alfred/ipranges), автор **Lord_Alfred**, **CC0-1.0**, ~1.2k★ / 165 форков, живёт с 07.2021) — это **не программа, а репозиторий-датасет**: простые `.txt` со списками CIDR по каждому крупному провайдеру и поисковому/AI-боту, которые пересобирает GitHub Actions. Тебе не надо ничего ставить — нужен один `curl` за нужным файлом.

Практический смысл: не держать у себя парсер под каждый облачный API (у Google — SPF-записи в DNS + два JSON, у Telegram — свой `cidr.txt`, у AWS — свой формат), а взять уже нормализованный список и скормить его `nft`/`ipset`/nginx.

> [!warning] Факты против пересказа в посте
> | Заявление поста | Как на самом деле |
> | :--- | :--- |
> | «инструмент», «программа поддерживает…» | локально запускать нечего: это **набор текстовых файлов** + по `downloader.sh` на каждый источник, которые гоняет CI. Клонировать ради «запустить» смысла нет |
> | «ежедневные обновления» | в workflow стоит `cron: '8 */4 * * *'` — **каждые 4 часа**, 6 запусков в сутки (коммитов реально ~3–6 в день; последний на момент заметки — **20.09.2026**). Даже README проекта пишет «daily», хотя расписание давно чаще |
> | «Google, Bing, Amazon, Microsoft, Oracle, GitHub, OpenAI и других» | «другие» — это ещё **половина списка**: Cloudflare, DigitalOcean, Linode, Vultr, Telegram, Twitter, Facebook, Apple Private Relay, ProtonVPN, Perplexity, DuckDuckBot, DuckAssistBot, Pingdom, StatusCake, отдельно GoogleBot. Итого **22 набора + сводный `all/`** |
> | «Lang: Shell» | наполовину: `downloader.sh` — bash (`curl`, `dig`, `jq`, `awk`), а свёртка диапазонов — **Python 3.13 + netaddr** (`utils/merge.py`); в CI ещё `whois`, `parallel`, `gawk` |
> | про лицензию молчок | **CC0-1.0** — по сути public domain: списки можно тащить в свой продукт без оглядки (приятный контраст с типичным «репо без лицензии») |

## 📦 Что внутри

На каждый источник — своя папка с 3–5 файлами:

| Файл | Что это |
| :--- | :--- |
| `downloader.sh` | bash-парсер первоисточника (например, `google/` тянет `gstatic.com/ipranges/goog.txt`, `cloud.json`, `googlebot.json` **и** рекурсивно разворачивает SPF-записи `_netblocks*.google.com` через `dig`) |
| `ipv4.txt` / `ipv6.txt` | сырой результат парсинга: всё подряд, с пересечениями и дублями |
| `ipv4_merged.txt` / `ipv6_merged.txt` | то же, схлопнутое в **минимальный непересекающийся набор CIDR** (`netaddr.cidr_merge`) |

> [!tip] Всегда бери `_merged`
> Разница не косметическая. Замерил на 21.09.2026:
>
> | Набор | Строк |
> | :--- | ---: |
> | `all/ipv4.txt` (сырой) | **112 413** |
> | `all/ipv4_merged.txt` | **7 723** (×14,5 меньше) |
> | `all/ipv6_merged.txt` | 13 132 |
> | `apple-proxy/ipv4_merged.txt` | 3 291 |
> | `amazon/ipv4_merged.txt` | 1 739 |
> | `protonvpn/ipv4_merged.txt` | 672 |
> | `microsoft/ipv4_merged.txt` | 457 |
> | `openai/ipv4_merged.txt` | 253 |
> | `google/ipv4_merged.txt` | 97 |
> | `googlebot/ipv4_merged.txt` | 41 |
> | `cloudflare/ipv4_merged.txt` | 15 |
> | `telegram/ipv4_merged.txt` | 7 |
>
> Сырой `ipv4.txt` содержит пересекающиеся сети — `nft ... flags interval` без `auto-merge` на таком просто откажется добавлять элементы, а `ipset` раздуется. `_merged` уже дедуплицирован и отсортирован.

Часть источников — только IPv4 (Bing, Oracle, OpenAI, Perplexity, ProtonVPN, StatusCake, DuckDuckBot/DuckAssistBot): у первоисточников IPv6 там просто нет.

## 🛠️ Как применять

### nftables (Gentoo / Debian-Ubuntu / Arch)

Именованный set, который наполняется из файла и обновляется без перезагрузки правил:

```nft
# /etc/nftables.conf
table inet filter {
	set ai_bots_v4 {
		type ipv4_addr
		flags interval
		auto-merge
	}
	chain input {
		type filter hook input priority filter; policy accept;
		ip saddr @ai_bots_v4 counter drop
	}
}
```

Скрипт обновления (`/usr/local/sbin/update-ipranges.sh`):

```bash
#!/bin/bash
set -euo pipefail
BASE="https://raw.githubusercontent.com/lord-alfred/ipranges/main"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

curl -fsS --retry 3 "$BASE/openai/ipv4_merged.txt" -o "$TMP"
grep -qE '^[0-9]+\.' "$TMP"                      # sanity-check: не пустой и похоже на CIDR

nft flush set inet filter ai_bots_v4
nft add element inet filter ai_bots_v4 "{ $(paste -sd, "$TMP") }"
```

Запуск по расписанию:

- **Gentoo (OpenRC)** — cron: `crontab -e` → `17 */6 * * * /usr/local/sbin/update-ipranges.sh` (плюс `rc-update add nftables default`, чтобы сеты поднимались при загрузке).
- **Debian/Ubuntu, Arch (systemd)** — `systemd-timer`: юнит `update-ipranges.service` (`Type=oneshot`) + `update-ipranges.timer` c `OnCalendar=*-*-* 03,09,15,21:17:00` и `Persistent=true`.

### ipset + iptables (Entware / ASUS RT-AX56U)

Состав репозитория `armv7sf-k3.2` проверил: **`ipset` 7.24 и `iptables` есть, `nftables` нет** (только `libnftnl`) — на роутере путь один, через ipset:

```sh
opkg install ipset iptables curl ca-certificates

ipset create tg_v4 hash:net family inet maxelem 65536 -exist
curl -fsS https://raw.githubusercontent.com/lord-alfred/ipranges/main/telegram/ipv4_merged.txt \
  | sed 's/^/add tg_v4 /' | ipset restore -exist

iptables -t mangle -I PREROUTING -m set --match-set tg_v4 dst -j MARK --set-mark 0x2
```

- **`maxelem`**: дефолт у `hash:net` — 65536, для `_merged`-наборов хватает с запасом; а вот сырой `all/ipv4.txt` (112 тыс.) в него **не влезет** — понадобится `maxelem 262144` и заметно больше RAM.
- Обновление — `cron` из Entware (`/opt/etc/init.d/S10cron`), скрипт складывать на USB, а не во flash.
- Типовой сценарий на роутере — не блокировка, а **policy-based routing**: пометить трафик к диапазонам Telegram/Cloudflare и увести его в туннель.

### nginx — белый список (пускать только Cloudflare)

```bash
curl -fsS https://raw.githubusercontent.com/lord-alfred/ipranges/main/cloudflare/ipv4_merged.txt \
  | sed 's/^/allow /; s/$/;/' > /etc/nginx/cloudflare.conf
# в server{}: include /etc/nginx/cloudflare.conf; deny all;
```
15 строк, обновлять раз в сутки — типовая защита origin-сервера от захода в обход CDN.

## ⚠️ Грабли

> [!danger] `all/` — это НЕ блоклист
> В сводный набор входят Google, AWS, Microsoft, Cloudflare, GitHub, Telegram. Повесишь `drop` на `all/ipv4_merged.txt` — отрежешь себе обновления пакетов, CDN половины сайтов, GitHub и заодно собственные сервисы, если они в облаке. `all/` нужен для другого: **отличить «трафик из ЦОД» от «трафик домашнего пользователя»** (антифрод, скоринг регистраций, «этот заход — точно бот или VPN»).

> [!caution] Задержка и свежесть
> Между изменением у провайдера и файлом в репозитории — **до 4 часов** (расписание CI) плюс кэш CDN GitHub. Для белых списков и роутинга нормально; для строгого фильтра доступа к критичному сервису диапазоны лучше тянуть **из первоисточника** (`cloud.json` у Google, `ip-ranges.json` у AWS), а ipranges держать как удобный агрегат.

> [!note] Блокировка AI-краулеров по IP работает только против честных
> `openai/`, `perplexity/`, `duckassistbot/` закрывают тех, кто ходит со **своих объявленных адресов** и уважает правила. Серый скрапинг идёт через резидентные прокси и в этих списках не появится никогда. IP-фильтр — дополнение к `robots.txt` и rate-limit, а не замена.

> [!tip] Доступ из РФ и вес репозитория
> `raw.githubusercontent.com` из российских сетей часто не открывается. Рабочие обходы без VPN:
> - зеркало jsDelivr (проверил — отдаёт те же файлы, `200`):
>   `https://cdn.jsdelivr.net/gh/lord-alfred/ipranges@main/telegram/ipv4_merged.txt`
> - `git clone --depth 1 https://github.com/lord-alfred/ipranges` — **обязательно `--depth 1`**: полная история это коммит каждые 4 часа с 2021 года, ~40 МБ упакованных объектов ради 8 тысяч строк текста.

> [!note] Проверка ботов: список ≠ доказательство
> Для «пускать Googlebot» связка правильная: репо парсит **официальный** `googlebot.json` от Google. Но если решение важное (доступ к закрытому контенту, отдача другого HTML), надёжнее классика — **reverse DNS + forward-подтверждение** на `googlebot.com`/`google.com`: IP-список стареет между запусками CI, PTR — нет.

## 🖥️ Применимость на системах владельца

| Система | Как | Нюанс |
| :--- | :--- | :--- |
| **Gentoo** | `nft` + named set, обновление по cron (OpenRC) | `emerge net-firewall/nftables`, `rc-update add nftables default` |
| **Debian / Ubuntu** | то же + `systemd-timer` | `apt install nftables`; если жив старый `iptables-legacy` — можно через `ipset` |
| **Arch** | то же, `pacman -S nftables` | systemd-таймер один в один с Debian |
| **Entware / RT-AX56U** | только `ipset` + `iptables` | `nftables` в репозитории **нет**; брать `_merged`, скрипт и cron держать на USB, во flash не писать |

## 🔗 Связанные заметки

- База по фильтрации пакетов: [IPTables](IPTables.md)
- Блокировка на уровне DNS, а не IP (реклама/трекеры/malware): [1Hosts](1Hosts%20%E2%80%94%20DNS-%D0%B1%D0%BB%D0%BE%D0%BA%D0%BB%D0%B8%D1%81%D1%82%D1%8B%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%20%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D1%8B%2C%20%D1%82%D1%80%D0%B5%D0%BA%D0%B5%D1%80%D0%BE%D0%B2%20%D0%B8%20malware%20%28Lite-Xtra%2C%20Pi-hole-AdGuard%20Home%29.md)
- Железо, на котором это крутить: [ASUS RT-AX56U и Asuswrt-Merlin](Routers/ASUS%20RT-AX56U%20%D0%B8%20Asuswrt-Merlin%20%E2%80%94%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%BE%D0%BD%D1%87%D0%B8%D0%BB%D0%B8%D1%81%D1%8C%20%D0%BD%D0%B0%203004.388.8_4%20%28%D1%82%D0%BE%D1%87%D0%BD%D0%B0%D1%8F%20%D0%BF%D1%80%D0%B8%D1%87%D0%B8%D0%BD%D0%B0%2C%20Entware%2C%20%D1%81%D0%B0%D0%BC%D0%BE%D1%81%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%2C%20%D1%81%D1%82%D0%BE%D0%BA%20ASUS%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/lord-alfred/ipranges](https://github.com/lord-alfred/ipranges) (**CC0-1.0**) · автор: [@Lord_Alfred](https://t.me/Lord_Alfred)
- Сводные файлы: [`all/ipv4_merged.txt`](https://raw.githubusercontent.com/lord-alfred/ipranges/main/all/ipv4_merged.txt) · [`all/ipv6_merged.txt`](https://raw.githubusercontent.com/lord-alfred/ipranges/main/all/ipv6_merged.txt)
- Первоисточники для сверки: [Google Cloud IP](https://www.gstatic.com/ipranges/cloud.json) · [GoogleBot](https://developers.google.com/search/apis/ipranges/googlebot.json) · [Telegram CIDR](https://core.telegram.org/resources/cidr.txt)
- Соседние датасеты (из README проекта): [Tor exit nodes](https://github.com/SecOps-Institute/Tor-IP-Addresses) · [Spamhaus](https://github.com/SecOps-Institute/SpamhausIPLists) · [Akamai](https://github.com/SecOps-Institute/Akamai-ASN-and-IPs-List)
- Источник новости: пост от **29.07.2026** в [@open_source_friend](https://t.me/open_source_friend/5825)

#Network #Firewall #Iptables #Nftables #Ipset #Bots #OpenSource
