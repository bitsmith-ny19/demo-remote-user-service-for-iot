from flask_mongoengine import MongoEngine
import logging
#import click
#from flask.cli import with_appcontext

def db_connect(app):
 
  mongo = MongoEngine()

  if not app.config["TESTING"]:
    from uwsgidecorators import postfork
    @postfork
    def setup_db():
      mongo.init_app( app )

  else:
    logging.info(
      app.config["MONGODB_DB"],
      app.config["MONGODB_HOST"]
    )
    mongo.init_app( app )
