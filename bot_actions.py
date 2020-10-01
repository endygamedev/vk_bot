# модули для работы с сообщениями ВК
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import requests
import random
import json
import datetime


def write_message(vk: vk_api.vk_api.VkApi, user_id, message: str, keyboard) -> None:
    ''' Отправка текстового сообщения с текстом (message).

        Аргументы:
            vk: vk_api.vk_api.VkApi - объект VkApi для работы с группой
            user_id - id пользователя Вконтакте, которому отправится сообщение
            message: str - сообщение пользователю
            keyboard - клавиатура диалога в Вконтакте

        Возвращает:
            None

        Побочный эффект:
            Отправляет сообщению пользователю
    '''


    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': random.getrandbits(31) * random.choice([-1, 1]),
        'keyboard': keyboard
    })


def send_photo(vk: vk_api.vk_api.VkApi, user_id, message: str, picture, keyboard) -> None:
    ''' Отправка сообщения сообщения с текстом (message) и с картинкой (picture).

        Аргументы:
            vk: vk_api.vk_api.VkApi - объект VkApi для работы с группой
            user_id - id пользователя Вконтакте, которому отправится сообщение
            message: str - сообщение пользователю
            picture - картинка для пользователя
            keyboard - клавиатура диалога в Вконтакте

        Возвращает:
            None

        Побочный эффект:
            Отправляет сообщению пользователю с картинкой
    '''


    picURLFromServer = vk.method('photos.getMessagesUploadServer')  # получаем ссылку от сервера ВК на загрузку фото
    sendPicToServer = requests.post(picURLFromServer['upload_url'], files = {'photo': open(picture, 'rb')}).json()  # загружаем фото на адрес сервера, которое нам выдал VK Api Server
    savePicToServer = vk.method('photos.saveMessagesPhoto', {'photo': sendPicToServer['photo'], 'server': sendPicToServer['server'], 'hash': sendPicToServer['hash']})[0]  # сохраняем добавленное фото на сервера ВК
    dataPic = f'photo{savePicToServer["owner_id"]}_{savePicToServer["id"]}'  # записываем все данные о фотографии

    vk.method("messages.send", {  # высылаем сообщение
        'user_id': user_id,
        'message': message,
        'attachment': dataPic,
        'random_id': random.getrandbits(31) * random.choice([-1, 1]),
        'keyboard': keyboard
     })


def history_messages(vk: vk_api.vk_api.VkApi, user_id) -> str:
    ''' Количество сообщений от пользователя и определение его уровня.

        Аргументы:
            vk: vk_api.vk_api.VkApi - объект VkApi для работы с группой
            user_id - id пользователя Вконтакте, которому отправится сообщение

        Возвращает:
            str - сообщение пользователю в зависимости от количества сообщений в переписке с ботом
    '''


    history = vk.method('messages.getHistory', {  # учитывается сообщения пользователя и бота
        'user_id': user_id,
        'count': 200
    })

    count_messages = int(round(history['count'] / 2, 1))

    return {
        0 <= count_messages <= 20: f'🐥 Уровень 0.\nВы даже на уровень не смогли наприсылать запросов, что с вас взять...\nКоличество собщений: {count_messages}',
        21 <= count_messages <= 40: f'🌝 Уровень 1.\nВы малюсенький и поганенький студентик!\nКоличество собщений: {count_messages}',
        41 <= count_messages <= 80: f'🌚 Уровень 2.\nВы маленький любознательный поганец!\nКоличество собщений: {count_messages}',
        81 <= count_messages <= 200: f'👨‍💻 Уровень 3.\nВы больше не маленький поганец, вы большой поганец!\nКоличество собщений: {count_messages}',
        count_messages >= 201: f'🏅 Уровень 4.\nВам ещё не выдали Нобелевскую премию?\nКоличество собщений: {count_messages}'
    }[1]


def send_films(data: list) -> str:
    ''' Отправка трёх фильмов, которые рекомендую пользователи.

        Аргументы:
            data: list - список со всеми фильмами

        Возвращает:
            str - строку (список) трёх случайно выбранных фильмов из списка
    '''


    return '🎬 Другие primats рекомендуют:\n\n' + ''.join(random.sample(data, 3))


def send_task(data: list) -> str:
    ''' Отправка олимпиадной задачки.

        Аргументы:
            data: list - список олимпиадных задачек

        Возвращает:
            str - строку со слуйчайно выбранной олимпиадной задачкой
    '''


    return '🤓 Развлекайся\n\n' + random.choice(data)


def birthday_on_week(data: list) -> str:
    ''' Возвращает людей у которых день рождения на этой неделе.

        Аргументы:
            data: list - список со всеми днями рождениями

        Возвращает:
            str - строку (список) людей у которых день рождение на этой неделе
    '''


    lst = []
    s = 'На этой неделе пока никто не родился, но есть шанс это исправить)\n😏 Свободен сегодня вечером?'

    for b in range(1, 8):
        date_today = datetime.date.today()
        date_delta = datetime.timedelta(days = b)
        date_today_delta = date_today + date_delta
        lst.append(str(date_today_delta))

    lst1 = [_[5:7] for _ in lst]
    lst2 = [_[-2:] for _ in lst]
    lst_birthday = [_ for _ in data if _[-3:-1] in lst1 and _[-6:-4] in lst1]   # TODO: возможно тут ошибка, зачем тогда нужен lst (?)

    return s if lst_birthday == [] else ''.join(lst_birthday)



def birthday_on_month(month: str, data: list) -> str:
    ''' Возвращает людей у которых день рождения в этом месяце.

        Аргументы:
            month - месяц
            data - список со всеми днями рождениями

        Возвращает:
            str - строку (список) людей у которых день рождение в месяце month

        dr(m, data) - возвращает список людей у которых День рождения в определённом месяце m.
    '''

    s = 'В этом месяце пока никто не родился, но есть шанс это исправить)\n😏 Свободен сегодня вечером?'

    month_dict = {
            'январь': '01',
            'февраль': '02',
            'март': '03',
            'апрель': '04',
            'май': '05',
            'июнь': '06',
            'июль': '07',
            'август': '08',
            'сентябрь': '09',
            'октябрь': '10',
            'ноябрь': '11',
            'декабрь': '12'
        }

    lst_birthday_on_month = [element for element in data if element[-3:-1] == month_dict.get(month)]

    return s if lst_birthday_on_month == [] else ''.join(lst_birthday_on_month)


# Клавиатура
def create_keyboard(response: str) -> VkKeyboard:
    ''' Возвращает пользователю сформированную клавиатуру.

        Аргументы:
            response: str - запрос, который отправляет пользователь

        Возвращает:
            VkKeyboard - сформированную клавиатуру, которую запросил пользователь
    '''


    keyboard = VkKeyboard(one_time = False)

    if response == 'кнопка на случай, если устал учиться':
        keyboard.add_button('но не устал от математики', color = VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Что посмотреть?', color = VkKeyboardColor.POSITIVE)

    elif response == 'дни рождения':
        keyboard.add_button('На месяц', color = VkKeyboardColor.POSITIVE)
        keyboard.add_button('На неделю', color = VkKeyboardColor.POSITIVE)
        keyboard.add_button('Все', color = VkKeyboardColor.POSITIVE)
    
    elif response == 'журналы':
        keyboard.add_openlink_button('Журнал ПМ-1901', 'https://docs.google.com/spreadsheets/d/1bkuZWPd4poOCDnAlB_Q6nTssKl7RAgQJWdeR-H3f5p4/edit?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Журнал ПМ-1902', 'https://docs.google.com/spreadsheets/d/12BweSMPcNlnrSGqC3ojNCwSVIUX4ckU7uN0zJ7W_8AQ/edit?usp=sharing')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'учебники':
        keyboard.add_button('1 курс', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('2 курс', color = VkKeyboardColor.POSITIVE)

    elif response == '1 курс':
        keyboard.add_button('Мат. анализ', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Алгебра', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Дискр. мат', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Wolfram Mathematica', color = VkKeyboardColor.PRIMARY)
        keyboard.add_openlink_button('Python', 'https://drive.google.com/drive/folders/1gZ5SsNq9-9eVDHBjnu0E0WRly2Xgq4kW')
        keyboard.add_line()
        keyboard.add_button('Английский', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == '2 курс':
        keyboard.add_button('Мат. анализ', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Диффуры', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_openlink_button('Python', 'https://yadi.sk/d/GyZhNPZfU41Znw?w=1')
        keyboard.add_line()
        keyboard.add_button('Английский', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'диффуры':
        keyboard.add_openlink_button('Филиппов (задачник)', 'https://drive.google.com/file/d/1vgoG9860XxwyUYgHbn77qeij3EDUUhYM/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Филиппов (учебник)', 'https://drive.google.com/file/d/1w14id9t4uAoY43H8ofqCHAHI0rQsKrPH/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Самойленко', 'https://drive.google.com/file/d/1lxTncQv4LBv_XVblqR-xl7-kSuPG6Nu_/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'английский':
        keyboard.add_openlink_button('Market Leader', 'https://drive.google.com/file/d/1erhO4mlomjMJmNBiesKzbUBTxhnpZhyt/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Facilitator', 'https://drive.google.com/file/d/1W--_OH5gCdeKtTpdRbrfComGIW47xhHA/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Practical Grammar Course', 'https://drive.google.com/file/d/18K5DeIlanen5FK81GBQNJ9T2Pt-w5kTd/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'wolfram mathematica':
        keyboard.add_openlink_button('Фридман, Леора', 'https://drive.google.com/file/d/1xg9g1LAuw-jIH6HwH9e-UE_GU9bq8Kri/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('S. Wolfram "Wolfram Language"', 'https://www.wolfram.com/language/elementary-introduction/2nd-ed/index.html')
        keyboard.add_line()
        keyboard.add_openlink_button('Help', 'https://reference.wolfram.com/language/')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'мат. анализ':
        keyboard.add_openlink_button('Демидович (задачник)', 'https://drive.google.com/file/d/1VnHhcsfAlVg48nsYXWdXfNZiVkakamv-/view')
        keyboard.add_line()
        keyboard.add_openlink_button('Виноградов, Громов', 'https://drive.google.com/file/d/1WgfLnZ2DOyz7d0rW34cBfzY_A4Ew5-_T/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Фихтенгольц', 'https://drive.google.com/file/d/1pZ3DSjtPLJMmk12mP3e-kcW9QIez4_dq/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Конспект (1 курс 2 сем.)', 'https://drive.google.com/file/d/1AB5NmJGMzNU8HWodGXJfld0ycp9bQncR/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'алгебра':
        keyboard.add_openlink_button('Икрамов', 'https://drive.google.com/file/d/1KxIrUV3yGT_IKzz2X52JW6x1mUmoqP7C/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Воеводин', 'https://drive.google.com/file/d/1KxIrUV3yGT_IKzz2X52JW6x1mUmoqP7C/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Курош', 'https://drive.google.com/file/d/1ylNm8CkkiKSu27dJMEx0PcDKQWrjZjmA/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Фадеев', 'https://drive.google.com/file/d/1Dvui_BDw4EA-3eh5A0EYNyzcCjamPCYK/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'дискр. мат':
        keyboard.add_openlink_button('Иванов, Фридман', 'https://drive.google.com/file/d/1_dAhc25iIYUQ-S877zowmfzYt07kN9gZ/view?usp=sharing')
        keyboard.add_line()
        keyboard.add_openlink_button('Корте, Фиген "Комбинаторная оптимизация"', 'https://drive.google.com/file/d/1kOZcitXuRBTKX0pgpXC8FEPenW4rjz6y/view')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'полезные ссылки':
        keyboard.add_openlink_button('Мат. анализ', 'https://us02web.zoom.us/j/86270022069?pwd=ZndYYjhFVlJvTGlGNkVteHBTVkx6QT09')
        keyboard.add_line()
        keyboard.add_openlink_button('Диффуры', 'https://zoom.us/j/97568214849')
        keyboard.add_line()
        keyboard.add_openlink_button('БРС', 'http://www.rating.unecon.ru/')
        keyboard.add_line()
        keyboard.add_openlink_button('Moodle', 'https://student.unecon.ru/')
        keyboard.add_line()
        keyboard.add_button('Назад', color = VkKeyboardColor.NEGATIVE)

    elif response == 'на месяц':
        keyboard.add_button('Январь', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Февраль', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Март', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Апрель', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Май', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Июнь', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Июль', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Август', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Сентябрь', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Октябрь', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Ноябрь', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Декабрь', color = VkKeyboardColor.PRIMARY)

    else:
        keyboard.add_button('Привет', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Пока', color = VkKeyboardColor.DEFAULT)
        keyboard.add_button('Уровень', color = VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        
        keyboard.add_button('Журналы', color = VkKeyboardColor.POSITIVE)
        keyboard.add_button('Учебники', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Дедлайны', color = VkKeyboardColor.NEGATIVE)
        keyboard.add_line()

        keyboard.add_button('Дни Рождения', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Почты', color = VkKeyboardColor.PRIMARY)
        keyboard.add_button('Полезные ссылки', color = VkKeyboardColor.POSITIVE)
        keyboard.add_line()

        keyboard.add_button('Кнопка на случай, если устал учиться', color = VkKeyboardColor.PRIMARY)


    keyboard = keyboard.get_keyboard()
    return keyboard
