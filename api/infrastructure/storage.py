from uuid import uuid4
from abc import ABCMeta, abstractmethod

from pymongo import MongoClient


class StorageInterface(metaclass=ABCMeta):
    @abstractmethod
    def add_lease(self, paragraphs, **kwargs):
        pass


class MemStorage(StorageInterface):
    def __init__(self):
        self.storage = {}

    def add_lease(self, paragraphs, **kwargs):
        lease = {
            "paragraphs": paragraphs,
        }
        lease.update(kwargs)

        lease_id = str(uuid4())

        self.storage[lease_id] = lease

        return lease_id


class MongoStorage(StorageInterface):
    def __init__(self):
        # Connection setup
        conn = MongoClient(
            "mongodb+srv://admin:jLtC_Q4wHJmKZ4BfvaCR@rent-safe-test-db.ldmk8.mongodb.net/<dbname>?retryWrites=true&w=majority"
        )
        self.storage = conn["rent-safe"]["leases"]

    def add_lease(self, paragraphs, **kwargs):
        lease = {
            "paragraphs": paragraphs,
        }
        lease.update(kwargs)

        return self.storage.insert_one(lease).inserted_id
