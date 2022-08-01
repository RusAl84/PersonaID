import datetime
import psycopg2
import time
import psycopg2
import uvicorn, asyncio, cv2
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer

# initialize WebGear app without any source
web = WebGear(logging=True)

def fromPG(connection):
    cursor = connection.cursor()
    # data = r.zrange("z1frame", 0, -1)
    postgreSQL_select_Query = "SELECT * FROM public.z2frame ORDER BY milliseconds ASC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
        frame = datarecord[1]
        milliseconds = datarecord[2]
        timestr = datarecord[3]
        cmilliseconds = int(time.time() * 1000)
        # if abs(milliseconds - cmilliseconds) > 5000:
        #     sql_delete_query = "Delete from public.z1frame"
        # else:
        #     sql_delete_query = "Delete from public.z1frame where id = " + str(id)
        sql_delete_query = "Delete from public.z2frame where id = " + str(id)
        cursor.execute(sql_delete_query)
        connection.commit()
        # dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        # now = datetime.datetime.now()
        # print(str(dt.time()) + " " + str(now))
        img = bytearray(frame)
    return img

# create your own custom frame producer
async def my_frame_producer():
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    sql_delete_query = "Delete from public.z1frame"
    cursor.execute(sql_delete_query)
    connection.commit()
    time.sleep(0.5)
    while True:
        encodedImage = fromPG(connection)
        if encodedImage:
            # encodedImage = cv2.resize(encodedImage, (960, 540))
            yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
            await asyncio.sleep(0)
    stream.release()

web.config["generator"] = my_frame_producer
uvicorn.run(web(), host="localhost", port=8008)
web.shutdown()