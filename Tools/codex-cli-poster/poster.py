#!/usr/bin/env python3
"""Генератор постера-шпаргалки Codex CLI (2560x1440) для заметки
AI/Agents/Codex CLI — шпаргалка команд.md.

Оформление и движок — как у Tools/claude-code-poster (цветные шапки блоков,
клавиши «кнопками», бейджи). Содержимое (BLOCKS) правится вручную по заметке-шпаргалке.

Запуск:  python3 Tools/codex-cli-poster/poster.py            # собрать PNG в Cache/
         python3 Tools/codex-cli-poster/poster.py --size 19  # кегль меньше, если не влезает
Нужно:   Firefox или Chromium (headless-скриншот); Pillow — по желанию (сжатие и проверка высоты).
Шрифты Inter и JetBrains Mono скачиваются один раз в ~/.cache/bok-poster-fonts/.
"""
import argparse, html, io, os, shutil, subprocess, sys, tempfile, urllib.request, zipfile
from datetime import date
from pathlib import Path

# Палитра — как у постера Claude Code (Tools/claude-code-poster)
C = {
    "blue":    ("#035f98", "#eaf5f8"),
    "purple":  ("#61449e", "#f3f2f9"),
    "teal":    ("#03767b", "#e1f3f4"),
    "amber":   ("#a06402", "#f2eddd"),
    "red":     ("#b53b37", "#f9efee"),
    "magenta": ("#8b4286", "#faeffb"),
    "orange":  ("#b45005", "#f4eee3"),
    "green":   ("#03723d", "#e6f4ec"),
    "slate":   ("#3e4b57", "#f4f8fc"),
}

def K(*keys):
    return ("keys", keys)

NEW = "new"
PREVIEW = "preview"

EXP = PREVIEW  # экспериментальные функции и бета

BLOCKS = [
 ("ГОРЯЧИЕ КЛАВИШИ", "⌨️", "blue", [
  ("Ход и сессия", [
   (K("Esc"), "прервать текущий ход"),
   (K("Esc", "Esc"), "пусто — править прошлое + форк"),
   (K("Enter"), "в работе — указание в текущий ход"),
   (K("Tab"), "в работе — в очередь на след. ход"),
   (K("Ctrl", "C"), "выйти (как /exit)"),
   (K("Ctrl", "L"), "очистить экран, чат остаётся"),
   (K("⇧", "↑"), "/ ⇧↓ — reasoning выше / ниже"),
   (K("⇧", "←"), "править сообщение из очереди"),
  ]),
  ("Навигация и просмотр", [
   (K("Ctrl", "T"), "транскрипт (/ — поиск, q — выход)"),
   (K("F3"), "поиск по транскрипту"),
   (K("F4"), "свернуть / раскрыть действия"),
   (K("Ctrl", "O"), "скопировать ответ (/copy)"),
   (K("Ctrl", "R"), "поиск по истории промптов"),
   (K("Ctrl", "G"), "промпт во внешнем редакторе"),
   (K("Alt", "R"), "raw-вывод для выделения"),
   (K("Ctrl", "/"), "побочная беседа (/side)"),
   (K("F2"), "предупреждения (/warnings)"),
   (K("F8"), "/ F9 — голос / микрофон", EXP),
  ]),
  ("Редактирование строки", [
   (K("Ctrl", "A"), "/ Ctrl E — в начало / в конец"),
   (K("Ctrl", "K"), "удалить до конца строки"),
   (K("Ctrl", "U"), "удалить до начала строки"),
   (K("Ctrl", "W"), "удалить слово назад"),
   (K("Ctrl", "Y"), "вставить удалённое"),
   (K("Alt", "B"), "/ Alt F — на слово назад / вперёд"),
  ]),
  ("Ввод", [
   (K("Ctrl", "J"), "новая строка (ещё ⇧Enter)"),
   (K("@"), "найти файл, вставить путь"),
   (K("!"), "shell под текущими правами"),
   (K("/"), "слэш-команда"),
   (K("$"), "скилл или приложение"),
   (K("?"), "панель клавиш (на пустой строке)"),
  ]),
 ]),
 ("СЛЭШ-КОМАНДЫ", "📋", "purple", [
  ("Чат и сессия", [
   ("/new [имя]", "новый чат в той же сессии"),
   ("/clear [имя]", "то же + очистка экрана"),
   ("/resume", "вернуться к сохранённому чату"),
   ("/fork", "копия текущего чата"),
   ("/side", "побочная беседа (/btw)"),
   ("/compact", "сжать диалог"),
   ("/recap", "резюме без сжатия"),
   ("/goal <цель>", "работать до цели"),
   ("/plan [задача]", "сначала план"),
   ("/rename · /archive", "назвать · скрыть чат"),
   ("/delete", "удалить чат насовсем"),
   ("/cd <путь>", "сменить каталог"),
   ("/pwd", "показать каталог (/cwd)"),
   ("/export [файл]", "диалог в Markdown"),
   ("/exit", "выйти (/quit)"),
  ]),
  ("Проект и память", [
   ("/init", "стартовый AGENTS.md"),
   ("/import", "из Claude Code или Cursor"),
   ("/memories", "локальная память", EXP),
   ("/mention <путь>", "приложить файл"),
   ("/ide", "открытые файлы из IDE"),
  ]),
 ]),
 ("МОДЕЛЬ И ЛИМИТЫ", "🧠", "teal", [
  ("Модель и reasoning", [
   ("/model", "модель и уровень reasoning"),
   ("/fast", "быстрый тариф (лимит ×2,5)"),
   ("-m gpt-6.1-sol", "модель при запуске"),
   ("low … ultra", "уровни reasoning"),
  ]),
  ("Состояние", [
   ("/status", "модель, права, контекст"),
   ("/usage", "расход: daily · weekly"),
   ("/debug-config", "какой слой что задал"),
   ("/experimental", "включить функции"),
  ]),
 ]),
 ("КОД И ПРОВЕРКА", "🔍", "amber", [
  ("Ревью", [
   ("/diff", "изменения + новые файлы"),
   ("/review", "ревью рабочего дерева"),
   ("codex review --base main", "ревью ветки"),
   ("  --uncommitted", "незакоммиченное"),
   ("  --commit <sha>", "один коммит"),
  ]),
  ("Фоновые терминалы", [
   ("/ps", "что крутится, последний вывод"),
   ("/stop", "остановить все (/clean)"),
  ]),
 ]),
 ("ПРАВА И ПЕСОЧНИЦА", "🔀", "red", [
  ("Пресеты /permissions", [
   ("Read Only", "только чтение (вне git)"),
   ("Auto", "правки и команды в каталоге"),
   ("Approve for me", "запросы — ревьюеру"),
   ("Full access", "всё; только ВМ или контейнер"),
   ("/approve", "повторить отказ ревьюера"),
  ]),
  ("Флаги", [
   ("-s read-only", "песочница: только чтение"),
   ("-s workspace-write", "запись, сеть выкл."),
   ("-a on-request", "спрашивать при выходе"),
   ("-a never", "не спрашивать (CI)"),
   ("--add-dir DIR", "ещё каталог на запись"),
   ("--yolo", "без песочницы и вопросов"),
  ]),
  ("Shell и защита", [
   ("! npm test", "под теми же правами"),
   (".git .codex .aws", "всегда только чтение"),
  ]),
 ]),
 ("АГЕНТЫ И ЧАТЫ", "🪄", "magenta", [
  ("Субагенты и чаты", [
   ("/subagents", "потоки субагентов сессии"),
   ("/agents", "центр управления чатами"),
   ("codex queue", "сообщение в идущую сессию"),
   ("worker · explorer", "встроенные субагенты"),
  ]),
  ("Изоляция", [
   ("/worktree", "чат в отдельном worktree"),
   ("--worktree", "то же при запуске"),
   ("/daemon", "фоновый сервер Codex"),
  ]),
 ]),
 ("SKILLS, ПЛАГИНЫ, MCP", "🧩", "green", [
  ("Управление", [
   ("/skills", "выбрать скилл"),
   ("$skill-creator", "создать скилл"),
   ("/plugins", "плагины; Space — вкл/выкл"),
   ("/apps", "приложения → $app-slug"),
   ("/mcp [verbose]", "MCP-инструменты"),
   ("/hooks", "хуки: доверить, выключить"),
  ]),
  ("Где лежат", [
   (".agents/skills/<n>/", "скилл проекта"),
   ("~/.agents/skills/", "личные скиллы"),
   (".codex/agents/<n>.toml", "субагент проекта"),
   (".codex/hooks.json", "хуки проекта"),
  ]),
 ]),
 ("КОНФИГ И ИНТЕРФЕЙС", "⚙️", "orange", [
  ("Файлы", [
   ("~/.codex/config.toml", "свой конфиг"),
   (".codex/config.toml", "проект (доверенный)"),
   ("~/.codex/<p>.config.toml", "профиль (-p)"),
   ("AGENTS.md", "инструкции проекта"),
   ("~/.codex/auth.json", "вход: беречь!"),
   ("~/.codex/rules/*.rules", "правила команд", EXP),
  ]),
  ("Интерфейс", [
   ("/statusline", "строка состояния"),
   ("/title", "заголовок окна"),
   ("/theme · /keymap", "тема · клавиши"),
   ("/vim · /raw", "Vim-режим · сырой вывод"),
   ("/tui", "полный экран или прокрутка"),
   ("/pets", "питомец в терминале"),
  ]),
  ("Аккаунт и связь", [
   ("/logout", "выйти из аккаунта"),
   ("/feedback", "логи разработчикам"),
   ("/app", "в десктоп-приложение"),
  ]),
 ]),
 ("CLI И ФЛАГИ", "💻", "slate", [
  ("Команды", [
   ("codex", "интерактивно"),
   ('codex "q"', "с готовым промптом"),
   ('codex exec "q"', "без TUI, ответ в stdout"),
   ("codex resume --last", "последний чат"),
   ("codex fork", "копия сессии"),
   ("codex login", "--device-auth · status"),
   ("codex mcp add", "<n> -- <cmd> · --url"),
   ("codex doctor", "диагностика"),
   ("codex update", "обновить CLI"),
  ]),
  ("Запуск", [
   ("-m · -p", "модель · профиль"),
   ("-C DIR · -i FILE", "каталог · картинка"),
   ("-c key=value", "переопределить конфиг"),
   ("--search", "живой веб-поиск"),
   ("--oss", "локальная модель (Ollama)"),
   ("--enable · --disable", "функции (features)"),
  ]),
  ("Автоматизация (exec)", [
   ("--json", "события JSONL"),
   ("-o FILE", "финальный ответ в файл"),
   ("--output-schema F", "ответ по JSON Schema"),
   ("--ephemeral", "не сохранять сессию"),
   ("--skip-git-repo-check", "вне репозитория"),
   ("CODEX_API_KEY=…", "ключ на один запуск"),
  ]),
 ]),
]

COLUMNS = [[0], [1, 3], [2, 4], [7, 6], [8, 5]]



def keycaps(keys):
    out = []
    for k in keys:
        out.append(f'<span class="kbd">{html.escape(k)}</span>')
    return "".join(out)


def row(r):
    badge = r[2] if len(r) > 2 else None
    left, desc = r[0], r[1]
    if isinstance(left, tuple) and left[0] == "keys":
        l = f'<span class="keys">{keycaps(left[1])}</span>'
    else:
        l = f'<code>{html.escape(left)}</code>'
    b = ""
    if badge == NEW:
        b = ' <span class="badge new">NEW</span>'
    elif badge == PREVIEW:
        b = ' <span class="badge preview">EXP</span>'
    return f'<div class="row">{l}<span class="desc">{html.escape(desc)}{b}</span></div>'


def block(i):
    title, icon, col, sections = BLOCKS[i]
    hdr, body = C[col]
    parts = [f'<section class="card" style="--hdr:{hdr};--body:{body}">',
             f'<h2><span class="ico">{icon}</span>{html.escape(title)}</h2><div class="inner">']
    for sub, rows in sections:
        parts.append(f'<h3>{html.escape(sub)}</h3>')
        parts += [row(r) for r in rows]
    parts.append('</div></section>')
    return "\n".join(parts)



HERE = Path(__file__).resolve().parent
VAULT = HERE.parent.parent
DEFAULT_OUT = VAULT / "Cache" / "Codex-CLI" / "codex-cli-cheatsheet-2560x1440.png"
FONT_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "bok-poster-fonts"
JBM_URL = "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/{}.ttf"
INTER_ZIP = "https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip"
INTER_FILES = ["Inter-Regular", "Inter-SemiBold", "Inter-Bold", "Inter-ExtraBold", "Inter-BoldItalic"]
JBM_FILES = ["JetBrainsMono-Regular", "JetBrainsMono-Bold"]
W, H = 2560, 1440


def ensure_fonts():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    for name in JBM_FILES:
        p = FONT_DIR / f"{name}.ttf"
        if not p.exists():
            print(f"скачиваю {name}…")
            urllib.request.urlretrieve(JBM_URL.format(name), p)
    if not all((FONT_DIR / f"{n}.ttf").exists() for n in INTER_FILES):
        print("скачиваю Inter…")
        data = urllib.request.urlopen(INTER_ZIP).read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for n in z.namelist():
                base = n.rsplit("/", 1)[-1]
                if n.startswith("extras/ttf/") and base[:-4] in INTER_FILES:
                    (FONT_DIR / base).write_bytes(z.read(n))


def build_html(BASE, stamp):
    FONT = FONT_DIR.as_uri()
    css = f"""
    @font-face {{ font-family: Inter; src: url({FONT}/Inter-Regular.ttf); font-weight: 400; }}
    @font-face {{ font-family: Inter; src: url({FONT}/Inter-SemiBold.ttf); font-weight: 600; }}
    @font-face {{ font-family: Inter; src: url({FONT}/Inter-Bold.ttf); font-weight: 700; }}
    @font-face {{ font-family: Inter; src: url({FONT}/Inter-ExtraBold.ttf); font-weight: 800; }}
    @font-face {{ font-family: Inter; src: url({FONT}/Inter-BoldItalic.ttf); font-weight: 700; font-style: italic; }}
    @font-face {{ font-family: JBM; src: url({FONT}/JetBrainsMono-Bold.ttf); font-weight: 700; }}
    @font-face {{ font-family: JBM; src: url({FONT}/JetBrainsMono-Regular.ttf); font-weight: 400; }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: 2560px; height: 1440px; background: #fffffd; overflow: hidden; }}
    body {{ font-family: Inter, sans-serif; font-size: {BASE}px; color: #5b6168; padding: 22px 22px 0; }}
    .grid {{ display: flex; gap: 18px; align-items: flex-start; }}
    .col {{ flex: 1 1 0; display: flex; flex-direction: column; gap: 16px; min-width: 0; }}
    .card {{ background: var(--body); border: 1.5px solid color-mix(in srgb, var(--hdr) 28%, transparent); border-radius: 9px; overflow: hidden; }}
    .card h2 {{ background: var(--hdr); color: #fff; font-weight: 800; font-size: {BASE*1.25:.1f}px; letter-spacing: .04em; padding: 9px 14px 8px; display: flex; align-items: center; gap: 9px; }}
    .card h2 .ico {{ font-family: 'Noto Color Emoji'; font-size: {BASE*1.05:.1f}px; filter: saturate(.55); }}
    .inner {{ padding: 6px 14px 11px; }}
    h3 {{ font-style: italic; font-weight: 700; color: #2b2f33; font-size: {BASE*1.0:.1f}px; margin: 7px 0 5px; padding-bottom: 3px; border-bottom: 1px solid rgba(60,70,80,.18); }}
    .row {{ display: grid; grid-template-columns: auto 1fr; align-items: baseline; column-gap: 8px; line-height: 1.32; margin: 2.5px 0; }}
    code {{ font-family: JBM, monospace; font-weight: 700; color: #22272b; white-space: pre; font-size: {BASE*0.97:.1f}px; flex: none; }}
    .desc {{ color: #5f656c; flex: 1 1 auto; min-width: 0; text-align: left; }}
    .keys {{ display: inline-flex; gap: 4px; flex: none; }}
    .kbd {{ font-family: JBM, monospace; font-weight: 700; font-size: {BASE*0.82:.1f}px; color: #4a5059; background: #eef0f3; border: 1px solid #c3c8cf; border-bottom-width: 2px; border-radius: 4px; padding: 0 6px; min-width: 22px; text-align: center; line-height: 1.45; }}
    .badge {{ white-space: nowrap; font-family: Inter, sans-serif; font-weight: 800; font-size: {BASE*0.66:.1f}px; letter-spacing: .05em; border-radius: 4px; padding: 1px 6px; vertical-align: 1px; margin-left: 3px; }}
    .badge.new {{ background: #d9363e; color: #fff; }}
    .badge.preview {{ background: #e8f2fc; color: #2b6cb0; border: 1px solid #6aa3d8; }}
    .foot {{ position: absolute; right: 26px; bottom: 10px; font-size: {BASE*0.8:.1f}px; color: #9aa0a6; }}
    """

    cols_html = "".join('<div class="col">' + "".join(block(i) for i in col) + '</div>' for col in COLUMNS)
    return (f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Codex CLI — шпаргалка</title><style>{css}</style></head>
<body><div class="grid">{cols_html}</div>
<div class="foot">Codex CLI 0.164 — шпаргалка · по документации learn.chatgpt.com и исходникам openai/codex на {stamp} · EXP — экспериментальное или бета</div></body></html>""")


def screenshot(html_path, png_path):
    ff = shutil.which("firefox")
    if ff:
        with tempfile.TemporaryDirectory() as prof:
            subprocess.run([ff, "--headless", "--no-remote", "--profile", prof, f"--window-size={W},{H}",
                            "--screenshot", str(png_path), html_path.as_uri()],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        return
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        ch = shutil.which(name)
        if ch:
            subprocess.run([ch, "--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                            f"--screenshot={png_path}", html_path.as_uri()],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            return
    sys.exit("Нужен Firefox или Chromium для скриншота")


def check_and_compress(png_path):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow не найден: проверка высоты и сжатие пропущены")
        return
    im = Image.open(png_path).convert("RGB")
    colw = (W - 44 - 4 * 18) / 5
    bottoms = []
    for c in range(5):
        x0 = int(22 + c * (colw + 18))
        xs = range(x0 + 10, int(x0 + colw - 10), 6)
        last = 0
        for y in range(H - 40):
            if any(sum(im.getpixel((x, y))) < 700 for x in xs):
                last = y
        bottoms.append(last)
    print("низ колонок, px:", bottoms)
    if max(bottoms) >= H - 45:
        print("⚠ колонка упирается в низ — уменьшите --size или перераспределите COLUMNS")
    im.save(png_path, optimize=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=float, default=21, help="базовый кегль, px (по умолчанию 21)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="куда положить PNG")
    ap.add_argument("--date", default=date.today().strftime("%d.%m.%Y"), help="дата сверки с документацией")
    ap.add_argument("--html", type=Path, help="сохранить и промежуточный HTML")
    a = ap.parse_args()
    ensure_fonts()
    page = build_html(a.size, a.date)
    with tempfile.TemporaryDirectory() as tmp:
        hp = Path(a.html) if a.html else Path(tmp) / "poster.html"
        hp.write_text(page, encoding="utf-8")
        a.out.parent.mkdir(parents=True, exist_ok=True)
        screenshot(hp.resolve(), a.out.resolve())
    if not a.out.exists():
        sys.exit("скриншот не получился")
    check_and_compress(a.out)
    print("готово:", a.out)


if __name__ == "__main__":
    main()
