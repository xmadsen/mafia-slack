import pytest
from app.models.gameState import Game, States as GameStates
from app.models.player import Player, States as PlayerStates
from app.stateManagers.gameStateManager import GameStateManager, Actions
from tests.unit.testHelpers import createVillager

def test_GameStateDay_AccuseAction_StateIsTrialPlayerIsOnTrial():
    state = Game()
    state.state = GameStates.DAY
    systemUnderTest = GameStateManager(state)
    player = createVillager('test')
    state.players = [player]

    systemUnderTest.transition(Actions.ACCUSE, player.id)

    assert state.state == GameStates.TRIAL
    assert player.state == PlayerStates.ON_TRIAL