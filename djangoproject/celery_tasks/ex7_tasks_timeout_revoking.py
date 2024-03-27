import sys
from time import sleep

from djangoproject.celery import app


@app.task(queue="tasks", time_limit=10)
def long_running_task():
    sleep(6)
    return "task completed"


@app.task(queue="tasks", bind=True)
def process_task(self, result):
    if result is None:
        return "Task was revoked"
    else:
        return f"Task result: {result}"


def execute_task_examples():
    result = long_running_task.delay()
    try:
        task_result = result.get(timeout=40)
    except TimeoutError:
        print("task timed out...")

    task = long_running_task.delay()
    task.revoke(terminate=True)
    sleep(3)
    sys.stdout.write(task.status)

    if task.status == "REVOKED":
        process_task.delay(None)
    else:
        process_task.delay(task.result)
