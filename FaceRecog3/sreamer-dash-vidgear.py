import datetime

from vidgear.gears import StreamGear
import cv2
import psycopg2
import time
import numpy as np
import os

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


if __name__ == '__main__':
    connection = psycopg2.connect(user="personauser", password="pgpwd4persona", host="127.0.0.1", port="5432",
                                  database="personadb")
    cursor = connection.cursor()
    sql_delete_query = "Delete from public.z1frame"
    cursor.execute(sql_delete_query)
    connection.commit()
    sql_delete_query = "Delete from public.z2frame"
    cursor.execute(sql_delete_query)
    connection.commit()
    dashpath = "./nginx/content/dash/"
    # dashpath = "./static/dash_out.mpd"
    # add various streams with custom Video Encoder and optimizations
    # define various streams
    # {"-resolution": "1280x720", "-framerate": 10.0},  # Stream2: 1280x720 at 30fps framerate
    # {"-resolution": "640x360", "-framerate": 10.0},  # Stream3: 640x360 at 60fps framerate
    # {"-resolution": "990x540", "-video_bitrate": "4096k"},  # Stream3: 320x240 at 500kbs bitrate

    stream_params = {"-input_framerate": 10, "-livestream": True}
    # stream_params = {"-input_framerate": 10,"-vcodec":"libx264", "-livestream": True}
    # stream_params = {"-input_framerate": 10,"-vcodec":"libx264"}
    # stream_params = {"-input_framerate": 10}
    # stream_params = {"-input_framerate": 10, "-livestream": True, "-window_size":5, "-gop": 70}
    # stream_params = {"-resolution": "990x540", "-livestream": True}
    filelist = [f for f in os.listdir(dashpath)]
    for f in filelist:
        os.remove(os.path.join(dashpath, f))
    dashpath += "dash_out.mpd"

    streamer = StreamGear(output=dashpath, **stream_params)
    # streamer = StreamGear(output=dashpath, custom_ffmpeg='D:/ffmpeg/bin/ffmpeg.exe', logging=False, **stream_params)
    # streamer = StreamGear(output=dashpath)
    # loop over
    while True:

        # read frames from stream
        # frame = stream.read()
        frame = fromPG(connection)
        # check for frame if Nonetype
        if frame is None:
            break
        # {do something with the frame here}
        # send frame to streamer
        if len(frame) > 1:
            streamer.stream(frame)
            # Show output window
        #     cv2.imshow("Output Frame", frame)
        #
        # # check for 'q' key if pressed
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break

    # # close output window
    # cv2.destroyAllWindows()

    # safely close streamer
    streamer.terminate()
