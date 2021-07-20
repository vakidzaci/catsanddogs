import os
import requests
import json

os.environ['NO_PROXY'] = '127.0.0.1'
# r = requests.get('http://127.0.0.1:5000')
# print(r.content)

import base64

import os
from os.path import join

path = "../dogs-vs-cats/train"
paths = os.listdir(path)
paths = paths[:10]
items = []
for i in range(2):
    with open(join(path,paths[i]), "rb") as image_file:
        image_64_encode = base64.encodebytes(image_file.read())


    image_64_encode = image_64_encode.decode("utf-8")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


    item = {"img_code":image_64_encode,"ID":paths[i]}
    items.append(item)

data = {}
data['photos'] = items
r = requests.post('http://localhost:8000/catordog', headers = headers, json=data)
json_data = json.loads(r.content)
for j in json_data:
    print(j)