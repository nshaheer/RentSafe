from uuid import uuid4
from abc import ABCMeta, abstractmethod

import boto3


class EntityRecogInterface(metaclass=ABCMeta):
    def recognize(self, paragraphs):
        pass


class DummyEntityRecog(EntityRecogInterface):
    def recognize(self, paragraphs):
        return 1


class AWSComprehendEntityRecognizer(EntityRecogInterface):
    def __init__(self, bucket):

        self.role_arn = "arn:aws:iam::005097899236:role/RentSafeAWSComprehendRole"

        self._id = str(uuid4())
        self.bucket = bucket

        # User: simar-cs446-automation
        # User ARN: arn:aws:iam::005097899236:user/simar-cs446-automation
        self.session = boto3.Session(
            aws_access_key_id="AKIAQCL63YTSKPN5MAFU",
            aws_secret_access_key="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",
            region_name="ca-central-1",
        )

    @staticmethod
    def _compile_txt_string(paragraphs):
        return "\n".join(paragraphs)

    def _upload_txt_to_s3(self, txt_string):
        s3_key = "lease-data/input/{}.txt".format(self._id)

        s3 = self.session.resource("s3")
        s3_object = s3.Object(self.bucket, s3_key)
        s3_object.put(Body=txt_string.encode("utf-8"))

    def _schedule_recognition_job(self):
        s3_input_path = "s3://{}/lease-data/input/{}.txt".format(self.bucket, self._id)
        s3_output_path = "s3://{}/lease-data/output/".format(self.bucket)

        client = self.session.client("comprehend")

        response = client.start_entities_detection_job(
            InputDataConfig={"S3Uri": s3_input_path, "InputFormat": "ONE_DOC_PER_LINE"},
            OutputDataConfig={"S3Uri": s3_output_path,},
            DataAccessRoleArn=self.role_arn,
            JobName="Entity-Recog-Job-{}".format(self._id),
            LanguageCode="en",
        )

        return response["JobId"]

    def recognize(self, paragraphs):
        txt_string = self._compile_txt_string(paragraphs)
        self._upload_txt_to_s3(txt_string)

        return self._schedule_recognition_job()
