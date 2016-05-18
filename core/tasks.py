from __future__ import absolute_import
from celery import shared_task, task
from django.conf import settings
from httplib2 import ServerNotFoundError
from core.models import *
import requests
from twilio.rest import TwilioRestClient
from core import utils
from structlog import get_logger
from django.core.mail import send_mail

client = TwilioRestClient(account="ACdfd9a716b667929ff1454542f918f871", token="b4d2983a0c8b34e2c2d3b5e7d8f66bf4")
logger = get_logger('celery')

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
    """
    Send SMS message
    :param token:
    :return:
    """
    try:
        client.messages.create(
            body=token,
            to="+254703299139",
            from_=settings.TWILIO_PHONE_NUMBER,
        )
        logger.info('message_success', message={"token": token})
    except ServerNotFoundError as e:
        logger.exception('message_failure', exception=e.message)


@shared_task
def send_email(token, url):
    """
    Send Email

    :param token:
    :param url:
    :return:
    """
    body = 'To verify your email and complete your Registration click {0}'.format(url)
    try:
        send_mail('Email Verification',
                  body,
                  'noreply-bauth@bauth.com',
                  ['kalosobat@gmail.com'],
                  )
        logger.info('email_success', message={"token": token})
    except ServerNotFoundError as e:
        logger.exception('email_failure', exception=e.message)
