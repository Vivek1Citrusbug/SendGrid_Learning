import os
import shutil
from fastapi import FastAPI, UploadFile, HTTPException
from Extra_task.myapp.tasks import *
from myapp.celery_config import celery_app

app = FastAPI()

UPLOAD_DIR = "./uploads"

@app.post("/process-dataset/")
async def process_dataset(file:UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    chain = (validate_data.s(file_path) |
             transform_data.s() |
             analyze_data.s() |
             generate_report.s())
    
    result = chain.apply_async()
    
    return {"task_id": result.id, "message": "Processing started."}

@app.get("/task-status/{task_id}")
async def task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}
