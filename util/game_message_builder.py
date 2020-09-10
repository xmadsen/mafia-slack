from stateManagers.gameStateManager import Actions
def get_state_change_message(gameState, actionSuccess, action, playerId):
    if action == Actions.ADD_PLAYER:
        if actionSuccess:
            return f'<@{playerId}> has joined the game!'
