import time
import json
from tasks.celery_app import celery_app
from generals import load_data, save_data


@celery_app.task(bind=True)
def mark_as_absent(self, pk):
    """
    Celery task to mark attendance of the given pk as absent for remaining ideal for 120 seconds after exam started
    """
    exam_data = load_data()
    exam = next((exam for exam in exam_data if exam["pk"] == pk), None)
    if exam and exam["status"] == "started":
        exam["status"] = "absent"
        save_data(exam_data)
        print(f"Exam {pk} status updated to absent.")
    else:
        print(f"Exam {pk} result already received or task already executed.")
