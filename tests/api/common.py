"""
Common functions to support integration/API testing.
"""

import json
import os

import requests

_app_host = os.environ["IDOVEN_APP_HOST"]
LOGIN_URL = f"http://{_app_host}:5000/login"
USER_URL = f"http://{_app_host}:5000/user"
ECG_URL = f"http://{_app_host}:5000/ecg"


def make_headers(token: str) -> dict:
    """
    Create API request headers.

    :param token: The JWT to use for authentication
    :return: A dictionary of headers for use by requests
    """
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def login(username: str, password: str) -> dict:
    """
    Authenticates the user and provides a JWT token.

    :param username: The user to log in
    :param password: The user's password
    :return: A dictionary with keys "status_code" and "jwt"
    """
    payload = {"username": username, "password": password}
    response = requests.post(LOGIN_URL, json=payload)

    if response.text:
        jwt = json.loads(response.text).get("access_token", None)
    else:
        jwt = None

    return {
        "status_code": response.status_code,
        "token": jwt,
    }


def create_user(username: str, password: str) -> None:
    """
    Create a user in the system

    :param username: The username
    :param password: The password
    """
    login_response = login("admin", "password")
    assert login_response["status_code"] == 200

    payload = {"username": username, "password": password}
    headers = make_headers(login_response["token"])
    response = requests.put(USER_URL, json=payload, headers=headers)
    assert response.status_code == 200

    login_response = login(username, password)
    assert login_response["status_code"] == 200


def delete_user(username: str, password: str) -> None:
    """
    Deletes the specified user.

    :param username: The username
    :param password: The password
    """
    login_response = login("admin", "password")
    assert login_response["status_code"] == 200

    headers = make_headers(login_response["token"])
    response = requests.delete(f"{USER_URL}/{username}", headers=headers)
    assert response.status_code == 200

    login_response = login(username, password)
    assert login_response["status_code"] == 401
