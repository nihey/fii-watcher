from traceback import format_exception
from datetime import datetime
import math

import requests

from fii.database import get_store
from fii.models import Watcher
from fii.settings import Config


def log(string):
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '-', string


def send_email(emails, subject, body):
    if emails == '':
        return

    requests.get(Config.MAILER_URL, params={
        'emails': emails,
        'subject': subject,
        'body': body,
    })


def distribute(list_, parts):
    # Get the maximum size a sublist can have
    size = math.ceil(len(list_) / float(parts))
    # Determine the cut points on which the list will be divided
    slices = [(int(i * size), int((i + 1) * size)) for i in xrange(parts)]
    # Slice the list
    return [list_[s[0]:s[1]] for s in slices]


def notify_generic_change(fii):
    emails = ','.join([w.email for w in fii.watchers
                       if w.status != 'inactive'])

    # Variables used to compose e-mail
    variables = fii.dict()
    subject = Config.FII_GENERIC_CHANGE_SUBJECT.format(**variables)
    body = Config.FII_GENERIC_CHANGE_BODY.format(**variables)

    log('sending e-mails for {} to "{}"'.format(fii.code, emails))
    send_email(emails, subject, body)


def notify_change(fii_log):
    emails = ','.join([w.email for w in fii_log.fii.watchers
                       if w.status != 'inactive'])

    # Variables used to compose e-mail
    variables = fii_log.dict()
    variables.update(fii_log.fii.dict())
    subject = Config.FII_CHANGE_SUBJECT.format(**variables)
    body = Config.FII_CHANGE_BODY.format(**variables)

    log('sending e-mails for {} to "{}"'.format(fii_log.fii_code, emails))
    send_email(emails, subject, body)


def notify_fail(command):
    store = get_store()
    admins = store.query(Watcher).filter(Watcher.status == 'admin')

    emails = ','.join([w.email for w in admins])
    subject = '[FII] failed to run {}'.format(command)
    body = 'Error logs may have more details, check it back later'

    log('sending fail log e-mails for "{}"'.format(emails))
    send_email(emails, subject, body)


def excepthook(type_, value, traceback):
    store = get_store()

    admins = store.query(Watcher).filter(Watcher.status == 'admin')
    if admins.count() == 0:
        return

    emails = ','.join([a.email for a in admins])
    subject = '[FII] Error: {}'.format(value.message)
    body = ''.join(format_exception(type_, value, traceback))
    log(body)

    log('sending error e-mail to "{}"'.format(emails))
    send_email(emails, subject, body)
