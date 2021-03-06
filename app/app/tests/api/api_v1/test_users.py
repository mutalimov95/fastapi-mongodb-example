import requests

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import (get_server_api, random_email,
                                   random_lower_string)


def test_get_users_superuser_me(superuser_token_headers):
    server_api = get_server_api()
    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(normal_user_token_headers):
    server_api = get_server_api()
    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/users/me", headers=normal_user_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(superuser_token_headers):
    server_api = get_server_api()
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(email=email)
    assert user.email == created_user["email"]


def test_get_existing_user(superuser_token_headers):
    server_api = get_server_api()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(obj_in=user_in)
    user_id = user.id
    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    user = crud.user.get_by_email(email=email)
    assert user.email == api_user["email"]


def test_create_user_existing_email(superuser_token_headers):
    server_api = get_server_api()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    crud.user.create(obj_in=user_in)
    data = {"email": email, "password": password}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(normal_user_token_headers):
    server_api = get_server_api()
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 400


def test_retrieve_users(superuser_token_headers):
    server_api = get_server_api()
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(obj_in=user_in)

    email2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=email2, password=password2)
    crud.user.create(obj_in=user_in2)

    r = requests.get(
        f"{server_api}{settings.API_V1_STR}/users/", headers=superuser_token_headers
    )
    all_users = r.json()

    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user
