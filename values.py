import datetime
# Не трогати це!
length = 12 # Розмір ID
users = {}

class User:
    def __init__(self):
        self.name = None
        self.birthdate = None
        self.firstname = None
        self.url_face = None
        self.url_sign = None
        self.id = None
        self.passport_id = None
        self.chatID = None
        self.kpp_id = None
        self.isAdmin = None
        self.isBlocked = None
        self.username = None


    def json(self):

        info = {
            "name":self.name,
            "birthdate": self.birthdate, 
            "firstname": self.firstname
        }

        img = {
            "urlFace": self.url_face,
            "urlSign": self.url_sign
        }

        details = {
            "passport_id": self.passport_id,
            "kpp_id": self.kpp_id,
        }

        status = {
            "isAdmin": self.isAdmin,
            "isBlocked": self.isBlocked,
            "isLimited": True,
            "unlimit_end": datetime.datetime.today()
        }

        return {
            "username": self.username,
            "chatID": self.chatID,
            "id": self.id,
            "info": info,
            "img": img,
            "details": details,
            "status": status
        }


# Можна трогати це!
token = "7217985516:AAE3k-mTsXVlHd3Mc3gQZDntP6L19opZNlU"
img_api_key = "d2f5768f8798f57a63d32ddd6a4e9f8e"
server_url = 'https://xnet-server.onrender.com' # IP чи URL-адреса вашого xnet-server
client_url = 'https://juliphy.github.io/magicdocs_frontend' # URL-адреса вашого project-x



