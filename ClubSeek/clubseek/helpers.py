from flask import make_response


# Iterates through an Array of Class Objects and finds the greatest value of wowFactor or capacity
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

# Shortcut to create Flask Response
def createResponse(body, statusCode):
    response = make_response(body, statusCode)
    response.mimetype = "text/html"
    return(response)