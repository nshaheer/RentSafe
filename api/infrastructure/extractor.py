class GVisionDocumentTextExtractor:
    def start_extraction_job(self, lease_id, document_path):
        # Saving  {lease_id: "", extraction_job_id: "", status: "PENDING"}
        return 1

    def get_extraction_results(self, job_id):
        return ["", ""]
