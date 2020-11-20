from abc import ABC, abstractmethod
from models.player import Roles, States as PlayerStates


class Actions:
    START_GAME = 'START_GAME'
    ACCUSE = 'ACCUSE'
    MURDER = 'MURDER'
    GUILTY = 'GUILTY'
    NOT_GUILTY = 'NOT_GUILTY'

    ADD_PLAYER = 'ADD_PLAYER'
    REMOVE_PLAYER = 'REMOVE_PLAYER'


class GameStateManager(ABC):

    def __init__(self, gameState):
        self.gameState = gameState

    def transition(self, action, data=None, executor=None):
        '''
            data - typically the player id of the player who the action is targeting
            executor - the player id of the player who is taking the action.
        '''
        print(f'state {self.gameState.state} - {action} - {data} - {executor}')
        oldState = self.gameState.state
        ret = self._transitionFromState(action, data, executor)

        if self.gameState.state != oldState:
            # reset player votes
            for p in self.gameState.players:
                p.vote = None
        return ret

    @abstractmethod
    def _transitionFromState(self, action, data, executor):
        pass

    def _isGameOver(self):
        mafiaCount = len([p for p in self.gameState.findPlayersWithRole(
            Roles.MAFIA) if p.state == PlayerStates.ALIVE])
        villagerCount = len([p for p in self.gameState.findPlayersWithRole(
            Roles.VILLAGER) if p.state == PlayerStates.ALIVE])

        return mafiaCount == 0 or villagerCount == mafiaCount

    def printGameState(self):
        playerList = sorted(self.gameState.players,
                            key=lambda player: player.role)
        print('ROSTER:')
        print('id|role|state')
        for p in playerList:
            print(p)
        print(f'GAME STATE: {self.gameState.state}')
