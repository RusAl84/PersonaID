import json
import os


def load(filename="./photo/zdata.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        jsonstring = file.read()
    zdata = []
    zdata = json.loads(jsonstring)
    return zdata


if __name__ == '__main__':
    zdata = load()
    print(zdata[4]['name'])
