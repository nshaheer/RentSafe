from infrastructure.storage import StorageInterface
from services.thumbnail import ThumbnailService
from request import Request


class GetLeaseThumbnail:
    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def execute(self, request: Request):

        lease_id = request.data["lease_id"]
        file_path = request.data["lease_file_path"]
        thumbnail_str = ThumbnailService.get_thumbnail_as_binary_string(file_path)

        lease_props = {
            "ThumbnailString": thumbnail_str,
        }

        self.storage.update_lease(lease_id, lease_props)
