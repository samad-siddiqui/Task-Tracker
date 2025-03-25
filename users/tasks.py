from celery import shared_task
from time import sleep


@shared_task
def add(x, y):
    sleep(5)
    return x + y
