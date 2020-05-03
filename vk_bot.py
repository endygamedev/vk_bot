# VK API
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# Мои модули
from bot_actions import * # Модуль для работы с ботом, базовые функции
from deadlines_data import * # Модуль для работы с таблицей дедлайнов

# Доп. модули
import datetime
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
_TOKEN = 'токен группы'
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

# Определяет текущую неделю, мы выявили опытным путём, что начало недель датируется 11.8.2019
weekNumber = Week.fromdate(datetime.date(2019,8,11)).weektuple()[-1]


# Запускаем нашего бота
for session in longpoll.listen():
    if session.type == VkEventType.MESSAGE_NEW:
        if session.to_me:
            user_message = session.text

            if user_message.lower() == commands_list[0]: # привет
                send_photo(vk, session.user_id, random.choice(_EMOJIS) + random.choice(greetings_list[25:-40]), random.choice(_PICTURES['hello']))

            elif user_message.lower() == commands_list[1]: # пока
                send_photo(vk, session.user_id, random.choice(_EMOJIS) + random.choice(goodbye_list),random.choice(_PICTURES['bye']))

            elif user_message.lower() == commands_list[2]: # расписание
                if weekNumber%2 == 0:
                    write_message(vk, session.user_id, evenWeek)
                else:
                    write_message(vk, session.user_id, oddWeek)

            elif user_message.lower() == commands_list[3]: # команды
                write_message(vk, session.user_id, messages_list[3])

            elif user_message.lower() == commands_list[4]: # дедланы
                write_message(vk, session.user_id, update_deadlines(client))

            elif user_message.lower() == commands_list[5]: # почта
                write_message(vk, session.user_id, messages_list[5])

            elif user_message.lower() == commands_list[6]: # добавляем кол-во сообщений в переписке
                send_photo(vk, session.user_id, history_messages(vk, session.user_id), _PICTURES['level'][0])


            elif user_message.lower() == commands_list[7] or user_message.lower() == commands_list[8]: # обновляем клавиатуру
                vk_keyboard(vk, session.user_id, keyboard)

            else:
                write_message(vk, session.user_id, "Я тупой бот и не понимаю вашего человеческого языка...\n\n" + messages_list[3])
