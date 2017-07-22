#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import functools
import logging

from flask import abort, make_response, request
from six.moves.http_client import BAD_REQUEST, NO_CONTENT
from twilio.jwt.client import ClientCapabilityToken
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from twilio.twiml import TwiML


APPLICATION_XML = 'application/xml'

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

    app = None

    account_sid = None
    auth_token = None

    application_sid = None

    api_key_sid = None
    api_key_secret = None

    client = None
    request_validator = None

    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):

        self.app = app

        self.account_sid = account_sid = app.config.get('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token = app.config.get('TWILIO_AUTH_TOKEN')
        if not (account_sid and auth_token):
            logger.warning('TWILIO_ACCOUNT_SID and/or TWILIO_AUTH_TOKEN not set')
            return

        self.application_sid = app.config.get('TWILIO_APPLICATION_SID')

        self.api_key_sid = app.config.get('TWILIO_API_KEY_SID')
        self.api_key_secret = app.config.get('TWILIO_API_KEY_SECRET')

        self.client = Client(account_sid, auth_token, **kwargs)
        self.request_validator = RequestValidator(auth_token)

    def request(self, model_class):
        """
        https://www.twilio.com/docs/api/security
        https://www.twilio.com/docs/api/twiml
        https://www.twilio.com/docs/api/twiml/twilio_request
        https://www.twilio.com/docs/api/twiml/your_response
        """

        def decorator(view_func):

            @functools.wraps(view_func)
            def decorated_view(*args, **kwargs):

                signature = request.headers.get('X-Twilio-Signature')
                if not self.request_validator.validate(request.url, request.values, signature):
                    logger.warning('Invalid signature')
                    abort(BAD_REQUEST)

                response = view_func(model_class(request.form, strict=False), *args, **kwargs)
                if response is None:
                    response = make_response()
                    response.content_type = APPLICATION_XML
                    return response, NO_CONTENT

                if not isinstance(response, TwiML):
                    raise ValueError('View function did not return a TwiML response')

                return self.app.response_class(response.to_xml(), mimetype=APPLICATION_XML)

            return decorated_view

        return decorator

    def capability_token(self):
        return ClientCapabilityToken(self.account_sid, self.auth_token)

    def __getattr__(self, name):
        return getattr(self.client, name)


# EOF
