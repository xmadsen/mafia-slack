import pytest
import random
from models.gameState import Game, States as GameStates
from models.player import Player, Roles
from stateManagers.gameStateManager import GameStateManager, Actions
from tests.unit.testHelpers import createVillager

def test_GameStateMarshallingWithEnoughPlayers_GameStartAction_StateIsNight():
    state = Game()
    state.state = GameStates.MARSHALLING
    state.players = [Player(), Player(), Player(), Player()]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert state.state == GameStates.NIGHT

def test_GameStateMarshallingWithoutEnoughPlayers_GameStartAction_StateIsMarshalling():
    state = Game()
    state.state = GameStates.MARSHALLING
    state.players = [Player(),Player(),Player()]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert state.state == GameStates.MARSHALLING

def test_GameStateMarshallingWithEnoughPlayers_GameStartAction_PlayersAssignedRoles():
    num_players = random.randint(4,10)
    expected_mafia = num_players//3
    expected_villagers = num_players - expected_mafia
    state = Game()
    state.state = GameStates.MARSHALLING
    state.players = [Player() for x in range(num_players)]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.START_GAME)

    assert len([p for p in state.players if p.role == Roles.MAFIA]) == expected_mafia
    assert len([p for p in state.players if p.role == Roles.VILLAGER]) == expected_villagers

def test_GameStateMarshalling_AddPlayerAction_PlayerAdded():
    state = Game()
    state.state = GameStates.MARSHALLING
    systemUnderTest = GameStateManager(state)
    player = Player()

    systemUnderTest.transition(Actions.ADD_PLAYER, player)

    assert player in state.players

def test_GameStateMarshalling_RemovePlayerAction_PlayerRemoved():
    state = Game()
    state.state = GameStates.MARSHALLING
    systemUnderTest = GameStateManager(state)
    player = createVillager('test')
    state.players = [player]

    systemUnderTest.transition(Actions.REMOVE_PLAYER, player.id)

    assert player not in state.players

#TODO add non happy path tests