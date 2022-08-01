import os, time
import datetime
import psycopg2

boundary = '--boundarydonotcross'

def request_headers():
    return {
        'Cache-Control': 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0',
        'Connection': 'close',
        'Content-Type': 'multipart/x-mixed-replace;boundary=%s' % boundary,
        'Expires': 'Mon, 1 Jan 2030 00:00:00 GMT',
        'Pragma': 'no-cache',
		'Access-Control-Allow-Origin': '*' # CORS
    }

def image_headers(lsize):
    return {
        'X-Timestamp': time.time(),
        'Content-Length': lsize,
        'Content-Type': 'image/jpeg',
    }

def image():
    connection = psycopg2.connect(user="personauser",
                                  # пароль, который указали при установке PostgreSQL
                                  password="pgpwd4persona",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    # data = r.zrange("z1frame", 0, -1)
    postgreSQL_select_Query = "SELECT * FROM public.z1frame ORDER BY milliseconds ASC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
        frame = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]
        # cmilliseconds = int(time() * 1000)
        # if abs(milliseconds - cmilliseconds) > 5000:
        #     sql_delete_query = "Delete from public.z1frame"
        # else:
        #     sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        now = datetime.datetime.now()
        print(str(dt.time()) + " " + str(now))
        img = bytearray(frame)
        # print(img)
        # img = np.asarray(bytearray(frame), dtype="uint8")
        # img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img

