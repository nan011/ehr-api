import json
from apps.v1.area.models import Province, City

with open('initial_data/area/area.json', 'r+') as f:
    data = json.loads(f.read())
    for prov in data:
        prov_e = Province.objects.create(name = prov["name"])
        for city in prov["cities"]:
            city_e = City.objects.create(name = city, province = prov_e)