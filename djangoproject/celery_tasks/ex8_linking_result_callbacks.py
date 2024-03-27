import sys

from djangoproject.celery import app


@app.task(queue="tasks")
def long_running_task():
    raise ValueError("Something went wrong my boy")


@app.task(queue="tasks")
def process_task_result():
    sys.stdout.write("process task result")
    sys.stdout.flush()


@app.task(queue="tasks")
def error_handler(task_id, exc, traceback):
    sys.stdout.write(">>>>")
    sys.stdout.write(str(exc))
    sys.stdout.write(">>>>")
    sys.stdout.flush()


### Define sequence of tasks
def run_task():
    long_running_task.apply_async(
        link=[
            process_task_result.s(),
        ],
        link_error=[
            error_handler.s(),
        ],
    )
