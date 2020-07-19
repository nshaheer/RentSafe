from abc import ABCMeta, abstractmethod


class ClassifierInterface(metaclass=ABCMeta):
    def classify(self, lease_id, paragraphs):
        pass


class DummyClassifier(ClassifierInterface):
    def classify(self, lease_id, paragraphs):
        # Upload to S3 - CSV in valid format
        # Call AWS Boto3 Customer Comprehend Job
        return 1
