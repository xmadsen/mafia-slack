import pytest
from models.gameState import Game, States as GameStates
from models.player import Player, Roles, States as PlayerStates
from stateManagers import getInstance, Actions
from tests.unit.testHelpers import createVillager, createMafia

def test_GameStateNight_MurderAction_StateIsDayPlayerDead():
    player = createVillager('test')
    mafia = createMafia('mafia')
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player, createVillager(), createVillager(), mafia]
    systemUnderTest = getInstance(state)

    systemUnderTest.transition(Actions.MURDER, player.id, mafia.id)

    assert state.state == GameStates.DAY
    assert player.state == PlayerStates.DEAD

def test_GameStateNight_MurderResultsInVillagerCountEqualingMafia_StateIsGameOver():
    player = createVillager('test')
    mafia = createMafia('mafia')
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player, createVillager(), mafia]
    systemUnderTest = getInstance(state)

    systemUnderTest.transition(Actions.MURDER, player.id, mafia.id)

    assert state.state == GameStates.GAME_OVER
    assert player.state == PlayerStates.DEAD

def test_MultipleMafiaMembers_MustAgreeOnWhoToKill():
    player1 = createVillager('test1')
    player2 = createVillager('test2')
    mafia1 = createMafia('mafia1')
    mafia2 = createMafia('mafia2')
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player1, player2, createVillager(), createVillager(), mafia1, mafia2]
    systemUnderTest = getInstance(state)
    #mafia 1 wants to kill player 1
    systemUnderTest.transition(Actions.MURDER, player1.id, mafia1.id)

    assert state.state == GameStates.NIGHT
    assert player1.state == PlayerStates.ALIVE

    #mafia 2 wants to kill player 2
    systemUnderTest.transition(Actions.MURDER, player2.id, mafia2.id)

    assert state.state == GameStates.NIGHT
    assert player1.state == PlayerStates.ALIVE
    assert player2.state == PlayerStates.ALIVE

    #mafia 1 decides to agree and kill player2 instead
    systemUnderTest.transition(Actions.MURDER, player2.id, mafia1.id)

    assert state.state == GameStates.DAY
    assert player2.state == PlayerStates.DEAD

def test_VillagerCanNotMurder():
    player1 = createVillager('test1')
    player2 = createVillager('test1')
    mafia = createMafia('mafia')
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player1, player2, mafia]
    systemUnderTest = getInstance(state)

    systemUnderTest.transition(Actions.MURDER, player2.id, player1.id)

    assert state.state == GameStates.NIGHT
    assert player2.state == PlayerStates.ALIVE