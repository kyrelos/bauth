from __future__ import absolute_import
from celery import shared_task, task
from django.conf import settings
from core.models import *
import requests
from twilio.rest import TwilioRestClient
from core import utils


client = TwilioRestClient(account="ACdfd9a716b667929ff1454542f918f871", token="b4d2983a0c8b34e2c2d3b5e7d8f66bf4")


# The @shared_task decorator lets you create tasks without having any concrete app instance:
@shared_task
def add(x, y):
    """
    You can import this example task as: from core.tasks import add
    """
    return x + y


@task
def backup_db():
    utils.backup_db()



@shared_task
def restore_db():
    utils.restore_db()

@shared_task
def send_message(token):
    message = client.messages.create(
        body=token,
        to="+254703299139",
        from_="+17315060403",
    )


