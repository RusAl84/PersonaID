import time
import atexit
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
import zdata
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

Items = []
gdata = []

from apscheduler.schedulers.background import BackgroundScheduler


def update_items():
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    postgreSQL_select_Query = "SELECT * FROM public.zdash ORDER BY milliseconds ASC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()

    if datarecord:
        id = datarecord[0]
        milliseconds = datarecord[1]
        timestr = datarecord[2]
        photo = datarecord[3]
        name = datarecord[4]
        capture = datarecord[5]
        name_id = datarecord[6]
        sql_delete_query = "Delete from public.zdash where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        dic = {}
        dic['milliseconds'] = milliseconds
        dic['timestr'] = timestr
        dic['photo'] = photo
        dic['name'] = name
        dic['capture'] = capture
        dic['name_id'] = name_id
        print(gdata[int(name_id)]["desc"])
        Items.append(dic)
    return
    # print("updated" + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_items, trigger="interval", seconds=7)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def dafault_route():
    return 'FaceRecog '


# получение сообщений
@app.route("/dash/<int:id>")
def GetMessage(id):
    print(id)
    if id >= 0 and id < len(Items):
        print(Items[id])
        return Items[id], 200

        # //update
    else:
        return "not found", 400


@app.route('/photo/<path:path>')
def send_photo(path):
    return send_from_directory('photo', path)


@app.route('/capture/<path:path>')
def send_capture(path):
    return send_from_directory('capture', path)


if __name__ == '__main__':
    gdata = zdata.load()
    Items = []
    # Items.append(gdata[1])
    # Items.append(gdata[2])
    # Items.append(gdata[3])
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    sql_delete_query = "Delete from public.zdash"
    cursor.execute(sql_delete_query)
    connection.commit()
    app.run()
