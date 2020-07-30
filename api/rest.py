# API Server

import os
import json

from flask import Flask, request, Response, redirect, url_for
from werkzeug.utils import secure_filename

from infrastructure.classifier import AwsComprehendClassifier
from infrastructure.storage import MongoStorage
from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer
from infrastructure.extractor import GoogleVisionExtractor

from request import Request

from use_cases.submit_for_analysis import SubmitForAnalysis
from use_cases.get_analysis_results import GetAnalysis

from celery_app import make_celery


UPLOAD_FOLDER = "/tmp"
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config.update(
    CELERY_BROKER_URL="redis://redis:6379", CELERY_RESULT_BACKEND="redis://redis:6379"
)

celery = make_celery(app)


@app.route("/", methods=["GET"])
def root():
    return "Rent Safe API"


@app.route("/leases", methods=["POST"])
def submit_for_analysis():
    if "file" not in request.files:
        return {"status": "failed", "message": "No file provided"}

    lease_doc = request.files["file"]

    if lease_doc and allowed_file(lease_doc.filename):
        filename = secure_filename(lease_doc.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        lease_doc.save(filepath)

        bucket = "rent-safe"
        recognizer = AWSComprehendEntityRecognizer(bucket)
        classifier = AwsComprehendClassifier(bucket)

        extractor = GoogleVisionExtractor()
        storage = MongoStorage()

        submit = SubmitForAnalysis(extractor, recognizer, classifier, storage)

        response = submit.execute(Request({"lease_file_path": filepath}))

        return Response(
            json.dumps(response.data, default=str), mimetype="application/json"
        )

    return {"status": "failed", "message": "invalid file"}


@app.route("/leases/<lease_id>", methods=["GET"])
def get_analysis_results(lease_id):
    bucket = "rent-safe"

    recognizer = AWSComprehendEntityRecognizer(bucket)
    classifier = AwsComprehendClassifier(bucket)
    storage = MongoStorage()

    submit = GetAnalysis(storage, classifier, recognizer)

    response = submit.execute(Request({"lease_id": lease_id}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")
