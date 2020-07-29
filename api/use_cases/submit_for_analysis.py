from response import Response
from request import Request
from infrastructure.storage import StorageInterface
from infrastructure.extractor import ExtractorInteface


class SubmitForAnalysis:
    def __init__(
        self, extractor: ExtractorInteface, storage: StorageInterface,
    ):
        self.storage = storage
        self.extractor = extractor

    def execute(self, request: Request) -> Response:

        lease_props = {
            "extraction_status": "PENDING",
            "entity_recognition_status": "PENDING",
            "classification_status": "PENDING",
        }

        lease_id = self.storage.add_lease(lease_props)

        file_path = request.data["lease_file_path"]
        extraction_job_id = self.extractor.extract(lease_id, file_path)

        self.storage.add_job(lease_id, "extraction", extraction_job_id)

        return Response({"lease": self.storage.get_lease(lease_id)})
