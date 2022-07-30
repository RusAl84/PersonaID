from av import VideoFrame
from aiortc import VideoStreamTrack


class ImageRenderingTrack(VideoStreamTrack):

    def __init__(self):
        super().__init__()
        self.queue = asyncio.Queue(10)

    def add_image(self, img: humpy.ndarray):
        try:
            self.queue.put_nowait(img)
        except asyncio.queues.QueueFull:
            pass

    async def add_image_async(self, img: numpy.ndarray):
        await self.queue.put(img)

    async def recv(self):
        img = await self.queue.get()
        frame = VideoFrame.from_ndarray(img, format="bgr24")
        pts, time_base = await self.next_timestamp()
        frame.pts = pts
        frame.time_base = time_base
        return frame