import pytest
from models.gameState import State, Constants
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateDay_AccuseAction_StateIsTrial():
    state = State()
    state.state = Constants.DAY
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.ACCUSE)

    assert state.state == Constants.TRIAL