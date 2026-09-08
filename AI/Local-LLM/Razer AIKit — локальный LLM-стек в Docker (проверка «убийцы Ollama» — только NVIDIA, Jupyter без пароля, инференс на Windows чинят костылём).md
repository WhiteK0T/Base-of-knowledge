---
создал заметку: 2026-09-08T23:10:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - Local-LLM
  - Docker
  - NVIDIA
  - vLLM
  - Безопасность
Источник:
  - https://t.me/bugnotfeature/26984
  - https://github.com/razerofficial/aikit
  - https://www.razer.ai/aikit/
  - https://hub.docker.com/r/razerofficial/aikit
---

# 🐍 Razer AIKit — «убийца Ollama» на поверку оказался чужой сборкой в Docker

Разбор [поста «Не баг, а фича» от 11.08.2026](https://t.me/bugnotfeature/26984): *«Razer выпустила убийцу Ollama и LM Studio»*. Проект настоящий — [`razerofficial/aikit`](https://github.com/razerofficial/aikit), Apache-2.0, организация Razer на GitHub с 2015 года. Но заголовок не выдерживает ни одной проверки, а конфигурация «расширенного режима» из официального репозитория поднимает **Jupyter Lab без пароля на всех интерфейсах**.

Проверено 08.09.2026 по репозиторию, Docker Hub и файлам конфигурации.

> [!info] Факты о проекте
> | | |
> | :--- | :--- |
> | Репозиторий | [razerofficial/aikit](https://github.com/razerofficial/aikit), создан 30.09.2025 |
> | Звёзд / форков | **202** · 25 |
> | Контрибьюторов | **2** (`aakulish-rz` — 11 коммитов, `matthewg-21` — 1) |
> | Релизов | 5, от v0.2.0 (29.01.2026) до **v0.6.0 (05.08.2026)** |
> | Последний коммит | 05.08.2026 — за неделю до поста, с тех пор тишина |
> | Docker-образ | `razerofficial/aikit:latest`, **9,2 ГБ**, **5 543 загрузки** всего |
> | Лицензия | Apache-2.0 |

## 🚫 Почему это не «убийца Ollama и LM Studio»

Два независимых аргумента.

**Первый — цифры.** Сравнивать всерьёз не с чем:

| Проект | Звёзд | Последняя активность |
| :--- | ---: | :--- |
| [ollama/ollama](https://github.com/ollama/ollama) | **180 469** | 08.09.2026 |
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | **127 513** | 08.09.2026 |
| razerofficial/aikit | **202** | 05.08.2026 |

Разрыв — почти в **900 раз**. За всё время образ скачали 5 543 раза.

**Второй, куда важнее — это разные категории продуктов.** Ollama и LM Studio построены вокруг `llama.cpp` и GGUF: работают на CPU, на AMD, на Apple Silicon, ставятся одним кликом и рассчитаны на потребительское железо. AIKit — обёртка вокруг **vLLM**, движка для батчевой отдачи на серверных картах, и требует NVIDIA с Docker. Он не заменяет Ollama, он решает другую задачу.

> [!important] Своего кода в AIKit почти нет
> Технологический стек по README — целиком чужой опенсорс:
> - **vLLM** — движок инференса;
> - **LlamaFactory** — фреймворк дообучения;
> - **Ray** — распределение по нескольким GPU;
> - **Open WebUI** — тот самый «веб-интерфейс для общения» из поста;
> - **Grafana + Prometheus** — мониторинг;
> - **Jupyter Lab** — ноутбуки.
>
> Вклад Razer — CLI `rzr-aikit` (13 подкоманд) и упаковка всего этого в один образ. Это нормальная и полезная работа, но называть её «убийцей» чего-либо — подмена. Имена версий образа не скрывают устройство: `cuda13.0-torch2.11.0-vllm0.24.0-aikit0.6.0`.

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :--- | :--- |
| «Убийца Ollama и LM Studio» | ❌ Нет | 202 звезды против 180 469; другая категория (vLLM/NVIDIA против llama.cpp/CPU) |
| Скачивание моделей с HuggingFace напрямую | ⚠️ С оговоркой | Нужен `HUGGING_FACE_HUB_TOKEN`, пробрасываемый в контейнер |
| Поддерживает генерацию картинок | ✅ Верно | Заявлено как одна из четырёх ключевых возможностей |
| Поддерживает дообучение | ✅ Верно | Через LlamaFactory, есть ноутбук с LoRA |
| Работает с несколькими GPU | ✅ Верно | Через Ray, есть `rzr-aikit cluster join/run/status` |
| Есть веб-интерфейс | ✅ Верно | Это **Open WebUI**, чужой проект, порт 1919 |
| Есть Jupyter Lab | ✅ Верно | Порт 8888 — и вот тут проблема, см. ниже |
| Собственный CLI `rzr-aikit` | ✅ Верно | 13 подкоманд: `model`, `cluster`, `ui` |
| Всё упаковано в Docker | ✅ Верно | Образ 9,2 ГБ |
| **«Работает на Windows и Linux»** | ⚠️ Сильно приукрашено | Windows — только внутри **WSL 2**, и инференс там официально чинится костылём. Linux — в требованиях только **Ubuntu 22.04/24.04** |
| **Ничего про NVIDIA** | ❌ Умолчание | **Только NVIDIA**, минимум Compute Capability 7.0. Ни AMD, ни Intel, ни Apple, ни CPU |

## 🔴 Безопасность: официальный compose поднимает RCE без пароля

Это главная причина, по которой заметка написана. В [`docker_compose/docker-compose.yaml`](https://github.com/razerofficial/aikit/blob/main/docker_compose/docker-compose.yaml) из «Advanced Mode»:

```yaml
  rzr-aikit:
    image: razerofficial/aikit:latest
    network_mode: host
    command: >
      -c "rzr-aikit cluster run --metrics-export-port 8080 &&
      jupyter lab --NotebookApp.token='' --NotebookApp.password='' --ip=0.0.0.0 --port=8888 "
    volumes:
      - $HOME/.cache/huggingface:/var/aikit/.cache/huggingface
```

**Jupyter Lab без токена, без пароля, на `0.0.0.0`, при `network_mode: host`.** Jupyter Lab — это выполнение произвольного кода. Плюс контейнеру отданы все GPU и примонтирован `~/.cache/huggingface`, где лежит твой токен HuggingFace, если ты хоть раз делал `huggingface-cli login`.

Остальные службы не лучше:

```yaml
  grafana:
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin      # анонимам сразу права администратора

  openwebui:
    environment:
      - WEBUI_AUTH=false                       # аутентификация выключена
      - DEFAULT_USER_ROLE=admin                # все — администраторы
```

Все четыре сервиса — на `network_mode: host`, то есть комментарий «Access: http://localhost:3000» вводит в заблуждение: слушают они на всех интерфейсах.

> [!danger] На Windows README сам просит открыть вход в WSL
> В разделе Prerequisites для Windows 11 предлагается выполнить в PowerShell от администратора:
> ```powershell
> Set-NetFirewallHyperVVMSetting -Name '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -DefaultInboundAction Allow
> ```
> В связке с беспарольным Jupyter на `0.0.0.0` это означает, что любой в твоей сети (кафе, коворкинг, общая Wi-Fi) получает **выполнение кода на твоей машине с доступом к GPU и к токену HuggingFace**.
>
> Справедливости ради: комментарии в самом compose-файле честно пишут `JupyterLab (port 8888, no authentication)` и `no authentication required`. Razer не скрывает — но и не защищает, а пост про это молчит вовсе.

**Что сделать перед запуском:**

```bash
# 1. Не использовать Advanced Mode как есть. Убрать network_mode: host,
#    оставить явные привязки только на петлю:
#      ports: ["127.0.0.1:8888:8888"]
# 2. Вернуть Jupyter пароль:
#      jupyter lab --ip=127.0.0.1 --port=8888       # токен сгенерируется сам
# 3. Grafana:
#      GF_AUTH_ANONYMOUS_ENABLED=false
#      GF_SECURITY_ADMIN_PASSWORD=<свой>
# 4. Open WebUI:
#      WEBUI_AUTH=true
# 5. Не монтировать весь ~/.cache/huggingface, если там лежит рабочий токен —
#    завести отдельный каталог кэша под контейнер.
```

## 🖥️ Железо: только NVIDIA, и не любая

| Требование | Значение |
| :--- | :--- |
| Минимум | Compute Capability **7.0** (Volta) |
| Поддерживаемые архитектуры | Blackwell, Hopper, Ada Lovelace, Ampere, Turing, Volta |
| Не поддерживается | Всё старше Turing — **GTX 10xx (Pascal, CC 6.1) и ниже**, а также AMD, Intel Arc, Apple Silicon и режим CPU |

Заявлены Razer Blade с RTX 20/30/40/50, профессиональные RTX, а также DGX и датацентровые B200/H100/A100/L40S. То есть целевая аудитория — рабочие станции и серверы, а не «поставил на ноутбук вместо LM Studio».

## 🪟 Windows: два признания из документации

В [`docs/known-issues.md`](https://github.com/razerofficial/aikit/blob/main/docs/known-issues.md) лежат две записи, которые многое говорят о зрелости.

**1. Меньше 10 ГБ VRAM — нехватка памяти.** Это поведение vLLM: он резервирует большую долю видеопамяти заранее.

```bash
rzr-aikit model run <your-model> --gpu-memory-utilization 0.8
```

**2. Инференс на Windows просто не работает** — и чинится так:

> *«The AIKit model runs successfully, but inference commands like `rzr-aikit model generate` fail or port 8000 is not accessible.»*
>
> **Solution**: выполнить `python -m http.server --bind 0.0.0.0 8000`, получить ошибку «порт занят vLLM» — *«this is normal»* — и после этого соединение с vLLM заработает.

То есть штатный способ починить сеть в WSL2 — запустить постороннний веб-сервер, чтобы он упал с ошибкой. Это не «работает на Windows», это обход недоделки.

## 📦 Установка на твоих системах

Официально поддерживаются только Windows 11 (через WSL 2) и Ubuntu 22.04/24.04. Но требования сводятся к трём вещам: Docker, драйвер NVIDIA и NVIDIA Container Toolkit — значит запустится на любом дистрибутиве, где они есть.

| Система | Что нужно |
| :--- | :--- |
| **Gentoo** (основная) | Всё есть в основном дереве: `emerge app-containers/docker app-containers/docker-compose app-containers/nvidia-container-toolkit` плюс `x11-drivers/nvidia-drivers`. Дальше `rc-update add docker default`. Проверка — `nvidia-smi` и `docker run --rm --gpus all <образ> nvidia-smi`. Учти: **9,2 ГБ образа** и ещё столько же под модели |
| **Debian / Ubuntu** | Единственная официально протестированная платформа. Docker Engine по гайду Docker, драйвер через `Software & Updates → Additional Drivers`, затем NVIDIA Container Toolkit из репозитория NVIDIA |
| **Arch** | `pacman -S docker docker-compose nvidia nvidia-container-toolkit` (всё в официальных репозиториях), `systemctl enable --now docker`. В требованиях не заявлен, но ничего специфичного для Ubuntu в образе нет |
| **Entware / RT-AX56U** | ❌ **Неприменимо.** armv7, 512 МБ RAM, 256 МБ флеша, нет GPU и нет Docker. Образ на 9,2 ГБ туда не поместится физически |

Минимальный запуск без «расширенного режима» — так безопаснее, поднимается только контейнер AIKit:

```bash
mkdir -p $HOME/.cache/huggingface

docker run -it --rm \
  --gpus all --ipc host \
  -p 127.0.0.1:8888:8888 -p 127.0.0.1:8000:8000 \
  --mount type=bind,source=$HOME/.cache/huggingface,target=/var/aikit/.cache/huggingface \
  --env HUGGING_FACE_HUB_TOKEN=<токен> \
  razerofficial/aikit:latest

# внутри контейнера
rzr-aikit model run deepseek-ai/deepseek-coder-1.3b-instruct
```

> [!note] Отличия от команды из README
> В официальном примере стоят `--network host` и `--restart=unless-stopped`. Заменил на явный проброс портов **только на петлю** и `--rm`: иначе сервисы окажутся доступны из сети, а контейнер будет подниматься при каждой перезагрузке.

## 💡 Кому это может пригодиться

- **Есть NVIDIA-станция или несколько карт, и нужен vLLM + Ray с мониторингом из коробки.** Собрать этот стек руками — работа на день; здесь он в одном образе. Это единственный настоящий плюс проекта.
- **Нужно дообучение** — LlamaFactory внутри, но для одной этой задачи проще взять [Soup](Soup%20%E2%80%94%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20LLM%20%D0%B8%D0%B7%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%B3%D0%BE%20YAML%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20VRAM-%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%D0%B2%D0%B5%D1%80%D0%BD%D0%B0%2C%20%D0%BD%D0%BE%20%D0%BD%D0%B0%20Python%203.13%2B%20pip%20%D1%82%D0%B8%D1%85%D0%BE%20%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%20%D1%81%D1%82%D0%B0%D1%80%D1%83%D1%8E%200.72.4%29.md), он легче и не тянет 9 ГБ.
- **Просто хочется гонять модели локально** — Ollama или LM Studio. Они работают на CPU и на AMD, не требуют Docker и не открывают беспарольный Jupyter. Обзор вариантов — в [LLMs-local](LLMs-local%20%E2%80%94%20awesome-%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%B2%D1%81%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0%20%D0%98%D0%98%20%28%D0%B4%D0%B2%D0%B8%D0%B6%D0%BA%D0%B8%2C%20UI%2C%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20RAG%2C%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%BE%2C%20%D0%B3%D0%B0%D0%B9%D0%B4%D1%8B%29.md).
- **Хочется всё в вебе и локально** — [LocallyUncensored](LocallyUncensored%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20AI-%D1%81%D1%82%D1%83%D0%B4%D0%B8%D1%8F%20%28%D1%87%D0%B0%D1%82%2C%20%D0%BA%D0%BE%D0%B4%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%29.md).

Отдельно про зрелость: **2 контрибьютора**, история коммитов состоит почти целиком из записей вида «Release v0.5.0» — то есть разработка идёт закрыто, наружу выкладываются готовые срезы. Для проекта под брендом Razer это нормально, но означает, что ни ревью изменений, ни реакции сообщества на баги здесь ждать не стоит. Последний коммит — 05.08.2026.

## 🔗 Ссылки

- Пост: [t.me/bugnotfeature/26984](https://t.me/bugnotfeature/26984) (11.08.2026)
- Проект: [GitHub](https://github.com/razerofficial/aikit) · [razer.ai/aikit](https://www.razer.ai/aikit/) · [Docker Hub](https://hub.docker.com/r/razerofficial/aikit)
- Ключевые файлы: [`docker-compose.yaml`](https://github.com/razerofficial/aikit/blob/main/docker_compose/docker-compose.yaml) · [`known-issues.md`](https://github.com/razerofficial/aikit/blob/main/docs/known-issues.md) · [`gpu-compatibility.md`](https://github.com/razerofficial/aikit/blob/main/docs/gpu-compatibility.md)
- Что внутри: [vLLM](https://github.com/vllm-project/vllm) · [LlamaFactory](https://github.com/hiyouga/LLaMA-Factory) · [Ray](https://github.com/ray-project/ray) · [Open WebUI](https://github.com/open-webui/open-webui)
- Связанные: [Soup — файнтюн LLM из одного YAML](Soup%20%E2%80%94%20%D1%84%D0%B0%D0%B9%D0%BD%D1%82%D1%8E%D0%BD%20LLM%20%D0%B8%D0%B7%20%D0%BE%D0%B4%D0%BD%D0%BE%D0%B3%D0%BE%20YAML%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%E2%80%94%20VRAM-%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%D0%B2%D0%B5%D1%80%D0%BD%D0%B0%2C%20%D0%BD%D0%BE%20%D0%BD%D0%B0%20Python%203.13%2B%20pip%20%D1%82%D0%B8%D1%85%D0%BE%20%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%20%D1%81%D1%82%D0%B0%D1%80%D1%83%D1%8E%200.72.4%29.md) · [LLMs-local — каталог локального ИИ](LLMs-local%20%E2%80%94%20awesome-%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%20%D0%B2%D1%81%D0%B5%D0%B3%D0%BE%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0%20%D0%98%D0%98%20%28%D0%B4%D0%B2%D0%B8%D0%B6%D0%BA%D0%B8%2C%20UI%2C%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%2C%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%8B%2C%20RAG%2C%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%BE%2C%20%D0%B3%D0%B0%D0%B9%D0%B4%D1%8B%29.md) · [LocallyUncensored — локальная AI-студия](LocallyUncensored%20%E2%80%94%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20AI-%D1%81%D1%82%D1%83%D0%B4%D0%B8%D1%8F%20%28%D1%87%D0%B0%D1%82%2C%20%D0%BA%D0%BE%D0%B4%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%29.md)

#AI #LLM #Local-LLM #Docker #NVIDIA #vLLM #Безопасность
