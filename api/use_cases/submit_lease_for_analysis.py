from infrastructure.storage import StorageInterface
from services.thumbnail import ThumbnailService
from services.formatter import LeaseFormatterService

from response import Response
from request import Request


class SubmitLeaseForAnalysis:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def execute(self, request: Request):
        file_path = request.data["lease_file_path"]
        thumbnail_str = ThumbnailService.get_thumbnail_as_binary_string(file_path)

        lease_props = {
            "Status": "PENDING_EXTRACTION",
            "ThumbnailString": thumbnail_str,
        }

        lease_id = self.storage.add_lease(lease_props)

        formatted_lease = LeaseFormatterService.format_lease_for_android(
            self.storage.get_lease(lease_id)
        )
        return Response({"Lease": formatted_lease})
