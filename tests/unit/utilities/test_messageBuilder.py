from util.game_message_builder import get_state_change_message
from stateManagers.gameStateManager import Actions

def test_addPlayerSuccess():
    p_id = "test"
    message = get_state_change_message({}, True, Actions.ADD_PLAYER, p_id)

    assert message == f"<@{p_id}> has joined the game!"

def test_removePlayerSuccess():
    p_id = "test"
    message = get_state_change_message({}, True, Actions.REMOVE_PLAYER, p_id)

    assert message == f"<@{p_id}> has left the game!"
