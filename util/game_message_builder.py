from stateManagers.gameStateManager import Actions
from models.gameState import States
def get_state_change_message(gameState, actionSuccess, action, executor=None, target = None):
    if action == Actions.ADD_PLAYER:
        if actionSuccess:
            return f'<@{executor}> has joined the game!'
        elif executor in [p.id for p in gameState.players]:
            return "You can't join if you're already in."
        elif gameState.state != States.MARSHALLING:
            return "The game has started. Maybe next time."
        else:
            return "Something is wrong. You can't join the game."
    elif action == Actions.REMOVE_PLAYER:
        if actionSuccess:
            return f'<@{executor}> has left the game!'
        elif gameState.state != States.MARSHALLING:
            return "The game has started. You can't leave now!"
    elif action == Actions.START_GAME:
        if actionSuccess:
            return "The game is starting now! If you are in the mafia you will be notified..."
        else:
            return "The game can't start with less than 4 players!"
    elif action == Actions.MURDER:
        if actionSuccess and gameState.state == States.DAY:
            return f"Another beautiful morning! One that <@{target}> won't get to experience, for they are dead! Murdered in the night! One among you is the culprit!"
        else:
            return 'Hit attempt failed. Either this person does not exist or they are a member of the mafia and are under protection. Make sure you are tagging your target with @'