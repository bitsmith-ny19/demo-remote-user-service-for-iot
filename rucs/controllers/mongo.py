from flask_mongoengine import MongoEngine
import logging
#import click
#from flask.cli import with_appcontext
from os import environ

def db_connect(app):
 
  mongo = MongoEngine()

  if not app.config["TESTING"]:
    # allow fork() calls by pymongo while the
    # wsgi process executes this flask app
    if "UWSGI_LOADED" in environ:
      from uwsgidecorators import postfork
      @postfork
      def setup_db():
        mongo.init_app( app )
      return

  else:
    logging.info(
      app.config["MONGODB_DB"],
      app.config["MONGODB_HOST"]
    )
    mongo.disconnect()

  mongo.init_app( app )
