from tasks.task_1_celery import mark_as_absent,load_data,save_data
from datetime import datetime

def start_exam(pk):
    exam_data = load_data()
    exam_data.append({"pk": pk, "status": "started"})
    save_data(exam_data)
    mark_as_absent.apply_async(args=[pk], countdown=120) 
    print(f"Exam {pk} started at {datetime.now()}")
