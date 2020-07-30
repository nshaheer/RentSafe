from infrastructure.entity_recognizer import (
    EntityRecogInterface,
    RecognizerResultsNotAvailable,
)
from infrastructure.classifier import ClassifierInterface, ClassifierResultsNotAvailable
from infrastructure.storage import StorageInterface

from services.analysis import AnalysisService


class ProcessPendingAnalysis:
    def __init__(
        self,
        recognizer: EntityRecogInterface,
        classifier: ClassifierInterface,
        storage: StorageInterface,
    ):
        self.recognizer = recognizer
        self.classifier = classifier
        self.storage = storage

    def execute(self):
        pending_analysis = self.storage.get_pending_analysis()

        for analysis in pending_analysis:
            self._process(analysis)

    def _process(self, analysis):
        try:
            c_results = self.classifier.get_results(analysis["ClassificationJobId"])
            r_results = self.recognizer.get_results(analysis["EntityRecognitionJobId"])

            c_analysis = AnalysisService.analyze_classification_results(c_results)
            r_analysis = AnalysisService.analyze_recognition_results(r_results)

            lease_update = {}
            lease_update.update(c_analysis)
            lease_update.update(r_analysis)
            lease_update.update({"Status": "COMPLETED"})

            self.storage.update_lease(analysis["_id"], lease_update)

        except (ClassifierResultsNotAvailable, RecognizerResultsNotAvailable) as _:
            # Classification and Entity Recognition results are not available yet
            pass
