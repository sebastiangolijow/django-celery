from datetime import timedelta

from djangoproject.celery import app


app.conf.beat_schedule = {
    "task1": {
        "task": "djangoproject.celery_tasks.ex12_task_schedule_custom.task1",
        "schedule": timedelta(seconds=5),
        "kwargs": {"foo": "bar"},
        "args": {1, 2},
        "options": {"queue": "tasks", "priority": 5},
    },
    "task2": {
        "task": "djangoproject.celery_tasks.ex12_task_schedule_custom.task2",
        "schedule": timedelta(seconds=10),
    },
}


@app.task(queue="tasks")
def task1(a, b, **kwargs):
    result = a + b
    print("running task 1 ", result)


@app.task(queue="tasks")
def task2():
    print("running task 2")
