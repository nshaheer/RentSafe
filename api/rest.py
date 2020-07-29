# API Server

import json

from flask import Flask, request, Response

from infrastructure.classifier import AwsComprehendClassifier
from infrastructure.storage import MongoStorage
from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer
from infrastructure.extractor import DummyExtractor

from request import Request

from use_cases.submit_for_analysis import SubmitForAnalysis
from use_cases.get_analysis_results import GetAnalysis

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return "Rent Safe API"


@app.route("/leases", methods=["POST"])
def submit_for_analysis():
    data = request.get_json()

    extractor = DummyExtractor()
    storage = MongoStorage()

    submit = SubmitForAnalysis(extractor, storage)

    response = submit.execute(Request({"paragraphs": data["paragraphs"]}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")


@app.route("/leases/<lease_id>", methods=["GET"])
def get_analysis_results(lease_id):
    bucket = "rent-safe"

    recognizer = AWSComprehendEntityRecognizer(bucket)
    classifier = AwsComprehendClassifier(bucket)
    storage = MongoStorage()

    submit = GetAnalysis(storage, classifier, recognizer)

    response = submit.execute(Request({"lease_id": lease_id}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")
