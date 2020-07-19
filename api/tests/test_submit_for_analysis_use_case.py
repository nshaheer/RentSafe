from use_cases.submit_for_analysis import SubmitForAnalysis

from services.storage import MemStorage
from services.classifier import DummyClassifier
from services.entity_recognizer import DummyEntityRecog

# Write Pytests

test_storage = MemStorage()
test_classifier = DummyClassifier()
test_entity_recog = DummyEntityRecog()

use_case = SubmitForAnalysis(test_storage, test_classifier, test_entity_recog)
