import pytest

from app.core.config import settings
from app.db.mongodb import db
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_server_api, get_superuser_token_headers


@pytest.fixture(scope="module")
def server_api():
    return get_server_api()


@pytest.fixture(scope="module")
def superuser_token_headers():
    return get_superuser_token_headers()


@pytest.fixture(scope="module")
def normal_user_token_headers():
    return authentication_token_from_email(settings.EMAIL_TEST_USER)


@pytest.fixture(scope="session", autouse=True)
def db_setup(request):
    db.connect_to_mongo()

    def db_teardown():
        db.close_mongo_connection()

    request.addfinalizer(db_teardown)
