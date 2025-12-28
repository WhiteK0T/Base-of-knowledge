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
