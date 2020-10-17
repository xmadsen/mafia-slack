from stateManagers.gameStateManager import GameStateManager, Actions
from models.player import Roles, States as PlayerStates
from models.gameState import States as GameStates

class NightStateManager(GameStateManager):
    def _transitionFromState(self, action, data, executor):
        if action == Actions.MURDER:
            toMurder = self.gameState.findPlayerWithId(data)
            if toMurder == None or toMurder.role == Roles.MAFIA:
                return False
            murderer = self.gameState.findPlayerWithId(executor)
            if murderer.role != Roles.MAFIA:
                return False
            murderer.vote = toMurder.id
            mafiaMembers = self.gameState.findPlayersWithRole(Roles.MAFIA)
            livingMafia = [m for m in mafiaMembers if m.state == PlayerStates.ALIVE]
            if len([m for m in mafiaMembers if m.vote == toMurder.id]) == len(livingMafia):
                toMurder.state = PlayerStates.DEAD
                if self._isGameOver():
                    self.gameState.state = GameStates.GAME_OVER
                else:
                    self.gameState.state = GameStates.DAY
            return True
        return False