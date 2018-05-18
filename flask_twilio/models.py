#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from enum import Enum

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
        super().__init__({_(k): v for k, v in raw_data.items() if v}, *args, **kwargs)

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
    """Describes whether or not the person called correctly entered the validation code. Possible values are `success` or `failed`."""

    outgoing_caller_id_sid = StringType()
    """If the verification process was successful, the SID value of the newly-created OutgoingCallerId resource for the verified number."""


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


class FaxRequest(TwiMLRequest):
    """
    https://www.twilio.com/docs/api/fax/receive
    """

    fax_sid = StringType(required=True)
    """The 34-character unique identifier for the fax"""

    from_ = StringType(required=True, serialized_name='from')
    """The caller ID or SIP From display name"""

    to = StringType(required=True)
    """The phone number or SIP URI of the destination"""


class FaxDirection(Enum):
    """"""

    OUTBOUND = 'outbound'
    """Sent"""

    INBOUND = 'inbound'
    """Received"""


class FaxStatus(Enum):
    """
    https://www.twilio.com/docs/api/fax/rest/faxes#fax-status-values
    """

    QUEUED = 'queued'
    """The fax is queued, waiting for processing"""

    PROCESSING = 'processing'
    """The fax is being downloaded, uploaded, or transcoded into a different format"""

    SENDING = 'sending'
    """The fax is in the process of being sent"""

    DELIVERED = 'delivered'
    """The fax has been successfuly delivered"""

    RECEIVING = 'receiving'
    """The fax is in the process of being received"""

    RECEIVED = 'received'
    """The fax has been successfully received"""

    NO_ANSWER = 'no-answer'
    """The outbound fax failed because the other end did not pick up"""

    BUSY = 'busy'
    """The outbound fax failed because the other side sent back a busy signal"""

    FAILED = 'failed'
    """The fax failed to send or receive"""

    CANCELED = 'canceled'
    """The fax was canceled, either by using the REST API, or rejected by TwiML"""


class FaxStatusRequest(FaxRequest):
    """
    https://www.twilio.com/docs/api/fax/receive
    """

    remote_station_id = StringType()
    """The transmitting subscriber identification (TSID) reported by the sending fax machine"""

    fax_status = StringType(choices=[e.value for e in FaxStatus])
    """The status of the fax transmission"""

    num_pages = IntType()
    """The number of pages received (if successful)"""

    media_url = URLType()
    """A media URL on Twilio's servers that can be used to fetch the received media"""

    original_media_url = URLType()
    """The original URL passed when sending the fax"""

    error_code = IntType()
    """A Twilio error code that gives more information about a failure (if any)"""

    error_message = StringType()
    """A detailed message describing a failure (if any)"""


# EOF
