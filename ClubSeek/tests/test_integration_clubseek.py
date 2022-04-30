from clubseek import *
from requests.auth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from get_docker_secret import get_docker_secret
import requests
import time
import json

passwordAdmin = "password"

# Wait for API Endpoint to Connect to Database
while True:
    try:
        response = requests.get("http://clubseek:3000/readiness")
        if response.status_code == 200:
            break
    except:
        print("Waiting for API Endpoint")
        time.sleep(5)
        continue

def test_bar_adding():
    # Add Bar
    request = [{
        "barName": "SuperAwais",
        "wowFactor": 54,
        "capacity": 836,
        "currentTraffic": 111,
        "address": "255 Sidhu Drive Eoin, NJ 08841"
    }]

    addBar = requests.post("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))

    getBar = requests.get("http://clubseek:3000/bars")
    
    expected = [dict(
        address = "255 Sidhu Drive Eoin, NJ 08841",
        barName = "SuperAwais",
        capacity = 836,
        currentTraffic = 111,
        wowFactor = 54
        )]

    assert json.loads(getBar.content) == expected

def test_bar_deleting_bar():
    request = {
        "barName": "SuperAwais",
        "address": "255 Sidhu Drive Eoin, NJ 08841"
        }

    # Delete Bar
    delBar = requests.delete("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))

    getBar = requests.get("http://clubseek:3000/bars")
    
    assert(delBar.status_code == 200)

    


