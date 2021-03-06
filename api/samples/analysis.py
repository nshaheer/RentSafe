from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer
from infrastructure.classifier import AwsComprehendClassifier
from services.analysis import AnalysisService


def analyze_recog_results():

    recog = AWSComprehendEntityRecognizer("rent-safe")
    results = recog.get_results("2cd66f26dd8ec2c4eeb3446d8b3d4baa")
    analysis = AnalysisService.analyze_recognition_results(results)
    print(analysis)


def analyze_classifier_results():

    cls = AwsComprehendClassifier("rent-safe")
    results = cls.get_results("b921035b3e9b0cda1f9536fceecce0da")
    analysis = AnalysisService.analyze_classification_results(results)
    print(analysis)
