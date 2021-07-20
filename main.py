from fastapi import Body, FastAPI, File, UploadFile, Request
from pydantic import BaseModel
from typing import List
import base64
from io import BytesIO
import predict
import json
from PIL import  Image
import io
app = FastAPI()

import re

import six
import uuid
import imghdr


def get_file_extension(file_name, decoded_file):
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension
def decode_base64_file(data):
    """
    Fuction to convert base 64 to readable IO bytes and auto-generate file name with extension
    :param data: base64 file input
    :return: tuple containing IO bytes file and filename
    """
    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension,)

        return io.BytesIO(decoded_file), complete_file_name


class Item(BaseModel):
    ID: str
    img_code: str

class MyInput(BaseModel):
    photos: List[Item]


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/catordog")
async def catordog(photos: MyInput):
    # data = request.get_json(force=True)
    # image = BytesIO(requests.get(data['url']).content)
    # image = BytesIO(file)
    # output = predict.predict(image)
    # return data
    items = photos.photos
    res = []
    # print("SUKA")
    for item in items:

        ID = item.ID
        img_code = item.img_code
        data = base64.decodebytes(img_code.encode())
        image = Image.open(BytesIO(data))

        output = predict.predict(image)
        output['ID'] = ID
        res.append(output)
    return res

class ConjuntoDeProcessos(BaseModel):
    # campos a serem recebidos
    npus: list
    # adicione aqui novos campos a serem recebidos


@app.post("/dados_de_processos/")
def dados_de_processos(conjunto: ConjuntoDeProcessos = Body(
        ...,
        example={
            "npus": [ "0001647-60.2019.8.17.8232",
                      "0819166-41.2019.8.15.2001",
                      "0000000-00.2013.8.15.2001",
                      "0000000-00.2013.8.15.2001",
                      "0000000-00.2013.8.15.2001",
                      "0000000-00.2013.8.15.2001",
                      "0000000-00.2013.8.15.2001",
                      "0000000-03.2010.8.15.0601",
                      "0000000-03.2014.5.23.0026",
                      "0000000-03.2014.5.23.0026" ]
        },
    )):
    
    return {"processos":conjunto}
