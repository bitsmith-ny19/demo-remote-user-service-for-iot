from flask import Blueprint
from flask import session
from flask import g
from rucs.models.house_state import HouseState

router = Blueprint( "/", __name__ )

# check cookie / define auth error
# this is a mock auth function that verifies
# a hard-coded token that will be given
# to users of the demo app
@router.before_app_request
def controller_auth():
  # try to move this to controller.auth
  g.id = session.get("oid")
  # check demo token
  # if g.id != DEMO_TOKEN raise authFail

# possible extension: GET value of specific field
# or embedded item instead of entire document
@router.route("/", methods = ["GET"])
def get():
  sal = house_state.objects( termo = 27.4 )
  return sal[0].to_json()

@router.route("/", methods = ["POST"])
def post():
  p1_1 = house_state( termo = 27.4 )
  p1_1.save()
  return "se registró el valor"
