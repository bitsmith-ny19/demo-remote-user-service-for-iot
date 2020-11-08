from flask import (Blueprint, g, request, abort)
# todo - change Lighting HouseStatex
#         to HouseStateSchema, LightingModelSchema
from rucs.models.house_state import (HouseState, Lighting)
from rucs.views import HouseStateInterface
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
  g.house_id = request.cookies.get("house_id")
  if g.house_id:
    print( "rucs.router before_request: house id found" )

  # bypass authentication if BYPASS_AUTH flag is set:
  if environ["BYPASS_AUTH"]:
    g.house_id = HouseState.objects()[0].id.__str__()

  if g.house_id == None:
    print( "rucs.router: no house id in session" )
    abort( 400, '{"error": {"message": "no access"}}' )

router.add_url_rule( "/", view_func = \
  HouseStateInterface.as_view("house_state") )
