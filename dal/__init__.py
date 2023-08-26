"""
A data access layer to the mongodb instance. Handles access to mongodb and exposes constants for the ECG and Auth
collections.
"""

import os

from pymongo import MongoClient
from pymongo.collection import Collection

# set up mongo client
_mongo_host = os.environ["IDOVEN_MONGO_HOST"]
_mongo_db_name = os.environ["IDOVEN_MONGO_DATABASE"]
_mongo_user = os.environ["IDOVEN_MONGO_USER"]
_mongo_password = os.environ["IDOVEN_MONGO_PASS"]

_mongo_uri = f"mongodb://{_mongo_user}:{_mongo_password}@{_mongo_host}"

_mongo_ecgs_collection_name = os.environ["IDOVEN_MONGO_ECGS_COLLECTION"]
_mongo_auth_collection_name = os.environ["IDOVEN_MONGO_AUTH_COLLECTION"]

# set up collections
MONGO_ECGS_COLLECTION: Collection = MongoClient(
    _mongo_uri, uuidRepresentation="standard"
)[_mongo_db_name][_mongo_ecgs_collection_name]

MONGO_AUTH_COLLECTION: Collection = MongoClient(
    _mongo_uri, uuidRepresentation="standard"
)[_mongo_db_name][_mongo_auth_collection_name]

MONGO_AUTH_COLLECTION.create_index("username", unique=True)
MONGO_ECGS_COLLECTION.create_index("id", unique=True)
