from .db import exist_user, update_user, find_user, delete_user, ban_user
from .check import is_admin, get_settings_text, update_settings, count_users
from .markup import Markup
from telebot import formatting

from telebot.util import quick_markup
from values import client_url
from telebot.types import ReplyKeyboardMarkup


class AdminMarkup:
    def __init__(self, type, info):
        match type:
            case "start":
                if info:
                    text = {
                        "ℹ️Інформація о профілі": {"callback_data": "info"},
                        "✏️Змінити дане в профілі": {"callback_data": "settings"},
                        "✅Ввійти в профіль": {"url": client_url},
                        "❌Видалити профіль": {"callback_data": "delete"},
                        "⚜️Адмін": {"callback_data": "admin_menu"}
                    }

                    markup = quick_markup(text, row_width=1)
                    self.markup = markup
                else:
                    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                    markup.add('Зареєструватися')

                    self.markup = markup

            case "settings":
                markup = quick_markup({
                    "Змінити ПІБ": {"callback_data": "update_name"},
                    "Змінити дату": {"callback_data": "update_date"},
                    "Змінити фото": {"callback_data": "update_photo"},
                    "⬅️Назад до меню": {"callback_data": "back_start"}
                }, row_width=1)

                self.markup = markup

            case "only_back":
                markup = quick_markup({
                    "⬅️Назад до меню": {"callback_data": "back_start"}
                }, row_width=1)

                self.markup = markup
            
            case "only_back_admin":
                markup = quick_markup({
                    "⬅️Назад до Адмін меню": {"callback_data": "back_start_admin"}
                }, row_width=1)

                self.markup = markup

            case "admin_menu":
                text = get_settings_text()
                markup = quick_markup({
                    text['allowCreateText']: {"callback_data": text['actionCreateTo']},
                    text['allowLoginText']: {"callback_data": text['actionLoginTo']},
                    "Заблокувати юзера": {"callback_data": "ban"},
                    "Інформація о сервісі": {"callback_data": "info_admin"},
                    "Назад до меню": {"callback_data": "back_start"}
                }, row_width=1)

                self.markup = markup
            

def process_admin_callback(call,bot):
    message = call.message.message_id
    id = call.from_user.id

    match (call.data):
        case "settings":
            bot.edit_message_text('Settings', id, message_id=message)
            bot.edit_message_reply_markup(id, message, reply_markup=AdminMarkup('settings', True).markup)

        case "back_start":
            if exist_user(id, bot):

                bot.edit_message_text('Start', id, message_id=message)
                bot.edit_message_reply_markup(id, message, reply_markup=AdminMarkup('start', True).markup)
            else:
                bot.edit_message_text('Start', id, message_id=message)
                bot.send_message(id, 'Ви можете зареєструватися знову.', reply_markup=AdminMarkup('start', False).markup)

        case "info":
            user = find_user(id, bot)
            bot.edit_message_text("Ім'я: " + user['info']["name"] + "\nДата народження: " + user['info'][
                "birthdate"] + "\nID для входу: " + formatting.hcode(user['id']), id, message_id=message)
            bot.edit_message_reply_markup(id, message, reply_markup=Markup('only_back', exist_user(id, bot)).markup)

        case "delete":
            delete_user(id, bot)
            bot.edit_message_text(
                'Профіль видалено. Щоб знову зробити профіль, натисніть кнопку Назад або пропишіть /start.', id,
                message)
            bot.edit_message_reply_markup(id, message, reply_markup=AdminMarkup('only_back', exist_user(id, bot)).markup)

        # Admin menu processing

        case "admin_menu":
            bot.edit_message_text("Admin start", id,message)
            bot.edit_message_reply_markup(id, message, reply_markup = AdminMarkup('admin_menu', exist_user(id, bot)).markup)
        
        case "disable_create":
            update_settings("allowCreate", False)
            bot.edit_message_reply_markup(id, message, reply_markup = AdminMarkup('admin_menu', exist_user(id, bot)).markup)
        
        case "enable_create":
            update_settings("allowCreate", True)
            bot.edit_message_reply_markup(id, message, reply_markup = AdminMarkup('admin_menu', exist_user(id, bot)).markup)

        case "enable_login":
            update_settings("allowLogin", True)
            bot.edit_message_reply_markup(id, message, reply_markup = AdminMarkup('admin_menu', exist_user(id, bot)).markup)
        
        case "disable_login":
            update_settings("allowLogin", False)
            bot.edit_message_reply_markup(id, message, reply_markup = AdminMarkup('admin_menu', exist_user(id, bot)).markup)

        case "ban":
            msg = bot.send_message(id, "Напиши @username або chatID юзера, якого ти хочеш забанити. Назад, якщо не хочеш нікого банити.", reply_markup=AdminMarkup("only_back_admin", True).markup)

            bot.register_next_step_handler(msg,ban_user,bot)

        case "back_start_admin":
            bot.edit_message_text("Admin start", id, message)
            bot.edit_message_reply_markup(id, message,
                                          reply_markup=AdminMarkup('admin_menu', exist_user(id, bot)).markup)
            
        case "info_admin":
            bot.edit_message_text("Інформація о сервісі:\n\nЗареєстровано: " + str(count_users()),id,message)
            bot.edit_message_reply_markup(id, message,
                                          reply_markup=AdminMarkup('only_back_admin', exist_user(id, bot)).markup)
            

        

    if call.data.startswith('update'):
        bot.edit_message_text('Якщо ви вже не хочете змінювати, то натисніть кнопку снизу.', id, message)
        bot.edit_message_reply_markup(id, message, reply_markup=AdminMarkup('only_back', True).markup)

        if call.data.endswith('name'):
            msg = bot.send_message(id, 'Відправте бажаний ПІБ')

            bot.register_next_step_handler(msg, update_user, bot, 'name')
        elif call.data.endswith('date'):
            msg = bot.send_message(id, 'Відправте бажану дату народження')

            bot.register_next_step_handler(msg, update_user, bot, 'birthdate')

        elif call.data.endswith('photo'):
            msg = bot.send_message(id, 'Відправте бажене фото. Тільки 3x4 фото підтримуются.')

            bot.register_next_step_handler(msg, update_user, bot, 'photo')


