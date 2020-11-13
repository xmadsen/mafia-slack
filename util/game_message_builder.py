from stateManagers.gameStateManager import Actions
from models.player import Roles
from models.player import States as PlayerStates
from models.gameState import States
from util.constants import Emoji


def identify_player(gameState, id):
    player = gameState.findPlayerWithId(id)
    if player.role == Roles.MAFIA:
        return 'Justice prevails! A member of the mafia has been rooted out.'
    if player.role == Roles.VILLAGER:
        return 'In truth, they were no criminal. An innocent villager has been killed.'


def build_gameover_message(gameState):
    if gameState.determineWinner() == Roles.VILLAGER:
        message = 'The villagers have shown bravery and determination in their resistance to organized crime. The mafia will think twice before trying again. GAME OVER. The villagers win.'
    else:
        message = 'The mafia has made an example of this village. No longer will they resist the criminal empire. GAME OVER. The mafia wins.'
    return message + '\n' + build_roster_message(gameState, True)


def role_emoji(role):
    return Emoji.mafia if role == Roles.MAFIA else Emoji.villager


def state_emoji(state):
    return Emoji.alive if state == PlayerStates.ALIVE else Emoji.dead


def build_roster_message(gameState, isGameOver=False):
    roster_message = ''
    for p in gameState.players:
        if isGameOver:
            roster_message += f'{role_emoji(p.role)}  {p.role.capitalize()} {"   " if p.role == Roles.MAFIA else ""}| '
        roster_message += f'{state_emoji(p.state)}  {p.state.capitalize()} | <@{p.id}>\n'

    return roster_message


def build_how_to_cast_vote_message():
    return 'To vote guilty: /mafia vote-guilty\nto vote not guilty: /mafia vote-innocent'


def build_how_to_accuse_message():
    return 'To accuse or second an accusation: /mafia accuse @who-to-accuse'


def get_state_change_message(gameState, actionSuccess, action, executor=None, target=None):
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
            return f"The game is starting now! If you are in the mafia you will be notified...\n\nNight falls on the village. It is peaceful here, but not for long. The mafia is up to something.\n{build_roster_message(gameState)}"
        else:
            return "The game can't start with less than 4 players!"
    elif action == Actions.MURDER:
        if actionSuccess:
            if gameState.state == States.DAY:
                return f"Another beautiful morning! One that <@{target}> won't get to experience, for they are dead! Murdered in the night! One among you is the culprit!\n{build_how_to_accuse_message()}"
            elif gameState.state == States.GAME_OVER:
                return f'<@{target}> is found dead in the morning. {build_gameover_message(gameState)}'
        else:
            return 'Hit attempt failed. Either this person does not exist or they are a member of the mafia and are under protection. Make sure you are tagging your target with @'
    elif action == Actions.ACCUSE:
        if actionSuccess and gameState.state == States.TRIAL:
            return f'The charge against <@{target}> has been seconded by <@{executor}>. In accordance with the village by-laws they now stand before a jury of their peers. The penalty for guilt is... DEATH. Will you vote guilty or not guilty?\n{build_how_to_cast_vote_message()}'
        elif actionSuccess:
            return f'<@{target}> has been formally accused of being a member of the mafia by <@{executor}>. This is a serious accusation and before they stand trial it must be seconded!\n{build_how_to_accuse_message()}'
        else:
            return 'Sorry that is not a valid target.'
    elif action == Actions.GUILTY or Actions.NOT_GUILTY:
        if actionSuccess:
            if gameState.state == States.NIGHT:
                return f'<@{executor}> casts their ballot. {action}! <@{gameState.last_accused}> has been found guilty. {identify_player(gameState, gameState.last_accused)} They swing from the gallows as night falls on the village.\n{build_roster_message(gameState)}'
            elif gameState.state == States.GAME_OVER:
                return f'<@{executor}> casts their ballot. {action}! <@{gameState.last_accused}> has been found guilty. {identify_player(gameState, gameState.last_accused)} {build_gameover_message(gameState)} '
            elif gameState.state == States.DAY:
                return f'<@{executor}> casts their ballot. {action}! <@{gameState.last_accused}> has mounted a successful defense and been found not guilty. Someone\'s gonna hang before the day is through. The question is who?'
            else:
                return f'<@{executor}> casts their ballot. {action}!\nThe current vote is:\n{gameState.voteCount(Actions.GUILTY)} Guilty\n{gameState.voteCount(Actions.NOT_GUILTY)} Not Guilty\n{build_how_to_cast_vote_message()}'
        else:
            return 'Sorry! You can\'t vote!'
