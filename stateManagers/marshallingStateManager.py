import random
from stateManagers.gameStateManager import GameStateManager, Actions
from models.player import Player, Roles
from models.gameState import States as GameStates


class MarshallingStateManager(GameStateManager):
    def _transitionFromState(self, action, data, executor):
        if action == Actions.START_GAME:
            if len(self.gameState.players) >= 4:
                self._assignPlayerRoles()
                self.gameState.state = GameStates.NIGHT
                return True
        elif action == Actions.ADD_PLAYER:
            p = Player(executor)
            if self.gameState.findPlayerWithId(executor) is None:
                self.gameState.players.append(p)
                return True
        elif action == Actions.REMOVE_PLAYER:
            toRemove = self.gameState.findPlayerWithId(executor)
            self.gameState.players.remove(toRemove)
            return True
        return False

    def _assignPlayerRoles(self):
        numMafia = self._getMafiaCount()
        shuffledRoster = random.sample(
            self.gameState.players, len(self.gameState.players))
        for p in shuffledRoster[:numMafia]:
            p.role = Roles.MAFIA
        for p in shuffledRoster[numMafia:]:
            p.role = Roles.VILLAGER

    def _getMafiaCount(self):
        return len(self.gameState.players) // 3
