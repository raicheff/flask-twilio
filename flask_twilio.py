#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import functools
import logging

from flask import abort, current_app, make_response, request
from six.moves.http_client import BAD_REQUEST, NO_CONTENT
from twilio.rest import Client
from twilio.security import RequestValidator


logger = logging.getLogger('Flask-Twilio')


class Twilio(object):
    """
    Flask-Twilio

    Documentation:
    https://flask-twilio.readthedocs.io

    https://github.com/lpsinger/flask-twilio
    http://pythonhosted.org/Flask-Twilio

    :param app: Flask app to initialize with. Defaults to `None`
    """

    account_sid = None
    auth_token = None
    application_sid = None

    client = None

    def __init__(self, app=None, blueprint=None):
        if app is not None:
            self.init_app(app, blueprint)

    def init_app(self, app, blueprint=None):
        self.account_sid = account_sid = app.config.get('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token = app.config.get('TWILIO_AUTH_TOKEN')
        if not (account_sid and auth_token):
            logger.warning('TWILIO_ACCOUNT_SID and/or TWILIO_AUTH_TOKEN not set')
            return
        self.application_sid = app.config.get('TWILIO_APPLICATION_SID')
        self.client = Client(account_sid, auth_token)

    def __getattr__(self, name):
        return getattr(self.client, name)


def twilio_request(func):
    """
    https://www.twilio.com/docs/api/twiml
    https://www.twilio.com/docs/api/security
    https://www.twilio.com/docs/api/twiml/your_response#status-callbacks
    """

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        validator = RequestValidator(current_app.config.get('TWILIO_AUTH_TOKEN'))
        signature = request.headers.get('x-twilio-signature')
        if not validator.validate(request.url, request.values, signature):
            logger.warning('Invalid signature')
            abort(BAD_REQUEST)
        _response = func(*args, **kwargs)
        if _response is None:
            response = make_response('')
            response.content_type = 'application/xml'
            return response, NO_CONTENT
        response = make_response(str(_response))
        response.content_type = 'application/xml'
        return response

    return decorated_view


# EOF
