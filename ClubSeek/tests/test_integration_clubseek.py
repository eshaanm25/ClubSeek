from xml.etree.ElementTree import tostring
from clubseek import *
from requests.auth import HTTPBasicAuth
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
 
def test_bar_adding_no_auth():
   request = [{
       "barName": "SuperAwais",
       "wowFactor": 54,
       "capacity": 836,
       "currentTraffic": 111,
       "address": "255 Sidhu Drive Eoin, NJ 08841"
   }]
 
   addBar = requests.post("http://clubseek:3000/bars", json = request)
 
   assert addBar.status_code == 401
 
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

def test_bar_updating_bar():
    request = {
        "barName": "SuperAwais",
        "wowFactorChange": 60,
        "capacityChange": 850,
        "currentTrafficChange": 150,
        "address": "255 Sidhu Drive Eoin, NJ 08841"
    }

    upBar = requests.put("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))
    assert (upBar.status_code == 200)

def test_bar_bad_update():
    request = {
        "barName": "SuperAwais",
        "wowFactorChange": 60,
        "capacityChange": 850,
        "currentTrafficChange": 900,
        "address": "255 Sidhu Drive Eoin, NJ 08841"
    }

    upBar = requests.put("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))
    assert (upBar.status_code == 400)

def test_bar_selection():
    request = {
        "name": "Eshaan Mathur",
        "phoneNumber": "732-732-7787",
        "minWowFactor": 50,
        "maxTraffic": 700,
        "preference": "capacity"
    }

    barSel = requests.get("http://clubseek:3000/barSelection", json = request)

    assert (barSel.status_code == 200)

def test_bar_selection_duplicate_Request():
    request = {
        "name": "Eshaan Mathur",
        "phoneNumber": "732-732-7787",
        "minWowFactor": 50,
        "maxTraffic": 700,
        "preference": "capacity"
    }

    barSel = requests.get("http://clubseek:3000/barSelection", json = request)

    assert (barSel.status_code == 400)

def test_bar_selection_no_avail_Bars():
    request = {
        "name": "Eshaan Mathur",
        "phoneNumber": "732-732-7787",
        "minWowFactor": 80,
        "maxTraffic": 700,
        "preference": "wowFactor"
    }

    barSel = requests.get("http://clubseek:3000/barSelection", json = request)

    assert (barSel.status_code == 211)

def test_view_clients():
    request = {
    }

    viewClients = requests.get("http://clubseek:3000/users", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))

    assert (viewClients.status_code == 200)

def test_view_clients_no_auth():
    request = {
    }

    viewClients = requests.get("http://clubseek:3000/users", json = request)

    assert (viewClients.status_code == 401)
 
def test_bar_deleting_bar_without_auth():
   request = {
       "barName": "SuperAwais",
       "address": "255 Sidhu Drive Eoin, NJ 08841"
       }
 
   # Delete Bar
   delBar = requests.delete("http://clubseek:3000/bars", json = request)
 
   getBar = requests.get("http://clubseek:3000/bars")
  
   assert(delBar.status_code == 401)
 
def test_bar_deleting_bar():
   request = {
       "barName": "SuperAwais",
       "address": "255 Sidhu Drive Eoin, NJ 08841"
       }
 
   # Delete Bar
   delBar = requests.delete("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))
 
   getBar = requests.get("http://clubseek:3000/bars")
  
   assert(delBar.status_code == 200)
 
 
def test_bar_fail_deleting_bar():
   request = {
       "barName": "SuperAwais",
       "address": "255 Sidhu Drive Eoin, NJ 08841"
       }
 
   # Delete Bar
   delBar = requests.delete("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))
 
   getBar = requests.get("http://clubseek:3000/bars")
  
   assert(delBar.status_code == 400)


def test_bar_add_300_bars():
    i = 0
    while True:
        name = str(i)
        request = [{
            "barName": name,
            "wowFactor": 54,
            "capacity": 836,
            "currentTraffic": 111,
            "address": name
        }]
        addBar = requests.post("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))
        i += 1
        if i > 299:
            break
    assert(addBar.status_code == 200)

def test_view_300_bars():
    viewBar = requests.get("http://clubseek:3000/bars")
    assert(viewBar.status_code == 200)
 
def test_bar_selection_with_many_bars():
    request = [{
            "barName": "target",
            "wowFactor": 70,
            "capacity": 836,
            "currentTraffic": 111,
            "address": "target"
        }]
    addBar = requests.post("http://clubseek:3000/bars", json = request, auth = HTTPBasicAuth('admin', passwordAdmin))

    request = {
        "name": "Joe Smith",
        "phoneNumber": "732-555-5555",
        "minWowFactor": 65,
        "maxTraffic": 300,
        "preference": "wowFactor"
    }

    barSel = requests.get("http://clubseek:3000/barSelection", json = request)

    assert (barSel.status_code == 200)

 
 
 
 


 
 
 

