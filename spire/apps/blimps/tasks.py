from __future__ import absolute_import
import logging

from celery import shared_task, task
from django.core.mail import send_mail

from . import lib

@shared_task
def start_blimp(blimp):
    #TODO: only notify admin if the automatic start didn't succeed
    logging.info('0. notify admins...')
    blimp.notify_admin()
    result = blimp.start() # tell docker to start it
    logging.debug(result)
    return

@shared_task
def stop_blimp(blimp):
    blimp.stop() # stop the container
    return

@shared_task
def activate_blimp(blimp):
    blimp.notify_user_blimp_ready()
    return

@task
def notify_admin(blimp):
    logging.info('notify admins')
    blimp.notify_admin()

@task
def create_pagekite_account(blimp):
    logging.info('create pagekite account')
    lib.create_pagekite_account(blimp)
