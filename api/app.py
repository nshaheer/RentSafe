# API Server

import os
import json

from celery.schedules import crontab
from flask import Flask, request, Response, redirect, url_for, json
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from infrastructure.classifier import AwsComprehendClassifier
from infrastructure.storage import MongoStorage
from infrastructure.entity_recognizer import AWSComprehendEntityRecognizer
from infrastructure.extractor import GoogleVisionExtractor, ExtractorException

from request import Request

from use_cases.submit_lease_for_analysis import SubmitLeaseForAnalysis
from use_cases.submit_text_for_analysis import SubmitTextForAnalysis
from use_cases.process_pending_analysis import ProcessPendingAnalysis
from use_cases.get_analysis_results import GetAnalysis
from use_cases.get_lease_thumbnail import GetLeaseThumbnail
from use_cases.email_lease_analysis import EmailLeaseAnalysis

from utils import allowed_file

from celery_app import make_celery

from config import Config

sentry_sdk.init(
    dsn="https://ad90b18ea8cc45408888226a015512a6@o429995.ingest.sentry.io/5377755",
    integrations=[FlaskIntegration()],
)

app = Flask(__name__)
app.config.from_object(Config())
app.config.update(
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
    recognizer = AWSComprehendEntityRecognizer(app.config["AWS_S3_BUCKET"])
    classifier = AwsComprehendClassifier(
        app.config["AWS_S3_BUCKET"],
        app.config["AWS_COMPREHEND_ROLE_ARN"],
        app.config["AWS_COMPREHEND_CLASSIFIER_ARN"],
    )

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

    try:
        paragraphs = infra["Extractor"].extract(lease_id, file_path)
        submit = SubmitTextForAnalysis(
            infra["Recognizer"], infra["Classifier"], infra["Storage"]
        )
        submit.execute(Request({"lease_id": lease_id, "paragraphs": paragraphs}))
    except ExtractorException as e:
        print(e)
        # Set Status for Lease to FAILED


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
        filepath = os.path.join(app.config["LEASE_DOCS_FOLDER"], filename)
        lease_doc.save(filepath)

        infra = init_infrastucture()

        submit_lease_for_analysis = SubmitLeaseForAnalysis(infra["Storage"])
        response = submit_lease_for_analysis.execute(
            Request({"lease_file_path": filepath, "file_name": filename})
        )

        # Celery needs a String instead of an ObjectId
        lease_id = str(response.data["Lease"]["Id"])
        task_extract_paragraphs.delay(lease_id, filepath)
        task_get_lease_thumbnail.delay(lease_id, filepath)

        return Response(
            json.dumps(response.data, default=str), mimetype="application/json"
        )

    return {"status": "failed", "message": "invalid file"}


@app.route("/leases/<lease_id>/email", methods=["POST"])
def email_lease_analysis(lease_id):
    infra = init_infrastucture()

    email_lease = EmailLeaseAnalysis(infra["Storage"])
    response = email_lease.execute(
        Request({"lease_id": lease_id, "to_email": request.json["email"]})
    )

    return response.data


@app.route("/leases/<lease_id>", methods=["GET"])
def get_analysis_results(lease_id):
    infra = init_infrastucture()

    get_analysis = GetAnalysis(infra["Storage"])
    response = get_analysis.execute(Request({"lease_id": lease_id}))

    return Response(json.dumps(response.data, default=str), mimetype="application/json")


@app.route("/questionnaire", methods=["POST"])
def collect_questionnaire_answers():
    infra = init_infrastucture()

    infra["Storage"].add_questionnaire_submission(request.json)

    return {"status": "SUCCESS"}
