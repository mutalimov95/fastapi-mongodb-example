import requests

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import (get_server_api, random_email,
                                   random_lower_string)


def user_authentication_headers(server_api, email, password):
    data = {"username": email, "password": password}

    r = requests.post(f"{server_api}{settings.API_V1_STR}/auth/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user():
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(obj_in=user_in)
    return user


def authentication_token_from_email(email):
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(email=email)
    if not user:
        user_in = UserCreate(email=email, password=password)
        user = crud.user.create(obj_in=user_in)
    else:
        user_in = UserUpdate(password=password)
        user = crud.user.update(db_obj=user, obj_in=user_in)

    return user_authentication_headers(get_server_api(), email, password)
