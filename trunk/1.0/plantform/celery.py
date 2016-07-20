from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings   
from celery import platforms

platforms.C_FORCE_ROOT = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantform.settings')
app = Celery('plantform')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))  #dumps its own request information

