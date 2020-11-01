from os import environ
from flask import Flask
from rucs.config import Config
from uwsgidecorators import postfork
from flask_mongoengine import MongoEngine
from rucs.router import router
from demo import routes_demo_only

def create_app( testing_conf = None ):

  mongo = MongoEngine()
  
  rucs = Flask( __name__, instance_relative_config = True )

  if testing_conf is None:
    rucs.config.from_object( Config )
  else:
    rucs.config.from_mapping( testing_conf )

  # allow fork() calls by pymongo while the
  # wsgi process executes this flask app
  @postfork
  def setup_db():
    mongo.init_app( rucs )

  if "RUCS_DEMO" in environ:
    rucs.register_blueprint(routes_demo_only.routes)

  rucs.register_blueprint(router)

  # to move this to a controller subpackage?
  @rucs.after_request
  def set_json( res ):
    res.headers["Content-Type"] = "application/json"
    return res

  return rucs
