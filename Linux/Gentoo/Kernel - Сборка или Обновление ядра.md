---
создал заметку: 2024-04-25T14:07:00
author: WhiteK0T
---
### Сборка ядра Gentoo

#### Установка символьной ссылки на новый исходный код ядра
```bash
eselect kernel list
eselect kernel set 1-9

cd /usr/src/linux
```
#### Копирование предыдущей конфигурации ядра
```bash
cp /usr/src/linux-5.15.80-gentoo/.config /usr/src/linux/
```
#### Конфигурация ядра
Обзор изменений между версиями ядра, а так же обновление их для создания нового .config для ядра.
```bash
make oldconfig
```
Создаёт новый конфигурационный файл с настройками по умолчанию, которые берутся из архитектурно-зависимых defconfig файлов, сохраняя при этом все предыдущие опции, установленные в файле .config по пути /usr/src/linux/.config. 
Это быстрый и безопасный метод обновления конфигурации (в которой уже есть все параметры, необходимые для поддержки оборудования) для того, чтобы получить исправления ошибок и патчи безопасности.
```bash
make defconfig
```
Конфигурация с текстовым интерфейсом. Вопросы следуют один за другим. На все вопросы должен быть дан ответ по порядку. Доступ к предыдущим вопросам невозможен.
```bash
make menuconfig
```
Конфигурация с текстовым интерфейсом.
```bash
make olddefconfig
```
**make olddefconfig** оставит все настройки с старого файла .config, и установит новые настройки в их рекомендуемое значение (то есть в значение по умолчанию)
```bash
make xconfig
```
Конфигуратор с графическим интерфейсом, основанный на Qt5. Должен быть установлен пакет [dev-qt/qtwidgets](https://packages.gentoo.org/packages/dev-qt/qtwidgets)|
```bash
make gconfig
```
Конфигуратор с графическим интерфейсом, основанный на GTK. Должны быть установлены пакеты [x11-libs/gtk+](https://packages.gentoo.org/packages/x11-libs/gtk+), [dev-libs/glib](https://packages.gentoo.org/packages/dev-libs/glib) и [gnome-base/libglade](https://packages.gentoo.org/packages/gnome-base/libglade)
#### Под монтируем boot 
```bash
mount /boot/efi
```
#### Сборка и компиляция ядра и модулей
```bash
make modules_prepare
emerge --ask @module-rebuild
make -j9 && make modules_install
make install

```
#### Поправим config Grub
```bash
grub-mkconfig -o /boot/efi/grub/grub.cfg
```

При включении USE флага **grub** в sys-kernel/installkernel **grub-mkconfig** будет автоматически обновляться при каждой установке нового ядра.
#### Решение проблем сборки
Если возникают проблемы при пере сборке текущего ядра, то может помочь очистка исходного кода ядра. Удостоверьтесь, что сохранили файл .config, так как данная операция удалит его. Удостоверьтесь, что не используется окончание файла .bak или ~ для бэкапа, так как make distclean очищает и такие файлы.
```bash
cp .config /usr/src/kernel_config_bk
make distclean
mv /usr/src/kernel_config_bk .config
```
### Установка или удаление новой версии ядра
#### Установка нового исходного кода ядра
Для обновления ядра в начале нужно установить новый исходный код ядра. Этот исходный код иногда устанавливается в результате обновления системы при запуске следующей команды:
```bash
emerge --ask --update --deep --with-bdeps=y --newuse @world
```
Конечно, исходный код ядра можно установить напрямую, используя команду (замените gentoo-sources на любую версию ядра, которую используете):
```bash
emerge --ask --update --deep --with-bdeps=y --newuse sys-kernel/gentoo-sources:5.15.122
```
#### Удаление исходного кода ядра

```bash
emerge --ask --depclean gentoo-sources:5.15.122
```

#### Удаление остатков ядра
##### Ручное удаление
Portage, однако, удаляет только те файлы, которые он установил - файлы, созданные во время сборки ядра и установки остаются. Они могут быть безопасно удалены.

- После сборки ядра, файлы созданные во время компиляции остаются и не удаляются Portage:
```bash
rm -r /usr/src/linux-3.X.Y
```
- Во время установки ядра, модули ядра с копируются в подкаталоги /lib/modules/:
```bash
rm -r /lib/modules/3.X.Y
```
- Старые файлы в /boot также могут быть удалены:
```bash
rm /boot/vmlinuz-3.X.Y
rm /boot/System.map-3.X.Y
rm /boot/config-3.X.Y
rm /boot/initramfs-X.Y.Z
```
- И наконец, удалите все оставшиеся записи из файла конфигурации вашего загрузчика.
##### Использование eclean-kernel
[app-admin/eclean-kernel](https://packages.gentoo.org/packages/app-admin/eclean-kernel) это простая программа для очистки/удаления старого ядра. Она удаляет сборочные файлы и каталоги ядра, если на них не ссылается никакое сохраненное ядро.

Смотрите **eclean-kernel --help** после установки для получения инструкций по использованию.

Например, чтобы сохранить три последних ядра:
```bash
eclean-kernel -n 3
```
### Работа со списком не удаляемых пакетов
#### Добавление ядра в список не удаляемых
```bash
emerge --noreplace sys-kernel/gentoo-sources:5.15.122
```
#### Удаление ядра из списка не удаляемых
```bash
emerge --deselect sys-kernel/gentoo-sources:здесь.ненужная.версия
```
#### Просмотр списка не удаляемых ядер 
Чтобы узнать, какое ядро добавлено в список не удаляемых в Gentoo, вы можете воспользоваться командой `equery`.
```bash
equery list sys-kernel/gentoo-sources
```
### Сравнение текущей конфигурации ядра с конфигурацией по умолчанию

Используйте следующую процедуру, чтобы получить список конфигураций ядра, которые отличаются от значений по умолчанию.
Имейте ввиду, что модификация одних параметров настроек может повлечь за собой изменение других параметров настроек.
```bash
cd /usr/src/linux
cp -p .config ../.config.working
make defconfig
mv .config ../.config.default
cp -p ../.config.working .config
cd ..
/usr/src/linux/scripts/diffconfig .config.working .config.default > .config.diff
```
Функцию поиска из make menuconfig можно использовать для поиска обозначения (symbols) и их описание. Когда вы закончите 
очистите:
```bash
cd /usr/src/
rm .config.working .config.default .config.diff
```

#Gentoo 
#Linux 
#Kernel
#CheatSheet