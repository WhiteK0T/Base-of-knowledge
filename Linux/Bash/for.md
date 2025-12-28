---
создал заметку: 2025-12-20T21:40:00
author: WhiteK0T
tags:
  - Bash
  - for
Источник:
  - https://t.me/bashdays/553
---
Я тут решил протестировать циклы for и поделиться результатами.
```bash
for ((i = 0 ; i < 100 ; i++)); do
    echo $i
done
```
Годный цикл. Главное логичный и понятный.

```bash
for i in {1..3}; do
    echo $i
done

# или его расширенная версия с шагом

for i in {50..5..-5}; do
    echo $i
done
```
Возможно построение циклов с нарастанием и убыванием. Циклы не допускают подстановки переменных в параметры цикла!!! Чистый башизм. Не рекомендую.

```bash
for i in $(seq 1 10); do
    echo "Итерация: $i"
done

# С шагом 
for i in $(seq 1 2 10); do
    echo "Нечётные: $i" 
done
# 1 3 5 7 9 

# С параметрами 
START=3 
END=8 
for i in $(seq $START 1 $END); do 
    echo "Обработка $i" 
done
```
sec позволяет использовать переменные

```bash
IFS=$'\n'
for i in $(cat /etc/passwd); do
    echo $i
done
```
Годный цикл для построчного чтения файла, но нужно помнить про разделитель IFS.

```bash
for i in "./space test/"*; do
    echo $i
done
```
Годный цикл для перебора файлов, обратите внимание путь в кавычках, а звездочка - нет.

```bash
for i in 5 9 8 3;do
  echo $i
done
```
Годный цикл с перечислятельством, для не очень больших количеств.

```bash
echo 1 2 3|for i in $(</dev/stdin);do
  echo $i
done
```
Если цикл не работает - верните IFS=" "


Тройка упоротых конструкций:
```bash
for ((a=0,b=9;a<10;a++,b--));do
   echo $a,$b
done

for ((a=1;a<2000;a+=a));do
  echo $a
done

for i in $(j=10;while ((j--));do echo $j;done);do
   echo $i
done
```

#Bash 
#for 