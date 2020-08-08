import pytest
from app.models.gameState import Game, States as GameStates
from app.models.player import Player, Roles, States as PlayerStates
from app.stateManagers.gameStateManager import GameStateManager, Actions
from tests.unit.testHelpers import createVillager, createMafia

def test_GameStateNight_MurderAction_StateIsDayPlayerDead():
    player = createVillager('test')
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player, createVillager(), createVillager(), createMafia()]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.MURDER, player.id)

    assert state.state == GameStates.DAY
    assert player.state == PlayerStates.DEAD

def test_GameStateNight_MurderResultsInVillagerCountEqualingMafia_StateIsGameOver():
    player = createVillager('test')
    state = Game()
    state.state = GameStates.NIGHT
    state.players = [player, createVillager(), createMafia()]
    systemUnderTest = GameStateManager(state)

    systemUnderTest.transition(Actions.MURDER, player.id)

    assert state.state == GameStates.GAME_OVER
    assert player.state == PlayerStates.DEAD
