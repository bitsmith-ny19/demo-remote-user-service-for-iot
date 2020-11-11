from rucs.models.house_state import (HouseState, Lighting)

def init_db():

  demo_state = HouseState( thermostat = 27.0 )
  lighting0 = Lighting(
    id = 1,
    label = "main-entrance-left",
    is_on = 0
  )
  demo_state.lighting.append( lighting0 )
  demo_state.save()
