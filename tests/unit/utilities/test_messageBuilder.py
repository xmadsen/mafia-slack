from util.game_message_builder import get_state_change_message, build_roster_message
from stateManagers.gameStateManager import Actions
from models.gameState import Game, States
from models.player import Player

def test_addPlayerSuccess():
    p_id = "test"
    message = get_state_change_message({}, True, Actions.ADD_PLAYER, p_id)

    assert message == f"<@{p_id}> has joined the game!"

def test_addPlayerFailure_AlreadyJoined():
    p_id = "test"
    game = Game()
    game.players.append(Player(p_id))
    message = get_state_change_message(game, False, Actions.ADD_PLAYER, p_id)

    assert message == f"You can't join if you're already in."

def test_addPlayerFailure_GameStarted():
    game = Game()
    game.state = States.NIGHT
    message = get_state_change_message(game, False, Actions.ADD_PLAYER, None)

    assert message == f"The game has started. Maybe next time."

def test_removePlayerSuccess():
    p_id = "test"
    message = get_state_change_message({}, True, Actions.REMOVE_PLAYER, p_id)

    assert message == f"<@{p_id}> has left the game!"

def test_removePlayerFailure_GameStarted():
    game = Game()
    game.state = States.NIGHT
    message = get_state_change_message(game, False, Actions.REMOVE_PLAYER, None)

    assert message == f"The game has started. You can't leave now!"

def test_startGameSuccess():
    message = get_state_change_message(Game(), True, Actions.START_GAME, None)
    assert message == f"The game is starting now! If you are in the mafia you will be notified...\n{build_roster_message(Game())}"

def test_startGameFailure():
    message = get_state_change_message({}, False, Actions.START_GAME, None)
    assert message == "The game can't start with less than 4 players!"

def test_playerMurderedSuccess():
    game = Game()
    game.state = States.DAY
    p_id = "test"
    message = get_state_change_message(game, True, Actions.MURDER, target=p_id)
    assert message == f"Another beautiful morning! One that <@{p_id}> won't get to experience, for they are dead! Murdered in the night! One among you is the culprit!"