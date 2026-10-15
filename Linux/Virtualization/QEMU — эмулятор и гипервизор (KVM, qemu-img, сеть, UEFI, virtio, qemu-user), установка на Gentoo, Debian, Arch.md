---
создал заметку: 2026-10-16T12:00:00
author: WhiteK0T
tags:
  - Linux
  - Виртуализация
  - QEMU
  - KVM
  - Gentoo
Источник:
  - https://www.qemu.org/docs/master/
  - https://wiki.gentoo.org/wiki/QEMU
  - https://wiki.archlinux.org/title/QEMU
  - https://wiki.debian.org/QEMU
  - https://download.qemu.org/
---

# 🖥️ QEMU — эмулятор и гипервизор

**QEMU** (Quick EMUlator) — открытая программа, которая запускает виртуальные машины. Работает в двух режимах:

- **Эмуляция** — программно выполняет код чужой архитектуры: ARM-образ на x86-ноутбуке, MIPS-прошивку роутера и т.п. Медленно, зато работает что угодно на чём угодно.
- **Виртуализация с ускорением KVM** — если архитектура гостя совпадает с хостом, код гостя исполняет сам процессор, а QEMU только эмулирует устройства (диски, сеть, видео). Скорость близка к «железу».

Кроме полной ВМ, у QEMU есть **режим пользователя** (`qemu-user`): запускает одну программу чужой архитектуры прямо в вашей системе, без ВМ.

| | |
| :--- | :--- |
| Лицензия | GPL-2.0 |
| Последний выпуск | **11.1.2** (октябрь 2026); новые версии — примерно в апреле, августе и декабре |
| Ускорители | **KVM** (Linux), HVF (macOS), WHPX (Windows), Xen, TCG (чистая эмуляция) |
| Над ним | [libvirt](libvirt%20%E2%80%94%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%92%D0%9C%20%28virsh%2C%20virt-install%2C%20virt-manager%2C%20%D1%81%D0%B5%D1%82%D0%B8%2C%20%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%29%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch.md), virt-manager, Proxmox, GNOME Boxes, Quickemu — все они в итоге запускают `qemu-system-*` |

> [!tip] Когда запускать QEMU руками, а когда через libvirt
> Руками — для быстрых опытов, разовых загрузок образа, эмуляции ARM/MIPS, скриптов. Для ВМ, которые живут постоянно (автозапуск, снапшоты, графический менеджер), удобнее **libvirt** — он хранит конфигурацию ВМ и сам собирает длинную командную строку QEMU.

---

## 1. Как устроено

```
┌──────────── гость (Linux / Windows / BSD) ────────────┐
│  драйверы virtio-blk, virtio-net, virtio-gpu …        │
└────────────────────────────┬──────────────────────────┘
                             │ (обращения к «устройствам»)
┌────────────────────────────▼──────────────────────────┐
│  процесс qemu-system-x86_64 (обычный процесс хоста)    │
│  эмуляция устройств, диски qcow2, сеть, VNC/SPICE     │
└───────────────┬────────────────────────────┬──────────┘
                │ ioctl(/dev/kvm)            │ vhost-net (сеть в ядре)
┌───────────────▼────────────────────────────▼──────────┐
│  ядро Linux: модули kvm + kvm_amd / kvm_intel          │
└───────────────────────────────────────────────────────┘
```

- Каждая ВМ — **отдельный процесс** `qemu-system-…`, каждый виртуальный процессор — его поток. Видно в `top`, убивается `kill`, ограничивается cgroups.
- **TCG** — встроенный транслятор кода, используется без KVM и для чужих архитектур.
- **virtio** — паравиртуальные устройства: гость знает, что он в ВМ, и общается с QEMU через общие очереди в памяти. Намного быстрее эмуляции «настоящих» IDE-дисков и сетевых карт e1000.

---

## 2. Проверка, что KVM доступен

```bash
grep -cE 'vmx|svm' /proc/cpuinfo   # >0 — процессор умеет виртуализацию (vmx — Intel, svm — AMD)
lsmod | grep kvm                   # kvm_amd или kvm_intel загружен
ls -l /dev/kvm                     # crw-rw---- root kvm — устройство есть
```

Если `/proc/cpuinfo` пуст — включите **SVM / Intel VT-x** в BIOS. На VPS виртуализация внутри ВМ (**nested**) есть не у всех провайдеров.

Пользователю нужен доступ к `/dev/kvm`:

```bash
sudo gpasswd -a "$USER" kvm        # затем перелогиниться
```

**Вложенная виртуализация** (ВМ внутри ВМ) на хосте:

```bash
cat /sys/module/kvm_amd/parameters/nested     # 1 — включена (у Intel — kvm_intel)
echo "options kvm_amd nested=1" | sudo tee /etc/modprobe.d/kvm.conf
```

> [!warning] Безопасность nested
> Вложенная виртуализация расширяет поверхность атаки на KVM — именно через неё работают некоторые побеги из ВМ, например [Zapscape (CVE-2026-64561)](../../Security/Vulns/Linux/CVE/CVE-2026-64561%20%E2%80%94%20Zapscape%20%28KVM%20shadow-MMU%20UAF%2C%20%D0%BF%D0%BE%D0%B1%D0%B5%D0%B3%20%D0%B8%D0%B7%20%D0%B3%D0%BE%D1%81%D1%82%D0%B5%D0%B2%D0%BE%D0%B9%20VM%20%D0%BD%D0%B0%20%D1%85%D0%BE%D1%81%D1%82%3B%20%D0%BD%D1%83%D0%B6%D0%B5%D0%BD%20nested%20virt%2C%20%D0%BD%D0%B0%20Intel%20%E2%80%94%20EPT%20walk%204%20%D0%B8%205%29.md). На хосте с чужими ВМ включайте её, только если она действительно нужна.

---

## 3. Установка

| Система | Команда | Примечания |
| :--- | :--- | :--- |
| **Gentoo** | `emerge --ask app-emulation/qemu` | настройка через USE и цели — см. ниже |
| **Debian / Ubuntu** | `sudo apt install qemu-system-x86 qemu-utils ovmf swtpm` | для ARM-гостей — `qemu-system-arm`; для `qemu-user` — `qemu-user qemu-user-binfmt`. Debian 13 (trixie) — QEMU 10.0, в `trixie-backports` — 11.1 |
| **Arch** | `sudo pacman -S qemu-desktop edk2-ovmf swtpm` | `qemu-base` — без графики (сервер), `qemu-desktop` — x86 с графикой, `qemu-full` — все архитектуры; `qemu-user-static qemu-user-static-binfmt` — для `qemu-user` |
| **Entware** | **нет пакета** | на роутере (armv7, 512 МБ) запускать ВМ незачем. Наоборот, QEMU на ПК удобен, чтобы проверять ARM-программы для роутера — см. раздел 10 |

### Gentoo: USE-флаги и цели

```bash
# /etc/portage/package.use/qemu
app-emulation/qemu  QEMU_SOFTMMU_TARGETS: x86_64 aarch64 arm
app-emulation/qemu  QEMU_USER_TARGETS: aarch64 arm
app-emulation/qemu  spice usbredir virgl gtk sdl opengl passt io-uring vhost-net -xen
```

| Флаг | Зачем |
| :--- | :--- |
| `QEMU_SOFTMMU_TARGETS` | какие **полные ВМ** собрать (`qemu-system-<арх>`). Только нужные — сильно сокращает сборку |
| `QEMU_USER_TARGETS` | какие **`qemu-<арх>`** для запуска отдельных программ |
| `gtk`, `sdl`, `opengl`, `virgl` | окно ВМ на десктопе и 3D-ускорение в Linux-гостях |
| `spice`, `usbredir` | протокол SPICE (удобнее VNC: буфер обмена, USB-проброс) |
| `vnc` (по умолчанию) | доступ к экрану по VNC — для серверов |
| `slirp` (по умолчанию), `passt` | пользовательская сеть без root (раздел 6) |
| `io-uring`, `aio` | быстрый ввод-вывод дисков |
| `virtfs` | общие папки 9p (для virtiofs нужен отдельный `app-emulation/virtiofsd`) |
| `static-user` | статически собранные `qemu-<арх>` — нужны для `chroot` в чужую систему |
| `pin-upstream-blobs` (по умолчанию) | ставить те версии прошивок (SeaBIOS, edk2), с которыми QEMU проверен |

Ядро (если собираете сами):

```
Virtualization  --->  <M> Kernel-based Virtual Machine (KVM) support
                      <M>   KVM for AMD processors support      (или Intel)
Device Drivers -> Network device support -> <M> Universal TUN/TAP device driver support
                                            <M> vhost-net
Networking -> 802.1d Ethernet Bridging (BRIDGE)
```

Модуль при загрузке (OpenRC): добавьте `kvm_amd` (или `kvm_intel`) в `/etc/conf.d/modules`: `modules="kvm_amd vhost_net tun"`.

Прошивка UEFI для гостей: `emerge --ask sys-firmware/edk2-bin` (ставится вместе с QEMU), TPM для Windows 11 — `app-crypt/swtpm`.

---

## 4. Диски: qemu-img

**qcow2** — родной формат QEMU: файл растёт по мере заполнения, умеет снапшоты, сжатие, шифрование и «наложенные» образы. **raw** — просто байты диска: чуть быстрее, проще, но без этих возможностей.

```bash
qemu-img create -f qcow2 disk.qcow2 40G           # создать (занимает ~200 КБ, растёт по мере записи)
qemu-img info disk.qcow2                          # формат, виртуальный и фактический размер, снапшоты
qemu-img resize disk.qcow2 +20G                   # увеличить (потом расширить раздел в госте)
qemu-img convert -O qcow2 win.vmdk win.qcow2      # из VMware/VirtualBox (vmdk, vdi, vhdx) в qcow2
qemu-img convert -O raw disk.qcow2 disk.img       # в raw (например, для dd на флешку)
qemu-img convert -O qcow2 -c disk.qcow2 small.qcow2   # сжать и выкинуть пустые блоки
qemu-img check disk.qcow2                         # проверить целостность
```

### Наложенные образы (backing file)

Один «золотой» образ и много лёгких копий поверх него — каждая хранит только свои изменения:

```bash
qemu-img create -f qcow2 -b debian-base.qcow2 -F qcow2 test1.qcow2
qemu-img create -f qcow2 -b debian-base.qcow2 -F qcow2 test2.qcow2
```

Базовый образ после этого **нельзя менять** — иначе все наложенные сломаются. Объединить слой с базой: `qemu-img commit test1.qcow2`; отвязать слой и сделать самостоятельным: `qemu-img rebase -b "" test1.qcow2`.

### Внутренние снапшоты qcow2

```bash
qemu-img snapshot -c before-update disk.qcow2     # создать (ВМ выключена!)
qemu-img snapshot -l disk.qcow2                   # список
qemu-img snapshot -a before-update disk.qcow2     # откатиться
qemu-img snapshot -d before-update disk.qcow2     # удалить
```

> [!warning] Не трогайте образ работающей ВМ
> `qemu-img` с образом, открытым запущенной ВМ, портит его. QEMU ставит блокировку и обычно ругается `Failed to get "write" lock`, но не обходите её флагом `-U` для записи. Снапшоты работающей ВМ — через монитор (`savevm`) или libvirt.

### Готовые облачные образы

Вместо установки с ISO можно взять готовый образ (Debian `genericcloud`, Ubuntu cloud, Arch `cloudimg`, Fedora Cloud) и задать пользователя и SSH-ключ через **cloud-init**:

```bash
cat > user-data <<'EOF'
#cloud-config
users:
  - name: me
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys: [ "ssh-ed25519 AAAA... me@pc" ]
EOF
echo "instance-id: vm1" > meta-data
# ISO с меткой cidata. xorriso: Gentoo — dev-libs/libisoburn, Debian — xorriso, Arch — libisoburn
xorriso -as mkisofs -output seed.iso -volid cidata -joliet -rock user-data meta-data
```

Затем подключить `seed.iso` как CD-ROM вторым диском — гость прочитает настройки при первой загрузке.

---

## 5. Запуск ВМ

### Минимальный Linux-гость с KVM

```bash
qemu-system-x86_64 \
  -enable-kvm -machine q35 -cpu host -smp 4 -m 4G \
  -drive file=disk.qcow2,if=virtio,cache=none,aio=io_uring,discard=unmap \
  -cdrom debian-13-amd64-netinst.iso -boot order=d \
  -nic user,model=virtio-net-pci,hostfwd=tcp::2222-:22 \
  -device virtio-vga -display gtk
```

| Опция | Смысл |
| :--- | :--- |
| `-enable-kvm` (или `-accel kvm`) | аппаратное ускорение. **Без него всё работает в 10–50 раз медленнее** |
| `-machine q35` | современный чипсет (PCIe). `pc` (i440FX) — старый, для очень старых систем |
| `-cpu host` | показать гостю все возможности процессора хоста. Самый быстрый вариант, но ВМ нельзя перенести на хост с другим процессором; для переносимости — модели вроде `EPYC-Genoa` или `x86-64-v3` |
| `-smp 4 -m 4G` | 4 виртуальных ядра, 4 ГБ памяти |
| `if=virtio` | диск virtio-blk. Для Windows нужны драйверы virtio (раздел 8) |
| `cache=none,aio=io_uring` | быстрый ввод-вывод мимо кэша хоста (на tmpfs `cache=none` не работает — уберите) |
| `discard=unmap` | `fstrim` в госте освобождает место в qcow2 |
| `-boot order=d` | сначала грузиться с CD; после установки уберите `-cdrom` |
| `-nic user,...hostfwd=tcp::2222-:22` | сеть без root + проброс порта: `ssh -p 2222 me@localhost` |
| `-device virtio-vga -display gtk` | видеокарта и окно на рабочем столе |

### Без графики (сервер, SSH)

```bash
qemu-system-x86_64 -enable-kvm -machine q35 -cpu host -smp 2 -m 2G \
  -drive file=disk.qcow2,if=virtio \
  -nic user,model=virtio-net-pci,hostfwd=tcp:127.0.0.1:2222-:22 \
  -nographic                       # консоль гостя — прямо в терминале (нужна serial-консоль в госте)
# выход из -nographic: Ctrl+A, затем X;   Ctrl+A, C — переключиться в монитор QEMU
```

Или экран по VNC только на localhost и туннель SSH до него: `-display none -vnc 127.0.0.1:1` (порт 5901). VNC без пароля, поэтому **никогда не слушайте на внешнем адресе**.

### Как фоновая служба

```bash
qemu-system-x86_64 ... -display none -vnc 127.0.0.1:1 \
  -daemonize -pidfile /run/vm1.pid \
  -monitor unix:/run/vm1.mon,server,nowait \
  -name vm1,process=qemu-vm1
```

---

## 6. Сеть

| Режим | Опция | Root нужен | Гость доступен из LAN | Когда |
| :--- | :--- | :---: | :---: | :--- |
| **user (SLIRP)** | `-nic user` | нет | только через `hostfwd` | по умолчанию, быстрые опыты. Медленный, `ping` из гостя часто не работает |
| **passt** | `-nic passt` (QEMU 10.1+) или через сокет | нет | через проброс портов | современная замена SLIRP: быстрее, IPv6, проще правила |
| **tap + мост** | `-nic bridge,br=br0` | для настройки моста | **да**, гость получает адрес в вашей сети | постоянные ВМ-серверы |
| **tap без моста** | `-nic tap,ifname=tap0,script=no` | да | через маршрутизацию/NAT хоста | свои схемы сети, nftables |
| **socket / vde** | `-nic socket,...` | нет | — | связать несколько ВМ между собой |

В режиме **user** гость видит сеть `10.0.2.0/24`: шлюз `10.0.2.2` — это сам хост, DNS — `10.0.2.3`.

### Мост через qemu-bridge-helper (без запуска QEMU от root)

1. Мост `br0` на хосте, в который включена физическая сетевая карта (как настроить на Gentoo, Debian, Arch — см. [заметку про libvirt](libvirt%20%E2%80%94%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%92%D0%9C%20%28virsh%2C%20virt-install%2C%20virt-manager%2C%20%D1%81%D0%B5%D1%82%D0%B8%2C%20%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%29%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch.md#6-сети)).
2. Разрешить мост: `echo "allow br0" | sudo tee -a /etc/qemu/bridge.conf`.
3. Запускать: `-nic bridge,br=br0,model=virtio-net-pci`.

Помощнику `qemu-bridge-helper` нужны права на создание tap-устройств. В Gentoo ebuild сам даёт ему `cap_net_admin` (`/usr/libexec/qemu-bridge-helper`). В Debian и Arch он лежит в `/usr/lib/qemu/qemu-bridge-helper`; если QEMU пишет `failed to create tun device: Operation not permitted` — `sudo chmod u+s /usr/lib/qemu/qemu-bridge-helper`.

> [!warning] Мост и Wi-Fi
> Wi-Fi-адаптер в режиме клиента нельзя включить в мост — точка доступа не пропустит чужие MAC-адреса. Для ноутбука на Wi-Fi используйте NAT (user/passt или сеть `default` в libvirt).

---

## 7. UEFI, Secure Boot и TPM

По умолчанию QEMU грузит **SeaBIOS** (старый BIOS). Для UEFI нужна прошивка **OVMF** (из проекта edk2): файл кода (только чтение) и **своя копия** файла переменных для каждой ВМ.

| Система | Где лежит OVMF |
| :--- | :--- |
| **Gentoo** (`sys-firmware/edk2-bin`) | `/usr/share/edk2/OvmfX64/` |
| **Debian / Ubuntu** (`ovmf`) | `/usr/share/OVMF/OVMF_CODE_4M.fd`, `OVMF_VARS_4M.fd` (`*.ms.fd` — с ключами Microsoft для Secure Boot) |
| **Arch** (`edk2-ovmf`) | `/usr/share/edk2/x64/OVMF_CODE.4m.fd`, `OVMF_VARS.4m.fd` |

```bash
cp /usr/share/OVMF/OVMF_VARS_4M.fd vm1_VARS.fd     # своя копия переменных для ВМ
qemu-system-x86_64 -enable-kvm -machine q35 ... \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
  -drive if=pflash,format=raw,file=vm1_VARS.fd
```

**TPM 2.0** (обязателен для Windows 11) — через программный TPM `swtpm`:

```bash
mkdir -p /tmp/vm1-tpm
swtpm socket --tpm2 --tpmstate dir=/tmp/vm1-tpm \
  --ctrl type=unixio,path=/tmp/vm1-tpm/sock --daemon
qemu-system-x86_64 ... \
  -chardev socket,id=chrtpm,path=/tmp/vm1-tpm/sock \
  -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis,tpmdev=tpm0
```

Состояние TPM храните не в `/tmp`, а рядом с диском ВМ: в нём ключи BitLocker.

---

## 8. Windows-гость

1. Скачать ISO Windows и **ISO драйверов virtio** (`virtio-win.iso` из проекта Fedora: https://github.com/virtio-win/virtio-win-pkg-scripts).
2. Запустить с UEFI, TPM и двумя CD:

```bash
qemu-system-x86_64 -enable-kvm -machine q35 -cpu host,hv_relaxed,hv_spinlocks=0x1fff,hv_vapic,hv_time \
  -smp 4 -m 8G \
  -drive if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.ms.fd \
  -drive if=pflash,format=raw,file=win_VARS.fd \
  -drive file=win.qcow2,if=virtio,cache=none,aio=io_uring,discard=unmap \
  -drive file=Win11.iso,media=cdrom -drive file=virtio-win.iso,media=cdrom \
  -nic user,model=virtio-net-pci -device qxl-vga -usb -device usb-tablet \
  -chardev socket,id=chrtpm,path=/tmp/vm1-tpm/sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis,tpmdev=tpm0
```

3. В установщике диск не виден → «Загрузить драйвер» → CD с virtio → `viostor\w11\amd64`.
4. После установки поставить с того же CD `virtio-win-guest-tools.exe` (сеть, баллон памяти, гостевой агент, драйвер QXL/SPICE).

Флаги `hv_*` (**Hyper-V enlightenments**) заметно ускоряют Windows в KVM. Проще всего всё это делает **virt-manager** — см. заметку про libvirt.

---

## 9. Удобства

### Монитор QEMU и QMP

Монитор — консоль управления запущенной ВМ: `Ctrl+Alt+2` в окне GTK, `Ctrl+A C` при `-nographic` или сокет `-monitor unix:/run/vm1.mon,server,nowait` (подключение: `socat - UNIX-CONNECT:/run/vm1.mon`).

| Команда | Действие |
| :--- | :--- |
| `info status`, `info block`, `info network` | состояние ВМ, диски, сеть |
| `savevm name` / `loadvm name` / `info snapshots` | снапшот **с памятью** работающей ВМ (только qcow2) |
| `change ide1-cd0 new.iso` / `eject ide1-cd0` | сменить диск в CD-приводе |
| `system_powerdown` | «нажать кнопку питания» — корректное выключение |
| `system_reset` | жёсткая перезагрузка |
| `stop` / `cont` | пауза / продолжить |
| `quit` | убить ВМ без выключения гостя |
| `hostfwd_add tcp::8080-:80` | добавить проброс порта на лету (сеть user) |

**QMP** — то же самое в JSON для программ (`-qmp unix:/run/vm1.qmp,server,nowait`). Через него ВМ управляет libvirt.

### Гостевой агент

`qemu-guest-agent` внутри гостя позволяет хосту корректно выключать ВМ, замораживать ФС перед снапшотом, узнавать IP-адреса гостя. В госте: Debian `apt install qemu-guest-agent`, Arch `pacman -S qemu-guest-agent`, Gentoo `emerge app-emulation/qemu-guest-agent` (OpenRC: `rc-update add qemu-guest-agent default`). На хосте добавьте канал:

```
-device virtio-serial -chardev socket,path=/run/vm1.qga,server=on,wait=off,id=qga0 \
-device virtserialport,chardev=qga0,name=org.qemu.guest_agent.0
```

### Общие папки хост ↔ гость

- **virtiofs** — быстрый, рекомендуемый. Нужен отдельный демон `virtiofsd` и общая память:

  ```bash
  /usr/libexec/virtiofsd --socket-path=/tmp/vfs.sock --shared-dir ~/share &   # в Arch — /usr/lib/virtiofsd
  qemu-system-x86_64 ... -m 4G \
    -object memory-backend-memfd,id=mem,size=4G,share=on -numa node,memdev=mem \
    -chardev socket,id=vfs,path=/tmp/vfs.sock \
    -device vhost-user-fs-pci,chardev=vfs,tag=share
  # в госте:  mount -t virtiofs share /mnt
  ```

- **9p** (`-virtfs local,path=~/share,mount_tag=share,security_model=mapped-xattr`) — проще, без демона, но медленнее. В госте: `mount -t 9p -o trans=virtio share /mnt`.

### Проброс USB-устройства

```bash
lsusb                                 # Bus 001 Device 005: ID 0bda:8153 ...
qemu-system-x86_64 ... -device qemu-xhci -device usb-host,vendorid=0x0bda,productid=0x8153
```

Нужны права на `/dev/bus/usb/...` (udev-правило или запуск через libvirt). Проброс целой видеокарты (VFIO, IOMMU) — отдельная большая тема, удобнее делать через libvirt.

### Загрузить ядро напрямую (без установки)

Для отладки ядер и initramfs:

```bash
qemu-system-x86_64 -enable-kvm -m 1G -kernel arch/x86/boot/bzImage \
  -initrd initramfs.img -append "console=ttyS0" -nographic
```

---

## 10. qemu-user: программы чужой архитектуры

`qemu-<арх>` запускает **одну программу** другой архитектуры как обычный процесс: системные вызовы переводятся в вызовы ядра хоста. Это удобно, например, чтобы проверить на ПК бинарник под ARM-роутер:

```bash
qemu-arm -L /path/to/armv7-sysroot ./mybinary      # -L — где искать библиотеки чужой архитектуры
qemu-aarch64-static ./static-aarch64-binary         # статический бинарник библиотек не требует
```

С **binfmt_misc** ядро само запускает чужие ELF-файлы через QEMU — можно даже сделать `chroot` в ARM-систему:

| Система | binfmt |
| :--- | :--- |
| **Gentoo** | `QEMU_USER_TARGETS` + USE `static-user`, затем `rc-update add qemu-binfmt default && rc-service qemu-binfmt start` |
| **Debian / Ubuntu** | `apt install qemu-user qemu-user-binfmt` (регистрируется через systemd-binfmt) |
| **Arch** | `pacman -S qemu-user-static qemu-user-static-binfmt` |

```bash
cat /proc/sys/fs/binfmt_misc/qemu-arm      # enabled — регистрация работает
docker run --rm --platform linux/arm/v7 alpine uname -m   # → armv7l: Docker тоже пользуется binfmt
```

Сборка программ под Entware-роутер удобнее кросс-компилятором (см. [crossdev](../Build/crossdev%20%E2%80%94%20%D0%BA%D1%80%D0%BE%D1%81%D1%81-%D0%BA%D0%BE%D0%BC%D0%BF%D0%B8%D0%BB%D1%8F%D1%86%D0%B8%D1%8F%20%D0%B2%20Gentoo%20%28%D0%BE%D1%82%D0%B4%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B5%D0%BF%D0%BE%D0%B7%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B9%2C%20%D1%81%D1%82%D0%B0%D0%B4%D0%B8%D0%B8%20s0-s4%2C%20emerge-CTARGET%3B%20%D0%BF%D0%BE%D1%87%D0%B5%D0%BC%D1%83%20%D0%B4%D0%BB%D1%8F%20Entware-%D1%80%D0%BE%D1%83%D1%82%D0%B5%D1%80%D0%B0%20%D0%BE%D0%BD%20%D0%BD%D0%B5%20%D0%BF%D0%BE%D0%B4%D0%BE%D0%B9%D0%B4%D1%91%D1%82%29.md)), а `qemu-user` — чтобы быстро проверить результат, не копируя его на роутер.

### Полная ARM-ВМ

```bash
qemu-system-aarch64 -machine virt -cpu cortex-a72 -smp 4 -m 4G \
  -bios /usr/share/edk2/aarch64/QEMU_EFI.fd \
  -drive file=debian-arm64.qcow2,if=virtio \
  -nic user,model=virtio-net-pci -nographic
```

Прошивка UEFI для aarch64: Arch — пакет `edk2-aarch64` (путь как выше), Debian — `qemu-efi-aarch64` (`/usr/share/qemu-efi-aarch64/QEMU_EFI.fd`), Gentoo — `sys-firmware/edk2-bin` с целью `aarch64` в `QEMU_SOFTMMU_TARGETS`. Без KVM (на x86-хосте) это чистая эмуляция — работает, но в разы медленнее «родной» ВМ.

---

## 11. Производительность — короткий список

- `-enable-kvm` и `-cpu host` (если перенос ВМ не нужен).
- Все устройства **virtio**: диск, сеть, видео (`virtio-vga` / `virtio-gpu`), баллон памяти.
- Диск: `cache=none,aio=io_uring` (или `aio=native`), образ на SSD; для максимума — raw-образ или целый LVM-том/раздел.
- Сеть: tap + `vhost=on` (`-netdev tap,id=n0,vhost=on -device virtio-net-pci,netdev=n0`) — обработка пакетов в ядре.
- Большие страницы памяти для больших ВМ: `-mem-path /dev/hugepages` (после настройки hugepages на хосте).
- Не давайте ВМ больше ядер, чем есть у хоста: лишние vCPU только мешают.

---

## 12. Частые проблемы

| Симптом | Причина и решение |
| :--- | :--- |
| `Could not access KVM kernel module: Permission denied` | пользователь не в группе `kvm` или не перелогинился |
| `KVM kernel module: No such file or directory` | модуль `kvm_amd`/`kvm_intel` не загружен, виртуализация выключена в BIOS или nested нет на VPS |
| ВМ ужасно медленная | забыли `-enable-kvm`, или QEMU сам откатился на TCG — смотрите предупреждения при запуске |
| `Failed to get "write" lock` | образ уже открыт другой ВМ или `qemu-img` |
| Гость не видит диск при установке Windows | нужен драйвер virtio с `virtio-win.iso`, или временно `if=ide` |
| Мышь «убегает» / смещена | добавьте `-device usb-tablet` (абсолютные координаты) |
| Из гостя в режиме user не работает `ping` | это нормально для SLIRP: ICMP требует настройки `net.ipv4.ping_group_range`; TCP/UDP работают |
| Выйти из окна, захватившего мышь | `Ctrl+Alt+G` |

## 🔗 Ссылки

- Документация: https://www.qemu.org/docs/master/
- Скачать исходники: https://download.qemu.org/
- Gentoo Wiki: https://wiki.gentoo.org/wiki/QEMU
- ArchWiki: https://wiki.archlinux.org/title/QEMU
- Debian Wiki: https://wiki.debian.org/QEMU
- Драйверы virtio для Windows: https://github.com/virtio-win/virtio-win-pkg-scripts

Связанные заметки: [libvirt](libvirt%20%E2%80%94%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%92%D0%9C%20%28virsh%2C%20virt-install%2C%20virt-manager%2C%20%D1%81%D0%B5%D1%82%D0%B8%2C%20%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D0%BB%D0%B8%D1%89%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%29%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch.md), [WinPodX — Windows-приложения в контейнерной ВМ](../WinPodX%20%E2%80%94%20Windows-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BA%D0%B0%D0%BA%20%D0%BD%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BE%D0%BA%D0%BD%D0%B0%20Linux%20%28%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%B9%D0%BD%D0%B5%D1%80%D0%BD%D0%B0%D1%8F%20Windows-%D0%92%D0%9C%20%2B%20RemoteApp%29.md), [Januscape (CVE-2026-53359) — побег из ВМ через KVM](../../Security/Vulns/Linux/CVE/CVE-2026-53359%20%E2%80%94%20Januscape%20%28KVM%20shadow-MMU%20UAF%2C%20%D0%BF%D0%BE%D0%B1%D0%B5%D0%B3%20%D0%B8%D0%B7%20%D0%B3%D0%BE%D1%81%D1%82%D0%B5%D0%B2%D0%BE%D0%B9%20VM%20%D0%BD%D0%B0%20%D1%85%D0%BE%D1%81%D1%82%2C%20Intel%20%D0%B8%20AMD%29.md).

#Linux #Виртуализация #QEMU #KVM #Gentoo
