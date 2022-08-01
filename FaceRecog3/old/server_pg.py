import psycopg2

import pymjpeg
from glob import glob
import sys
import logging

from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level = logging.DEBUG)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.debug('GET response code: 200')
        self.send_response(200)
        # Response headers (multipart)
        for k, v in pymjpeg.request_headers().items():
            self.send_header(k, v)
            logging.debug('GET response header: ' + k + '=' + v)
        # Multipart content
        # for filename in glob('img/*.jpg'):
        while True:
            # Part boundary string
            self.end_headers()
            self.wfile.write(bytes(pymjpeg.boundary, 'utf-8'))
            self.end_headers()
            # Part headers
            img = []
            img = pymjpeg.image()
            for k, v in pymjpeg.image_headers(len(img)).items():
                self.send_header(k, v)
                # logging.debug('GET response header: ' + k + '=' + v)
            self.end_headers()
            # Part binary
            # logging.debug('GET response image: ' + filename)
            self.wfile.write(img)
    def log_message(self, format, *args):
        return

logging.info('Listening on port 8008...')
# connection = psycopg2.connect(user="personauser",
#                               password="pgpwd4persona",
#                               host="127.0.0.1",
#                               port="5432",
#                               database="personadb")
# cursor = connection.cursor()
# sql_delete_query = "Delete from public.z1frame"
# cursor.execute(sql_delete_query)
# connection.commit()

httpd = HTTPServer(('', 8008), MyHandler)
httpd.serve_forever()
