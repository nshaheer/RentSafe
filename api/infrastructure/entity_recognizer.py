import json
import os
import tarfile
import zipfile
from uuid import uuid4
from abc import ABCMeta, abstractmethod

import requests
import boto3
from s3urls import parse_url

from .dummy_results import recog_job_results as dummy_results


class EntityRecognitionException(Exception):
    pass


class RecognizerResultsNotAvailable(EntityRecognitionException):
    pass


class EntityRecogInterface(metaclass=ABCMeta):
    @abstractmethod
    def recognize(self, paragraphs):
        pass

    @abstractmethod
    def get_results(self, job_id):
        pass


class DummyEntityRecog(EntityRecogInterface):
    def recognize(self, paragraphs):
        return 1

    def get_results(self, job_id):
        return dummy_results


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

    def get_results(self, job_id):

        response = self.session.client("comprehend").describe_entities_detection_job(
            JobId=job_id
        )

        status = response["EntitiesDetectionJobProperties"]["JobStatus"]
        if status != "COMPLETED":
            raise RecognizerResultsNotAvailable(status)

        # Parse S3 Output Uri
        output_s3_uri = response["EntitiesDetectionJobProperties"]["OutputDataConfig"][
            "S3Uri"
        ]
        s3_parsed = parse_url(output_s3_uri)

        # Download output.tar.gz
        tmp_location = "/tmp/{}.tar.gz".format(self._id)
        self.session.client("s3").download_file(
            s3_parsed["bucket"], s3_parsed["key"], tmp_location
        )

        # Extract output.tar.gz
        names = []
        with tarfile.open(tmp_location) as tar:
            names = tar.getnames()
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path="/tmp/{}/".format(self._id))

        results = []
        for name in names:
            # Parse JSON in output
            with open("/tmp/{}/{}".format(self._id, name)) as json_output:
                results.extend([json.loads(line) for line in json_output.readlines()])

        return results
