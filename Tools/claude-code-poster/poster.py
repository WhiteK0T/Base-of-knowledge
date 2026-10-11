#!/usr/bin/env python3
"""Генератор постера-шпаргалки Claude Code (2560x1440) для заметки
AI/Agents/Claude Code — шпаргалка команд.md.

Оформление повторяет исходную шпаргалку из поста https://t.me/bugnotfeature/27215:
цвета шапок и подложек сняты с оригинала, клавиши «кнопками», бейджи NEW.
Содержимое (BLOCKS) правится вручную по заметке-шпаргалке.

Запуск:  python3 Tools/claude-code-poster/poster.py            # собрать PNG в Cache/
         python3 Tools/claude-code-poster/poster.py --size 19  # кегль меньше, если не влезает
Нужно:   Firefox или Chromium (headless-скриншот); Pillow — по желанию (сжатие и проверка высоты).
Шрифты Inter и JetBrains Mono скачиваются один раз в ~/.cache/bok-poster-fonts/.
"""
import argparse, html, io, os, shutil, subprocess, sys, tempfile, urllib.request, zipfile
from datetime import date
from pathlib import Path

# Палитра снята с оригинала (медианы пикселей шапок и подложек)
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

BLOCKS = [
 ("ГОРЯЧИЕ КЛАВИШИ", "⌨️", "blue", [
  ("Управление сессией", [
   (K("Esc"), "прервать Claude / закрыть диалог"),
   (K("Esc", "Esc"), "пусто — rewind; текст — очистить"),
   (K("Ctrl", "C"), "прервать или очистить ввод"),
   (K("Ctrl", "D"), "выйти из сессии"),
   (K("Ctrl", "Z"), "приостановить (Unix), вернуться — fg"),
   (K("Ctrl", "L"), "перерисовать экран"),
   (K("⇧", "Tab"), "цикл режимов прав"),
  ]),
  ("Навигация и просмотр", [
   (K("Ctrl", "O"), "транскрипт"),
   (K("Ctrl", "R"), "обратный поиск по истории"),
   (K("Ctrl", "T"), "чек-лист задач Claude"),
   (K("Ctrl", "B"), "bash и агентов — в фон (tmux: ×2)"),
   (K("Ctrl", "S"), "спрятать / вернуть черновик"),
   (K("Ctrl", "G"), "промпт во внешнем редакторе"),
   (K("Ctrl", "X", "Ctrl", "K"), "стоп всех фоновых субагентов"),
   (K("Alt", "P"), "сменить модель"),
   (K("Alt", "T"), "расширенное мышление"),
   (K("Alt", "O"), "fast mode"),
  ]),
  ("Редактирование строки", [
   (K("Ctrl", "A"), "/ Ctrl E — в начало / в конец"),
   (K("Ctrl", "K"), "/ Ctrl U — удалить до конца / начала"),
   (K("Ctrl", "W"), "удалить слово назад"),
   (K("Ctrl", "Y"), "вставить удалённое"),
   (K("Alt", "B"), "/ Alt F — на слово назад / вперёд"),
  ]),
  ("Ввод", [
   (K("\\", "Enter"), "новая строка (везде; ещё Ctrl J)"),
   (K("@"), "упомянуть файл"),
   (K("!"), "shell-режим"),
   (K("/"), "команда или скилл"),
   (K(":"), "шорткод эмодзи"),
   (K("?"), "панель клавиш (на пустой строке)"),
  ]),
 ]),
 ("СЛЭШ-КОМАНДЫ", "📋", "purple", [
  ("Контекст и сессия", [
   ("/clear", "новый диалог, память проекта остаётся"),
   ("/compact [фокус]", "сжать диалог"),
   ("/context", "чем занят контекст + подсказки"),
   ("/rewind", "откат кода и диалога (/undo)"),
   ("/branch", "ответвить диалог"),
   ("/goal <условие>", "работать до условия", NEW),
   ("/cd <путь>", "сессию — в другой каталог", NEW),
   ("/recap", "резюме сессии в одну строку"),
   ("/focus", "только промпт, сводка и ответ"),
   ("/btw <вопрос>", "вопрос «в сторону»"),
   ("/exit", "выйти из CLI"),
  ]),
  ("Проект и память", [
   ("/init", "стартовый CLAUDE.md"),
   ("/memory", "CLAUDE.md и авто-память"),
   ("/add-dir", "добавить рабочий каталог"),
   ("/import", "конфиги Codex/Gemini/Cursor", NEW),
   ("/team-onboarding", "гайд для коллеги из сессий"),
   ("/insights", "HTML-отчёт по сессиям"),
  ]),
 ]),
 ("МОДЕЛЬ И ЛИМИТЫ", "🧠", "teal", [
  ("Модель и усилия", [
   ("/model", "сменить модель (←/→ — reasoning)"),
   ("/effort", "low…xhigh · max (сессия) · auto"),
   ("/effort ultracode", "оркестрация workflow"),
   ("/advisor", "второй «модель-советник»", NEW),
   ("/fast", "fast mode вкл/выкл"),
   ("/autocompact", "порог автосжатия контекста"),
  ]),
  ("Стоимость и лимиты", [
   ("/usage", "стоимость, лимиты (/cost, /stats)"),
   ("/rate-limit-options", "что делать при лимите"),
   ("/usage-credits", "настроить / запросить кредиты"),
   ("/upgrade", "сменить тариф"),
  ]),
 ]),
 ("КОД И ПРОВЕРКА", "🔍", "amber", [
  ("Ревью", [
   ("/code-review [lvl]", "баги: дифф, PR, ветка"),
   ("  --fix · --comment", "исправить · в PR/MR"),
   ("/code-review ultra", "глубокое облачное ревью"),
   ("/review", "псевдоним /code-review"),
   ("/security-review", "уязвимости ветки"),
   ("/simplify", "4 ревьюера + сразу правки", NEW),
   ("/diff", "изменения в рабочем дереве"),
  ]),
  ("Проверка в деле", [
   ("/verify", "собрать, запустить, убедиться"),
   ("/run", "запустить приложение проекта"),
   ("/debug", "отладочный лог сессии"),
  ]),
 ]),
 ("РЕЖИМЫ ПРАВ И SHELL", "🔀", "red", [
  ("Режимы (⇧Tab)", [
   ("default", "Manual: без запроса только чтение"),
   ("acceptEdits", "+ правки, mkdir / mv / cp"),
   ("plan", "чтение и анализ → план"),
   ("auto", "всё, с фоновыми проверками"),
   ("dontAsk", "только разрешённое (CI)"),
   ("bypassPermissions", "всё; только контейнер/ВМ"),
   ("deny-правила", "действуют во всех режимах"),
  ]),
  ("Shell-режим", [
   ("! npm test", "без Claude, вывод — в контекст"),
   (K("Tab"), "автодополнение прошлых ! команд"),
   (K("Esc"), "выход (или Backspace на пустой)"),
  ]),
 ]),
 ("ОРКЕСТРАЦИЯ (MULTI-AGENT)", "🪄", "magenta", [
  ("Фоновая работа", [
   ("/subtask <задача>", "субагент, итог — сюда", NEW),
   ("/fork", "копия — в фон. сессию", NEW),
   ("/background", "увести всю сессию в фон"),
   ("claude agents", "экран фоновых сессий"),
   ("/tasks", "шеллы и субагенты сессии"),
   ("/list-agents", "кому можно написать"),
  ]),
  ("Массово и по расписанию", [
   ("/batch", "5–30 юнитов, у каждого worktree"),
   ("/workflows", "прогресс workflow"),
   ("/loop [интервал]", "повторять промпт"),
  ]),
 ]),
 ("SKILLS И ПЛАГИНЫ", "🧩", "green", [
  ("Управление", [
   ("/skills", "список; t — по цене в токенах"),
   ("/skill-doctor", "цена и частота каждого скилла"),
   ("/reload-skills", "пересканировать без рестарта"),
   ("/plugin", "плагины и marketplace"),
  ]),
  ("Где лежат", [
   (".claude/skills/<n>/SKILL.md", "скилл проекта"),
   (".claude/commands/<n>.md", "тоже /n (= skill)"),
   (".claude/agents/<n>.md", "субагент проекта"),
   ("~/.claude/…", "то же, но личное"),
  ]),
 ]),
 ("КОНФИГ И ДИАГНОСТИКА", "⚙️", "orange", [
  ("Файлы настроек", [
   ("~/.claude/settings.json", "пользовательские"),
   (".claude/settings.json", "проект (в VCS)"),
   (".claude/settings.local.json", "вне VCS"),
   ("CLAUDE.md / AGENTS.md", "память проекта"),
  ]),
  ("Настройка", [
   ("/config", "настройки"),
   ("/permissions", "allow / ask / deny"),
   ("/hooks · /keybindings", "хуки · клавиши"),
   ("/statusline · /theme", "статус-строка · тема"),
   ("/doctor", "проверка + исправления", None),
   ("/status · /sandbox", "статус · песочница"),
   ("/mcp", "MCP-серверы; reconnect"),
   ("/release-notes", "changelog по версиям"),
  ]),
  ("Интеграции", [
   ("/install-github-app", "GitHub App"),
   ("/chrome · /ide", "Chrome · IDE"),
   ("/desktop · /mobile", "десктоп · QR приложения"),
   ("/teleport", "веб-сессию — в терминал"),
   ("/remote-control", "сессию — для claude.ai"),
  ]),
 ]),
 ("CLI И ФЛАГИ", "💻", "slate", [
  ("Команды", [
   ("claude", "интерактивно"),
   ('claude "q"', "с готовым промптом"),
   ('claude -p "q"', "headless, вывод и выход"),
   ("claude -c", "продолжить последнюю сессию"),
   ('claude -r "имя"', "возобновить по ID или имени"),
   ("claude update", "обновить CLI"),
  ]),
  ("Запуск", [
   ("--model · --effort", "модель · усилия"),
   ("--agent · --add-dir", "агент · доп. каталоги"),
   ("--fallback-model", "резерв при перегрузке"),
   ("--session-id", "свой UUID сессии"),
  ]),
  ("Промпты и права", [
   ("--append-system-prompt", "+ к системному"),
   ("--tools · --agents", "инструменты · субагенты"),
   ("--permission-mode", "стартовый режим"),
   ("--dangerously-skip-permissions", "без спроса"),
   ("--safe-mode · --bare", "без кастомов · минимум"),
  ]),
  ("Автоматизация", [
   ("--output-format", "text / json / stream-json"),
   ("--json-schema", "ответ строго по схеме"),
   ("--max-turns · --max-budget-usd", "лимиты"),
   ("--mcp-config", "MCP-серверы из JSON"),
   ("--worktree · --tmux", "изолированный worktree"),
  ]),
 ]),
]

COLUMNS = [[0], [1, 4], [2, 3, 5], [7, 6], [8]]


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
        b = ' <span class="badge preview">PREVIEW</span>'
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
DEFAULT_OUT = VAULT / "Cache" / "Claude-Code" / "claude-code-cheatsheet-2560x1440.png"
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
    return (f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Claude Code — шпаргалка</title><style>{css}</style></head>
<body><div class="grid">{cols_html}</div>
<div class="foot">Claude Code — шпаргалка · по документации code.claude.com на {stamp} · NEW — новое в этой версии шпаргалки</div></body></html>""")


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
    ap.add_argument("--size", type=float, default=20, help="базовый кегль, px (по умолчанию 20)")
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
