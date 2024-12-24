import sendgrid
from django.conf import settings
from sendgrid.helpers.mail import *
import os
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


## sendgrid mail service
def mail_service(to_email, username):
    """
    Service for sending email using sendgrid api client.
    """

    message = Mail(
        from_email="vivek1.citrusbug@gmail.com",
        to_emails=to_email,
    )
    message.dynamic_template_data = {"user_name": username}
    message.template_id = os.getenv("TEMPLATE_ID")
    try:
        sg = SendGridAPIClient(os.environ.get("EMAIL_HOST_PASSWORD"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
