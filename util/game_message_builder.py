from stateManagers.gameStateManager import Actions
from models.player import Roles
from models.player import States as PlayerStates
from models.gameState import States
from util.constants import Emoji, Header
from util.messagetext import MessageText as txt


def identify_player(gameState, id):
    player = gameState.findPlayerWithId(id)
    if player.role == Roles.MAFIA:
        return txt.KILLED_MAFIA
    if player.role == Roles.VILLAGER:
        return txt.KILLED_VILLAGER


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
        message = txt.VILLAGERS_WIN
    else:
        message = txt.MAFIA_WINS
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
    return txt.HOW_TO_VOTE


def build_how_to_accuse_message():
    return txt.HOW_TO_ACCUSE


def get_state_change_message(gameState, actionSuccess, action, executor=None,
                             target=None):
    if action == Actions.ADD_PLAYER:
        if actionSuccess:
            message = txt.ADD_PLAYER_SUCCESS.substitute(
                executor=executor,
                num_players=len(gameState.players)
            )
            header = Header.SETUP
        elif executor in [p.id for p in gameState.players]:
            message = txt.ADD_PLAYER_ALREADY_IN
            header = Header.ERROR
        elif gameState.state != States.MARSHALLING:
            message = txt.ADD_PLAYER_GAME_ALREADY_STARTED
            header = Header.ERROR
        else:
            message = txt.ADD_PLAYER_FAILURE_GENERIC
            header = Header.ERROR
    elif action == Actions.REMOVE_PLAYER:
        if actionSuccess:
            message = txt.REMOVE_PLAYER_SUCCESS.substitute(executor=executor)
            header = Header.PLAYER_LEFT
        elif gameState.state != States.MARSHALLING:
            message = txt.REMOVE_PLAYER_FAILURE
            header = Header.ERROR
    elif action == Actions.START_GAME:
        if actionSuccess:
            message = txt.START_GAME_SUCCESS.substitute(
                message=build_roster_message(gameState)
            )
            header = Header.NIGHT
        else:
            message = txt.START_GAME_FAILURE
            header = Header.ERROR
    elif action == Actions.MURDER:
        if actionSuccess:
            if gameState.state == States.DAY:
                message = txt.MURDER_DAY.substitute(
                    target=target,
                    accuse_message=build_how_to_accuse_message())
                header = Header.MORNING
            elif gameState.state == States.GAME_OVER:
                message = txt.MURDER_GAMEOVER.substitute(
                    target=target,
                    gameover_message=build_gameover_message(gameState)
                )
                header = Header.GAMEOVER
        else:
            message = txt.MURDER_FAILED
            header = Header.ERROR
    elif action == Actions.ACCUSE:
        if actionSuccess and gameState.state == States.TRIAL:
            message = txt.ACCUSE_SECONDED.substitute(
                target=target,
                executor=executor,
                howtovotemessage=build_how_to_cast_vote_message()
            )
            header = Header.TRIAL
        elif actionSuccess:
            message = txt.ACCUSE_FIRSTTIME.substitute(
                target=target,
                executor=executor,
                howtoaccusemessage=build_how_to_accuse_message()
            )
            header = Header.ACCUSED
        else:
            message = txt.ACCUSE_INVALID
            header = Header.ERROR
    elif action == Actions.GUILTY or action == Actions.NOT_GUILTY:
        if actionSuccess:
            message = txt.VOTE.substitute(
                executor=executor,
                action=action
            )
            message = f'<@{executor}> casts their ballot. {action}!\n'
            if gameState.state == States.NIGHT:
                message += txt.VOTED_GUILTY.substitute(
                    guilty=gameState.last_accused,
                    killedmessage=identify_player(
                        gameState, gameState.last_accused),
                    roster=build_roster_message(gameState)
                )
                header = Header.GUILTY + "\n" + Header.NIGHT
            elif gameState.state == States.GAME_OVER:
                message += txt.VOTED_GUILTY_GAMEOVER.substitute(
                    guilty=gameState.last_accused,
                    killedmessage=identify_player(gameState,
                                                  gameState.last_accused),
                    gameovermessage=build_gameover_message(gameState)
                )
                header = Header.GUILTY + "\n" + Header.GAMEOVER
            elif gameState.state == States.DAY:
                message += txt.VOTED_INNOCENT.substitute(
                    innocent=gameState.last_accused
                )
                header = Header.INNOCENT
            else:
                message += txt.VOTED_STILL_IN_PROGRESS.substitute(
                    executor=executor,
                    action=action,
                    guiltyvotes=gameState.voteCount(Actions.GUILTY),
                    innocentvotes=gameState.voteCount(Actions.NOT_GUILTY),
                    howtovotemessage=build_how_to_cast_vote_message()
                )
                header = Header.TRIAL
        else:
            message = txt.CANNOT_VOTE
            header = Header.ERROR

    return message, header
