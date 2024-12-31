# exam_result.py
from tasks.task_1_celery import update_exam_status

def update_exam(pk, status):
    update_exam_status.apply_async(args=[pk, status])
    print(f"Exam {pk} status updated to {status}")
