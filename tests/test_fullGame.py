import pytest
from models.gameState import Game, States as GameStates
from models.player import Player, Roles, States as PlayerStates
from stateManagers.gameStateManager import GameStateManager, Actions
from tests.unit.testHelpers import createMafia, createVillager

def test_FullGame_MafiaWins():
    game = Game()
    manager = GameStateManager(game)
    print('game marshalling no players yet.')
    manager.printGameState()

    manager.transition(Actions.ADD_PLAYER,Player('1'))
    manager.transition(Actions.ADD_PLAYER,Player('2'))
    manager.transition(Actions.ADD_PLAYER,Player('3'))
    manager.transition(Actions.ADD_PLAYER,Player('4'))
    print('enough players have joined to start')
    manager.printGameState()

    manager.transition(Actions.START_GAME)
    print('game begins')
    manager.printGameState()

    mafia = [p for p in manager.gameState.players if p.role == Roles.MAFIA][0]
    to_kill = [p for p in manager.gameState.players if p.role == Roles.VILLAGER and p.state == PlayerStates.ALIVE][0]
    manager.transition(Actions.MURDER, to_kill.id, mafia.id)
    print('the mafia has killed a villager')
    manager.printGameState()

    to_accuse = [p for p in manager.gameState.players if p.role == Roles.VILLAGER and p.state == PlayerStates.ALIVE][0]
    manager.transition(Actions.ACCUSE, to_accuse.id)
    print('the villagers accuse one of their own')
    manager.printGameState()

    manager.transition(Actions.GUILTY)
    print('an innocent man has died')
    print('game over mafia wins. they control the town')
    manager.printGameState()

    assert game.state == GameStates.GAME_OVER

def test_FullGame_VillageWins():
    game = Game()
    manager = GameStateManager(game)
    print('game marshalling no players yet.')
    manager.printGameState()

    manager.transition(Actions.ADD_PLAYER,Player('1'))
    manager.transition(Actions.ADD_PLAYER,Player('2'))
    manager.transition(Actions.ADD_PLAYER,Player('3'))
    manager.transition(Actions.ADD_PLAYER,Player('4'))
    print('enough players have joined to start')
    manager.printGameState()

    manager.transition(Actions.START_GAME)
    print('game begins')
    manager.printGameState()

    mafia = [p for p in manager.gameState.players if p.role == Roles.MAFIA][0]
    to_kill = [p for p in manager.gameState.players if p.role == Roles.VILLAGER and p.state == PlayerStates.ALIVE][0]
    manager.transition(Actions.MURDER, to_kill.id, mafia.id)
    print('the mafia has killed a villager')
    manager.printGameState()

    to_accuse = [p for p in manager.gameState.players if p.role == Roles.MAFIA and p.state == PlayerStates.ALIVE][0]
    manager.transition(Actions.ACCUSE, to_accuse.id)
    print('the villagers accuse a member of the mafia')
    manager.printGameState()

    manager.transition(Actions.GUILTY)
    print('the murderer has been executed')
    print('game over village wins. organized crime has been purged from the town')
    manager.printGameState()

    assert game.state == GameStates.GAME_OVER