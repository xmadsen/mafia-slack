import pytest
import random
from models.gameState import Game, States as GameStates
from models.player import Player, Roles
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateTrial_FoundNotGuiltyAction_StateIsDay():
    state = Game()
    state.state = GameStates.TRIAL
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.NOT_GUILTY)

    assert state.state == GameStates.DAY

def test_GameStateTrial_FoundGuiltyAction_StateIsNight():
    state = Game()
    state.state = GameStates.TRIAL
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.GUILTY)

    assert state.state == GameStates.NIGHT