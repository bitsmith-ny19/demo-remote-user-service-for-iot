from rucs import create_app
import json
from os import environ

def test_config():
  environ["RUCS_CONFIG"] = "dev.cfg"
  assert not create_app().testing
  del environ["RUCS_CONFIG"]
  assert create_app({
    "TESTING": True,
    "MONGODB_DB": "test0",
    "MONGODB_HOST": "mongomock://localhost"
  }).testing

def test_route( client ):
  resp = client.get("/test")
  assert json.loads(resp.data) == "test 123"
