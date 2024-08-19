from telebot import TeleBot

from values import *
from packs.generate import process_name_step
from packs.markup import Markup
from packs.db import exist_user
from packs.check import  is_admin, is_signup_allowed
from packs.admin import AdminMarkup
from packs.callback import process_callback
from telebot.types import ReplyKeyboardRemove

bot = TeleBot(token, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start_handler(message):
    if not is_admin(message.chat.id) and is_signup_allowed():
        bot.send_message(message.chat.id, "Start",reply_markup=Markup('start', exist_user(message.chat.id, bot)).markup)


    elif not is_signup_allowed() and not is_admin(message.chat.id) and not exist_user(message.chat.id, bot):
        bot.send_message(message.chat.id, "Вибачте! На данний момент реєстрація заблокована.", reply_markup=ReplyKeyboardRemove())


    elif not is_admin(message.chat.id) and not is_signup_allowed() and exist_user(message.chat.id, bot):
        bot.send_message(message.chat.id, "Start",reply_markup=Markup('start', True).markup)

    elif is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Start", reply_markup=AdminMarkup('start', exist_user(message.chat.id, bot)).markup)

@bot.message_handler(regexp='Зареєструватися')
def create_handler(message):
    if not is_signup_allowed():
        bot.send_message(message.chat.id, "Вибачте! На данний момент реєстрація заблокована.", reply_markup=ReplyKeyboardRemove())
        return
    else:
        if exist_user(message.chat.id, bot):
            bot.send_message(message.chat.id, 'Ви вже зареєстровані. Видаліть профіль, якщо хочете зареєструватися знову.')
            return
        else:
            msg = bot.send_message(message.chat.id, 'Введіть ваш ПІБ', reply_markup=ReplyKeyboardRemove())
            bot.register_next_step_handler(msg,process_name_step, bot) # generate.py

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call): # <- passes a CallbackQuery type object to your function
    process_callback(call,bot) # callback.py
            
            
bot.infinity_polling()
