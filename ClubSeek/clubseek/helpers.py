from get_docker_secret import get_docker_secret
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from flask import make_response
import json

'''
Helper Functions for API Endpoints
'''

# Iterates through an Array of Class Objects and finds the Bar with the greatest value of wowFactor
def getGreatestWow(bars):
    index = 0
    greatestPreference = 0
    bestBarIndex = 0

    for bar in bars:
        if bar.wowFactor >= greatestPreference:
            bestBarIndex = index
            greatestPreference = bar.wowFactor
        index += 1
    
    return(bars[bestBarIndex])

# Iterates through an Array of Class Objects and finds the Bar with the smallest Capacity
def getLowestCapacity(bars):
    index = 0
    greatestPreference = 0
    bestBarIndex = 0

    for bar in bars:
        if bar.capacity <= greatestPreference:
            bestBarIndex = index
            greatestPreference = bar.capacity
        index += 1
    
    return(bars[bestBarIndex])

# Shortcut to create Flask Response
def createResponse(body, statusCode):
    response = make_response(body, statusCode)
    response.mimetype = "text/html"
    return(response)

# Authentication for Protected Endpoints
auth = HTTPBasicAuth()
# Application credential hashes are stored in the application credentials file in the secrets folder
applicationCredentials = json.loads((get_docker_secret('application_credentials')))

# Validate Inputted Password Against Stored Hash
@auth.verify_password
def verify_password(username, password):
    if username in applicationCredentials and \
            check_password_hash(applicationCredentials.get(username), password):
        return username