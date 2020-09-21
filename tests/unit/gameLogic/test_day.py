import pytest
from models.gameState import Game, States as GameStates
from models.player import Player, States as PlayerStates
from stateManagers.gameStateManager import GameStateManager, Actions
from tests.unit.testHelpers import createVillager

def test_GameStateDay_TwoAccuseActions_StateIsTrialPlayerIsOnTrial():
    state = Game()
    state.state = GameStates.DAY
    systemUnderTest = GameStateManager(state)
    accused = createVillager('test')
    p1 = createVillager('p1')
    p2 = createVillager('p2')
    state.players = [accused, p1, p2]

    systemUnderTest.transition(Actions.ACCUSE, accused.id, p1.id)
    systemUnderTest.transition(Actions.ACCUSE, accused.id, p2.id)

    assert state.state == GameStates.TRIAL
    assert accused.state == PlayerStates.ON_TRIAL

def test_GameStateDay_OneAccuseAction_StateIsStillDay():
    state = Game()
    state.state = GameStates.DAY
    systemUnderTest = GameStateManager(state)
    accused = createVillager('test')
    p1 = createVillager('p1')
    p2 = createVillager('p2')
    state.players = [accused, p1, p2]

    systemUnderTest.transition(Actions.ACCUSE, accused.id, p1.id)

    assert state.state == GameStates.DAY
    assert accused.state == PlayerStates.ALIVE

def test_CanNotAccuseDeadPerson():
    state = Game()
    state.state = GameStates.DAY
    systemUnderTest = GameStateManager(state)
    player = createVillager('test')
    player.state=PlayerStates.DEAD
    state.players = [player]

    systemUnderTest.transition(Actions.ACCUSE, player.id)

    assert state.state == GameStates.DAY
    assert player.state == PlayerStates.DEAD