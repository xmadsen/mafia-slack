import re


def parse_payload(raw_args):
    return {x[0]: x[1] for x in [x.split("=") for x in raw_args.split("&")]}


def extract_user_id(input):
    '''extract the user id from an @tag'''
    m = re.search(r'%3C%40(\w+)%7C', input)
    if m:
        return m[1]
