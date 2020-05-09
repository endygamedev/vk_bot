# Модули для работы с сообщениями ВК
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import requests
import random
import json
import datetime

# Метод для отправки сообщения
def write_message(vk, user_id, message, keyboard):
    '''
    write_message(vk, user_id, message) - отправка текстового сообщения с текстом message.
    '''
    vk.method('messages.send', {
    'user_id': user_id,
    'message': message,
    'random_id': random.getrandbits(31) * random.choice([-1, 1]),
    'keyboard': keyboard
    })

# Метод для отправки сообщения с картинкой
def send_photo(vk, user_id, message, picture, keyboard):
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
    'random_id': random.getrandbits(31) * random.choice([-1, 1]),
    'keyboard': keyboard
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

# День рожения на неделе
def week(data):
    '''
    week(data) - возвращает список людей у которых День рождения на этой неделе.
    '''
    l=[]
    for b in range(1,8):
        a = datetime.date.today()
        bb = datetime.timedelta(days=b)
        cc = a+bb
        l.append(str(cc))
    l1=[i[5:7] for i in l]
    l2=[i[-2:] for i in l]
    dr=[i for i in data if i[-3:-1] in l1 and i[-6:-4] in l1]
    if dr == []:
        return 'На этой неделе пока никто не родился, но есть шанс это исправить)\n😏 Свободен сегодня вечером?'
    else:
        return ''.join(dr)

# Список фильмов
def send_films(list):
    '''
    send_films(list) - возвращает список фильмов.
    '''
    return '🎬 Другие Primats рекомендуют:\n\n'+''.join(random.sample(list,3))

# Генерация олимпиадной задачки
def send_task(list):
    '''
    send_task(list) - возвращает олимпиадную задачку.
    '''
    return '🤓 Развлекайся\n\n' + random.choice(list)

# День рожения за месяц
def dr(m, data):
    '''
    dr(m, data) - возвращает список людей у которых День рождения в определённом месяце m.
    '''
    mon={"январь":'01','февраль':'02','март':"03",'апрель':'04','май':'05','июнь':'06','июль':'07','август':'08','сентябрь':'09',"октябрь":'10','ноябрь':'11','декабрь':'12'}
    L=[i for i in data if i[-3:-1]  ==  mon.get(m)]
    if L == []:
        return 'В этом месяце пока никто не родился, но есть шанс это исправить)\n😏 Свободен сегодня вечером?'
    else:
        return ''.join(L)

# Клавиатура
def create_keyboard(response):
    '''
    create_keyboard(response) - возвращает пользователю сформированную клавиатуру.
    '''
    keyboard = VkKeyboard(one_time=False)

    if response == 'кнопка на случай, если устал учиться':
        keyboard.add_button('но не устал от математики', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Что посмотреть?', color=VkKeyboardColor.POSITIVE)

    elif response == 'дни рождения':
        keyboard.add_button('На месяц',color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('На неделю',color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Все',color=VkKeyboardColor.POSITIVE)

    elif response == 'учебники':
        keyboard.add_button('Мат.анализ',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Алгебра',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Дискр.мат',color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Wolfram Math',color=VkKeyboardColor.PRIMARY)
        keyboard.add_openlink_button('Python','https://vk.com/away.php?to=https%3A%2F%2Fvk.cc%2FalOWY8&cc_key=')
        keyboard.add_line()
        keyboard.add_button('Английский',color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Назад',color=VkKeyboardColor.NEGATIVE)

    elif response == 'английский':
        keyboard.add_openlink_button('Market Leader','https://vk.com/away.php?to=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F1xEkwAyIT2AtAuJ56xVyfFQ5w8czPtJAa%2Fview&cc_key=')
        keyboard.add_line()
        keyboard.add_openlink_button('Facilitator','https://vk.com/away.php?to=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F17P1MYWDJDREdfGQRGD9inyREZAqEXlR6%2Fview&cc_key=')
        keyboard.add_line()
        keyboard.add_openlink_button('Practical Grammar Course','https://vk.com/away.php?to=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F1LJLLploS_8epi8yYWsVjm5JsDi7nmHYu%2Fview&cc_key=')
        keyboard.add_line()
        keyboard.add_button('Назад',color=VkKeyboardColor.NEGATIVE)

    elif response == 'wolfram math':
        keyboard.add_openlink_button('Фридман,Леора','https://vk.com/away.php?to=https%3A%2F%2Fdrive.google.com%2Fopen%3Fid%3D1xg9g1LAuw-jIH6HwH9e-UE_GU9bq8Kri&cc_key=')
        keyboard.add_line()
        keyboard.add_openlink_button('S.Wolfram "Wolfram Language"','https://vk.com/away.php?to=https%3A%2F%2Fwww.wolfram.com%2Flanguage%2Felementary-introduction%2F2nd-ed%2Findex.html&cc_key=')
        keyboard.add_line()
        keyboard.add_openlink_button('Help','https://reference.wolfram.com/language/')
        keyboard.add_line()
        keyboard.add_button('Назад',color=VkKeyboardColor.NEGATIVE)

    elif response == 'мат.анализ':
        keyboard.add_openlink_button('Демидович (задачник)','https://drive.google.com/file/d/1VnHhcsfAlVg48nsYXWdXfNZiVkakamv-/view')
        keyboard.add_line()
        keyboard.add_openlink_button('Виноградов, Громов','https://vk.com/doc108898977_514996947?hash=984e14ef93de90b23e&dl=a91def24fdbf7a14b9')
        keyboard.add_line()
        keyboard.add_button('Назад',color=VkKeyboardColor.NEGATIVE)

    elif response == 'алгебра':
        keyboard.add_openlink_button('Икрамов (задачник)','https://vk.com/away.php?to=https%3A%2F%2Fdrive.google.com%2Fopen%3Fid%3D1KxIrUV3yGT_IKzz2X52JW6x1mUmoqP7C&cc_key=')
        keyboard.add_line()
        keyboard.add_openlink_button('Воеводин','https://vk.com/away.php?to=https%3A%2F%2Fdrive.google.com%2Fopen%3Fid%3D1Cd-Q2GMVhLERwJSh1lyriE89DsBRUc6V&cc_key=')
        keyboard.add_line()
        keyboard.add_openlink_button('Курош','https://vk.com/doc61070830_524793039?hash=12ae30e78883526a84&dl=afb96283e5d1fe460f')
        keyboard.add_line()
        keyboard.add_openlink_button('Фадеев','https://vk.com/doc437171420_515200818?hash=336121839fac36e083&dl=dfed8ac668a6205674')
        keyboard.add_line()
        keyboard.add_button('Назад',color=VkKeyboardColor.NEGATIVE)

    elif response == 'дискр.мат':
        keyboard.add_openlink_button('Иванов, Фридман','https://vk.com/doc234167654_514661330?hash=9fead45b2c2f3e2ce2&dl=0bef1a3cd3e9273e36')
        keyboard.add_line()
        keyboard.add_openlink_button('Корте "Комбинаторная оптимизация"','https://drive.google.com/file/d/1kOZcitXuRBTKX0pgpXC8FEPenW4rjz6y/view')
        keyboard.add_line()
        keyboard.add_button('Назад',color=VkKeyboardColor.NEGATIVE)

    elif response == 'полезные ссылки':
        keyboard.add_openlink_button('Мат. анализ','https://us02web.zoom.us/j/624529129?pwd=bHBoODh3YTlad3VlNHFOcStNM3ZxQT09')
        keyboard.add_line()
        keyboard.add_openlink_button('БРС','http://www.rating.unecon.ru/')
        keyboard.add_line()
        keyboard.add_openlink_button('Moodle','https://student.unecon.ru/')
        keyboard.add_line()
        keyboard.add_button('Назад',color=VkKeyboardColor.NEGATIVE)

    elif response == 'на месяц':
        keyboard.add_button('Январь',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Февраль',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Март',color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Апрель',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Май',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Июнь',color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Июль',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Август',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Сентябрь',color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Октябрь',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Ноябрь',color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Декабрь',color=VkKeyboardColor.PRIMARY)

    else:
        keyboard.add_button('Привет', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Пока', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('Уровень', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()

        keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Учебники', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Дедлайны', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()

        keyboard.add_button('Дни Рождения', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Почта', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Полезные ссылки', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()

        keyboard.add_button('Кнопка на случай, если устал учиться', color=VkKeyboardColor.PRIMARY)


    keyboard = keyboard.get_keyboard()
    return keyboard
