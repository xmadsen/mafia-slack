import random
from models.gameState import States as GameStates
from models.player import Roles, States as PlayerStates

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
        if self.gameState.state == GameStates.MARSHALLING:
            self.transitionFromMarshalling(action, data)
        elif self.gameState.state == GameStates.NIGHT:
            self.transitionFromNight(action, data)
        elif self.gameState.state == GameStates.DAY:
            self.transitionFromDay(action, data)
        elif self.gameState.state == GameStates.TRIAL:
            self.transitionFromTrial(action)
    
    def transitionFromMarshalling(self, action, data):
        if action == Actions.START_GAME:
            if len(self.gameState.players) >= 3:
                self.assignPlayerRoles()
                self.gameState.state = GameStates.NIGHT
        elif action == Actions.ADD_PLAYER:
            self.gameState.players.append(data)
        elif action == Actions.REMOVE_PLAYER:
            toRemove = self.findPlayerWithId(data)
            self.gameState.players.remove(toRemove)

    def transitionFromNight(self, action, data):
        if action == Actions.MURDER:
            toMurder = self.findPlayerWithId(data)
            toMurder.state = PlayerStates.DEAD
            if self.isGameOver():
                self.gameState.state = GameStates.GAME_OVER
            else:
                self.gameState.state = GameStates.DAY

    def transitionFromDay(self, action, data):
        if action == Actions.ACCUSE:
            accusedPlayer = self.findPlayerWithId(data)
            accusedPlayer.state = PlayerStates.ON_TRIAL
            self.gameState.state = GameStates.TRIAL

    def transitionFromTrial(self, action):
        player = self.findPlayersWithState(PlayerStates.ON_TRIAL)[0]
        if action == Actions.NOT_GUILTY:
            player.state = PlayerStates.ALIVE
            self.gameState.state = GameStates.DAY
        elif action == Actions.GUILTY:
            player.state = PlayerStates.DEAD
            if self.isGameOver():
                self.gameState.state = GameStates.GAME_OVER
            else:
                self.gameState.state = GameStates.NIGHT

    def assignPlayerRoles(self):
        numMafia = self.getMafiaCount()
        shuffledRoster = random.sample(self.gameState.players,len(self.gameState.players))
        for p in shuffledRoster[:numMafia]:
            p.role = Roles.MAFIA
        for p in shuffledRoster[numMafia:]:
            p.role = Roles.VILLAGER
    
    def getMafiaCount(self):
        return len(self.gameState.players) // 3

    def findPlayerWithId(self, id):
        return [p for p in self.gameState.players if p.id == id][0]
    
    def findPlayersWithState(self, state):
        return [p for p in self.gameState.players if p.state == state]

    def isGameOver(self):
        mafiaCount = len([p for p in self.gameState.players if p.role == Roles.MAFIA and p.state == PlayerStates.ALIVE])
        villagerCount = len([p for p in self.gameState.players if p.role == Roles.VILLAGER and p.state == PlayerStates.ALIVE])
        
        return mafiaCount == 0 or villagerCount == mafiaCount