import mongoengine as mongo
class house_state( mongo.Document ):
  termo = mongo.FloatField(
    required = True,
    min_value = -50.0,
    max_value = +60.0
  )
