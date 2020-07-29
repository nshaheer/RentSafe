# API Server

import json

from flask import Flask, request, Response

from infrastructure.extractor import DummyExtractor
from infrastructure.classifier import DummyClassifier
from infrastructure.entity_recognizer import DummyEntityRecog
from infrastructure.storage import MemStorage

from request import Request

from use_cases.submit_for_analysis import SubmitForAnalysis
from use_cases.get_analysis_results import GetAnalysis

app = Flask(__name__)

storage = MemStorage()
classifier = DummyClassifier()
recognizer = DummyEntityRecog()


@app.route("/", methods=["GET"])
def root():
    return "Rent Safe API"


@app.route("/leases", methods=["POST"])
def submit_for_analysis():
    data = request.get_json()

    extractor = DummyExtractor()
    submit = SubmitForAnalysis(extractor, storage)

    response = submit.execute(Request({"paragraphs": data["paragraphs"]}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")


@app.route("/leases/<lease_id>", methods=["GET"])
def get_analysis_results(lease_id):

    submit = GetAnalysis(storage, classifier, recognizer)

    response = submit.execute(Request({"lease_id": lease_id}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")
