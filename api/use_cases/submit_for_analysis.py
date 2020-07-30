from response import Response
from request import Request
from infrastructure.storage import StorageInterface
from infrastructure.extractor import ExtractorInteface
from infrastructure.entity_recognizer import EntityRecogInterface
from infrastructure.classifier import ClassifierInterface
from services.thumbnail import ThumbnailService
from services.formatter import LeaseFormatterService


class SubmitForAnalysis:
    def __init__(
        self,
        extractor: ExtractorInteface,
        recognizer: EntityRecogInterface,
        classifier: ClassifierInterface,
        storage: StorageInterface,
    ):
        self.storage = storage
        self.extractor = extractor
        self.classifier = classifier
        self.recognizer = recognizer

    def execute(self, request: Request) -> Response:

        file_path = request.data["lease_file_path"]
        thumbnail_str = ThumbnailService.get_thumbnail_as_binary_string(file_path)

        lease_props = {
            "Status": "PENDING",
            "ThumbnailString": thumbnail_str,
        }

        lease_id = self.storage.add_lease(lease_props)

        # Celery Task
        paragraphs = self.extractor.extract(lease_id, file_path)

        classification_job_id = self.classifier.classify(paragraphs)
        recog_job_id = self.recognizer.recognize(paragraphs)

        self.storage.update_lease(
            lease_id,
            {
                "Paragraphs": paragraphs,
                "ClassificationJobId": classification_job_id,
                "EntityRecognitionJobId": recog_job_id,
            },
        )

        formatted_lease = LeaseFormatterService.format_lease_for_android(
            self.storage.get_lease(lease_id)
        )
        return Response({"Lease": formatted_lease})
