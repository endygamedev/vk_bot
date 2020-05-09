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
                'дни рождения': '💊 Выбери нужный вариант',
                'на месяц': '📅 Выбери нужный месяц',
                'на неделю': 'week(birthdaysList)',
                'все': "'.join(birthdaysList)",
                'учебники': '💼 Выбери нужный предмет',
                '_SUBJECTS': '📚 Выбери нужный учебник',
                'назад': '🛠 Вываливаемся, товарищи',
                'кнопка на случай, если устал учиться': '😺 Как же я тебя понимаю...',
                'что посмотреть?': 'send_films(filmlist)',
                'но не устал от математики': 'send_task(olimplist)',
                'полезные ссылки': '🔗 Выберите ссылку'
             }

commands_list = list(_COMMANDS.keys())
messages_list = list(_COMMANDS.values())

# Месяца
_MONTHS = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь','июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

# Предметы
_SUBJECTS = ['английский', 'алгебра', 'wolfram math', 'мат.анализ', 'дискр.мат']

# Фоточки
pic_path = os.listdir(path='pictures')
all_pic = [list(map(lambda x: 'pictures/'+x, i)) for i in list(group_by(0, pic_path).values())]
pic_category = ['hello', 'bye', 'level']
_PICTURES = dict(zip(pic_category,all_pic))

# Расписание
with open('data/oddWeek.txt', 'r', encoding='utf-8') as file_odd, open('data/evenWeek.txt', 'r', encoding="utf-8") as file_even:
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

            elif user_message == commands_list[7]: # узнаём Дни рождения
                write_message(vk, session.user_id, messages_list[7], keyboard)

            elif user_message == commands_list[8]: # Дни рождения на месяц
                write_message(vk, session.user_id, messages_list[8], keyboard)

            elif user_message == commands_list[9]: # Дни рождения на неделю
                write_message(vk, session.user_id, week(birthdaysList), keyboard)

            elif user_message == commands_list[10]: # Дни рожения на год
                write_message(vk, session.user_id, ''.join(birthdaysList), keyboard)

            elif user_message in _MONTHS: # Дни рожения в определённом месяце
                write_message(vk, session.user_id, dr(user_message, birthdaysList), keyboard)

            elif user_message == commands_list[11]: # учебники
                write_message(vk, session.user_id, messages_list[11], keyboard)

            elif user_message in _SUBJECTS:
                write_message(vk, session.user_id, messages_list[12], keyboard)

            elif user_message == commands_list[13]: # возвращаемся в главное "меню"
                write_message(vk, session.user_id, messages_list[13], keyboard)

            elif user_message == commands_list[14]: # меню с задачками или фильмами
                write_message(vk, session.user_id, messages_list[14], keyboard)

            elif user_message == commands_list[15]: # фильмы
                write_message(vk, session.user_id, send_films(filmlist), keyboard)

            elif user_message == commands_list[16]: # задачки
                write_message(vk, session.user_id, send_task(olimplist), keyboard)

            elif user_message == commands_list[17]: # полезные ссылки
                write_message(vk, session.user_id, messages_list[17], keyboard)

            else:
                write_message(vk, session.user_id, "Я тупой бот и не понимаю вашего человеческого языка...\n\n" + messages_list[3], keyboard)
