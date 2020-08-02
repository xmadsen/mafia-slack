import pytest
import random
from models.gameState import State, Constants
from models.player import Player, Roles
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateMarshallingWithEnoughPlayers_GameStartAction_StateIsNight():
    state = State()
    state.state = Constants.MARSHALLING
    state.players = [Player(), Player(), Player()]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert state.state == Constants.NIGHT

def test_GameStateMarshallingWithoutEnoughPlayers_GameStartAction_StateIsMarshalling():
    state = State()
    state.state = Constants.MARSHALLING
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert state.state == Constants.MARSHALLING

def test_GameStateMarshallingWithoutEnoughPlayers_GameStartAction_PlayersAssignedRoles():
    num_players = random.randint(3,10)
    expected_mafia = num_players//3
    expected_villagers = num_players - expected_mafia
    state = State()
    state.state = Constants.MARSHALLING
    state.players = [Player() for x in range(num_players)]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert len([p for p in state.players if p.role == Roles.MAFIA]) == expected_mafia
    assert len([p for p in state.players if p.role == Roles.VILLAGER]) == expected_villagers

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