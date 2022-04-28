from flask import make_response

def getGreatest(bars, preference):
    index = 0
    greatestPreference = 0
    bestBarIndex = 0

    for bar in bars:
        if preference == "wowFactor":
            barPreference = bar.wowFactor
        else: 
            barPreference = bar.capacity
        if barPreference >= greatestPreference:
            bestBarIndex = index
            greatestPreference = bar.wowFactor
        index += 1
    
    return(bars[bestBarIndex])

def createResponse(body, statusCode):
    response = make_response(body, statusCode)
    response.mimetype = "text/html"
    return(response)