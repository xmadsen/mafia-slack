
class Roles:
    NONE = 'NONE' # only valid if game is still marshalling
    VILLAGER = 'VILLAGER'
    MAFIA = 'MAFIA'

class States:
    ALIVE = 'ALIVE'
    DEAD = 'DEAD'
    ON_TRIAL = 'ON_TRIAL'

class Player(object):
    def __init__(self):
        self.role = Roles.NONE
        self.state = States.ALIVE
        self.id = None