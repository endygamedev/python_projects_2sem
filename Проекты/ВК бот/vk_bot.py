# VK API
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# Доп. модули
import random
import datetime
import requests
from bs4 import BeautifulSoup
from epiweeks import Week
import json

# Работа с GoogleDocs
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

# Токен нашей группы
_TOKEN = '3d423eb8812629fc6834d96bd0b5352f75f83f7691f828ca84ac57b909bf2ff519f438bc6aa4d9316cc03'

vk = vk_api.VkApi(token=_TOKEN)

# Эмоджи
_EMOJIS = ['👻 ','🤡 ','🤓 ','😁 ','😏 ','😛 ','👋 ']

# Команды
_COMMANDS = {
             'привет': 'random.choice(_EMOJIS)+random.choice(greetings_list[25:-40])',
             'пока': 'random.choice(_EMOJIS)+random.choice(goodbye_list)',
             'расписание': 'weekNumber',
             'команды': "🔧 Команды:\n• привет\n• пока\n• расписание\n• дедлайны\n• почта\n• уровень\n• команды",
             'дедлайны': 'update_deadlines(client)',
             'почта': "📬Логин: appliedmath1900@yahoo.com\n🔒Пароль: PMstudents1900",
             'уровень': 'history_messages(session.user_id)'
             }

commands_list = list(_COMMANDS.keys())
messages_list = list(_COMMANDS.values())

# Фоточки
_PICTURES = ['level.png','bye1.png','bye2.png','bye3.png','bye4.png','hello1.png','hello2.png','hello3.png','hello4.png','hello5.png','hello6.png','hello7.png']

# Расписание
with open('oddWeek.txt', 'r', encoding="utf-8") as file_odd, open('evenWeek.txt', 'r', encoding="utf-8") as file_even:
    oddWeek = file_odd.read()
    evenWeek = file_even.read()

# Определяет текущую неделю, мы выявили опытным путём, что начало недель датируется 13.8.2019
weekNumber = Week.fromdate(datetime.date(2019,8,10)).weektuple()[-1]


# Метод для отправки сообщения
def write_message(user_id, message):
    '''
    write_message(user_id, message) - отправка текстового сообщения с текстом message.
    '''
    vk.method('messages.send', {
    'user_id': user_id,
    'message': message,
    'random_id': random.getrandbits(31) * random.choice([-1, 1])
    })

# Метод для отправки сообщения с картинкой
def send_photo(user_id, message, picture):
    '''
    send_photo(user_id, message, picture) - отправка сообщения сообщения с текстом message и с картинкой picture.
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
def history_messages(user_id):
    '''
    history_messages(user_id) - кол-во сообщений от пользователя и определение его уровня.
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
    81 <= count_messages <= 200: f'👨‍💻 Уровень 3.\nВы больше не мальенький поганец, вы большой поганец!\nКоличество собщений: {count_messages}',
    count_messages >= 201: f'🏅 Уровень 4.\nВам ещё не выдали Нобелевскую премию?\nКоличество собщений: {count_messages}'
    }[1]


# Данные для GoogleDrive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Метод для отправки сообщения с картинкой
def update_deadlines(client):
    '''
    update_deadlines(client) - обновление данных гугл таблице и формирование читаемого сообщения.
    '''
    sheet = client.open('DeadlinesTable').sheet1 # открываем таблицу

    deadline_table = sheet.get_all_records() # забираем оттуда все записи

    all_deadlines = list(map(lambda x: list(x.values()), deadline_table)) # забираем все значения
    str_rows = [list(map(str, row)) for row in all_deadlines] # конвертируем все элеементы в таблице в string

    format_deadlines = [] # Форматируем данные, чтобы всё было по красоте
    for row in str_rows:
        row[0]+=')'
        row[1]+=':'
        row[2]+=', Дедлайн до:'
        format_deadlines.append(row)

    finally_deadlines = list(map(lambda x: ' '.join(x), format_deadlines)) # формируем список списков в простой список с отформтированными дедлайнами
    deadlines = '\n'.join(finally_deadlines) # выводим наши отформатированные и готовенькие дедлайны
    return deadlines

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

# Очищаем все кодировки
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


longpoll = VkLongPoll(vk)

for session in longpoll.listen():
    if session.type == VkEventType.MESSAGE_NEW:
        if session.to_me:
            user_message = session.text

            if user_message.lower() == commands_list[0]: # привет
                send_photo(session.user_id, random.choice(_EMOJIS)+random.choice(greetings_list[25:-40]), random.choice(_PICTURES[5:13]))

            elif user_message.lower() == commands_list[1]: # пока
                send_photo(session.user_id, random.choice(_EMOJIS)+random.choice(goodbye_list),random.choice(_PICTURES[1:5]))

            elif user_message.lower() == commands_list[2]: # расписание
                if weekNumber%2 == 0:
                    write_message(session.user_id, evenWeek)
                else:
                    write_message(session.user_id, oddWeek)

            elif user_message.lower() == commands_list[3]: # команды
                write_message(session.user_id, messages_list[3])

            elif user_message.lower() == commands_list[4]: # дедланы
                write_message(session.user_id, update_deadlines(client))

            elif user_message.lower() == commands_list[5]: # почта
                write_message(session.user_id, messages_list[5])

            elif user_message.lower() == commands_list[6]: # добавляем кол-во сообщений в переписке
                send_photo(session.user_id, history_messages(session.user_id), _PICTURES[0])


            elif user_message.lower() == "клавиатура" or user_message.lower() == "начать": # обновляем клавиатуру
                vk.method("messages.send", {
                            "user_id": session.user_id,
                            "message": "⌨ Используй клавиатуру для общения со мной",
                            "random_id": random.getrandbits(31) * random.choice([-1, 1]),
                            "keyboard": keyboard
                            })

            else:
                write_message(session.user_id, "Я тупой бот и не понимаю вашего человеческого языка...\n\n" + messages_list[3])
