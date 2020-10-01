# VK API
from vk_api.longpoll import VkLongPoll, VkEventType

# нативные модули
from bot_actions import *       # модуль для работы с ботом, базовые функции
from deadlines_data import *    # модуль для работы с таблицей дедлайнов

# доп. модули
import os
from funcy import group_by
from bs4 import BeautifulSoup


# делаем оригинальные приветствия
urlGreetings = "https://heaclub.ru/originalnye-neobychnye-privetstviya-pri-vstreche-na-vse-sluchai-zhizni-spisok-privetstvennyh-slov-i-fraz-primery"

greetings_list = []

resp = requests.get(urlGreetings)
soup = BeautifulSoup(resp.content, features="html.parser")
greetings = soup.findAll('li')
for hello in greetings:
    greetings_list.append(hello.text)

# делаем оригинальные прощания
goodbye_list = ['Пока-пока, человек...', 'Пока!\nБудь здоров!', 'Увидимся!', 'Пока, бывай', 'До скорого']

# токен группы и работа с запросами
_TOKEN = 'token'
vk = vk_api.VkApi(token = _TOKEN)
longpoll = VkLongPoll(vk)

# эмоджи
_EMOJIS = ['👻 ','🤡 ','🤓 ','😁 ','😏 ','😛 ','👋 ']

# команды
_COMMANDS = {
                'привет': 'random.choice(_EMOJIS) + random.choice(greetings_list[25:-40])',
                'пока': 'random.choice(_EMOJIS) + random.choice(goodbye_list)',
                'команды': '🔧 Команды:\n• привет\n• пока\n• журналы\n• дедлайны\n• почта\n• уровень\n• команды\n• полезные ссылки',
                'дедлайны': 'update_deadlines(client)',
                'почты': 'mails_list',
                'уровень': 'history_messages(vk, session.user_id)',
                'дни рождения': '💊 Выберите нужный вариант',
                'на месяц': '📅 Выберите нужный месяц',
                'на неделю': 'birthday_on_week(birthdays_list)',
                'все': "birthdays_list",
                'учебники': '💊 Выберите курс',
                '_SUBJECTS': '📚 Выбери нужный учебник',
                'назад': '🛠 Вываливаемся, товарищи',
                'кнопка на случай, если устал учиться': '😺 Как же я тебя понимаю...',
                'что посмотреть?': 'send_films(film_list)',
                'но не устал от математики': 'send_task(olimplist)',
                'полезные ссылки': '🔗 Выберите ссылку',
                '1 курс': '💼 Учебники 1 курса',
                '2 курс': '💼 Учебники 2 курса',
                'журналы': '📖 Выберите журналы',
                'начать': 'https://www.youtube.com/watch?v=bQLADRNBItw&ab_channel=LocalDad',
             }

commands_list = list(_COMMANDS.keys())
messages_list = list(_COMMANDS.values())

# месяца
_MONTHS = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь','июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

# предметы
_SUBJECTS = ['английский', 'алгебра', 'wolfram mathematica', 'мат. анализ', 'дискр. мат', 'диффуры']

# фото
pic_path = os.listdir(path = 'pictures')
all_pic = [list(map(lambda x: 'pictures/' + x, i)) for i in list(group_by(0, pic_path).values())]
pic_category = ['hello', 'bye', 'level']
_PICTURES = dict(zip(pic_category, all_pic))

# дни рождения
with open('data/birth.txt', 'r', encoding = 'utf-8') as birthdays:
    birthdays_list = birthdays.readlines()

# фильмы
with open('data/films.txt', 'r', encoding = 'utf-8') as films:
    film_list = films.readlines()

# олипипиадные задачки
with open('data/olimp.txt', 'r', encoding = 'utf-8') as olimp:
    olimp_list = olimp.readlines()

with open('data/mails.txt', 'r', encoding = 'utf-8') as mails:
    mails_list = ''.join(mails.readlines())

# запуск бота
for session in longpoll.listen():
    if session.type == VkEventType.MESSAGE_NEW:

        user_message = session.text.lower()
        keyboard = create_keyboard(user_message)

        if session.to_me:
            if user_message == commands_list[0]:    # привет
                send_photo(vk, session.user_id, random.choice(_EMOJIS) + random.choice(greetings_list[25:-40]), random.choice(_PICTURES['hello']), keyboard)

            elif user_message == commands_list[1]:  # пока
                send_photo(vk, session.user_id, random.choice(_EMOJIS) + random.choice(goodbye_list),random.choice(_PICTURES['bye']), keyboard)

            elif user_message == commands_list[2]:  # команды
                write_message(vk, session.user_id, messages_list[2], keyboard)

            elif user_message == commands_list[3]:  # дедлайны
                write_message(vk, session.user_id, update_deadlines(client), keyboard)

            elif user_message == commands_list[4]:  # почты
                write_message(vk, session.user_id, mails_list, keyboard)

            elif user_message == commands_list[5]:  # добавляем количсетво сообщений в переписке
                send_photo(vk, session.user_id, history_messages(vk, session.user_id), _PICTURES['level'][0], keyboard)

            elif user_message == commands_list[6]:  # узнаём дни рождения
                write_message(vk, session.user_id, messages_list[6], keyboard)

            elif user_message == commands_list[7]:  # дни рождения на месяц
                write_message(vk, session.user_id, messages_list[7], keyboard)

            elif user_message == commands_list[8]:  # дни рождения на неделю
                write_message(vk, session.user_id, birthday_on_week(birthdays_list), keyboard)

            elif user_message == commands_list[9]:  # дни рожения на год
                write_message(vk, session.user_id, ''.join(birthdays_list), keyboard)

            elif user_message in _MONTHS:           # дни рожения в определённом месяце
                write_message(vk, session.user_id, birthday_on_month(user_message, birthdays_list), keyboard)

            elif user_message == commands_list[10]: # учебники
                write_message(vk, session.user_id, messages_list[10], keyboard)

            elif user_message in _SUBJECTS:
                write_message(vk, session.user_id, messages_list[11], keyboard)

            elif user_message == commands_list[12]: # возвращаемся в главное меню
                write_message(vk, session.user_id, messages_list[12], keyboard)

            elif user_message == commands_list[13]: # меню с задачками или фильмами
                write_message(vk, session.user_id, messages_list[13], keyboard)

            elif user_message == commands_list[14]: # фильмы
                write_message(vk, session.user_id, send_films(film_list), keyboard)

            elif user_message == commands_list[15]: # задачки
                write_message(vk, session.user_id, send_task(olimp_list), keyboard)

            elif user_message == commands_list[16]: # полезные ссылки
                write_message(vk, session.user_id, messages_list[16], keyboard)

            elif user_message == commands_list[17]: # учебники 1 курс
                write_message(vk, session.user_id, messages_list[17], keyboard)
            
            elif user_message == commands_list[18]: # учебники 2 курс
                write_message(vk, session.user_id, messages_list[18], keyboard)
 
            elif user_message == commands_list[19]: # журналы
                write_message(vk, session.user_id, messages_list[19], keyboard)
            
            elif user_message == commands_list[20]: # начать
                write_message(vk, session.user_id, messages_list[20], keyboard)

            else:
                write_message(vk, session.user_id, "Я тупой бот и не понимаю вашего человеческого языка...\n\n" + messages_list[2], keyboard)
