
class Roles:
    NONE = 'NONE' # only valid if game is still marshalling
    VILLAGER = 'VILLAGER'
    MAFIA = 'MAFIA'

class States:
    ALIVE = 'ALIVE'
    DEAD = 'DEAD'
    ON_TRIAL = 'ON_TRIAL'

class Player(object):
    def __init__(self, id = None):
        self.role = Roles.NONE
        self.state = States.ALIVE
        self.id = id
    def __str__(self):
        return f'{self.id}\t{self.role}\t{self.state}'