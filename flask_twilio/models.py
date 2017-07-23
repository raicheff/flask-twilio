#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from schematics import Model
from schematics.types import IntType, StringType, URLType

from .helpers import _


class TwiMLRequest(Model):
    """
    https://www.twilio.com/docs/api/twiml/twilio_request
    """

    account_sid = StringType(required=True)
    """The Twilio account ID. It is 34 characters long, and always starts with the letters AC."""

    api_version = StringType(required=True)
    """The version of the Twilio API used to handle this call."""

    def __init__(self, raw_data, *args, **kwargs):
        super().__init__({_(k): v for k, v in raw_data.items()}, *args, **kwargs)

    def _repr_info(self):
        return {k: v for k, v in self.items()}


class VoiceRequest(TwiMLRequest):
    """
    https://www.twilio.com/docs/api/twiml/twilio_request#synchronous
    https://www.twilio.com/docs/api/twiml/twilio_request#synchronous-request-parameters
    """

    call_sid = StringType(required=True)

    from_ = StringType(required=True, serialized_name='from')

    forwarded_from = StringType()

    to = StringType(required=True)

    call_status = StringType(required=True)

    direction = StringType(required=True)

    caller_name = StringType()


class VoiceStatusRequest(VoiceRequest):
    """
    https://www.twilio.com/docs/api/twiml/twilio_request#request-parameters
    """

    call_duration = StringType()

    recording_url = StringType()
    recording_sid = StringType()
    recording_duration = StringType()


class VerificationStatusRequest(VoiceRequest):
    """
    https://www.twilio.com/docs/api/rest/outgoing-caller-ids#status-callback-parameter
    """

    verification_status = StringType()
    outgoing_caller_id_sid = StringType()


class RecordingStatusRequest(TwiMLRequest):
    """
    https://www.twilio.com/docs/api/twiml/dial#attributes-recording-status-callback
    """

    call_sid = StringType(required=True)

    recording_sid = StringType(required=True)

    recording_channels = IntType()
    recording_duration = IntType()
    recording_source = StringType()
    recording_status = StringType()
    recording_url = URLType()


class GatherRequest(VoiceRequest):
    """
    https://www.twilio.com/docs/api/twiml/gather#attributes-action-parameters
    """

    digits = StringType()
    """The digits the caller pressed, excluding the `finishOnKey` digit if used."""


class SIPVoiceRequest(VoiceRequest):
    """"""

    sip_call_id = StringType(required=True)
    """The Call Id of the incoming INVITE."""

    sip_domain = StringType(required=True)
    """The Twilio SIP Domain to which the INVITE was sent."""

    sip_domain_sid = StringType(required=True)
    """(Undocumented)"""

    sip_username = StringType()
    """The username given when authenticating the request, if Credential List is the authentication method."""

    sip_source_ip = StringType(required=True)
    """The IP Address the incoming INVITE came from."""


# EOF
