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
from requests import Request, Session
from six.moves.http_client import BAD_REQUEST, NO_CONTENT
from twilio.http import HttpClient, get_cert_file
from twilio.http.response import Response
from twilio.jwt.client import ClientCapabilityToken
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from twilio.twiml import TwiML


logger = logging.getLogger('Flask-Twilio')


class TwilioHttpClient(HttpClient):
    """
    General purpose HTTP Client for interacting with the Twilio API
    """

    def __init__(self) -> None:
        session = Session()
        session.verify = get_cert_file()
        self.session = session

    def request(self, method, url, params=None, data=None, headers=None, auth=None, timeout=None, allow_redirects=False):
        """
        Make an HTTP Request with parameters provided.

        :param str method: The HTTP method to use
        :param str url: The URL to request
        :param dict params: Query parameters to append to the URL
        :param dict data: Parameters to go in the body of the HTTP request
        :param dict headers: HTTP Headers to send with the request
        :param tuple auth: Basic Auth arguments
        :param float timeout: Socket/Read timeout for the request
        :param boolean allow_redirects: Whether or not to allow redirects
        See the requests documentation for explanation of all these parameters

        :return: An http response
        :rtype: A :class:`Response <twilio.rest.http.response.Response>` object
        """

        headers.pop('User-Agent', None)

        request = Request(method.upper(), url, params=params, data=data, headers=headers, auth=auth)

        prepped_request = self.session.prepare_request(request)
        response = self.session.send(
            prepped_request,
            allow_redirects=allow_redirects,
            timeout=timeout,
        )

        return Response(int(response.status_code), response.content.decode('utf-8'))


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

    client = None
    request_validator = None

    blueprint = None

    def __init__(self, app=None, blueprint=None):
        self._routes = {}
        if app is not None:
            self.init_app(app, blueprint)

    def init_app(self, app, blueprint=None, url_prefix=None):

        self.app = app

        self.account_sid = account_sid = app.config.get('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token = app.config.get('TWILIO_AUTH_TOKEN')
        if not (account_sid and auth_token):
            logger.warning('TWILIO_ACCOUNT_SID and/or TWILIO_AUTH_TOKEN not set')
            return
        self.application_sid = app.config.get('TWILIO_APPLICATION_SID')
        self.client = Client(account_sid, auth_token, http_client=TwilioHttpClient())
        self.request_validator = RequestValidator(auth_token)

        if blueprint is None:
            blueprint = Blueprint('twilio', __name__, url_prefix=url_prefix)
        self.blueprint = blueprint

        for rule, options in self._routes.items():
            view_func = self.request(options.pop('view_func'))
            rule = '/twilio' + rule
            endpoint = 'twilio-' + options.pop('endpoint')
            methods = options.pop('methods', ['POST'])
            blueprint.add_url_rule(rule, endpoint, view_func, methods=methods, **options)

    def request(self, func):
        """
        https://www.twilio.com/docs/api/security
        https://www.twilio.com/docs/api/twiml
        https://www.twilio.com/docs/api/twiml/twilio_request
        https://www.twilio.com/docs/api/twiml/your_response
        """

        response_class = self.app.response_class

        @functools.wraps(func)
        def decorated_view(*args, **kwargs):

            signature = _request.headers.get('x-twilio-signature')
            if not self.request_validator.validate(_request.url, _request.values, signature):
                logger.warning('Invalid signature')
                abort(BAD_REQUEST)

            _response = func(_underscore(_request.form), *args, **kwargs)

            if _response is None:
                response = make_response('')
                response.content_type = 'application/xml'
                return response, NO_CONTENT

            if not isinstance(_response, TwiML):
                raise ValueError('View function did not return a TwiML response')

            return response_class(_response.to_xml(), mimetype='application/xml')

        return decorated_view

    def route(self, rule, **options):
        def decorator(f):
            self._routes[rule] = {'view_func': f, **options}
            return f
        return decorator

    def capability_token(self):
        return ClientCapabilityToken(self.account_sid, self.auth_token)

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
