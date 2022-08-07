# import numpy as np
# from PIL import ImageFont, ImageDraw, Image
import os
import re
from time import time

from flask import Flask, render_template, Response, request
import cv2
import redis
import numpy as np
import datetime
import psycopg2
import time

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def get_chunk(byte1=None, byte2=None, filename="1.mp4"):
    file_size = os.stat(filename).st_size
    start = 0

    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(filename, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size


@app.route('/')
def get_file():
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
    for i in range(3):
        chunk, start, length, file_size = get_chunk(byte1, byte2, str(i) + ".mp4")
        resp = Response(chunk, 206, mimetype='video/mp4',
                        content_type='video/mp4', direct_passthrough=True)
        resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
        return resp


if __name__ == '__main__':
    app.run(threaded=True)
