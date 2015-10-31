import time

from blogapp.extensions import celery


@celery.task()
def log(msg):
    time.sleep(5)
    return msg
