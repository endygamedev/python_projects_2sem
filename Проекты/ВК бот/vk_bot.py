import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
import datetime
import requests
from epiweeks import Week
import json


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

# Конструктор для кнопки
def button(label, color):
    '''
    button(label, color) - конструктор для создания кнопок
    '''
    return {
        "action": {
            "type": "text",
            "label": label
        },
        "color": color
    }

# Клавиатура
keyboard = {
    "one_time": False,
    "buttons": [
        [
        button("Привет", "positive"),
        button("Команды","default"),
        button("Пока","negative")
        ],
        [
        button("Расписание","primary"),
        ]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


# Токен нашей группы
_TOKEN = '3d423eb8812629fc6834d96bd0b5352f75f83f7691f828ca84ac57b909bf2ff519f438bc6aa4d9316cc03'

vk = vk_api.VkApi(token=_TOKEN)

# Команды
_COMMANDS = {
             'привет': "🤓 Привет-привет, человек!",
             'пока': "👋 Пока-пока, человек!",
             'расписание': "📅 Не подскажите какая неделька (чётная или нечётная)",
             'команды': "Команды:\n• привет\n• пока\n• расписание\n• команды"
             }

commands_list = list(_COMMANDS.keys())
messages_list = list(_COMMANDS.values())

# Фоточки
_PICTURES = ['goodbye.jpg','hello2.jpg','hello1.png']

# Расписание
with open('oddWeek.txt', 'r', encoding="utf-8") as file_odd, open('evenWeek.txt', 'r', encoding="utf-8") as file_even:
    oddWeek = file_odd.read()
    evenWeek = file_even.read()

# Определяет текущую неделю, мы выявили опытным путём, что начало недель датируется 13.8.2019
weekNumber = Week.fromdate(datetime.date(2019,8,13)).weektuple()[-1]


longpoll = VkLongPoll(vk)

for session in longpoll.listen():
    if session.type == VkEventType.MESSAGE_NEW:
        if session.to_me:
            user_message = session.text

            if user_message.lower() == commands_list[0]: # привет
                send_photo(session.user_id, messages_list[0], random.choice(_PICTURES[1:3]))

            elif user_message.lower() == commands_list[1]: # пока
                send_photo(session.user_id, messages_list[1], _PICTURES[0])

            elif user_message.lower() == commands_list[2]: # расписание
                if weekNumber%2 == 0:
                    write_message(session.user_id, evenWeek)
                else:
                    write_message(session.user_id, oddWeek)

            elif user_message.lower() == commands_list[3]: # команды
                write_message(session.user_id, messages_list[3])

            elif user_message.lower() == "клавиатура": # обновляем клавиатуру
                vk.method("messages.send", {
                            "user_id": session.user_id,
                            "message": "⌨",
                            "random_id": random.getrandbits(31) * random.choice([-1, 1]),
                            "keyboard": keyboard
                            })

            else:
                write_message(session.user_id, "Я тупой бот и не понимаю вашего человеческого языка...\n\n" + messages_list[3])
