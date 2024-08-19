from pymongo import MongoClient
from telebot import formatting

from .markup import Markup
from .get_link import get_image_link

uri = "mongodb+srv://juliphyy:l7jOBx88bEV9kvw5@cluster0.vpa0axs.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
collection = client.magicdocs.data
settings = client.magicdocs.settings

def exist_user(id, bot):
    try:
        x = collection.find_one({"chatID": id})
        if x is not None:
            return True
        else:
            return False

    except:
        bot.send_message(id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')
        print('Error caught in exist_user')


def find_user(id, bot):
    try:
        x = collection.find_one({"chatID": id})

        if x:
            return x
        else:
            raise ValueError("ID не найден.")
    except:
        bot.send_message(id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')

def find_user_by_username(username, bot):
    try:
        x = collection.find_one({"username": username})

        if x:
            return x
        else:
            raise ValueError("ID не найден.")
    except:
        bot.send_message(id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')


def create_user(user, bot):
    try:
        collection.insert_one(user)
    except Exception as e:
        bot.send_message(user["chatID"],
                        'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')
        print(e)



def delete_user(id, bot):
    try:
        collection.delete_one({"chatID": id})
    except Exception as e:
        bot.send_message(id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')
        print(e)


def update_user(msg, bot, change_type):
    try:
        if change_type == 'name' or change_type == 'birthdate':
            collection.update_one({"chatID": int(msg.chat.id)}, {"$set": {"info." + change_type: msg.text}})

            if change_type == 'name':
                change_type = "Ім'я"
                text1 = ' було змінено на '
            else:
                change_type = "Дата народження"
                text1 = ' була змінена '

            bot.send_message(msg.chat.id, formatting.hitalic(change_type) + text1 + formatting.hbold(msg.text),
                             reply_markup=Markup('only_back', True).markup)
        else:
            image = get_image_link(msg, bot)

            collection.update_one({"chatID": int(msg.chat.id)}, {"$set": {"img.urlFace": image}})

            bot.send_message(msg.chat.id, 'Фото змінено.', reply_markup=Markup('only_back', True).markup)
    except Exception as e:
        bot.send_message(msg.chat.id,
                         'Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.')
        print("Something went wrong. chatID: " + str(msg.chat.id) + ". Error:")
        print(e)

def delete_user_by_username(username, bot):
    try:
        collection.delete_one({"username": username})
    except Exception as e:
        print(e)



def ban_user(msg,bot):
    try:
        text = msg.text

        if text[0] == "@":
            text = text[1:]

        # myquery = {"username": text}
        # newvalues = {"$set": {"status":{"isBlocked": True}}}

        # collection.update_one(myquery, newvalues)
        # a = collection.find_one({"chatID":msg.chat.id})

        # bot.send_message(msg.chat.id, "Юзер " + text + " (" + str(a['chatID']) + ") був забанен.")

        user = find_user_by_username(text,bot)
        delete_user_by_username(text,bot)

        user['status']['isBlocked'] = True

        create_user(user,bot)
    except Exception as e:
        print(e)
        bot.send_message(msg.chat.id, "Вибачте! Щось трапилось з базою данних. Спробуйте ще раз пізніше чи напишіть до підтримки.")
    

    
