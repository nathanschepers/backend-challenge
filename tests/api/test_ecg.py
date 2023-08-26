"""
Automated tests for ECG endpoints.
"""

import time

import requests

from common import create_user, login, make_headers, ECG_URL


def test_create_ecg():
    """
    Test uploading ECG data. See docstring on the PUT endpoint in app.py for API details.
    """
    user, password = "create_ecg_user", "pw"
    ecg_id = "test1"

    create_user(user, password)
    login_response = login(user, password)
    assert login_response["status_code"] == 200

    payload = {
        "id": f"{ecg_id}",
        "date": int(time.time()),
        "leads": [
            {
                "name": "I",
                "num_samples": "10",
                "samples": [1, 2, 3, -3, -2, -1, 3, 2, 1, -10],
            },
            {
                "name": "II",
                "num_samples": "9",
                "samples": [1, -1, 3, -3, 5, -5, 7, -7, 11],
            },
        ],
    }

    headers = make_headers(login_response["token"])

    response = requests.put(ECG_URL, json=payload, headers=headers)
    assert response.status_code == 201


def test_get_crossings():
    """
    Test getting the zero crossings data. See docstring on the PUT endpoint in app.py for API details.
    """
    user, password = "create_ecg_user", "pw"
    ecg_id = "test1"

    create_user(user, password)
    login_response = login(user, password)
    assert login_response["status_code"] == 200

    headers = make_headers(login_response["token"])
    payload = {
        "id": f"{ecg_id}",
        "date": int(time.time()),
        "leads": [
            {
                "name": "I",
                "num_samples": "10",
                "samples": [1, 2, 3, -3, -2, -1, 3, 2, 1, -10],
            },
            {
                "name": "II",
                "num_samples": "9",
                "samples": [1, -1, 3, -3, 5, -5, 7, -7, 11],
            },
        ],
    }
    response = requests.put(ECG_URL, json=payload, headers=headers)
    assert response.status_code == 201

    crossings_url = ECG_URL + f"/{ecg_id}/crossings"

    response = requests.get(crossings_url, headers=headers)
    assert response.status_code == 200

    crossings_data = response.json()
    assert crossings_data["leads"][0]["zero_crossings"] == 3
    assert crossings_data["leads"][1]["zero_crossings"] == 8
