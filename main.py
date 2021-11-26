import vk_api
import vk
import vk_api.bot_longpoll
from vk_api.utils import get_random_id
import random
from config import token
from data import data, DataBase


def write_msg(chat, msg, chat_id):
    if msg != False:
        if chat == 'local':
            vk.messages.send(user_id = chat_id, message = msg, random_id = get_random_id())

vk_session = vk_api.VkApi(token = token)
longpoll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, group_id=151231486)
vk = vk_session.get_api()
print('Сервер запущен')
db = DataBase('database.db')


for event in longpoll.listen():
    print(event.object)
    obj = event.message
    if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
        print(f"{obj.from_id}, {obj.text}")
        if event.from_user:
            chat_id = obj.from_id
            msg = obj.text
            if msg.lower() == "кинь пикчу":
                img = db.get_image()
                write_msg('local', img, chat_id)
            if msg.lower()  in ['нигер', 'хуй']:
                db.add_user(chat_id)
                db.alert(chat_id)
                write_msg('local', msg = 'ты гандон', chat_id = chat_id)
            elif msg != '':
                write_msg(chat = 'local', msg = msg, chat_id = chat_id)
            elif obj.attachments[0]['type'] == 'link':
                if obj.attachments[0]['link']['title'][-3:] in ['mp3', 'wav', 'ogg']:
                    write_msg(chat = 'local', msg = random.choice(data), chat_id = chat_id)
                else:
                    write_msg(chat = 'local', msg = 'Сука!!! Ты чо скинул', chat_id = chat_id)
            else:
                write_msg(chat = 'local', msg = 'ошибка!', chat_id = chat_id)
