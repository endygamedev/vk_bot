# работа с GoogleDocs
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# данные для GoogleDrive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('data/client_secret.json', scope)
client = gspread.authorize(creds)


def update_deadlines(client) -> str:
    ''' Обновляет данные из Google-таблицы и формирует сообщение.

        Аргументы:
            client - аккаунт бота для входа в Google-таблицы

        Возвращает:
            str - строку (список) с дедлайнами
    '''


    sheet = client.open('DeadlinesTable').sheet1    # открываем таблицу

    deadline_table = sheet.get_all_records()        # забираем оттуда все записи

    all_deadlines = list(map(lambda x: list(x.values()), deadline_table))   # забираем все значения
    str_rows = [list(map(str, row)) for row in all_deadlines]               # конвертируем все элементы в таблице в stк

    format_deadlines = []   # форматируем данные, чтобы всё было по красоте
    for row in str_rows:
        row[0] += ')'
        row[1] += ':'
        row[2] += ', Дедлайн до:'
        format_deadlines.append(row)

    finally_deadlines = list(map(lambda x: ' '.join(x), format_deadlines))  # формируем список списков в простой список с отформтированными дедлайнами
    deadlines = '\n'.join(finally_deadlines)                                # выводим наши отформатированные и готовенькие дедлайны

    return deadlines
