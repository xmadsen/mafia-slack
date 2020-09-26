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
    dead_player = createVillager('test')
    live_player = createVillager('v1')
    dead_player.state=PlayerStates.DEAD
    state.players = [dead_player,live_player]

    result = systemUnderTest.transition(Actions.ACCUSE, dead_player.id, live_player.id)

    assert state.state == GameStates.DAY
    assert result == False

def test_DeadManCanNotAccuse():
    state = Game()
    state.state = GameStates.DAY
    systemUnderTest = GameStateManager(state)
    dead_player = createVillager('test')
    live_player = createVillager('v1')
    dead_player.state=PlayerStates.DEAD
    state.players = [dead_player, live_player]

    result = systemUnderTest.transition(Actions.ACCUSE, live_player.id, dead_player.id)

    assert state.state == GameStates.DAY
    assert result == False