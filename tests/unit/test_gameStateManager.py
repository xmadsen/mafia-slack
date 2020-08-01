import pytest
from models.gameState import State, Constants
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateMarshallingWithEnoughPlayers_GameStartAction_StateIsNight():
    state = State()
    state.state = Constants.MARSHALLING
    state.players = [1,2,3]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert state.state == Constants.NIGHT

def test_GameStateMarshallingWithoutEnoughPlayers_GameStartAction_StateIsMarshalling():
    state = State()
    state.state = Constants.MARSHALLING
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert state.state == Constants.MARSHALLING

def test_GameStateNight_MurderAction_StateIsDay():
    state = State()
    state.state = Constants.NIGHT
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.MURDER)

    assert state.state == Constants.DAY

def test_GameStateDay_AccuseAction_StateIsTrial():
    state = State()
    state.state = Constants.DAY
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.ACCUSE)

    assert state.state == Constants.TRIAL

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