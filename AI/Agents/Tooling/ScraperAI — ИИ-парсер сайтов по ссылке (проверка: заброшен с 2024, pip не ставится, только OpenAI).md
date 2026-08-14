---
создал заметку: 2026-08-14T21:40:00
author: WhiteK0T
tags:
  - ScraperAI
  - Парсинг
  - AI
  - Selenium
  - Python
  - XPath
  - OpenAI
Источник:
  - https://t.me/bugnotfeature/26825
  - https://github.com/scraperai/scraperai
  - https://docs.scraper-ai.com
  - https://pypi.org/project/scraperai/
---

# ScraperAI — ИИ-парсер сайтов по ссылке

> [!danger] Короткий вывод
> **Проект заброшен.** Автор написал это прямым текстом в issue #2 (30.05.2025): «У меня сейчас нет времени на этот проект». Последний содержательный коммит — **июнь 2024**, последний релиз на PyPI — **17 апреля 2024**, сайт `scraper-ai.com` отдаёт **502**.
>
> **`pip install scraperai` не работает** на Python 3.13+ — проверил лично, падает на сборке `htmlmin` (`ModuleNotFoundError: No module named 'cgi'`). Это открытый issue #4 (июль 2025) и висящий 3 месяца непринятый PR #7.
>
> **«Любую модель — Claude, GPT, Gemini, Ollama» — неправда.** В коде есть ровно одна реализация — OpenAI. Claude/Gemini/Ollama числятся в разделе README **«Roadmap»**, то есть в планах, которые не сделали.
>
> При этом сама **идея хорошая** и незаслуженно переврана постом: ИИ вызывается **один раз**, чтобы построить XPath-«рецепт», а сам парсинг потом идёт без нейросети. Об этом ниже — и о том, как забрать эту идею без самого ScraperAI.

---

## Что обещает пост

Пост из «Не баг, а фича» ([26825](https://t.me/bugnotfeature/26825)) продаёт ScraperAI так:

1. «Для парсинга достаточно кинуть ссылку на сайт»;
2. «ИИ сам всё найдёт в соответствии с промптом»;
3. «Бот нажимает кнопки, прокручивает страницы, переходит по страницам и выполняет другие действия, **как обычный человек**»;
4. «Под капот можно засунуть **любую модель — Claude, GPT, Gemini, а также локальные модели через Ollama**».

Формулировка «нашли ИИ-парсер» намекает на свежую находку. Репозиторий создан **27 октября 2023 года**, ему почти три года.

---

## Проверка утверждений

| Утверждение поста | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «Достаточно кинуть ссылку» | ⚠️ | CLI действительно запускается как `scraperai --url ...`, но дальше это **интерактивный мастер** из 5–6 шагов, где ИИ предлагает, а вы подтверждаете или правите — вплоть до ручного ввода XPath (`view.py:100`: `Enter xpath to select catalog cards`) |
| «ИИ сам всё найдёт в соответствии с промптом» | ⚠️ | Промпт есть, но это **механизм исправления**, а не ввода: у CLI всего два флага, `--url` и `--log-level`, опции `--prompt` нет. Текстовое описание запрашивается только когда вы отклоняете вариант ИИ (`Enter description of the field(s)`) |
| «Нажимает кнопки, прокручивает, переходит по страницам» | ✅ | Реализовано в `SeleniumCrawler.switch_page()` — три режима: `xpath` (клик), `scroll`, `urls` |
| «…как обычный человек» | ❌ | Никакой имитации человека нет. `_scroll()` — это `window.scrollBy(0, 500)` фиксированным шагом, клик — `elem.click()` по заранее найденному XPath, между страницами `time.sleep(3)`. Ни рандомизации, ни движений мыши |
| «Любую модель — Claude, GPT, Gemini» | ❌ | В `scraperai/llm/` только `base.py` (абстракции) и `openai.py`. Все три класса — `JsonOpenAI`, `VisionOpenAI`, `PythonCodeOpenAI` — обёртки над `langchain_openai.ChatOpenAI`. Claude и Gemini не упоминаются в коде ни разу |
| «…локальные модели через Ollama» | ❌→⚠️ | Из коробки нет. В README это пункт **Roadmap**: «Add support of different LLMs», «Add gpt4all integration». Но обходной путь существует и работает — см. [ниже](#как-всё-таки-подключить-ollama-claude-или-gemini) |
| Проект актуален и живой | ❌ | Последний осмысленный коммит — 26.06.2024. Единственная активность после — внешний PR от 18.09.2025. Автор публично отказался от поддержки |
| `pip install scraperai` работает | ❌ | На Python 3.13/3.14 падает на сборке зависимости. Проверено лично, лог ниже |

---

## Что это на самом деле: «рецепт», а не постоянный ИИ

Главное, что пост упустил, — и это как раз сильная сторона проекта.

ScraperAI **не гоняет нейросеть на каждой странице**. Он использует LLM один раз, на этапе настройки, чтобы получить набор XPath-выражений, и сохраняет их в конфиг (`ScraperConfig`). Дальше работает обычный детерминированный цикл на `lxml`:

```
Настройка (LLM, один раз)          Работа (без LLM, сколько угодно раз)
─────────────────────────          ────────────────────────────────────
скриншот → тип страницы            crawler.get(url)
HTML     → XPath пагинации         tree.xpath(card_xpath)
HTML     → XPath карточки          для каждого поля: tree.xpath(field_xpath)
HTML     → XPath полей             crawler.switch_page(pagination)
        ↓
   ScraperConfig (JSON)  ──────────────► повторно используемый «рецепт»
```

В `scraper.py` (`Scraper.scrape_catalog_items`) нет ни одного обращения к модели — только `html.fromstring` и `tree.xpath`. Это значит:

- парсинг **бесплатный** после настройки — платите только за несколько вызовов при создании конфига;
- результат **воспроизводимый** — никакой недетерминированности LLM в проде;
- конфиг **переносимый** — это обычный JSON, его можно гонять там, где никакого Python-стека с langchain нет (см. раздел про роутер).

Именно это авторы называют «reusable and shareable scraping recipes». Подход правильный, его же используют взрослые инструменты. Проблема не в архитектуре, а в том, что реализация не поддерживается.

### Из чего состоит

| Компонент | Файл | Что делает |
| :--- | :--- | :--- |
| Классификатор страницы | `parsers/webpage_classifier.py` | catalog / detailed_page / captcha / other. По скриншоту через vision-модель, с текстовым fallback |
| Детектор пагинации | `parsers/pagination_detector.py` | XPath кнопки «дальше», бесконечный скролл или список URL |
| Детектор карточки | `parsers/catalog_item_detector.py` | Находит повторяющийся элемент списка |
| Извлекатель полей | `parsers/data_fields_extractor.py` | Статические поля (значение без имени) и динамические (имя+значение, как в таблице характеристик) |
| Минификатор HTML | `utils/html.py` | Выкидывает `script`/`style`/`meta`/`noscript` и все атрибуты кроме `class`/`id`/`name`/`href`/`text`/`src` |
| Краулеры | `crawlers/selenium.py`, `crawlers/requests.py` | Selenium (по умолчанию) и голый `requests` |
| «Агент» | `parsers/agent.py` | Вопреки названию — не агент, а обёртка «спросить модель → провалидировать → до 3 раз переспросить с текстом ошибки» |

---

## Состояние проекта

> [!caution] Автор объявил о заморозке
> Issue #2 «Discontinued models», 30 мая 2025. Вопрос: «Значительная часть используемых моделей снята с поддержки. Проект будут обновлять?»
> Ответ `iakov-kaiumov`: **«Unfortunately I don't have enough time for this project right-now, but you're welcome to open a PR.»**

| Показатель | Значение | Комментарий |
| :--- | :--- | :--- |
| Создан | 27.10.2023 | не новый проект |
| Звёзд / форков | 466 / 64 | скромно |
| Коммитов | 113 | из них 107 — один человек |
| Контрибьюторов | 3 | `iakov-kaiumov` (107), `rrr2rrr` (4), `AnnaLisachenko` (2) |
| Последний коммит | 18.09.2025 | внешний PR, до него — 26.06.2024 |
| Последний релиз на PyPI | **0.0.2, 17.04.2024** | тег 0.0.3 на GitHub есть, на PyPI его нет |
| Лицензия | **GPL-3.0** | копилефт, а не MIT — важно, если строите продукт |
| Сайт `scraper-ai.com` | **502** | обещанный в Roadmap SaaS не запустился |
| Открытых issue | 4 | из них ни одна не закрыта с 2025 года |

Отдельная деталь: workflow `.github/workflows/cd.yml` («Publish to pypi») по данным GitHub Actions API имеет **0 запусков**. Бейдж в README рабочим не является, а релиз 0.0.3 из-за этого до PyPI так и не доехал.

### Открытые issue — это карта поломок

| # | Дата | Суть | Статус |
| :--- | :--- | :--- | :--- |
| #1 | 05.08.2024 | Chromedriver падает (`DevToolsActivePort file doesn't exist`) | Автор ответил «проверю через пару дней» и не вернулся. **Открыт 2 года** |
| #3 | 12.06.2025 | `gpt-4-vision-preview` снята с поддержки | Закрыт |
| #4 | 01.07.2025 | `pip install` не работает на Python 3.13 | **Открыт** |
| #5 | 01.08.2025 | `OSError: Path to the extension doesn't exist` | **Открыт** |
| #7 | 25.05.2026 | PR с однострочным фиксом #4 | **Не влит 3 месяца** |

---

## Мои проверки

### 1. `pip install scraperai` падает на современном Python

Python 3.14.6, чистое виртуальное окружение:

```console
$ python3 -m venv venv && venv/bin/pip install scraperai
...
  File "/tmp/pip-install-.../htmlmin/main.py", line 28, in <module>
      import cgi
  ModuleNotFoundError: No module named 'cgi'
ERROR: Failed to build 'htmlmin' when getting requirements to build wheel
```

Причина: модуль `cgi` **удалён из стандартной библиотеки в Python 3.13** ([PEP 594](https://peps.python.org/pep-0594/)), а `htmlmin` 0.1.12 (последний релиз — 2020 год) импортирует его прямо в `setup.py`. Пакет `scraperai` жёстко тянет `htmlmin`.

Это бьёт по всем актуальным дистрибутивам: в Gentoo, Arch и Debian trixie питон по умолчанию уже 3.13+.

**Обход** — заменить дистрибутив на форк `htmlmin2` (сохраняет тот же импорт `htmlmin`), ровно то, что предлагает непринятый PR #7:

```console
git clone https://github.com/scraperai/scraperai.git
sed -i 's/^htmlmin$/htmlmin2/' scraperai/requirements.txt
venv/bin/pip install ./scraperai
```

После этого установка проходит. Но заметьте, что тянется за собой:

```
langchain-0.1.16  langchain-core-0.1.53  langchain_community-0.0.38
langchain_openai-0.1.7  selenium-4.9.1  numpy-1.26.4  packaging-23.2
```

Это стек **весны 2024 года**, зафиксированный жёсткими пинами `==`. `numpy==1.26.4` не имеет колёс под 3.13/3.14 и собирается из исходников (несколько минут и компилятор C). Ставить такое в системный Python нельзя ни в коем случае — только в изолированный venv.

### 2. Selenium-краулер сломан у всех, кто ставил через pip

Открытый issue #5 никто не диагностировал. Причина находится за одну минуту.

`DefaultChromeWebdriver._setup_options()` безусловно подгружает расширение браузера:

```python
cookies_extension_path = current_dir / 'extensions' / 'cookies.crx'
options.add_extension(cookies_extension_path.__str__())
```

А `MANIFEST.in` в репозитории состоит из **одной строки**:

```
include scraperai/crawlers/webdriver/useragents.txt
```

`cookies.crx` там не указан, поэтому в собранный пакет он не попадает. Проверил и колесо с PyPI, и своё, собранное из исходников, — в обоих есть `useragents.txt` и **нет** `.crx`. Воспроизводится мгновенно, ещё до запуска браузера:

```console
$ venv/bin/python -c "from scraperai.crawlers.webdriver.local import DefaultChromeWebdriver; DefaultChromeWebdriver._setup_options()"
OSError: Path to the extension doesn't exist
```

Итог: **`pip install scraperai` + краулер по умолчанию нерабочи в принципе**. Работает только запуск из каталога склонированного репозитория. Починка — одна строка в `MANIFEST.in`:

```
include scraperai/crawlers/webdriver/extensions/cookies.crx
```

### 3. «Сжатие HTML в 10–20 раз» — на деле в 2–3 раза

Документация утверждает: «Usually this tool allows to decrease HTML size by 10-20 times». Прогнал `minify_html()` на реальных страницах (токены — `tiktoken`, `o200k_base`):

| Страница | HTML до | HTML после | Раз | Токенов до → после | Раз |
| :--- | ---: | ---: | ---: | ---: | ---: |
| news.ycombinator.com | 34 424 | 29 508 | **1,2×** | 11 760 → 10 018 | 1,2× |
| ru.wikipedia.org (Gentoo Linux) | 307 538 | 179 243 | **1,7×** | 99 269 → 59 019 | 1,7× |
| habr.com/ru/articles | 283 610 | 135 056 | **2,1×** | 88 442 → 39 882 | 2,2× |
| ycombinator.com/companies | 28 677 | 12 970 | **2,2×** | 8 398 → 4 030 | 2,1× |
| github.com (страница репозитория) | 315 745 | 123 415 | **2,6×** | 119 866 → 36 446 | **3,3×** |

По байтам — 1,2–2,6×, по токенам чуть лучше (до 3,3× там, где много inline-скриптов: они выкидываются целиком и токенов в них непропорционально много). Заявленные 10–20× не подтверждаются **ни на одной** странице. Порядок величины завышен примерно в пять раз.

Практический смысл: минификатор не спасает от того, что страница вроде Википедии — это всё ещё **59 тысяч токенов на один вызов детектора**. С учётом до трёх ретраев в `ChatModelAgent.query_with_validation` настройка одного парсера легко обходится в сотни тысяч входных токенов.

### 4. Ядро парсинга работает

Собрал `ScraperConfig` руками (без вызовов LLM — просто чтобы проверить движок) для Hacker News, две страницы:

```console
rows: 60 | 0.96 s
{"title": "Qwen 3.8 27B", "site": "huggingface.co"}
```

60 карточек с двух страниц — ровно столько, сколько нужно. Цикл `Scraper` + `RequestsCrawler` работает корректно и быстро.

### 5. Три бага, которые я нашёл в коде

**`extract_mode` — мёртвое поле.** Модель `StaticField` объявляет `extract_mode: Literal['text', 'href', 'src'] = 'text'`, но `grep -r extract_mode` по всему пакету даёт **одно совпадение** — саму декларацию. Ни `extract_static_fields()`, ни `extract_field_by_xpath()` его не читают, там всегда вызывается `get_node_text()`. Проверка:

```python
StaticField(field_name='href_mode', field_xpath='//a', extract_mode='href')  # → 'Заголовок'  (текст!)
StaticField(field_name='src_mode',  field_xpath='//img', extract_mode='src')  # → ''
StaticField(field_name='href_ok',   field_xpath='//a/@href')                  # → '/page/1'   ✅
```

То есть попытка вытащить ссылку или картинку «правильным» способом молча даёт неверные данные. **Обход:** всегда пишите `/@href` и `/@src` прямо в XPath.

**Поле `multiple` всегда `False`.** В `data_fields_extractor.py`:

```python
model.fields[i].multiple = isinstance(model.fields[i], list)
```

Сравнивается сам объект `StaticField` со списком — результат всегда `False`. Проверять надо было `first_value`. Последствие: поля с несколькими значениями (список тегов, размеров, категорий) молча обрезаются до первого, потому что `extract_field_by_xpath` при `multiple=False` возвращает `nodes[0]`.

**Берётся только первый чанк HTML.** Там же:

```python
html_part = TokenTextSplitter(chunk_size=self.max_chunk_size).split_text(html_snippet)[0]
```

Всё, что не влезло в первые 16 000 токенов минифицированного HTML, отбрасывается без предупреждения. Для карточки товара это нормально, для длинной страницы с характеристиками внизу — нет.

---

## Как всё-таки подключить Ollama, Claude или Gemini

Обещания поста в коробке нет, но дорога есть, и она короткая. `JsonOpenAI` прокидывает `**kwargs` прямо в `ChatOpenAI`, значит проходит и `base_url`. Проверил:

```python
from scraperai import JsonOpenAI
m = JsonOpenAI(openai_api_key='ollama', model_name='qwen3', base_url='http://127.0.0.1:11434/v1')
print(m.chat.openai_api_base)   # http://127.0.0.1:11434/v1
```

Значит подходит **любой OpenAI-совместимый эндпоинт**:

| Что подключаем | Как |
| :--- | :--- |
| Локальная модель | [Ollama](../../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md), `base_url='http://localhost:11434/v1'` |
| Claude / Gemini / что угодно | [LiteLLM](../../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md) как шлюз, `base_url='http://localhost:4000'` |
| Бесплатные провайдеры | [подборка free-API](../../ProxyLLM/%D0%91%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B5%20AI-API%20%E2%80%94%20%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B0%D0%B9%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%20%D1%81%20free-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BE%D0%BC%20%D0%BA%20LLM%20%28OpenRouter%2C%20Groq%2C%20Cerebras%20%D0%B8%20%D0%B4%D1%80.%29.md) |

> [!warning] Две оговорки
> `JsonOpenAI` жёстко передаёт `response_format={"type": "json_object"}` — модель обязана уметь строгий JSON-режим. Ollama это поддерживает, часть бесплатных прокси — нет.
>
> Для определения типа страницы используется **vision**-модель (`VisionOpenAI` шлёт base64-скриншот). Локальная замена должна быть мультимодальной. Без неё останется только текстовый fallback-классификатор.

---

## Безопасность и право

> [!danger] В репозиторий вкоммичено чужое расширение браузера с полным доступом к трафику
> `scraperai/crawlers/webdriver/extensions/cookies.crx` — бинарный блоб на 478 КБ, который `DefaultChromeWebdriver` подгружает в Chrome автоматически. Распаковал и посмотрел манифест:
>
> **Название:** `Accept all cookies` (автоматически принимает баннеры о cookies).
> **Права:** `tabs`, `storage`, `webRequest`, `webRequestBlocking`, `webNavigation`, `http://*/*`, `https://*/*`.
>
> То есть расширение может **читать и изменять весь трафик на всех сайтах** в этом профиле браузера. Источник, автор и способ сборки в репозитории не документированы, `update_url` ведёт на Chrome Web Store. Ставить такое в свой основной профиль нельзя. Плюс манифест — **Manifest V2**, поддержка которого в Chrome отключена, так что на актуальном браузере он всё равно не загрузится.

Прочее:

- **`--no-sandbox`** прописан в опциях Chrome безусловно. Это отключает песочницу браузера — а именно она защищает систему, когда вы открываете произвольные сайты из интернета.
- **Список User-Agent устарел на 8 лет.** В `useragents.txt` 848 строк, и самый свежий Chrome в них — **70-й** (октябрь 2018), большинство ещё старше. При этом `get()` подменяет UA через CDP на случайный из этого списка, а реальный браузер — современный Chrome. Client Hints (`sec-ch-ua`) при этом не подменяются. Расхождение «UA говорит Chrome 41, а Client Hints — Chrome 140» является **более сильным сигналом бота**, чем отсутствие подмены вообще. Антибот-системы вроде Cloudflare и DataDome ловят это тривиально.
- **Антидетект образца 2021 года:** `--disable-blink-features=AutomationControlled`, `excludeSwitches`, переопределение `navigator.webdriver`. Публично известные приёмы, детектируемые современными защитами.
- **Ни robots.txt, ни rate limiting.** По всему пакету нет ни одного упоминания robots. Пауз между запросами тоже нет — только `sleep(1)` после перехода и `sleep(3)` после клика по пагинации. Ответственность за нагрузку на чужой сайт целиком на вас. Правовые аспекты парсинга разбирались в заметках про [OpenSERP](../../../Security/OSINT/OpenSERP%20%E2%80%94%20self-hosted%20SERP-API%20%D0%B8%20CLI%20%28Google-Yandex-Baidu%20%D0%B8%20%D0%B4%D1%80.%29%20%D0%B4%D0%BB%D1%8F%20OSINT%2C%20LLM%20%D0%B8%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md) и [Lightpanda](Lightpanda%20%E2%80%94%20headless-%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%20%D0%BD%D0%B0%20Zig%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B8%20%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%D0%BE%D0%B2%2C%20AGPL%2C%20robots.txt%2C%20%D1%87%D0%B5%D0%B3%D0%BE%20%D0%BD%D0%B5%D1%82%29.md).
- **`RequestsCrawler` наивен до предела:** `requests.get(url).text` — без User-Agent, без таймаута, без обработки ошибок. Тестовый запрос к `ozon.ru` вернул мне 5-килобайтную антибот-заглушку вместо страницы.
- **Лицензия GPL-3.0.** Если встраиваете в свой продукт — копилефт распространяется на него. Все перечисленные ниже альтернативы, кроме Firecrawl, лицензированы мягче.

---

## Установка по системам

> [!important] Общее правило
> Ставить **только в venv**, никогда в системный Python: пакет тянет жёсткие пины (`langchain==0.1.16`, `selenium==4.9.1`, `numpy==1.26.4`, `packaging==23.2`), которые снесут вам актуальные версии. И ставить **из git с патчем `htmlmin` → `htmlmin2`**, потому что PyPI-версия 0.0.2 старше репозитория на два года и не соберётся.

Общий подготовительный шаг для всех Linux-систем:

```bash
git clone https://github.com/scraperai/scraperai.git ~/src/scraperai
cd ~/src/scraperai
sed -i 's/^htmlmin$/htmlmin2/' requirements.txt
# фикс открытого issue #5 — иначе Selenium-краулер упадёт
echo 'include scraperai/crawlers/webdriver/extensions/cookies.crx' >> MANIFEST.in

python3 -m venv ~/venv/scraperai
~/venv/scraperai/bin/pip install -U pip
~/venv/scraperai/bin/pip install .
~/venv/scraperai/bin/scraperai --url https://example.com
```

### Gentoo (основная)

В Portage пакета нет и не будет. Нужны компилятор (для сборки `numpy==1.26.4` из исходников — колёс под 3.13/3.14 у неё нет) и браузер для Selenium.

```bash
# питон и заголовки для сборки lxml/numpy
sudo emerge --ask dev-lang/python:3.13 dev-python/pip dev-libs/libxml2 dev-libs/libxslt

# браузер: сборка chromium из исходников — это несколько часов и десятки ГБ
sudo emerge --ask www-client/chromium
```

> [!tip] Сэкономьте часы сборки
> `www-client/chromium` собирается из исходников очень долго. Если ScraperAI нужен на один-два раза, обойдитесь **без браузера вообще**: `RequestsCrawler` не требует Chrome. Потеряете скриншоты (а значит vision-классификатор типа страницы), клик-пагинацию и скролл — останется только пагинация по списку URL. Для статических каталогов этого часто достаточно:
> ```python
> from scraperai import ParserAI, RequestsCrawler
> crawler = RequestsCrawler()
> ```

USE-флаги: для `dev-python/lxml` ничего специфичного не нужно, `libxml2`/`libxslt` подтянутся зависимостями.

### Debian / Ubuntu

Самый спокойный вариант: в стабильных ветках питон обычно 3.11–3.12, где `cgi` ещё на месте и патч `htmlmin` может не понадобиться (но лучше сделать в любом случае).

```bash
sudo apt update
sudo apt install -y python3-venv python3-dev build-essential \
                    libxml2-dev libxslt1-dev git \
                    chromium chromium-driver
```

В Ubuntu chromium ставится как snap, что часто ломает Selenium из-за путей и confinement. Надёжнее взять `chromium-browser` из репозитория Debian либо поставить Google Chrome из официального `.deb`.

### Arch (планируется с июня 2026)

В AUR пакета `scraperai` **нет** (проверил через RPC API — 0 результатов). Питон в Arch — 3.13+, поэтому патч `htmlmin` обязателен.

```bash
sudo pacman -S --needed python python-pip base-devel libxml2 libxslt git chromium
# chromedriver в Arch входит в пакет chromium
```

Если `numpy==1.26.4` откажется собираться на слишком свежем питоне — поставьте отдельный слот через AUR (`yay -S python312`) и создайте venv на нём:

```bash
python3.12 -m venv ~/venv/scraperai
```

### Entware (ASUS RT-AX56U)

> [!danger] Не ставится и ставить не нужно
> Три независимых блокера, проверил по `Packages` для `armv7sf-k3.2`:
> 1. `python3` в Entware — **3.13.9**, то есть ровно та версия, где удалён `cgi`. `htmlmin` не соберётся;
> 2. `python3-numpy` в репозитории — **2.3.4**, а ScraperAI требует `numpy==1.26.4`; сборка 1.26.4 из исходников на armv7 с 512 МБ ОЗУ почти наверняка упадёт по памяти;
> 3. `python3-pandas`, `python3-pydantic`, `chromium`, `chromedriver` — **в репозитории отсутствуют**. Selenium на роутере невозможен в принципе.
>
> Плюс сам стек langchain + openai + pandas — это сотни мегабайт на разделе, где всего 256 МБ флеша.

Но полезное на роутере всё-таки сделать можно, и здесь пригождается архитектура «рецептов». **Конфиг настраивается на десктопе, а исполняется на роутере обычным `lxml`** — сам `scraperai` для этого не нужен:

```bash
opkg install python3-light python3-lxml python3-urllib python3-openssl
```

Проверенный скрипт-исполнитель (нужны только `lxml` и `requests`; выдал те же 60 строк, что и полноценный `Scraper`, — и, в отличие от него, корректно вытащил ссылки):

```python
#!/opt/bin/python3
# запуск: ./run_config.py config.json
import json, sys, urllib.request
from lxml import html, etree

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', 'replace')

def run(cfg):
    rows = []
    for url in ([cfg['start_url']] + cfg['pagination'].get('urls', []))[:cfg['max_pages']]:
        tree = html.fromstring(fetch(url))
        for node in tree.xpath(cfg['catalog_item']['card_xpath']):
            row = {}
            for f in cfg['fields']['static_fields']:
                xp = f['field_xpath']
                xp = xp if xp.startswith('.') else '.' + xp
                vals = [v if isinstance(v, str)
                        else etree.tostring(v, method='text', encoding='unicode').strip()
                        for v in node.xpath(xp)]
                row[f['field_name']] = vals if f.get('multiple') else (vals[0] if vals else None)
            rows.append(row)
            if len(rows) >= cfg['max_rows']:
                return rows
    return rows

print(json.dumps(run(json.load(open(sys.argv[1]))), ensure_ascii=False, indent=1))
```

Тридцать строк без единой зависимости от ScraperAI, langchain и OpenAI — зато работают на роутере, в cron, годами и бесплатно. Это, по сути, и есть вся ценность подхода в чистом виде.

---

## Чем заменить

Если нужен ровно тот инструмент, который описан в посте, — берите не ScraperAI. Состояние на 14.08.2026:

| Проект | Звёзд | Лицензия | Последний push | Любые LLM (Claude/Gemini/Ollama) |
| :--- | ---: | :--- | :--- | :--- |
| **[ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai)** | 29 526 | MIT | 20.07.2026 | ✅ OpenAI, Groq, Azure, Gemini, **Ollama** — заявлено в README |
| **[crawl4ai](https://github.com/unclecode/crawl4ai)** | 78 122 | Apache-2.0 | 13.08.2026 | ✅ через LiteLLM: `provider="ollama/qwen2"` и что угодно ещё |
| **[Firecrawl](https://github.com/firecrawl/firecrawl)** | 167 364 | AGPL-3.0 | 14.08.2026 | ⚠️ упор на облако, self-host есть |
| **[Scrapy](https://github.com/scrapy/scrapy)** | 63 845 | BSD-3 | 14.08.2026 | ❌ без ИИ, но это индустриальный стандарт |
| ScraperAI | 466 | GPL-3.0 | 18.09.2025 | ❌ только OpenAI |

**ScrapeGraphAI** — самая точная замена: та же идея «ссылка + промпт → структурированные данные», но многопровайдерная по-настоящему и живая. **crawl4ai** — если нужен упор на подготовку данных для LLM и Markdown-выдачу. Для чистого парсинга без ИИ по-прежнему вне конкуренции **Scrapy**.

---

## Стоит ли смотреть

| Кому | Вердикт |
| :--- | :--- |
| Хочу «кинуть ссылку и получить данные» | ❌ Берите ScrapeGraphAI или crawl4ai |
| Хочу локальную модель / Claude / Gemini | ❌ Из коробки нет; обход через `base_url` возможен, но проект всё равно не поддерживается |
| Нужен рабочий инструмент в продакшн | ❌ Заброшен, `pip install` сломан, Selenium-краулер сломан |
| Хочу разобраться, как устроен ИИ-парсер | ✅ Кодовая база маленькая (~2500 строк), читается за вечер, архитектура «рецептов» правильная |
| Нужна сама идея «LLM один раз → XPath навсегда» | ✅ Забирайте идею, реализацию пишите свою — она умещается в 30 строк |

---

## Связанные заметки

- [Lightpanda — headless-браузер на Zig для ИИ-агентов и парсинга](Lightpanda%20%E2%80%94%20headless-%D0%B1%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80%20%D0%BD%D0%B0%20Zig%20%D0%B4%D0%BB%D1%8F%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B8%20%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3%D0%B0%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%D0%BE%D0%B2%2C%20AGPL%2C%20robots.txt%2C%20%D1%87%D0%B5%D0%B3%D0%BE%20%D0%BD%D0%B5%D1%82%29.md) — альтернатива Selenium там, где браузер всё-таки нужен
- [PixelRAG — RAG по скриншотам страниц вместо HTML](PixelRAG%20%E2%80%94%20RAG%20%D0%BF%D0%BE%20%D1%81%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%D0%B0%D0%BC%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20HTML%20%28visual%20RAG%2C%20VLM-%D1%8D%D0%BC%D0%B1%D0%B5%D0%B4%D0%B4%D0%B8%D0%BD%D0%B3%D0%B8%2C%20%D0%BF%D0%BB%D0%B0%D0%B3%D0%B8%D0%BD%20Claude%20Code%29.md) — противоположный подход: не минифицировать HTML, а смотреть на страницу глазами
- [pdf-inspector (Firecrawl) — PDF в Markdown на Rust без OCR](pdf-inspector%20%28Firecrawl%29%20%E2%80%94%20PDF%20%D0%B2%20Markdown%20%D0%BD%D0%B0%20Rust%20%D0%B1%D0%B5%D0%B7%20OCR%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%C2%AB%D1%81%D0%B0%D0%BC%D0%BE%D0%B3%D0%BE%20%D0%B1%D1%8B%D1%81%D1%82%D1%80%D0%BE%D0%B3%D0%BE%C2%BB%3A%20%D1%8D%D1%82%D0%BE%20%D1%80%D0%BE%D1%83%D1%82%D0%B5%D1%80%20%D0%BA%20OCR%2C%20%D1%81%D0%B2%D0%BE%D0%B8%20%D0%B7%D0%B0%D0%BC%D0%B5%D1%80%D1%8B%20%D0%B8%20%D1%87%D1%82%D0%BE%20%D0%BB%D0%BE%D0%BC%D0%B0%D0%B5%D1%82%D1%81%D1%8F%29.md) — та же логика «дешёвый детерминированный проход вместо дорогой модели»
- [hh-ai-agent — ИИ-агент авто-откликов на HH.ru (Ollama + Playwright)](../hh-ai-agent%20%28fikstt2%29%20%E2%80%94%20%D0%98%D0%98-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%20%D0%B0%D0%B2%D1%82%D0%BE-%D0%BE%D1%82%D0%BA%D0%BB%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%BD%D0%B0%20HH.ru%20%28Ollama%2BPlaywright%29%20%2B%20%D1%80%D0%B5%D0%B2%D1%8C%D1%8E%20%D0%BA%D0%BE%D0%B4%D0%B0.md) — рабочий пример связки локальной модели и браузерной автоматизации
- [Ollama — менеджер и сервер локальных LLM](../../Local-LLM/Ollama%20%E2%80%94%20%D0%BC%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%B5%D1%80%20%D0%B8%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md) — тот самый `base_url` для обхода
- [LiteLLM — единый шлюз (proxy) к 100+ LLM](../../ProxyLLM/LiteLLM%20%E2%80%94%20%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9%20%D1%88%D0%BB%D1%8E%D0%B7%20%28proxy%29%20%D0%BA%20100%2B%20LLM.md) — как подсунуть Claude или Gemini туда, где ждут OpenAI
- [OpenSERP — self-hosted SERP-API для OSINT и автоматизации](../../../Security/OSINT/OpenSERP%20%E2%80%94%20self-hosted%20SERP-API%20%D0%B8%20CLI%20%28Google-Yandex-Baidu%20%D0%B8%20%D0%B4%D1%80.%29%20%D0%B4%D0%BB%D1%8F%20OSINT%2C%20LLM%20%D0%B8%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8%20%28%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80%2C%20%D0%BF%D1%80%D0%B0%D0%B2%D0%BE%29.md) — правовая сторона парсинга
- [92 AI-сервиса — шпаргалка по назначению](../../92%20AI-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%B0%20%E2%80%94%20%D1%88%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0%20%D0%BF%D0%BE%20%D0%BD%D0%B0%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8E%20%28%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%29.md)

---

## Ссылки

- Репозиторий: <https://github.com/scraperai/scraperai>
- Документация: <https://docs.scraper-ai.com>
- PyPI (0.0.2, апрель 2024): <https://pypi.org/project/scraperai/>
- Issue #2 — заявление автора о заморозке: <https://github.com/scraperai/scraperai/issues/2>
- Issue #4 — pip не ставится на Python 3.13: <https://github.com/scraperai/scraperai/issues/4>
- Issue #5 — `Path to the extension doesn't exist`: <https://github.com/scraperai/scraperai/issues/5>
- PR #7 — фикс, висящий с мая 2026: <https://github.com/scraperai/scraperai/pull/7>
- PEP 594 (удаление `cgi` из stdlib): <https://peps.python.org/pep-0594/>
- Исходный пост: <https://t.me/bugnotfeature/26825>

#ScraperAI #Парсинг #AI #Selenium #Python #XPath #OpenAI #Ollama
