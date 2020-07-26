from abc import ABCMeta, abstractmethod


class EntityRecogInterface(metaclass=ABCMeta):
    def recognize(self, paragraphs):
        pass


class DummyEntityRecog(EntityRecogInterface):
    def recognize(self, paragraphs):
        # Upload to S3 - CSV in valid format
        # Call AWS Boto3 Comprehend Job
        return 1
