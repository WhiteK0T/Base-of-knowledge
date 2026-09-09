---
создал заметку: 2026-09-09T23:10:00
author: WhiteK0T
tags:
  - AI
  - Агенты
  - CLI
  - Python
  - SWE-bench
  - Bash
  - Безопасность
Источник:
  - https://t.me/bugnotfeature/27573
  - https://github.com/SWE-agent/mini-swe-agent
  - https://mini-swe-agent.com
  - https://www.swebench.com/
---

# 🤖 mini-swe-agent — кодинг-агент «в 100 строк»: что здесь правда

**mini-swe-agent** ([github.com/SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent)) — минималистичный агент-программист от команды Принстона и Стэнфорда, которая сделала **SWE-bench** и **SWE-agent**. **7255★, 1000 форков, MIT**, 1022 коммита, 39 контрибьюторов, живёт с 28.06.2025 и активно пилится (последний пуш — 07.09.2026). Сейчас это **v2** (в README висит предупреждение о миграции). Документация: [mini-swe-agent.com](https://mini-swe-agent.com).

> [!info] Коротко
> Проект хороший и честный — но пост пересказывает его рекламный заголовок буквально, а он не про то. **«100 строк»** — это про один файл класса агента (в нём **190 строк**), тогда как установка тянет **618 МБ и 78 пакетов**. **74 %** — это результат **модели** в этой обвязке, а не самой обвязки: тот же агент даёт **9 % с Qwen2.5-Coder 32B и 76,8 % с Claude 4.5 Opus**. А фраза «запускается в безопасных изолированных средах» прямо противоречит их же документации: у CLI `mini` окружение по умолчанию — **`local`, «No isolation»**, команды идут в твою же текущую папку.

---

## ✅ Проверка заявлений из поста

| Заявление | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «исправляет ошибки в ПО, используя всего **100 строк кода**» | ❌ | 100 строк — маркетинговая округлённая цифра **для одного файла** `agents/default.py`, в котором **190 строк** (158 логических). Весь `src/` — **5349 строк в 59 файлах**, а установленный пакет со всеми зависимостями — **618 МБ, 78 пакетов** |
| «в бенчмарках справляется с **74 %** задач на программирование» | ⚠️ | Цифра настоящая и даже устарела в лучшую сторону (**76,8 %**), но это **не заслуга агента**. Это SWE-bench Verified — **500 реальных issue из 12 Python-репозиториев**, и в одной и той же обвязке результат гуляет **от 9 % до 76,8 %** в зависимости от модели |
| «работает с **ЛЮБОЙ** моделью — с Claude тоже» | ✅ | Правда. Работает через `litellm`, есть классы под OpenRouter, Portkey, Requesty, локальные модели через `api_base`. Более того, **топ-1 в их таблице — именно Claude 4.5 Opus** |
| «запускается в **безопасных, изолированных средах**» | ❌ | Изолированные среды **есть, но не по умолчанию**. Их же документация: *«If you run the `mini` CLI, you will run in the `local` environment by default»* и про `local` — *«Executes commands directly on the host machine using `subprocess.run`. **No isolation.**»* |
| «**не перекручивает проект**» | ❌ | В `local`-режиме рабочий каталог — `os.getcwd()`, то есть **твой проект**, и команды выполняются с твоими правами и твоим окружением. Единственная защита из коробки — режим `confirm`, который спрашивает подтверждение перед каждой командой (и отключается флагом `-y`) |

---

## 🔢 Про «100 строк»

Считал сам, по HEAD (`04d809c`, 03.09.2026):

| Файл | Строк | Что это |
| :--- | ---: | :--- |
| `agents/default.py` | **190** (158 без пустых, комментариев и docstring) | тот самый «100-строчный агент» |
| `environments/local.py` | 92 | выполнение команд |
| `models/litellm_model.py` | 164 | обращение к модели |
| `run/mini.py` | 109 | CLI |
| `run/hello_world.py` | 42 | минимальный пример |
| **весь `src/`** | **5349** в 59 файлах | реальный размер проекта |

Формулировка в README при этом аккуратная и не врёт: *«Just some 100 lines of python **for the agent class** (and a bit more for the environment, model, and run script)»*. Пост эту оговорку выкинул и получил «тулза из 100 строк».

> [!warning] «no fancy dependencies» — проверил, это не так
> Ставил в чистый venv и мерил:
> - `pip install mini-swe-agent` → **618 МБ, 78 пакетов**.
> - Самые жирные: `pyarrow` **155,7 МБ**, `litellm` **123 МБ**, `pandas` 73,5 МБ, `numpy` 42,6 + 26,1 МБ, `botocore` 29,7 МБ, `openai` 20,4 МБ, `hf_xet` 11,6 МБ, `tokenizers` 11,2 МБ.
> - `pyarrow`/`pandas`/`numpy` приходят из `datasets`, а он нужен **только раннеру SWE-bench**, но объявлен обычной зависимостью — то есть тянется всем.

**Как поставить вдвое легче** (проверил, `mini` работает):

```bash
python3 -m venv .venv
.venv/bin/pip install --no-deps mini-swe-agent
.venv/bin/pip install pyyaml requests jinja2 'pydantic>=2' 'litellm>=1.75.5' \
  tenacity rich python-dotenv typer platformdirs textual prompt_toolkit
```

Результат — **309 МБ и 71 пакет** вместо 618 МБ и 78. Отваливаются `datasets`, `dill`, `multiprocess`, `numpy`, `pandas`, `pyarrow`, `xxhash`; CLI при этом полностью рабочий, теряется только batch-прогон SWE-bench.

Что до скорости: замерил холодный старт `mini --help` — **0,23–0,24 с**. Их тезис «starts much faster than Claude Code» правдоподобен, тут действительно нет тяжёлого Node-рантайма.

---

## 📈 74 % — это про модель, а не про агента

На [swebench.com](https://www.swebench.com/) есть отдельная таблица **Bash Only** — «every model in the same mini-SWE-agent environment», ровно 500 задач SWE-bench Verified. Вытащил из неё все **60 записей** (все прогнаны через mini). Вот верх, низ и цена:

| % решено | $/задача | вызовов модели | Модель |
| ---: | ---: | ---: | :--- |
| **76,8** | $0,754 | 32,9 | Claude 4.5 Opus (high) |
| **75,8** | $0,356 | 56,1 | Gemini 3 Flash (high) |
| **75,8** | **$0,073** | 60,5 | **MiniMax M2.5 (high)** — открытые веса |
| 75,6 | $0,552 | 28,9 | Claude 4.6 Opus |
| 74,2 | $0,460 | 40,3 | Gemini 3 Pro Preview |
| 72,8 | $0,534 | 76,2 | GLM 5 (high) — открытые веса |
| 70,8 | $0,147 | 51,2 | Kimi K2.5 (high) — открытые веса |
| 60,0 | $0,028 | 46,4 | DeepSeek V3.2 Reasoner |
| 43,8 | $0,532 | 37,5 | Kimi K2 Instruct |
| 26,0 | $0,057 | 27,6 | gpt-oss-120b |
| 21,0 | $0,314 | 48,1 | Llama 4 Maverick |
| **9,0** | $0,068 | 48,2 | **Qwen2.5-Coder 32B Instruct** |

**Разброс — в 8,5 раза при одном и том же коде агента.** Это, собственно, и есть заявленная авторами цель: обвязка нарочно сделана тупой, чтобы таблица мерила модели, а не скаффолды. Но из этого следует ровно обратное посту: 74 % даёт не «100 строк», а фронтир-модель, за которую ты платишь.

> [!tip] Практический вывод из таблицы
> **MiniMax M2.5 (high) — 75,8 % за $0,073 за задачу против 76,8 % за $0,754 у Claude 4.5 Opus.** Один процентный пункт разницы при десятикратной разнице в деньгах. Если гонять агента пачками — смотреть надо именно сюда, а не на верхнюю строку.

Про сам бенчмарк тоже стоит держать в голове: SWE-bench Verified — это **500 отобранных вручную issue из 12 Python-репозиториев**, к каждой есть тесты, проверяющие починку. «74 % задач на программирование» из поста — сильное обобщение: это 74 % конкретных багов в конкретных питоновских проектах, где заранее известно, что фикс существует и проверяем.

---

## 🔓 Про «безопасные изолированные среды»

Цитаты из их же `docs/advanced/environments.md`:

> If you run the `mini` CLI, you will run in the **`local` environment by default**.
>
> **`local`** … Executes commands directly on the host machine using `subprocess.run`. **No isolation.** Directly works in your current python environment.

И код это подтверждает — `environments/local.py`, докстринг класса гласит *«This class executes bash commands directly on the local machine»*, а дальше:

```python
cwd = cwd or self.config.cwd or os.getcwd()
...
subprocess.Popen(command, shell=True, cwd=cwd, env=os.environ | self.config.env, ...)
```

То есть: **shell=True**, рабочий каталог — текущий (твой проект), окружение — **твоё целиком** (`os.environ`), включая все экспортированные токены.

Изолированные среды действительно есть, но их надо **выбрать явно** через `--environment-class`:

| Класс | Что делает |
| :--- | :--- |
| `local` | **по умолчанию**, без изоляции |
| `docker` | `docker exec` в контейнере |
| `singularity` | Singularity/Apptainer, для HPC |
| `bubblewrap` | лёгкая непривилегированная песочница, **только Linux, помечена экспериментальной** |
| `contree` | внешний сервис-песочница [contree.dev](https://contree.dev/) |
| `swerex_docker` / `swerex_modal` | через SWE-ReX, в т.ч. облако Modal |

**bubblewrap** — самый уместный вариант для десктопа: по умолчанию монтирует `/usr`, `/bin`, `/lib`, `/lib64`, `/etc` **только на чтение**, даёт `tmpfs` на `/tmp`, `--unshare-user-try`, `--new-session`, и пишет только в один каталог (`--bind cwd cwd`), по умолчанию свежий `/tmp/minisweagent-<hex>`. Домашний каталог не пробрасывается — значит `~/.ssh`, `~/.aws` и прочее агенту не видны. Оговорка: `--clearenv` там не передаётся, так что **переменные окружения родителя наследуются** — ключи из `export` внутри песочницы всё равно видны.

### Что есть из защиты по умолчанию

| Настройка | Значение по умолчанию | Где |
| :--- | :--- | :--- |
| `agent.mode` | **`confirm`** — спрашивает подтверждение перед каждой командой | `mini.yaml` |
| `whitelist_actions` | пустой список — исключений нет, спрашивает про всё | `interactive.py` |
| `cost_limit` | **$3** на запуск (`-l 0` отключает) | `mini.yaml` |
| `step_limit` | `0` — без ограничения числа шагов | `mini.yaml` |
| `timeout` | 30 с на команду, дальше убивается вся группа процессов | `local.py` |
| `-y` / `--yolo` | режим без подтверждений | CLI |

Режимов три: `human` (ты сам пишешь команды), `confirm` (по умолчанию), `yolo`. Переключаются на лету — `/u`, `/c`, `/y`.

> [!warning] Как запускать, чтобы не было больно
> ```bash
> # песочница + подтверждения + лимит денег
> mini --environment-class bubblewrap -l 1.0 -t "почини падающий тест X"
> ```
> И не давать `-y` на своём рабочем репозитории. Если очень нужен `yolo` — только внутри `docker`/`bubblewrap`.

---

## ⚙️ Как он устроен (и почему это красиво)

Идея авторов честная и стоит того, чтобы её понимать:

- **Никаких инструментов, кроме bash.** Агент не использует tool-calling — значит запускается буквально с любой моделью, и в песочнице не надо ничего доустанавливать, хватает `bash`.
- **`subprocess.run` на каждое действие**, без постоянной shell-сессии. Каждая команда независима — поэтому в промпте прямо написано: *«Directory or environment variable changes are not persistent. Every action is executed in a new subshell»*, и предлагается писать `cd /path && ...`. Взамен получается тривиальная замена `subprocess.run` на `docker exec` и стабильность при масштабировании.
- **Линейная история.** Каждый шаг просто дописывается в список сообщений — траектория и промпт совпадают, удобно для отладки и файнтюна.
- **Завершение по кодовому слову**: агент заканчивает работу командой `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`.

Кто это использует, по README: Meta, NVIDIA, IBM, Essential AI, Nebius, Anyscale, Princeton, Stanford. Плюс на нём построен [SWE-bench Ramp](https://labs.ramp.com/swebench).

Мелочь, которая говорит о качестве сопровождения: в `pyproject.toml` зависимость записана как `litellm >= 1.75.5, != 1.82.7, != 1.82.8` с комментарием *«Security: Skip compromised 1.82.7/8»* — то есть скомпрометированные версии litellm заблокированы явно.

---

## 💻 Установка по системам

Ни в одном дистрибутиве пакета нет — только PyPI (`mini-swe-agent`, сейчас **2.4.6**, `requires-python >= 3.10`, MIT). В AUR тоже пусто (проверял: ни `mini-swe-agent`, ни `swe-agent`), `litellm` не упакован нигде.

### Gentoo (основная)

В ::gentoo нет ни `mini-swe-agent`, ни `litellm`, ни `openai`, ни `textual`. Ставится в venv:

```bash
emerge -av dev-python/pip dev-python/virtualenv sys-apps/bubblewrap  # bubblewrap 0.12.0
python3 -m venv ~/.venvs/mini
~/.venvs/mini/bin/pip install mini-swe-agent
ln -s ~/.venvs/mini/bin/mini ~/.local/bin/mini
```

> [!tip] Чтобы не тащить бинарные колёса
> Тяжёлое из зависимостей в Portage **есть** и собирается из исходников: `dev-python/numpy` 2.5.3, `dev-python/pandas` 3.0.5, `dev-python/pyarrow` 25.0.1, `dev-python/pydantic` 2.13.5, `dev-python/typer` 0.27.2. Собери их через `emerge`, а venv создай с доступом к системным пакетам — pip тогда не будет их скачивать:
> ```bash
> emerge -av dev-python/numpy dev-python/pandas dev-python/pyarrow dev-python/pydantic dev-python/typer
> python3 -m venv --system-site-packages ~/.venvs/mini
> ```
> Либо используй «лёгкий» рецепт выше — без `datasets` эти три пакета вообще не нужны.

Системный Python 3.14.7 требованию `>=3.10` удовлетворяет. Для песочницы: `sys-apps/bubblewrap` 0.12.0, для контейнеров — `app-containers/docker` 29.8.0 или `app-containers/podman` 6.1.0.

### Debian / Ubuntu

```bash
sudo apt install pipx bubblewrap          # bubblewrap: stable 0.11.0, testing 0.12.0
pipx install mini-swe-agent               # pipx: stable 1.7.1, testing 1.15.0
```

`uv` есть только в testing/unstable (0.9.17); в stable его нет — если нужен `uvx`, ставь официальным установщиком. `litellm` в репозиториях отсутствует, приходит из PyPI.

### Arch (с июня 2026)

```bash
sudo pacman -S python-pipx bubblewrap uv podman
pipx install mini-swe-agent
# или разово, без установки:
uvx mini-swe-agent
```

| Пакет | Версия |
| :--- | :--- |
| `extra/python-pipx` | 1.15.0 |
| `extra/bubblewrap` | 0.12.0 |
| `extra/uv` | 0.12.10 |
| `extra/podman` | 6.1.1 |

### Entware / ASUS RT-AX56U (armv7, 512 МБ RAM, 256 МБ flash)

❌ **Не поставится.** `python3` в Entware есть и подходит по версии (**3.13.9-2** при требуемых ≥3.10), но дальше упирается во всё сразу: зависимости весят **309–618 МБ** при 256 МБ flash, `tokenizers` и `hf_xet` — нативные расширения без готовых колёс под armv7, а `litellm` в 123 МБ на 512 МБ RAM сам по себе тяжёлый.

Обходного пути «запустить агента на роутере» тоже нет: среди классов окружений (`local`, `docker`, `singularity`, `bubblewrap`, `contree`, `swerex_*`) нет варианта «выполнять команды по SSH на другой машине» — сам агент всегда живёт рядом с окружением. Роутер тут может быть только целью для отдельно написанного класса окружения.

---

## 🎯 Итог

| | |
| :--- | :--- |
| **Что правда** | Отличный, честно сделанный проект от авторов SWE-bench; MIT; действительно радикально простое ядро; работает с любой моделью; изолированные среды есть; стартует за 0,24 с; 76,8 % на SWE-bench Verified — реальный верх таблицы |
| **Что переврал пост** | «100 строк» — это один файл на 190 строк при 618 МБ зависимостей; «74 % справляется тулза» — справляется **модель**, разброс 9–77 %; «безопасные изолированные среды» — по умолчанию **никакой** изоляции, работа идёт прямо в твоём каталоге |
| **Скрытая цена** | Своя модель и свой ключ. По их же замерам — **$0,03–1,13 за одну задачу**; дефолтный лимит запуска $3 |
| **Как пользоваться** | «Лёгкая» установка (309 МБ) → `--environment-class bubblewrap` → `-l 1.0` → режим `confirm`, без `-y`. Модель выбирать по таблице цены/качества, а не по верхней строке |

Как инструмент — годится и заслуживает внимания, особенно из-за прозрачности: ядро реально можно прочитать за вечер и переписать под себя. Как «ИИ-помощник из 100 строк, который сам всё чинит в песочнице» — такого продукта не существует.

---

## 🔗 Связанные заметки

- Другой агент с заявкой «весь цикл в N строк» — тоже с проверкой: [Waku Agent (ShenSeanChen)](Waku%20Agent%20%28ShenSeanChen%29%20%E2%80%94%20%D1%83%D1%87%D0%B5%D0%B1%D0%BD%D1%8B%D0%B9%20local-first%20%D0%98%D0%98-%D0%B0%D1%81%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BD%D1%82%20%D0%BD%D0%B0%20Python%20%28%D1%86%D0%B8%D0%BA%D0%BB%20%D0%B2%2095%20%D1%81%D1%82%D1%80%D0%BE%D0%BA%2C%20%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D1%8C%20%D0%B2%20SQLite%29%2C%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%C2%AB%D0%BF%D0%BE%D0%BB%D0%BD%D0%BE%D1%81%D1%82%D1%8C%D1%8E%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%C2%BB.md)
- Обзор кодинг-агентов и чем они отличаются: [Сводная таблица AI-агентов для программирования](%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20AI-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BB%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%20%28%D0%B0%D0%B2%D0%B3%D1%83%D1%81%D1%82%202026%29.md)
- Тяжеловесная альтернатива с собственным набором инструментов: [Claude Code — гайд](Claude%20Code%20%E2%80%94%20%D0%B3%D0%B0%D0%B9%D0%B4.md)
- Через что mini общается с моделями: [LiteLLM — единый шлюз к 100+ LLM](../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md)
- Если гонять на локальной модели через `api_base`: [Ollama](../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md)
- Где взять ключ подешевле: [Бесплатные AI-API — подборка провайдеров](../ProxyLLM/%D0%91%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B5%20AI-API%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D1%81%20free-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BE%D0%BC%20%D0%BA%20LLM%20%28OpenRouter%2C%20Groq%2C%20Cerebras%20%D0%B8%20%D0%B4%D1%80.%29.md)

## 🔗 Ссылки

- Репозиторий: [github.com/SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) (MIT) · Документация: [mini-swe-agent.com](https://mini-swe-agent.com)
- Класс агента целиком: [`agents/default.py`](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py) · Окружения: [environments.md](https://mini-swe-agent.com/latest/advanced/environments/)
- Таблица моделей в одной обвязке: [swebench.com → Bash Only](https://www.swebench.com/) · PyPI: [mini-swe-agent](https://pypi.org/project/mini-swe-agent/)
- Учебник авторов по построению минимальных агентов: [minimal-agent.com](https://minimal-agent.com/)
- Источник новости: [@bugnotfeature](https://t.me/bugnotfeature/27573)

#AI #Агенты #CLI #Python #SWE-bench #Bash #Безопасность
