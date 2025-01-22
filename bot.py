import telebot
import bot_config
import subprocess
import os
from transliterate import translit
import time
import datetime
import shutil

API_key=bot_config.API_key
passwd=bot_config.passwd
# example bot_config.py
# API_key = "5982175377:XXXXXX"
# passwd="1234"



default_message = """/del - очистить текущие данные
/reset - перезагрузить Персону
"""
newpath = "\\new\\"


bot = telebot.TeleBot(API_key)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if len(str(message.text))>3:
        if str(message.text).lower() == "/del":
            os.remove("image.jpg")
            bot.send_message(message.from_user.id, "Данные сброшены")
        elif str(message.text).lower() == "/reset":
            subprocess.run(["python", "./zdata.py"])
            bot.send_message(message.from_user.id, "Персона перезагружена")
        elif str(message.text).startswith(passwd):
            lines = str(message.text).split('\n')
            name = lines[1]
            decr = lines[2]
            filename = "image.jpg"
            folder_name = translit(name, 'ru',reversed=True)
            milliseconds = int(time.time() * 1000)
            dt = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
            dt = str(dt).replace(":","_").replace(".", "_")
            dt = "".join(dt.split())
            folder_name = "".join(folder_name.split())
            new_dir_name=f"{newpath+folder_name}_{dt}"
            dir = os.path.dirname(os.path.abspath(__file__))
            print("dir  "+dir)
            print("os.mkdir  "+dir+new_dir_name)
            os.mkdir(dir+new_dir_name)
            print("with open  "+f"{dir+new_dir_name}\\data.txt")
            print(f"dir+\\image.jpg    " +dir+"\\image.jpg")
            print(f"dir+new_dir_name  {dir+new_dir_name}")
            shutil.copy(dir+"\\image.jpg", dir+new_dir_name)
            newfilename=dir+new_dir_name+"\\f_"+folder_name+f"{dt}.jpg"
            os.rename(dir+new_dir_name+"\\image.jpg", newfilename)
            with open(f"{dir+new_dir_name}\\data.txt", "w", encoding="utf-8") as file:
                file.write(f"{name}\n")
                file.write(f"{decr}\n")
                file.write("f_"+folder_name+f"{dt}.jpg\n")
            bot.send_message(message.from_user.id, "Новые данные добавлены в персону")
        else:
            mess=""
            if os.path.exists("image.jpg"):
                mess="ФОТО загружено"
            bot.send_message(message.from_user.id, f"{default_message} \n {mess}")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, "Фото загружено")

if __name__ == "__main__":
    try:
        os.remove("image.jpg")
    except:
        pass
    bot.polling(none_stop=True, interval=0)