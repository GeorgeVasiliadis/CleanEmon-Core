"""JSON Schemas"""
schema_devices = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "devices": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "type": "string",
                "minLength": 1
            }
        }
    },
    "required": [
        "devices"
    ]
}

schema_meta = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "definitions": {
        "sharedProperties": {
            "RSOA": {
                "type": "string",
                "enum": [
                    "Rarely",
                    "Sometimes",
                    "Often",
                    "Always"
                ]
            }
        }
    },
    "type": "object",
    "properties": {
        "_id": {
            "type": "string"
        },
        "_rev": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "built": {
            "type": "integer",
            "minimum": 0
        },
        "Household m2": {
            "type": "number",
            "minimum": 0
        },
        "Dwelling": {
            "type": "string",
            "enum": [
                "Semidetached",
                "Townhome",
                "Apartment",
                "Family House"
            ]
        },
        "Bedrooms": {
            "type": "integer",
            "minimum": 0
        },
        "Heating Source": {
            "type": "boolean"
        },
        "Income": {
            "type": "integer",
            "minimum": 0
        },
        "Occupants": {
            "type": "integer",
            "minimum": 0
        },
        "Children": {
            "type": "integer",
            "minimum": 0
        },
        "Teenagers": {
            "type": "integer",
            "minimum": 0
        },
        "Adults": {
            "type": "integer",
            "minimum": 0
        },
        "Elders": {
            "type": "integer",
            "minimum": 0
        },
        "Fulltimers": {
            "type": "integer",
            "minimum": 0
        },
        "Parttimers": {
            "type": "integer",
            "minimum": 0
        },
        "Grads": {
            "type": "integer",
            "minimum": 0
        },
        "PostGrads": {
            "type": "integer",
            "minimum": 0
        },
        "Recycling": {
            "$ref": "#/definitions/sharedProperties/RSOA"
        },
        "Energy Class": {
            "$ref": "#/definitions/sharedProperties/RSOA"
        },
        "Thermostats": {
            "$ref": "#/definitions/sharedProperties/RSOA"
        },
        "Smart Plugs": {
            "$ref": "#/definitions/sharedProperties/RSOA"
        },
        "Awareness": {
            "$ref": "#/definitions/sharedProperties/RSOA"
        },
        "microwave": {
            "type": "boolean"
        },
        "electric_space_heater": {
            "type": "boolean"
        },
        "kettle": {
            "type": "boolean"
        },
        "fridge": {
            "type": "boolean"
        },
        "washing_machine": {
            "type": "boolean"
        },
        "dish_washer": {
            "type": "boolean"
        },
        "tumble_dryer": {
            "type": "boolean"
        },
        "computer": {
            "type": "boolean"
        },
        "electric_oven": {
            "type": "boolean"
        },
        "light": {
            "type": "boolean"
        },
        "max_scale_microwave": {
            "type": "integer"
        },
        "max_scale_electric_space_heater": {
            "type": "integer"
        },
        "max_scale_kettle": {
            "type": "integer"
        },
        "max_scale_fridge": {
            "type": "integer"
        },
        "max_scale_washing_machine": {
            "type": "integer"
        },
        "max_scale_dish_washer": {
            "type": "integer"
        },
        "max_scale_tumble_dryer": {
            "type": "integer"
        },
        "max_scale_computer": {
            "type": "integer"
        },
        "max_scale_electric_oven": {
            "type": "integer"
        },
        "max_scale_light": {
            "type": "integer"
        }
    },
    "additionalProperties": False
}
