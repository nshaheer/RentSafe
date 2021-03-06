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
    def add_lease(self, lease):
        pass

    @abstractmethod
    def get_lease(self, lease_id):
        pass

    @abstractmethod
    def update_lease(self, lease_id, update):
        pass

    @abstractmethod
    def get_pending_analysis(self):
        pass

    @abstractmethod
    def find_leases_for_address(self, address):
        pass

    @abstractmethod
    def add_questionnaire_submission(self, submission):
        pass


class MemStorage(StorageInterface):
    def __init__(self):
        self.leases = {}
        self.questionnaire_submissions = {}

    def add_lease(self, lease):
        lease_id = str(uuid4())

        self.leases[lease_id] = lease

        return lease_id

    def get_lease(self, lease_id):
        return self.leases.get(lease_id, None)

    def update_lease(self, lease_id, update):
        lease = self.leases.get(lease_id, {})
        lease.update(update)

        self.leases[lease_id] = lease
        return lease

    def get_pending_analysis(self):
        return [a for a in self.leases.values() if a["Status"] == "PENDING_ANALYSIS"]

    def find_leases_for_address(self, address):
        return []

    def add_questionnaire_submission(self, submission):
        submission_id = str(uuid4())

        self.questionnaire_submissions[submission_id] = submission


class MongoStorage(StorageInterface):
    def __init__(self):
        # Connection setup
        conn = MongoClient(
            "mongodb+srv://admin:jLtC_Q4wHJmKZ4BfvaCR@rent-safe-test-db.ldmk8.mongodb.net/<dbname>?retryWrites=true&w=majority",
            ssl=True,
            ssl_cert_reqs=CERT_NONE,
        )
        self.leases = conn["rent-safe"]["leases"]
        self.questionnaire_submissions = conn["rent-safe"]["questionnaire_submissions"]

    def add_lease(self, lease):
        return self.leases.insert_one(lease).inserted_id

    def get_lease(self, lease_id):
        return self.leases.find_one({"_id": ObjectId(lease_id)})

    def update_lease(self, lease_id, update):
        result = self.leases.update_one({"_id": ObjectId(lease_id)}, {"$set": update})

        if result.modified_count != 1 and result.matched_count != 1:
            raise UpdateFailedException()

        return self.leases.find_one({"_id": ObjectId(lease_id)})

    def get_pending_analysis(self):
        return self.leases.find({"Status": "PENDING_ANALYSIS"})

    def find_leases_for_address(self, address):
        return self.leases.find({"Locations.0": address, "Amounts.0": {"$gt": 1}})

    def add_questionnaire_submission(self, submission):
        return self.questionnaire_submissions.insert_one(submission).inserted_id
