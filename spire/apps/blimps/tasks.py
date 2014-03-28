from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def start_blimp(blimp):
    print(blimp.start()) # tell docker to start it
    return

@shared_task
def stop_blimp(blimp):
    blimp.stop() # stop the container
    return
