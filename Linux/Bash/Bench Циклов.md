---
создал заметку: 2025-12-28T22:06:00
author: WhiteK0T
tags:
  - Bench
  - for
  - while
  - Bash
Источник:
  - https://t.me/bashdays/561
---
> [! ]
> - Ты такой душный...
> - Не могли бы вы поподробнее разъяснить мне, в чём конкретно это выражается?

Сегодня будем собирать пенки на кабачковой икре и протестируем несколько циклов.

Скрипт для тестирования циклов. Каждый цикл выводит два числа.

Первое - число секунд от начала цикла до вывода первого значения.

Второе - число секунд длительности цикла.

Если решите перетестировать у себя - обратите внимание, что в циклах FOR0 и GAWK число итераций прописаны константами.

В остальных - через переменную MAX. Меняйте синхронно. Выводы будут в конце. Рекомендую рассмотреть код.

Может найдете для себя что-то новое. Да, у некоторых циклов обратный порядок. Это для случаев, когда переменная цикла не используется, а важно количество итераций.

```bash
#!/bin/bash
declare -i MAX=5000000
declare -i MA1=MAX+1
declare -i Z0=0
declare -i Z1=1
declare -i P
declare LOG=./log.txt
declare LOOPNAME

clear
LOOPNAME=FOR0
P=0
SECONDS=0
for i in {1..5000000};do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

LOOPNAME=FOR1
P=0
SECONDS=0
for i in $(seq $Z1 $MAX);do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

LOOPNAME=FOR2
P=0
SECONDS=0
seq $Z1 $MAX|for i in $(</dev/stdin);do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

LOOPNAME=FOR3
P=0
SECONDS=0
for ((i=$Z0;i++<$MAX;));do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

LOOPNAME=FOR4
P=0
SECONDS=0
for ((i=$MAX;i--!=0;));do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

LOOPNAME=FOR5
P=0
SECONDS=0
for ((i=$Z1;i<$MA1;i++));do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

LOOPNAME=WHL0
P=0
i=$Z0
SECONDS=0
while ((i++<$MAX));do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

LOOPNAME=WHL1
P=0
i=$MAX
SECONDS=0
while ((i--));do
  if [[ $P -eq 0 ]];then
    echo $LOOPNAME $SECONDS
    P=1
  fi
done
echo $LOOPNAME $SECONDS

gawk 'BEGIN{p=0
  for(i = 1;i < 5000000;i++){
    if(p==0)
     print "GAWK 0";p++}
  }'

gawk 'BEGIN{t=systime();p=0
  for(i = 1;i < 5000000;i++){
    if(p==0){
      print "GAWK " systime()-t;p++}
  }
print "GAWK "systime()-t}'
```


> [!AMD E1-6010 6Gb Swap 0] AMD E1-6010 6Gb Swap 0
> FOR0 14
> FOR0 76
> FOR1 11
> FOR1 72
> FOR2 10
> FOR2 53
> FOR3 0
> FOR3 97
> FOR5 0
> FOR5 103
> WHL0 0
> WHL0 100
> WHL1 0
> WHL1 78

--- Я немного отделил, поскольку gawk не совсем bash, но привел для примера.


> [! ] 
> GAWK 0
> GAWK 2 (тут реально 1.6) но баш оперирует целыми.


> [!Intel i3 10100 16Gb Win10 WSL] Intel i3 10100 16Gb Win10 WSL
> FOR0 3
> FOR0 31
> FOR1 4
> FOR1 29
> FOR2 5
> FOR2 10
> FOR3 0
> FOR3 31
> FOR4 0
> FOR4 30
> FOR5 0
> FOR5 31
> WHL0 0
> WHL0 30
> WHL1 0
> WHL1 29
> GAWK 0
> GAWK 0
> GAWK 0

Выводы:

1. Самый быстрый - FOR2  for in (seq)

2. Самый медленный - FOR5 (сишный классический)

3. Несмотря на небольшие разницы в скорости выполнения скорость циклов соизмерима.

4. Циклы for in - ВНАЧАЛЕ получают полный список значений (в памяти) потом быстро его перебирают.

4.1 Эти циклы жрут больше памяти, в случае нахватки - может быть критическая потеря производительности при использовании swap.

4.2 У этих циклов может быть большая задержка на инициализацию цикла. Это может быть критичным - если сам цикл большой, но очень часто происходит прерывание цикла в самом начале.

5. awk (а gawk самый медленный awk) значительно быстрее bash. Если скорость в приоритете - используйте его.

6. Цикл FOR0 вообще нежелательно применять, постокольку пределы цикла и инкремент нельзя задать переменными. только константы. Но сам конструкт {1..5} применять можно и даже нужно в подстановках (но не циклах). Например: ls text{9..27}.txt.

7. Главное помнить, что скорость выполнения определяется не скоростью самого цикла, а оптимизацией его тела.

#Bash 
#Bench 
#for 
#while 