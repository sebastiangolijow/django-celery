import logging

from celery import Task

from djangoproject.celery import app


class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, ConnectionError):
            logging.error("connection error...")
        else:
            print("{0!r} failes: {1!r}".format(task_id, exc))


app.Task = CustomTask


@app.task(
    queue="tasks",
    autoretry_for=(ConnectionError,),
    default_retry_delay=5,
    retry_kwargs={"max_retries": 5},
)
def my_task4():
    raise ConnectionError("Connection error ocurred...")
