from datetime import datetime
import math

import requests

from fii.settings import Config


def log(string):
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '-', string


def distribute(list_, parts):
    # Get the maximum size a sublist can have
    size = math.ceil(len(list_) / float(parts))
    # Determine the cut points on which the list will be divided
    slices = [(int(i * size), int((i + 1) * size)) for i in xrange(parts)]
    # Slice the list
    return [list_[s[0]:s[1]] for s in slices]


def notify_change(fii_log):
    emails = ','.join([w.email for w in fii_log.fii.watchers
                       if w.status != 'inactive'])

    # Variables used to compose e-mail
    variables = fii_log.dict()
    variables.update(fii_log.fii.dict())
    subject = Config.FII_CHANGE_SUBJECT.format(**variables)
    body = Config.FII_CHANGE_BODY.format(**variables)

    # Do not attempt to send e-mails if no email is provided
    if emails == '':
        return log('no e-mails for {}, skipping'.format(fii_log.fii_code))

    log('sending e-mails for {} to "{}"'.format(fii_log.fii_code, emails))
    requests.get(Config.MAILER_URL, params={
        'emails': emails,
        'subject': subject,
        'body': body,
    })
