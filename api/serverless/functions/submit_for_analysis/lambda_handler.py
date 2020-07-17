from use_cases.submit_for_analysis import SubmitForAnalysis
from storage import MongoStorage
from classifier import DummyClassifier
from entity_recognizer import DummyEntityRecog


def lambda_handler(event, context):
    print(event)
    print(context)

    # lease_classifier = DummyClassifier()
    # lease_entity_recog = DummyEntityRecog()
    # lease_storage = MongoStorage()

    # use_case = SubmitForAnalysis(lease_storage, lease_classifier, lease_entity_recog)
    # use_case.execute(request)
