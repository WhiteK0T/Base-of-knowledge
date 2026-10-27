---
создал заметку: 2026-10-27T04:30:00
author: WhiteK0T
tags:
  - GPU
  - NVIDIA
  - CUDA
  - Hardware
  - LocalLLM
  - ComfyUI
  - vLLM
  - Linux
  - Kernel
  - Gentoo
Источник:
  - https://t.me/prohitec/15091
  - https://github.com/Zagitta/gpu-unlock
  - https://github.com/JustAResearcher/gpu-unlock-ada
  - https://github.com/haohervchb/Turing-unlock
  - https://github.com/KohakuBlueleaf/KohakUnlock
  - https://wccftech.com/nvidia-geforce-rtx-30-gpus-get-up-to-2x-faster-ai-compute-performance-with-new-gpu-unlock-mod-real-world-gains-of-up-to-60/
  - https://xenospectrum.com/en/gpu-unlock-rtx-3090-ti-benchmarks/
---

# ⚡ GPU Unlock — полная скорость тензорных ядер на GeForce RTX 20/30/40

Разбор [поста @prohitec от 26.10.2026](https://t.me/prohitec/15091) «Моддеры разблокировали скрытую производительность ИИ на видеокартах NVIDIA RTX 20, 30 и 40 серий». Его заголовок совпадает с новостью VideoCardz. В октябре 2026 энтузиасты нашли способ снять с потребительских GeForce искусственное ограничение. Тензорные ядра считают FP16/BF16/TF32 с FP32-аккумулятором вдвое медленнее, чем на профессиональных картах того же кристалла. Разблокировку делает модуль ядра Linux. Он загружается из initramfs **до драйвера NVIDIA**, VBIOS не прошивает, и после выключения питания карта снова работает как стоковая.

Суть в посте передана верно. Но его цифры взяты из **четырёх разных проектов и тестов**, и на практике прирост сильно зависит от задачи: от двукратного в синтетике до нуля в квантованном llama.cpp.

> [!warning] Твоя GTX 1080 Ti — мимо
> У Pascal (GTX 10xx) **нет тензорных ядер**, разблокировать нечего. Поддерживаются только карты с тензорными ядрами, нормально пока только RTX 30 и RTX 4090. Остальная серия 40 экспериментальна, а серия 20 пока на уровне исследований (подробности ниже).

> [!info] Факты
> | | |
> | :--- | :--- |
> | Пост | [t.me/prohitec/15091](https://t.me/prohitec/15091), 26.10.2026 21:07 МСК |
> | Основной проект (RTX 30) | [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) 1.1.0: создан 18.10.2026, ~10,6 тыс. ★, модуль под GPL-2.0-only |
> | Форк для RTX 40 | [JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada) 1.1.1: создан 23.10.2026, ~4,1 тыс. ★, GPL-2.0 |
> | RTX 20 (исследования) | [haohervchb/Turing-unlock](https://github.com/haohervchb/Turing-unlock) (одна ASUS 2080 Ti, UEFI-приложение) и [KohakuBlueleaf/KohakUnlock](https://github.com/KohakuBlueleaf/KohakUnlock) (TU102 через initramfs) |
> | Как работает | модуль ядра `gpu_unlock` в initramfs → эксплойт подписанной прошивки NVIDIA → запись регистров скорости → сброс FLR → стоковый драйвер `nvidia` |
> | ОС | Linux x86_64 (готовые пакеты для Arch, Debian/Ubuntu, Fedora). Под Windows есть только сторонние порты |
> | Сохраняется ли | нет: сбрасывается при выключении питания, после сна модуль разблокирует заново |

## 🧠 Что на самом деле разблокируется

**Почему GeForce медленнее.** У GeForce и профессиональных карт общие кристаллы: RTX 3090 и RTX A6000 сделаны на GA102, RTX 4090 и RTX 6000 Ada на AD102. NVIDIA различает их в том числе тем, что на GeForce **матричные операции с FP32-аккумулятором** выполняются на половинной скорости. Это FP16 и BF16 (на Ampere и Ada ещё TF32, на Ada ещё FP8). В спецификации RTX 4090 это видно прямо: FP16 с FP16-аккумулятором даёт 330 TFLOPS, а с FP32-аккумулятором только 165. При этом PyTorch, cuBLAS и почти все фреймворки обучения и диффузии считают именно с FP32-аккумулятором, потому что он точнее.

**Где сидит ограничение.** Скорость выдачи инструкций задают два регистра SM:

| Регистр | Адрес | Что делает |
| :--- | :--- | :--- |
| `FEAT_OVR_SM_SPD` (SS0) | `0x0082381c` | восемь 4-битных полей: DP, FFMA, FMLA16, **FMLA32**, IMLA0–3 |
| `FEAT_OVR_SM_SPD_1` (SS1) | `0x00823820` | одно поле: IMLA4 |

В каждом поле бит 3 включает переопределение, а биты 2:0 задают скорость (`000` значит полная, `001` половина). Цель простая: записать `SS0 = 0x88888888` и `SS1 = 0x8`. Но с хоста эти регистры не пишутся. Доступ к ним задаёт маска привилегий `FEAT_OVR_PLM` (`0x00823804`, по умолчанию `0xffffff8f`), а она разрешает запись только высшему уровню L3, то есть коду в режиме heavy-secure.

**Как обходят.** Проект использует цепочку, которую раньше нашли при разблокировке майнинговых CMP-карт ([cmpunlocker](https://github.com/amoghmunikote/cmpunlocker), V67 от Jon Pry):

1. Драйвер при старте карты запускает на процессоре безопасности SEC2 подписанную прошивку **Booter**. Она расшифровывает и загружает GSP-RM.
2. NVIDIA публиковала и отладочный Booter. Он был зашифрован известным тестовым ключом, его расшифровали и нашли переполнение буфера на стеке.
3. Payload V67 через ROP-цепочку выполняет одну запись в режиме heavy-secure: `FEAT_OVR_PLM = 0xFFFFFFFF`.
4. Теперь SS0 и SS1 пишутся с хоста. Модуль записывает полную скорость, делает FLR (сброс PCIe-функции), и **немодифицированный** драйвер `nvidia` поднимает карту как обычно.

Всё это должно случиться, пока драйвер NVIDIA ещё не трогал карту. Поэтому модуль загружается из initramfs, а запустить его вручную после загрузки системы не выйдет. Подробно механизм описан в [How Ampere was unlocked](https://github.com/Zagitta/gpu-unlock/blob/main/docs/How%20Ampere%20was%20unlocked.md).

**Что не меняется.** Число CUDA-ядер, SM и тензорных ядер, объём и пропускная способность VRAM, скорость INT8/INT4, FP16 с FP16-аккумулятором (он и так полноскоростной) и обычный FP32 на шейдерах остаются прежними.

## 📊 Цифры и откуда они

**Синтетика.** Это пиковая скорость выдачи инструкций или большие GEMM:

| Карта | Тест | До → после | Источник |
| :--- | :--- | :--- | :--- |
| RTX 4090 | FP16→FP32, скорость выдачи MMA | 165,6 → **331,6** TFLOPS | [README gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada) |
| RTX 4090 | BF16→FP32, то же | 165,5 → 330,6 TFLOPS | там же |
| RTX 4090 | реальный cuBLAS GEMM (независимый замер, 450 Вт) | FP16 **+12–34%**, BF16 **+16–20%** (на 4096³ без изменений) | там же |
| RTX 3090 Ti | GEMM 8192³, 450 Вт | FP16 87,5 → 118,4 · BF16 87,5 → **157,4** · TF32 42,6 → 82,6 | [README Zagitta](https://github.com/Zagitta/gpu-unlock), [issue #1](https://github.com/Zagitta/gpu-unlock/issues/1) |
| RTX 3090 Ti | GEMM, другой владелец | FP16 84,6 → 150,6 · BF16 83,4 → 149,5 · TF32 41,0 → 75,9 | [issue #1](https://github.com/Zagitta/gpu-unlock/issues/1) |
| RTX 3090 | PyTorch GEMM 8192³ FP16→FP32 | 73,0 → 122,8 TFLOPS | [KohakUnlock](https://github.com/KohakuBlueleaf/KohakUnlock) |
| RTX 2080 Ti | `mmapeak` FP16→FP32 | 59,9 → **111,0** TFLOPS | KohakUnlock, карты Leadtek с допаянной памятью 22 ГБ |
| RTX 2080 Ti | MMA FP16→FP32 / cuBLAS 8192 | 46,9 → 93,7 / 48,1 → 85,2 TFLOPS | [Turing-unlock](https://github.com/haohervchb/Turing-unlock), стоковая ASUS 11 ГБ |

Пояснения к таблице:

- **331,6 TFLOPS у 4090** — это скорость выдачи инструкций, она удвоилась ровно. В реальных GEMM прирост меньше, потому что разблокированный чип быстрее упирается в лимит мощности (346 Вт против 313 Вт у стоковой карты на тех же задачах). До RTX 6000 Ada (≈364 TFLOPS) 4090 всё равно немного не дотягивает: у неё 128 SM против 142.
- **2080 Ti.** Пост ссылается на Turing-unlock, но число 59,9 → 111 взято из KohakUnlock. Это другой проект и другая карта, с допаянной памятью. В Turing-unlock на стоковой ASUS получилось 46,9 → 93,7. Удвоение есть в обоих случаях. На Turing нет BF16 и TF32, поэтому ускоряется только FP16 с FP32-аккумулятором.
- **FP16 на 3090 Ti в README прибавил только 35%**, а BF16 80%. У другого владельца на той же модели FP16 тоже прибавил почти 80%. Похоже, первый замер упёрся в мощность или частоты, а не в разблокировку.

**Реальные задачи:**

- **ComfyUI на RTX 3090 Ti** (замеры с Reddit, [u/under-_-null](https://www.reddit.com/r/StableDiffusion/comments/1xdoh8k/i_tested_the_rtx_30series_gpu_unlock_up_to_59/)): MOSS-Image SFT в BF16 71,98 → 45,40 с (**+58,6%**), Qwen-Image 2.1 Turbo **+57,2%**, Z-Image Turbo **+56,1%**, MiniMax H3 (видео со звуком) 253,3 → 158,1 с (+60,2%), FLUX.1 dev из FP8-чекпойнта +54,6% (внутри всё равно считает в BF16), LTX-2.5 +16,8%. Та же MOSS-Image в INT8 даёт **+0,3%**. Картинки до и после совпадают побайтно.
- **LLM, prefill (обработка промпта):** прирост зависит от формата весов и движка:
  - vLLM на RTX 3090 даёт +33% ([#25](https://github.com/Zagitta/gpu-unlock/issues/25));
  - vLLM W4A16 на RTX 3090 даёт prefill +25–50% и −20–35% Дж на токен ([#107](https://github.com/Zagitta/gpu-unlock/issues/107));
  - 4×RTX 3090 с лимитом 240 Вт на Qwen 27B в BF16 дают только +10% ([#2](https://github.com/Zagitta/gpu-unlock/issues/2));
  - **llama.cpp с GGUF Q8_0** на 3090 + 3060 даёт **−0,5%**, то есть без изменений (тоже [#2](https://github.com/Zagitta/gpu-unlock/issues/2));
  - квантованная MoE на RTX 4090 48 ГБ даёт 0,98× (README gpu-unlock-ada).
- **Генерация токенов почти не меняется.** Декодирование упирается в пропускную способность памяти, а не в тензорные ядра.
- **Игры и DLSS:** прироста никто не показал, и ждать его неоткуда. В играх тензорные ядра почти не участвуют, а там, где участвуют (DLSS), упора в FP32-аккумулятор нет.

**Правило большого пальца.** Разблокировка помогает там, где время уходит на **матричные умножения FP16, BF16 или TF32 (на Ada ещё FP8) с FP32-аккумулятором**:

- обучение и LoRA;
- диффузионные модели в BF16 (Flux, Qwen-Image, видео);
- prefill и большие батчи в vLLM или SGLang на BF16 и W4A16-весах.

Почти не помогает квантованным GGUF в llama.cpp, INT8 и INT4, генерации токенов и играм. Если модель в FP32, включи TF32: `torch.set_float32_matmul_precision("high")`. По умолчанию PyTorch считает матмулы в честном FP32, и разблокировка их не затронет.

## 🧩 Какие карты поддерживаются и каким проектом

| Серия | Чипы | Проект | Статус на 27.10.2026 |
| :--- | :--- | :--- | :--- |
| **RTX 30** (Ampere), десктоп и ноутбуки | GA102, GA103, GA104, GA106 | [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) | основной путь: пакеты, `targets=all`, десятки отчётов о совместимости в issues (3060…3090 Ti, ноутбучные 3050…3080 Ti) |
| RTX 3050 6 ГБ | GA107 (`2584`) | gpu-unlock-ada | одна карта |
| **RTX 4090** | AD102 (`2684`) | [gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada) | работает, несколько независимых повторов. Payload взят из [TOTORONG/AD103_win_unlocker](https://huggingface.co/TOTORONG/AD103_win_unlocker) |
| 4090 D, 4080 / 4080 SUPER, 4070 Ti / Ti SUPER, 4070 / 4070 SUPER, 4060 Ti, 4060, ноутбучные 4050–4090 | AD102–AD107 | gpu-unlock-ada | **экспериментально**: на каждую модель свой флаг вида `gpu_unlock.ad103_experimental=1`, обязателен точный PCI-адрес, `all` их не выбирает. Проверено на 1–3 картах |
| **RTX 20** (Turing) | TU102 (2080 Ti) | Turing-unlock, KohakUnlock | **исследования**: привязка к конкретной плате и прошивке, нет установщика и автоприменения. Turing-unlock прямо пишет, что это не установщик для всех |
| RTX 50 (Blackwell) | — | — | не поддерживается, только как цель исследований |
| GTX 10 и старше (Pascal…) | — | — | тензорных ядер нет, разблокировать нечего |

**Windows.** Основной путь здесь Linux. Под Windows есть сторонние порты: [impacifist/Windows-GPU-UNLOCK](https://github.com/impacifist/Windows-GPU-UNLOCK) для Ampere (автор Zagitta его не сопровождает), путь через UEFI для 4090 в KohakUnlock и [эталонный порт для одной MSI RTX 4070 Ti](https://github.com/JustAResearcher/gpu-unlock-ada/tree/main/windows/ad104-msi) в gpu-unlock-ada.

## ⚠️ Риски и ограничения

- **Это эксплойт прошивки NVIDIA**, который выполняет код на карте с высшими привилегиями. Автор Zagitta считает повреждение «очень маловероятным»: троттлинг и управление питанием остаются штатными. Исследовательские репозитории (Turing-unlock, KohakUnlock) прямо предупреждают о зависаниях, незагрузке и порче данных. Не тестируй на машине с важной работой и держи под рукой обычный пункт загрузки без параметра. NVIDIA модификацию никак не комментировала. Гарантия — на твой риск.
- **Первая попытка — только после полного выключения питания.** После тёплой перезагрузки карта может сохранить состояние WPR2, и тогда модуль откажется работать. На одних платах это проходит, на других нет.
- **Экран основной карты** гаснет от сброса до момента, когда управление подхватит `nvidia-drm`. Это нормально.
- **Сон.** Suspend-to-RAM обесточивает карту. Zagitta после пробуждения разблокирует заново (параметр `gpu_unlock.resume=1`, по умолчанию включён, добавляет около секунды). Гибернация не поддерживается.
- **Прошивка генерируется локально.** При сборке скачиваются драйвер NVIDIA 610.43.03 и его исходники с `download.nvidia.com`, и из них извлекаются Booter и GSP. Версия установленного драйвера при этом не важна. Форк gpu-unlock-ada сверяет SHA-256 скачанного. В основном репозитории пока только HTTPS, сверка хешей ждёт в [issue #219](https://github.com/Zagitta/gpu-unlock/issues/219).
- **Secure Boot и подпись модулей.** Модуль собирается локально (DKMS), поэтому при включённом Secure Boot или `CONFIG_MODULE_SIG_FORCE` его нужно подписать своим ключом, иначе он не загрузится.
- **Проектам неделя.** Код меняется ежедневно, отчёты о совместимости идут десятками. Перед установкой загляни в issues своей модели.

## 📦 Установка

Порядок одинаковый на всех системах:

1. Собрать модуль и сгенерировать прошивку.
2. Положить модуль в initramfs раньше `nvidia`.
3. Добавить параметр ядра `gpu_unlock.targets=...`.
4. **Выключить** машину и включить снова.
5. Проверить результат.

Какой репозиторий брать:

- **RTX 30** — `Zagitta/gpu-unlock`.
- **RTX 40** — `JustAResearcher/gpu-unlock-ada`. Он поддерживает и весь список Ampere, сборка и установка такие же.

Без параметра ядра модуль ничего не делает. Варианты значения:

```text
gpu_unlock.targets=all                                       # все поддерживаемые карты, ещё не занятые драйвером
gpu_unlock.targets=0000:01:00.0                              # только эта карта (адрес из lspci -D)
gpu_unlock.targets=0000:01:00.0 gpu_unlock.ad103_experimental=1   # экспериментальная Ada: флаг + точный адрес
```

### Debian / Ubuntu (systemd)

```bash
sudo apt install git build-essential dkms linux-headers-$(uname -r) python3 zstd
git clone https://github.com/Zagitta/gpu-unlock          # для RTX 40: .../JustAResearcher/gpu-unlock-ada
cd gpu-unlock
make install       # → install-deb: apt-get build-dep, dpkg-buildpackage, apt-get install
                   #   пакеты gpu-unlock-dkms + gpu-unlock-firmware, хук initramfs-tools (или dracut)

sudoedit /etc/default/grub   # GRUB_CMDLINE_LINUX_DEFAULT="quiet splash gpu_unlock.targets=all"
sudo update-grub
sudo poweroff                # именно выключить, потом включить
```

На Ubuntu 22.04 сборка падает на Python 3.10 и заголовках ядра старше 6.0. Исправление пока ждёт в [PR #189](https://github.com/Zagitta/gpu-unlock/issues/189).

### Arch (systemd)

```bash
sudo pacman -S --needed git base-devel dkms linux-headers python zstd openssl   # для linux-lts — linux-lts-headers
git clone https://github.com/Zagitta/gpu-unlock && cd gpu-unlock
make install       # → install-arch: makepkg -sif; drop-in /etc/mkinitcpio.conf.d/zz-gpu-unlock.conf,
                   #   образы пересобираются сами
```

Параметр ядра:

- **GRUB:** допиши его в `GRUB_CMDLINE_LINUX_DEFAULT` и выполни `sudo grub-mkconfig -o /boot/grub/grub.cfg`.
- **systemd-boot:** добавь в строку `options` записи загрузки (где она лежит, покажет `bootctl status`).
- **UKI:** добавь в `/etc/kernel/cmdline` и выполни `sudo mkinitcpio -P`.

В AUR пакета пока нет, его добавление ждёт в [PR #223](https://github.com/Zagitta/gpu-unlock/issues/223). Собирай из репозитория, как выше.

### Gentoo (OpenRC)

`make install` знает только Arch, Debian и Fedora, поэтому на Gentoo собираем вручную. Служба OpenRC не нужна: всё происходит в initramfs. Нужен initramfs на **dracut** (`sys-kernel/installkernel` с USE `dracut` или ручной `dracut`), а `nvidia-drivers` должен грузиться уже с корневой ФС, как обычно и бывает.

```bash
sudo emerge --ask --noreplace dev-vcs/git app-arch/zstd sys-kernel/dracut
git clone https://github.com/Zagitta/gpu-unlock && cd gpu-unlock     # или gpu-unlock-ada для RTX 40

make assets                    # качает NVIDIA 610.43.03 в ~/.cache/gpu-unlock и генерирует прошивку
make -C kernel/gpu_unlock      # модуль под текущее ядро (нужен /lib/modules/$(uname -r)/build)
sudo make -C /lib/modules/$(uname -r)/build M="$PWD/kernel/gpu_unlock" modules_install
sudo depmod -a

# прошивку кладём в /lib/firmware: на split-usr ядро не ищет её в /usr/lib/firmware
sudo make install-firmware ASSETS="$HOME/.cache/gpu-unlock/assets" FWDIR=/lib/firmware/gpu-unlock/610.43.03
sudo make install-dracut       # /usr/lib/dracut/dracut.conf.d/gpu-unlock.conf: force_drivers+=" gpu_unlock "
sudo dracut --force --kver "$(uname -r)"
```

Параметр ядра:

- **GRUB:** допиши `gpu_unlock.targets=all` в `GRUB_CMDLINE_LINUX_DEFAULT` в `/etc/default/grub` и выполни `sudo grub-mkconfig -o /boot/grub/grub.cfg`.
- **installkernel с systemd-boot или UKI:** допиши параметр в `/etc/kernel/cmdline` и переустанови ядро. Для dist-kernel это `sudo emerge --config sys-kernel/gentoo-kernel`.

После этого `sudo poweroff` и включение.

Особенности Gentoo:

- **Форку для RTX 40 нужен `CONFIG_CRYPTO_LIB_SHA256`** (`=y` или `=m`): он сверяет хеши прошивки прямо в ядре. Проверить можно так: `zgrep CRYPTO_LIB_SHA256 /proc/config.gz`.
- **Подпись модулей.** Если ядро требует подписи модулей, подпиши `gpu_unlock.ko` тем же ключом, что и `nvidia-drivers`. Это `MODULES_SIGN_KEY` и `MODULES_SIGN_CERT` из `make.conf`, подписывать через `/usr/src/linux/scripts/sign-file sha512 …`.
- **Обновление ядра.** Модуль собран под конкретную версию ядра. После обновления повтори сборку и `modules_install` с `/lib/modules/<новая>/build`, затем `dracut --force --kver <новая>`. Если забудешь, ничего не сломается: система загрузится как обычно, просто без разблокировки. Можно отдать это DKMS (`sys-kernel/dkms` есть в ::gentoo): выполни `sudo make install-dkms && sudo dkms install gpu-unlock/$(cat VERSION)`, а после обновления ядра `sudo dkms autoinstall -k <версия>` и `dracut`.

### Entware (RT-AX56U)

Не применимо: это модуль ядра для x86_64 Linux с видеокартой NVIDIA.

## ✅ Проверка и отключение

```bash
dmesg | grep gpu_unlock            # OpenRC; на systemd: journalctl -k -b | grep gpu_unlock
lspci -nnk -s 0000:01:00.0         # адрес из lspci -D; «Kernel driver in use: nvidia»
```

Ищи для своей карты строку `gpu_unlock: unlocked`. Само по себе то, что модуль загрузился, ничего не доказывает. `nvidia-smi` разблокировку тоже не показывает, поэтому мерить нужно бенчмарком. Сравни цифры до и после при одинаковом лимите мощности.

<details>
<summary>Python (PyTorch): TFLOPS тензорных ядер в FP16 / BF16 / TF32</summary>

```python
# tc_bench.py — TFLOPS тензорных ядер в GEMM с FP32-аккумулятором
import time
import torch

N, ITERS = 8192, 50

def tflops(dtype):
    a = torch.randn(N, N, device="cuda", dtype=dtype)
    b = torch.randn(N, N, device="cuda", dtype=dtype)
    for _ in range(5):  # прогрев: выбор алгоритма cuBLAS, разгон частот
        a @ b
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(ITERS):
        a @ b
    torch.cuda.synchronize()
    return 2 * N**3 * ITERS / (time.perf_counter() - t0) / 1e12

torch.backends.cuda.matmul.allow_tf32 = True  # FP32-матмулы пойдут через TF32
print(torch.cuda.get_device_name(), "| torch", torch.__version__)
for name, dt in (("FP16", torch.float16), ("BF16", torch.bfloat16), ("TF32", torch.float32)):
    print(f"{name}: {tflops(dt):6.1f} TFLOPS")
```

Запусти один раз со стоковой загрузкой и один раз с `gpu_unlock.targets=…`. На RTX 30/40 BF16 и TF32 должны вырасти в 1,5–2 раза (FP16 тоже, если не упирается в лимит мощности). На RTX 20 смотри только FP16: BF16 и TF32 Turing аппаратно не умеет. Матрица 8192×8192 в FP32 занимает 256 МБ, так что тест влезает в любую карту от 4 ГБ.

Пример только на Python: из Java, Go или Rust до cuBLAS с BF16 пришлось бы тянуть CUDA-биндинги (JCuda и т. п.), а PyTorch и так стоит у всех, кто запускает ComfyUI или vLLM. Встроенные бенчмарки самих проектов: `diagnostics/bench` в gpu-unlock-ada и `tools/tensor_baseline.cu` в Turing-unlock.

</details>

**Отключить:**

- Убери `gpu_unlock.targets=` из параметров ядра. На одну загрузку его можно стереть в редакторе GRUB по клавише `e`.
- Затем полностью выключи питание, и карта вернётся в стоковое состояние.
- Удаление пакетов убирает модуль и хуки initramfs.

## 💡 Итог

- **Суть поста верна.** Ограничение на GeForce программное: тензорные ядра с FP32-аккумулятором работают на половине скорости, и его снимают без прошивки VBIOS, до загрузки стокового драйвера, до следующего выключения питания. Двукратный рост в синтетике подтверждён на RTX 30 и 4090.
- **Уточнения к посту:**
  - Число 59,9 → 111 TFLOPS для 2080 Ti взято из KohakUnlock (карта с допаянной памятью), а по ссылке из поста (Turing-unlock) на стоковой ASUS 46,9 → 93,7.
  - Обе работы для RTX 20 исследовательские, готового установщика нет.
  - Из RTX 40 стабильно поддерживается 4090, остальные экспериментальны и включаются отдельными флагами.
  - «Уровень RTX 6000 Ada» — это 331,6 против ≈364 TFLOPS.
  - Сводка «+14–36% в prefill» правдива для vLLM на BF16 и W4A16. С квантованным GGUF в llama.cpp прирост около нуля.
- **Кому стоит:** владельцам RTX 30/4090 под Linux, которые обучают модели, генерируют в ComfyUI в BF16 или гоняют vLLM с длинными промптами. Там реальные +15–60%. Для llama.cpp с GGUF и для игр смысла нет.
- **Тебе сейчас:** на GTX 1080 Ti неприменимо. Если появится RTX 3090 (как в [тесте 2×RTX 3090 против Tesla V100](../../Education/Youtube/%D0%9A%D0%B8%D0%B1%D0%B5%D1%80%20%D0%9A%D1%83%D0%B7%D0%BD%D0%B8%D1%86%D0%B0/4%C3%97Tesla%20V100%20SXM2%20%D1%81%20NVLink%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%202%C3%97RTX%203090%20%E2%80%94%20%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%BE%D0%B9%20%D1%82%D0%B5%D1%81%D1%82%20%28%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D1%81%D0%BA%D0%BE%D1%80%D0%BE%D1%81%D1%82%D0%B8%2C%20%D1%84%D0%BE%D1%80%D0%BA%20vLLM%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%2C%20%D1%81%D0%BC%D0%B5%D1%82%D0%B0%29.md)), путь для серии 30 самый зрелый, а на Gentoo он ставится вручную за десяток команд (см. выше).

## 🔗 Ссылки

- Пост: [t.me/prohitec/15091](https://t.me/prohitec/15091) (26.10.2026)
- Проекты: [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) (RTX 30) · [JustAResearcher/gpu-unlock-ada](https://github.com/JustAResearcher/gpu-unlock-ada) (RTX 40) · [haohervchb/Turing-unlock](https://github.com/haohervchb/Turing-unlock) (2080 Ti) · [KohakuBlueleaf/KohakUnlock](https://github.com/KohakuBlueleaf/KohakUnlock) (2080 Ti, 4090 под Windows через UEFI)
- Как это устроено: [How Ampere was unlocked](https://github.com/Zagitta/gpu-unlock/blob/main/docs/How%20Ampere%20was%20unlocked.md) · [технический отчёт по RTX 4090](https://github.com/JustAResearcher/gpu-unlock-ada/blob/main/rtx4090-register-report.md) · истоки: [cmpunlocker](https://github.com/amoghmunikote/cmpunlocker), [cmp90hx-unlock](https://github.com/WildFlash1st/cmp90hx-unlock), [TOTORONG/AD103_win_unlocker](https://huggingface.co/TOTORONG/AD103_win_unlocker)
- Замеры: [issue #1 (3090 Ti, GEMM)](https://github.com/Zagitta/gpu-unlock/issues/1) · [issue #2 (что даёт на практике)](https://github.com/Zagitta/gpu-unlock/issues/2) · [ComfyUI на 3090 Ti (Reddit)](https://www.reddit.com/r/StableDiffusion/comments/1xdoh8k/i_tested_the_rtx_30series_gpu_unlock_up_to_59/) · [Wccftech, 24.10.2026](https://wccftech.com/nvidia-geforce-rtx-30-gpus-get-up-to-2x-faster-ai-compute-performance-with-new-gpu-unlock-mod-real-world-gains-of-up-to-60/) · [Xenospectrum](https://xenospectrum.com/en/gpu-unlock-rtx-3090-ti-benchmarks/)
- Windows-порт для Ampere (сторонний): [impacifist/Windows-GPU-UNLOCK](https://github.com/impacifist/Windows-GPU-UNLOCK)
- Связанные: [llama.cpp — движок инференса GGUF](../../AI/Local-LLM/llama.cpp%20%E2%80%94%20%D0%B4%D0%B2%D0%B8%D0%B6%D0%BE%D0%BA%20%D0%BB%D0%BE%D0%BA%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B8%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%81%D0%B0%20GGUF.md) · [MoE-оффлоад в llama.cpp (как выжать 1080 Ti)](../../AI/Local-LLM/MoE-%D0%BE%D1%84%D1%84%D0%BB%D0%BE%D0%B0%D0%B4%20%D0%B2%20llama.cpp%20%28--n-cpu-moe%29%20%E2%80%94%20Qwen3.6-35B%20%D0%BD%D0%B0%2012%20%D0%93%D0%91%20VRAM%20%28%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%BF%D0%BE%D1%81%D1%82%D0%B0%20%E2%80%94%20%D1%82%D1%80%D1%8E%D0%BA%D1%83%20%D0%BF%D0%BE%D0%BB%D1%82%D0%BE%D1%80%D0%B0%20%D0%B3%D0%BE%D0%B4%D0%B0%2C%20--fit%20%D0%B4%D0%B5%D0%BB%D0%B0%D0%B5%D1%82%20%D1%8D%D1%82%D0%BE%20%D1%81%D0%B0%D0%BC%2C%201080%20Ti%20%D0%BF%D0%BE%D0%B4%D1%85%D0%BE%D0%B4%D0%B8%D1%82%29.md) · [2×RTX 3090 против 4×Tesla V100](../../Education/Youtube/%D0%9A%D0%B8%D0%B1%D0%B5%D1%80%20%D0%9A%D1%83%D0%B7%D0%BD%D0%B8%D1%86%D0%B0/4%C3%97Tesla%20V100%20SXM2%20%D1%81%20NVLink%20%D0%BF%D1%80%D0%BE%D1%82%D0%B8%D0%B2%202%C3%97RTX%203090%20%E2%80%94%20%D0%B1%D0%BE%D0%BB%D1%8C%D1%88%D0%BE%D0%B9%20%D1%82%D0%B5%D1%81%D1%82%20%28%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%20%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%BE%20%D1%81%D0%BA%D0%BE%D1%80%D0%BE%D1%81%D1%82%D0%B8%2C%20%D1%84%D0%BE%D1%80%D0%BA%20vLLM%2C%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%2C%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%2C%20%D1%81%D0%BC%D0%B5%D1%82%D0%B0%29.md)

#GPU #NVIDIA #CUDA #Hardware #LocalLLM #ComfyUI #vLLM #Linux #Kernel #Gentoo
