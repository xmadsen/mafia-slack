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
            self._transitionFromMarshalling(action, data)
        elif self.gameState.state == GameStates.NIGHT:
            self._transitionFromNight(action, data)
        elif self.gameState.state == GameStates.DAY:
            self._transitionFromDay(action, data)
        elif self.gameState.state == GameStates.TRIAL:
            self._transitionFromTrial(action)
    
    def _transitionFromMarshalling(self, action, data):
        if action == Actions.START_GAME:
            if len(self.gameState.players) >= 3:
                self._assignPlayerRoles()
                self.gameState.state = GameStates.NIGHT
        elif action == Actions.ADD_PLAYER:
            self.gameState.players.append(data)
        elif action == Actions.REMOVE_PLAYER:
            toRemove = self._findPlayerWithId(data)
            self.gameState.players.remove(toRemove)

    def _transitionFromNight(self, action, data):
        if action == Actions.MURDER:
            toMurder = self._findPlayerWithId(data)
            toMurder.state = PlayerStates.DEAD
            if self._isGameOver():
                self.gameState.state = GameStates.GAME_OVER
            else:
                self.gameState.state = GameStates.DAY

    def _transitionFromDay(self, action, data):
        if action == Actions.ACCUSE:
            accusedPlayer = self._findPlayerWithId(data)
            accusedPlayer.state = PlayerStates.ON_TRIAL
            self.gameState.state = GameStates.TRIAL

    def _transitionFromTrial(self, action):
        player = self._findPlayersWithState(PlayerStates.ON_TRIAL)[0]
        if action == Actions.NOT_GUILTY:
            player.state = PlayerStates.ALIVE
            self.gameState.state = GameStates.DAY
        elif action == Actions.GUILTY:
            player.state = PlayerStates.DEAD
            if self._isGameOver():
                self.gameState.state = GameStates.GAME_OVER
            else:
                self.gameState.state = GameStates.NIGHT

    def _assignPlayerRoles(self):
        numMafia = self._getMafiaCount()
        shuffledRoster = random.sample(self.gameState.players,len(self.gameState.players))
        for p in shuffledRoster[:numMafia]:
            p.role = Roles.MAFIA
        for p in shuffledRoster[numMafia:]:
            p.role = Roles.VILLAGER
    
    def _getMafiaCount(self):
        return len(self.gameState.players) // 3

    def _findPlayerWithId(self, id):
        return [p for p in self.gameState.players if p.id == id][0]
    
    def _findPlayersWithState(self, state):
        return [p for p in self.gameState.players if p.state == state]

    def _isGameOver(self):
        mafiaCount = len([p for p in self.gameState.players if p.role == Roles.MAFIA and p.state == PlayerStates.ALIVE])
        villagerCount = len([p for p in self.gameState.players if p.role == Roles.VILLAGER and p.state == PlayerStates.ALIVE])
        
        return mafiaCount == 0 or villagerCount == mafiaCount