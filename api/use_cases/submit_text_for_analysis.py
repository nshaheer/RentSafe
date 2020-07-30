from response import Response
from request import Request
from infrastructure.storage import StorageInterface
from infrastructure.entity_recognizer import EntityRecogInterface
from infrastructure.classifier import ClassifierInterface
from services.thumbnail import ThumbnailService
from services.formatter import LeaseFormatterService


class SubmitTextForAnalysis:
    def __init__(
        self,
        recognizer: EntityRecogInterface,
        classifier: ClassifierInterface,
        storage: StorageInterface,
    ):
        self.storage = storage
        self.classifier = classifier
        self.recognizer = recognizer

    def execute(self, request: Request) -> Response:

        lease_id = request.data["lease_id"]
        paragraphs = request.data["paragraphs"]

        classification_job_id = self.classifier.classify(paragraphs)
        recog_job_id = self.recognizer.recognize(paragraphs)

        self.storage.update_lease(
            lease_id,
            {
                "Status": "PENDING_ANALYSIS",
                "Paragraphs": paragraphs,
                "ClassificationJobId": classification_job_id,
                "EntityRecognitionJobId": recog_job_id,
            },
        )

        formatted_lease = LeaseFormatterService.format_lease_for_android(
            self.storage.get_lease(lease_id)
        )
        return Response({"Lease": formatted_lease})
