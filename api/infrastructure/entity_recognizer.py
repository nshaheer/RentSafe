from uuid import uuid4
from abc import ABCMeta, abstractmethod

import boto3


class EntityRecogInterface(metaclass=ABCMeta):
    def recognize(self, paragraphs):
        pass


class DummyEntityRecog(EntityRecogInterface):
    def recognize(self, paragraphs):
        # Upload to S3 - CSV in valid format
        # Call AWS Boto3 Comprehend Job
        return 1


class AWSComprehendEntityRecognizer(EntityRecogInterface):
    def __init__(self, bucket):
        self.bucket = bucket

    @staticmethod
    def _compile_txt_string(paragraphs):
        return "\n".join(paragraphs)

    def _upload_txt_to_s3(self, txt_string):
        s3_key = "lease-data/input/{}.txt".format(str(uuid4()))

        session = boto3.Session(
            aws_access_key_id="AKIAQCL63YTSKPN5MAFU",
            aws_secret_access_key="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",
            region_name="ca-central-1",
        )

        s3 = session.resource("s3")
        s3_object = s3.Object(self.bucket, s3_key)
        s3_object.put(Body=txt_string.encode("utf-8"))

        return s3_key

    def _schedule_recognition_job(self, s3_key):
        s3_path = self.bucket + "/" + s3_key
        return s3_path

    def recognize(self, paragraphs):
        txt_string = self._compile_txt_string(paragraphs)
        s3_key = self._upload_txt_to_s3(txt_string)

        return self._schedule_recognition_job(s3_key)
