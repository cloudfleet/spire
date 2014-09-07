from __future__ import absolute_import
import logging

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def start_blimp(blimp):
    #TODO: only notify admin if the automatic start didn't succeed
    logging.debug('0. notify admins...')
    blimp.notify_admin()
    result = blimp.start() # tell docker to start it
    logging.debug(result)
    return

@shared_task
def stop_blimp(blimp):
    blimp.stop() # stop the container
    return
