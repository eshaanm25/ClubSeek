from multiprocessing.connection import wait
from flask import Flask, request, jsonify
import time


# Initialize Application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return jsonify({ 'msg': 'Hello World'})

# Run Server
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=3000)