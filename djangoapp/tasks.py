import time

from celery import shared_task
from django.core.management import call_command


@shared_task(task_rate_limit=10)
def task1(queue="celery"):
    time.sleep(3)
    return


@shared_task
def task2(queue="celery:1"):
    time.sleep(3)
    return


@shared_task
def task3(queue="celery:2"):
    time.sleep(3)
    return


@shared_task
def manage_command(queue="tasks"):
    call_command("test_command")
    return


# @app.task(queue="tasks")
# def t3():
#     time.sleep(3)
#     return
