from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer


def get_recog_results():

    recog = AWSComprehendEntityRecognizer("rent-safe")
    recog.get_results("a910c923f9227f50bac105c59a1e821d")


from infrastructure.classifier import AwsComprehendClassifier


def get_classifier_results():

    cls = AwsComprehendClassifier("rent-safe")
    cls.get_results("b921035b3e9b0cda1f9536fceecce0da")
