import os

DIR = os.path.dirname(__file__)


def get(resource):
    with open(os.path.join(DIR, resource)) as f:
        return f.read()
