import sys

from celery.signals import task_failure

from djangoproject.celery import app


"""task_prerun, task_postrun, task_success, task_failure, task_revoked, task_retry"""


@app.task(queue="tasks")
def cleanup_failed_task(task_id, *args, **kwargs):
    sys.stdout.write("CLEAN UP")


@app.task(queue="tasks")
def my_task9():
    raise ValueError("task failed")


@task_failure.connect(sender=my_task9)
def handle_task_failure(sender=None, task_id=None, **kwargs):
    cleanup_failed_task.delay(task_id)


def run_tasks():
    my_task9.apply_async()
