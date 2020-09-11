from stateManagers.gameStateManager import Actions
from models.gameState import States
def get_state_change_message(gameState, actionSuccess, action, playerId):
    if action == Actions.ADD_PLAYER:
        if actionSuccess:
            return f'<@{playerId}> has joined the game!'
        elif playerId in [p.id for p in gameState.players]:
            return "You can't join if you're already in."
        elif gameState.state != States.MARSHALLING:
            return "The game has started. Maybe next time."
        else:
            return "Something is wrong. You can't join the game."
    elif action == Actions.REMOVE_PLAYER:
        if actionSuccess:
            return f'<@{playerId}> has left the game!'
        elif gameState.state != States.MARSHALLING:
            return "The game has started. You can't leave now!"
    elif action == Actions.START_GAME:
        if actionSuccess:
            return "The game is starting now! If you are in the mafia you will be notified..."
        else:
            return "The game can't start with less than 4 players!"