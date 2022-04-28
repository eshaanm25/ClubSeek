from main import db 

barSchema = {
    'type': 'object',
    'properties': {
        'barName': {'type': 'string',  "minLength": 4, "maxLength": 30},
        'wowFactor': {'type': 'integer', "minimum": 1, "maximum": 100},
        'capacity': {'type': 'integer', "minimum": 1, "maximum": 1000},
        'currentTraffic': {'type': 'integer', "minimum": 1, "maximum": 1000},
        'address': {'type': 'string', "minLength": 4, "maxLength": 255},
    },
    'required': ['barName', 'wowFactor', 'capacity', 'currentTraffic']
}

barDeleteSchema = {
    'type': 'object',
    'properties': {
        'barName': {'type': 'string',  "minLength": 4, "maxLength": 30},
        'address': {'type': 'string',  "minLength": 4, "maxLength": 30}
    },
    'required': ['barName', 'address']
}

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

# Bars Schema
class Bars(db.Model):
    __tablename__ = "Bars"

    address = db.Column(db.String(255), primary_key = True)
    barName = db.Column(db.String(30), primary_key = True)
    capacity = db.Column(db.Integer)
    currentTraffic = db.Column(db.Integer)
    wowFactor = db.Column(db.Integer)

