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

    def findPlayerOnTrial(self):
        players = self._findPlayersWithState(PlayerStates.ON_TRIAL)
        if len(players) > 0:
            return players[0]
        return None
    
    def findPlayersWithRole(self, role):
        return [p for p in self.players if p.role == role]
        
    def determineWinner(self):
        if self.state == States.GAME_OVER:
            living_mafia = len([p for p in self.players if p.role == Roles.MAFIA and p.state == PlayerStates.ALIVE])
            if living_mafia == 0:
                return Roles.VILLAGER
            else:
                return Roles.MAFIA
    def voteCount(self, vote):
        return len([p for p in self.players if p.vote == vote])

    def _findPlayersWithState(self, state):
        return [p for p in self.players if p.state == state]
                