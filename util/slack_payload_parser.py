
def parse_payload(raw_args):
    return {x[0] : x[1] for x in [x.split("=") for x in raw_args.split("&") ]}