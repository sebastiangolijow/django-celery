import logging

from djangoproject.celery import app


logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(actime)s %(levelname)s %(message)s",
)


@app.task(queue="tasks")
def my_task2():
    try:
        raise ConnectionError("Connection error ocurred...")
    except ConnectionError:
        logging.error("Connection error ocurred...")
        raise ConnectionError()
    except ValueError:
        ### send something to user
        pass
