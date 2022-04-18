from flask import Flask
from api import apiEndpoints

# Run API Endpoint
if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(apiEndpoints)
    app.run(debug=True,host='0.0.0.0', port=3000)
