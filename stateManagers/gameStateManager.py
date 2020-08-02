import random
from models.gameState import Constants as PossibleStates
class Actions:
    START_GAME = 'START_GAME'
    ACCUSE = 'ACCUSE'
    MURDER = 'MURDER'
    GUILTY = 'GUILTY'
    NOT_GUILTY = 'NOT_GUILTY'

class GameStateManager(object):
    
    def __init__(self, gameState):
        self.gameState = gameState

    def transition(self, action):
        if self.gameState.state == PossibleStates.MARSHALLING:
            self.transitionFromMarshalling(action)
        elif self.gameState.state == PossibleStates.NIGHT:
            self.transitionFromNight(action)
        elif self.gameState.state == PossibleStates.DAY:
            self.transitionFromDay(action)
        elif self.gameState.state == PossibleStates.TRIAL:
            self.transitionFromTrial(action)
    
    def transitionFromMarshalling(self, action):
        if len(self.gameState.players) >= 3:
            self.assignPlayerRoles()
            self.gameState.state = PossibleStates.NIGHT

    def transitionFromNight(self, action):
        self.gameState.state = PossibleStates.DAY

    def transitionFromDay(self, action):
        self.gameState.state = PossibleStates.TRIAL

    def transitionFromTrial(self, action):
        if action == Actions.NOT_GUILTY:
            self.gameState.state = PossibleStates.DAY
        elif action == Actions.GUILTY:
            self.gameState.state = PossibleStates.NIGHT

    def assignPlayerRoles(self):
        numMafia = self.getMafiaCount()
        shuffledRoster = random.sample(self.gameState.players,len(self.gameState.players))
        for idx in range(numMafia):
            shuffledRoster.pop().role = 'MAFIA'
        for p in shuffledRoster:
            p.role = 'VILLAGER'
    
    def getMafiaCount(self):
        return len(self.gameState.players) // 3
