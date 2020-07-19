from response import Response
from storage import StorageInterface
from classifier import ClassifierInterface
from entity_recognizer import EntityRecogInterface


class SubmitForAnalysis:
    def __init__(
        self,
        storage: StorageInterface,
        classifier: ClassifierInterface,
        entity_recog: EntityRecogInterface,
    ):
        self.storage = storage
        self.classifier = classifier
        self.entity_recog = entity_recog

    def execute(self, request):

        paragraphs = request.paragraphs

        classification_job_id = self.classifier.classify(paragraphs)
        recog_job_id = self.entity_recog.recognize(paragraphs)

        lease_id = self.storage.add_lease(
            paragraphs=paragraphs,
            status="PENDING",
            classification_job=classification_job_id,
            recog_job=recog_job_id,
        )

        return Response({"lease_id": lease_id})
