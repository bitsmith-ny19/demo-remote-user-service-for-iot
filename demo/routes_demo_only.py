from flask import (session, g, request, Blueprint)
import json
routes = Blueprint( "/demo", __name__ )

@routes.route("/set_token", methods = ["POST"])
def post():
  """
  This route is defined only if DEMO_RUCS is set
  in the environment variable when uwsgi starts.
  It serves to the security of the demo service by
  use of a cookie token that is accessible only to
  the user of the demo - the object ID of the
  Mongo document that stores the demo house state.
  `flask.session` can be set up quickly and sets
  HttpOnly flag, although in the demo use case, one
  could equally use the `flask.after_this_request`
  decorator to set the cookie headers in the response
  object.
  """
  #g.house_id = session.get("house_id")
  session["demo_house_id"] = request.get_json()["demo_house_id"]
  return "\"tested 123\""
