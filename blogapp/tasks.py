import os
import time

from flask.ext.mail import Message

from blogapp.extensions import celery, mail
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

    msg = Message("Your reminder", sender="joel@joelburton.com", recipients=[reminder.email])
    msg.body = reminder.text

    try:
        mail.send(msg)
    except Exception, e:
        self.retry(exc=e)


def on_reminder_save(mapper, connect, self):
    print "ORS", mapper, connect, self, self.id, self.date
    remind.apply_async(args=(self.id,), eta=self.date)