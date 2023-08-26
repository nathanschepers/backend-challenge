"""
Utility functions accessing the underlying database.
"""

from typing import Optional

from dal import MONGO_AUTH_COLLECTION


def get_role_for_user(username: str) -> Optional[str]:
    """

    Get the role for a given user.

    :param username: The username
    :return: If the user exists, returns the user's role (currently can be 'ADMIN' or 'USER'
    """

    user = MONGO_AUTH_COLLECTION.find_one({"username": username})

    if user:
        return user["role"]

    return None
