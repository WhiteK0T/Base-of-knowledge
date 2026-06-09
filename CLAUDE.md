# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is an **Obsidian knowledge-base vault**, not a software project. It is a personal "second brain" of Markdown notes, written primarily in **Russian**. There is no build, lint, or test step — changes are made by editing/creating `.md` files. Obsidian reads the vault directly; the `.obsidian/` directory holds app config and plugins.

When asked to "add a note" or "document X", create or edit a Markdown file following the conventions below. Match the existing language of the surrounding notes (Russian for content; code/commands stay as-is).

## Layout

Top-level folders group notes by domain, e.g. `AI/`, `VCS/`, `Network/`, `Linux/`, `Programming/`, `Health/`, `Education/`, `Windows/`, `Drones/`, `Apps/`. Each domain is further nested by topic (`Linux/Package-Manager/`, `Programming/Java/JCF/`, `VCS/GitHub/`, etc.). Two special folders:

- `Templates/` — note skeletons inserted by Obsidian's Templates plugin (`Book`, `Course`, `Daily`, `Default`, `Planner`, `Reference`).
- `Cache/` — the **attachment folder** (`app.json: attachmentFolderPath = "Cache"`). All images/binaries live here, mirroring the note's path (e.g. images for `Network/IPTables.md` live in `Cache/Netfilter/`).

## Note conventions

Every content note starts with YAML frontmatter. The shared fields seen across the vault:

```yaml
---
создал заметку: 2025-09-28T01:07:00   # "created note" — ISO datetime; templates use {{date}} (YYYY-MM-DD)
author: WhiteK0T
tags:
  - APT
  - Linux
Источник:                              # "Source" — optional list of reference URLs
  - https://example.com
---
```

- **Tags** are declared in frontmatter and frequently *also* repeated as inline `#tag` lines at the bottom of the note. Tags are managed via the `tag-wrangler` plugin — keep tag names consistent (e.g. `#Пакетный_Менеджер`).
- **Internal links** use Obsidian wiki/Markdown link syntax to other notes, often by filename only: `[dpkg](DPKG.md)`. `app.json` has `alwaysUpdateLinks: true`, so renaming/moving a note via Obsidian fixes links — but when editing raw files, update links by hand.
- **Image embeds** reference files under `Cache/`. Both relative (`![alt](../../Cache/Netfilter/iptables-chain.jpg)`) and vault-absolute (`![](/Cache/JCF/.../example.png)`) forms appear; prefer the style already used in the file you are editing.
- Templates store the creation date via the `{{date}}` placeholder (format `YYYY-MM-DD`, configured in `.obsidian/templates.json`).

## Target systems (platform coverage)

The vault owner runs (and asks notes to support) **four systems on a permanent basis**. Whenever a note involves installation, packages, services, or other OS-specific setup, **cover all relevant platforms below** with their native tooling — don't write a note that only works on one distro:

| Система | Менеджер пакетов / приём | Службы | Примечания |
| :--- | :--- | :--- | :--- |
| **Gentoo** (основная) | Portage: `emerge`, USE-флаги в `/etc/portage/package.use/`, маски | **OpenRC** (`rc-update`, `rc-service`; `/etc/conf.d/*`) | главный «рабочий» дистрибутив владельца |
| **Debian / Ubuntu** | `apt` / `dpkg`, официальные PPA | systemd | папка заметок `Linux/Debian-Ubuntu/` |
| **Arch** | `pacman`, AUR (`yay`/`paru`) | systemd | владелец **собирается пробовать в ближайшее время** (с июня 2026) — давай рабочие инструкции |
| **Entware** | `opkg` на роутерах/embedded | init-скрипты Entware / `/opt/etc/init.d/` | ARM (`armv7`/`aarch64`), **урезанный репозиторий**: тяжёлых десктоп-пакетов (Qt и т.п.) часто нет → предлагай лёгкие аналоги. Конкретное железо владельца: **ASUS RT-AX56U** (BCM6755 armv7, 512 МБ RAM, 256 МБ flash) с уже настроенными Entware + USB-диском |

Guidance: if a platform is genuinely irrelevant to a note, it may be omitted, but prefer covering those that apply. For Entware always sanity-check that the package actually exists for the router's ARM arch before recommending it (the repo is much smaller than a desktop distro's).

## Plugins in use

Community plugins (`.obsidian/community-plugins.json`): `dataview`, `tag-wrangler`, plus `calendar` and `obsidian-kanban` present under `.obsidian/plugins/`. `Dataview` means some notes may contain `dataview` query blocks that render from frontmatter fields — preserve frontmatter field names so those queries keep working. `Obsidian Base Settings.md` documents the broader intended plugin/setup list.
