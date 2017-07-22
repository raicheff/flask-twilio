#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import re


RE_FIRST_CAP = re.compile('(.)([A-Z][a-z]+)')
RE_ALL_CAP = re.compile('([a-z0-9])([A-Z])')


def _(string):
    """
    https://gist.github.com/jaytaylor/3660565
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    https://stackoverflow.com/questions/21169792/python-function-to-convert-camel-case-to-snake-case
    """
    s1 = RE_FIRST_CAP.sub(r'\1_\2', string)
    return RE_ALL_CAP.sub(r'\1_\2', s1).lower()


# EOF
