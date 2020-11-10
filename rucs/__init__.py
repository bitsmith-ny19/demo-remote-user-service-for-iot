from os import environ
import logging
from flask import (Flask, jsonify)
#from uwsgidecorators import postfork
#from flask_mongoengine import MongoEngine
from rucs.router import router
from demo import routes_demo_only
from flask_cors import CORS
from flask_swagger import swagger
from rucs.controllers.mongo import db_connect

def create_app( testing_conf = None ):

#  mongo = MongoEngine()
  
  rucs = Flask(
    __name__,
    instance_relative_config = True,
    instance_path = "/usr/lib/rucs-api-instance" )

  CORS(rucs)

  if testing_conf is None:
    logging.info( "loading config from", environ["RUCS_CONFIG"] )
    rucs.config.from_envvar("RUCS_CONFIG")
  else:
    logging.info( "loading config from testing config" )
    rucs.config.from_mapping( testing_conf )
    
  db_connect(rucs)

  # allow fork() calls by pymongo while the
  # wsgi process executes this flask app
#  @postfork
#  def setup_db():
#    mongo.init_app( rucs )

  if environ["DEMO"]:
    logging.info("initializing demo mode")
    rucs.register_blueprint(routes_demo_only.routes)

  rucs.register_blueprint(router)

  @rucs.route("/spec")
  def spec():
    openapi = swagger(rucs)
    openapi["info"]["version"] = "0.0a"
    openapi["info"]["title"] = "RUCS"
    openapi["info"]["description"] = \
      "(R)emote (U)ser (C)ontrol (S)ervice"
    return jsonify( openapi )
  logging.info( "added openapi specs endpoint at /rucs/spec" )

  # to move this to a controller subpackage?
  @rucs.after_request
  def set_json( res ):
    res.headers["Content-Type"] = "application/json"
    return res

  return rucs
