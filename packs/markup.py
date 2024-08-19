from telebot.util import quick_markup
from values import client_url
from telebot.types import ReplyKeyboardMarkup
from .check import is_login_allowed


class Markup:
    def __init__(self, type, info):
        match type:
            case "start":
                if info:
                    startList = {
                        "ℹ️Інформація о профілі": {"callback_data": "info"},
                        "✏️Змінити дане в профілі": {"callback_data": "settings"},
                        "✅Ввійти в профіль": {"url": client_url},
                        "❌Видалити профіль": {"callback_data": "delete"},
                    }

                    if not is_login_allowed():
                        del startList['✅Ввійти в профіль']

                    markup = quick_markup(startList, row_width=1)
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
