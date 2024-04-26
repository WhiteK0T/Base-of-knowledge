---
создал заметку: 2024-04-25T15:59:00
tags:
  - WikiGentoo
  - Gentoo
  - Kernel
  - Linux
Источник: https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru
---

## Необязательно: Установка файлов прошивки и/или микрокода

### Файлы прошивки

#### Linux Firmware

Перед тем, как приступить к настройке ядра, полезно будет помнить, что некоторые аппаратные устройства требуют установки в систему дополнительной, иногда не совместимой с принципами FOSS (free (as in freedom) and open source software/свободное и открытое программное обеспечение), прошивки, прежде чем они будут работать правильно. Чаще всего это касается беспроводных сетевых интерфейсов, обычно встречающихся как в настольных, так и в портативных компьютерах. Современные видеочипы от таких производителей, как AMD, Nvidia и Intel также часто требуют установки внешней прошивки для обеспечения полной функциональности. Большинство прошивок для современных аппаратных устройств можно найти в пакете [sys-kernel/linux-firmware](https://packages.gentoo.org/packages/sys-kernel/linux-firmware).

Рекомендуется установить пакет [sys-kernel/linux-firmware](https://packages.gentoo.org/packages/sys-kernel/linux-firmware) перед первоначальной перезагрузкой системы, чтобы прошивка была доступна в случае необходимости:
```bash
emerge --ask sys-kernel/linux-firmware
```
**Заметка**  
Установка определённых пакетов прошивок часто требует принятия соответствующих лицензий на прошивку. При необходимости посетите раздел руководства [о принятии лицензии](https://wiki.gentoo.org/wiki/Handbook:AMD64/Working/Portage/ru#Licenses "Handbook:AMD64/Working/Portage/ru") для получения помощи.

Важно отметить, что символы ядра, собранные как модули (M), при загрузке ядром загружают связанные с ними файлы прошивок из файловой системы. Нет необходимости встраивать в двоичный образ ядра файлы прошивок для них.

#### SOF Firmware

Sound Open Firmware (SOF) is a new open source audio driver meant to replace the proprietary Smart Sound Technology (SST) audio driver from Intel. 10th gen+ and Apollo Lake (Atom E3900, Celeron N3350, and Pentium N4200) Intel CPUs require this firmware for certain features and certain AMD APUs also have support for this firmware. SOF's supported platforms matrix can be found [here](https://thesofproject.github.io/latest/platforms/index.html) for more information.
```bash
emerge --ask sys-firmware/sof-firmware
```
### Микрокод

Вдобавок к сетевому оборудованию и видеокартам, процессоры также могут требовать обновления прошивки. Обычно подобный вид прошивок называется _микрокодом_. Обновления микрокода иногда нужны, чтобы исправить нестабильность, улучшить безопасность, или исправить прочие разнообразные баги в процессоре.

Обновления микрокода для процессоров AMD распространяются в вышеупомянутом пакете [sys-kernel/linux-firmware](https://packages.gentoo.org/packages/sys-kernel/linux-firmware). Обновления микрокода для процессоров Intel находятся в пакете [sys-firmware/intel-microcode](https://packages.gentoo.org/packages/sys-firmware/intel-microcode), который необходимо установить отдельно. См. [статью Микрокол](https://wiki.gentoo.org/wiki/Microcode "Microcode") для получения дополнительной информации о том, как применять обновления микрокода.

## Конфигурация и компиляция ядра

Теперь настало время сконфигурировать и скомпилировать исходные тексты ядра. Для целей процесса установки будут представлены три способа управления ядром, однако в любой момент после установки можно выбрать другой способ.

От наименьшего вмешательства к наибольшему:

[Полностью автоматический подход: Distribution-ядра](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#Distribution_kernels "Handbook:AMD64/Installation/Kernel/ru")

[Проект Distribution Kernel](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel "Project:Distribution Kernel") используется для конфигурации, автоматической сборки и установки ядра Linux, связанных с ним модулей и (опционально, но по умолчанию включено) файла initramfs. Новые обновления ядра полностью автоматизированы, поскольку они обрабатываются через менеджер пакетов, как и любой другой системный пакет. В случае необходимости [можно предоставить пользовательский конфигурационный файл ядра](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel#Modifying_kernel_configuration "Project:Distribution Kernel"). Это наименее сложный процесс и идеально подходит для новых пользователей Gentoo, так как работает "из коробки" и требует минимального участия системного администратора.

[Гибридный подход: Genkernel](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#Alternative:_Genkernel "Handbook:AMD64/Installation/Kernel/ru")

Новые обновления ядра устанавливаются через системный менеджер пакетов. Системные администраторы могут использовать инструмент Gentoo **genkernel** для общей конфигурации, автоматической сборки и установки ядра Linux, связанных с ним модулей и (опционально, но _**не**_ включено по умолчанию) файла initramfs. Можно предоставить пользовательский файл конфигурации ядра, если необходима кастомизация. Будущая конфигурация, сборка и установка ядра требуют участия системного администратора в виде выполнения **eselect kernel, genkernel** и, возможно, других команд для каждого обновления.

[Полностью ручная настройка](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#Alternative:_Manual_configuration "Handbook:AMD64/Installation/Kernel/ru")

Новые исходные тексты ядра устанавливаются с помощью системного менеджера пакетов. Ядро конфигурируется, собирается и устанавливается вручную с помощью команды **eselect kernel** и множества команд **make**. С новыми обновлениями ядра повторяется ручной процесс конфигурирования, сборки и установки файлов ядра. Это самый сложный процесс, но он обеспечивает максимальный контроль над процессом обновления ядра.

Основой, вокруг которой строятся все дистрибутивы, является ядро Linux. Оно является прослойкой между пользовательскими программами и аппаратным обеспечением системы. Хотя руководство предоставляет своим пользователям несколько возможных источников ядра, более подробная информация с более детальным описанием доступна на странице {{|Link|Kernel/Overview|Общие сведения о ядре}}.

**Совет**  
Kernel installation tasks such as, copying the kernel image to /boot or the [EFI System Partition](https://wiki.gentoo.org/wiki/EFI_System_Partition/ru "EFI System Partition/ru"), generating an [initramfs](https://wiki.gentoo.org/wiki/Initramfs "Initramfs") and/or [Unified Kernel Image](https://wiki.gentoo.org/wiki/Unified_Kernel_Image "Unified Kernel Image"), updating bootloader configuration, can be automated with [installkernel](https://wiki.gentoo.org/wiki/Installkernel "Installkernel"). Users may wish to configure and install [sys-kernel/installkernel](https://packages.gentoo.org/packages/sys-kernel/installkernel) before proceeding. See the [Kernel installation section below](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel#Kernel_installation.2Fru "Handbook:AMD64/Installation/Kernel") for more more information.
### Distribution-ядра

_[Distribution-ядра](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel "Project:Distribution Kernel")_ — это ebuild-файлы, которые охватывают полный процесс распаковки, конфигурирования, компиляции и установки ядра. Основным преимуществом этого метода является то, что ядра обновляются до новых версий менеджером пакетов во время обновления @world. Для этого используется только команда **emerge**. Distribution-ядра по умолчанию сконфигурированы для поддержки большинства оборудования, для более тонкой настройки предлагаются два механизма: saveconfig и сниппеты конфигурации. Смотрите страницу проекта для [более подробной информации о конфигурации.](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel#Modifying_kernel_configuration "Project:Distribution Kernel")

#### Установка distribution-ядра

Before installing the kernel package the [dracut](https://packages.gentoo.org/useflags/dracut)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag needs to be added for the package [sys-kernel/installkernel](https://packages.gentoo.org/packages/sys-kernel/installkernel) in [/etc/portage/package.use](https://wiki.gentoo.org/wiki//etc/portage/package.use/ru "/etc/portage/package.use/ru"):

ФАЙЛ **`/etc/portage/package.use/installkernel`** Enable dracut support
```bash
sys-kernel/installkernel dracut
```
Users may also wish to enable additional [sys-kernel/installkernel](https://packages.gentoo.org/packages/sys-kernel/installkernel) USE flags at this stage. See the [Installation/Kernel#Installkernel](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel#Installkernel.2Fru "Handbook:AMD64/Installation/Kernel") section for details.

Чтобы собрать ядро из исходного кода с патчами Gentoo, введите:
```bash
emerge --ask sys-kernel/gentoo-kernel
```
Администраторы систем, которые хотят избежать сборки ядра из исходных текстов на компьютере, могут вместо этого использовать предварительно скомпилированные образы ядра:
```bash
emerge --ask sys-kernel/gentoo-kernel-bin
```
##### Optional: Signed kernel modules

The kernel modules in the prebuilt distribution kernel ([sys-kernel/gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin)) are already signed. To sign the modules of kernels built from source enable the [modules-sign](https://packages.gentoo.org/useflags/modules-sign)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag, and optionally specify which key to use for signing in [/etc/portage/make.conf](https://wiki.gentoo.org/wiki//etc/portage/make.conf/ru "/etc/portage/make.conf/ru"):

ФАЙЛ **`/etc/portage/make.conf` Enable module signing**
```bash
USE="modules-sign"
# Optionally, to use custom signing keys.
MODULES_SIGN_KEY="/path/to/kernel_key.pem"
MODULES_SIGN_CERT="/path/to/kernel_key.pem" # Only required if the MODULES_SIGN_KEY does not also contain the certificate.
MODULES_SIGN_HASH="sha512" # Defaults to sha512.
```
If **MODULES_SIGN_KEY** is not specified the kernel build system will generate a key, it will be stored in **/usr/src/linux-x.y.z/certs**. It is recommended to manually generate a key to ensure that it will be the same for each kernel release. A key may be generated with:
```bash
openssl req -new -nodes -utf8 -sha256 -x509 -outform PEM -out kernel_key.pem -keyout kernel_key.pem
```
**Заметка**  
The **MODULES_SIGN_KEY** and **MODULES_SIGN_CERT** may be different files. For this example the pem file generated by OpenSSL includes both the key and the accompanying certificate, and thus both variables are set to the same value.

OpenSSL will ask some questions about the user generating the key, it is recommended to fill in these questions as detailed as possible.

Store the key in a safe location, at the very least the key should be readable only by the root user. Verify this with:

```bash
root # ls -l kernel_key.pem
 -r-------- 1 root root 3164 Jan  4 10:38 kernel_key.pem 
```

If this outputs anything other then the above, correct the permissions with:
```bash
chown root:root kernel_key.pem
chmod 400 kernel_key.pem
```
##### Optional: Signing the kernel image (Secure Boot)

The kernel image in the prebuilt distribution kernel ([sys-kernel/gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin)) is already signed for use with [Secure Boot](https://wiki.gentoo.org/wiki/Secure_Boot "Secure Boot"). To sign the kernel image of kernels built from source enable the [secureboot](https://packages.gentoo.org/useflags/secureboot)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag, and optionally specify which key to use for signing in [/etc/portage/make.conf](https://wiki.gentoo.org/wiki//etc/portage/make.conf/ru "/etc/portage/make.conf/ru"). Note that signing the kernel image for use with secureboot requires that the kernel modules are also signed, the same key may be used to sign both the kernel image and the kernel modules:

ФАЙЛ **`/etc/portage/make.conf` Enable custom signing keys**

```bash
USE="modules-sign secureboot"
# Optionally, to use custom signing keys.
MODULES_SIGN_KEY="/path/to/kernel_key.pem"
MODULES_SIGN_CERT="/path/to/kernel_key.pem" # Only required if the MODULES_SIGN_KEY does not also contain the certificate.
MODULES_SIGN_HASH="sha512" # Defaults to sha512.

# Optionally, to boot with secureboot enabled, may be the same or different signing key.
SECUREBOOT_SIGN_KEY="/path/to/kernel_key.pem"
SECUREBOOT_SIGN_CERT="/path/to/kernel_key.pem"
```

**Заметка**  
The **SECUREBOOT_SIGN_KEY** and **SECUREBOOT_SIGN_CERT** may be different files. For this example the pem file generated by OpenSSL includes both the key and the accompanying certificate, and thus both variables are set to the same value.

**Заметка**  
For this example the same key that was generated to sign the modules is used to sign the kernel image. It is also possible to generate and use a second separate key for signing the kernel image. The same OpenSSL command as in the previous section may be used again.

See the above section for instructions on generating a new key, the steps may be repeated if a separate key should be used to sign the kernel image.

To successfully boot with Secure Boot enabled, the used bootloader must also be signed and the certificate must be accepted by the [UEFI](https://wiki.gentoo.org/wiki/UEFI "UEFI") firmware or [Shim](https://wiki.gentoo.org/wiki/Shim "Shim"). This will be explained later in the handbook.

#### Обновление и очистка

После установки ядра менеджер пакетов будет автоматически обновлять его до более новых версий. Предыдущие версии будут храниться до тех пор, пока менеджер пакетов не получит запрос на очистку устаревших пакетов. Чтобы освободить место на диске, устаревшие пакеты можно удалить, периодически запуская emerge с опцией `--depclean`:

Также можно удалить именно устаревшие ядра:
```bash
emerge --prune sys-kernel/gentoo-kernel sys-kernel/gentoo-kernel-bin
```
#### Задачи после установки/обновления

Distribution-ядра способны пере собирать модули ядра, установленные другими пакетами. linux-mod.eclass предоставляет USE-флаг `dist-kernel`, который управляет зависимостью от под слота [virtual/dist-kernel](https://packages.gentoo.org/packages/virtual/dist-kernel).

Включение этого USE-флага для таких пакетов, как [sys-fs/zfs](https://packages.gentoo.org/packages/sys-fs/zfs) и [sys-fs/zfs-kmod](https://packages.gentoo.org/packages/sys-fs/zfs-kmod) позволит им автоматически пере собираться в соответствии с обновленным ядром и, в случае необходимости, пере собирать initramfs.

##### Ручная пере сборка initramfs

Если понадобится, вручную запустите перестройку, выполнив после обновления ядра команду:
```bash
emerge --ask @module-rebuild
```
Если какой-то модуль ядра (например, ZFS) необходим при ранней загрузке, пере соберите initramfs при помощи:
```bash
emerge --config sys-kernel/gentoo-kernel
emerge --config sys-kernel/gentoo-kernel-bin
```
### Установка исходного кода ядра

**Заметка**  
Этот раздел актуален только при использовании следующих методов **genkernel** (гибридного) или ручного подхода к управлению ядром.

The use of [sys-kernel/installkernel](https://packages.gentoo.org/packages/sys-kernel/installkernel) is not strictly required, but highly recommended. When this package is installed, the kernel installation process will be delegated to [installkernel](https://wiki.gentoo.org/wiki/Installkernel "Installkernel"). This allows for installing several different kernel versions side-by-side as well as managing and automating several tasks relating to kernel installation described [later](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel#Kernel_installation.2Fru "Handbook:AMD64/Installation/Kernel") in the handbook. Install it now with:
```bash
emerge --ask sys-kernel/installkernel
```
При установке и компиляции ядра для систем на базе amd64 Gentoo рекомендует использовать пакет [sys-kernel/gentoo-sources](https://packages.gentoo.org/packages/sys-kernel/gentoo-sources).

Выберите подходящий исходный код ядра и установите его с помощью **emerge**:
```bash
emerge --ask sys-kernel/gentoo-sources
```
Данная команда установит исходный код ядра Linux в **/usr/src/**, используя в названии версию ядра. Эта команда не установит автоматически символьную ссылку, пока вы не укажете USE-флаг [symlink](https://packages.gentoo.org/useflags/symlink)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") для выбранного исходного кода ядра.

Обычно, символьная ссылка **/usr/src/linux** указывает на исходный код текущего работающего ядра. Однако, эта символьная ссылка не создаётся по умолчанию. Создать её поможет kernel модуль для eselect.

Чтобы подробнее узнать, зачем нужна эта символьная ссылка и как ею управлять, смотрите [Kernel/Upgrade](https://wiki.gentoo.org/wiki/Kernel/Upgrade/ru "Kernel/Upgrade/ru").

Для начала, просмотрите список установленных ядер (в виде исходного кода):
```
eselect kernel list

Available kernel symlink targets:
  [1]   linux-6.6.21-gentoo
```

Для того, чтобы создать символьную ссылку linux, используйте:
```bash
eselect kernel set 1
ls -l /usr/src/linux

lrwxrwxrwx    1 root   root    20 мар  3 22:44 /usr/src/linux -> linux-6.6.21-gentoo
```
### Альтернатива: Genkernel

**Заметка**  
In case it was missed, this section requires [the kernel sources to be installed.](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#Installing_the_kernel_sources "Handbook:AMD64/Installation/Kernel/ru") Be sure to obtain the relevant kernel sources, then return here for the rest of section.

Если полностью ручная настройка кажется слишком сложной, системным администраторам следует рассмотреть возможность использования утилиты [genkernel](https://wiki.gentoo.org/wiki/Genkernel/ru "Genkernel/ru") в качестве гибридного подхода к обслуживанию ядра.

Genkernel предоставляет базовый файл конфигурации ядра и соберет ядро и initramfs, а затем устанавливает полученные двоичные файлы в соответствующие места. Это обеспечивает минимальную и базовую аппаратную поддержку при первой загрузке системы, а в дальнейшем позволяет дополнительно контролировать обновление и настраивать конфигурацию ядра.

Учтите: хотя использование **genkernel** для поддержки ядра обеспечивает системным администраторам больший контроль над обновлением ядра системы, initramfs и других опций, это _требует_ затрат времени и усилий для выполнения будущих обновлений ядра по мере выпуска новых источников. Тем, кто ищет автоматический подход к обслуживанию ядра, следует [использовать distribution-ядра](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#Alternative:_Using_distribution_kernels "Handbook:AMD64/Installation/Kernel/ru").

Для большей ясности, это является _заблуждением_, что genkernel автоматически генерирует _специальную_ конфигурацию ядра для оборудования, на котором он запущен; он использует определённую конфигурацию ядра, которая поддерживает большинство оборудования и автоматически обрабатывает команды **make**, необходимые для сборки и установки ядра, сопутствующих модулей и файла initramfs.

#### Группа лицензий на "программное обеспечение, распространяемое в бинарном виде"

Если пакет linux-firmware был уже установлен, перейдите к разделу [установки](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#Installation "Handbook:AMD64/Installation/Kernel/ru").

Поскольку по умолчанию для пакета [sys-kernel/genkernel](https://packages.gentoo.org/packages/sys-kernel/genkernel) включен USE-флаг `firwmare`, пакетный менеджер также попытается установить пакет [sys-kernel/linux-firmware](https://packages.gentoo.org/packages/sys-kernel/linux-firmware). Перед установкой linux-firmware необходимо принять лицензии на "программное обеспечение, распространяемое в бинарном виде".

Эта группа лицензий может быть принята для всей системы путем добавления `@BINARY-REDISTRIBUTABLE` в переменную ACCEPT_LICENSE в файле **/etc/portage/make.conf**. Лицензия также может быть принята только для пакета linux-firmware с помощью добавления в файле **/etc/portage/package.license/linux-firmware**.

При необходимости ознакомьтесь с [методами разрешения лицензий на программное обеспечение](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base/ru#Optional:_Configure_the_ACCEPT_LICENSE_variable "Handbook:AMD64/Installation/Base/ru"), о которых говорится в главе руководства [Установка базовой системы](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base/ru "Handbook:AMD64/Installation/Base/ru") , а затем внесите некоторые изменения для допустимых лицензий на программное обеспечение.

Для упрощения, примеры разрешения лицензий:
```bash
mkdir /etc/portage/package.license
```

ФАЙЛ **`/etc/portage/package.license/linux-firmware` Разрешения лицензий на "программное обеспечение, распространяемое в бинарном виде" для linux-firmware**
```bash
sys-kernel/linux-firmware @BINARY-REDISTRIBUTABLE
```

#### Установка

Итак, установите пакет [sys-kernel/genkernel](https://packages.gentoo.org/packages/sys-kernel/genkernel):
```bash
emerge --ask sys-kernel/genkernel
```
#### Генерация

Скомпилируйте исходные тексты ядра, выполнив команду **genkernel all**. Имейте в виду, что, поскольку **genkernel** компилирует ядро, поддерживающее широкий набор аппаратных средств для различных архитектур компьютеров, процесс компиляции может занять довольно много времени.

**Заметка**  
Если для корневого раздела/тома используется файловая система, отличная от ext4, может потребоваться вручную настроить ядра с помощью **genkernel --menuconfig all**, чтобы добавить встроенную поддержку ядра для данной файловой системы (т.е. не собирать файловую систему как модуль).

**Заметка**  
Пользователи LVM2 должны добавить `--lvm` в качестве аргумента к команде genkernel ниже.
```bash
genkernel --mountboot --install all
```
По завершению работы genkernel будут сформированы ядро, полный набор модулей и файловая система инициализации (initramfs). Ядро и initrd нам понадобятся позднее. Запишите название файлов ядра и initrd, так как они нам понадобятся при настройке загрузчика. Initrd запускается сразу после ядра для определения оборудования (как при загрузке установочного CD), перед запуском самой системы.

После завершения работы genkernel, ядро и начальная файловая система ram (initramfs) будут сформированы и установлены в каталог /boot. Соответствующие модули будут установлены в каталог /lib/modules. initramfs будет запущена сразу после загрузки ядра для автоматического определения оборудования (как при загрузке "живого" (live) загрузочного диска).
```bash
ls /boot/vmlinu* /boot/initramfs*
ls /lib/modules
```
### Альтернатива: Ручная настройка

#### Введение

**Заметка**  
In case it was missed, this section requires [the kernel sources to be installed.](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#Installing_the_kernel_sources "Handbook:AMD64/Installation/Kernel/ru") Be sure to obtain the relevant kernel sources, then return here for the rest of section.

Согласно расхожему мнению, настройка ядра — одна из наиболее сложных процедур, с которыми приходится сталкиваться администратору системы. Это совсем не так — после пары-тройки настроек не всякий вспомнит, что это было сложно!

Однако одна вещь является истиной: при ручной конфигурации ядра очень важно понимать свою систему. Большую часть сведений можно почерпнуть, установив пакет [sys-apps/pciutils](https://packages.gentoo.org/packages/sys-apps/pciutils), который содержит в команду lspci:
```bash
emerge --ask sys-apps/pciutils
```

**Заметка**  
Находясь внутри изолированного окружения chroot, можно спокойно игнорировать любые предупреждения pcilib (например, _pcilib: cannot open /sys/bus/pci/devices_), которые могут появляться в выводе lspci.

Другим источником информации о системе может стать вывод команды lsmod, по которому можно понять, какие модули ядра использует установочный носитель, чтобы потом включить аналогичные настройки.

Остаётся перейти в каталог с ядром и выполнить make menuconfig, который запустит экран меню конфигурации.
```bash
cd /usr/src/linux
make menuconfig
```
В конфигурации ядра Linux есть много-много разделов. Сначала пройдёмся по пунктам, которые должны быть обязательно включены (иначе Gentoo будет работать неправильно или же вовсе не запустится). Также в вики есть [Руководство по настройке ядра Gentoo](https://wiki.gentoo.org/wiki/Kernel/Gentoo_Kernel_Configuration_Guide/ru "Kernel/Gentoo Kernel Configuration Guide/ru"), которое поможет понять более тонкие детали.

#### Включение обязательных параметров

При использовании [sys-kernel/gentoo-sources](https://packages.gentoo.org/packages/sys-kernel/gentoo-sources), строго рекомендуется включить Gentoo-специфичные настройки. С помощью них включается необходимый минимум настроек ядра для корректной работы:

ЯДРО **Включение Gentoo-специфичных настроек**

```
Gentoo Linux --->
  Generic Driver Options --->
    [*] Gentoo Linux support
    [*]   Linux dynamic and persistent device naming (userspace devfs) support
    [*]   Select options required by Portage features
        Support for init systems, system and service managers  --->
          [*] OpenRC, runit and other script based systems and managers
          [*] systemd
```

Выбор в последних двух строках зависит от того, какую систему инициализации вы выбрали — [OpenRC](https://wiki.gentoo.org/wiki/OpenRC/ru "OpenRC/ru") или [systemd](https://wiki.gentoo.org/wiki/Systemd/ru "Systemd/ru"). Ничего страшного не случится, если вы включите поддержку обоих систем.

При использовании [sys-kernel/vanilla-sources](https://packages.gentoo.org/packages/sys-kernel/vanilla-sources), этих вспомогательных настроек не будет. Вы можете включить нужные настройки вручную, но это выходит за рамки данного руководства.

#### Включение поддержки основных компонентов системы

Убедитесь, что все драйверы, необходимые для загрузки системы (такие как контроллер SATA, поддержка блочных устройств NVMe, поддержка файловой системы и другие) собраны прямо в ядре, а не в виде модуля. В противном случае, система может не загрузиться.

Далее следует выбрать тип процессора. Также рекомендуется включить возможности MCE (если они доступны), чтобы пользователи системы могли получать оповещение о любых проблемах с оборудованием. На некоторых архитектурах (например, x86_64) подобные ошибки выводятся не в dmesg, а в /dev/mcelog. А для него понадобится пакет [app-admin/mcelog](https://packages.gentoo.org/packages/app-admin/mcelog).

Также включите _Maintain a devtmpfs file system to mount at /dev_, чтобы критически важные файлы устройств были доступны на самом раннем этапе загрузки (CONFIG_DEVTMPFS и CONFIG_DEVTMPFS_MOUNT):

ЯДРО **Включение поддержки devtmpfs (CONFIG_DEVTMPFS)**

```
Device Drivers --->
  Generic Driver Options --->
    [*] Maintain a devtmpfs filesystem to mount at /dev
    [*]   Automount devtmpfs at /dev, after the kernel mounted the rootfs
```

Убедитесь, что поддержка SCSI-дисков включена (CONFIG_BLK_DEV_SD):

ЯДРО **Включение поддержки SCSI-дисков (CONFIG_SCSI, CONFIG_BLK_DEV_SD)**

```
Device Drivers --->
  SCSI device support  ---> 
    <*> SCSI device support
    <*> SCSI disk support
```

ЯДРО **Включение базовой поддержки SATA и PATA (CONFIG_ATA_ACPI, CONFIG_SATA_PMP, CONFIG_SATA_AHCI, CONFIG_ATA_BMDMA, CONFIG_ATA_SFF, CONFIG_ATA_PIIX)**

```
Device Drivers --->
  <*> Serial ATA and Parallel ATA drivers (libata)  --->
    [*] ATA ACPI Support
    [*] SATA Port Multiplier support
    <*> AHCI SATA support (ahci)
    [*] ATA BMDMA support
    [*] ATA SFF support (for legacy IDE and PATA)
    <*> Intel ESB, ICH, PIIX3, PIIX4 PATA/SATA support (ata_piix)
```

Убедитесь, что включена базовая поддержка NVMe:

ЯДРО **Включение базовой поддержки NVMe для Linux 4.4.x (CONFIG_BLK_DEV_NVME)**

```
Device Drivers  --->
  <*> NVM Express block device
```

ЯДРО **Включение базовой поддержки NVMe для Linux 5.x.x (CONFIG_DEVTMPFS)**

```
Device Drivers --->
  NVME Support --->
    <*> NVM Express block device
```

Не помешает включить следующую дополнительную поддержку NVMe:

ЯДРО **Включение дополнительной поддержки NVMe (CONFIG_NVME_MULTIPATH, CONFIG_NVME_MULTIPATH, CONFIG_NVME_HWMON, CONFIG_NVME_FC, CONFIG_NVME_TCP, CONFIG_NVME_TARGET, CONFIG_NVME_TARGET_PASSTHRU, CONFIG_NVME_TARGET_LOOP, CONFIG_NVME_TARGET_FC, CONFIG_NVME_TARGET_FCLOOP, CONFIG_NVME_TARGET_TCP**

```
[*] NVMe multipath support
[*] NVMe hardware monitoring
<M> NVM Express over Fabrics FC host driver
<M> NVM Express over Fabrics TCP host driver
<M> NVMe Target support
  [*]   NVMe Target Passthrough support
  <M>   NVMe loopback device support
  <M>   NVMe over Fabrics FC target driver
  < >     NVMe over Fabrics FC Transport Loopb
  <M>   NVMe over Fabrics TCP target support
```

Теперь перейдите в раздел File Systems и выберите те файловые системы, которые планируете использовать. Файловая система, используемая в качестве корневой, должна быть включена в ядро (не модулем), иначе система не сможет подключить раздел при загрузке. Также включите _Virtual memory_ и _/proc file system_. При необходимости выберите один или несколько параметров, необходимых системе:

ЯДРО **Включение поддержки файловой системы (CONFIG_EXT2_FS, CONFIG_EXT3_FS, CONFIG_EXT4_FS, CONFIG_BTRFS_FS, CONFIG_XFS_FS, CONFIG_MSDOS_FS, CONFIG_VFAT_FS, CONFIG_PROC_FS, и CONFIG_TMPFS)**

```
File systems --->
  <*> Second extended fs support
  <*> The Extended 3 (ext3) filesystem
  <*> The Extended 4 (ext4) filesystem
  <*> Btrfs filesystem support
  <*> XFS filesystem support
  DOS/FAT/NT Filesystems  --->
    <*> MSDOS fs support
    <*> VFAT (Windows-95) fs support
  Pseudo Filesystems --->
    [*] /proc file system support
    [*] Tmpfs virtual memory file system support (former shm fs)
```

Если для подключения к Интернету используется PPPoE или модемное соединение, то включите следующие параметры (CONFIG_PPP, CONFIG_PPP_ASYNC и CONFIG_PPP_SYNC_TTY):

ЯДРО **Включение поддержки PPPoE (PPPoE, CONFIG_PPPOE, CONFIG_PPP_ASYNC, CONFIG_PPP_SYNC_TTY**

```
Device Drivers --->
  Network device support --->
    <*> PPP (point-to-point protocol) support
    <*> PPP over Ethernet
    <*> PPP support for async serial ports
    <*> PPP support for sync tty ports
```

Два параметра сжатия не повредят, но и не являются обязательными, как и PPP over Ethernet. Фактически, последний используется в случае, если ppp сконфигурирован на использование ядерный PPPoE режим.

Не забудьте настроить поддержку сетевых карт (Ethernet или беспроводных).

Поскольку большинство современных систем являются многоядерными, важно включить _Symmetric multi-processing support_ (CONFIG_SMP):

ЯДРО **Включение поддержки SMP (CONFIG_SMP)**

```
Processor type and features  --->
  [*] Symmetric multi-processing support
```

**Заметка**  
Во многоядерных системах каждое ядро считается за один процессор.

Если используются USB-устройства ввода (например, клавиатура и мышь) или другие устройства, то не забудьте включить и эти параметры:

ЯДРО **Включение поддержки USB и HID(CONFIG_HID_GENERIC, CONFIG_USB_HID, CONFIG_USB_SUPPORT, CONFIG_USB_XHCI_HCD, CONFIG_USB_EHCI_HCD, CONFIG_USB_OHCI_HCD, (CONFIG_HID_GENERIC, CONFIG_USB_HID, CONFIG_USB_SUPPORT, CONFIG_USB_XHCI_HCD, CONFIG_USB_EHCI_HCD, CONFIG_USB_OHCI_HCD, CONFIG_USB4)**

```
Device Drivers --->
  HID support  --->
    -*- HID bus support
    <*>   Generic HID driver
    [*]   Battery level reporting for HID devices
      USB HID support  --->
        <*> USB HID transport layer
  [*] USB support  --->
    <*>     xHCI HCD (USB 3.0) support
    <*>     EHCI HCD (USB 2.0) support
    <*>     OHCI HCD (USB 1.1) support
  <*> Unified support for USB4 and Thunderbolt  --->
```

#### Optional: Signed kernel modules

To automatically sign the kernel modules enable *CONFIG_MODULE_SIG_ALL*:

ЯДРО **Sign kernel modules CONFIG_MODULE_SIG_ALL**

```
[*] Enable loadable module support  
  -*-   Module signature verification    
    [*]     Automatically sign all modules    
    Which hash algorithm should modules be signed with? (Sign modules with SHA-512) --->
```

Optionally change the hash algorithm if desired.

To enforce that all modules are signed with a valid signature, enable *CONFIG_MODULE_SIG_FORCE* as well:

ЯДРО **Enforce signed kernel modules CONFIG_MODULE_SIG_FORCE**

```
[*] Enable loadable module support  
  -*-   Module signature verification    
    [*]     Require modules to be validly signed
    [*]     Automatically sign all modules
    Which hash algorithm should modules be signed with? (Sign modules with SHA-512) --->
```

To use a custom key, specify the location of this key in *CONFIG_MODULE_SIG_KEY*, if unspecified the kernel build system will generate a key. It is recommended to generate one manually instead. This can be done with:
```bash
openssl req -new -nodes -utf8 -sha256 -x509 -outform PEM -out kernel_key.pem -keyout kernel_key.pem
```
OpenSSL will ask some questions about the user generating the key, it is recommended to fill in these questions as detailed as possible.

Store the key in a safe location, at the very least the key should be readable only by the root user. Verify this with:

```bash
ls -l kernel_key.pem 
 -r-------- 1 root root 3164 Jan  4 10:38 kernel_key.pem 
```

If this outputs anything other then the above, correct the permissions with:
```bash
chown root:root kernel_key.pem
chmod 400 kernel_key.pem
```
ЯДРО **Specify signing key CONFIG_MODULE_SIG_KEY**

```
-*- Cryptographic API  ---> 
  Certificates for signature checking  --->  
    (/path/to/kernel_key.pem) File name or PKCS#11 URI of module signing key
```

To also sign external kernel modules installed by other packages via `linux-mod-r1.eclass`, enable the [modules-sign](https://packages.gentoo.org/useflags/modules-sign)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag globally:

ФАЙЛ **`/etc/portage/make.conf` Enable module signing**

```bash
USE="modules-sign"
# Optionally, when using custom signing keys.
MODULES_SIGN_KEY="/path/to/kernel_key.pem"
MODULES_SIGN_CERT="/path/to/kernel_key.pem" # Only required if the MODULES_SIGN_KEY does not also contain the certificate
MODULES_SIGN_HASH="sha512" # Defaults to sha512
```

**Заметка**  
The **MODULES_SIGN_KEY** and **MODULES_SIGN_CERT** may be different files. For this example the pem file generated by OpenSSL includes both the key and the accompanying certificate, and thus both variables are set to the same value.

#### Optional: Signing the kernel image (Secure Boot)

When signing the kernel image (for use on systems with [Secure Boot](https://wiki.gentoo.org/wiki/Secure_Boot "Secure Boot") enabled) it is recommended to set the following kernel config options:

ЯДРО **Lockdown for secureboot**

```
General setup  --->
  Kexec and crash features  --->   
    [*] Enable kexec system call                                                                                          
    [*] Enable kexec file based system call                                                                               
    [*]   Verify kernel signature during kexec_file_load() syscall                                                        
    [*]     Require a valid signature in kexec_file_load() syscall                                                        
    [*]     Enable ""image"" signature verification support

[*] Enable loadable module support  
  -*-   Module signature verification    
    [*]     Require modules to be validly signed
    [*]     Automatically sign all modules
    Which hash algorithm should modules be signed with? (Sign modules with SHA-512) --->  

Security options  ---> 
[*] Integrity subsystem   
  [*] Basic module for enforcing kernel lockdown                                                                       
  [*]   Enable lockdown LSM early in init                                                                       
        Kernel default lockdown mode (Integrity)  --->            

  [*]   Digital signature verification using multiple keyrings                                                            
  [*]     Enable asymmetric keys support                                                                                     
  -*-       Require all keys on the integrity keyrings be signed                                                              
  [*]       Provide keyring for platform/firmware trusted keys                                                                
  [*]       Provide a keyring to which Machine Owner Keys may be added                                                        
  [ ]         Enforce Machine Keyring CA Restrictions
```

Where ""image"" is a placeholder for the architecture specific image name. These options, from the top to the bottom: enforces that the kernel image in a kexec call must be signed (kexec allows replacing the kernel in-place), enforces that kernel modules are signed, enables lockdown integrity mode (prevents modifying the kernel at runtime), and enables various keychains.

On arches that do not natively support decompressing the kernel (e.g. **arm64** and **riscv**), the kernel must be built with its own decompressor (zboot):

ЯДРО **zboot CONFIG_EFI_ZBOOT**

```
Device Drivers --->                                               
  Firmware Drivers --->                                           
    EFI (Extensible Firmware Interface) Support --->              
      [*] Enable the generic EFI decompressor
```

After compilation of the kernel, as explained in the next section, the kernel image must be signed. First install [app-crypt/sbsigntools](https://packages.gentoo.org/packages/app-crypt/sbsigntools) and then sign the kernel image:
```bash
emerge --ask app-crypt/sbsigntools

sbsign /usr/src/linux-x.y.z/path/to/kernel-image --cert /path/to/kernel_key.pem --key /path/to/kernel_key.pem --out /usr/src/linux-x.y.z/path/to/kernel-image
```

**Заметка**  
For this example the same key that was generated to sign the modules is used to sign the kernel image. It is also possible to generate and use a second sperate key for signing the kernel image. The same OpenSSL command as in the previous section may be used again.

Then proceed with the installation.

To automatically sign EFI executables installed by other packages, enable the [secureboot](https://packages.gentoo.org/useflags/secureboot)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag globally:

ФАЙЛ **`/etc/portage/make.conf` Enable Secure Boot**

```bash
USE="modules-sign secureboot"

# Optionally, to use custom signing keys.
MODULES_SIGN_KEY="/path/to/kernel_key.pem"
MODULES_SIGN_CERT="/path/to/kernel_key.pem" # Only required if the MODULES_SIGN_KEY does not also contain the certificate.
MODULES_SIGN_HASH="sha512" # Defaults to sha512

# Optionally, to boot with secureboot enabled, may be the same or different signing key.
SECUREBOOT_SIGN_KEY="/path/to/kernel_key.pem"
SECUREBOOT_SIGN_CERT="/path/to/kernel_key.pem"
```

**Заметка**  
The **SECUREBOOT_SIGN_KEY** and **SECUREBOOT_SIGN_CERT** may be different files. For this example the pem file generated by OpenSSL includes both the key and the accompanying certificate, and thus both variables are set to the same value.

**Заметка**  
When generating an [Unified Kernel Image](https://wiki.gentoo.org/wiki/Unified_Kernel_Image "Unified Kernel Image") with systemd's `ukify` the kernel image will be signed automatically before inclusion in the unified kernel image and it is not necessary to sign it manually.

#### Настройка ядра, специфичная для архитектуры

Если необходимо поддерживать 32-битные программы, убедитесь, что выбраны пункты IA32 Emulation и 32-bit time_t (CONFIG_IA32_EMULATION и CONFIG_COMPAT_32BIT_TIME). Gentoo устанавливает систему multilib (смешанные 32/64-битные вычисления) по умолчанию, поэтому, если не был выбран профиль no-multilib, то эти параметры необходимы.

ЯДРО **Выбор типа процессора и возможностей**

```
Processor type and features  --->
   [ ] Machine Check / overheating reporting 
   [ ]   Intel MCE Features
   [ ]   AMD MCE Features
   Processor family (AMD-Opteron/Athlon64)  --->
      ( ) Opteron/Athlon64/Hammer/K8
      ( ) Intel P4 / older Netburst based Xeon
      ( ) Core 2/newer Xeon
      ( ) Intel Atom
      ( ) Generic-x86-64
Binary Emulations --->
   [*] IA32 Emulation
General architecture-dependent options  --->
   [*] Provide system calls for 32-bit time_t
```

Включите поддержку меток GPT, если использовали их ранее при разбиении диска (CONFIG_PARTITION_ADVANCED и CONFIG_EFI_PARTITION):

ЯДРО **Включение поддержки GPT**

```
-*- Enable the block layer --->
   Partition Types --->
      [*] Advanced partition selection
      [*] EFI GUID Partition support
```

Включите поддержку EFI stub, EFI variables и EFI Framebuffer в ядре Linux, если для загрузки системы используется UEFI (CONFIG_EFI, CONFIG_EFI_STUB, CONFIG_EFI_MIXED, CONFIG_EFI_VARS и CONFIG_FB_EFI):

ЯДРО **Включение поддержки UEFI**

```
Processor type and features  --->
    [*] EFI runtime service support 
    [*]   EFI stub support
    [*]     EFI mixed-mode support
 
Device Drivers
    Firmware Drivers  --->
        EFI (Extensible Firmware Interface) Support  --->
            <*> EFI Variable Support via sysfs
    Graphics support  --->
        Frame buffer Devices  --->
            <*> Support for frame buffer devices  --->
                [*]   EFI-based Framebuffer Support
```

Чтобы включить параметры ядра для использования описанной выше [прошивки SOF](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Kernel/ru#SOF_Firmware "Handbook:AMD64/Installation/Kernel/ru"):

ЯДРО **Включение поддержки прошивки SOF (CONFIG_SND_SOC_SOF_TOPLEVEL, CONFIG_SND_SOC_SOF_PCI, CONFIG_SND_SOC_SOF_ACPI, CONFIG_SND_SOC_SOF_AMD_TOPLEVEL, CONFIG_SND_SOC_SOF_INTEL_TOPLEVEL)**

```
Device Drivers --->
  Sound card support --->
    Advanced Linux Sound Architecture --->
      <M> ALSA for SoC audio support --->
        [*] Sound Open Firmware Support --->
            <M> SOF PCI enumeration support
            <M> SOF ACPI enumeration support
            <M> SOF support for AMD audio DSPs
            [*] SOF support for Intel audio DSPs
```

#### Компиляция и установка

Когда настройка закончена, настало время скомпилировать и установить ядро. Выйдите из настройки и запустите процесс компиляции:
```bash
make && make modules_install
```
**Заметка**  
Можно включить параллельную сборку, используя **make -jX**, где `X` — это число параллельных задач, которые может запустить процесс сборки. Это похоже на инструкции, которые были даны ранее относительно файла **/etc/portage/make.conf** в части переменной *MAKEOPTS*.

По завершении компиляции, скопируйте образ ядра в каталог **/boot/**. Это делается командой **make install**:
```bash
make install
```
Данная команда скопирует образ ядра в каталог **/boot/** вместе с файлом **System.map** и файлом настройки ядра.

## Kernel installation

### Installkernel

[Installkernel](https://wiki.gentoo.org/wiki/Installkernel "Installkernel") may be used to automate, the kernel installation, [initramfs](https://wiki.gentoo.org/wiki/Initramfs "Initramfs") generation, [unified kernel image](https://wiki.gentoo.org/wiki/Unified_kernel_image "Unified kernel image") generation and/or bootloader configuration among other things. [sys-kernel/installkernel](https://packages.gentoo.org/packages/sys-kernel/installkernel) implements two paths of achieving this: the traditional **installkernel** originating from Debian and [systemd](https://wiki.gentoo.org/wiki/Systemd/ru "Systemd/ru")'s **kernel-install**. Which one to choose depends, among other things, on the system's bootloader. By default systemd's **kernel-install** is used on systemd profiles, while the traditional **installkernel** is the default for other profiles.

If unsure, follow the 'Traditional layout' subsection below.

#### systemd-boot

When using [systemd-boot](https://wiki.gentoo.org/wiki/Systemd/systemd-boot "Systemd/systemd-boot") (formerly gummiboot) as the bootloader, systemd's **kernel-install** must be used. Therefore ensure the [systemd](https://packages.gentoo.org/useflags/systemd)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") and the [systemd-boot](https://packages.gentoo.org/useflags/systemd-boot)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flags are enabled on [sys-kernel/installkernel](https://packages.gentoo.org/packages/sys-kernel/installkernel), and then install the relevant package for systemd-boot.

On **OpenRC** systems:

ФАЙЛ **`/etc/portage/package.use/systemd-boot`**

```bash
sys-apps/systemd-utils boot kernel-install
sys-kernel/installkernel systemd systemd-boot
```

`emerge --ask sys-apps/systemd-utils`

On **systemd** systems:

ФАЙЛ **`/etc/portage/package.use/systemd`**

```bash
sys-apps/systemd boot
sys-kernel/installkernel systemd-boot
```

`emerge --ask sys-apps/systemd`

#### GRUB

Users of GRUB can use either systemd's **kernel-install** or the traditional Debian **installkernel**. The [systemd](https://packages.gentoo.org/useflags/systemd)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag switches between these implementations. To automatically run **grub-mkconfig** when installing the kernel, enable the [grub](https://packages.gentoo.org/useflags/grub)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") [USE flag](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru").

ФАЙЛ **`/etc/portage/package.use/installkernel`**

```bash
sys-kernel/installkernel grub
```

```bash
emerge --ask sys-kernel/installkernel
```


#### Traditional layout, other bootloaders (e.g. lilo, etc.)

The traditional /boot layout (for e.g. LILO, etc.) is used by default if the [grub](https://packages.gentoo.org/useflags/grub)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru"), [systemd-boot](https://packages.gentoo.org/useflags/systemd-boot)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") and [uki](https://packages.gentoo.org/useflags/uki)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flags are **not** enabled. No further action is required.

### Building an initramfs

In certain cases it is necessary to build an [initramfs](https://wiki.gentoo.org/wiki/Initramfs "Initramfs") - an **i**nitial **ram**\-based **f**ile **s**ystem. The most common reason is when important file system locations (like /usr/ or /var/) are on separate partitions. With an initramfs, these partitions can be mounted using the tools available inside the initramfs. The default configuration of the [Project:Distribution Kernel](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel "Project:Distribution Kernel") requires an initramfs.

Without an initramfs, there is a risk that the system will not boot properly as the tools that are responsible for mounting the file systems require information that resides on unmounted file systems. An initramfs will pull in the necessary files into an archive which is used right after the kernel boots, but before the control is handed over to the init tool. Scripts on the initramfs will then make sure that the partitions are properly mounted before the system continues booting.

**Важно**  
If using genkernel, it should be used for both building the kernel _and_ the initramfs. When using genkernel only for generating an initramfs, it is crucial to pass `--kernel-config=/path/to/kernel.config` to genkernel or the generated initramfs **may not work** with a manually built kernel. Note that manually built kernels go beyond the scope of support for the handbook. See the [kernel configuration](https://wiki.gentoo.org/wiki/Kernel/Configuration/ru "Kernel/Configuration/ru") article for more information.

[Installkernel](https://wiki.gentoo.org/wiki/Installkernel "Installkernel") can automatically generate an initramfs when installing the kernel if the [dracut](https://packages.gentoo.org/useflags/dracut)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag is enabled:

ФАЙЛ **`/etc/portage/package.use/installkernel`**

```bash
sys-kernel/installkernel dracut
```

Alternatively, dracut may be called manually to generate an initramfs. Install [sys-kernel/dracut](https://packages.gentoo.org/packages/sys-kernel/dracut) first, then have it generate an initramfs:
```bash
emerge --ask sys-kernel/dracut
dracut --kver=6.6.21-gentoo
```
The initramfs will be stored in **/boot/**. The resulting file can be found by simply listing the files starting with _initramfs_:
```bash
ls /boot/initramfs*
```
### Optional: Building an Unified Kernel Image

An [Unified Kernel Image](https://wiki.gentoo.org/wiki/Unified_Kernel_Image "Unified Kernel Image") (UKI) combines, among other things, the kernel, the initramfs and the kernel command line into a single executable. Since the kernel command line is embedded into the unified kernel image it should be specified before generating the unified kernel image (see below). Note that any kernel command line arguments supplied by the bootloader or firmware at boot are ignored when booting with secure boot enabled.

An unified kernel image requires a stub loader, currently the only one available is **systemd-stub**. To enable it:

For systemd systems:

ФАЙЛ **`/etc/portage/package.use/systemd`**

For OpenRC systems:

ФАЙЛ **`/etc/portage/package.use/systemd-utils`**

```bash
sys-apps/systemd-utils boot
```

[Installkernel](https://wiki.gentoo.org/wiki/Installkernel "Installkernel") can automatically generate an unified kernel image using either dracut or ukify, by enabling the respective flag. The [uki](https://packages.gentoo.org/useflags/uki)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag should be enabled as well to install the generated unified kernel image to the **$ESP/EFI/Linux** directory on the [EFI system partition](https://wiki.gentoo.org/wiki/EFI_system_partition "EFI system partition") (ESP).

For dracut:

ФАЙЛ **`/etc/portage/package.use/installkernel`**

```bash
sys-kernel/installkernel dracut uki
```

ФАЙЛ **`/etc/dracut.conf`**

```bash
uefi="yes"
kernel_cmdline="some-kernel-command-line-arguments"
```

For ukify:

ФАЙЛ **`/etc/portage/package.use/installkernel`**

```bash
sys-kernel/installkernel dracut ukify uki
```

ФАЙЛ **`/etc/kernel/cmdline`**

```bash
some-kernel-command-line-arguments
```

Note that while dracut can generate both an initramfs and an unified kernel image, ukify can only generate the latter and therefore the initramfs must be generated separately with dracut.

#### Generic Unified Kernel Image

The prebuilt [sys-kernel/gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin) can optionally install a prebuilt generic unified kernel image containing a generic initramfs that is able to boot most systemd based systems. It can be installed by enabling the [generic-uki](https://packages.gentoo.org/useflags/generic-uki)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag, and configuring [installkernel](https://wiki.gentoo.org/wiki/Installkernel "Installkernel") to not generate a custom initramfs or unified kernel image:

ФАЙЛ **`/etc/portage/package.use/generic-uki`**

```bash
sys-kernel/gentoo-kernel-bin generic-uki
sys-kernel/installkernel -dracut -ukify uki
```

#### Secure Boot

The generic Unified Kernel Image optionally distributed by [sys-kernel/gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin) is already pre-signed. How to sign a locally generated unified kernel image depends on whether dracut or ukify is used. Note that the location of the key and certificate should be the same as the SECUREBOOT_SIGN_KEY and SECUREBOOT_SIGN_CERT as specified in **/etc/portage/make.conf**.

For dracut:

ФАЙЛ **`/etc/dracut.conf`**

```bash
uefi="yes"
kernel_cmdline="some-kernel-command-line-arguments"
uefi_secureboot_key="/path/to/kernel_key.pem"
uefi_secureboot_cert="/path/to/kernel_key.pem"
```

For ukify:

ФАЙЛ **`/etc/kernel/uki.conf`**

```bash
[UKI]
SecureBootPrivateKey=/path/to/kernel_key.pem
SecureBootCertificate=/path/to/kernel_key.pem
```

### Rebuilding external kernel modules

External kernel modules installed by other packages via `linux-mod-r1.eclass` must be rebuilt for each new kernel version. When the distribution kernels are used this may be automated by enabling the [dist-kernel](https://packages.gentoo.org/useflags/dist-kernel)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") flag globally.

ФАЙЛ **`/etc/portage/package.use/module-rebuild`**
```bash
*/* dist-kernel
```
External kernel modules may also be rebuilt manually with:
```bash
emerge --ask @module-rebuild
```

## Модули ядра

### Список доступных модулей ядра

**Заметка**  
Модули оборудования не обязательно указывать вручную. В большинстве случаев, udev автоматически загрузит все необходимые модуля для обнаруженных устройств. Однако, не будет никакого вреда, если добавить автоматически загружаемые модули в список. Модули не могут быть загружены дважды; они либо загружаются, либо выгружаются. Иногда очень специфическим устройствам необходима помощь, чтобы загрузить их драйвера.

Модули, которые должны загружаться при каждой загрузке, могут быть добавлены в файлы /etc/modules-load.d/\*.conf, по одному модулю в строке. Если для модулей необходимы дополнительные параметры, их следует указывать в файлах /etc/modprobe.d/\*.conf.

Чтобы просмотреть все модули, доступные для определённой версии ядра, выполните следующую команду find. Не забудьте заменить **kernel version** на соответствующую версию ядра для поиска:
```bash
find /lib/modules/<kernel version>/ -type f -iname '*.o' -or -iname '*.ko' | less
```
### Принудительная загрузка отдельных модулей ядра

Чтобы принудительно загрузить в систему модуль **3c59x.ko** (драйвер для определённого семейства сетевых карт от 3Com), отредактируйте файл **/etc/modules-load.d/network.conf** и добавьте туда имя модуля.
```bash
mkdir -p /etc/modules-load.d
nano -w /etc/modules-load.d/network.conf
```

Обратите внимание, что суффикс в имени файла модуля .ko несущественен для механизма загрузки и не включается в файл:

ФАЙЛ **`/etc/modules-load.d/network.conf` Принудительная загрузка модуля 3c59x**
```bash
3c59x
```

Продолжите установку с раздела [Настройка системы](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/System/ru "Handbook:AMD64/Installation/System/ru").

#Gentoo 
#Linux 
#Kernel 
#WikiGentoo