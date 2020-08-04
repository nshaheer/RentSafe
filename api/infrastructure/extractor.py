import os, io
import re
from uuid import uuid4
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format

from uuid import uuid4
from abc import ABCMeta, abstractmethod

from services.image_conversion import ImageConversionService
from utils import get_file_type
from .dummy_results import extraction_job_results as dummy_results


class ExtractorException(Exception):
    pass


class ExtractorResultsNotAvailable(ExtractorException):
    pass


class ExtractorImageConversionFailed(ExtractorException):
    pass


class ExtractorInteface(metaclass=ABCMeta):
    @abstractmethod
    def extract(self, lease_id, document_path):
        pass


class DummyExtractor(ExtractorInteface):
    def extract(self, lease_id, document_path):
        return dummy_results


class GoogleVisionExtractor(ExtractorInteface):
    def __init__(self):
        self.bucket_file_storage_path = "gs://cs446-lease-files/"
        self.bucket_paragraph_output_path = "gs://cs446-lease-text/"
        self.bucket_name = "cs446-lease-files"
        self.credentials_relative_file_location = "../.gcp/servicekey"

    def _detect_document(self, gcs_source_uri, gcs_destination_uri):
        # Get location of current file
        dirname = os.path.dirname(__file__)
        # Get credentials file location by relative path
        credentials_file_location = os.path.join(dirname, "../.gcp/servicekey")

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file_location
        mime_type = "application/pdf"

        # How many pages should be grouped into each json output file.
        batch_size = 8

        client = vision.ImageAnnotatorClient()

        feature = vision.types.Feature(
            type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION
        )

        gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
        input_config = vision.types.InputConfig(
            gcs_source=gcs_source, mime_type=mime_type
        )

        gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
        output_config = vision.types.OutputConfig(
            gcs_destination=gcs_destination, batch_size=batch_size
        )

        async_request = vision.types.AsyncAnnotateFileRequest(
            features=[feature], input_config=input_config, output_config=output_config
        )

        operation = client.async_batch_annotate_files(requests=[async_request])

        print("Waiting for the operation to finish.")
        operation.result(timeout=420)

        # Once the request has completed and the output has been
        # written to GCS, we can list all the output files.
        storage_client = storage.Client()

        match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
        bucket_name = match.group(1)
        prefix = match.group(2)

        bucket = storage_client.get_bucket(bucket_name)

        # List objects with the given prefix.
        blob_list = list(bucket.list_blobs(prefix=prefix))
        print("Output files:")
        for blob in blob_list:
            print(blob.name)

        # Process the first output file from GCS.
        # Since we specified batch_size=2, the first response contains
        # the first two pages of the input file.
        output = blob_list[0]

        json_string = output.download_as_string()
        response = json_format.Parse(json_string, vision.types.AnnotateFileResponse())

        paragraph_array = []

        for my_response in response.responses:
            annotation = my_response.full_text_annotation
            for page in annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        para = ""
                        for word in paragraph.words:
                            for symbol in word.symbols:
                                para = para + symbol.text
                            para = para + " "
                        paragraph_array.append(para)
        return paragraph_array

    def _upload_file_to_bucket(self, lease_id, document_path):
        """Uploads a file to the bucket."""
        source_file_name = document_path
        destination_blob_name = str(lease_id)

        # Get location of current file
        dirname = os.path.dirname(__file__)
        credentials_file_location = os.path.join(
            dirname, self.credentials_relative_file_location
        )

        storage_client = storage.Client.from_service_account_json(
            credentials_file_location
        )
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))

    def extract(self, lease_id, document_path):

        if get_file_type(document_path) != "pdf":
            tmp_path = "/tmp/{}.pdf".format(uuid4())
            try:
                ImageConversionService.convert(document_path, tmp_path)
                document_path = tmp_path
            except Exception as _:
                raise ExtractorImageConversionFailed()

        self._upload_file_to_bucket(lease_id, document_path)
        paragraphs = self._detect_document(
            self.bucket_file_storage_path + str(lease_id),
            self.bucket_paragraph_output_path + str(lease_id),
        )

        return paragraphs
