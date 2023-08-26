"""
Init script to create an admin user prior to using the application.
"""

import os

from dal import MONGO_AUTH_COLLECTION, MONGO_ECGS_COLLECTION

_ADMIN_USERNAME = os.environ["IDOVEN_APP_ADMIN_USERNAME"]
_ADMIN_PASSWORD = os.environ["IDOVEN_APP_ADMIN_PASSWORD"]
_ADMIN_ROLE = "ADMIN"


def clean_and_initialize():
    """
    Clean the database and create the admin user.
    """

    MONGO_ECGS_COLLECTION.delete_many({})
    MONGO_AUTH_COLLECTION.delete_many({})

    admin_data = {
        "username": _ADMIN_USERNAME,
        # This is currently stored as plaintext and in production we should use a hashed password.
        # Ideally, we would use an off-the-shelf auth system here rather than implement our own.
        "password": _ADMIN_PASSWORD,
        "role": _ADMIN_ROLE,
    }
    MONGO_AUTH_COLLECTION.insert_one(admin_data)


if __name__ == "__main__":
    clean_and_initialize()
