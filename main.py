"""
steal my api keys, they were granted for free by yandex,
and requested to publish them in a repo. So fuck them
"""

import requests
import sys
from io import BytesIO
from PIL import Image
from yandexapi import *


toponym_to_find = " ".join(sys.argv[1:])
response = get_geocoder(location=toponym_to_find)

if not response:
    print('Ошибка сервера')
    exit(1)


long, lat, delta = get_location(response.json())

response = get_static(ll=",".join([long, lat]),
                      spn=",".join([delta, delta]),
                      pt=",".join([long, lat]))
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
