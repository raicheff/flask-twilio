#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import functools
import logging
import re

from flask import Blueprint, abort, make_response, request as _request
from six.moves.http_client import BAD_REQUEST, NO_CONTENT
from twilio.jwt.client import CapabilityToken
from twilio.rest import Client
from twilio.security import RequestValidator


logger = logging.getLogger('Flask-Twilio')


class Twilio(object):
    """
    Flask-Twilio

    Documentation:
    https://flask-twilio.readthedocs.io

    Alternatives:
    https://github.com/lpsinger/flask-twilio

    :param app: Flask app to initialize with. Defaults to `None`
    """

    account_sid = None
    auth_token = None
    application_sid = None

    client = None
    request_validator = None

    blueprint = None

    def __init__(self, app=None, blueprint=None):
        if app is not None:
            self.init_app(app, blueprint)

    def init_app(self, app, blueprint=None, url_prefix=None):

        self.account_sid = account_sid = app.config.get('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token = app.config.get('TWILIO_AUTH_TOKEN')
        if not (account_sid and auth_token):
            logger.warning('TWILIO_ACCOUNT_SID and/or TWILIO_AUTH_TOKEN not set')
            return
        self.application_sid = app.config.get('TWILIO_APPLICATION_SID')
        self.client = Client(account_sid, auth_token)
        self.request_validator = RequestValidator(auth_token)

        if blueprint is None:
            blueprint = Blueprint('twilio', __name__, url_prefix=url_prefix)
        blueprint.add_url_rule('/twilio/voice', 'twilio-voice', self._voice_handler, methods=['POST'])
        self.blueprint = blueprint

    def request(self, func):
        """
        https://www.twilio.com/docs/api/security
        https://www.twilio.com/docs/api/twiml
        https://www.twilio.com/docs/api/twiml/twilio_request
        https://www.twilio.com/docs/api/twiml/your_response
        """

        @functools.wraps(func)
        def decorated_view(*args, **kwargs):

            signature = _request.headers.get('x-twilio-signature')
            if not self.request_validator.validate(_request.url, _request.values, signature):
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

    def voice(self, handler):
        self._voice_handler = self.request(lambda: handler(_underscore(_request.form)))
        return handler

    def capability_token(self):
        return CapabilityToken(self.account_sid, self.auth_token)

    def __getattr__(self, name):
        return getattr(self.client, name)


def _underscore(data):
    """
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    https://stackoverflow.com/questions/21169792/python-function-to-convert-camel-case-to-snake-case
    """

    def _(name):
        s1 = RE_FIRST_CAP.sub(r'\1_\2', name)
        return RE_ALL_CAP.sub(r'\1_\2', s1).lower()

    return {_(k): v for k, v in data.items() if data[k]}


RE_FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
RE_ALL_CAP = re.compile('([a-z0-9])([A-Z])')


# EOF
