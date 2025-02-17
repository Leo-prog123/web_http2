import sys

import requests
import math

def geocoder(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym
    else:
        raise RuntimeError("ошибка запросов")
    return


def get_spn(toponym_to_find):
    toponym = geocoder(toponym_to_find)
    if not toponym:
        return None, None
    toponym_coordinates = toponym["Point"]["pos"]
    lon, lan = toponym_coordinates.split(" ")
    border = toponym["boundedBy"]["Envelope"]
    left, bottom = border["lowerCorner"].split(' ')
    right, top = border["upperCorner"].split(' ')
    dx = abs(float(left) - float(right)) / 2
    dy = abs(float(top) - float(bottom)) / 2
    return dx, dy


def get_coordinates(toponym_to_find):
    toponym = geocoder(toponym_to_find)
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    lon, lan = toponym_coodrinates.split(" ")
    return float(lon), float(lan)


def get_organization(address_ll, spn, text):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": text,
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "spn": spn
    }
    response = requests.get(search_api_server, params=search_params)
    if response:
        json_response = response.json()
        print(json_response)
        # Получаем первую найденную организацию.
        organization = json_response["features"][0]
        return organization
    else:
        raise RuntimeError(response.status_code)
        sys.exit(-1)


def get_distance(a, b):
    a_lon, a_lan = a
    b_lon, b_lan = b
    factor = 111*1000
    radians_lan = math.radians((a_lan + b_lan) / 2)
    lan_lon_coeff = math.cos(radians_lan)
    dx = abs(a_lon - b_lon) * factor * lan_lon_coeff
    dy = abs(a_lan - b_lan) * factor
    distance = math.sqrt(dx**2 + dy**2)
    return distance
