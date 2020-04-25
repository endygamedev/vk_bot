# Модули для работы с сообщениями ВК
import requests
import random
import json

# Метод для отправки сообщения
def write_message(vk, user_id, message):
    '''
    write_message(vk, user_id, message) - отправка текстового сообщения с текстом message.
    '''
    vk.method('messages.send', {
    'user_id': user_id,
    'message': message,
    'random_id': random.getrandbits(31) * random.choice([-1, 1])
    })

# Метод для отправки сообщения с картинкой
def send_photo(vk, user_id, message, picture):
    '''
    send_photo(vk, user_id, message, picture) - отправка сообщения сообщения с текстом message и с картинкой picture.
    '''
    picURLFromServer = vk.method("photos.getMessagesUploadServer") # Получаем ссылку от сервера ВК на загрузку фото
    sendPicToServer = requests.post(picURLFromServer['upload_url'], files={'photo': open(picture, 'rb')}).json() # Загружаем фото на адрес сервера, которое нам выдал VK Api Server
    savePicToServer = vk.method('photos.saveMessagesPhoto', {'photo': sendPicToServer['photo'], 'server': sendPicToServer['server'], 'hash': sendPicToServer['hash']})[0] # Сохраняем добавленное фото на сервера ВК
    dataPic = f'photo{savePicToServer["owner_id"]}_{savePicToServer["id"]}' # Записываем все данные о фотографии

    vk.method("messages.send", { # высылаем наше сообщение
    'user_id': user_id,
    'message': message,
    'attachment': dataPic,
    'random_id': random.getrandbits(31) * random.choice([-1, 1])
     })

# Метод для работы с уровнем пользовалеля
def history_messages(vk, user_id):
    '''
    history_messages(vk, user_id) - кол-во сообщений от пользователя и определение его уровня.
    '''
    history = vk.method('messages.getHistory', { # учитывается сообщения пользователя и бота
        "user_id": user_id,
        "count": 200
    })
    count_messages = int(round(history['count']/2, 1))
    return {
        0 <= count_messages <= 20: f'🐥 Уровень 0.\nВы даже на уровень не смогли наприсылать запросов, что с вас взять...\nКоличество собщений: {count_messages}',
        21 <= count_messages <= 40: f'🌝 Уровень 1.\nВы малюсенький и поганенький студентик!\nКоличество собщений: {count_messages}',
        41 <= count_messages <= 80: f'🌚 Уровень 2.\nВы маленький любознательный поганец!\nКоличество собщений: {count_messages}',
        81 <= count_messages <= 200: f'👨‍💻 Уровень 3.\nВы больше не маленький поганец, вы большой поганец!\nКоличество собщений: {count_messages}',
        count_messages >= 201: f'🏅 Уровень 4.\nВам ещё не выдали Нобелевскую премию?\nКоличество собщений: {count_messages}'
    }[1]

# Конструктор для текстовой кнопки
def text_button(label, color):
    '''
    button(label, color) - конструктор для создания кнопок.
    '''
    return {
        "action": {
            "type": "text",
            "label": label
        },
        "color": color
    }

# Конструктор для ссылки
def link_button(link, label):
    '''
    link_button(link, label) - конструктор для кнопок-ссылок.
    '''
    return {
        "action": {
            "type": "open_link",
            "link": link,
            "label": label
        }
    }

# Клавиатура
keyboard = {
    "one_time": False,
    "buttons": [
        [
            text_button("Привет", "primary"),
            text_button("Пока","primary")
        ],
        [
            text_button("Уровень", "primary"),
            text_button("Команды","default"),
            text_button("Почта","primary")
        ],
        [
            text_button("Расписание","positive"),
            text_button("Дедлайны","negative")
        ],
        [
            link_button('http://www.rating.unecon.ru/', "БРС"),
            link_button('https://student.unecon.ru/', "Moodle")
        ],
    ]
}

# Очищаем все кодировки, так требует ВК
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


# Метод для предоставления пользовалелю клавиатуры
def vk_keyboard(vk, user_id, keyboard):
    '''
    vk_keyboard(vk, user_id, keyboard) - выдаёт пользователю клавиатуру.
    '''
    vk.method("messages.send", {
                "user_id": user_id,
                "message": "⌨ Используй клавиатуру для общения со мной",
                "random_id": random.getrandbits(31) * random.choice([-1, 1]),
                "keyboard": keyboard
                })
