
class States:
    MARSHALLING = 'MARSHALLING'
    NIGHT = 'NIGHT'
    DAY = 'DAY'
    TRIAL = 'TRIAL'
    GAME_OVER = 'GAME_OVER'

class Game(object):
    def __init__(self, id = None):
        self.id = id
        self.state = States.MARSHALLING
        self.players = []