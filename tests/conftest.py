import tests
import pytest
import rucs

@pytest.fixture
def rucs_testing():

  rucs_testing_app = create_app({
    "TESTING": True,
    "MONGODB_DB": "test0",
    "MONGODB_HOST": "mongomock://localhost"
  })

  tests.data_init.house_state()

  yield rucs_testing_app

@pytest.fixture
def client( app ):
  return app.test_client()

@pytest.fixture
def runner( app ):
  return app.test_cli_runner()
