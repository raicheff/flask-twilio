#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from twilio.twiml import TwiML
from twilio.twiml.voice_response import VoiceResponse


class TwiMLError(RuntimeError):
    """"""

    response_class = TwiML

    def __init__(self, *args):
        self.response = self.response_class()


class VoiceResponseError(TwiMLError):
    """"""

    response_class = VoiceResponse


class RejectError(VoiceResponseError):
    """
    https://www.twilio.com/docs/api/twiml/reject
    """

    def __init__(self, reason=None):
        super().__init__()
        self.response.reject(reason)


# EOF
