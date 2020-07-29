from infrastructure.extractor import ExtractorInteface, ExtractorResultsNotAvailable
from infrastructure.entity_recognizer import (
    EntityRecogInterface,
    RecognizerResultsNotAvailable,
)
from infrastructure.classifier import ClassifierInterface, ClassifierResultsNotAvailable
from infrastructure.storage import StorageInterface

from services.analysis import AnalysisService


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
        pending_jobs = self.storage.get_pending_jobs()

        for job in pending_jobs:
            self.process_job(job)

    def process_job(self, job):
        if job["type"] == "extraction":
            self.process_extraction_job(job)
        if job["type"] == "recognition":
            self.process_recognition_job(job)
        if job["type"] == "classification":
            self.process_classification_job(job)

    def process_classification_job(self, job):

        try:
            results = self.classifier.get_results(job["job_id"])
            analysis = AnalysisService.analyze_classification_results(results)

            analysis.update({"classification_status": "COMPLETED"})

            self.storage.update_lease(job["lease_id"], analysis)
            self.storage.mark_job_completed(job["job_id"])

        except ClassifierResultsNotAvailable as _:
            pass

    def process_recognition_job(self, job):

        try:
            results = self.recognizer.get_results(job["job_id"])
            analysis = AnalysisService.analyze_recognition_results(results)

            analysis.update({"entity_recognition_status": "COMPLETED"})

            self.storage.update_lease(job["lease_id"], analysis)
            self.storage.mark_job_completed(job["job_id"])
        except ClassifierResultsNotAvailable as _:
            pass

    def process_extraction_job(self, job):

        try:
            results = self.extractor.get_results(job["job_id"])
            self.storage.update_lease(
                job["lease_id"], {"extraction_status": "COMPLETED"}
            )

            classification_job_id = self.classifier.classify(results)
            recog_job_id = self.recognizer.recognize(results)

            self.storage.mark_job_completed(job["job_id"])
            self.storage.add_job(
                job["lease_id"], "classification", classification_job_id
            )
            self.storage.add_job(job["lease_id"], "recognition", recog_job_id)

        except ExtractorResultsNotAvailable as _:
            pass
