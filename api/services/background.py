from infrastructure.extractor import ExtractorInteface
from infrastructure.entity_recognizer import EntityRecogInterface
from infrastructure.classifier import ClassifierInterface
from infrastructure.storage import StorageInterface


class BackgroundService:
    def __init__(
        self,
        extractor: ExtractorInteface,
        recognizer: EntityRecogInterface,
        classifier: ClassifierInterface,
        storage: StorageInterface,
    ):
        self.extractor = extractor
        self.recognizer = recognizer
        self.classifier = classifier
        self.storage = storage

    def process_pending_jobs(self):
        pending_jobs = storage.storage.get_pending_jobs()

        for job in pending_jobs:
            if job["type"] == "extraction":
                pass
            elif job["type"] == "entity_recognition":
                pass
            elif job["type"] == "classification":
                pass
