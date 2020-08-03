import pytest
from models.gameState import Game, States as GameStates
from models.player import Player, Roles, States as PlayerStates
from stateManagers.gameStateManager import GameStateManager, Actions

def test_GameStateNight_MurderAction_StateIsDayPlayerDead():
    player = Player()
    player.id = 'test'
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player, createVillager(), createVillager(), createMafia()]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.MURDER, player.id)

    assert state.state == GameStates.DAY
    assert player.state == PlayerStates.DEAD

def test_GameStateNight_MurderResultsInVillagerCountEqualingMafia_StateIsGameOver():
    player = createVillager()
    player.id = 'test'
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player, createVillager(), createMafia()]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.MURDER, player.id)

    assert state.state == GameStates.GAME_OVER
    assert player.state == PlayerStates.DEAD

def createVillager():
    player = Player()
    player.state = PlayerStates.ALIVE
    player.role = Roles.VILLAGER
    return player

def createMafia():
    player = Player()
    player.state = PlayerStates.ALIVE
    player.role = Roles.MAFIA
    return player