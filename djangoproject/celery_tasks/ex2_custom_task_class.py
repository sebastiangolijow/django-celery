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


@app.task(queue="tasks")
def my_task3():
    try:
        raise ConnectionError("Connection error ocurred...")
    except ConnectionError:
        logging.error("Connection error ocurred...")
        raise ConnectionError()
    except ValueError:
        ### send something to user
        pass
