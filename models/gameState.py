from models.player import Roles, States as PlayerStates

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
        self.meta = None
        #store the last player who was accused of being in the mafia by the villagers
        self.last_accused = None

    def findPlayerWithId(self, id):
        playerList = [p for p in self.players if p.id == id]
        if len(playerList) > 0:
            return playerList[0]
        return None
        
    def determineWinner(self):
        if self.state == States.GAME_OVER:
            living_mafia = len([p for p in self.players if p.role == Roles.MAFIA and p.state == PlayerStates.ALIVE])
            if living_mafia == 0:
                return Roles.MAFIA
            else:
                return Roles.VILLAGER