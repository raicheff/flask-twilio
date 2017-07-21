#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from schematics import Model
from schematics.types import IntType, StringType, URLType


class TwiMLRequest(Model):
    """
    https://www.twilio.com/docs/api/twiml/twilio_request
    """

    account_sid = StringType(required=True)
    application_sid = StringType()

    api_version = StringType()


class VoiceRequest(TwiMLRequest):
    """
    https://www.twilio.com/docs/api/twiml/twilio_request#synchronous
    https://www.twilio.com/docs/api/twiml/twilio_request#synchronous-request-parameters
    """

    call_sid = StringType(required=True)

    call_status = StringType()
    direction = StringType()
    from_ = StringType(serialized_name='from')
    forwarded_from = StringType()
    to = StringType()


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
    """The digits the caller pressed, excluding the finishOnKey digit if used."""


class SIPVoiceRequest(VoiceRequest):
    """"""

    sip_domain = StringType(required=True)
    """The Twilio SIP Domain to which the INVITE was sent."""

    sip_username = StringType()
    """The username given when authenticating the request, if Credential List is the authentication method."""

    sip_call_id = StringType(required=True)
    """The Call-Id of the incoming INVITE."""

    sip_source_ip = StringType(required=True)


# EOF
