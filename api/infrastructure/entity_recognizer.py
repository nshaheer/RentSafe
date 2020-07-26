from abc import ABCMeta, abstractmethod


class EntityRecogInterface(metaclass=ABCMeta):
    def recognize(self, paragraphs):
        pass


class DummyEntityRecog(EntityRecogInterface):
    def recognize(self, paragraphs):
        # Upload to S3 - CSV in valid format
        # Call AWS Boto3 Comprehend Job
        return 1


class AWSComprehendEntityRecognizer(EntityRecogInterface):
    @staticmethod
    def _compile_csv_string(paragraphs):
        pass

    @staticmethod
    def _upload_csv_to_s3(csv_string):
        pass

    @staticmethod
    def _schedule_recognition_job(s3_path):
        pass

    def recognize(self, paragraphs):
        csv_string = self._compile_csv_string(paragraphs)
        s3_path = self._upload_csv_to_s3(csv_string)

        return self._schedule_recognition_job(s3_path)
