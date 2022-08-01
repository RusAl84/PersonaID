import datetime
import time
import psycopg2
import uvicorn, asyncio, cv2
import cv2
from vidgear.gears import CamGear
from vidgear.gears import WriteGear
import numpy as np

# open any valid video stream(for e.g `foo.mp4` file)
stream = CamGear().start()

# define required FFmpeg parameters for your writer
output_params = {"-f": "rtsp", "-rtsp_transport": "tcp"}

# Define writer with defined parameters and RSTP address
# [WARNING] Change your RSTP address `rtsp://localhost:8554/mystream` with yours!
writer = WriteGear(
    output_filename="rtsp://localhost:8554/mystream", logging=True, **output_params
)


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
        dt = datetime.datetime.fromtimestamp(int(milliseconds) / 1000.0)
        now = datetime.datetime.now()
        print(str(dt.time()) + " " + str(now))
        img = bytearray(frame)
        img = frame
    return img

connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                            database="personadb")
# loop over
while True:

    # read frames from stream
    # frame = stream.read()
    frame = fromPG(connection)
    if len(frame)>1:
        frame = np.asarray(bytearray(frame), dtype="uint8")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # # check for frame if Nonetype
        # if frame is None:
        #     break

        # {do something with the frame here}

        # write frame to writer

        writer.write(frame)

# safely close video stream
stream.stop()

# safely close writer
writer.close()