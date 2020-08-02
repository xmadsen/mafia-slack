import random
from models.gameState import Constants as PossibleStates
from models.player import Roles
class Actions:
    START_GAME = 'START_GAME'
    ACCUSE = 'ACCUSE'
    MURDER = 'MURDER'
    GUILTY = 'GUILTY'
    NOT_GUILTY = 'NOT_GUILTY'

    ADD_PLAYER = 'ADD_PLAYER'
    REMOVE_PLAYER = 'REMOVE_PLAYER'

class GameStateManager(object):
    
    def __init__(self, gameState):
        self.gameState = gameState

    def transition(self, action, data=None):
        if self.gameState.state == PossibleStates.MARSHALLING:
            self.transitionFromMarshalling(action, data)
        elif self.gameState.state == PossibleStates.NIGHT:
            self.transitionFromNight(action)
        elif self.gameState.state == PossibleStates.DAY:
            self.transitionFromDay(action)
        elif self.gameState.state == PossibleStates.TRIAL:
            self.transitionFromTrial(action)
    
    def transitionFromMarshalling(self, action, data):
        if action == Actions.START_GAME:
            if len(self.gameState.players) >= 3:
                self.assignPlayerRoles()
                self.gameState.state = PossibleStates.NIGHT
        elif action == Actions.ADD_PLAYER:
            self.gameState.players.append(data)
        elif action == Actions.REMOVE_PLAYER:
            toRemove = [p for p in self.gameState.players if p.id == data][0]
            self.gameState.players.remove(toRemove)

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
        for p in shuffledRoster[:numMafia]:
            p.role = Roles.MAFIA
        for p in shuffledRoster[numMafia:]:
            p.role = Roles.VILLAGER
    
    def getMafiaCount(self):
        return len(self.gameState.players) // 3
