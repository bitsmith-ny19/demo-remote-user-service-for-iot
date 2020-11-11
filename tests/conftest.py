from tests.data_init import init_db
import pytest
from rucs import create_app

@pytest.fixture
def rucs_testing():

  rucs_testing_app = create_app({
    "TESTING": True,
    "MONGODB_DB": "test0",
    "MONGODB_HOST": "mongomock://localhost"
  })

  init_db()

  yield rucs_testing_app

# note about pytest: "fixtures" suggest metaprogramming
# techniques - the argument rucs_testing is
# not really an argument - it's a value, evaluated
# as the rucs_testing fixture defined above!
# this also occurs in test_ functions defined
# in pytest tests.
@pytest.fixture
def client( rucs_testing ):
  return rucs_testing.test_client()

@pytest.fixture
def runner( app ):
  return app.test_cli_runner()
