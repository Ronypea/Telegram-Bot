# Telegram-Bot
Python lab 1 course ITMO

## Суть проекта 
Целью всей работы является написать бота, который бы позволил получить расписание занятий для любой группы ИТМО. 

Бот должен понимать следующие команды:
* ` near_lesson GROUP_NUMBER ` - ближайшее занятие для указанной группы;
* ` DAY WEEK_NUMBER GROUP_NUMBER ` - расписание занятий в указанный день (monday, thuesday, ...). Неделя может быть четной (1), нечетной (2) или же четная и нечетная (0);
* ` tommorow GROUP_NUMBER ` - расписание на следующий день (если это воскресенье, то выводится расписание на понедельник, учитывая, что неделя может быть четной или нечетной);
* ` all WEEK_NUMBER GROUP_NUMBER ` - расписание на всю неделю.

## Реализация 
Работа осуществлялась через модуль ` pyTelegramBotAPI `.

Чтобы извлечь расписание, необходимо получить код html-страницы для соответствующей группы, а затем из этой страницы выделить интересующую нас информацию.
Чтобы получить исходный код страницы достаточно выполнить GET запрос. 

URL, к которому мы будем обращаться, имеет следующий формат:
http://www.ifmo.ru/ru/schedule/0/GROUP/WEEK/raspisanie_zanyatiy_GROUP.htm 

Теперь из этой страницы нам нужно извлечь время занятий, место проведения, аудиторию и название дисциплины. Для этого нам понадобится HTML-парсер. В этой работе предлогается использовать модуль BeautifulSoup.

Запустить бота можно следующим образом:
```bash
$ python3 bot.py
```
