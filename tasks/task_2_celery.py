# #############################################################################################
# ### Task : Create recurring celery task that simulates email sending for every 20 seconds. ###
# #############################################################################################

import smtplib
from celery import shared_task, Celery
from celery.schedules import crontab
from email.message import EmailMessage

app = Celery("tasks.task_2_celery", broker="redis://localhost:6379", backend='redis://localhost:6379')


@app.task
def send_email_celery():
    """Function to send email address at every 20 seconds"""

    msg = EmailMessage()
    try:
        print("########### Inside email service ##################")
        msg["Subject"] = f"Testing email functionality for every 20 seconds"
        msg["From"] = "vivek1.citrusbug@gmail.com"
        msg["To"] = "vivek1.citrusbug@gmail.com"
        msg.set_content("This is a test email sent every 20 seconds.")
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 587) as smtp:
            smtp.starttls()
            smtp.login("a5634ec7138a39", "63bbdfc9cce507") ## Used maitrap for mail service.thats why not used environment variables.
            smtp.send_message(msg)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Configure periodic tasks
app.conf.beat_schedule = {
    "run-periodic-task-every-20-seconds": {
        "task": "tasks.task_2_celery.send_email_celery",
        "schedule": 20.0,
    },
}

app.conf.timezone = "Asia/Kolkata"
