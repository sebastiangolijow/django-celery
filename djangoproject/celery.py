import os
import time

from celery import Celery
from kombu import Exchange
from kombu import Queue


# from sentry_sdk.integrations.celery import CeleryIntegration


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")

app = Celery("djangoproject")

app.config_from_object("django.conf:settings", namespace="CELERY")
sentry_dsn = ""
# sentry_sdk.init(dsn=sentry_sdk, integrations=[CeleryIntegration()])

app.conf.task_queues = [
    Queue(
        "tasks",
        Exchange("tasks"),
        routing_key="tasks",
        queue_arguments={"x-max-priority": 10},
    ),
    Queue("dead_letter", routing_key="dead_letter"),
]

### does not take put the task of the queue unless it is completed
app.conf.task_acks_late = True
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1
app.conf.worker_concurrency = 1


### look for tasks.py files inside apps

base_dir = os.getcwd()
task_folder = os.path.join(base_dir, "djangoproject", "celery_tasks")

if os.path.exists(task_folder) and os.path.isdir(task_folder):
    task_modules = []
    for filename in os.listdir(task_folder):
        if filename.startswith("ex") and filename.endswith("py"):
            module_name = f"djangoproject.celery_tasks.{filename[:-3]}"

            module = __import__(module_name, fromlist=["*"])
            for name in dir(module):
                obj = getattr(module, name)
                if callable(obj) and name.startswith("my_tasks"):
                    task_modules.append(f"{module_name}.{name}")

    app.autodiscover_tasks(task_modules)

app.autodiscover_tasks()


# app.conf.task_routes = {
#     "djangoapp.tasks.task1": {"queue": "queue1"},
#     "djangoapp.tasks.task2": {"queue": "queue2"},
# }

# app.conf.task_default_rate_limit = "1/m"

# app.conf.broker_transport_options = {
#     "priority_steps": list(range(10)),
#     "sep": ":",
#     "queue_order_strategy": "priority",
# }
