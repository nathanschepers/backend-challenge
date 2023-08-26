"""
Integration tests for the auth endpoints of the application
"""

import requests

from common import USER_URL, make_headers, login, create_user


def test_login():
    """
    Test login with the default admin username/password
    """
    login_response = login("admin", "password")
    assert login_response["status_code"] == 200


def test_create_user_with_admin_login():
    """
    Test user creation (successful)
    """
    user, password = "test_user", "test_password"

    login_response = login("admin", "password")
    assert login_response["status_code"] == 200

    payload = {"username": user, "password": password}
    headers = make_headers(login_response["token"])
    response = requests.put(USER_URL, json=payload, headers=headers)
    assert response.status_code == 200

    login_response = login(user, password)
    assert login_response["status_code"] == 200


def test_create_user_not_admin():
    """
    Test unsuccessful user creation (not admin)
    """
    user, password = "not_admin", "test_password"
    create_user(user, password)

    login_response = login(user, password)
    assert login_response["status_code"] == 200

    payload = {"username": "newuser", "password": "newpassword"}
    headers = make_headers(login_response["token"])
    response = requests.put(USER_URL, json=payload, headers=headers)
    assert response.status_code == 401


def test_delete_user():
    """
    Test user deletion (successful)
    """
    user, password = "test_user", "test_password"
    create_user(user, password)

    login_response = login("admin", "password")
    assert login_response["status_code"] == 200

    headers = make_headers(login_response["token"])
    response = requests.delete(f"{USER_URL}/{user}", headers=headers)
    assert response.json()["message"] == "1 records deleted successfully."
    assert response.status_code == 200

    login_response = login(user, password)
    assert login_response["status_code"] == 401


def test_delete_user_not_admin():
    """
    Test user deletion (not successful, not admin)
    """
    user, password = "not_admin", "test_password"
    create_user(user, password)

    login_response = login(user, password)
    assert login_response["status_code"] == 200

    headers = make_headers(login_response["token"])
    response = requests.delete(f"{USER_URL}/{user}", headers=headers)
    print(response.content)
    assert response.json()["error"] == "Not authorized to perform this action."
    assert response.status_code == 401
