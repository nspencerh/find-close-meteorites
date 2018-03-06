import math
import requests

def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2) ** 2 + \
        math.cos(lat1) * \
        math.cos(lat2) * \
        math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

# Para obtener el atributo 'distance' dentro del diccionario
# de cada elemento de la lista. Si no tiene elemento 'distance', se le asigna
# un valor grande con math.inf para que no aparesca en los primeros resultados
def get_dist(meteor):
    return meteor.get('distance', math.inf)

my_loc = (29.4244122, -98.493628)

#Con la libreria request se va a buscar con get y devuelve un string (meteor_resp)
meteor_resp = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
#se transforma estos datos a formato json. Ahora meteor_data es una lista (list)
#donde cada elemento posee los atributos de un meteorito
meteor_data = meteor_resp.json()

# se realiza un for donde por cada meteor en la lista, si existen los atributos
# reclat y reclong dentro del diccionario dentro de cada elemento de la lista,
# se agrega el elemento 'distance' dentro del diccionario que se calcula entre
# la tupla my_loc y la coordenada de cada meteorito
for meteor in meteor_data:
    if not ('reclat' in meteor and 'reclong' in meteor): continue
    meteor['distance'] = calc_dist(my_loc[0], my_loc[1], float(meteor['reclat']), float(meteor['reclong']))

# se ordenan los elementos de la lista meteor_data. Se pasa una funcion (get_dist)
# para ordenar los elementos por el atributo 'distance'.
meteor_data.sort(key=get_dist)

# se imprimen los primeros 10 elementos que representan los meteoritos mas
# cerca a my_loc
print(meteor_data[0:10])
