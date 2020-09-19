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
    villager1 = createVillager('v1')
    villager2 = createVillager('v2')
    mafia = createMafia('m')
    player.state = PlayerStates.ON_TRIAL
    state.players = [player, villager2, villager1 ,mafia]

    systemUnderTest.transition(Actions.GUILTY,executor='m')
    assert state.state == GameStates.TRIAL
    systemUnderTest.transition(Actions.NOT_GUILTY,executor='v1')
    assert state.state == GameStates.TRIAL
    systemUnderTest.transition(Actions.NOT_GUILTY,executor='v2')

    assert state.state == GameStates.DAY
    assert player.state == PlayerStates.ALIVE

def test_GameStateTrial_FoundGuiltyAction_StateIsNightPlayerOnTrialIsDead():
    state = Game()
    state.state = GameStates.TRIAL
    systemUnderTest = GameStateManager(state)
    player = createVillager('test')
    villager1 = createVillager('v1')
    villager2 = createVillager('v2')
    mafia = createMafia('m')
    player.state = PlayerStates.ON_TRIAL
    state.players = [player, villager2, villager1 ,mafia]

    systemUnderTest.transition(Actions.NOT_GUILTY,executor='v1')
    systemUnderTest.transition(Actions.GUILTY,executor='v2')
    systemUnderTest.transition(Actions.GUILTY,executor='m')

    assert state.state == GameStates.NIGHT
    assert player.state == PlayerStates.DEAD

def test_GameStateTrial_LastMafiaMemberFoundGuilty_StateIsGameOver():
    state = Game()
    state.state = GameStates.TRIAL
    systemUnderTest = GameStateManager(state)
    mafia = createMafia('test')
    villager1 = createVillager('v1')
    villager2 = createVillager('v2')
    mafia.state = PlayerStates.ON_TRIAL
    state.players = [mafia,villager1,villager2]

    systemUnderTest.transition(Actions.GUILTY,executor='v1')
    systemUnderTest.transition(Actions.GUILTY,executor='v2')

    assert state.state == GameStates.GAME_OVER
    assert mafia.state == PlayerStates.DEAD