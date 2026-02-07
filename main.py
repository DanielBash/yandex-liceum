import requests
import sys
from io import BytesIO

import requests
from PIL import Image


geocoder_apikey = "8013b162-6b42-4997-9691-77b7074026e0"
static_apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
org_apikey = "72e09cfa-9163-4f5c-ba75-916fb947567b"


def get_static(api=static_apikey, ll='37.677751,55.757718', spn="0.016457,0.00619"):
    return requests.get("https://static-maps.yandex.ru/v1", params={
        'apikey': api,
        'll': ll,
        'spn': spn})


def get_geocoder(location='Красная пл-дь, 1', api=geocoder_apikey, formating='json'):
    return requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        'apikey': api,
        'format': formating,
        'geocode': location
    })

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "apikey": apikey,

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()