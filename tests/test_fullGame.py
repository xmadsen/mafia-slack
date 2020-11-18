import pytest
from models.gameState import Game, States as GameStates
from models.player import Player, Roles, States as PlayerStates
from stateManagers import getInstance, Actions
from tests.unit.testHelpers import createMafia, createVillager


def test_FullGame_MafiaWins():
    game = Game()
    manager = getInstance(game)
    print('game marshalling no players yet.')
    manager.printGameState()

    manager.transition(Actions.ADD_PLAYER, executor='1')
    manager.transition(Actions.ADD_PLAYER, executor='2')
    manager.transition(Actions.ADD_PLAYER, executor='3')
    manager.transition(Actions.ADD_PLAYER, executor='4')
    print('enough players have joined to start')
    manager.printGameState()

    manager.transition(Actions.START_GAME)
    print('game begins')
    manager.printGameState()
    manager = getInstance(game)

    mafia = [p for p in manager.gameState.players if p.role == Roles.MAFIA][0]
    to_kill = [p for p in manager.gameState.players if p.role ==
               Roles.VILLAGER and p.state == PlayerStates.ALIVE][0]
    manager.transition(Actions.MURDER, to_kill.id, mafia.id)
    print('the mafia has killed a villager')
    manager.printGameState()
    manager = getInstance(game)

    villagers = [p for p in manager.gameState.players if p.role ==
                 Roles.VILLAGER and p.state == PlayerStates.ALIVE]
    to_accuse = villagers[0]
    accuser = villagers[1]
    manager.transition(Actions.ACCUSE, to_accuse.id, accuser.id)
    manager.transition(Actions.ACCUSE, to_accuse.id, mafia.id)
    print('the villagers accuse one of their own')
    manager.printGameState()
    manager = getInstance(game)

    manager.transition(Actions.GUILTY, executor='1')
    manager.transition(Actions.GUILTY, executor='2')
    manager.transition(Actions.GUILTY, executor='3')
    manager.transition(Actions.GUILTY, executor='4')
    print('an innocent man has died')
    print('game over mafia wins. they control the town')
    manager.printGameState()

    assert game.state == GameStates.GAME_OVER


def test_FullGame_VillageWins():
    game = Game()
    manager = getInstance(game)
    print('game marshalling no players yet.')
    manager.printGameState()

    manager.transition(Actions.ADD_PLAYER, executor='1')
    manager.transition(Actions.ADD_PLAYER, executor='2')
    manager.transition(Actions.ADD_PLAYER, executor='3')
    manager.transition(Actions.ADD_PLAYER, executor='4')
    print('enough players have joined to start')
    manager.printGameState()

    manager.transition(Actions.START_GAME)
    manager = getInstance(game)
    print('game begins')
    manager.printGameState()

    mafia = [p for p in manager.gameState.players if p.role == Roles.MAFIA][0]
    to_kill = [p for p in manager.gameState.players if p.role ==
               Roles.VILLAGER and p.state == PlayerStates.ALIVE][0]
    manager.transition(Actions.MURDER, to_kill.id, mafia.id)
    manager = getInstance(game)
    print('the mafia has killed a villager')
    manager.printGameState()

    to_accuse = [p for p in manager.gameState.players if p.role ==
                 Roles.MAFIA and p.state == PlayerStates.ALIVE][0]
    living_villagers = [p for p in manager.gameState.players if p.role ==
                        Roles.VILLAGER and p.state == PlayerStates.ALIVE]
    accuser1, accuser2 = living_villagers[0], living_villagers[1]
    manager.transition(Actions.ACCUSE, to_accuse.id, accuser1.id)
    manager.transition(Actions.ACCUSE, to_accuse.id, accuser2.id)
    manager = getInstance(game)
    print('the villagers accuse a member of the mafia')
    manager.printGameState()

    manager.transition(Actions.GUILTY, executor='1')
    manager.transition(Actions.GUILTY, executor='2')
    manager.transition(Actions.GUILTY, executor='3')
    manager.transition(Actions.GUILTY, executor='4')
    print('the murderer has been executed')
    print('game over village wins. organized crime has been purged from the town')
    manager.printGameState()

    assert game.state == GameStates.GAME_OVER
