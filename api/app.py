# API Server

import os
import json

from celery.schedules import crontab
from flask import Flask, request, Response, redirect, url_for
from werkzeug.utils import secure_filename

from infrastructure.classifier import AwsComprehendClassifier
from infrastructure.storage import MongoStorage
from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer
from infrastructure.extractor import GoogleVisionExtractor

from request import Request

from use_cases.submit_lease_for_analysis import SubmitLeaseForAnalysis
from use_cases.submit_text_for_analysis import SubmitTextForAnalysis
from use_cases.process_pending_analysis import ProcessPendingAnalysis
from use_cases.get_analysis_results import GetAnalysis

from utils import allowed_file

from celery_app import make_celery


app = Flask(__name__)
app.config.update(
    UPLOAD_FOLDER="/tmp",
    CELERY_BROKER_URL="redis://redis:6379",
    CELERY_RESULT_BACKEND="redis://redis:6379",
    CELERYBEAT_SCHEDULE={
        "process-pending-analysis": {
            "task": "app.task_process_pending_analysis",
            # Every minute
            "schedule": crontab(minute="*"),
        }
    },
)

bucket = "rent-safe"

storage = MongoStorage()
extractor = GoogleVisionExtractor()
recognizer = AWSComprehendEntityRecognizer(bucket)
classifier = AwsComprehendClassifier(bucket)

celery = make_celery(app)


@celery.task()
def task_extract_paragraphs(lease_id, file_path):
    paragraphs = extractor.extract(lease_id, file_path)

    submit = SubmitTextForAnalysis(recognizer, classifier, storage)
    submit.execute(Request({"lease_id": lease_id, "paragraphs": paragraphs}))


@celery.task()
def task_process_pending_analysis():
    background = ProcessPendingAnalysis(recognizer, classifier, storage)
    background.execute()


@app.route("/", methods=["GET"])
def root():
    return "Rent Safe API"


@app.route("/leases", methods=["POST"])
def submit_lease_for_analysis():
    if "file" not in request.files:
        return {"status": "failed", "message": "No file provided"}

    lease_doc = request.files["file"]

    if lease_doc and allowed_file(lease_doc.filename):
        filename = secure_filename(lease_doc.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        lease_doc.save(filepath)

        submit_lease_for_analysis = SubmitLeaseForAnalysis(storage)
        response = submit_lease_for_analysis.execute(
            Request({"lease_file_path": filepath})
        )

        # Celery needs a String instead of an ObjectId
        lease_id = str(response.data["Lease"]["Id"])
        task_extract_paragraphs.delay(lease_id, filepath)

        return Response(
            json.dumps(response.data, default=str), mimetype="application/json"
        )

    return {"status": "failed", "message": "invalid file"}


@app.route("/leases/<lease_id>", methods=["GET"])
def get_analysis_results(lease_id):
    get_analysis = GetAnalysis(storage, classifier, recognizer)
    response = get_analysis.execute(Request({"lease_id": lease_id}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")