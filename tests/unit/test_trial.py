import pytest
import random
from models.gameState import State, Constants
from models.player import Player, Roles
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateTrial_FoundNotGuiltyAction_StateIsDay():
    state = State()
    state.state = Constants.TRIAL
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.NOT_GUILTY)

    assert state.state == Constants.DAY

def test_GameStateTrial_FoundGuiltyAction_StateIsNight():
    state = State()
    state.state = Constants.TRIAL
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.GUILTY)

    assert state.state == Constants.NIGHT