from datetime import timedelta

from celery.schedules import crontab

from djangoproject.celery import app


app.conf.beat_schedule = {
    "task1": {
        "task": "djangoproject.celery_tasks.ex12_task_schedule_custom.task1",
        "schedule": crontab(minute="0-59/10", hour="0-5", day_of_week="mon"),
        "kwargs": {"foo": "bar"},
        "args": (1, 2),
        "options": {"queue": "tasks", "priority": 5},
    },
    "task2": {
        "task": "djangoproject.celery_tasks.ex12_task_schedule_custom.task2",
        "schedule": crontab(),  ### run every minute
    },
}


@app.task(queue="tasks")
def task1(a, b, **kwargs):
    result = a + b
    print("running task 1 ", result)


@app.task(queue="tasks")
def task2():
    print("running task 2")
