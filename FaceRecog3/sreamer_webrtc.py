import uvicorn, cv2
from vidgear.gears import ScreenGear
from vidgear.gears.helper import reducer
from vidgear.gears.asyncio import WebGear_RTC
import cv2
import psycopg2
import time
import numpy as np
import os
from vidgear.gears import CamGear

# create your own custom streaming class
def fromPG(connection):
    cursor = connection.cursor()
    # data = r.zrange("z1frame", 0, -1)
    postgreSQL_select_Query = "SELECT * FROM public.z2frame ORDER BY milliseconds ASC LIMIT 1"
    cursor.execute(postgreSQL_select_Query)
    datarecord = cursor.fetchone()
    img = []
    if datarecord:
        id = datarecord[0]
        frame = []
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
        # print(str(dt.time()) + " " + str(now) + " " +timestr)
        # img = bytearray(frame)
        # img = frame
        # print(img)
        img = np.asarray(bytearray(frame), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img

class Custom_Stream_Class:
    """
    Custom Streaming using ScreenGear
    """

    def __init__(self, backend="mss", logging=False):

        # !!! define your own video source here !!!
        # self.source = CamGear(source=0, logging=True).start()
        self.source = ScreenGear(backend=backend, logging=logging)
        print(self.source)

        # define running flag
        self.running = True

        self.connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
        cursor = self.connection.cursor()
        sql_delete_query = "Delete from public.z1frame"
        cursor.execute(sql_delete_query)
        self.connection.commit()
        sql_delete_query = "Delete from public.z2frame"
        cursor.execute(sql_delete_query)
        self.connection.commit()



    def start(self):

        # don't forget this function!!!
        # This function is specific to VideoCapture APIs only

        if not self.source is None:
            self.source.start()

    def read(self):

        # don't forget this function!!!

        # check if source was initialized or not
        if self.source is None:
            return None
        # check if we're still running
        if self.running:
            # read frame from provided source
            self.source.read()

            frame = fromPG(self.connection)
            # self.source.frame = frame
            # print(frame2)
            # check if frame is available
            if not(frame is None):
                if len(frame) > 1:
                    # do something with your OpenCV frame here

                    # reducer frames size if you want more performance otherwise comment this line
                    # frame = reducer(frame, percentage=20)  # reduce frame by 20%
                    # print("vvvvvvvvvvvvvv")

                    # return our gray frame
                    return frame
            else:
                # signal we're not running now
                self.running = False
                self.running = True
                self.source.start()
        # return None-type
        return None

    def stop(self):
        if not self.source is None:
            self.source.start()
        # don't forget this function!!!
        self.running = True
        # # flag that we're not running
        # self.running = False
        # # close stream
        # if not self.source is None:
        #     self.source.stop()


# assign your Custom Streaming Class with adequate ScreenGear parameters
# to `custom_stream` attribute in options parameter
# options = {"custom_stream": Custom_Stream_Class(backend="pil", logging=True)}
options = {"custom_stream": Custom_Stream_Class(backend="pil", logging=True)}

# initialize WebGear_RTC app without any source
web = WebGear_RTC(logging=True, **options)

# run this app on Uvicorn server at address http://localhost:8000/
uvicorn.run(web(), host="localhost", port=8000)

# close app safely
web.shutdown()