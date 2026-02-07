import requests

API_KEY = '8013b162-6b42-4997-9691-77b7074026e0'


def geocode(address):
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/'
    response = requests.get(geocoder_request, params={
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    })
    if response:
        json_response = response.json()
    else:
        print(response)
        print('Failed')
        return False

    features = json_response['response']['GeoObjectCollection']['featureMember']

    return features[0]['GeoObject'] if features else None


def get_coordinates(address):
    toponim = geocode(address)

    toponim_coordinates = toponim['Point']['pos']
    toponim_longitude, toponim_lattitude = toponim_coordinates.split(' ')
    return float(toponim_longitude), float(toponim_lattitude)

