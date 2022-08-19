from flask import Flask, request, jsonify
from flask_cors import CORS
import zdata
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

Items = []
gdata = []


@app.route('/')
def dafault_route():
    return 'FaceRecog '


# получение сообщений
@app.route("/dash/<int:id>")
def GetMessage(id):
    print(id)
    if id >= 0 and id < len(Items):
        print(Items[id])
        return Items[id], 200

        # //update
    else:
        return "not found", 400

@app.route('/photo/<path:path>')
def send_photo(path):
    return send_from_directory('photo', path)

@app.route('/capture/<path:path>')
def send_capture(path):
    return send_from_directory('capture', path)


if __name__ == '__main__':
    gdata = zdata.load()
    Items.append(gdata[1])
    Items.append(gdata[2])
    Items.append(gdata[3])
    app.run()
