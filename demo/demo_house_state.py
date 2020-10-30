from mongoengine import (connect, disconnect)
from house_state import (HouseState, Lighting)

def init_db():
  connect( host = \
    "mongodb://python_house_state_db_1:27017/house_state"
  )
  demo_state = HouseState( thermostat = 27.0 )
  lighting0 = Lighting(
    label = "main-entrance-left",
    is_on = 0
  )
  demo_state.lighting.append( lighting0 )
  demo_state.save()
  print( "demo_house_state: initialization complete" )
  disconnect()

if __name__ == "__main__":
  init_db()
