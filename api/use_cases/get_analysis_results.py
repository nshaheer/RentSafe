from response import Response
from request import Request
from infrastructure.storage import StorageInterface
from infrastructure.classifier import ClassifierInterface, ClassifierResultsNotAvailable
from infrastructure.entity_recognizer import (
    EntityRecogInterface,
    RecognizerResultsNotAvailable,
)
from services.analysis import AnalysisService
from services.formatter import LeaseFormatterService


class GetAnalysis:
    def __init__(
        self, storage: StorageInterface,
    ):
        self.storage = storage

    def execute(self, request: Request) -> Response:

        lease_id = request.data["lease_id"]

        lease = self.storage.get_lease(lease_id)

        formatted_lease = LeaseFormatterService.format_lease_for_android(lease)
        return Response({"Lease": formatted_lease})
