import pytest
from models.gameState import State, Constants
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateNight_MurderAction_StateIsDay():
    state = State()
    state.state = Constants.NIGHT
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.MURDER)

    assert state.state == Constants.DAY