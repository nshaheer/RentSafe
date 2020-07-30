# API Server

import os
import json

from celery.schedules import crontab
from flask import Flask, request, Response, redirect, url_for, json
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException

from infrastructure.classifier import AwsComprehendClassifier
from infrastructure.storage import MongoStorage
from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer
from infrastructure.extractor import GoogleVisionExtractor

from request import Request

from use_cases.submit_lease_for_analysis import SubmitLeaseForAnalysis
from use_cases.submit_text_for_analysis import SubmitTextForAnalysis
from use_cases.process_pending_analysis import ProcessPendingAnalysis
from use_cases.get_analysis_results import GetAnalysis
from use_cases.get_lease_thumbnail import GetLeaseThumbnail

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


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {"code": e.code, "name": e.name, "description": e.description,}
    )
    response.content_type = "application/json"
    return response


bucket = "rent-safe"


def init_infrastucture():
    storage = MongoStorage()
    extractor = GoogleVisionExtractor()
    recognizer = AWSComprehendEntityRecognizer(bucket)
    classifier = AwsComprehendClassifier(bucket)

    return {
        "Storage": storage,
        "Extractor": extractor,
        "Recognizer": recognizer,
        "Classifier": classifier,
    }


celery = make_celery(app)


@celery.task()
def task_get_lease_thumbnail(lease_id, file_path):

    get_lease_thumbnail = GetLeaseThumbnail(init_infrastucture()["Storage"])
    get_lease_thumbnail.execute(
        Request({"lease_id": lease_id, "lease_file_path": file_path})
    )


@celery.task()
def task_extract_paragraphs(lease_id, file_path):
    infra = init_infrastucture()

    paragraphs = infra["Extractor"].extract(lease_id, file_path)

    submit = SubmitTextForAnalysis(
        infra["Recognizer"], infra["Classifier"], infra["Storage"]
    )
    submit.execute(Request({"lease_id": lease_id, "paragraphs": paragraphs}))


@celery.task()
def task_process_pending_analysis():
    infra = init_infrastucture()

    background = ProcessPendingAnalysis(
        infra["Recognizer"], infra["Classifier"], infra["Storage"]
    )
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

        infra = init_infrastucture()

        submit_lease_for_analysis = SubmitLeaseForAnalysis(infra["Storage"])
        response = submit_lease_for_analysis.execute(
            Request({"lease_file_path": filepath})
        )

        # Celery needs a String instead of an ObjectId
        lease_id = str(response.data["Lease"]["Id"])
        task_extract_paragraphs.delay(lease_id, filepath)
        task_get_lease_thumbnail.delay(lease_id, filepath)

        return Response(
            json.dumps(response.data, default=str), mimetype="application/json"
        )

    return {"status": "failed", "message": "invalid file"}


@app.route("/leases/<lease_id>", methods=["GET"])
def get_analysis_results(lease_id):
    infra = init_infrastucture()

    get_analysis = GetAnalysis(
        infra["Storage"], infra["Classifier"], infra["Recognizer"]
    )
    response = get_analysis.execute(Request({"lease_id": lease_id}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")
