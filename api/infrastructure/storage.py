from ssl import CERT_NONE
from uuid import uuid4
from abc import ABCMeta, abstractmethod

from bson.objectid import ObjectId

from pymongo import MongoClient


class StorageException(Exception):
    pass


class UpdateFailedException(StorageException):
    pass


class StorageInterface(metaclass=ABCMeta):
    @abstractmethod
    def add_lease(self, paragraphs, **kwargs):
        pass

    @abstractmethod
    def get_lease(self, lease_id):
        pass


class MemStorage(StorageInterface):
    def __init__(self):
        self.leases = {}

    def add_lease(self, lease):
        lease_id = str(uuid4())

        self.leases[lease_id] = lease

        return lease_id

    def get_lease(self, lease_id):
        return self.leases.get(id, None)


class MongoStorage(StorageInterface):
    def __init__(self):
        # Connection setup
        conn = MongoClient(
            "mongodb+srv://admin:jLtC_Q4wHJmKZ4BfvaCR@rent-safe-test-db.ldmk8.mongodb.net/<dbname>?retryWrites=true&w=majority",
            ssl=True,
            ssl_cert_reqs=CERT_NONE,
        )
        self.leases = conn["rent-safe"]["leases"]

    def add_lease(self, lease):
        return self.leases.insert_one(lease).inserted_id

    def get_lease(self, lease_id):
        return self.leases.find_one({"_id": ObjectId(lease_id)})

    def update_lease(self, lease_id, update):
        result = self.leases.update_one({"_id": ObjectId(lease_id)}, {"$set": update})

        if result.modified_count != 1:
            raise UpdateFailedException()

        return self.leases.find_one({"_id": ObjectId(lease_id)})
