from abc import ABCMeta, abstractmethod


class ClassifierInterface(metaclass=ABCMeta):
    def classify(self, paragraphs):
        pass


class DummyClassifier(ClassifierInterface):
    def classify(self, paragraphs):
        # Upload to S3 - CSV in valid format
        # Call AWS Boto3 Custom Comprehend Job
        return 1


class AwsComprehendClassifier(ClassifierInterface):
    @staticmethod
    def _compile_csv_string(paragraphs):
        pass

    @staticmethod
    def _upload_csv_to_s3(csv_string):
        pass

    @staticmethod
    def _schedule_classification_job(s3_path):
        pass

    def classify(self, paragraphs):
        csv_string = self._compile_csv_string(paragraphs)
        s3_path = self._upload_csv_to_s3(csv_string)

        return self._schedule_classification_job(s3_path)
