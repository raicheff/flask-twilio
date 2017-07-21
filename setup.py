#
# Flask-Twilio
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from setuptools import find_packages, setup


setup(
    name='Flask-Twilio',
    version='0.1.0',
    description='Flask-Twilio',
    author='Boris Raicheff',
    author_email='b@raicheff.com',
    url='https://github.com/raicheff/flask-twilio',
    install_requires=('flask', 'six', 'schematics', 'twilio'),
    packages=find_packages(),
)


# EOF
