import json
from unittest.mock import patch
import mafiaManageSlack
from tests.unit.testHelpers import createMafia
from models.gameState import Game, States
from stateManagers.gameStateManager import Actions
from data_access.dataRepos import GameStateRepo

def createSqsEvent(body):
    return {
        'Records' : [
            {
                'body':json.dumps(body)
            }
        ]
    }
def test_StartGame_CreatesChannelAndInvitesMafia():
    repo = GameStateRepo()
    game = Game()
    testpId = 'test'
    testcId = 'testChannel'
    game.players = [createMafia(id=testpId)]
    game.state = States.NIGHT
    with patch('mafiaManageSlack.WebClient') as slackClientConstructor:
        slackClient = slackClientConstructor.return_value
        slackClient.conversations_create.return_value = {'channel':{'id':testcId}}
        mafiaManageSlack.lambda_handler(createSqsEvent({'state':repo._serializeGame(game), 'action':Actions.START_GAME}), None)
        slackClient.conversations_create.assert_called_with(name='mafia-secrets', is_private=True)
        slackClient.conversations_invite.assert_called_with(channel=testcId, users=testpId)
        slackClient.chat_postMessage.assert_called_with(channel=testcId, text='You are members of the local mafia. Rabble-rousers in the village have decided to make a stand against you. It is time you taught them a lesson...')