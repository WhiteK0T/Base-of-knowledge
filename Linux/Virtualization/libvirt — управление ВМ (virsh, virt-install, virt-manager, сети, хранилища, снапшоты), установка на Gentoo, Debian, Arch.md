---
создал заметку: 2026-10-16T13:00:00
author: WhiteK0T
tags:
  - Linux
  - Виртуализация
  - libvirt
  - QEMU
  - KVM
  - Gentoo
Источник:
  - https://libvirt.org/docs.html
  - https://libvirt.org/manpages/virsh.html
  - https://wiki.gentoo.org/wiki/Libvirt
  - https://wiki.archlinux.org/title/Libvirt
  - https://wiki.debian.org/KVM
  - https://download.libvirt.org/
---

# 🗄️ libvirt — управление виртуальными машинами

**libvirt** — библиотека и набор служб, которые управляют виртуальными машинами через единый интерфейс. Сама libvirt ВМ не исполняет: для KVM-машин она запускает [QEMU](QEMU%20%E2%80%94%20%D1%8D%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80%20%D0%B8%20%D0%B3%D0%B8%D0%BF%D0%B5%D1%80%D0%B2%D0%B8%D0%B7%D0%BE%D1%80%20%28KVM%2C%20qemu-img%2C%20%D1%81%D0%B5%D1%82%D1%8C%2C%20UEFI%2C%20virtio%2C%20qemu-user%29%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch.md), собирая его длинную командную строку из XML-описания. Взамен даёт:

- **хранение конфигурации** ВМ (XML в `/etc/libvirt/qemu/`), автозапуск при загрузке хоста, корректное выключение ВМ при выключении хоста;
- **виртуальные сети** с NAT, DHCP и DNS (dnsmasq) «из коробки»;
- **пулы хранения** (каталоги, LVM, ZFS, iSCSI, NFS, Ceph);
- **снапшоты**, клонирование, живую миграцию между хостами;
- **безопасность**: QEMU работает от отдельного пользователя, изоляция через cgroups, sVirt (SELinux/AppArmor);
- **единый API** для инструментов: `virsh`, `virt-install`, **virt-manager**, Cockpit, GNOME Boxes, OpenStack, Terraform/OpenTofu-провайдер.

| | |
| :--- | :--- |
| Лицензия | LGPL-2.1+ |
| Последний выпуск | **12.8.0** (1 октября 2026); новые версии выходят каждый месяц, старший номер меняется в январе |
| Драйверы | **QEMU/KVM** (основной), LXC, Xen, VirtualBox, VMware ESX, Hyper-V, bhyve, Cloud Hypervisor |

---

## 1. Как устроено

```
 virsh   virt-manager   virt-install   Cockpit   ...
    └──────────┴──────────────┴───────────┘
                     │  URI: qemu:///system
                     ▼
     службы libvirt (libvirtd или virtqemud + virtnetworkd + …)
       │              │                 │
       ▼              ▼                 ▼
 qemu-system-*    dnsmasq + nftables   пулы: каталоги, LVM, ZFS
 (по процессу      (сеть default,       (/var/lib/libvirt/images)
  на каждую ВМ)     мост virbr0)
```

### Службы: монолитная и модульные

| Вариант | Службы | Где по умолчанию |
| :--- | :--- | :--- |
| **Монолитная** | `libvirtd` — всё в одном процессе | **Gentoo (OpenRC)**, **Debian / Ubuntu** (запуск по сокету `libvirtd.socket`) |
| **Модульные** (рекомендуются разработчиками) | `virtqemud` (ВМ QEMU), `virtnetworkd` (сети), `virtstoraged` (хранилища), `virtnodedevd` (устройства хоста), `virtsecretd`, `virtinterfaced`, `virtnwfilterd`, `virtproxyd` | Fedora, RHEL; можно включить на любом дистрибутиве с systemd, в том числе на **Arch** |

Для пользователя разницы почти нет — те же `virsh` и virt-manager. Плюс модульных служб: падение или обновление одной части не трогает остальные.

Рядом всегда работают **`virtlogd`** (журналы консолей ВМ, `/var/log/libvirt/qemu/<ВМ>.log`) и **`virtlockd`** (блокировки дисков).

### URI: system и session

| URI | Кто запускает ВМ | Сети | Когда |
| :--- | :--- | :--- | :--- |
| **`qemu:///system`** | системная служба, ВМ от пользователя `qemu` / `libvirt-qemu` | NAT `default`, мосты, всё | **обычный выбор** для постоянных ВМ и серверов |
| `qemu:///session` | процессы вашего пользователя | только user-сеть/passt, мост — через `qemu-bridge-helper` | ВМ «для себя» без прав администратора |

`virsh` от обычного пользователя **по умолчанию подключается к `session`** — отсюда частая путаница «где мои ВМ?». Чтобы всегда работать с системными:

```bash
echo 'export LIBVIRT_DEFAULT_URI=qemu:///system' >> ~/.bashrc
# или в ~/.config/libvirt/libvirt.conf:   uri_default = "qemu:///system"
```

---

## 2. Установка

QEMU и проверку KVM см. в [заметке про QEMU](QEMU%20%E2%80%94%20%D1%8D%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80%20%D0%B8%20%D0%B3%D0%B8%D0%BF%D0%B5%D1%80%D0%B2%D0%B8%D0%B7%D0%BE%D1%80%20%28KVM%2C%20qemu-img%2C%20%D1%81%D0%B5%D1%82%D1%8C%2C%20UEFI%2C%20virtio%2C%20qemu-user%29%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch.md#2-проверка-что-kvm-доступен).

### Gentoo (OpenRC)

```bash
# /etc/portage/package.use/libvirt
app-emulation/libvirt     qemu virt-network policykit nfs lvm zfs   # лишнее уберите
app-emulation/virt-manager gui policykit
net-dns/dnsmasq           script

emerge --ask app-emulation/libvirt app-emulation/virt-manager \
             app-emulation/virt-viewer sys-firmware/edk2-bin app-crypt/swtpm
gpasswd -a "$USER" libvirt              # доступ к qemu:///system без root (через polkit)
rc-update add libvirtd default && rc-service libvirtd start
rc-update add libvirt-guests default    # корректно останавливать ВМ при выключении хоста
```

| USE | Зачем |
| :--- | :--- |
| `qemu` (по умолчанию) | драйвер QEMU/KVM |
| `libvirtd` (по умолчанию) | сама служба (без неё — только клиентская библиотека) |
| **`virt-network`** | NAT-сети с DHCP: подтягивает `dnsmasq`, `ebtables` и iptables/nftables. **Без него сеть `default` не заработает** |
| `policykit` | доступ к системным ВМ для группы `libvirt` |
| `lvm`, `zfs`, `nfs`, `iscsi`, `rbd` | соответствующие пулы хранения |
| `virtiofsd` | общие папки virtiofs |
| `firewalld` | если на хосте firewalld |
| `caps` (по умолчанию) | QEMU работает от `qemu:qemu`, а не от root — файлы дисков должны быть доступны этому пользователю |

Параметры службы — в `/etc/conf.d/libvirtd`, поведение ВМ при выключении хоста — в `/etc/conf.d/libvirt-guests` (по умолчанию ВМ «засыпают» через `managedsave` и просыпаются при загрузке). В Gentoo актуальная стабильная — 12.6.0, 12.7.0 — в `~amd64`.

Ядро: помимо опций из заметки про QEMU нужны `CONFIG_BRIDGE`, `CONFIG_NETFILTER_XT_*`/`CONFIG_NF_TABLES` с NAT, `CONFIG_VETH`, `CONFIG_CGROUPS` — список проверяет `virt-host-validate`.

### Debian / Ubuntu

```bash
sudo apt install --no-install-recommends qemu-system-x86 libvirt-daemon-system \
     libvirt-clients virtinst virt-manager virt-viewer ovmf swtpm-tools dnsmasq-base
sudo adduser "$USER" libvirt          # и перелогиниться
sudo systemctl enable --now libvirtd.socket
```

В Debian 13 (trixie) — libvirt 11.3, в `sid` — 12.8. Для сервера без графики `virt-manager` и `virt-viewer` не нужны. QEMU работает от пользователя `libvirt-qemu`; профили **AppArmor** включены (при «Permission denied» на диск смотрите `journalctl -k | grep apparmor`).

### Arch

```bash
sudo pacman -S libvirt qemu-desktop dnsmasq iptables-nft virt-install virt-manager virt-viewer edk2-ovmf swtpm
sudo usermod -aG libvirt "$USER"
sudo systemctl enable --now libvirtd.socket
# или модульные службы:
# for d in qemu network storage nodedev secret interface; do sudo systemctl enable --now virt${d}d.socket; done
```

`dnsmasq` и `iptables-nft` — **необязательные** зависимости, но без них не работает NAT-сеть `default`. QEMU запускается от `libvirt-qemu`.

### Entware

**Не подходит**: на роутере нет KVM, а libvirt и QEMU нет в репозитории Entware. Управлять ВМ на сервере удобнее с ПК — через `virsh` или virt-manager по SSH (раздел 9).

### Проверка

```bash
virt-host-validate qemu        # KVM, cgroups, IOMMU — все строки должны быть PASS (IOMMU — WARN, если не нужна VFIO)
virsh -c qemu:///system version
virsh net-list --all           # сеть default
```

---

## 3. virsh — основные команды

`virsh` — консольный клиент. Каждая команда работает и интерактивно (`virsh` → приглашение `virsh #`), и одной строкой.

### Жизненный цикл ВМ

| Команда | Действие |
| :--- | :--- |
| `virsh list --all` | все ВМ (`--all` — и выключенные) |
| `virsh start vm1` | запустить |
| `virsh shutdown vm1` | корректно выключить (ACPI или гостевой агент) |
| `virsh destroy vm1` | **жёстко** выключить (как выдернуть питание; ВМ не удаляется!) |
| `virsh reboot vm1` / `virsh reset vm1` | перезагрузка корректная / жёсткая |
| `virsh suspend vm1` / `virsh resume vm1` | пауза в памяти / продолжить |
| `virsh managedsave vm1` | сохранить память на диск и остановить; следующий `start` продолжит с того же места |
| `virsh autostart vm1` (`--disable`) | запускать при старте хоста |
| `virsh undefine vm1 --nvram` | удалить описание ВМ (`--nvram` — и файл переменных UEFI; `--remove-all-storage` — и диски) |

### Информация и доступ

| Команда | Действие |
| :--- | :--- |
| `virsh dominfo vm1` | память, процессоры, состояние, автозапуск |
| `virsh domblklist vm1` / `virsh domiflist vm1` | диски / сетевые интерфейсы |
| `virsh domifaddr vm1` | IP-адреса гостя (из DHCP; с `--source agent` — от гостевого агента) |
| `virsh console vm1` | текстовая консоль гостя по последовательному порту (выход — `Ctrl+]`) |
| `virsh vncdisplay vm1` | на каком порту VNC |
| `virsh domstats vm1` / `virsh domblkstat vm1 vda` | статистика нагрузки |
| `virsh dumpxml vm1` | полное XML-описание |

### Изменение конфигурации

| Команда | Действие |
| :--- | :--- |
| `virsh edit vm1` | открыть XML в `$EDITOR`, после сохранения libvirt проверит его. **Не правьте файлы в `/etc/libvirt/qemu/` руками** — libvirt их не перечитает |
| `virsh setvcpus vm1 4 --config` | число процессоров (`--live` — на работающей, если разрешено) |
| `virsh setmaxmem vm1 8G --config` и `virsh setmem vm1 8G --config` | память |
| `virsh attach-disk vm1 /var/lib/libvirt/images/data.qcow2 vdb --subdriver qcow2 --persistent` | подключить диск |
| `virsh change-media vm1 sda /path/new.iso` (`--eject`) | сменить ISO в CD-приводе |
| `virsh domrename vm1 web1` | переименовать (ВМ выключена) |

Ключи `--live` (только на работающей до перезапуска), `--config` (только в сохранённое описание), `--persistent` (и туда, и туда) встречаются во многих командах.

---

## 4. Создание ВМ: virt-install

### Установка Linux с ISO

```bash
virt-install \
  --name deb13 --memory 4096 --vcpus 4 --cpu host-passthrough \
  --osinfo debian13 \
  --disk size=30,format=qcow2,bus=virtio,discard=unmap \
  --cdrom /var/lib/libvirt/images/debian-13-amd64-netinst.iso \
  --network network=default,model=virtio \
  --graphics spice --boot uefi
```

- `--osinfo` (раньше `--os-variant`) — **обязателен**: libvirt подбирает правильные устройства под систему. Список: `virt-install --osinfo list` или `osinfo-query os` (пакет `osinfo-db-tools`). Если системы нет в списке — `--osinfo linux2024` или `--osinfo detect=on,require=off`.
- `--disk size=30` создаёт файл в пуле `default` (`/var/lib/libvirt/images/`).
- `--boot uefi` — сам найдёт OVMF и создаст копию переменных в `/var/lib/libvirt/qemu/nvram/`.
- Для сервера без графики: `--graphics none --console pty,target_type=serial --extra-args 'console=ttyS0'` вместе с `--location <ISO или URL>` вместо `--cdrom` — установка пойдёт прямо в терминале.

### Готовый облачный образ + cloud-init (быстрее всего)

```bash
cd /var/lib/libvirt/images
sudo curl -LO https://cloud.debian.org/images/cloud/trixie/latest/debian-13-genericcloud-amd64.qcow2
sudo qemu-img create -f qcow2 -b debian-13-genericcloud-amd64.qcow2 -F qcow2 web1.qcow2 20G

virt-install --name web1 --memory 2048 --vcpus 2 --osinfo debian13 \
  --disk web1.qcow2,bus=virtio --import \
  --cloud-init root-ssh-key=$HOME/.ssh/id_ed25519.pub \
  --network network=default,model=virtio --graphics none --noautoconsole
virsh domifaddr web1      # через полминуты — адрес, дальше ssh root@<адрес>
```

Для сложной настройки — свой файл: `--cloud-init user-data=user-data.yaml`.

### Windows 11

```bash
virt-install --name win11 --memory 8192 --vcpus 4 --cpu host-passthrough \
  --osinfo win11 \
  --disk size=80,bus=virtio,discard=unmap \
  --cdrom /var/lib/libvirt/images/Win11.iso \
  --disk /var/lib/libvirt/images/virtio-win.iso,device=cdrom \
  --network network=default,model=virtio \
  --tpm backend.type=emulator,backend.version=2.0,model=tpm-crb \
  --boot uefi,firmware.feature0.name=secure-boot,firmware.feature0.enabled=yes \
  --graphics spice
```

`--osinfo win11` сам включит Hyper-V-оптимизации (`hv_*`). Драйвер диска при установке — с CD `virtio-win` (`viostor\w11\amd64`), после установки — `virtio-win-guest-tools.exe`.

### Клонирование

```bash
virt-clone --original deb13 --name deb13-test --auto-clone     # ВМ-источник выключена
virt-sysprep -d deb13-test                                       # сбросить machine-id, SSH-ключи хоста, логи (guestfs-tools)
```

`virt-sysprep`, `virt-customize`, `virt-builder`, `guestmount` — из пакета **guestfs-tools** (Gentoo `app-emulation/guestfs-tools`, Debian `guestfs-tools`, Arch `guestfs-tools`): правят диски ВМ без запуска.

---

## 5. XML-описание ВМ

Всё, что умеет libvirt, задаётся в XML. Полезно уметь прочитать и поправить через `virsh edit`:

```xml
<domain type='kvm'>
  <name>deb13</name>
  <memory unit='GiB'>4</memory>
  <vcpu placement='static'>4</vcpu>
  <os firmware='efi'>
    <type arch='x86_64' machine='q35'>hvm</type>
  </os>
  <cpu mode='host-passthrough'/>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' cache='none' io='io_uring' discard='unmap'/>
      <source file='/var/lib/libvirt/images/deb13.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
    <channel type='unix'>                       <!-- гостевой агент -->
      <target type='virtio' name='org.qemu.guest_agent.0'/>
    </channel>
    <graphics type='spice' autoport='yes' listen='127.0.0.1'/>
  </devices>
</domain>
```

| Режим `<cpu mode=…>` | Смысл |
| :--- | :--- |
| `host-passthrough` | все возможности процессора хоста — быстрее всего, но живая миграция только на такой же процессор |
| `host-model` (по умолчанию в virt-manager) | ближайшая именованная модель процессора + флаги хоста; переносимее |
| `custom` + `<model>` | фиксированная модель (`EPYC-Genoa`, `x86-64-v3`) для кластера из разных машин |

Посмотреть, какую командную строку QEMU libvirt соберёт из XML: `virsh domxml-to-native qemu-argv --domain deb13`. Журнал запуска и ошибки QEMU — `/var/log/libvirt/qemu/deb13.log`.

---

## 6. Сети

### Сеть default (NAT)

После установки есть сеть **`default`**: мост `virbr0`, подсеть `192.168.122.0/24`, DHCP и DNS через dnsmasq, выход наружу через NAT хоста. ВМ видят интернет и друг друга, а из локальной сети ВМ не видны.

```bash
virsh net-list --all
virsh net-start default && virsh net-autostart default     # если не активна
virsh net-dhcp-leases default                              # кто какой адрес получил
virsh net-dumpxml default
```

Постоянный адрес для ВМ:

```bash
virsh net-update default add ip-dhcp-host \
  "<host mac='52:54:00:12:34:56' name='web1' ip='192.168.122.10'/>" --live --config
```

Правила фаервола для NAT libvirt создаёт сам. С версии 10.4 есть выбор — `firewall_backend = "nftables"` или `"iptables"` в `/etc/libvirt/network.conf` (по умолчанию первый доступный; в Debian приоритет у iptables). Правила nftables лежат в отдельной таблице `libvirt_network` и с вашими правилами не конфликтуют, но если ваш `nftables.conf` начинается с `flush ruleset`, то при его перезагрузке правила libvirt исчезнут — перезапустите сеть (`virsh net-destroy default && virsh net-start default`) или службу.

### Мост в локальную сеть (ВМ — как отдельный компьютер)

Нужен мост `br0` на хосте, в который включена сетевая карта. Хост после этого получает адрес **на мосте**, а не на карте.

**Gentoo (netifrc, OpenRC)** — `/etc/conf.d/net`:

```bash
config_enp1s0="null"
bridge_br0="enp1s0"
config_br0="dhcp"                 # или "192.168.1.10/24" + routes_br0="default via 192.168.1.1"
bridge_forward_delay_br0=0
rc_net_br0_need="net.enp1s0"
```

```bash
cd /etc/init.d && ln -s net.lo net.br0 && ln -s net.lo net.enp1s0
rc-update add net.br0 default && rc-update del net.enp1s0 default 2>/dev/null; rc-service net.br0 start
```

**Debian (ifupdown)** — `apt install bridge-utils`, `/etc/network/interfaces`:

```
auto enp1s0
iface enp1s0 inet manual

auto br0
iface br0 inet dhcp
    bridge_ports enp1s0
    bridge_stp off
    bridge_fd 0
```

**Arch (systemd-networkd)** — три файла в `/etc/systemd/network/`:

```ini
# 10-br0.netdev
[NetDev]
Name=br0
Kind=bridge

# 20-enp1s0.network
[Match]
Name=enp1s0
[Network]
Bridge=br0

# 30-br0.network
[Match]
Name=br0
[Network]
DHCP=yes
```

**Где есть NetworkManager** (любой дистрибутив):

```bash
nmcli con add type bridge ifname br0 con-name br0 stp no
nmcli con add type bridge-slave ifname enp1s0 master br0
nmcli con down "Wired connection 1"; nmcli con up br0
```

> [!warning] Настраивайте мост с консоли, а не по SSH
> При ошибке хост потеряет сеть. На удалённом сервере держите под рукой KVM-консоль/IPMI провайдера. На Wi-Fi-клиенте мост не работает — используйте NAT.

Подключить ВМ к мосту: `virt-install ... --network bridge=br0,model=virtio`, или в XML:

```xml
<interface type='bridge'>
  <source bridge='br0'/>
  <model type='virtio'/>
</interface>
```

### Другие виды сетей

| Вид | Для чего |
| :--- | :--- |
| **isolated** (`<forward>` нет) | сеть только между ВМ и хостом, без выхода наружу — лаборатории, пентест-стенды |
| **routed** (`<forward mode='route'/>`) | маршрутизация без NAT — ВМ видны по своим адресам, если на роутере прописан маршрут |
| **macvtap** (`--network type=direct,source=enp1s0,source_mode=bridge`) | ВМ в локальной сети без настройки моста. Минус: **хост и ВМ не видят друг друга** |
| **open** | libvirt не трогает фаервол — всё настраиваете сами (nftables) |

Своя изолированная сеть:

```bash
cat > lab.xml <<'EOF'
<network>
  <name>lab</name>
  <bridge name='virbr10'/>
  <ip address='10.10.10.1' netmask='255.255.255.0'>
    <dhcp><range start='10.10.10.100' end='10.10.10.200'/></dhcp>
  </ip>
</network>
EOF
virsh net-define lab.xml && virsh net-start lab && virsh net-autostart lab
```

---

## 7. Хранилища (пулы и тома)

**Пул** — место, где лежат диски ВМ; **том** — один диск. Пул `default` — каталог `/var/lib/libvirt/images`.

```bash
virsh pool-list --all
virsh pool-define-as vms dir --target /data/vms && virsh pool-build vms && virsh pool-start vms && virsh pool-autostart vms
virsh vol-create-as vms web2.qcow2 20G --format qcow2
virsh vol-list vms
virsh vol-resize web2.qcow2 30G --pool vms
virsh vol-delete web2.qcow2 --pool vms
```

| Тип пула | Пример |
| :--- | :--- |
| `dir` | каталог с qcow2/raw — проще всего |
| `logical` | группа томов LVM: каждый диск ВМ — логический том (быстрее файла) |
| `zfs` | zvol в пуле ZFS — снапшоты на уровне ФС |
| `netfs` | NFS-ресурс — общий для нескольких хостов (для миграции) |
| `iscsi`, `rbd` | сетевые блочные устройства (СХД, Ceph) |

> [!tip] Файлы дисков на Btrfs
> На Btrfs файлы qcow2 сильно фрагментируются из-за CoW. Для каталога с образами отключите CoW **до** создания файлов: `chattr +C /var/lib/libvirt/images` (подробнее — в заметке [Btrfs](../Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md)).

Диски вне пулов тоже работают, но QEMU запускается от пользователя `qemu` / `libvirt-qemu`, поэтому каталог должен быть ему доступен. Классическая ошибка — образ в `/home/user/`, куда `qemu` не пускают: `Permission denied`. Решения — положить образ в пул или дать права на каталоги (`setfacl -m u:qemu:x /home/user`).

---

## 8. Снапшоты и резервные копии

### Снапшоты

```bash
virsh snapshot-create-as deb13 before-upgrade --description "до dist-upgrade"
virsh snapshot-list deb13
virsh snapshot-revert deb13 before-upgrade
virsh snapshot-delete deb13 before-upgrade
```

| Вид | Как | Особенности |
| :--- | :--- | :--- |
| **Внутренний** (по умолчанию для qcow2) | состояние диска (и памяти, если ВМ работает) внутри файла qcow2 | просто откатывать; не работает с raw-дисками, а у UEFI-ВМ на старых версиях libvirt и QEMU — тогда используйте внешние |
| **Внешний** (`--disk-only`, `--memory`) | исходный файл замораживается, изменения идут в новый файл-наложение | работает с любыми дисками и с работающей ВМ; откат и удаление поддерживаются с libvirt 9.x |

Перед снапшотом работающей ВМ с гостевым агентом добавьте `--quiesce` — агент сбросит буферы ФС в госте.

### Резервная копия диска работающей ВМ

```bash
virsh backup-begin deb13                 # push-бэкап в файлы рядом с дисками (libvirt 7.2+)
virsh domjobinfo deb13                   # прогресс
```

Классический способ — внешний снапшот, копирование «замороженного» базового файла и слияние обратно:

```bash
virsh snapshot-create-as deb13 bk --disk-only --atomic --no-metadata --quiesce
cp /var/lib/libvirt/images/deb13.qcow2 /backup/
virsh blockcommit deb13 vda --active --pivot     # влить изменения обратно в основной файл
rm /var/lib/libvirt/images/deb13.bk              # файл-наложение больше не нужен
virsh dumpxml deb13 > /backup/deb13.xml          # не забыть описание ВМ (и nvram для UEFI)
```

---

## 9. Удалённое управление

libvirt умеет управлять ВМ на другом сервере **через SSH** — на сервере ничего открывать не нужно, кроме SSH:

```bash
virsh -c qemu+ssh://admin@server/system list --all
virt-manager -c qemu+ssh://admin@server/system        # или «Файл → Добавить соединение»
```

Пользователь на сервере должен быть в группе `libvirt`; на сервере нужен `nc` (Arch — `openbsd-netcat`) или встроенный `virt-ssh-helper` (новые версии используют его сами). Удобно с SSH-ключом, см. [SSH-ключи](../../Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md).

Графический экран удалённой ВМ virt-manager пробрасывает через тот же SSH. Ручной вариант — `virt-viewer -c qemu+ssh://admin@server/system web1`.

> [!warning] Не открывайте TCP-порт libvirt
> Режим `qemu+tcp://` без TLS и аутентификации даёт полный контроль над хостом любому, кто дотянется до порта 16509. Используйте `qemu+ssh://` или `qemu+tls://` с сертификатами. Экран ВМ (`<graphics listen=…>`) держите на `127.0.0.1`.

### Живая миграция

```bash
virsh migrate --live --persistent --undefinesource web1 qemu+ssh://server2/system
# диски на общем хранилище (NFS, Ceph); без него — добавить --copy-storage-all
```

Процессоры хостов должны быть совместимы (поэтому для кластеров — `host-model` или фиксированная модель, а не `host-passthrough`).

---

## 10. virt-manager и другие интерфейсы

- **virt-manager** — графический менеджер: мастер создания ВМ, редактор устройств, консоль, графики нагрузки, снапшоты. Работает с локальными и удалёнными (по SSH) хостами. Новые версии по умолчанию создают ВМ с UEFI, TPM для Windows 11 и virtio.
- **virt-viewer / remote-viewer** — только экран ВМ (SPICE/VNC).
- **Cockpit** + модуль `cockpit-machines` — управление ВМ из браузера на сервере.
- **GNOME Boxes** — простой интерфейс поверх libvirt для десктопа (работает с `qemu:///session`).
- **Terraform/OpenTofu** (провайдер `dmacvicar/libvirt`), **Ansible** (`community.libvirt`) — ВМ как код.

---

## 11. Полезные приёмы

### Проброс устройств хоста

```bash
virsh nodedev-list --cap pci             # PCI-устройства хоста
virsh nodedev-list --cap usb_device
virsh attach-device vm1 usb.xml --persistent
```

```xml
<!-- usb.xml: флешка по vendor/product -->
<hostdev mode='subsystem' type='usb' managed='yes'>
  <source><vendor id='0x0bda'/><product id='0x8153'/></source>
</hostdev>
```

PCI-устройство целиком (видеокарта, сетевая карта) — то же с `type='pci'`, но сначала нужны IOMMU (`amd_iommu=on`/`intel_iommu=on`, обычно уже включено) и отдельная IOMMU-группа устройства; `managed='yes'` сам отвяжет его от драйвера хоста.

### Общая папка (virtiofs)

```xml
<memoryBacking>
  <source type='memfd'/>
  <access mode='shared'/>
</memoryBacking>
...
<filesystem type='mount' accessmode='passthrough'>
  <driver type='virtiofs'/>
  <source dir='/srv/share'/>
  <target dir='share'/>
</filesystem>
```

В госте: `mount -t virtiofs share /mnt`. Нужен `virtiofsd` на хосте (Gentoo — USE `virtiofsd`, Debian — `virtiofsd`, Arch — `virtiofsd`).

### Хуки

Скрипт `/etc/libvirt/hooks/qemu` (исполняемый) вызывается при запуске и остановке каждой ВМ с аргументами `<имя ВМ> <prepare|start|started|stopped|release>` — например, чтобы пробросить порт с хоста к ВМ правилом nftables при её старте.

---

## 12. Частые проблемы

| Симптом | Причина и решение |
| :--- | :--- |
| `virsh list --all` пустой, а в virt-manager ВМ есть | вы в `qemu:///session` — `virsh -c qemu:///system list --all` или `LIBVIRT_DEFAULT_URI` |
| `Network 'default' is not active` | `virsh net-start default && virsh net-autostart default`; на Gentoo — USE `virt-network`, на Arch — пакеты `dnsmasq` и `iptables-nft` |
| `Cannot access storage file ... Permission denied` | у пользователя `qemu`/`libvirt-qemu` нет доступа к каталогу; на Debian/Ubuntu — ещё и AppArmor |
| `authentication unavailable: no polkit agent` | пользователь не в группе `libvirt` или не перелогинился |
| ВМ без интернета после перезагрузки nftables | `flush ruleset` удалил правила libvirt — перезапустить сеть (раздел 6) |
| `dnsmasq: failed to bind ... Address already in use` | на хосте уже работает dnsmasq на всех интерфейсах — добавьте ему `bind-interfaces` и `except-interface=virbr0` |
| `unsupported configuration: Domain requires KVM, but it is not available` | нет `/dev/kvm` — см. проверку KVM в заметке про QEMU |
| Нельзя удалить ВМ с UEFI: `cannot undefine domain with nvram` | `virsh undefine vm --nvram` |

## 🔗 Ссылки

- Документация: https://libvirt.org/docs.html
- Справка virsh: https://libvirt.org/manpages/virsh.html
- Формат XML ВМ: https://libvirt.org/formatdomain.html
- Сети: https://libvirt.org/formatnetwork.html
- Модульные службы: https://libvirt.org/daemons.html
- Gentoo Wiki: https://wiki.gentoo.org/wiki/Libvirt
- ArchWiki: https://wiki.archlinux.org/title/Libvirt
- Debian Wiki: https://wiki.debian.org/KVM
- virt-manager: https://virt-manager.org/

Связанные заметки: [QEMU](QEMU%20%E2%80%94%20%D1%8D%D0%BC%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80%20%D0%B8%20%D0%B3%D0%B8%D0%BF%D0%B5%D1%80%D0%B2%D0%B8%D0%B7%D0%BE%D1%80%20%28KVM%2C%20qemu-img%2C%20%D1%81%D0%B5%D1%82%D1%8C%2C%20UEFI%2C%20virtio%2C%20qemu-user%29%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%BD%D0%B0%20Gentoo%2C%20Debian%2C%20Arch.md), [Btrfs](../Filesystems/Btrfs%20%E2%80%94%20%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F%20CoW-%D0%A4%D0%A1%20%28%D0%BF%D0%BE%D0%B4%D1%82%D0%BE%D0%BC%D0%B0%2C%20%D1%81%D0%BD%D0%B0%D0%BF%D1%88%D0%BE%D1%82%D1%8B%2C%20RAID%29%20%E2%80%94%20%D0%BF%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0%20%D0%B8%20%D1%83%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%BE.md), [SSH-ключи](../../Network/SSH/SSH-%D0%9A%D0%BB%D1%8E%D1%87%D0%B8.md).

#Linux #Виртуализация #libvirt #QEMU #KVM #Gentoo
