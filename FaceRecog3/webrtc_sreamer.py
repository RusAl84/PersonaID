# import necessary libs
import uvicorn, cv2
from vidgear.gears import ScreenGear
from vidgear.gears.helper import reducer
from vidgear.gears.asyncio import WebGear_RTC

# create your own custom streaming class
class Custom_Stream_Class:
    """
    Custom Streaming using ScreenGear
    """

    def __init__(self, backend="mss", logging=False):

        # !!! define your own video source here !!!
        self.source = ScreenGear(backend=backend, logging=logging)

        # define running flag
        self.running = True

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
            frame = self.source.read()
            # check if frame is available
            if not(frame is None):

                # do something with your OpenCV frame here

                # reducer frames size if you want more performance otherwise comment this line
                frame = reducer(frame, percentage=20)  # reduce frame by 20%

                # return our gray frame
                return frame
            else:
                # signal we're not running now
                self.running = False
        # return None-type
        return None

    def stop(self):

        # don't forget this function!!!

        # flag that we're not running
        self.running = False
        # close stream
        if not self.source is None:
            self.source.stop()


# assign your Custom Streaming Class with adequate ScreenGear parameters
# to `custom_stream` attribute in options parameter
options = {"custom_stream": Custom_Stream_Class(backend="pil", logging=True)}

# initialize WebGear_RTC app without any source
web = WebGear_RTC(logging=True, **options)

# run this app on Uvicorn server at address http://localhost:8000/
uvicorn.run(web(), host="localhost", port=8000)

# close app safely
web.shutdown()