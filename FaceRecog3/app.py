from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

@app.route('/')
def index():
    # return render_template('index.html')
    # return render()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
