from uuid import uuid4
from abc import ABCMeta, abstractmethod

from .dummy_results import extraction_job_results as dummy_results


class ExtractorException(Exception):
    pass


class ExtractorResultsNotAvailable(ExtractorException):
    pass


class ExtractorInteface(metaclass=ABCMeta):
    @abstractmethod
    def extract(self, lease_id, document_path):
        pass

    @abstractmethod
    def get_results(self, job_id):
        pass


class DummyExtractor(ExtractorInteface):
    def extract(self, lease_id, document_path):
        return str(uuid4())

    def get_results(self, job_id):
        return dummy_results
