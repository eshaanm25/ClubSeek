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
    },
    'required': ['barName']
}

class Bars:
    def __init__(self,barName, wowFactor, capacity, currentTraffic, address):
        self.barName = barName
        self.wowFactor = wowFactor
        self.capacity = capacity
        self.currentTraffic = currentTraffic
        self.address = address