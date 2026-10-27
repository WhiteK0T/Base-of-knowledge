# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is an **Obsidian knowledge-base vault**, not a software project. It is a personal "second brain" of Markdown notes, written primarily in **Russian**. There is no build, lint, or test step — changes are made by editing/creating `.md` files. Obsidian reads the vault directly; the `.obsidian/` directory holds app config and plugins.

When asked to "add a note" or "document X", create or edit a Markdown file following the conventions below. Match the existing language of the surrounding notes (Russian for content; code/commands stay as-is).

**Talk to the owner in Russian** — summaries, questions and reports in chat; code, commands, paths and file names stay as they are.

**Notes are viewed in two places — Obsidian and GitHub** (the repository is public). Every note must render correctly in both: plain relative Markdown links, no hand-made TOC, collapsible blocks via `<details>` (see the conventions below).

## Layout

Top-level folders group notes by domain, e.g. `AI/`, `VCS/`, `Network/`, `Linux/`, `Programming/`, `Security/`, `Pentest/`, `Health/`, `Education/`, `Windows/`, `Drones/`, `Apps/`, `Tools/`. Each domain is further nested by topic (`Linux/Package-Manager/`, `Programming/Java/JCF/`, `VCS/GitHub/`, etc.).

**`Pentest/` vs `Security/`:** **offensive** tooling lives in `Pentest/`, split by area — `Pentest/Web/`, `Pentest/Windows-AD/`, `Pentest/Wireless/`, `Pentest/Recon/` (OSINT), `Pentest/Social-Engineering/`, `Pentest/Frameworks/`. `Security/` keeps CVE writeups (`Security/Vulns/`), forensics, radio/SDR, privacy and **defensive** tools. New offensive-tool notes go under `Pentest/<area>`; CVE research and defensive/privacy notes stay in `Security/`.

**Where other topics go:**

| Topic | Folder | Notes |
| :--- | :--- | :--- |
| Containers (Docker, runc, containerd, LXC, podman, namespaces/cgroups/OverlayFS) | `Linux/Containers/` | images in `Cache/Containers/`; container CVEs still go to `Security/Vulns/` |
| Remote-desktop / remote-support apps (RustDesk, AnyDesk, TeamViewer, ScreenConnect) | `Apps/Remote-Access/` | the owner's own deployment of such tools is a private note — see below |
| Git, forges, CI, trackers | `VCS/Git/`, `VCS/GitHub/`, `VCS/GitLab/`, `VCS/Forgejo-Gitea/`, `VCS/CI/`, `VCS/Trackers/` (incl. the `Jira/` series) | a forge's own issues/CI features go to that forge's folder; README section «🔧 VCS и трекеры» |
| Big skill collections | `AI/Skills/<author>/` (`addyosmani/`, `mattpocock/`, `pstack/`) | single skills from other authors stay flat in `AI/Skills/` |
| AI skills / MCP for reverse engineering | `Security/Reverse-Engineering/AI/` | classic RE tools one level up; README bullet goes in the «Реверс-инжиниринг / RE» line, not «Skills». Web-API reverse tools that generate clients stay in `AI/Agents/Tooling/` with a cross-link |
| Temporary files that must sit inside the project | `temp/` | ignored by git as a whole (`/temp/`); not present after a fresh clone — `mkdir temp` |

When a note moves one level deeper or elsewhere, fix the relative links inside it and every link pointing to it (README, sibling notes, Education notes).

**`Linux/Commands/` naming rule:** every note's filename is **exactly the system command name**, in its real case, plus `.md` — `rm.md`, `mv.md`, `lsof.md`, `curl.md`, `scp.md`. No descriptions, dashes or parentheses in the filename (this keeps quick-search by command instant). The descriptive title goes into the note's `# H1` and into the note's bullet in `README.md`. When adding a note there or renaming one, update every link to it by hand (percent-encode if needed).

**`Tools/` — vault tooling, not notes about tools:** scripts that *produce material for the vault itself* (poster/image/cheatsheet generators and similar helpers). One subfolder per tool: the script plus a `README.md` note (normal frontmatter, Russian) explaining what it builds, how to run it and its dependencies per platform. Generated output still goes to `Cache/`, mirroring the note it belongs to. Downloaded assets (fonts etc.) are cached outside the repo, never committed. Notes *about* third-party tools stay in their topic domains (`Apps/`, `AI/`, …).

- `Tools/claude-code-poster/poster.py` builds `Cache/Claude-Code/claude-code-cheatsheet-2560x1440.png` for `AI/Agents/Claude Code — шпаргалка команд.md`. Its design copies the original cheatsheet from https://t.me/bugnotfeature/27215 (header/body colors sampled from it). When the cheatsheet note changes, update `BLOCKS` in the script and regenerate the poster with it instead of drawing a new one by hand.
- `Tools/codex-cli-poster/poster.py` builds `Cache/Codex-CLI/codex-cli-cheatsheet-2560x1440.png` for `AI/Agents/Codex CLI — шпаргалка команд.md` with the same engine and design as claude-code-poster (blue `EXP` badge marks experimental/beta items). When the Codex cheatsheet changes, update `BLOCKS` there and regenerate.

Two special folders:

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
- **Internal links** are plain **Markdown links with relative paths**, not `[[wikilinks]]` — GitHub doesn't render wikilinks. Percent-encode spaces and non-ASCII (`[SCP](../../Commands/SCP.md)`, `SSH-Продвинутое%20руководство.md` → `%20` etc.). `app.json` has `alwaysUpdateLinks: true`, so renaming/moving a note via Obsidian fixes links — but when editing raw files, update links by hand.
- **No hand-made table of contents.** GitHub (kebab-case anchors) and Obsidian (literal heading text) use incompatible anchor schemes; rely on GitHub's ☰ outline and Obsidian's Outline panel.
- **Image embeds** reference files under `Cache/`. Both relative (`![alt](../../Cache/Netfilter/iptables-chain.jpg)`) and vault-absolute (`![](/Cache/JCF/.../example.png)`) forms appear; prefer the style already used in the file you are editing. Prefer your own summary plus a mermaid diagram over copying an article together with its pictures.
- Templates store the creation date via the `{{date}}` placeholder (format `YYYY-MM-DD`, configured in `.obsidian/templates.json`).

### Writing style for notes based on posts

- **Constructive, no debunking.** No "claim → ❌ verdict" tables and no «проверка — …» / «факты против хайпа» in the H1, the file name or the README bullet. Where a post is wrong or exaggerates, simply write the correct, verified facts (a short «уточнение» is fine). Fact-checking itself stays (clone, API, code); only the presentation changes. Legal and security warnings that matter are not debunking — keep them.
- **Weak or duplicate material:** if the post is thin or the vault already has a better note, prepare the note but **ask the owner before committing** (and offer to extend the existing note instead).

### Video notes

For notes summarizing a video or talk:
- `Источник`: the video URL first, then the channel URL, then other references — **never** a local file path.
- First paragraph: the video title linked to the video, the channel name linked to the channel; if the owner gives a local copy, add `([локальная копия](file:///…))` after the date/duration.
- «🔗 Ссылки» section: `- Видео: <url>`, `- Канал «…»: <url>`, and, only if a local copy exists, `- Локальная копия видео: [<plain path>](file://<percent-encoded path>)` (encode with `urllib.parse.quote(path, safe='/')`).
- Ask for the video/channel URLs if unknown rather than guessing.

### Code examples

When a note contains code examples, write them in **Java first (primary, most polished)**, then **Python, JavaScript, Go, Rust, Bash** — skip a language only when it genuinely can't be done, and say so next to the example. Keep the same behaviour across languages so the versions can be compared.

- Hide every example (code, JSON, curl) in `<details><summary>…</summary>` with a blank line after `<summary>`.
- **Run every version before committing** — a scripted fake server or a stub binary is a cheap way to test without real credentials. Build the note from a template that pulls in the tested files, then extract the code from the built note and run the tests again.
- Environment variables in examples must not start with `CLAUDE_` (Claude Code sets e.g. `CLAUDE_EFFORT`, which silently overrides defaults).

## Private and encrypted content

- **`Network/Tunnels/**` is git-crypt encrypted** (`.gitattributes`). Notes there reach GitHub as ciphertext and don't render, so **never add README bullets** for them. Before pushing, check that the file really is encrypted: `git-crypt status <file>` → `encrypted`, and the staged blob starts with `\0GITCRYPT\0` (`git cat-file -p :<path> | head -c 16 | od -c`). git-crypt does not hide file names or commit messages.
- **Notes about the owner's real infrastructure** (hosts, IPs, open ports and services, remote-access setup, keys, configs) **never go to GitHub.** Leave the note where it is, add **one exact-path line** (with a leading `/`) to `.gitignore`, verify with `git check-ignore -v <file>`. Don't use git-crypt for these. Never copy real IPs/hostnames/keys into public notes — use placeholders such as `<IP-VPS>`; a sanitized general note can be written separately.
- While such a private file sits in the tree, stage **explicit files**, not `git add -A`, and check `git status` before committing.

## Target systems (platform coverage)

The vault owner runs (and asks notes to support) **four systems on a permanent basis**. Whenever a note involves installation, packages, services, or other OS-specific setup, **cover all relevant platforms below** with their native tooling — don't write a note that only works on one distro:

| Система | Менеджер пакетов / приём | Службы | Примечания |
| :--- | :--- | :--- | :--- |
| **Gentoo** (основная) | Portage: `emerge`, USE-флаги в `/etc/portage/package.use/`, маски | **OpenRC** (`rc-update`, `rc-service`; `/etc/conf.d/*`) | главный «рабочий» дистрибутив владельца |
| **Debian / Ubuntu** | `apt` / `dpkg`, официальные PPA | systemd | папка заметок `Linux/Debian-Ubuntu/` |
| **Arch** | `pacman`, AUR (`yay`/`paru`) | systemd | владелец **собирается пробовать в ближайшее время** (с июня 2026) — давай рабочие инструкции |
| **Entware** | `opkg` на роутерах/embedded | init-скрипты Entware / `/opt/etc/init.d/` | ARM (`armv7`/`aarch64`), **урезанный репозиторий**: тяжёлых десктоп-пакетов (Qt и т.п.) часто нет → предлагай лёгкие аналоги. Конкретное железо владельца: **ASUS RT-AX56U** (BCM6755 armv7, 512 МБ RAM, 256 МБ flash) с уже настроенными Entware + USB-диском — установку Entware и USB заново не объяснять |

Guidance: if a platform is genuinely irrelevant to a note, it may be omitted, but prefer covering those that apply. For Entware always sanity-check that the package actually exists for the router's ARM arch before recommending it (the repo is much smaller than a desktop distro's).

**Checking Entware packages.** The router's main feed is `https://bin.entware.net/armv7sf-k3.2/` (some packages, e.g. `nginx` and `amneziawg-*`, come from an extra feed in `/opt/etc/opkg.conf`). Entware renames packages with suffixes, so an exact-name grep gives **false "not available" claims**:

| Searched | Real name |
| :--- | :--- |
| `unbound` | `unbound-daemon` (+ `-control`, `-anchor`, `-checkconf`, `-host`) |
| `nginx` | `nginx-ssl` (+ `nginx-mod-*`) |
| `sing-box` | `sing-box-go` |
| `wget` | `wget-ssl` |

`-daemon` = the service itself, `-ssl` = TLS build, `-go` = Go build, `_nohf` = no-hard-float variant (for `armv7sf` take the plain one). Before writing that a package is unavailable, grep the feed's `Packages` **by substring** (`grep -i '^Package:.*<stem>'`). The same rule applies to the AUR and to Gentoo package names (also check overlays such as `gentoo-zh`, `guru`).

## Git workflow

- The repo's git identity is set in the **local** repo config; never run `git config --global`.
- Commit messages carry **no `Co-Authored-By` trailer.**
- **One commit per note** when several notes are requested.
- After committing a note, **always `git pull --rebase` and `git push`** without asking. Don't push only when the owner says so («не коммить», «не пушь» — then commit only after an explicit command), when the request was a question rather than a note, or when the note is private (see above).
- `git pull --rebase` is needed because CI often adds a commit: the **note-count badge in `README.md` is generated by a GitHub Action** (`chore: update note count badge [skip ci]`). Never edit that badge line by hand and never include it in a commit.
- Pushing works only through the owner's forwarded SSH agent. If the agent is absent or the push is refused, commit locally, don't retry, and tell the owner to reconnect and push.
- When adding a note, add its bullet to the matching category of the `README.md` catalogue (except encrypted `Network/Tunnels/**` notes).

## Plugins in use

Community plugins (`.obsidian/community-plugins.json`): `dataview`, `tag-wrangler`, plus `calendar` and `obsidian-kanban` present under `.obsidian/plugins/`. `Dataview` means some notes may contain `dataview` query blocks that render from frontmatter fields — preserve frontmatter field names so those queries keep working. `Obsidian Base Settings.md` documents the broader intended plugin/setup list.
