from response import Response
from request import Request
from infrastructure.storage import StorageInterface

from services.email import EmailService


class EmailLeaseAnalysis:
    def __init__(
        self, storage: StorageInterface,
    ):
        self.storage = storage

    def execute(self, request: Request) -> Response:

        lease_id = request.data["lease_id"]
        to_email = request.data["to_email"]

        lease = self.storage.get_lease(lease_id)

        is_sent = EmailService.email_lease_analysis(to_email, lease)
        return Response({"status": "SUCCESS" if is_sent else "FAILED"})
