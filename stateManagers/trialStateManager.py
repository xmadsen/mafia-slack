from stateManagers.gameStateManager import GameStateManager, Actions
from models.player import States as PlayerStates
from models.gameState import States as GameStates

class TrialStateManager(GameStateManager):
    def _transitionFromState(self, action, data, executor):
        accused = self.gameState.findPlayerOnTrial()
        juror = self.gameState.findPlayerWithId(executor)
        ret = False
        if accused and juror and juror.can_vote():
            if action == Actions.NOT_GUILTY or action == Actions.GUILTY:
                juror.vote = action
                ret = True
            self._checkTrialState(accused)
        return ret

    def _checkTrialState(self, accused):
        jury_count = len([p for p in self.gameState.players if p.can_vote()])
        votes_to_acquit = self.gameState.voteCount(Actions.NOT_GUILTY)
        votes_to_convict = self.gameState.voteCount(Actions.GUILTY)
        print(f'{jury_count} members on the jury')
        print(f'{votes_to_acquit} votes to acquit')
        print(f'{votes_to_convict} votes to convict')
        if votes_to_acquit + votes_to_convict == jury_count:
            if votes_to_acquit >= votes_to_convict:
                accused.state=PlayerStates.ALIVE
                self.gameState.state = GameStates.DAY
            else:
                accused.state = PlayerStates.DEAD
                if self._isGameOver():
                    self.gameState.state = GameStates.GAME_OVER
                else:
                    self.gameState.state = GameStates.NIGHT