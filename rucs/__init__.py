from os import environ
from flask import Flask
from rucs.config import Config
from uwsgidecorators import postfork
from flask_mongoengine import MongoEngine
from rucs.router import router

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

  rucs.register_blueprint(router)

  return rucs
