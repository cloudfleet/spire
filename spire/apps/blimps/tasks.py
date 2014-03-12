from __future__ import absolute_import

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

from django.core.mail import send_mail

@shared_task
def start_blimp(blimp):
    send_mail('Cloudfleet blimp preview',
              'Your blimp is ready at: {}'.format(blimp.url()),
              'no-reply@cloudfleet.io',
              [blimp.owner.email], fail_silently=False)
    return
