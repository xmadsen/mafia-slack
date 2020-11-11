from stateManagers.gameStateManager import GameStateManager, Actions
from models.player import States as PlayerStates
from models.gameState import States as GameStates


class DayStateManager(GameStateManager):
    def _transitionFromState(self, action, data, executor):
        if action == Actions.ACCUSE:
            accusedPlayer = self.gameState.findPlayerWithId(data)
            accuser = self.gameState.findPlayerWithId(executor)
            if accusedPlayer and accuser and
                    accusedPlayer.state == PlayerStates.ALIVE and
                    accuser.state == PlayerStates.ALIVE:
                accuser.vote = accusedPlayer.id
                if self.gameState.voteCount(accusedPlayer.id) >= 2:
                    accusedPlayer.state = PlayerStates.ON_TRIAL
                    self.gameState.state = GameStates.TRIAL
                    self.gameState.last_accused = accusedPlayer.id
                return True
        return False
