from mongoengine import (connect, disconnect)
from house_state import (HouseState, Lighting)
import json

mongo0 = connect( host = \
  "mongodb://rucs_db:27017/house_state"
)
db1 = mongo0.get_default_database()
hs = db1.get_collection("house_state")
#  hs.drop()

demo_state = HouseState( thermostat = 27.0 )
lighting0 = Lighting(
  label = "main-entrance-left",
  id = 3,
  is_on = False
)
demo_state.lighting.append( lighting0 )
demo_state.save()


#import pdb; pdb.set_trace()
demo_state = HouseState.objects( lighting__id = 3 )[0]

id = [ lighting["id"] for lighting in demo_state.lighting ]
id.sort()
id_new = -1
i = 0
while i < len(id) - 1:
  if id[i+1] > id[i] + 1: id_new = id[i] + 1
  i += 1
if id_new == -1: id_new = id[-1] + 1
print( "******", id_new )

entr = {"id": id_new, "label": "prueba 123 123"}
demo_state.lighting.append(
  Lighting.from_json( json.dumps(entr) )
)
print( [ii.to_json() for ii in demo_state.lighting] )
#disconnect()
