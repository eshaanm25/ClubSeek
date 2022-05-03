import clubseek.main
import clubseek.helpers
import json

def test_verify_password():
    assert clubseek.helpers.verify_password("admin","password") == "admin"

def test_verify_password_fail():
    assert clubseek.helpers.verify_password("sidhu","fish") != "sidhu"
    
def test_bar_greatest_wow():
   allBarObjects = []
   allBarObjects.append(
       clubseek.main.Bars(
           address = "cheese",
           barName = "pizza",
           capacity = 365,
           currentTraffic = 12,
           wowFactor = 88
       )
   )
  
   allBarObjects.append(
       clubseek.main.Bars(
           address = "pizza",
           barName = "cheese",
           capacity = 365,
           currentTraffic = 12,
           wowFactor = 77
       )
   )
 
   greatestBar = clubseek.helpers.getGreatestWow(allBarObjects)
 
   assert greatestBar.address == "cheese"
 
def test_bar_lowest_traffic():
   allBarObjects = []
   allBarObjects.append(
       clubseek.main.Bars(
           address = "cheese",
           barName = "pizza",
           capacity = 330,
           currentTraffic = 120,
           wowFactor = 88
       )
   )
  
   allBarObjects.append(
       clubseek.main.Bars(
           address = "pizza",
           barName = "cheese",
           capacity = 365,
           currentTraffic = 110,
           wowFactor = 77
       )
   )
 
   greatestBar = clubseek.helpers.getLowestCapacity(allBarObjects)
 
   assert greatestBar.address == "cheese"

    
