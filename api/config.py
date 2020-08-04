class Config:
    CELERY_BROKER_URL = "redis://redis:6379"
    CELERY_RESULT_BACKEND = "redis://redis:6379"
    LEASE_DOCS_FOLDER = "/tmp/lease-docs"
    AWS_S3_BUCKET = "rent-safe"
    AWS_COMPREHEND_ROLE_ARN = "arn:aws:iam::005097899236:role/RentSafeAWSComprehendRole"
    AWS_COMPREHEND_CLASSIFIER_ARN = "arn:aws:comprehend:ca-central-1:005097899236:document-classifier/RentalClassifier-v1-0-0"
