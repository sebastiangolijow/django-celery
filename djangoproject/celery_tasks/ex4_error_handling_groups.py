from celery import group

from djangoproject.celery import app


@app.task(queue="tasks")
def my_task5(number):
    if number == 3:
        raise ValueError("error number is invalid")
    return number * 2


def handle_result(result):
    if result.successful():
        print("task completed ", result.get())
    elif result.failed() and isinstance(result.result, ValueError):
        print("task failed ", result.result)
    elif result.status == "REVOKED":
        print("task was revoked ", result.id)


def run_tasks():
    task_group = group(my_task5.s(i) for i in range(5))
    result_group = task_group.apply_async()
    ### get wait until all task are completed
    result_group.get(disable_sync_subtasks=False, propagate=False)

    for result in result_group:
        handle_result(result)
