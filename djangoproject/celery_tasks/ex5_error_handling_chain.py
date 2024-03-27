from celery import chain

from djangoproject.celery import app


@app.task(queue="tasks")
def add(x, y):
    return x + y


@app.task(queue="tasks")
def multiply(result):
    if result == 5:
        raise ValueError("Error: division by 0")
    return result * 2


### Chain stops is task fail
def run_tasks_chain():
    task_chain = chain(add.s(2, 3), multiply.s())
    result = task_chain.apply_async()
    result.get()
