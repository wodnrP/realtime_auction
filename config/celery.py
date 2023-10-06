import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
app.conf.worker_cancel_long_running_tasks_on_connection_loss = True


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
