from hospo_matcher.app import app
from hospo_matcher.utils.data_models import settings
from hospo_matcher.utils.database import Driver, driver

from fastapi.testclient import TestClient
from pytest import fixture

test_driver = Driver(settings.MONGODB_TEST_NAME)


@fixture(scope="module")
def client():
    # Override dependency to use test database
    def _override_get_db_client():
        return test_driver.get_db_client()

    app.dependency_overrides[driver.get_db_client] = _override_get_db_client

    client = TestClient(app)
    yield client