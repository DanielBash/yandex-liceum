import math
import sys
import requests
from mapapi_Arc import show_map
from geocode import get_coordinates
import yandexapi

geocoder_apikey = "8013b162-6b42-4997-9691-77b7074026e0"
static_apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
org_apikey = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


def long_distance(a, b):
    zoom = 111 * 1000

    a_lon, a_lat = a
    b_lon, b_lat = b

    radians = math.radians((a_lat + b_lat) / 2)
    factor = math.cos(radians)

    dx = abs(a_lon - b_lon) * zoom * factor
    dy = abs(a_lat - b_lat) * zoom

    return math.sqrt(dx * dx + dy * dy)


def find_business_osnova(ll, request, locale='ru_RU'):
    return requests.get("https://search-maps.yandex.ru/v1/", params={
        'apikey': org_apikey,
        'll': ll,
        "lang": locale,
        "text": request,
        'type': 'biz'
    }).json()['features']


def find_business(ll, request, locale='ru_RU'):
    orgs = find_business_osnova(ll, request, locale)
    if len(orgs):
        return orgs[0]


toponim_to_find = ' '.join(sys.argv[1:])
lat, long = get_coordinates(toponim_to_find)
address_ll = f'{lat},{long}'
span = "0.005,0.005"
organizations = find_business(address_ll, 'аптека')
point = organizations['geometry']['coordinates']
org_lat = float(point[0])
org_lon = float(point[1])
point_param = f'pt={org_lat},{org_lon},pm2dgl'
point_param = point_param + f'~{address_ll},pm2rdl'
name = organizations['properties']['CompanyMetaData']['name']
address = organizations['properties']['CompanyMetaData']['address']
time = organizations['properties']['CompanyMetaData']['Hours']['text']
distance = round(long_distance((lat, long), (org_lat, org_lon)))
print(f'''Название: {name}
Адрес:  {address}
Время работы:   {time}
Расстояние: {distance} м.
''')

show_map('', add_params=point_param)