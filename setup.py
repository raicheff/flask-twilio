#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from setuptools import setup


setup(
    name='Flask-Twilio',
    version='0.1.0',
    description='Flask-Twilio',
    author='Boris Raicheff',
    author_email='b@raicheff.com',
    url='https://github.com/raicheff/flask-twilio',
    install_requires=('flask', 'six', 'twilio'),
    py_modules=('flask_twilio',),
)


# EOF
