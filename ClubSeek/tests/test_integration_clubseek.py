from clubseek import *
import requests
import time
import json

# Connect to Database
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
    
    request = {
    "barName": "SuperAwais",
    "wowFactor": 54,
    "capacity": 836,
    "currentTraffic": 111,
    "address": "255 Sidhu Drive Eoin, NJ 08841"
    }

    addBar = requests.put("http://clubseek:3000/bars", json = request)

    getBar = requests.get("http://clubseek:3000/bars")
    
    expected = dict(
        address = "255 Sidhu Drive Eoin, NJ 08841",
        barName = "SuperAwais",
        capacity = 836,
        currentTraffic = 111,
        wowFactor = 54
        )
    
    expected = [expected]

    assert json.loads(getBar.content) == expected

def test_bar_deleting_bar():

    request = {
    "barName": "SuperAwais"
    }

    delBar = requests.delete("http://clubseek:3000/bars", json = request)

    getBar = requests.get("http://clubseek:3000/bars")
    
    assert(getBar.status_code == 300)



    


