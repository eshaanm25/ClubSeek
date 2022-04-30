from main import db 

'''
Schemas and DB Classes for validating API Request Schemas and Communicating with DB Tables
'''

# Request Schema for Adding Bars (/bars POST Request)
barSchema = {
    'type': 'array',
    "minItems": 1,
    'items': {
        'barName': {'type': 'string',  "minLength": 4, "maxLength": 30},
        'wowFactor': {'type': 'integer', "minimum": 1, "maximum": 100},
        'capacity': {'type': 'integer', "minimum": 1, "maximum": 1000},
        'currentTraffic': {'type': 'integer', "minimum": 1, "maximum": 1000},
        'address': {'type': 'string', "minLength": 4, "maxLength": 255},
    },
    'required': ['barName', 'wowFactor', 'capacity', 'currentTraffic']
}

# Request Schema for Deleting Bars (/bars DELETE Request)
barDeleteSchema = {
    'type': 'object',
    'properties': {
        'barName': {'type': 'string',  "minLength": 4, "maxLength": 30},
        'address': {'type': 'string',  "minLength": 4, "maxLength": 30}
    },
    'required': ['barName', 'address']
}

# Request Schema for Updating Bars (/bars PUT Request)
barUpdateSchema = {
    'type': 'object',
    'properties': {
        'barName': {'type': 'string',  "minLength": 4, "maxLength": 30},
        'wowFactorChange': {'type': 'integer', "minimum": 1, "maximum": 100},
        'capacityChange': {'type': 'integer', "minimum": 1, "maximum": 1000},
        'currentTrafficChange': {'type': 'integer', "minimum": 1, "maximum": 1000},
        'address': {'type': 'string', "minLength": 4, "maxLength": 255},
    },
    'required': ['barName', 'address']
}


# Request Schema for Choosing a Bar (/barSelection GET Request)
barAlgorithmSchema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string',  "minLength": 4, "maxLength": 30},
        'phoneNumber': {'type': 'integer'},
        'minWowFactor': {'type': 'integer'},
        'maxTraffic': {'type': 'integer'},
        'preference': {'type': 'string'}
    },
    'required': ['name', 'phoneNumber']
}

# SQL Alchemy DB Class for Communicating with Bars Table 
class Bars(db.Model):
    __tablename__ = "Bars"

    address = db.Column(db.String(255), primary_key = True)
    barName = db.Column(db.String(30), primary_key = True)
    capacity = db.Column(db.Integer)
    currentTraffic = db.Column(db.Integer)
    wowFactor = db.Column(db.Integer)

# SQL Alchemy DB Class for Communicating with Users Table 
class Users(db.Model):
    __tablename__ = "Users"

    userName = db.Column(db.String(255), primary_key = True)
    userPhoneNumber = db.Column(db.String(15), primary_key = True)
    assignedBarName = db.Column(db.String(30))
    assignedBarAddress = db.Column(db.String(255))

