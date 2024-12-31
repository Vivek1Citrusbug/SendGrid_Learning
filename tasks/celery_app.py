from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379/0")
celery_app.conf.result_backend = "redis://localhost:6379/0"

# add tasks according to their path here.
celery_app.autodiscover_tasks(
    ["tasks.task_1_celery.delayed_task"]
)
