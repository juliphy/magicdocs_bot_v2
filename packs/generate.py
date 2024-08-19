import string
import random
from .db import create_user

from values import User
from telebot import formatting
from .markup import Markup
from .get_link import get_image_link


def process_name_step(message, bot):
    try:
        print('PROCESS NAME STEP BEGIN')
        user = User()
        user.name = message.text
        firstname_array = user.name.split()

        msg = bot.reply_to(message, 'Напиши желаемую дату рождения в формате ДД.ММ.ГГГГ')
        bot.register_next_step_handler(msg, process_age_step, bot, user)

    except Exception as e:
        bot.reply_to(message, 'Sorry... Something went wrong.')


def process_age_step(message, bot, user):
    try:
        user.birthdate = message.text

        firstname_array = user.name.split()
        user.firstname = firstname_array[1]

        msg = bot.send_message(message.chat.id, 'Ваше фото 3X4')

        bot.register_next_step_handler(msg, process_face_image_step, bot, user)
    except Exception as err:
        bot.send_message(message.chat.id, "Помилка в данних. Спробуйте ще раз через /start")



def process_face_image_step(message, bot, user):
    # try:
        user.url_face = get_image_link(message, bot)

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits

        all = lower + upper + num
        user.url_sign = "null"

        sss = "".join(random.sample(all, 12))
        user.id = sss
        user.kpp_id = "".join(random.sample(num, 10))
        user.chatID = message.chat.id
        user.passport_id = "".join(random.sample(num, 9))

        user.isBlocked = False
        user.isAdmin = False
        user.username = message.chat.username

        create_user(user.json(), bot)

        bot.send_message(message.chat.id,
                         'Имя: ' + user.name + '\nДата: ' + user.birthdate + '\nID: ' + formatting.hcode(sss))
        bot.send_message(message.chat.id, 'Start', reply_markup=Markup('start', True).markup)

    # except Exception as e:
    #     print(e, 'ERROR')
