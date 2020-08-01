
class Constants:
    MARSHALLING = 'MARSHALLING'
    NIGHT = 'NIGHT'
    DAY = 'DAY'
    TRIAL = 'TRIAL'

class State(object):
    def __init__(self):
        self.state = Constants.MARSHALLING
        self.players = []