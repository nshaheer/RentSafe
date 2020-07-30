import base64
from preview_generator.manager import PreviewManager


class ThumbnailService:
    @staticmethod
    def _generate_thumbnail(file_path):

        cache_path = "/tmp"

        manager = PreviewManager(cache_path, create_folder=True)
        return manager.get_jpeg_preview(file_path)

    @staticmethod
    def get_thumbnail_as_url(thumbnail_path):
        pass

    @staticmethod
    def get_thumbnail_as_binary_string(file_path):

        thumbnail_path = ThumbnailService._generate_thumbnail(file_path)

        with open(thumbnail_path, "rb") as imageFile:
            thumbnail_str = base64.b64encode(imageFile.read())

        return thumbnail_str
