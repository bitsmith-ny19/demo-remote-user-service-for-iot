from flask import (Blueprint, session, g, request, abort)
from rucs.models.house_state import (HouseState, Lighting)
import json
from os import environ

router = Blueprint( "router", __name__ )

@router.before_request
def controller_auth():
  """
  this is where authentication components
  can be integrated to the service.
  The mock version requires a token
  that will be accessible to the users of the
  demo app - the Mongo object id of the demo
  house state (for convenience of
  the user of the demo, the id is printed to
  stdout of the uwsgi process). if demo
  is enabled, the user can enter the object id
  in the index page, and this sets the cookie
  with the value of this token.
  
  """
  # todo: to move this function to a controller.auth module

  g.house_id = None
  
  # check demo token
  if "house_id" in session:
    print( "rucs.router before_request: house id found" )
    g.house_id = session["house_id"]

  # bypass authentication if BYPASS_AUTH flag is set:
  if environ["BYPASS_AUTH"]:
    g.house_id = HouseState.objects()[0].id.__str__()

  if g.house_id == None:
    print( "rucs.router: no house id in session" )
    abort( 400, '{"error": {"message": "no access"}}' )

# possible extension: GET value of specific field
# or embedded item instead of entire document
@router.route("/", methods = ["GET"])
def get():
  """
  get house state as json. the house state object id
  is read before this in the request cycle from a cookie.
  Format of returned data:
  {"thermostat": TEMP, "lighting": [
    { "id": ID, "label": LABEL, "is_on": BOOLEAN },
    ...
  ] }
  """
  house_state = HouseState.objects( id = g.house_id )
  return house_state[0].to_json()

@router.route("/", methods = ["POST"])
def post():
  """
  post new lighting unit with give LABEL and on/off STATE.
  usage:
  { "label": LABEL, "is_on": STATE }

  Uniqueness condition verified manually  -
  mongodb can only verify uniqueness across a collection, and
  not in a list of embedded documents as a "virtual collection"
 
  """
  house_state = HouseState.objects( id = g.house_id )[0]
  label_new = request.get_json()["label"]

  # require unique label of lighting unit
  # todo - custom uniqueness exception class
  for lighting in house_state.lighting:
    if lighting.label == label_new:
      abort(500, description = "lighting unit already exists")

  # select new id (find smallest available id)
  id = [ lighting.id for lighting in house_state.lighting ]
  if id == []: id_new = 1
  else:
    id.sort()
    id_new = -1
    i = 0
    while i < len(id) - 1:
      if id[i+1] > id[i] + 1: id_new = id[i] + 1
      i += 1
    if id_new == -1: id_new = id[-1] + 1

  # insert new lighting unit
  lighting_new_json = json.dumps( {
    "id": id_new,
    "label": label_new,
    "is_on":  request.get_json()["is_on"]
  } )
  house_state.lighting.append(
    Lighting.from_json( lighting_new_json )
  )
  house_state.save()
  return '"new lighting unit saved posted"'

@router.route("/", methods = ["DELETE"])
def delete():
  """
  delete lighting unit.
  usage:
  { "id": ID }
  """
  house_state = HouseState.objects( id = g.house_id )[0]
  id = request.get_json()["id"]

  index = 0
  while index < len(house_state.lighting):
    if house_state.lighting[index]["id"] == id:
      del house_state.lighting[index]
    index += 1
#  for item in house_state.lighting:
#    if item["id"] == id: del item
#    break

  house_state.save() 
  return '"operation completed"'

@router.route("/", methods = ["PUT"])
def put():
  """
  Update lighting unit power state, label or thermostat state.
  this specification updates only one key per request (in fact,
  it can also update in a single request the thermostat, label &
  is_on of a single lighting unit, but this is not included in
  the specification).
  usage:
    { "thermostat": TEMP } ||
    { "lighting": [ { "id": ID, "label": LABEL } ] } ||
    { "lighting": [ { "id": ID, "is_on": STATE } ] }

  todo: the operation is simply to update a subgraph
  of a Mongo document - it seems that it can
  be abstracted to replace all the conditionals used bellow,
  and include also the ability to update any valid subgraph
  of the Mongo document
  **** BUG: uniqueness of labels not enforced on update ****
      to prevent repetitive programming, to fix this
      once the uniqueness validator is moved to a separate
      module
  """
  house_state = HouseState.objects( id = g.house_id )[0]
  house_state_update = request.get_json()

  if "thermostat" in house_state_update:
    house_state.thermostat = house_state_update["thermostat"]

  if "lighting" in house_state_update:
    lighting_unit_update = house_state_update["lighting"][0]
    id = lighting_unit_update["id"]
    lighting_unit = None

    # find the lighting Mongo embedded document with id from
    # the PUT request. Mongo can search accross collections
    # but not embedded documents in a list field.
    for item in house_state.lighting:
      if item["id"] == id:
        lighting_unit = item
    if lighting_unit == None:
      abort(500, ( '{"error": {"message":'
        '"id of lighting unit not found"}}'
      ) )

    if "is_on" in lighting_unit_update:
      lighting_unit["is_on"] = lighting_unit_update["is_on"]

    if "label" in lighting_unit_update:
      lighting_unit["label"] = lighting_unit_update["label"]

  house_state.save()
  return '"house state updated"'
