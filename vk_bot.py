# VK API
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# Мои модули
from bot_actions import * # Модуль для работы с ботом, базовые функции
from deadlines_data import * # Модуль для работы с таблицей дедлайнов

# Доп. модули
import os
from funcy import group_by
from bs4 import BeautifulSoup
from epiweeks import Week

# Делаем оригинальные приветствия
urlGreetings = "https://heaclub.ru/originalnye-neobychnye-privetstviya-pri-vstreche-na-vse-sluchai-zhizni-spisok-privetstvennyh-slov-i-fraz-primery"

greetings_list = []

resp = requests.get(urlGreetings)
soup = BeautifulSoup(resp.content, features="html.parser")
greetings = soup.findAll('li')
for hello in greetings:
    greetings_list.append(hello.text)

# Делаем оригинальные прощания
goodbye_list = ['Пока-пока, человек...', 'Пока!\nБудь здоров!', 'Увидимся!', 'Пока, бывай', 'До скорого']

# Токен нашей группы и работа с запросами
_TOKEN = '3d423eb8812629fc6834d96bd0b5352f75f83f7691f828ca84ac57b909bf2ff519f438bc6aa4d9316cc03'
vk = vk_api.VkApi(token=_TOKEN)
longpoll = VkLongPoll(vk)

# Эмоджи
_EMOJIS = ['👻 ','🤡 ','🤓 ','😁 ','😏 ','😛 ','👋 ']

# Команды
_COMMANDS = {
                'привет': 'random.choice(_EMOJIS)+random.choice(greetings_list[25:-40])',
                'пока': 'random.choice(_EMOJIS)+random.choice(goodbye_list)',
                'расписание': 'weekNumber',
                'команды': '🔧 Команды:\n• привет\n• пока\n• расписание\n• дедлайны\n• почта\n• уровень\n• команды',
                'дедлайны': 'update_deadlines(client)',
                'почта': "📬Логин: appliedmath1900@yahoo.com\n🔒Пароль: PMstudents1900",
                'уровень': 'history_messages(vk, session.user_id)',
                'клавиатура': 'vk_keyboard(vk, session.user_id, keyboard)',
                'начать': 'vk_keyboard(vk, session.user_id, keyboard)'
             }

commands_list = list(_COMMANDS.keys())
messages_list = list(_COMMANDS.values())

# Фоточки
pic_path = os.listdir(path='pictures')
all_pic = [list(map(lambda x: 'pictures/'+x, i)) for i in list(group_by(0, pic_path).values())]
pic_category = ['hello', 'bye', 'level']
_PICTURES = dict(zip(pic_category,all_pic))

# Расписание
with open('data/oddWeek.txt', 'r', encoding="utf-8") as file_odd, open('data/evenWeek.txt', 'r', encoding="utf-8") as file_even:
    oddWeek = file_odd.read()
    evenWeek = file_even.read()

# Дни рождения
with open('data/birth.txt','r', encoding='utf-8') as birthdays:
    birthdaysList=birthdays.readlines()

# Фильмы
with open ('data/films.txt','r', encoding='utf-8') as films:
    filmlist=films.readlines()

# Олипипиадные задачки
with open('data/olimp.txt','r', encoding='utf-8') as olimp:
    olimplist=olimp.readlines()


# Запускаем нашего бота
for session in longpoll.listen():
    if session.type == VkEventType.MESSAGE_NEW:
        user_message = session.text.lower()
        keyboard = create_keyboard(user_message)
        if session.to_me:
            if user_message == commands_list[0]: # привет
                send_photo(vk, session.user_id, random.choice(_EMOJIS) + random.choice(greetings_list[25:-40]), random.choice(_PICTURES['hello']), keyboard)

            elif user_message == commands_list[1]: # пока
                send_photo(vk, session.user_id, random.choice(_EMOJIS) + random.choice(goodbye_list),random.choice(_PICTURES['bye']), keyboard)

            elif user_message == commands_list[2]: # расписание
                # Определяет текущую неделю, мы выявили опытным путём, что начало недель датируется 10.8.2019
                weekNumber = Week.fromdate(datetime.date(2019,8,10)).weektuple()[-1]
                if weekNumber%2 == 0:
                    write_message(vk, session.user_id, evenWeek, keyboard)
                else:
                    write_message(vk, session.user_id, oddWeek, keyboard)

            elif user_message == commands_list[3]: # команды
                write_message(vk, session.user_id, messages_list[3], keyboard)

            elif user_message == commands_list[4]: # дедланы
                write_message(vk, session.user_id, update_deadlines(client), keyboard)

            elif user_message == commands_list[5]: # почта
                write_message(vk, session.user_id, messages_list[5], keyboard)

            elif user_message == commands_list[6]: # добавляем кол-во сообщений в переписке
                send_photo(vk, session.user_id, history_messages(vk, session.user_id), _PICTURES['level'][0], keyboard)

            elif user_message=='дни рождения':
                write_message(vk,session.user_id,'Выбери нужный вариант',keyboard=keyboard)

            elif user_message=='на месяц':
                write_message(vk,session.user_id,'Выбери нужный месяц',keyboard=keyboard)

            elif user_message=='на неделю':
                write_message(vk,session.user_id,week(birthdaysList),keyboard=keyboard)

            elif user_message=='все':
                write_message(vk,session.user_id,''.join(birthdaysList),keyboard=keyboard)

            elif user_message=='январь' or user_message=='февраль' or user_message=='март' or user_message=='апрель' or user_message=='май' or user_message=='июнь' or user_message=='июль' or user_message=='август' or user_message=='сентябрь' or user_message=='октябрь' or user_message=='ноябрь' or user_message=='декабрь':
                write_message(vk,session.user_id, dr(user_message, birthdaysList), keyboard=keyboard)

            elif user_message=='учебники':
                write_message(vk,session.user_id,  'Выбери нужный предмет',keyboard=keyboard)

            elif user_message=='английский' or user_message=='алгебра' or user_message=='wolfram math' or user_message=='мат.анализ' or user_message=='дискр.мат':
                write_message(vk,session.user_id,  'Выбери нужный учебник',keyboard=keyboard)

            elif user_message=='назад':
                write_message(vk,session.user_id ,'Вываливаемся товарищи',keyboard=keyboard)

            elif user_message=='кнопка на случай, если устал учиться':
                write_message(vk,session.user_id ,'Как же я тебя понимаю...',keyboard=keyboard)

            elif user_message=='что посмотреть?':
                write_message(vk,session.user_id ,send_films(filmlist),keyboard=keyboard)

            elif user_message=='но не устал от математики':
                write_message(vk,session.user_id ,send_task(olimplist),keyboard=keyboard)

            elif user_message=='полезные ссылки':
                write_message(vk,session.user_id ,'Ммммм',keyboard=keyboard)

            else:
                write_message(vk, session.user_id, "Я тупой бот и не понимаю вашего человеческого языка...\n\n" + messages_list[3],keyboard)
