import requests
from bs4 import BeautifulSoup
import telebot
import time
import datetime
import html5lib


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain='http://www.ifmo.ru/ru/schedule/0',
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page, day):
    soup = BeautifulSoup(web_page, 'html5lib')
    try:
        schedule_table = soup.find("table", attrs={"id": "{}day".format(day)})
        times_list = schedule_table.find_all("td", class_="time")
        times_list = [time.span.text for time in times_list]

        try:
            weeks_list = schedule_table.find_all("td", class_="time")
            weeks_list = [week.dt.text for week in weeks_list]
        except:
            weeks_list.append(' ')

        locations_list = schedule_table.find_all("td", class_="room")
        locations_list = [room.span.text for room in locations_list]

        lessons_list = schedule_table.find_all("td", class_="lesson")
        lessons_list = [lesson.text.split() for lesson in lessons_list]
        lessons_list = [' '.join([info for info in lesson_info if info])
                        for lesson_info in lessons_list]

        rooms_list = schedule_table.find_all("td", class_="room")
        rooms_list = [room.dd.text for room in rooms_list]
    except:
        times_list = weeks_list = locations_list = 0
        lessons_list = rooms_list = 0
    return times_list, weeks_list, locations_list, lessons_list, rooms_list


def get_day_schedule(day, week, group):
    web_page = get_page(group, week)
    times, weeks, locations, lessons, rooms = get_schedule(web_page, day)
    resp = ''
    if times == 0:
        resp = 'Нет занятий\n'
    else:
        for xtime, xweek, location, lesson, room in zip(times,
                                                        weeks,
                                                        locations,
                                                        lessons,
                                                        rooms):
            resp += '<b>{} {}</b>\n{}, {}, {}\n'.format(xtime,
                                                        xweek,
                                                        location,
                                                        lesson,
                                                        room)
    return resp


access_token = '299863676:AAHCDeEMvCQht5455QQRGHDEDPCJB7diHJU'
bot = telebot.TeleBot(access_token)


@bot.message_handler(commands=['monday',
                               'tuesday',
                               'wednesday',
                               'thursday',
                               'friday',
                               'saturday'])
def get_day(message):
    try:
        day, week, group = message.text.split()
    except:
        try:
            day, group = message.text.split()
            if group in ['0', '1', '2']:
                week = group
                group = 'M3100'
            else:
                week = '0'
        except:
            day = message.text
            group = 'M3100'
            week = '0'
    calendar = {'/monday': 1,
                '/tuesday': 2,
                '/wednesday': 3,
                '/thursday': 4,
                '/friday': 5,
                '/saturday': 6}
    resp = get_day_schedule(str(calendar.get(day)), week, group)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near_lesson'])
def get_near(message):
    try:
        _, group = message.text.split()
    except:
        group = 'M3100'
    day = time.strftime('%w')
    week = int(time.strftime('%W')) % 2 + 1
    web_page = get_page(group, week)
    resp = ''
    starts = [
        datetime.time(8, 20),
        datetime.time(10, 0),
        datetime.time(11, 40),
        datetime.time(13, 30),
        datetime.time(15, 20),
        datetime.time(17, 0),
        datetime.time(18, 40)]
    itmo_time = [
        '8:20-9:50',
        '10:00-11:30',
        '11:40-13:10',
        '13:30-15:00',
        '15:20-16:50',
        '17:00-18:30',
        '18:40-20:10']
    cur = datetime.time(int(time.strftime('%H')), int(time.strftime('%M')))

    def get_first():
        day = time.strftime('%w')
        resp = ''
        times = 0
        while times == 0:
            if day == '6' or day == '0':
                day = '1'
                week = (int(time.strftime('%W')) + 1) % 2 + 1
            else:
                day = int(day) + 1
                week = int(time.strftime('%W')) % 2 + 1
            times, weeks, locations, lessons, rooms = \
                get_schedule(web_page, str(day))
        resp += '<b>{}</b>\n{}, {}, {}\n'.format(times[0],
                                                 locations[0],
                                                 lessons[0],
                                                 rooms[0])
        return resp

    times, weeks, locations, lessons, rooms = get_schedule(web_page, str(day))
    if times == 0:
        resp = get_first()
    else:
        schedule = []
        num = 0
        for xtime in range(7):
            try:
                if itmo_time[xtime] == times[num]:
                    schedule.append(1)
                    num += 1
                else:
                    schedule.append(0)
            except:
                schedule.append(0)
        if cur < starts[0]:
            resp = '<b>{}</b>\n{}, {}, {}\n'.format(times[0],
                                                    locations[0],
                                                    lessons[0],
                                                    rooms[0])
        else:
            for num in range(0, 7):
                if cur < starts[num]:
                    break
            if cur > starts[6]:
                resp = get_first()
            i = 0
            while num < 7 and schedule[num] == 0:
                num += 1
            if num == 7:
                resp = get_first()
            else:
                for xtime in times:
                    i += 1
                    if times[i - 1] == itmo_time[num]:
                        i -= 1
                        resp = '<b>{}</b>\n{}, {}, {}\n'.format(times[i],
                                                                locations[i],
                                                                lessons[i],
                                                                rooms[i])
                        break
        if resp == '':
            resp = get_first()
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tmrw(message):
    try:
        _, group = message.text.split()
    except:
        group = 'M3100'
    day = time.strftime('%w')
    if day == '6' or day == '7':
        day = '1'
        week = (int(time.strftime('%W')) + 1) % 2 + 1
    else:
        day = int(day) + 1
        week = int(time.strftime('%W')) % 2 + 1
    resp = get_day_schedule(str(day), week, group)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all(message):
    try:
        _, week, group = message.text.split()
    except:
        try:
            _, group = message.text.split()
            if group in ['0', '1', '2']:
                week = group
                group = 'M3100'
            else:
                week = '0'
        except:
            group = 'M3100'
            week = '0'
    resp = ''
    calendar = {1: 'Понедельник',
                2: 'Вторник',
                3: 'Среда',
                4: 'Четверг',
                5: 'Пятница',
                6: 'Суббота'}
    for day in range(1, 7):
        resp += '\n<b>{}</b>\n'.format(calendar.get(day))
        resp += get_day_schedule(str(day), week, group)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
