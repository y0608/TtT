# Project for HackTUES Infinity
![header2b](https://user-images.githubusercontent.com/54147006/158683996-cc4a2001-8cb8-4dcb-bdc1-2deac70e14f8.png)
<br/>

Нашият проект цели лесна комуникация в космоса между космонавти, говорещи различни езици.
<br/>

## TtT pager - Space communication system

Когато пътуването в космоса стане по-достъпно, все по-голям брой хора от най-различни страни ще се запътят към космоса. Тук идва и проблемът за **езиковата бариера**, която Нашият проект TtT pager превъзмогва.<br/>
TtT pager представлява N на брой устройства - пейджъри, които всеки космонавт носи със себе си и един главен сървър, който се използва за обработване и превеждане на информацията. <br/>
 
### Тема:
![spho](https://user-images.githubusercontent.com/54147006/158684791-c95f0bd4-3810-4b0c-aede-064bcec634b1.png)

🟣 Да се разработи решение, подпомагащо живота на хората в Международната космическа станция (МКС).
<br/>

### Функционалност
Основната функционалност на пейджърите, която ги прави толкова уникални и използваеми е, че космонавтите ще могат **директно да комуникират един с друг**, без да е нужно да знаят езикът на другия и **без да им е нужен интернет** за превод(все пак в космоса няма интернет 😁). Пейджърите са **малки и компактни**, за да могат да се приложат на ръката на даден космонавт, те също така имат и екранче, което да визуализира съобщенията.  <br/><br/>

### Архитектура
#### - Комуникация
Комуникацията става чрез използването на главния сървър. Сървърът получава информация от един пейджър, преработва(превежда) я и я изпраща на пейджъра, за когото е предназначена.

#### - Главен сървър
#### - Пейджър

#### - Локална мрежа
Цялата комуникация се осъществява в **локална мрежа**. 
Предимства на използването на локална мрежа са:която няма нужда от достъп до интернет, премахва необходимостта от криптиране на данните и по време на авария не е нужно да се декриптира, което подобрява сигурността на космонавите в космоса.
В локалната мрежа е свързан един главен сървър и много пейджъри.
<br/>
![Untitled design](https://user-images.githubusercontent.com/54147006/158655021-d36ad44d-6dbd-4ca5-adee-4d3a07409b1b.jpg)
<br/>



Има два скрипта, единият е при всеки пейджър(човек), а другият при (Big)” мама”, която е сървър и приема и препраща информация и я превежда. Първото съобщение от всеки пейджър е init съобщение, което го добавя в архива на сървъра, всичко следващо съобщение, съдържа 4 компонента: име от кого, за кого, език, на който е съобщението и самото съобщение
За да се изпрати съобщение се използва json файл, използваме ги, защото те улесняват препращането на структура от данни.
Ние искаме всеки пейджър освен да изпраща и да получава, затова са два отделни процеса: единият слуша сървъра, а другият изпраща, за да се свържем към сървъра ние посочваме частна ip адреса на сървъра и показваме на кой порт искаме да изпращаме информацията и функциите, които използваме в пейджъра са : receive message, send message, send init message. 
-Receive message е да чака дали сървъра праща нещо, ако получи съобщение от сървъра и го показва на човека.
- Send message, чака потребителя да въведе съобщение и ще го в генерира json, които го изпраща на ”мамата”.
 -Send init message изпраща различен json, които показва, че има нов пейджър свързал се към системата, за да можем  да слушаме какво праща сървъра, и да пращаме към сървъра използваме два различни thread-a, два процеса, които са независят един от друг.
Идеята на сървъра(Big „мама”) е винаги да слуш!
а за идващо съобщение от пейджър към друг (насочен)  пейджър.

Слушането е отделен процес, по този начин сървъра ни може да обработи неограничен брой пейджъри.
Когато сървърът получи съобщение от пейджъра, преди да изпратим съобщение, то минава през „транслате”(превеждащата) функцията. Той създава съобщение с json формат и го изпраща на получателя. 
За реализиране на този скрипт използваме функциите, make server, multi threaded client, send message, save init message и translate message.
-Make server е функция, която създава връзка за всеки свързал се със сървъра пейджър посредством създаване на нов процес (треад(thread)).
-Send message получава  json и клиент използвайки json генериращ  съобщения, които искаме да изпратим, проверяваме пейджъра, дали съществува..

### Технологии
MCU-to ще бъде с микро Python, а Raspberry си е с Python

### Части
- 2x ESP 32; 
- 1x Raspberry pi 400(клавиатурата) 
- LSD екран PC1602A и е свързан в схема SPI
- Keypad свързан към ESPтата. Keypad-ът е свързан в схема UARD. Той е с цифри, които образуват букви, с които (идея за дисплей, като старите Nokia) да може да пишат изречения, a дисплея просто визуализира. 
- Батерия 2500 mAh и 3,7V и то ще обединява системата ТtТ пейджър с микро контролера ESPто

### В бъдеще
 - Ще има меню с опции, които ще се избират с джойстик.
 - Ще има speak to text и text to speach, но в бъдеще с части микрофон и speaker,  ама нямаме пари, 😭
 - Ще имат функционалност за водене на личен дневник на всеки един от космонавтите и отбелязване на забележки.
 - Ще работи точно като пейджър!!


### Инсталация
Модели нужни за argostranslate:
https://drive.google.com/drive/folders/1cIqOoBTIE0JV6LVrTgF-_7vFS1UtPZEJ?usp=sharing <br/>
За сървъра: big_mama.py <br/>
```python
pip install argostranslate
```
За пейджъра: pager.py <br/>
```python
pip intall socket, operator, json, threading, thread
```
### Библиотеки python
argostranslate
socket
operator
json
threading
thread
time <br/>


### Отбор
 - Живко
 - Митко
 - Георги
 - Йоан
 - Ради

### Версии
 - v1 - [HackTUES Infinity](https://github.com/y0608/TtT/releases/tag/HackTUES)


****************************************
Оригинална информация, която трябва да се добави към README <br/> 
Няма да е зле да се добавят и картинки<br/><br/>
Библиотеки и начин за инсталиране на превеждащата функцията pip3 install argostranslate 
За да работи трябва инсталиране и на модули (гоогл драйв)
N на брой пейджъри, които не говорят пряко един с друг, те общуват с едно raspberry pi, което е наречено „майка, която служи като сървър- получава, преработва (превежда) и предава информация в локална мрежа, недостъпна от други лица. Говорим хипотетично по-голяма космическа станция, в която може да има голям на брой космонавти, от най-различни страни. Тук идва проблемът за езиковата бариера, която пейджърите превъзмогват –  основната тяхна функционалност, която ги прави толкова уникални и използваеми е, че космонавтите  ще могат директно да комуникират един с друг, без да им трябва интернет за превод. Пейджърите са малки и компактни, за да могат да се приложат на ръката на даден астронавт, те също така имат и екранче (дисплей), което да визуализира съобщенията.  Те имат функционалност за водене на личен дневник на всеки един от космонавтите и отбелязване на забележки. 
Нашият проект представлява комуникацията в частна мрежа, която няма нужда до достъп в интернет. Това премахва необходимостта от криптиране на данните и подобрява сигурността на астронавтите в космоса по-време на авария.
(сега се замислям за черните магии на Митака, с които той се опитва да подкара хардуер частта на проекта, мъчи се и това за нас е наистина тъмна материя)
Indiana Mitko — 03/12/2022
obicham vi
jorh — 03/12/2022
Части използвани:
2 ESP 32ки; 1 Raspberry pi 400(клавиатурата) и LSD екран и Pad свързани към ESPтата(+ keypad).
Keypad-а е свързан в схема UARD, екрана е PC1602A и той е свързан в схема SPI.  Има батерия 2500 mAh и 3,7V и то ще обединява системата ТtТ пейджър с микро контролера ESPто (микро процесор ESP32)
MCU-to ще бъде с микро Python, а Raspberry с и е с Python
Keypad-а е с цифри, които образуват букви, с които (идея за дисплей, като старите Nokia) да може да пишат изречения, a дисплея просто визуализира. 
Ще има меню с опции, чрез което с джойстик ще се избират опции.
Ще има speak to text и text to speach, но в бъдеще с части микрофон и speaker,  ама нямаме пари, 😭
Ще работи точно като пейджър!!
jorh — 03/12/2022
Живко снощи е писал  комуникацията майка=пейджър, но на C, следователно едва ли ще го използваме)
Горе на космическата станция има wifi, но ние правим пейджъри, които да нямат нужда от интернет за да превеждат, защото библиотека е offline. 
Python 
1 библиотека от Github, позволява превод на текст offline, тъй като в нея има вградена невронна мрежа, няколко файла с данни от думи с големината  на файлове 1,5GB  за 10 езика.
Идеята е от един език се превежда към английски, а оттам към другия, за да се пести памет, от предавателя, знаем какъв език искаме да подадем и по тях превеждаме текста за получателя (до когото трябва да стигне).
 Комуникация между Discord и космонавтите.
 Реализация между пейджър и сървър на станцията като може да се изпраща лично съобщение до всеки един човек в мрежата, като първо се пише името му и после текста.
jorh — 03/12/2022
Dependency-тата (те са написани ама не знам дали трябва точно да се определят)
jorh — 03/12/2022
Има два скрипта, единият е при всеки пейджър(човек), а другият при (Big)” мама”, която е сървър и приема и препраща информация и я превежда. Първото съобщение от всеки пейджър е init съобщение, което го добавя в архива на сървъра, всичко следващо съобщение, съдържа 4 компонента: име от кого, за кого, език, на който е съобщението и самото съобщение
За да се изпрати съобщение се използва json файл, използваме ги, защото те улесняват препращането на структура от данни.
Ние искаме всеки пейджър освен да изпраща и да получава, затова са два отделни процеса: единият слуша сървъра, а другият изпраща, за да се свържем към сървъра ние посочваме частна ip адреса на сървъра и показваме на кой порт искаме да изпращаме информацията и функциите, които използваме в пейджъра са : receive message, send message, send init message. 
-Receive message е да чака дали сървъра праща нещо, ако получи съобщение от сървъра и го показва на човека.
- Send message, чака потребителя да въведе съобщение и ще го в генерира json, които го изпраща на ”мамата”.
 -Send init message изпраща различен json, които показва, че има нов пейджър свързал се към системата, за да можем  да слушаме какво праща сървъра, и да пращаме към сървъра използваме два различни thread-a, два процеса, които са независят един от друг.
Идеята на сървъра(Big „мама”) е винаги да слуша за идващо съобщение от пейджър към друг (насочен)  пейджър.
jorh — 03/12/2022
Слушането е отделен процес, по този начин сървъра ни може да обработи неограничен брой пейджъри.
Когато сървърът получи съобщение от пейджъра, преди да изпратим съобщение, то минава през „транслате”(превеждащата) функцията. Той създава съобщение с json формат и го изпраща на получателя. 
За реализиране на този скрипт използваме функциите, make server, multi threaded client, send message, save init message и translate message.
-Make server е функция, която създава връзка за всеки свързал се със сървъра пейджър посредством създаване на нов процес (треад(thread)).
-Send message получава  json и клиент използвайки json генериращ  съобщения, които искаме да изпратим, проверяваме пейджъра, дали съществува..

