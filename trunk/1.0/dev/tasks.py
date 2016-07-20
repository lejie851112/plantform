from time import sleep
from celery import task, current_task

@task()
def do_work():
 """ Get some rest, asynchronously, and update the state all the time """
 for i in range(100):
  sleep(0.1)
  current_task.update_state(state='PROGRESS',
   meta={'current': i, 'total': 100})