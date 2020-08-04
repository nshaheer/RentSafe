from infrastructure.storage import StorageInterface
from services.formatter import LeaseFormatterService

from response import Response
from request import Request


class SubmitLeaseForAnalysis:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def execute(self, request: Request):

        lease_props = {
            "Status": "PENDING_EXTRACTION",
            "LeaseDocument": request.data["lease_file_path"],
        }

        lease_id = self.storage.add_lease(lease_props)

        formatted_lease = LeaseFormatterService.format_lease_for_android(
            self.storage.get_lease(lease_id)
        )
        return Response({"Lease": formatted_lease})
