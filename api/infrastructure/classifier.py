import json
import os
import tarfile
import zipfile
from uuid import uuid4
from abc import ABCMeta, abstractmethod

import requests
import boto3
from s3urls import parse_url

from .dummy_results import classification_job_results as dummy_results


class ClassifierException(Exception):
    pass


class ClassifierResultsNotAvailable(ClassifierException):
    pass


class ClassifierInterface(metaclass=ABCMeta):
    @abstractmethod
    def classify(self, paragraphs):
        pass

    @abstractmethod
    def get_results(self, job_id):
        pass


class DummyClassifier(ClassifierInterface):
    def classify(self, paragraphs):
        # Upload to S3 - CSV in valid format
        # Call AWS Boto3 Custom Comprehend Job
        return 1

    def get_results(self, job_id):
        return dummy_results


class AwsComprehendClassifier(ClassifierInterface):
    def __init__(self, bucket):

        self.role_arn = "arn:aws:iam::005097899236:role/RentSafeAWSComprehendRole"
        self.classifier_arn = "arn:aws:comprehend:ca-central-1:005097899236:document-classifier/cs446-training"

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

    def _schedule_classification_job(self):
        s3_input_path = "s3://{}/lease-data/input/{}.txt".format(self.bucket, self._id)
        s3_output_path = "s3://{}/lease-data/output/".format(self.bucket)

        client = self.session.client("comprehend")

        response = client.start_document_classification_job(
            InputDataConfig={"S3Uri": s3_input_path, "InputFormat": "ONE_DOC_PER_LINE"},
            OutputDataConfig={"S3Uri": s3_output_path,},
            JobName="Classification-Job-{}".format(self._id),
            DataAccessRoleArn=self.role_arn,
            DocumentClassifierArn=self.classifier_arn,
        )

        return response["JobId"]

    def classify(self, paragraphs):
        txt_string = self._compile_txt_string(paragraphs)
        self._upload_txt_to_s3(txt_string)

        return self._schedule_classification_job()

    def get_results(self, job_id):

        response = self.session.client(
            "comprehend"
        ).describe_document_classification_job(JobId=job_id)

        status = response["DocumentClassificationJobProperties"]["JobStatus"]
        if status != "COMPLETED":
            raise ClassifierResultsNotAvailable(status)

        # Parse S3 Output Uri
        output_s3_uri = response["DocumentClassificationJobProperties"][
            "OutputDataConfig"
        ]["S3Uri"]
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
            tar.extractall(path="/tmp/{}/".format(self._id))

        results = []
        for name in names:
            # Parse JSON in output
            with open("/tmp/{}/{}".format(self._id, name)) as json_output:
                results.extend([json.loads(line) for line in json_output.readlines()])

        return results
