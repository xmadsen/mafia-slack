import pytest
from models.gameState import Game, States
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateDay_AccuseAction_StateIsTrial():
    state = Game()
    state.state = States.DAY
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.ACCUSE)

    assert state.state == States.TRIAL