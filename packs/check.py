from pymongo import MongoClient

uri = "mongodb+srv://juliphyy:l7jOBx88bEV9kvw5@cluster0.vpa0axs.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
collection = client.magicdocs.data
settings = client.magicdocs.settings


def get_settings_text():

    try:
        x = settings.find_one()

        if x["allowCreate"] == True:
            allowCreateText = "✅Регістрація увімкнена"
            actionCreateTo = "disable_create"
        else:
            allowCreateText = "❌Регістрація вимкнена"
            actionCreateTo = "enable_create"

        if x["allowLogin"] == True:
            allowLoginText = "✅Вхід дозволено"
            actionLoginTo = "disable_login"
        else:
            allowLoginText = "❌Вхід недозволений"
            actionLoginTo = "enable_login"

        return {"allowCreateText": allowCreateText, "allowLoginText": allowLoginText, "actionCreateTo": actionCreateTo,
                "actionLoginTo": actionLoginTo}
    except:
        print("Something went wrong...")


def is_signup_allowed():
    try:
        x = settings.find_one()

        return x["allowCreate"]
    except:
        print('Something went wrong...')



def is_login_allowed():
    try:
        x = settings.find_one()

        return x["allowLogin"]
    except:
        print('Something went wrong...')


def update_settings(type, value):
    value = {"$set": {type: value}}
    settings.update_one({}, value)


def is_admin(id):
    # try:
        x = collection.find_one({"chatID": id})

        if x is None:
            return False
        else:
            return x['status']['isAdmin']

        
    # except:
    #     print("Error caught in is_admin")

def count_users():
    total_count = collection.count_documents({})

    return total_count

