from response import Response
from request import Request
from infrastructure.storage import StorageInterface
from infrastructure.classifier import ClassifierInterface
from infrastructure.entity_recognizer import EntityRecogInterface


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

    def execute(self, request: Request) -> Response:

        paragraphs = request.data["paragraphs"]

        classification_job_id = self.classifier.classify(paragraphs)
        recog_job_id = self.entity_recog.recognize(paragraphs)

        lease_id = self.storage.add_lease(
            paragraphs=paragraphs,
            status="PENDING",
            classification_job=classification_job_id,
            recog_job=recog_job_id,
        )

        return Response({"lease_id": lease_id})
