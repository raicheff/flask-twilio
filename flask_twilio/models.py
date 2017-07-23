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

    api_version = StringType()
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


class ErrorMixin(object):
    """
    https://www.twilio.com/docs/api/security/availability-reliability
    """

    error_code = IntType()

    error_url = URLType()


class VoiceErrorRequest(ErrorMixin, VoiceRequest):
    """"""


class VerificationStatusRequest(VoiceRequest):
    """
    https://www.twilio.com/docs/api/rest/outgoing-caller-ids#status-callback-parameter
    """

    verification_status = StringType()
    outgoing_caller_id_sid = StringType()


class RecordingStatusRequest(TwiMLRequest):
    """
    https://www.twilio.com/docs/api/twiml/dial#attributes-recording-status-callback-parameters
    """

    call_sid = StringType(required=True)
    """A unique identifier for the call associated with the recording. This will always refer to the parent leg of a two leg call."""

    recording_sid = StringType(required=True)
    """The unique identifier for the recording."""

    recording_url = URLType()
    """The URL of the recorded audio."""

    recording_status = StringType()
    """The status of the recording. Possible values are: `completed`."""

    recording_duration = IntType()
    """The length of the recording, in seconds."""

    recording_channels = IntType()
    """The number of channels in the final recording file as an integer. Possible values are `1`, `2`."""

    recording_source = StringType()
    """The type of call that created this recording. For recordings initiated when record is set on `<Dial>`, `DialVerb` is returned."""


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
