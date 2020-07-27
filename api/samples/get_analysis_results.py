from infrastructure.classifier import AwsComprehendClassifier
from infrastructure.storage import MongoStorage
from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer

from request import Request

from use_cases.get_analysis_results import GetAnalysis


def func():

    bucket = "rent-safe"

    recognizer = AWSComprehendEntityRecognizer(bucket)
    classifier = AwsComprehendClassifier(bucket)
    storage = MongoStorage()

    submit = GetAnalysis(storage, classifier, recognizer)

    return submit.execute(Request({"lease_id": "5f1e687af0901e8b1e58c8e0"}))
