from infrastructure.classifier import AwsComprehendClassifier
from infrastructure.storage import MongoStorage
from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer

from request import Request

from use_cases.submit_for_analysis import SubmitForAnalysis


def func():

    bucket = "rent-safe"

    recognizer = AWSComprehendEntityRecognizer(bucket)
    classifier = AwsComprehendClassifier(bucket)
    storage = MongoStorage()

    paragraphs = [
        "865 Laurelwood Drive",
        "KW for Rent",
        "Pets - No animals, birds, reptiles, or pets of any kind will be kept on or about the premises without the written permission of the Landlord.",
    ]

    submit = SubmitForAnalysis(storage, classifier, recognizer)

    submit.execute(Request({"paragraphs": paragraphs}))
