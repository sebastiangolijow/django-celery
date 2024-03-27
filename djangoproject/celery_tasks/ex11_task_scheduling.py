from datetime import timedelta

from djangoproject.celery import app


app.conf.beat_schedule = {
    "task1": {
        "task": "djangoproject.celery_tasks.ex11_task_scheduling.task1",
        "schedule": timedelta(seconds=5),
    },
    "task2": {
        "task": "djangoproject.celery_tasks.ex11_task_scheduling.task2",
        "schedule": timedelta(seconds=10),
    },
}


@app.task(queue="tasks")
def task1():
    print("running task 1")


@app.task(queue="tasks")
def task2():
    print("running task 2")
