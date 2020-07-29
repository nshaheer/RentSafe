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

    @abstractmethod
    def update_lease(self, lease_id, update):
        pass

    @abstractmethod
    def add_job(self, lease_id, job_type, job_id):
        pass

    @abstractmethod
    def get_pending_jobs(self):
        pass

    @abstractmethod
    def mark_job_completed(self, job_id):
        pass


class MemStorage(StorageInterface):
    def __init__(self):
        self.leases = {}
        self.jobs = {}

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

    def add_job(self, lease_id, job_type, job_id):
        _id = str(uuid4())

        self.jobs[_id] = {
            "lease_id": lease_id,
            "job_type": job_type,
            "job_id": job_id,
            "status": "PENDING",
        }

    def get_pending_jobs(self):
        return [j for j in self.jobs.values() if j["status"] == "PENDING"]

    def mark_job_completed(self, job_id):
        self.jobs[job_id]["status"] = "COMPLETED"


class MongoStorage(StorageInterface):
    def __init__(self):
        # Connection setup
        conn = MongoClient(
            "mongodb+srv://admin:jLtC_Q4wHJmKZ4BfvaCR@rent-safe-test-db.ldmk8.mongodb.net/<dbname>?retryWrites=true&w=majority",
            ssl=True,
            ssl_cert_reqs=CERT_NONE,
        )
        self.leases = conn["rent-safe"]["leases"]
        self.jobs = conn["rent-safe"]["jobs"]

    def add_lease(self, lease):
        return self.leases.insert_one(lease).inserted_id

    def get_lease(self, lease_id):
        return self.leases.find_one({"_id": ObjectId(lease_id)})

    def update_lease(self, lease_id, update):
        result = self.leases.update_one({"_id": ObjectId(lease_id)}, {"$set": update})

        if result.modified_count != 1 and result.matched_count != 1:
            raise UpdateFailedException()

        return self.leases.find_one({"_id": ObjectId(lease_id)})

    def add_job(self, lease_id, job_type, job_id):
        return self.jobs.insert_one(
            {
                "lease_id": lease_id,
                "job_type": job_type,
                "job_id": job_id,
                "status": "PENDING",
            }
        )

    def get_pending_jobs(self):
        return self.jobs.find({"status": "PENDING"})

    def mark_job_completed(self, job_id):
        return self.jobs.update_one(
            {"job_id": job_id}, {"$set": {"status": "COMPLETE"}}
        )
