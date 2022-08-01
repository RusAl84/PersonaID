# import necessary libs
import time

import psycopg2
import uvicorn, cv2
from vidgear.gears.asyncio import WebGear_RTC
import numpy as np


# create your own custom streaming class
class Custom_Stream_Class:
    """
    Custom Streaming using OpenCV
    """

    def __init__(self, source=0):

        # !!! define your own video source here !!!
        # self.source = cv2.VideoCapture(source)
        self.source = 0

        # define running flag
        self.running = True

        self.connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                           database="personadb")

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
            # img = bytearray(frame)
            img = frame
        return img

    def read(self):

        # don't forget this function!!!

        # check if source was initialized or not
        # if self.source is None:
        #     return None
        # # check if we're still running
        # if self.running:
        #     # read frame from provided source
        #     (grabbed, frame) = self.source.read()
        #     # check if frame is available
        #     if grabbed:
        #
        #         # do something with your OpenCV frame here
        #
        #         # lets convert frame to gray for this example
        #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #
        #         # return our gray frame
        #         return gray
        #     else:
        #         # signal we're not running now
        #         self.running = False
        # return None-type
        encodedImage = self.fromPG(self.connection)
        img = np.asarray(bytearray(encodedImage), dtype="uint8")
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img

    def stop(self):

        # don't forget this function!!!

        # flag that we're not running
        self.running = False
        # close stream
        if not self.source is None:
            self.source.release()


# assign your Custom Streaming Class with adequate source (for e.g. foo.mp4)
# to `custom_stream` attribute in options parameter
options = {"custom_stream": Custom_Stream_Class(source=0)}

# initialize WebGear_RTC app without any source
web = WebGear_RTC(logging=True, **options)

# run this app on Uvicorn server at address http://localhost:8000/
uvicorn.run(web(), host="localhost", port=8000)

# close app safely
web.shutdown()
