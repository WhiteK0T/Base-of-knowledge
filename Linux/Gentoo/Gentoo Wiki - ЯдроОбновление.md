---
создал заметку: 2024-04-25T22:55:00
tags:
  - WikiGentoo
  - Gentoo
  - Kernel
  - Linux
Источник: https://wiki.gentoo.org/wiki/Kernel/Upgrade/ru
---
Эта статья описывает шаги необходимые для обновления [ядра](https://wiki.gentoo.org/wiki/Kernel/ru "Kernel/ru") Linux.

Сборка нового ядра из свежего исходного кода является практически тем же процессом, как и во время установки системы. Разница заключается в том, что для экономии времени можно конвертировать конфигурацию от старого ядра под изменения, сделанные в новом ядре, вместо того, чтобы снова устанавливать все опции (например, с помощью **make menuconfig**).

В новом ядре могут быть опции или возможности, которых нет в старом ядро, или наоборот, из нового ядра могут быть убраны некоторые из опций, которые были в старом ядре. Поэтому в конфигурационном файле нового ядра могут быть новые опции, которые отсутствуют в конфигурационном файле старого ядра, или некоторых опций больше нет в новом ядре, но они присутствовали в конфигурационном файле старого ядра.

Эта статья демонстрирует, как обращаться с такими изменениями файла конфигурации путём конвертации старой конфигурации в конфигурацию, пригодную для нового ядра.

Обновления ядра в Gentoo включает следующие шаги:

1.  Установка нового исходного кода ядра.
2.  Установка символьной ссылки на (недавно установленный) исходный код ядра.
3.  Вход в каталог с новым ядром.
4.  Настройка файла **.config** для параметров, которые были удалены или добавлены в конфигурацию нового ядра.
5.  Сборка ядра и initramfs.
6.  Обновление загрузчика.
7.  Удаление или сохранение старого ядра.

**Важно**  
Разумно будет сделать резервную копию конфигурации ядра, чтобы не потерять предыдущую конфигурацию. Многие пользователи потратили много времени на поиск оптимальной конфигурации системы, и терять эту информацию им точно не хочется. Для создания такой резервной копии вы можете использовать один из способов в [разделе про копирование предыдущей конфигурации ядра](https://wiki.gentoo.org/wiki/Kernel/Upgrade/ru#Copy_the_previous_kernel_configuration "Kernel/Upgrade/ru").

## Установка нового исходного кода ядра

Для обновление ядра в начале нужно установить новый исходный код ядра. Этот исходный код иногда устанавливается в результате обновления системы при запуске следующей команды:
```bash
emerge --ask --update --deep --with-bdeps=y --newuse @world
```
Конечно, исходный код ядра можно установить напрямую, используя команду (замените _gentoo-sources_ на любую версию ядра, которую используете):
```bash
emerge --ask --update --deep --with-bdeps=y --newuse sys-kernel/gentoo-sources
```
Установка нового исходного кода ядра не дает пользователю обновленное ядро. Новый исходный код нужно собрать в новое ядро и установить, а затем перезапустить систему.

## Установка символьной ссылки на новый исходный код ядра

Конфигурация ядра сохранена в файле **.config**, в каталоге с исходным кодом ядра.

Символьная ссылка **/usr/src/linux** должна всегда указывать на каталог, в котором находится исходный код используемого в настоящий момент ядра. Это может быть сделано одним из трех способов:

1.  По умолчанию: Настройка ссылки с помощью eselect
2.  Альтернатива 1: Ручное обновление символьной ссылки
3.  Альтернатива 2: Установка исходного кода ядра с `USE="symlink"`

### По умолчанию: Настройка символьной ссылки с помощью eselect

Для настройки символьной ссылки с помощью **eselect**:
```bash
eselect kernel list

Available kernel symlink targets:
 [1] linux-3.14.14-gentoo *
 [2] linux-3.16.3-gentoo
```
Это вывод доступных исходных кодов ядра. Звездочка указывает на выбранный исходный код.

Для выбора исходного кода ядра, например, второго в списке, выполните:
```bash
eselect kernel set 2
```
### Альтернатива 1: Изменение символьной ссылки вручную

Для изменения символьной ссылки вручную:
```bash
ln -sf /usr/src/linux-3.16.3-gentoo /usr/src/linux
```

```bash
ls -l /usr/src/linux
  lrwxrwxrwx 1 root root 19 Oct  4 10:21 /usr/src/linux -> linux-3.16.3-gentoo
```

### Альтернатива 2: Установка исходного кода ядра с **USE**-флагом **symlink**

Это заставит **/usr/src/linux** ссылаться на с веже установленный исходный код ядра.

Если необходимо, это можно изменить одним из двух методов.

## Переход в каталог с новым ядром

После того, как была изменена символьная ссылка, смените рабочую директорию на каталог с новым ядром.
```bash
cd /usr/src/linux
```
**Заметка**  
Эта команда необходима, даже если вы уже находились в каталоге **/usr/src/linux**, когда изменялась символьная ссылка. Пока вы не пере зайдете в каталог, консоль всё ещё будет в каталоге _старого_ ядра.

## Конвертация файла .config для нового ядра

### Копирование предыдущей конфигурации ядра

Конфигурацию от старого ядра необходимо скопировать в каталог с новым. Старую конфигурацию можно найти в нескольких местах:

-   В файловой системе [procfs](https://wiki.gentoo.org/wiki/Procfs/ru "Procfs/ru"), если параметр ядра _Enable access to .config through /proc/config.gz_ был включен в работающем на данный момент ядре:
```bash
zcat /proc/config.gz > /usr/src/linux/.config
```
-   Из старого ядра. Такое будет работать только в случае, если старое ядро было собрано с **CONFIG_IKCONFIG**:
```bash
/usr/src/linux/scripts/extract-ikconfig /path/to/old/kernel >/usr/src/linux/.config`
```
-   В каталоге **/boot**, если туда был установлен конфигурационный файл:
```bash
cp /boot/config-3.14.14-gentoo /usr/src/linux/.config
```
-   В каталоге ядра, которое работает на данный момент:
```bash
cp /usr/src/linux-3.14.14-gentoo/.config /usr/src/linux/
```
-   В каталоге **/etc/kernels/**, если **`SAVE_CONFIG="yes"`** настроено в **/etc/genkernel.conf** и ядро было собрано с помощью [genkernel](https://wiki.gentoo.org/wiki/Genkernel/ru "Genkernel/ru"):
```bash
cp /etc/kernels/kernel-config-x86_64-3.14.14-gentoo /usr/src/linux/.config
```
### Обновление файла **.config**

**Заметка**  
Команды **make oldconfig** и **make menuconfig** могут вызываться автоматически с помощью [genkernel](https://wiki.gentoo.org/wiki/Genkernel/ru "Genkernel/ru") во время сборки, если вы включите параметры _OLDCONFIG_ и _MENUCONFIG_ в файле **/etc/genkernel.conf**. Если вы включили параметр _OLDCONFIG_ в конфигурации genkernel или с помощью параметра _\--oldconfig_ команды **genkernel**, перейдите к разделу с [сборкой](https://wiki.gentoo.org/wiki/Kernel/Upgrade/ru#Build "Kernel/Upgrade/ru").

Новое ядро обычно требует новый файл .config для поддержки новых опций ядра. Файл .config с предыдущего ядра может быть с конвертирован для использования новым ядром. Конвертация может быть выполнена несколькими способами, например, с помощью команд **make oldconfig** или **make olddefconfig.**

#### make oldconfig

**Важно**  
**make syncconfig** стал частью внутреннего устройства; по возможности используйте **make oldconfig**. **make silentoldconfig** был удален, начиная с ядра Linux версии 4.19.

Следующая конфигурация похожа на текстовый интерфейс из **make config**. Для новых опций она предоставляет выбор пользователю. Например:
```bash
cd /usr/src/linux
make oldconfig
Anticipatory I/O scheduler (IOSCHED_AS) [Y/n/m/?] (NEW)
```

Надпись _(NEW)_ в конце строки означает, что это новая опция. В левой части, в квадратных скобках, указаны возможные ответы: _Yes, _no, _module или ?_ для справки. Рекомендуемый ответ (т.е. по умолчанию) написан большими буквами (здесь _Y_). В справке дано пояснение к опции или драйверу.

К сожалению, **make oldconfig** не дает исчерпывающей информации для каждой опции, так что иногда трудно выбрать правильный ответ. В этом случае, лучше запомнить название параметра и найти его позже с помощью одного из [инструментов конфигурации ядра](https://wiki.gentoo.org/wiki/Kernel/Configuration/ru#Configuration_tools "Kernel/Configuration/ru"). Для просмотра списка новых опций, используйте **make listnewconfig** перед **make oldconfig**.

#### make olddefconfig

make olddefconfig оставит все настройки с старого файла **.config**, и установит новые настройки в их рекомендуемое значение (т.е. в значение по умолчанию):
```bash
cd /usr/src/linux
make olddefconfig
```
#### make help

Используйте **make help** для просмотра других доступных методов преобразования конфиг файла:
```bash
make help
```
#### Наблюдение различий

Инструмент **diff** может быть использован для сравнения старого и нового файла **.config**, чтобы просмотреть вновь добавленные опции:
```bash
comm -2 -3 <(sort .config) <(sort .config.old)`
```
И какие были удалены:
```bash
comm -1 -3 <(sort .config) <(sort .config.old)
```
Так же, ядро предоставляет скрипт для точного сравнения двух файлов, даже, если опции уже были добавлены в файл:
```bash
/usr/src/linux/scripts/diffconfig .config.old .config
```
После этого опции могут быть изучены и изменены при необходимости командой:
```bash
make menuconfig
```
Цель menuconfig полезна тем, что она безопасно управляет зависимостями опций от других опций.
## Сборка

### Ручная сборка и установка

Having configured the new kernel as described in the previous sections, if external kernel modules are installed (like _nvidia_ or _zfs_), it may be necessary to prepare them before building the new kernel, and then to rebuild the modules with the newly built kernel:
```bash
make modules_prepare
make
emerge --ask @module-rebuild
```

**Заметка**  
Using the `-jN` option with `make` (where `N` is the number of parallel jobs) can speed up the compilation process on multi-threaded systems. For example, `make -j5` on a system with four logical cores.

Having built both the kernel and the modules, both should be installed:
```bash
make modules_install
make install
```
Finally, the bootloader must be reconfigured to account for the new kernel filenames, as described [below](https://wiki.gentoo.org/wiki/Kernel/Upgrade/ru#Update_the_bootloader "Kernel/Upgrade/ru"). initramfs must be rebuilt if one is used as well.
### Автоматическая сборка и установка

It is possible to automatically build and install the newly emerged kernel using Portage hooks. While other approaches are also possible, the following is based on genkernel and gentoo-sources package. It requires the following prerequisites:

1.  **genkernel all** is able to build and install the kernel to which the **/usr/src/linux symlink** points into `$BOOTDIR` and the bootloader.
2.  The `symlink` use flag is set for the kernel ebuild.

If those are fulfilled, simply install a `post_pkg_postinst` Portage hook as shown below. Keep in mind this calls genkernel with --`no-module-rebuild`, since using module-rebuild would run emerge in emerge, and result in a deadlock waiting on the lock file. Remember to run `emerge @module-rebuild` after any update that includes a kernel upgrade.

ФАЙЛ **`/etc/portage/env/sys-kernel/gentoo-sources` Automated kernel build and installation portage hook**

```bash
post_pkg_postinst() {
# Eselect the new kernel or genkernel will build the current one
	eselect kernel set linux-"${KV}"
	CURRENT_KV=$(uname -r)
# Check if genkernel has been run previously for the running kernel and use that config
	if [[ -f "${EROOT}/etc/kernels/kernel-config-${CURRENT_KV}" ]] ; then
		genkernel --no-module-rebuild --kernel-config="${EROOT}/etc/kernels/kernel-config-${CURRENT_KV}" all
# Use latest kernel config from current kernel
	elif [[ -f "${EROOT}/usr/src/linux-${CURRENT_KV}/.config" ]] ; then
		genkernel --no-module-rebuild --kernel-config="${EROOT}/usr/src/linux-${CURRENT_KV}/.config" all
# Use known running good kernel
	elif [[ -f /proc/config.gz ]] ; then
		zcat /proc/config.gz >> "${EROOT}/tmp/genkernel.config"
		genkernel --no-module-rebuild --kernel-config="${EROOT}/tmp/genkernel.config" all
		rm "${EROOT}/tmp/genkernel.config"
# No valid configs known, compile a clean one
	else
		genkernel --no-module-rebuild all
	fi
}
```
### Решение проблем сборки

Если возникают проблемы при пере сборке текущего ядра, то может помочь очистка исходного кода ядра. Удостоверьтесь, что сохранили файл .config, так как данная операция удалит его. Удостоверьтесь, что не используется окончание файла .bak или ~ для бэкапа, так как **make distclean** очищает и такие файлы.
```bash
cp .config /usr/src/kernel_config_bk
make distclean
mv /usr/src/kernel_config_bk .config
```
## Обновление загрузчика

The upgraded and installed kernel must be registered with the [bootloader](https://wiki.gentoo.org/wiki/Bootloader/ru "Bootloader/ru") or [directly with the UEFI firmware](https://wiki.gentoo.org/wiki/EFI_stub_kernel#Installation "EFI stub kernel"), see [Kernel/Configuration](https://wiki.gentoo.org/wiki/Kernel/Configuration/ru#Setup "Kernel/Configuration/ru"). Users of [GRUB](https://wiki.gentoo.org/wiki/GRUB/ru "GRUB/ru") can use the method below, users of other bootloaders must consult the [Handbook](https://wiki.gentoo.org/wiki/Handbook "Handbook").

Make sure **/boot** partition is mounted.

### Использование grub-mkconfig

The following command can be executed for updating [GRUB](https://wiki.gentoo.org/wiki/GRUB/ru "GRUB/ru")'s configuration file:
```bash
grub-mkconfig -o /boot/grub/grub.cfg
```
**Предупреждение**  
If GRUB itself was upgraded (besides the kernel), for instance as part of a world set upgrade, it is necessary to also re-install GRUB, otherwise it may not boot. See [GRUB#GRUB Bootloader Installation](https://wiki.gentoo.org/wiki/GRUB#GRUB_Bootloader_Installation "GRUB") for details.

**Совет**  
By enabling the [grub](https://packages.gentoo.org/useflags/grub)[](https://wiki.gentoo.org/wiki/USE_flag/ru "USE flag/ru") USE flag on [sys-kernel/installkernel](https://packages.gentoo.org/packages/sys-kernel/installkernel) grub-mkconfig will be regenerated automatically every time a new kernel is installed.

### Systemd-boot

A [systemd-boot](https://wiki.gentoo.org/wiki/Systemd-boot "Systemd-boot") configuration file for the new kernel is generated automatically when the kernel is installed. No manual action is required.

### Удаление старого ядра

Смотрите статью [Удаление ядра](https://wiki.gentoo.org/wiki/Kernel/Removal/ru "Kernel/Removal/ru").

## Смотрите также

-   [Genkernel](https://wiki.gentoo.org/wiki/Genkernel/ru "Genkernel/ru") — утилита созданная Gentoo, которая используется для автоматизации процесса сборки [ядра](https://wiki.gentoo.org/wiki/Kernel/ru "Kernel/ru") и [initramfs](https://wiki.gentoo.org/wiki/Initramfs "Initramfs").
-   [Dracut](https://wiki.gentoo.org/wiki/Dracut "Dracut") — an [initramfs](https://wiki.gentoo.org/wiki/Initramfs "Initramfs") infrastructure and aims to have as little as possible hard-coded into the initramfs.
-   [Kernel/Configuration](https://wiki.gentoo.org/wiki/Kernel/Configuration/ru "Kernel/Configuration/ru") — описывает ручную конфигурацию и настройку [ядра Linux](https://wiki.gentoo.org/wiki/Kernel/ru "Kernel/ru").
-   [Обновление GRUB на новое ядро](https://wiki.gentoo.org/wiki/GRUB/ru#Installing_a_new_kernel "GRUB/ru")

## Внешние ресурсы

-   [Журнал изменений ядра с разьяснениями некоторых новых возможностей](http://kernelnewbies.org/LinuxChanges)

#Gentoo 
#Linux 
#Kernel 
#WikiGentoo