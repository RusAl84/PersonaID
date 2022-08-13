import json
import cv2
import os
import time

# zdata = []
# item = {}
# item['filename'] = "\photo\Голованова.jpg"
# item['name'] = "Голованова Наталия Борисовна"
# item['desc'] = "Голованова Наталия Борисовна. Заместитель первого проректора."
# zdata.append(item)
# zdata.append(item)
# jsontext = str(zdata)
# print(jsontext)
#
# import os
#
# print("Path at terminal when executing this file")
# print(os.getcwd() + "\n")
#
# print("This file path, relative to os.getcwd()")
# print(__file__ + "\n")
#
# print("This file full path (following symlinks)")
# full_path = os.path.realpath(__file__)
# print(full_path + "\n")
#
# print("This file directory and name")
# path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
#
# print("This file directory only")
# print(os.path.dirname(full_path))

with open("./photo/zdata.json", 'r', encoding='utf-8') as file:
    jsonstring = file.read()
zdata = json.loads(jsonstring)
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

for item in zdata:
    img = cv2.imread(path + item['filename'])
    # img = cv2.imread(f'C:/Users/user/PycharmProjects/FaceRecog/FaceRecog4/photo/Golovanova.jpg')
    # cv2.imshow("img", img)
    # time.sleep(2)
# l=[[0, (530, 94, 59, 59), [0.8658851385116577]], [1, (90, 110, 70, 70), [0.853442907333374]]]
l = '0, (526, 85, 52, 52), [0.8178040385246277]'
import ast
l = ast.literal_eval(l)
print(l)
