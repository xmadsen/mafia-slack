from setuptools import setup

setup(
    name='mafia-slack',
    version='1.0',
    description='A game of Mafia for Slack.',
    packages=['mafia-slack'],
    install_requires=['boto3', 'slackclient']
)
