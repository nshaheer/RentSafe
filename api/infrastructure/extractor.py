from abc import ABCMeta, abstractmethod


class ExtractorInteface(metaclass=ABCMeta):
    @abstractmethod
    def start_extraction(self, lease_id, document_path):
        pass

    @abstractmethod
    def check_extraction_status(self, job_id):
        pass

    @abstractmethod
    def get_extraction_results(self, job_id):
        pass


class DummyExtractor(ExtractorInteface):
    def start_extraction(self, lease_id, document_path):
        return 1

    def check_extraction_status(self, job_id):
        return "COMPLETE"

    def get_extraction_results(self, job_id):
        return []
