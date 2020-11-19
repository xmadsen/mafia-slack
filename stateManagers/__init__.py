from stateManagers.gameStateManager import Actions
from stateManagers.dayStateManager import DayStateManager
from stateManagers.marshallingStateManager import MarshallingStateManager
from stateManagers.nightStateManager import NightStateManager
from stateManagers.trialStateManager import TrialStateManager
from models.gameState import States as GameStates


def getInstance(gameState):
    if gameState.state == GameStates.MARSHALLING:
        return MarshallingStateManager(gameState)
    elif gameState.state == GameStates.NIGHT:
        return NightStateManager(gameState)
    elif gameState.state == GameStates.DAY:
        return DayStateManager(gameState)
    elif gameState.state == GameStates.TRIAL:
        return TrialStateManager(gameState)
