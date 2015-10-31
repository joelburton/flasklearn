import os
import time
from blogapp.extensions import celery
from blogapp.models import Reminder


@celery.task()
def log(msg):
    time.sleep(5)
    return msg


import smtplib
from email.mime.text import MIMEText


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def remind(self, pk):
    reminder = Reminder.query.get(pk)
    msg = MIMEText(reminder.text)

    msg['Subject'] = "Your reminder"
    msg['From'] = "joel@joelburton.com"
    msg['To'] = reminder.email

    try:
        smtp_server = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com')
        smtp_server.starttls()
        smtp_server.login('AKIAIDQJEDLNTSM73G7A', os.environ['EMAIL_HOST_PASSWORD'])
        smtp_server.sendmail(
            "joel@joelburton.com",
            [reminder.email],
            msg.as_string()
        )
        smtp_server.close()

        return
    except Exception, e:
        self.retry(exc=e)


def on_reminder_save(mapper, connect, self):
    print "ORS", mapper, connect, self, self.id, self.date
    remind.apply_async(args=(self.id,), eta=self.date)