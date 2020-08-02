
class Roles:
    NONE = 'NONE' # only valid if game is still marshalling
    VILLAGER = 'VILLAGER'
    MAFIA = 'MAFIA'

class Player(object):
    def __init__(self):
        self.role = Roles.NONE
        self.state = 'ALIVE'