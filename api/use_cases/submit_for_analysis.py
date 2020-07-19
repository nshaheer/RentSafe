from uuid import uuid4

from storage import StorageInterface
from classifier import ClassifierInterface
from entity_recognizer import EntityRecogInterface


class SubmitForAnalysis:
    def __init__(
        self,
        storage: StorageInterface,
        classifier: ClassifierInterface,
        entity_recog: EntityRecogInterface,
    ):
        self.storage = storage
        self.classifier = classifier
        self.entity_recog = entity_recog

    def execute(self, request):

        lease_id = str(uuid4())

        paragraphs = request.paragraphs

        classification_job_id = self.classifier.classify(lease_id, paragraphs)
        recog_job_id = self.entity_recog.recognize(lease_id, paragraphs)

        self.storage.add_lease(
            lease_id,
            paragraphs=paragraphs,
            status="PENDING",
            classification_job=classification_job_id,
            recog_job=recog_job_id,
        )
