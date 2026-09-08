---
создал заметку: 2026-09-08T21:40:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - Файнтюн
  - Local-LLM
  - LoRA
  - Python
  - GGUF
Источник:
  - https://t.me/bugnotfeature/26972
  - https://github.com/MakazhanAlpamys/Soup
  - https://pypi.org/project/soup-cli/
  - https://trysoup.dev
  - https://doi.org/10.5281/zenodo.21771064
---

# 🍲 Soup — обучение своей LLM из одного YAML

Разбор поста [«Не баг, а фича» от 08.09.2026](https://t.me/bugnotfeature/26972) про **Soup** — CLI для файнтюна и пост-тренинга LLM: один YAML-конфиг, одна команда, без SSH и ручной настройки инфраструктуры.

Ссылок в посте нет, проект пришлось искать самому: это [`MakazhanAlpamys/Soup`](https://github.com/MakazhanAlpamys/Soup) на PyPI как **`soup-cli`**. Проверено 08.09.2026 по репозиторию, PyPI и руками — ставил в чистый venv и запускал.

> [!info] Что за проект
> | | |
> | :--- | :--- |
> | Репозиторий | [MakazhanAlpamys/Soup](https://github.com/MakazhanAlpamys/Soup), создан 20.02.2026 |
> | Звёзд / форков / issue | **5 794** · 877 · 71 открытых |
> | Лицензия / язык | **Apache-2.0** · Python |
> | Актуальная версия | **0.74.0** (04.09.2026), всего **176 релизов** |
> | Автор | Alpamys Makazhan, Астана, Казахстан (`@AlanaTechGroup`) |
> | Сайт / DOI | [trysoup.dev](https://trysoup.dev) · [10.5281/zenodo.21771064](https://doi.org/10.5281/zenodo.21771064) |

**Короткий вывод:** пост на удивление точен — почти всё, что он утверждает, подтверждается. Но он умалчивает о единственной вещи, которая сломает установку именно на твоей машине.

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :--- | :--- |
| `pip install 'soup-cli[train]'` | ⚠️ Кавычки не те | README прямо предупреждает: **двойные**, а не одинарные. В bash/zsh сработают и одинарные, в `cmd.exe` и PowerShell — нет |
| «На 7B достаточно 8 ГБ VRAM, на 14B — 16 ГБ» | ✅ Верно | Дословно из таблицы README. Важно: это **QLoRA 4-bit**, не полный файнтюн |
| «Десятки готовых шаблонов» | ✅ Верно | В установленном пакете **21** шаблон `soup init --template` |
| Шаблоны для чата, кода, медицины, рассуждений, зрения, RLHF | ✅ Все шесть есть | `chat`, `code`, `medical`, `reasoning`, `vision`, `rlhf` |
| `soup init --template chat` → `soup train` → `soup chat --model ./output` | ✅ Команды настоящие | Проверил руками, `init` работает даже на лёгкой установке без PyTorch |
| Экспорт в GGUF, запуск в Ollama, загрузка на HuggingFace | ✅ Верно | `soup export --format gguf --quant q4_k_m` и `soup push --repo you/my-model` |
| «Никаких SSH и инфраструктурного кошмара» | ✅ Это слоган проекта | *«No SSH, no config hell»* |
| «Всё автоматизировано» | ✅ Подтвердилось на практике | Без GPU сам определил CPU и переключил `quantization: 4bit → none` |
| **Ничего про версию Python** | ❌ **Умолчание** | Нужен **Python 3.10–3.12**. На 3.13+ pip молча ставит старую 0.72.4 |
| **Ничего про главную фичу проекта** | ⚠️ Странно | Заголовок самого репозитория — 8B на **4 ГБ** через layer streaming, а не 7B на 8 ГБ |

## 💥 Главная проблема: Python 3.13+ ломает установку молча

README честно пишет: *«Python 3.10, 3.11 or 3.12 ... 3.13+ is not supported yet because the PyTorch stack has not been validated there»*. Но проблема не в том, что установка упадёт. **Она пройдёт** — и это хуже.

История ограничения по версии Python на PyPI:

| Версия | Дата | `requires_python` |
| :--- | :--- | :--- |
| 0.1.0 | 02.03.2026 | `>=3.9` |
| 0.71.0 | 01.06.2026 | `>=3.10` |
| **0.73.0** | **09.08.2026** | **`<3.13,>=3.10`** ← потолок появился только здесь |

Потолок добавлен только в 0.73.0. Всё до 0.72.4 включительно объявляет `>=3.10` **без верхней границы**. Поэтому на Python 3.13/3.14 pip не ругается, а откатывается на последнюю версию без потолка:

```bash
# проверено на Gentoo, Python 3.14.7:
$ python3 -m venv soupvenv && ./soupvenv/bin/pip install soup-cli
...
Successfully installed ... soup-cli-0.72.4 ...
                              ^^^^^^^^^^^^^ вместо 0.74.0, без единого предупреждения
```

> [!danger] Что именно ты недополучаешь, оставшись на 0.72.4
> Это не «версия чуть постарее». Между 0.72.4 и 0.74.0 закрыты вещи, ради которых стоит обновляться:
> - **Frozen base грузился в fp32 на всех трёх путях загрузки.** База, которая вообще не получает шагов оптимизатора, разворачивалась в удвоенной точности. Замер авторов на H100 с Llama-3.1-8B + LoRA: **48 241 МиБ → 18 658 МиБ пикового VRAM, разница 2,59× (28,9 ГБ)**. То есть на 0.72.4 все расчёты «влезет / не влезет» врут в худшую сторону.
> - **Четыре обхода SSRF-защиты** одной природы — сокращённая, десятичная, шестнадцатеричная и восьмеричная записи IPv4 (`127.1`, `2130706433`, `0x7f000001`, `0177.0.0.1`) проходили через guard телеметрии, вебхуков и OTLP-валидатора.
> - **Исправление корректности из 0.73.0**, из-за которого пришлось пересматривать замеры производительности.
>
> Проверяй, что реально встало: `pip show soup-cli`. Если там не 0.74.0 — у тебя не тот Soup.

## 🧊 Про VRAM: пост занижает собственные обещания проекта

Цифры из поста взяты из таблицы README и верны:

| VRAM | Максимальная модель (QLoRA 4-bit) | Пример |
| :--- | :--- | :--- |
| 8 ГБ | ~7B | Llama-3.1-8B, Mistral-7B |
| 16 ГБ | ~14B | Phi-4-14B, Qwen2.5-14B |
| 24 ГБ | ~34B | CodeLlama-34B, Yi-1.5-34B |
| 48 ГБ | ~70B | Llama-3.3-70B |
| 80 ГБ+ | 70B+ (полный) или MoE | Mixtral-8x22B, DeepSeek-V3 |

Но заголовок самого репозитория звучит куда громче: *«Layer streaming trains an 8B model on a 4 GB laptop GPU»*. Замороженная база не держится в VRAM целиком, а подаётся на GPU по одному слою декодера. Заявленный замер — Llama-3.1-8B-Instruct + NF4 на RTX 3050 Laptop 4 ГБ: **119,6 tok/s при пике 3,32 ГБ**, бит-в-бит совпадая с обычным резидентным прогоном.

> [!warning] Почему я бы не строил на этом планы
> Авторы сами оговариваются, и это стоит процитировать:
> - режим **опциональный и в статусе BETA** (`stream_layers: true`, по умолчанию выключен);
> - *«The tok/s figure was measured on v0.72.2, before the v0.73.0 correctness repair that cost −4.8% at 32B; it has not been re-run on a 4 GB card since»* — то есть **цифра 119,6 tok/s устарела по признанию самих авторов**;
> - в 0.74.0 отдельно чинили то, что бесплатный тариф Colab/Kaggle (**T4, P100, V100, GTX 16xx**) вообще не мог стримить — падал.
>
> Проверить можно: в репозитории лежит [`notebooks/proof-4gb.ipynb`](https://github.com/MakazhanAlpamys/Soup/blob/main/notebooks/proof-4gb.ipynb) — ноутбук ограничивает процесс четырьмя гигабайтами и проверяет побитовое совпадение. Плюс каталог [`benchmarks/`](https://github.com/MakazhanAlpamys/Soup/tree/main/benchmarks) с отдельным отчётом на каждый релиз.

## 🧪 Что я проверил руками

Ставил в чистый venv на Python 3.14 (лёгкая установка, без PyTorch):

```bash
$ ./soupvenv/bin/pip list | grep -iE "^torch|transformers|peft|trl"
# пусто — лёгкий пакет действительно без обучающего стека, как и заявлено

$ soup init --template chat
Using template: chat
╭──────────── Ready! ────────────╮
│ Config saved to soup.yaml      │
│ Next step: soup train ...      │
╰────────────────────────────────╯
```

Сгенерированный `soup.yaml`:

```yaml
base: meta-llama/Llama-3.1-8B-Instruct
task: sft
data:
  train: ./data/train.jsonl
  format: alpaca
  val_split: 0.1
  max_length: 2048
training:
  epochs: 3
  lr: 2e-5
  batch_size: auto
  lora: { r: 64, alpha: 16, target_modules: auto }
  quantization: 4bit
output: ./output
```

Запуск `soup train` без GPU показал, что автоопределение работает:

```
Warning: 4bit quantization is not supported on CPU. Switching to quantization: none.
╭──────────── Training Setup ────────────╮
│ Device:  CPU (no GPU detected)         │
│ Model:   meta-llama/Llama-3.1-8B-Instruct │
│ Backend: transformers                  │
╰────────────────────────────────────────╯
Start training? [Y/n]:
```

Шаблонов в пакете **21** (README перечисляет 17 — в самом пакете есть ещё и compliance-шаблоны):

```
audio  bco  chat  code  embedding  eu-ai-act  hipaa  ipo  kto  longcontext
medical  moe  orpo  pretrain  reasoning  rlhf  simpo  soc2  sr-11-7
tool-calling  vision
```

> [!caution] Шаблон по умолчанию ссылается на закрытую модель
> `meta-llama/Llama-3.1-8B-Instruct` имеет на HuggingFace статус **`gated: manual`** — доступ выдаёт Meta вручную по заявке. То есть сгенерированный конфиг «из коробки» не запустится, пока не получишь одобрение. Меняй `base` на что-то открытое (`Qwen/Qwen2.5-7B-Instruct`, `mistralai/Mistral-7B-Instruct-v0.3`) либо подавай заявку заранее.

## 🔒 Приватность: лучше, чем можно было ожидать

Проверял в исходниках установленного пакета, а не по документации.

**Телеметрия — opt-IN, по умолчанию выключена.** В `utils/trackers.py` есть эндпоинт PostHog (`https://us.i.posthog.com`), но:

```python
_TELEMETRY_ENV_VAR = "SOUP_TELEMETRY"

def is_telemetry_enabled(env=None) -> bool:
    """Telemetry is opt-IN until v0.43.1 ships the network code.
    ... we keep it default-OFF so no payload is built or sent.
    Users may enable explicitly with `SOUP_TELEMETRY=1`.
    """
```

Ключ PostHog захардкожен намеренно (write-only), а свой инстанс подставляется парой `SOUP_POSTHOG_KEY` + `SOUP_POSTHOG_ENDPOINT`. OTLP-трейсинг тоже требует явного `enabled` и своего эндпоинта — это наблюдаемость для тебя, а не отчётность автору.

**А вот локальный журнал пишется по умолчанию.** Из `soup --help`:

> `--no-audit-log` — Disable the local HIPAA/SOC2 audit log for this invocation (also via `SOUP_NO_AUDIT_LOG=1`). **Default: a one-line record per command under `~/.soup/audit.jsonl`.**

Никуда не отправляется, но лежит у тебя на диске и содержит историю команд. Если это лишнее — `export SOUP_NO_AUDIT_LOG=1`.

## 📦 Установка на твоих системах

> [!tip] Главное правило
> Ставь **не системным pip**, а через `pipx` / `uv tool` / venv — и обязательно на **Python 3.12 или младше**. Иначе получишь 0.72.4 вместо 0.74.0 (см. выше).

| Система | Что делать |
| :--- | :--- |
| **Gentoo** (основная) | Здесь стоит только `python-3.14.7`, а Soup требует `<3.13`. Ставим нужный слот и делаем на нём venv: `emerge dev-lang/python:3.12` (в дереве есть `3.12.14`), затем `python3.12 -m venv ~/.venv/soup && ~/.venv/soup/bin/pip install "soup-cli[train]"`. **PyTorch из исходников через Portage не собирай** — `sci-ml/pytorch` тянет монструозную сборку; внутри venv придут готовые колёса с PyPI, и это нормальный путь для инструмента разработки |
| **Debian / Ubuntu** | С Debian 12 / Ubuntu 23.04+ системный pip заблокирован (PEP 668, `externally-managed-environment`) — README отдельно это объясняет. `sudo apt install pipx python3.12-venv`, затем `pipx install "soup-cli[train]"`. Если 3.12 нет в репозитории — `deadsnakes` PPA или venv на своей сборке |
| **Arch** | В официальных репозиториях и AUR пакета нет. Питон в Arch — свежий, поэтому нужен отдельный слот: `pacman -S python312` из AUR или `pyenv install 3.12`, дальше venv + `pip install "soup-cli[train]"` |
| **Entware / RT-AX56U** | ❌ **Неприменимо.** armv7, 512 МБ RAM, 256 МБ флеша, нет GPU и нет PyTorch в репозитории. Один только `[train]`-стек весит гигабайты. Роутер тут ни при чём — обучать на нём нечего и нечем |

Общий рабочий сценарий:

```bash
# 1. окружение на правильном питоне
python3.12 -m venv ~/.venv/soup
source ~/.venv/soup/bin/activate
pip install "soup-cli[train]"     # ДВОЙНЫЕ кавычки
pip show soup-cli                 # обязательно проверь: должно быть 0.74.0

# 2. конфиг
soup init --template chat
$EDITOR soup.yaml                 # смени base на открытую модель

# 3. проверка окружения перед запуском
soup doctor                       # GPU, зависимости, версия

# 4. обучение и проверка
soup train --config soup.yaml
soup chat  --model ./output

# 5. выкатка
soup merge  --adapter ./output
soup export --model ./output --format gguf --quant q4_k_m   # для Ollama/llama.cpp
soup push   --model ./output --repo you/my-model
```

Есть и альтернативы установке: `docker pull ghcr.io/makazhanalpamys/soup:latest` (образ публикуется на каждый релиз — обходит всю возню с версиями Python) и веб-морда `soup ui` на `127.0.0.1:7860`.

## 🧭 Насколько проекту можно доверять

Аргументы за:

- **Apache-2.0**, открытый код, DOI на Zenodo, каталог `benchmarks/` с отчётом на каждый релиз.
- **Необычная для такого проекта честность в README.** Прямо написано, что цифра tok/s устарела; что `torch>=2.5.0` в объявленных зависимостях не работает с `trl>=0.29` ([#651](https://github.com/MakazhanAlpamys/Soup/issues/651)); что неизвестные ключи конфига сейчас только предупреждают, а с v0.75 будут ронять загрузку.
- Телеметрия выключена по умолчанию, и в коде это подкреплено комментарием, а не только обещанием.

Аргументы против:

- **176 релизов за полгода** (~25 в месяц, около одного в день). Это не «стабильный инструмент», а быстро движущаяся мишень: ломающие изменения появляются между минорными версиями.
- **Из 42 контрибьюторов у автора 919 коммитов, у следующего — 37.** Заявление README про «116 из 120 PR в релизе пришли извне» верно для конкретного релиза, но общая картина — проект одного человека.
- Обвес из бейджей Product Hunt / Trendshift и версия 0.74.0 при таком объёме заявленных возможностей (SFT, DPO, GRPO, PPO, KTO, ORPO, SimPO, IPO, BCO, дистилляция, unlearning, RAG-обучение, HIPAA/SOC2/EU-AI-Act-шаблоны) — заявка шире, чем можно всерьёз протестировать силами одного мейнтейнера.

## 💡 Кому пригодится

- **Есть своя видеокарта и датасет** — Soup закрывает рутину: автоподбор батча, определение GPU, квантизация, экспорт в GGUF одной командой. Ради этого его и стоит попробовать.
- **Хочется просто «свою модель»** — реалистичнее взять готовый расцензуренный или дообученный чекпоинт: [Gemma 4 12B Coder](../Model/Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md), [Qwythos-9B](../Model/Qwythos-9B-Claude-Mythos-5-1M%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20Qwen3.5-9B%20%D0%BD%D0%B0%20%D1%82%D1%80%D0%B5%D0%B9%D1%81%D0%B0%D1%85%20Claude%20%281M%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%29.md). Файнтюн без нормального датасета модель не улучшит.
- **Нужно снять ограничения, а не учить на своих данных** — это другая задача, см. [Heretic (abliteration)](../Heretic%20%E2%80%94%20%D1%81%D0%BD%D1%8F%D1%82%D0%B8%D0%B5%20safety-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D1%81%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D1%85%20LLM%20%28abliteration%29.md).
- **Продакшен** — рано. 0.74.0, релиз почти каждый день, ломающие изменения обещаны уже в 0.75.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/26972](https://t.me/bugnotfeature/26972)
- Проект: [GitHub](https://github.com/MakazhanAlpamys/Soup) · [PyPI `soup-cli`](https://pypi.org/project/soup-cli/) · [trysoup.dev](https://trysoup.dev) · [DOI](https://doi.org/10.5281/zenodo.21771064)
- Доказательная база: [`benchmarks/`](https://github.com/MakazhanAlpamys/Soup/tree/main/benchmarks) · [`notebooks/proof-4gb.ipynb`](https://github.com/MakazhanAlpamys/Soup/blob/main/notebooks/proof-4gb.ipynb)
- Связанные: [LLMs-local — каталог всего для локального запуска ИИ](LLMs-local%20%E2%80%94%20awesome-%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%B2%D1%81%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0%20%D0%98%D0%98%20%28%D0%B4%D0%B2%D0%B8%D0%B6%D0%BA%D0%B8%2C%20UI%2C%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20RAG%2C%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%BE%2C%20%D0%B3%D0%B0%D0%B9%D0%B4%D1%8B%29.md) · [LocallyUncensored — локальная AI-студия](LocallyUncensored%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20AI-%D1%81%D1%82%D1%83%D0%B4%D0%B8%D1%8F%20%28%D1%87%D0%B0%D1%82%2C%20%D0%BA%D0%BE%D0%B4%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%29.md) · [Heretic — abliteration](../Heretic%20%E2%80%94%20%D1%81%D0%BD%D1%8F%D1%82%D0%B8%D0%B5%20safety-%D0%BE%D0%B3%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%B8%D0%B9%20%D1%81%20%D0%BE%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8B%D1%85%20LLM%20%28abliteration%29.md) · [Gemma 4 12B Coder](../Model/Gemma%204%2012B%20Coder%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20%D0%BD%D0%B0%20%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D0%B8%D0%BD%D0%B3%D0%B5%20Fable%205%20%28GGUF%29.md)

#AI #LLM #Файнтюн #Local-LLM #LoRA #Python #GGUF
