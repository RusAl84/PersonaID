import time
import psycopg2
from pygame import mixer
import zdata as zd
import os.path

global delta
global PlayTime
photopath = ".\\photo\\"

def playSound(filename):
    if os.path.exists(filename):
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
        mixer.music.set_volume(1)
        while mixer.music.get_busy():
            time.sleep(1)
    elif os.path.exists("./all.mp3"):
        mixer.init()
        mixer.music.load("./all.mp3")
        mixer.music.play()
        mixer.music.set_volume(1)
        while mixer.music.get_busy():
            time.sleep(1)


def updateSound(connection, name_id, delta):
    cursor = connection.cursor()
    postgreSQL_select_Query = f"SELECT * FROM public.zdash WHERE name_id = {name_id} and milliseconds < {delta} ORDER BY milliseconds DESC LIMIT 1;"

    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    if datarecord:
        face_id = datarecord[0]
        id = datarecord[0]
        milliseconds = datarecord[1]
        timestr = datarecord[2]
        photo = datarecord[3]
        name = datarecord[4]
        capture = datarecord[5]
        name_id = datarecord[6]
        return milliseconds
    else:
        return 0


def getCountFaceID(connection, name_id, cmilliseconds):
    cursor = connection.cursor()
    postgreSQL_select_Query = f"SELECT count(*) FROM public.zdash WHERE name_id = {name_id} and milliseconds > {cmilliseconds};"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    if datarecord:
        count = datarecord[0]
        return count
    else:
        return 0


if __name__ == "__main__":
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    connection.autocommit = True
    global PlayTime
    PlayTime = {}
    global delta
    # задержка звука
    delta = 1000 * 30
    emb = zd.getEmb()
    num = 0
    cMilliseconds = int(time.time() * 1000)
    for item in emb:
        PlayTime[num] = cMilliseconds
        num += 1
    # full_path = os.path.realpath(__file__)
    # path, filename = os.path.split(full_path)

    while True:
        for key, value in PlayTime.items():
            cMilliseconds = int(time.time() * 1000)
            uMilliseconds = updateSound(connection, key, cMilliseconds)
            time.sleep(0.01)
            # print(f"u={uMilliseconds - value}")
            if (uMilliseconds - value) > delta:
                # PlayTime[num]
                if (cMilliseconds - value) > delta:
                    countFaceID = getCountFaceID(connection, key, cMilliseconds - delta)
                    if countFaceID > 1:
                        PlayTime[key] = uMilliseconds
                        if not ("sound" in emb[key]):
                            filename = ""
                        else:
                            str1=emb[key]['sound']
                            if len(str1) > 0:
                                filename = photopath + emb[key]['sound']
                            else:
                                filename = ""
                        print(f"{emb[key]['name']} {filename} {int((cMilliseconds - value) / 1000)} countFaceID={countFaceID}")
                        playSound(filename)
        time.sleep(0.5)
        if zd.checkNew():
            zd.addEmb()
            emb = zd.getEmb()
    connection.commit()
    connection.close()
