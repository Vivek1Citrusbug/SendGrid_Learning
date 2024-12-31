from fastapi import FastAPI, BackgroundTasks
# from tasks.task_3_celery import delayed_task

app = FastAPI()

# @app.post("/run-task/")
# async def run_task(parameter: str):
#     delayed_task.apply_async(args=[parameter])
#     return {"message": "Thank you for submiting your email! we will get back to you with your email in 20 sec On our console"}

