import pytest
import random
from models.gameState import Game, States as GameStates
from models.player import Player, Roles, States as PlayerStates
from stateManagers.gameStateManager import GameStateManager, Actions
from tests.unit.testHelpers import createMafia, createVillager

def test_GameStateTrial_FoundNotGuiltyAction_StateIsDayPlayerOnTrialIsAlive():
    state = Game()
    state.state = GameStates.TRIAL
    systemUnderTest = GameStateManager(state)
    player = createVillager('test')
    player.state = PlayerStates.ON_TRIAL
    state.players = [player]

    systemUnderTest.transition(Actions.NOT_GUILTY)

    assert state.state == GameStates.DAY
    assert player.state == PlayerStates.ALIVE

def test_GameStateTrial_FoundGuiltyAction_StateIsNightPlayerOnTrialIsDead():
    state = Game()
    state.state = GameStates.TRIAL
    systemUnderTest = GameStateManager(state)
    player = createVillager('test')
    player.state = PlayerStates.ON_TRIAL
    state.players = [player, createVillager(), createVillager() ,createMafia()]

    systemUnderTest.transition(Actions.GUILTY)

    assert state.state == GameStates.NIGHT
    assert player.state == PlayerStates.DEAD

def test_GameStateTrial_LastMafiaMemberFoundGuilty_StateIsGameOver():
    state = Game()
    state.state = GameStates.TRIAL
    systemUnderTest = GameStateManager(state)
    player = createMafia('test')
    player.state = PlayerStates.ON_TRIAL
    state.players = [player]

    systemUnderTest.transition(Actions.GUILTY)

    assert state.state == GameStates.GAME_OVER
    assert player.state == PlayerStates.DEAD
