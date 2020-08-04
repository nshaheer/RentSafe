class Config:
    CELERY_BROKER_URL = "redis://redis:6379"
    CELERY_RESULT_BACKEND = "redis://redis:6379"
    LEASE_DOCS_FOLDER = "/tmp/lease-docs"
