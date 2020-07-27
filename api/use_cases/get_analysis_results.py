from response import Response
from request import Request
from infrastructure.storage import StorageInterface
from infrastructure.classifier import ClassifierInterface, ClassifierResultsNotAvailable
from infrastructure.entity_recognizer import (
    EntityRecogInterface,
    RecognizerResultsNotAvailable,
)
from services.analysis import AnalysisService


class GetAnalysis:
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

        lease_id = request.data["lease_id"]

        lease = self.storage.get_lease(lease_id)

        if lease["status"] == "PENDING":
            try:
                c_results = self.classifier.get_results(lease["classification_job_id"])
                r_results = self.entity_recog.get_results(lease["recog_job_id"])

                c_analysis = AnalysisService.analyze_classification_results(c_results)
                r_analysis = AnalysisService.analyze_recognition_results(r_results)

                lease_update = {}
                lease_update.update(c_analysis)
                lease_update.update(r_analysis)
                lease_update.update({"status": "COMPLETED"})

                lease = self.storage.update_lease(lease_id, lease_update)

            except (ClassifierResultsNotAvailable, RecognizerResultsNotAvailable) as _:
                return Response({"lease": lease})

        return Response({"lease": lease})
