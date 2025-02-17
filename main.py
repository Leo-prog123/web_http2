import requests
from io import BytesIO
from PIL import Image
import sys
from geocoder import get_coordinates, get_organization

# toponym_to_find = ' '.join(sys.argv[1:])
toponym_to_find = 'Тольятти Приморский бульвар, 40'
lan, lon = get_coordinates(toponym_to_find)
address_ll = f"{lon},{lan}"
spn = "0.005,0.005"
organization = get_organization(address_ll, spn, 'аптека')
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
delta = "0.005"
apikey = "f5e8d0d9-e8bf-40fb-8f03-b0f301319c2a"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "apikey": apikey,
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl".format(org_point)
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()

org_time = organization["properties"]["CompanyMetaData"]['Hours']
snippet = (f"Название:\t{org_name}\nАдрес:\t{org_address}\nВремя работы:\t{org_time}")
print(snippet)