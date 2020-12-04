from stateManagers.gameStateManager import Actions
from models.player import Roles
from models.player import States as PlayerStates
from models.gameState import States
from util.constants import Emoji, Header


def identify_player(gameState, id):
    player = gameState.findPlayerWithId(id)
    if player.role == Roles.MAFIA:
        return 'Justice prevails! A member of the mafia has been rooted out.'
    if player.role == Roles.VILLAGER:
        return 'In truth, they were no criminal. An innocent villager has '\
            'been killed.'


def get_blocks_for_message(message, header):
    blocks = [{
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": header,
            "emoji": True
        }
    }]

    message_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": message
        }
    }
    blocks.append(message_section)
    return blocks


def build_gameover_message(gameState):
    if gameState.determineWinner() == Roles.VILLAGER:
        message = 'The villagers have shown bravery and determination in'\
            ' their resistance to organized crime. The mafia will think twice'\
            ' before trying again. GAME OVER. The villagers win.'
    else:
        message = 'The mafia has made an example of this village. No longer '\
            'will they resist the criminal empire. GAME OVER. The mafia wins.'
    return message + '\n' + build_roster_message(gameState, True)


def role_emoji(role):
    return Emoji.mafia if role == Roles.MAFIA else Emoji.villager


def state_emoji(state):
    return Emoji.alive if state == PlayerStates.ALIVE else Emoji.dead


def build_roster_message(gameState, isGameOver=False):
    roster_message = ''
    for p in gameState.players:
        if isGameOver:
            roster_message += f'{role_emoji(p.role)}  {p.role.capitalize()}'\
                f' {"   " if p.role == Roles.MAFIA else ""}| '
        roster_message += f'{state_emoji(p.state)}  {p.state.capitalize()}'\
            f' | <@{p.id}>\n'

    return roster_message


def build_how_to_cast_vote_message():
    return 'To vote guilty: ```/mafia vote-guilty```\nTo vote not guilty: '\
        '```/mafia vote-innocent```'


def build_how_to_accuse_message():
    return 'To accuse or second an accusation: ```/mafia accuse @who-to-accuse```'


def get_state_change_message(gameState, actionSuccess, action, executor=None,
                             target=None):
    if action == Actions.ADD_PLAYER:
        if actionSuccess:
            message = f'<@{executor}> has joined the game! {len(gameState.players)} players have joined!'
            header = Header.SETUP
        elif executor in [p.id for p in gameState.players]:
            message = "You can't join if you're already in."
            header = Header.ERROR
        elif gameState.state != States.MARSHALLING:
            message = "The game has started. Maybe next time."
            header = Header.ERROR
        else:
            message = "Something is wrong. You can't join the game."
            header = Header.ERROR
    elif action == Actions.REMOVE_PLAYER:
        if actionSuccess:
            message = f'<@{executor}> has left the game!'
            header = Header.PLAYER_LEFT
        elif gameState.state != States.MARSHALLING:
            message = "The game has started. You can't leave now!"
            header = Header.ERROR
    elif action == Actions.START_GAME:
        if actionSuccess:
            message = f'The game is starting now! If you are in the mafia you '\
                'will be notified...\n\nNight falls on the village. It is '\
                'peaceful here, but not for long. The mafia is up to '\
                f'something.\n{build_roster_message(gameState)}'
            header = Header.NIGHT
        else:
            message = "The game can't start with less than 4 players!"
            header = Header.ERROR
    elif action == Actions.MURDER:
        if actionSuccess:
            if gameState.state == States.DAY:
                message = f'Another beautiful morning! One that <@{target}> '\
                    'won\'t get to experience, for they are dead! Murdered in'\
                    ' the night! One among you is the culprit!\n'\
                    f'{build_how_to_accuse_message()}'
                header = Header.MORNING
            elif gameState.state == States.GAME_OVER:
                message = f'<@{target}> is found dead in the morning. '\
                    f'{build_gameover_message(gameState)}'
                header = Header.GAMEOVER
        else:
            message = 'Hit attempt failed. Either this person does not exist or'\
                ' they are a member of the mafia and are under protection.'\
                ' Make sure you are tagging your target with @.'
            header = Header.ERROR
    elif action == Actions.ACCUSE:
        if actionSuccess and gameState.state == States.TRIAL:
            message = f'The charge against <@{target}> has been seconded by '\
                f'<@{executor}>. In accordance with the village by-laws they'\
                f'now stand before a jury of their peers. The penalty for'\
                f'guilt is... DEATH. Will you vote guilty or not guilty?\n'\
                f'{build_how_to_cast_vote_message()}'
            header = Header.TRIAL
        elif actionSuccess:
            message = f'<@{target}> has been formally accused of being a member'\
                f' of the mafia by <@{executor}>. This is a serious '\
                f'accusation and before they stand trial it must be'\
                f' seconded!\n{build_how_to_accuse_message()}'
            header = Header.ACCUSED
        else:
            message = 'Sorry that is not a valid target.'
            header = Header.ERROR
    elif action == Actions.GUILTY or action == Actions.NOT_GUILTY:
        if actionSuccess:
            message = f'<@{executor}> casts their ballot. {action}!\n'
            if gameState.state == States.NIGHT:
                message += f'<@{gameState.last_accused}> has been found guilty. {identify_player(gameState, gameState.last_accused)} They swing from the gallows as night falls on the village.\n{build_roster_message(gameState)}'
                header = Header.GUILTY + "\n" + Header.NIGHT
            elif gameState.state == States.GAME_OVER:
                message += f'<@{gameState.last_accused}> has been found guilty. {identify_player(gameState, gameState.last_accused)} {build_gameover_message(gameState)} '
                header = Header.GUILTY + "\n" + Header.GAMEOVER
            elif gameState.state == States.DAY:
                message += f'<@{gameState.last_accused}> has mounted a successful defense and been found not guilty. Someone\'s gonna hang before the day is through. The question is who?'
                header = Header.INNOCENT
            else:
                message += f'The current vote is:\n{gameState.voteCount(Actions.GUILTY)} Guilty\n{gameState.voteCount(Actions.NOT_GUILTY)} Not Guilty\n{build_how_to_cast_vote_message()}'
                header = Header.TRIAL
        else:
            message = 'Sorry! You can\'t vote!'
            header = Header.ERROR

    return message, header
