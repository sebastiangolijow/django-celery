from celery import group

from djangoproject.celery import app


app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True


@app.task(queue="dead_letter")
def handle_failed_task(z, exception):
    return "custom logic process"


@app.task(queue="tasks")
def my_task6(z):
    try:
        if z == 2:
            raise ValueError("error wrong number")
    except Exception as e:
        handle_failed_task.apply_async(args=(z, str(e)))


def run_Task_group():
    task_group = group(my_task6.s(1), my_task6.s(2), my_task6.s(3))
    task_group.apply_async()
