from typing import Tuple

import pymongo.errors
from flask import Flask, jsonify, request, Response
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

import dal.helpers
from dal import MONGO_AUTH_COLLECTION, MONGO_ECGS_COLLECTION
from ecg.helpers import count_zero_crossings

app = Flask(__name__)
# In production, this should be stored in a secrets manager.
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


# ECG Endpoints
@app.route("/ecg", methods=["PUT"])
@jwt_required()
def add_ecg() -> Tuple[Response, int]:
    """
    Endpoint to add ecg data to the database

    Expects JSON of the format:

        {
            "id": "test1",
            "date": 334368000000,
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
                ...
            ],
        }
    """
    user = get_jwt_identity()
    request_data = request.json
    if request_data is None:
        return jsonify({"error": "Malformed input."}), 400

    # add metadata to the request data
    ecg_data = {
        "owner": user,
    }
    ecg_data.update(request_data)

    try:
        MONGO_ECGS_COLLECTION.insert_one(ecg_data)
    except pymongo.errors.DuplicateKeyError:
        return jsonify({"error": "An ECG with this ID already exists."}), 400

    return jsonify({"id": ecg_data["id"]}), 201


@app.route("/ecg/<ecg_id>/crossings", methods=["GET"])
@jwt_required()
def get_ecg_crossings(ecg_id: str) -> Tuple[Response, int]:
    """
    Returns the zero-crossings data for the previously-uploaded ECG.

    Returns JSON of the format:

        {
            "id": "test1",
            "date": 334368000000,
            "leads": [
                {
                    "name": "I",
                    "zero_crossings": 3,
                },
                {
                    "name": "II",
                    "zero_crossings": 5,
                },
                ...
            ],
        }

    """
    user = get_jwt_identity()
    user_role = dal.helpers.get_role_for_user(user)
    ecg = MONGO_ECGS_COLLECTION.find_one({"id": ecg_id})

    if ecg is None:
        return jsonify({"error": f"ECG {ecg_id} not found"}), 404
    if ecg["owner"] != user and user_role != "ADMIN":
        return jsonify({"error": f"ECG {ecg_id} not found"}), 404

    result = {
        "id": ecg["id"],
        "date": ecg["date"],
        "leads": [],
    }

    for lead in ecg["leads"]:
        result["leads"].append(
            {
                "name": lead["name"],
                "zero_crossings": count_zero_crossings(lead["samples"]),
            }
        )

    return jsonify(result), 200


# Auth endpoints
@app.route("/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    Logs a user in with the supplied username and password, returning a jwt.

    Expects JSON of the format:

        {
            "username": "some_user"
            "password": "some_password"
        }

    Returns a JWT as a bare string.

    """

    if not request.json:
        return jsonify({"error": "Malformed input"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if None in (username, password):
        return jsonify({"error": "Invalid credentials."}), 401

    user = MONGO_AUTH_COLLECTION.find_one({"username": username})

    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials."}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route("/user", methods=["PUT"])
@jwt_required()
def add_user() -> Tuple[Response, int]:
    """
    Adds a user with role 'USER' to the system with the supplied username and password.

    Expects JSON of the format:

        {
            "username": "some_user"
            "password": "some_password"
        }

    Returns a message indicating success or failure.

    """

    if dal.helpers.get_role_for_user(get_jwt_identity()) != "ADMIN":
        return jsonify({"error": "Not authorized to perform this action."}), 401

    if not request.json:
        return jsonify({"error": "Malformed input"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if None in (username, password):
        return jsonify({"error": "Both username and password must be supplied."}), 400

    user_data = {
        "username": username,
        "password": password,
        "role": "USER",
    }

    try:
        MONGO_AUTH_COLLECTION.insert_one(user_data)
    except pymongo.errors.DuplicateKeyError:
        return jsonify({"error": "User already exists."}), 400

    return jsonify({"message": "User created successfully."}), 200


@app.route("/user/<username>", methods=["DELETE"])
@jwt_required()
def delete_user(username: str) -> Tuple[Response, int]:
    """
    Deletes the specified user from the system. Can only be run as an admin user.

    Expects the username to delete to be included in the URL.

    Returns the number of deleted records.
    """

    if dal.helpers.get_role_for_user(get_jwt_identity()) != "ADMIN":
        return jsonify({"error": "Not authorized to perform this action."}), 401

    if not username:
        return jsonify({"error": "Username must be supplied."}), 400

    delete_result = MONGO_AUTH_COLLECTION.delete_one({"username": username})

    return (
        jsonify(
            {"message": f"{delete_result.deleted_count} records deleted successfully."}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
