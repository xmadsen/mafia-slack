from setuptools import setup

setup(
    name='mafia-slack',
    version='1.0',
    description='A game of Mafia for Slack.',
    install_requires=['boto3', 'slackclient']
    packages=find_packages(where='.'),
    package_dir={
        '': '.',
    },
)
