from response import Response
from request import Request
from infrastructure.storage import StorageInterface
from infrastructure.extractor import ExtractorInteface
from services.thumbnail import ThumbnailService


class SubmitForAnalysis:
    def __init__(
        self, extractor: ExtractorInteface, storage: StorageInterface,
    ):
        self.storage = storage
        self.extractor = extractor

    def execute(self, request: Request) -> Response:

        file_path = request.data["lease_file_path"]
        thumbnail_str = ThumbnailService.get_thumbnail_as_binary_string(file_path)

        lease_props = {
            "extraction_status": "PENDING",
            "entity_recognition_status": "PENDING",
            "classification_status": "PENDING",
            "thumbnail_string": thumbnail_str,
        }

        lease_id = self.storage.add_lease(lease_props)

        extraction_job_id = self.extractor.extract(lease_id, file_path)

        self.storage.add_job(lease_id, "extraction", extraction_job_id)

        return Response({"lease": self.storage.get_lease(lease_id)})
