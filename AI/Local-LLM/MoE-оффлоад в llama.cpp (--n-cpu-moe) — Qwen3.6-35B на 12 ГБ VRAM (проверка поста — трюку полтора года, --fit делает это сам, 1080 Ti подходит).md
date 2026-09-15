---
создал заметку: 2026-09-15T10:56:00
author: WhiteK0T
tags:
  - AI
  - LLM
  - LocalLLM
  - llama_cpp
  - MoE
  - Qwen
  - Gemma
  - NVIDIA
Источник:
  - https://t.me/mknewsru/30518
  - https://www.xda-developers.com/old-gpus-are-finally-practical-for-home-server-ai/
  - https://www.xda-developers.com/i-replaced-chatgpt-and-claude-with-this-local-llm/
  - https://www.xda-developers.com/i-built-a-local-llm-workflow-that-runs-on-my-10-year-old-gpu/
  - https://github.com/ggml-org/llama.cpp/pull/15077
  - https://github.com/ggml-org/llama.cpp/pull/16653
---

# 🧩 MoE-оффлоад в llama.cpp — 35B-модель на карте с 12 ГБ VRAM

Разбор [поста @mknewsru от 14.09.2026](https://t.me/mknewsru/30518) («Трюк с ОЗУ позволяет запускать мощные нейромодели даже на картах с небольшим объемом видеопамяти»). Цифры в посте переданы честно. Но в нём не сказано главное: сколько при этом нужно оперативной памяти, что приёму уже полтора года и что свежий llama.cpp делает это **сам, без флагов**.

И важное лично для тебя: в отличие от [FreeToken](FreeToken%20%28FlashML%29%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%B4%D0%BB%D1%8F%20MoE-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B5%D0%B9%20%D0%BD%D0%B0%20%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%BE%D0%BC%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%B5%20%28%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20MoE%2C%20%D0%BD%D1%83%D0%B6%D0%BD%D1%8B%20CUDA%2013%20%D0%B8%20RTX%2030%2B%2C%20Pascal%20%D0%BC%D0%B8%D0%BC%D0%BE%29.md) это **работает на Pascal**. Автор первоисточника гоняет Gemma 4 26B на GTX 1080, а у тебя 1080 Ti с бо́льшим объёмом VRAM.

> [!info] Факты
> | | |
> | :--- | :--- |
> | Пост | [t.me/mknewsru/30518](https://t.me/mknewsru/30518), 14.09.2026, подпись «Мой Компьютер» |
> | Первоисточник | XDA, [«Old GPUs are finally practical for home server AI…»](https://www.xda-developers.com/old-gpus-are-finally-practical-for-home-server-ai/), **12.09.2026**, автор Ayush Pande |
> | Подробные замеры | его же статьи от **01.05.2026** ([Qwen3.6 на RTX 3080 Ti](https://www.xda-developers.com/i-replaced-chatgpt-and-claude-with-this-local-llm/)) и **10.05.2026** ([Gemma 4 на GTX 1080](https://www.xda-developers.com/i-built-a-local-llm-workflow-that-runs-on-my-10-year-old-gpu/)) |
> | Движок | [llama.cpp](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md), `llama-server` |
> | `-ot` (ручная раскладка тензоров) | [PR #11397](https://github.com/ggml-org/llama.cpp/pull/11397), влит **02.04.2025** |
> | `--n-cpu-moe` / `--cpu-moe` | [PR #15077](https://github.com/ggml-org/llama.cpp/pull/15077), влит **04.08.2025** |
> | Автоподбор `--fit` (включён по умолчанию) | [PR #16653](https://github.com/ggml-org/llama.cpp/pull/16653), влит **15.12.2025** |

## ✅ Проверка утверждений поста

| Утверждение | Вердикт | Что на самом деле |
| :--- | :---: | :--- |
| «Qwen3.6-35B-A3B на 12-ГБ RTX 3080 Ti, Q4_K_M, llama.cpp — 25 токенов/с» | ✅ Верно | В статье от 12.09 — «не меньше 25 т/с», в майской — 24 т/с, на её скриншоте — 26,2. **Опущено:** ПК с **32 ГБ ОЗУ**, Windows, `--n-cpu-moe 30`, контекст 65 536. Автор сам пишет, что именно 32 ГБ ОЗУ стали узким местом |
| «Gemma-4-26B-A4B Q4_K_M на GTX 1080 8 ГБ — 14 т/с» | ✅ Верно | В сентябрьской статье «14+», в майской 15 т/с. **Опущено:** Ryzen 5 1600, контейнеру LXC выделено **24 ГБ ОЗУ**, llama.cpp собран с **Vulkan** (CUDA не завелась), драйвер 580.119.02. При 8 ГБ ОЗУ было **2,5–3 т/с**: модель подгружалась с диска |
| «Раньше для 35 млрд параметров требовалось минимум в 2 раза больше памяти» | ⚠️ Подмена | Памяти нужно **столько же**: Q4_K_M весит 19,7 ГиБ. Просто теперь её складывают из VRAM и ОЗУ. Выгружать слои в ОЗУ (`-ngl`) llama.cpp умел всегда, просто это было медленно |
| «MoE — несколько параллельных сетей-экспертов, маршрутизатор выбирает нужные, это снижает нагрузку на видеопамять» | ⚠️ Неточно | Эксперты — не отдельные сети, а маленькие FFN-блоки **внутри каждого слоя**, и выбор делается на каждый токен в каждом слое. Объём памяти MoE **не уменьшает**: все эксперты где-то лежат. Уменьшается **объём вычислений на токен**, поэтому экспертов и можно держать в медленной ОЗУ |
| «Для слоёв в ОЗУ можно использовать CPU для ускорения» | ❌ Наоборот | Экспертов, лежащих в ОЗУ, **считает CPU**, и это не ускорение, а плата за экономию VRAM. Ускоряет как раз GPU: на нём внимание, общие веса и KV-кэш. А на длинных промптах llama.cpp по умолчанию отправляет считаться на GPU даже экспертов из ОЗУ (`--op-offload`) |
| «Главный нюанс — чтобы VRAM+ОЗУ хватало на всю модель» | ✅ Верно, но не всё | Кроме весов нужно место под KV-кэш, вычислительные буферы и саму ОС. Если памяти не хватит, модель пойдёт на диск, и скорость упадёт в разы: у XDA она упала с 15 до 2,5–3 т/с |
| Подача как свежего «трюка» | ⚠️ Не новость | `-ot` существует с апреля 2025-го, `--n-cpu-moe` — с августа 2025-го. С декабря 2025-го `--fit` раскладывает экспертов автоматически и **включён по умолчанию** |

## 🧠 Почему это работает

Возьмём `Qwen3.6-35B-A3B` (данные из `config.json`). В ней **40 слоёв**, в каждом **256 экспертов**, из которых на токен работают **8 маршрутизируемых и один общий**. Маршрутизируемые эксперты — это ~32 из 35 млрд параметров, около 92 % весов. А на каждый токен из них трогается ~3 %.

| Что | Доля весов | Что читается на каждом токене | Где держать |
| :--- | :---: | :--- | :--- |
| Внимание, эмбеддинги, роутер, общий эксперт | ~8 % | всё целиком | **GPU** |
| KV-кэш | зависит от контекста | всё целиком | **GPU** |
| Маршрутизируемые эксперты | ~92 % | 8 из 256 в каждом слое | **ОЗУ** (что влезет — на GPU) |

Скорость генерации упирается в то, сколько байт весов нужно прочитать на токен из медленной памяти. Отсюда разница с плотной моделью (оценка по порядку величин, DDR4 в двухканале отдаёт ≈ 50 ГБ/с):

- **Плотная `Qwen3.6-27B` Q4_K_M (15,7 ГиБ) на твоей 1080 Ti.** В VRAM влезает ~9 ГБ, остальные ~6–7 ГБ лежат в ОЗУ и **читаются целиком на каждом токене**. Потолок получается ~7 т/с, на практике у тебя вышло **~3 т/с**.
- **MoE `Qwen3.6-35B-A3B`.** На каждый токен CPU читает только 8 активных экспертов в выгруженных слоях: это ~25 млн параметров, или ~15 МБ на слой. На 30 выгруженных слоёв выходит **~0,45 ГБ за токен**, в 15 раз меньше. Упор смещается с памяти на CPU и PCIe, и выходит 15–25 т/с.

> [!note] Бонус гибридного внимания: длинный контекст здесь дешёвый
> У `Qwen3.6-35B-A3B` только **10 из 40 слоёв** с полным вниманием (остальные линейные), и у них по 2 KV-головы. KV-кэш в f16 — ~20 КиБ на токен, то есть **~1,25 ГиБ на 65K** и ~5 ГиБ на все 262K. У плотной `Qwen3.6-27B` таких слоёв 16 и по 4 головы: ~100 КиБ на токен, впятеро больше.
> У `Gemma-4-26B-A4B` глобальное внимание только в 5 слоях из 30, у остальных окно 1024 токена. По расчёту это около 2–2,5 ГиБ на 64K.

> [!warning] Цена MoE
> Три миллиарда активных параметров — это не «плотная 35B бесплатно». По качеству MoE обычно проигрывает плотной модели того же полного размера, особенно в рассуждениях ([XDA тоже это отмечает](https://www.xda-developers.com/moe-models-changed-the-hardware-for-local-ai/)). Сравнивай с 27B на своих задачах, а не по числу в названии.

## ⚙️ Флаги: как запускать сегодня

### Вариант 1 — автоматически (рекомендую)

В свежем llama.cpp включён `--fit`. Он оценивает свободную память и раскладывает модель сам: «плотные» части кладёт на GPU, а экспертов слоёв, которые не влезли, отправляет в ОЗУ. Это ровно то, что XDA подбирал руками (проверено по `common/fit.cpp`).

```bash
llama-server -m ~/models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf -c 65536 --host 127.0.0.1 --port 8080
```

> [!danger] Ручные флаги выключают автоподбор
> Если указать `-ngl`, `--n-cpu-moe`, `--cpu-moe` или `-ot`, `--fit` прерывается: в коде это `n_gpu_layers already set by user … abort`. Команды из статей XDA (`-ngl 999 --n-cpu-moe 30`) — это как раз ручной режим. Смешивать нельзя: либо доверяешь `--fit`, либо подбираешь всё сам.
> Если не задан `-c`, `--fit` может **урезать контекст**, чтобы модель влезла (не ниже `--fit-ctx`, по умолчанию 4096). Запас на устройство задаёт `--fit-target` (по умолчанию 1024 МиБ).

### Вариант 2 — вручную, как у XDA

```bash
llama-server -m ~/models/Qwen3.6-35B-A3B-UD-IQ4_XS.gguf \
  -c 65536 -ngl 999 --n-cpu-moe 24 \
  -t 8 -b 2048 -ub 2048 --load-mode none \
  --host 127.0.0.1 --port 8080
```

Раскладку видно в логе запуска: строки `load_tensors: … model buffer size` для GPU и CPU, а также таблица `memory breakdown [MiB]`.

| Флаг | Что делает | Нюанс |
| :--- | :--- | :--- |
| `-ngl 999` | все слои «номинально» на GPU | без следующего флага просто не влезет |
| `--n-cpu-moe N` (`-ncmoe`) | экспертов **первых N слоёв** держать в ОЗУ | начни с числа слоёв (40 у Qwen, 30 у Gemma) и уменьшай, пока хватает VRAM |
| `--cpu-moe` (`-cmoe`) | всех экспертов в ОЗУ | то же, что N ≥ числа слоёв. У XDA на Gemma стояло `40` при 30 слоях — то есть это именно оно |
| `-ot "regex=CPU"` | произвольная раскладка тензоров | например, `-ot "blk\.(2[0-9]\|3[0-9])\.ffn_.*_exps=CPU"` |
| `-t` | потоки CPU | ставь по числу **физических** ядер: экспертов считает именно CPU |
| `-b` / `-ub 2048` | размер батча | быстрее обрабатывает длинный промпт, но растёт вычислительный буфер в VRAM |
| `-ctk q8_0` | квантовать K-кэш | у XDA `-ctv q8_0` на Windows падал |
| `--load-mode none` | загрузить модель в ОЗУ целиком, без mmap | ⚠️ бывший `--no-mmap`: **устарел в v0.3.0 и удалён в v0.4.1 (14.09.2026)**. Команда из статьи XDA на свежей сборке упадёт с `error: invalid argument: --no-mmap`. В сборках до v0.3.0 пиши по-старому |
| `--jinja` | Jinja-шаблон чата | сейчас включён по умолчанию, указывать не нужно |
| `-hf репо:квант` | скачать модель с HF | вместе с ней скачается `mmproj` (зрение), а это лишняя VRAM. Если зрение не нужно, добавь `--no-mmproj` |

Подобрать N лучше замером, `llama-bench` принимает список значений через запятую:

```bash
llama-bench -m ~/models/Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 \
  --n-cpu-moe 20,24,28,32 -p 2048 -n 128 -t 8
```

## 🖥️ Что влезет на твоё железо

Размеры — реальные файлы с Hugging Face ([unsloth/Qwen3.6-35B-A3B-GGUF](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF), [lmstudio-community](https://huggingface.co/lmstudio-community/Qwen3.6-35B-A3B-GGUF), [unsloth/gemma-4-26B-A4B-it-GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF)).

| Модель и квант | Файл | GTX 1080 Ti 11 ГБ + 16 ГБ ОЗУ (27 ГБ) | VPS 7950X3D, 16 ГБ, без GPU |
| :--- | ---: | :--- | :--- |
| Gemma-4-26B-A4B UD-Q4_K_M | 15,8 ГиБ | ✅ Свободно. В VRAM влезут эксперты ≈10 слоёв, ≈9 ГиБ уйдёт в ОЗУ | ❌ Вместе с ОС не влезет |
| Gemma-4-26B-A4B UD-IQ3_XXS | 10,6 ГиБ | ✅ Но зачем, раз влезает Q4 | ✅ Только CPU |
| Qwen3.6-35B-A3B UD-IQ4_XS | 16,5 ГиБ | ✅ Нормально, в ОЗУ ≈9 ГиБ | ❌ |
| Qwen3.6-35B-A3B UD-Q3_K_XL | 15,7 ГиБ | ✅ | ❌ |
| Qwen3.6-35B-A3B Q4_K_M (как у XDA) | 19,7–20,6 ГиБ | ⚠️ **Впритык**: в ОЗУ ≈12 ГиБ, плюс ОС и рабочий стол. Жди свопа | ❌ |
| Qwen3.6-35B-A3B UD-IQ3_XXS | 12,3 ГиБ | ✅ | ✅ Только CPU, контекст держи скромным |
| **RT-AX56U** (512 МБ) | — | ❌ Неприменимо | ❌ |

Раскладка по слоям в таблице — моя оценка по размерам файлов, без KV-кэша и буферов. Точную покажет лог запуска.

**Чего ждать по скорости.** Сам я не мерил. Ориентир такой: у XDA GTX 1080 на 8 ГБ с Ryzen 5 1600 и DDR4 дала 14–15 т/с на Gemma, причём **все** эксперты лежали в ОЗУ. У 1080 Ti на 3 ГБ больше VRAM, значит, часть экспертов останется на GPU. При сопоставимом процессоре и DDR4 разумно ждать **не меньше** этого, то есть **в разы больше твоих ~3 т/с** на плотной 27B. Главная переменная тут — CPU и частота ОЗУ. Точную цифру покажет `llama-bench`.

> [!warning] Pascal: драйвер 580 и CUDA 12, либо Vulkan
> - NVIDIA **убрала Pascal (GTX 10xx) в ветке драйверов 590**. Последняя ветка с поддержкой — **580** ([новость Arch](https://archlinux.org/news/nvidia-590-driver-drops-pascal-support-main-packages-switch-to-open-kernel-modules/)).
> - **CUDA 13 не собирает код под Pascal.** В `ggml-cuda/CMakeLists.txt` архитектура `61` добавляется только при `CUDAToolkit_VERSION < 13`. Для CUDA-сборки нужна CUDA 12.x.
> - **Vulkan** такой проблемы не знает. Автор XDA на GTX 1080 выбрал именно его, потому что с CUDA toolkit намучился.
> - Про fp16 на Pascal (CC 6.1) — см. [заметку про Qwen 27B](../Model/Huihui-Qwen3.8-27B-abliterated%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20Qwen%2027B%20%28%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%20%D0%BE%D1%82%20%D0%B1%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%2C%20262k%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B0%20%D1%82%D1%80%D0%B5%D0%B1%D1%83%D1%8E%D1%82%2069%20%D0%93%D0%91%20KV-%D0%BA%D1%8D%D1%88%D0%B0%29.md).

## 📦 Установка под 1080 Ti

### Gentoo (OpenRC)

В основном дереве есть драйверы 580 (`580.178.04`, стабильный на amd64) и более новые ветки, но они уже без Pascal. Ebuild драйвера сам предупреждает, если ставится версия, не поддерживающая твою карту, и подсказывает маску.

```bash
# 1. Удержать драйвер на ветке 580
echo ">=x11-drivers/nvidia-drivers-590" > /etc/portage/package.mask/nvidia-pascal
emerge --ask --oneshot x11-drivers/nvidia-drivers

# 2. llama.cpp из GURU (sci-misc/llama-cpp, версия 0.3.0) — с Vulkan
eselect repository enable guru && emaint sync -r guru
echo "sci-misc/llama-cpp ~amd64" > /etc/portage/package.accept_keywords/llama-cpp
echo "sci-misc/llama-cpp vulkan openssl" > /etc/portage/package.use/llama-cpp
emerge --ask sci-misc/llama-cpp dev-util/vulkan-tools
vulkaninfo --summary | grep deviceName      # должна быть видна GTX 1080 Ti
```

> [!tip] CUDA вместо Vulkan
> CUDA на Pascal тоже работает, но только 12.x (в дереве есть `12.9.2`, ключевое слово `~amd64`). Понадобится ещё слот gcc, совместимый с этой CUDA:
> ```bash
> echo ">=dev-util/nvidia-cuda-toolkit-13" >> /etc/portage/package.mask/nvidia-pascal
> echo "dev-util/nvidia-cuda-toolkit ~amd64" >> /etc/portage/package.accept_keywords/llama-cpp
> echo "sci-misc/llama-cpp cuda openssl" > /etc/portage/package.use/llama-cpp
> ```

Служба OpenRC (в ebuild её нет, пишем сами):

```bash
useradd -r -d /var/lib/llama -s /sbin/nologin -G video llama   # video — доступ к /dev/nvidia*
mkdir -p /var/lib/llama/models && chown -R llama:llama /var/lib/llama
```

```sh
#!/sbin/openrc-run
# /etc/init.d/llama-server  (chmod +x)

description="llama.cpp OpenAI-compatible server"
command="/usr/bin/llama-server"
command_args="${LLAMA_OPTS}"
command_user="llama:llama"
supervisor="supervise-daemon"
output_log="/var/log/llama-server.log"
error_log="/var/log/llama-server.log"

depend() {
	need localmount
	after net
}

start_pre() {
	checkpath -f -o llama:llama -m 0640 /var/log/llama-server.log
}
```

```sh
# /etc/conf.d/llama-server
# без -ngl/--n-cpu-moe → раскладку сделает --fit
LLAMA_OPTS="-m /var/lib/llama/models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf -c 65536 --host 127.0.0.1 --port 8080"
```

```bash
rc-update add llama-server default && rc-service llama-server start
```

### Debian / Ubuntu (systemd)

- **Debian 13 (trixie).** `nvidia-driver` из non-free — это ветка **550**, Pascal поддерживается. Пакета `llama.cpp` в trixie нет: он есть только в forky/sid (`0.4.0`). Значит, собираем сами с Vulkan. CUDA 12.4 из non-free Pascal тоже поддерживает, но Vulkan проще.
- **Ubuntu 26.04.** Драйвер `nvidia-driver-580`. В universe есть `llama.cpp` (сборка `b8681`) и `libggml0-backend-vulkan`. В этой сборке уже есть `--fit` и `--n-cpu-moe`, но ещё нет `--load-mode` (там пока `--no-mmap`).

```bash
# Debian 13: драйвер + сборка llama.cpp с Vulkan
sudo apt install -y nvidia-driver firmware-misc-nonfree
sudo apt install -y build-essential cmake git libssl-dev libvulkan-dev glslc spirv-headers vulkan-tools
sudo git clone https://github.com/ggml-org/llama.cpp /opt/llama.cpp && cd /opt/llama.cpp
sudo cmake -B build -DGGML_VULKAN=ON
sudo cmake --build build --config Release -j"$(nproc)"

# Ubuntu 26.04: из пакетов
sudo apt install -y nvidia-driver-580 llama.cpp libggml0-backend-vulkan vulkan-tools
```

```ini
# /etc/systemd/system/llama-server.service
[Unit]
Description=llama.cpp server
After=network-online.target

[Service]
User=llama
Group=llama
SupplementaryGroups=video render
# для пакета Ubuntu путь — /usr/bin/llama-server
ExecStart=/opt/llama.cpp/build/bin/llama-server -m /srv/models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf -c 65536 --host 127.0.0.1 --port 8080
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo useradd -r -s /usr/sbin/nologin llama && sudo mkdir -p /srv/models
sudo systemctl daemon-reload && sudo systemctl enable --now llama-server
```

> В Debian forky/sid есть готовый `llama.cpp-services`: юнит плюс переменные `LLAMA_ARG_*` в `/etc/default/llama-server`.

### Arch (systemd)

```bash
# Драйвер: основной nvidia-open (590+) Pascal не поддерживает → ветка 580xx из AUR
yay -S nvidia-580xx-dkms nvidia-580xx-utils

# llama.cpp в extra: llama-cpp + бэкенд ggml. Для Pascal — только Vulkan:
# ggml-cuda собран с CUDA 13.4, в которой нет архитектуры Pascal
sudo pacman -S llama-cpp ggml-vulkan vulkan-tools
```

В пакете уже есть `llama-server.service`. Он запускается в режиме роутера по `/usr/share/llama/models`, с `DynamicUser` и `ProtectHome=yes`, так что модели из `/home` он не увидит. Проще переопределить запуск:

```ini
# sudo systemctl edit llama-server
[Service]
ExecStart=
ExecStart=/usr/bin/llama-server -m /usr/share/llama/models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf -c 65536 --host 127.0.0.1 --port 8080
```

```bash
sudo systemctl enable --now llama-server
```

### Entware (RT-AX56U)

❌ Неприменимо: 512 МБ ОЗУ против 10–20 ГБ, которые нужны модели. На роутер можно поставить разве что прокси к десктопному `llama-server`.

## 🔌 Где ещё есть этот приём

- **[LM Studio](LM%20Studio%20%E2%80%94%20%D0%B4%D0%B5%D1%81%D0%BA%D1%82%D0%BE%D0%BF-GUI%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20LLM.md).** В [0.3.23](https://lmstudio.ai/blog/lmstudio-v0.3.23) появился тумблер «Force Model Expert Weights onto CPU». По жалобам пользователей, в 0.4.0 его заменили слайдером, который выгружает слои целиком ([issue #1421](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1421), на момент заметки открыт). Проверь в своей версии.
- **[FreeToken](FreeToken%20%28FlashML%29%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%B4%D0%BB%D1%8F%20MoE-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B5%D0%B9%20%D0%BD%D0%B0%20%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%BE%D0%BC%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%B5%20%28%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20MoE%2C%20%D0%BD%D1%83%D0%B6%D0%BD%D1%8B%20CUDA%2013%20%D0%B8%20RTX%2030%2B%2C%20Pascal%20%D0%BC%D0%B8%D0%BC%D0%BE%29.md).** Та же идея, только умнее: на GPU держится LRU-кэш «горячих» экспертов. Но нужны CUDA 13 и RTX 30+, так что на 1080 Ti он не пойдёт, а llama.cpp пойдёт.
- **ik_llama.cpp.** Форк llama.cpp, заточенный под CPU и гибридный инференс. Есть в GURU (`sci-misc/ik_llama-cpp`, только live-ebuild) и в AUR (`ik-llama.cpp`, `ik-llama.cpp-vulkan`). Сам не сравнивал.

## 💡 Итог

- **Цифры поста верны** (25 и 14 т/с), первоисточник — XDA от 12.09.2026. Но **пост умалчивает об ОЗУ**: 32 ГБ у машины с 3080 Ti и 24 ГБ у GTX 1080. С 8 ГБ ОЗУ та же Gemma давала 2,5–3 т/с.
- **MoE не уменьшает объём памяти**, он уменьшает вычисления на токен. Поэтому экспертов и можно держать в медленной ОЗУ: модель целиком всё равно должна поместиться в VRAM + ОЗУ.
- **Не новость:** флагу `--n-cpu-moe` год, а с декабря 2025-го `--fit` делает раскладку **сам и по умолчанию**. Ручные `-ngl`/`--n-cpu-moe` автоподбор отключают.
- **`--no-mmap` из статьи XDA удалён в llama.cpp v0.4.1**, теперь это `--load-mode none`.
- **Для твоей 1080 Ti это рабочий путь**, в отличие от FreeToken. Нужны драйвер 580 и Vulkan (или CUDA 12). Начни с **Gemma-4-26B-A4B UD-Q4_K_M** или **Qwen3.6-35B-A3B UD-IQ4_XS**: обе с запасом влезают в 11 + 16 ГБ и должны заметно обогнать плотную 27B с её 3 т/с.

## 🔗 Ссылки

- Пост: [t.me/mknewsru/30518](https://t.me/mknewsru/30518) (14.09.2026)
- XDA: [Old GPUs are finally practical for home server AI](https://www.xda-developers.com/old-gpus-are-finally-practical-for-home-server-ai/) (12.09.2026) · [Qwen3.6-35B-A3B на RTX 3080 Ti](https://www.xda-developers.com/i-replaced-chatgpt-and-claude-with-this-local-llm/) (01.05.2026) · [Gemma 4 26B на GTX 1080](https://www.xda-developers.com/i-built-a-local-llm-workflow-that-runs-on-my-10-year-old-gpu/) (10.05.2026) · [Your old GPU can still run big LLMs](https://www.xda-developers.com/your-old-gpu-can-still-run-llms/) (06.05.2026)
- llama.cpp: [флаги llama-server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) · [PR #11397 (-ot)](https://github.com/ggml-org/llama.cpp/pull/11397) · [PR #15077 (--n-cpu-moe)](https://github.com/ggml-org/llama.cpp/pull/15077) · [PR #16653 (--fit)](https://github.com/ggml-org/llama.cpp/pull/16653)
- Модели: [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) · [google/gemma-4-26B-A4B-it](https://huggingface.co/google/gemma-4-26B-A4B-it) · GGUF: [unsloth Qwen3.6](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF), [unsloth Gemma 4](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF)
- Связанные: [llama.cpp — движок инференса GGUF](llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) · [FreeToken — MoE-движок (не для Pascal)](FreeToken%20%28FlashML%29%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%B4%D0%BB%D1%8F%20MoE-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B5%D0%B9%20%D0%BD%D0%B0%20%D0%BF%D0%BE%D1%82%D1%80%D0%B5%D0%B1%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%BE%D0%BC%20%D0%B6%D0%B5%D0%BB%D0%B5%D0%B7%D0%B5%20%28%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20MoE%2C%20%D0%BD%D1%83%D0%B6%D0%BD%D1%8B%20CUDA%2013%20%D0%B8%20RTX%2030%2B%2C%20Pascal%20%D0%BC%D0%B8%D0%BC%D0%BE%29.md) · [MTP-ускорение в llama.cpp (--fit)](MTP-%D1%83%D1%81%D0%BA%D0%BE%D1%80%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B2%20llama.cpp%20%28Qwen3.6%2027B%29%20%E2%80%94%20%D1%82%D1%8E%D0%BD%D0%B8%D0%BD%D0%B3%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20%28--fit%2C%20vLLM%2C%20%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D1%8B%29.md) · [Qwen 27B на 1080 Ti — ~3 т/с](../Model/Huihui-Qwen3.8-27B-abliterated%20%E2%80%94%20%D1%80%D0%B0%D1%81%D1%86%D0%B5%D0%BD%D0%B7%D1%83%D1%80%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20Qwen%2027B%20%28%D0%B1%D0%B5%D0%BD%D1%87%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%20%D0%BE%D1%82%20%D0%B1%D0%B0%D0%B7%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8%2C%20262k%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B0%20%D1%82%D1%80%D0%B5%D0%B1%D1%83%D1%8E%D1%82%2069%20%D0%93%D0%91%20KV-%D0%BA%D1%8D%D1%88%D0%B0%29.md)

#AI #LLM #LocalLLM #llama_cpp #MoE #Qwen #Gemma #NVIDIA
