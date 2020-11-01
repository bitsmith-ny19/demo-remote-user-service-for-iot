import mongoengine as mongo

class Lighting(mongo.EmbeddedDocument):
  id = mongo.IntField(
    min_value = 0,
    max_value = 1000,
    required = True
  )
  label = mongo.StringField(
    max_length = 30,
    required = True
  )
  is_on = mongo.BooleanField( required = True )
  description = mongo.StringField(
    max_length = 120,
    default = "",
    required = True
  )
class HouseState( mongo.Document ):
  # extension - fields with units (C, farenheit)
  thermostat = mongo.FloatField(
    required = True,
    min_value = -50.0,
    max_value = +60.0
  )
  lighting = mongo.ListField( mongo.EmbeddedDocumentField(Lighting) )
