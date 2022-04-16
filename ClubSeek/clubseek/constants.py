barSchema = {
    'type': 'object',
    'properties': {
        'barName': {'type': 'string',  "minLength": 4, "maxLength": 30},
        'wowFactor': {'type': 'integer', "minimum": 1, "maximum": 100},
        'capacity': {'type': 'integer', "minimum": 1, "maximum": 1000},
        'currentTraffic': {'type': 'integer', "minimum": 1, "maximum": 1000}
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