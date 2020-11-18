import os


def getEnvVar(name):
    if name in os.environ:
        return os.environ[name]
