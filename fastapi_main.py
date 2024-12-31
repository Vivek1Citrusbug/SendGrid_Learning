import json
from celery.result import AsyncResult
from fastapi import FastAPI, BackgroundTasks, HTTPException
from tasks.task_3_celery import delayed_task
from datetime import datetime
from tasks.task_1_celery import mark_as_absent
from generals import save_data, load_data
from datetime import timedelta

app = FastAPI()


@app.post("/task-3/")
async def run_task(parameter: str):
    delayed_task.apply_async(args=[parameter])
    return {
        "message": "Thank you for submiting your email! we will get back to you with your email in 20 sec On our console"
    }


@app.post("/start_exam/{pk}")
async def start_exam(pk: int):
    """
    Starting the exam for the given pk
    """

    exam_data = load_data()

    if any(exam["pk"] == pk for exam in exam_data):
        raise HTTPException(status_code=400, detail="Exam already started")

    exam_data.append({"pk": pk, "status": "started"})
    save_data(exam_data)
    now = datetime.now()
    eta = now + timedelta(seconds=10.00)
    print("########## Now : ", now, "######### ETA : ", eta)

    ## can also use countdown in place of eta.

    task = mark_as_absent.apply_async(
        args=[pk], eta=now + timedelta(seconds=10.00), task_id=str(pk)
    )

    return {"msg": f"Exam {pk} started at {datetime.now()}", "task_id": task.id}


@app.post("/update_exam_result/{pk}")
async def update_exam_result(pk: int, status: str):
    """
    Changing the result of the given primary key before 120 seconds.
    """

    if status not in ["pass", "fail"]:
        raise HTTPException(
            status_code=400, detail="Invalid status. Use 'pass' or 'fail'."
        )

    exam_data = load_data()
    exam = next((exam for exam in exam_data if exam["pk"] == pk), None)

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")

    exam["status"] = status
    save_data(exam_data)

    if pk:
        task = AsyncResult(str(pk))
        if task.status == "PENDING":
            task.revoke(terminate=True)
            print(f"Scheduled task for exam {pk} canceled.")

    return {"msg": f"Exam {pk} result updated to {status}."}
