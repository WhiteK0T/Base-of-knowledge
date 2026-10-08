---
создал заметку: 2026-10-09T00:30:00
author: WhiteK0T
tags:
  - GitHub
  - GitHub_Actions
  - Git
  - Релизы
  - SemVer
  - Changelog
Источник:
  - https://github.com/googleapis/release-please
  - https://github.com/googleapis/release-please-action
  - https://github.com/semantic-release/semantic-release
  - https://www.conventionalcommits.org/ru/v1.0.0/
  - https://semver.org/lang/ru/
---

# Автоматизация релизов: release-please и semantic-release

> [!info] Задача
> Номер версии, тег, GitHub Release и запись в Changelog должны появляться **сами**, по сообщениям коммитов, без ручного `git tag` и правки версии в трёх местах. Оба популярных инструмента — **release-please** (Google) и **semantic-release** — читают коммиты в формате **Conventional Commits** и считают следующую версию по **SemVer**. Различаются они моментом выпуска: release-please выпускает **через PR**, который вы мержите, а semantic-release — **сразу**, на каждый пуш в ветку релизов.

Версии на момент проверки (2026-10-09): release-please **17.11.2**, `release-please-action` **v5** (с апреля 2026 работает на Node 24), semantic-release **25.0.9** (требует Node `^22.14` или `≥ 24.10`).

---

## 1. Основа: Conventional Commits → SemVer

Формат сообщения: `тип(область)!: описание`.

| Коммит | Пример | Версия `1.2.0` станет |
| :--- | :--- | :--- |
| `fix:` | `fix: harden temp dir cleanup` | **1.2.1** (PATCH) |
| `perf:` | `perf(fb3): lazy unpacking` | 1.2.1 (PATCH) |
| `feat:` | `feat: add --gui=wx\|sdl\|both` | **1.3.0** (MINOR) |
| `feat!:` / `fix!:` / `refactor!:` или строка `BREAKING CHANGE:` в теле | `feat!: drop Ubuntu 20.04` | **2.0.0** (MAJOR) |
| `docs:`, `chore:`, `ci:`, `test:`, `build:`, `style:`, `refactor:` | `docs: fix README` | **релиза нет**, коммит копится до следующего |
| Не по формату | `gentoo: bump app-misc/far2l to 2.9.1` | **игнорируется** обоими инструментами (у такого коммита нет известного типа) |

> [!note] До версии 1.0.0
> В обоих инструментах можно смягчить правила для `0.x`: release-please — опции `bump-minor-pre-major` (ломающее изменение повышает MINOR, а не MAJOR) и `bump-patch-for-minor-pre-major` (`feat` повышает PATCH).

Чтобы формат соблюдался, коммиты проверяют **commitlint** (хук `commit-msg` или проверка в CI) или помогают их писать через `commitizen` (`cz commit`).

---

## 2. release-please — релиз через PR

### Как работает

1. На каждый пуш в `main` Action читает коммиты с последнего релиза.
2. Если среди них есть «релизные» (`feat`, `fix`, `perf`, `revert`, ломающие), он **открывает или обновляет один PR** вида `chore(main): release 1.2.1`. В PR лежат новая запись Changelog и правка версии в файлах.
3. Пока PR открыт, новые коммиты **дописываются в него**: номер и Changelog пересчитываются.
4. Вы **мержите PR, когда решили выпускаться**. Следующий прогон ставит тег `v1.2.1` и создаёт GitHub Release с теми же заметками.

Плюс подхода: **человек сам решает, когда выпускать**, и видит Changelog до выпуска (его можно поправить прямо в PR). Минус: лишний PR, который висит постоянно.

### Минимальная настройка

`.github/workflows/release-please.yml`:
```yaml
name: release-please
on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v5
        with:
          release-type: simple          # проект без package.json: версия в version.txt
```

Плюс один раз в репозитории: **Settings → Actions → General → «Allow GitHub Actions to create and approve pull requests»**. Без этой галки PR не создаётся.

> [!warning] PR от `GITHUB_TOKEN` не запускает другие workflow
> Release-PR, созданный стандартным токеном, **не запускает ваши CI-проверки** (защита GitHub от рекурсии). Если на `main` требуются зелёные проверки, передайте Action **PAT** или токен GitHub App (`token: ${{ secrets.RELEASE_PLEASE_TOKEN }}`).

### `release-type` для разных проектов

`node` (package.json), `python` (pyproject/setup.py), `rust` (Cargo.toml), `go`, `java`/`maven`, `helm`, `dart`, `elixir`, `php`, `ruby` и др. Для shell-скриптов, конфигов и оверлеев подходит **`simple`**: версия хранится в `version.txt`, а Changelog — в `CHANGELOG.md`.

Версию можно обновлять **в любом файле**, например в самом скрипте. Для этого строку помечают аннотацией и перечисляют файл в `extra-files`:
```bash
VERSION="1.2.0" # x-release-please-version
```

### Конфиг через манифест (рекомендуемый способ)

`release-please-config.json`:
```json
{
  "release-type": "simple",
  "changelog-path": "Changelog.md",
  "include-v-in-tag": true,
  "bump-minor-pre-major": true,
  "extra-files": ["far-build.sh"],
  "packages": { ".": {} }
}
```
`.release-please-manifest.json` — текущая версия, с которой стартуем:
```json
{ ".": "1.2.0" }
```
В workflow тогда вместо `release-type` указываются `config-file: release-please-config.json` и `manifest-file: .release-please-manifest.json`. Если релизы до этого ставили руками, в манифест впишите **последний существующий тег** (здесь `v1.2.0`), иначе инструмент начнёт считать с нуля.

Принудительно выпустить конкретный номер можно пустым коммитом:
```bash
git commit --allow-empty -m "chore: release 2.0.0" -m "Release-As: 2.0.0"
```

### Changelog: что на самом деле можно настроить

Распространённое мнение: «release-please пишет Changelog в своём формате и на английском, поэтому русский Changelog с эмодзи придётся либо отдать ему, либо отказаться от инструмента». Это **верно только наполовину**:

| Утверждение | Вердикт | Факт (по документации и исходникам) |
| :--- | :--- | :--- |
| «На английском» | ⚠️ частично | Пункты — это **заголовки коммитов как есть**: русские коммиты дадут русский Changelog. Названия разделов (`Features`, `Bug Fixes`) меняются опцией **`changelog-sections`**, в том числе на русские с эмодзи. Жёстко на английском остаётся только блок `⚠ BREAKING CHANGES` |
| «В своём формате» | ✅ | Заголовок версии — `## [1.2.1](ссылка-сравнения) (2026-10-09)`, пункт — `* описание ([abc1234](ссылка-на-коммит))`. Формат *Keep a Changelog* (`## [1.2.1] - 2026-10-09`) и эмодзи **у каждого пункта** штатно не получить, если они не стоят в самом сообщении коммита |
| «Придётся отдать ему весь Changelog» | ❌ | Он **не переписывает** старые записи: новая запись вставляется **над** последним заголовком версии, а история ниже остаётся как была |
| «Либо отдать, либо отказаться» | ❌ | Есть **третий путь**: `"skip-changelog": true`. release-please ведёт версию, тег и GitHub Release, а Changelog вы пишете сами — прямо в release-PR до мержа |

Русские разделы:
```json
"changelog-sections": [
  { "type": "feat",     "section": "✨ Добавлено" },
  { "type": "fix",      "section": "🐛 Исправлено" },
  { "type": "perf",     "section": "⚡ Производительность" },
  { "type": "revert",   "section": "↩️ Откаты" },
  { "type": "docs",     "section": "📝 Документация", "hidden": true },
  { "type": "chore",    "section": "Прочее",          "hidden": true }
]
```

> [!warning] Подвох с `## [Unreleased]`
> Место вставки ищется регуляркой `\n###? v?[0-9[]` (`src/updaters/changelog.ts`). Ей соответствует и `## [Unreleased]`, ведь он начинается с `[`. Поэтому новая версия встанет **над** блоком «Unreleased/Запланировано», а не под ним. Перенесите такой блок в README или issue, или поправляйте порядок в release-PR.

Совет из README инструмента: мержите PR **squash-мержем**. Тогда в историю `main` попадает одно сообщение на PR — заголовок PR, оформленный по Conventional Commits, — и Changelog не засоряется промежуточными `fix typo`.

---

## 3. semantic-release — релиз на каждый пуш

### Как работает

На каждый пуш в ветку релизов (`main`) CI запускает `npx semantic-release`. Он анализирует коммиты и, если есть релизные, **тут же** ставит тег, создаёт GitHub Release, может опубликовать пакет в npm и закоммитить Changelog. PR и ручного шага нет: смержили `fix:` — через минуту вышла новая версия.

Конвейер собирается из плагинов: `commit-analyzer` (какая версия) → `release-notes-generator` (текст) → `changelog` (файл) → `npm`/`git`/`github` (публикация). По умолчанию включены `commit-analyzer`, `release-notes-generator`, `npm` и `github`. Для проекта без npm их перечисляют явно.

`.releaserc.json` для проекта без npm, с файлом Changelog:
```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/changelog", { "changelogFile": "Changelog.md" }],
    ["@semantic-release/git", { "assets": ["Changelog.md"],
      "message": "chore(release): ${nextRelease.version} [skip ci]" }],
    "@semantic-release/github"
  ]
}
```
```yaml
# .github/workflows/release.yml
on: { push: { branches: [main] } }
permissions: { contents: write, issues: write, pull-requests: write }
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with: { fetch-depth: 0 }          # нужна вся история и теги
      - uses: actions/setup-node@v5
        with: { node-version: 24 }
      - run: npx semantic-release
        env: { GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}" }
```
Перед первым боевым запуском проверьте вывод с `npx semantic-release --dry-run`: он покажет, какую версию и заметки выпустил бы инструмент.

### Какие коммиты дают релиз (по умолчанию)

Из `commit-analyzer/lib/default-release-rules.js`: ломающее изменение → major; `feat` → minor; `fix`, `perf`, `revert` → patch. Всё остальное, в том числе `docs`, `chore`, `ci`, `build` и коммиты **не по формату**, релиз **не создаёт**. Правила меняются опцией `releaseRules`: например, `{ "type": "build", "scope": "ebuild", "release": "patch" }`.

### Про «каждый мерж ebuild плодит релиз»

Это **неверно в общем виде**. Релиз будет, только если коммит с ebuild оформлен как `feat:` или `fix:`. Автоматический коммит вида `gentoo: bump app-misc/far2l to 2.9.1` или `chore(gentoo): …` релиз **не запустит**. Наоборот, если обновление ebuild *должно* становиться релизом, это нужно прописать в `releaseRules`.

Справедливая часть критики другая: semantic-release выпускает версию **на каждый релизный мерж**. Пять `fix:` за вечер — это пять patch-релизов. «Копить» изменения можно так:
- держать отдельную ветку релизов (`branches: ["release"]`) и вливать в неё `main`, когда пора;
- или запускать workflow вручную (`on: workflow_dispatch`) вместо `on: push`.

Но тогда теряется главное его отличие от release-please.

---

## 4. Сравнение

| | **release-please** | **semantic-release** |
| :--- | :--- | :--- |
| Когда выходит версия | Когда вы смержили release-PR | Сразу на каждый релизный пуш |
| Контроль человека | Есть: PR можно придержать и поправить | Нет (только через ветки или ручной запуск) |
| Changelog | Своя структура; разделы настраиваются; можно отключить (`skip-changelog`) | Плагин `changelog`; шаблон настраивается через пресет `conventionalcommits` |
| Версия в файлах | Много `release-type` + `extra-files` с аннотациями | Плагины (`npm`, `exec`, `git`) |
| Публикация пакетов | Нет; это делает отдельный job по выходу `release_created` | Есть (`npm` и сторонние плагины) |
| Монорепо | Есть «из коробки» (манифест, `packages`) | Через сторонние обёртки |
| Зависимости | Готовый GitHub Action | Node.js в CI + плагины |
| Вне GitHub | Только GitHub | GitHub, GitLab, Bitbucket, Gitea (плагинами) |
| Кому подходит | Маленькие и средние проекты, где релиз — осознанное решение | Библиотеки с частыми релизами и полным CD (npm-пакеты) |

**Для маленького проекта** (скрипт и оверлей, релизы раз в несколько недель, русский Changelog) логичнее **release-please**. Если формат Changelog важен — с `skip-changelog: true` или с русскими `changelog-sections`.

---

## 5. Если нужен «свой» Changelog — git-cliff

Когда формат Changelog важнее автоматизации тегов (Keep a Changelog, русские разделы, эмодзи по шаблону), подходит **git-cliff** (Rust). Он строит Changelog по коммитам через **шаблон Tera**, полностью под ваш формат, и может посчитать следующую версию (`git cliff --bumped-version`). Тег и Release тогда ставятся руками или отдельным workflow (`orhun/git-cliff-action`).

| Система | Установка |
| :--- | :--- |
| Gentoo | `emerge --ask dev-vcs/git-cliff` (есть в основном дереве) |
| Arch | `pacman -S git-cliff` (репозиторий `extra`) |
| Debian/Ubuntu | в репозиториях нет: `cargo install git-cliff`, готовый бинарник из GitHub Releases или `npx git-cliff` |

```bash
git cliff --init                     # создаст cliff.toml с шаблоном
git cliff --bumped-version           # какая версия следующая
git cliff --unreleased --tag v1.3.0 --prepend Changelog.md
```

Остальные инструменты, которые стоит знать: **changesets** (для JS-монорепо; изменения описываются отдельными файлами, а не коммитами), **release-drafter** (черновик GitHub Release по меткам PR, без версии в файлах), **commitizen/cocogitto** (проверка коммитов + `bump` + Changelog локально).

---

## 6. Переход с ручных релизов (чек-лист)

- [ ] Коммиты в `main` уже по Conventional Commits (или включить squash-мерж с проверкой заголовка PR).
- [ ] Последний ручной тег (`v1.2.0`) существует — от него и будет считаться следующая версия.
- [ ] release-please: `release-please-config.json` + `.release-please-manifest.json` с текущей версией, `changelog-path`, при необходимости `extra-files` / `skip-changelog` / `changelog-sections`.
- [ ] Галка «Allow GitHub Actions to create and approve pull requests»; при обязательных проверках — PAT или GitHub App.
- [ ] Блок `## [Unreleased]` убран из Changelog или учтён (раздел 2).
- [ ] Автоматические коммиты ботов (bump ebuild и т.п.) оформлены так, как вы решили: `chore(gentoo):` — без релиза, `fix(gentoo):` — с релизом.
- [ ] semantic-release: сначала `--dry-run`.

## Ссылки

- release-please: https://github.com/googleapis/release-please
- Настройка (changelog-sections, extra-files, аннотации): https://github.com/googleapis/release-please/blob/main/docs/customizing.md
- Манифест и все опции: https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md
- GitHub Action: https://github.com/googleapis/release-please-action
- semantic-release: https://github.com/semantic-release/semantic-release
- Правила по умолчанию commit-analyzer: https://github.com/semantic-release/commit-analyzer/blob/master/lib/default-release-rules.js
- Conventional Commits (рус.): https://www.conventionalcommits.org/ru/v1.0.0/
- SemVer (рус.): https://semver.org/lang/ru/
- Keep a Changelog (рус.): https://keepachangelog.com/ru/1.1.0/
- git-cliff: https://git-cliff.org/
- commitlint: https://commitlint.js.org/

Связанные заметки: [commit](../Git/commit.md), [tag](../Git/tag.md), [GitHub Actions — автосчётчик заметок в README](GitHub%20Actions%20%E2%80%94%20%D0%B0%D0%B2%D1%82%D0%BE%D1%81%D1%87%D1%91%D1%82%D1%87%D0%B8%D0%BA%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%82%D0%BE%D0%BA%20%D0%B2%20README.md), [Changelog Sync After Ship](../../AI/Loops/Changelog%20Sync%20After%20Ship%20%E2%80%94%20%D0%BF%D0%B5%D1%82%D0%BB%D1%8F%20%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%20%D1%87%D0%B5%D0%B9%D0%BD%D0%B4%D0%B6%D0%BB%D0%BE%D0%B3%D0%B0.md).

#GitHub #GitHub_Actions #Git #Релизы #SemVer #Changelog
