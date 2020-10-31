from flask import (Blueprint, session, g, request)
from rucs.models.house_state import HouseState

router = Blueprint( "/", __name__ )

@router.before_app_request
def controller_auth():
  """
  this is where authentication components
  can be integrated to the service.
  The mock version expects the cookie value
  that will be accessible to the users of the
  demo app (it will be printed to the stdout
  of the uwsgi process) (this token is simply
  the object id of the demo house state)
  """
  # todo: to move this to a controller.auth module

  # check demo token
  # if g.id != DEMO_TOKEN raise authFail
  # g.house_id = session["house_id"]

# possible extension: GET value of specific field
# or embedded item instead of entire document
@router.route("/", methods = ["GET"])
def get():
  sal = HouseState.objects()
  print("************", request.headers , "*************" )
  return sal[0].to_json()

@router.route("/", methods = ["POST"])
def post():
  p1_1 = house_state( termo = 27.4 )
  p1_1.save()
  return "se registró el valor"
