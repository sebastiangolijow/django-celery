from djangoproject.celery import app


@app.task(queue="tasks")
def my_task():
    pass
