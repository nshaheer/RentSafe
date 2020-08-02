from celery.schedules import crontab


class Config:
    CELERY_BROKER_URL = ("redis://redis:6379",)
    CELERY_RESULT_BACKEND = ("redis://redis:6379",)
    CELERYBEAT_SCHEDULE = (
        {
            "process-pending-analysis": {
                "task": "app.task_process_pending_analysis",
                # Every minute
                "schedule": crontab(minute="*"),
            }
        },
    )
    LEASE_DOCS_FOLDER = "/tmp/lease-docs"
