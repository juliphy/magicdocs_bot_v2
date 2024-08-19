import requests


def get_image_link(message, bot):
    response_dict = message.json
    photo_array = response_dict.get('photo')
    photo_dict = photo_array[1]
    file_id = photo_dict.get('file_id')

    link = bot.get_file_url(file_id)

    x = requests.post('https://api.imgbb.com/1/upload?key=d2f5768f8798f57a63d32ddd6a4e9f8e&image=' + link)
    response = x.json()

    url = response['data']['url']

    return url
