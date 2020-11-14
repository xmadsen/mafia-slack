import pytest
import random
from models.gameState import Game, States as GameStates
from models.player import Player, Roles
from stateManagers import getInstance, Actions
from tests.unit.testHelpers import createVillager


def test_GameStateMarshallingWithEnoughPlayers_GameStartAction_StateIsNight():
    state = Game()
    state.state = GameStates.MARSHALLING
    state.players = [Player(), Player(), Player(), Player()]
    systemUnderTest = getInstance(state)

    success = systemUnderTest.transition(Actions.START_GAME)

    assert state.state == GameStates.NIGHT
    assert success


def test_GameStateMarshallingWithoutEnoughPlayers_GameStartAction_StateIsMarshalling():
    state = Game()
    state.state = GameStates.MARSHALLING
    state.players = [Player(), Player(), Player()]
    systemUnderTest = getInstance(state)

    success = systemUnderTest.transition(Actions.START_GAME)

    assert state.state == GameStates.MARSHALLING
    assert not success


def test_GameStateMarshallingWithEnoughPlayers_GameStartAction_PlayersAssignedRoles():
    num_players = random.randint(4, 10)
    expected_mafia = num_players//3
    expected_villagers = num_players - expected_mafia
    state = Game()
    state.state = GameStates.MARSHALLING
    state.players = [Player() for x in range(num_players)]
    systemUnderTest = getInstance(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert len([p for p in state.players if p.role ==
                Roles.MAFIA]) == expected_mafia
    assert len([p for p in state.players if p.role ==
                Roles.VILLAGER]) == expected_villagers


def test_GameStateMarshalling_AddPlayerAction_PlayerAdded():
    state = Game()
    p_id = 'test'
    state.state = GameStates.MARSHALLING
    systemUnderTest = getInstance(state)

    success = systemUnderTest.transition(Actions.ADD_PLAYER, executor=p_id)

    assert p_id in [p.id for p in state.players]
    assert success


def test_GameStateMarshalling_RemovePlayerAction_PlayerRemoved():
    state = Game()
    state.state = GameStates.MARSHALLING
    systemUnderTest = getInstance(state)
    player = createVillager('test')
    state.players = [player]

    success = systemUnderTest.transition(
        Actions.REMOVE_PLAYER, executor=player.id)

    assert player not in state.players
    assert success

# TODO add non happy path tests


def test_GameStateMarshalling_AddPlayerWithDupeId_PlayerNotAdded():
    state = Game()
    p_id = 'test'
    state.state = GameStates.MARSHALLING
    systemUnderTest = getInstance(state)

    systemUnderTest.transition(Actions.ADD_PLAYER, p_id)
    success = systemUnderTest.transition(Actions.ADD_PLAYER, p_id)

    assert len(state.players) == 1
    assert not success
