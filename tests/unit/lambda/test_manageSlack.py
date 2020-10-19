import json,os
from unittest.mock import patch, ANY
import mafiaManageSlack
from tests.unit.testHelpers import createMafia
from models.gameState import Game, States
from stateManagers.gameStateManager import Actions
from data_access.dataRepos import GameStateRepo

os.environ['DYNAMODB_TABLE'] = 'test_table'
os.environ['TOKEN_SOURCE'] = 'test_table2'

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
    testMafiaChannelId = 'testChannel'
    game.players = [createMafia(id=testpId)]
    game.state = States.NIGHT
    game.meta = {'channel_id':'channel'}
    with patch('mafiaManageSlack.WebClient') as slackClientConstructor:
        with patch('mafiaManageSlack.get_state_change_message') as messageBuilder:
            with patch('data_access.dataRepos.boto3'):
                with patch('mafiaManageSlack.boto3'):
                    slackClient = slackClientConstructor.return_value
                    slackClient.conversations_create.return_value = {'channel':{'id':testMafiaChannelId}}
                    mafiaManageSlack.lambda_handler(createSqsEvent({'state':repo._serializeGame(game), 'action':Actions.START_GAME, 'source': 'initiator', 'target':None}), None)
                    slackClient.conversations_create.assert_called_with(name='mafia-secrets', is_private=True)
                    slackClient.conversations_invite.assert_called_with(channel=testMafiaChannelId, users=testpId)
                    slackClient.chat_postMessage.assert_called_with(channel=testMafiaChannelId, text='You are members of the local mafia. Rabble-rousers in the village have decided to make a stand against you. It is time you taught them a lesson...\nKill one of them using the command: /mafiahit @who-to-kill\nIf there is more than one member of the mafia you must all /mafiahit the same villager before they will be killed.')

def test_RecordReceived_GenerateMessageAndBroadcastToChannel():
    repo = GameStateRepo()
    game = Game()
    testExecutorId = 'source'
    testTargetId = 'target'
    testMainChannelId = 'testChannel'
    game.meta = {'channel_id' : testMainChannelId}
    with patch('mafiaManageSlack.WebClient') as slackClientConstructor:
        with patch('mafiaManageSlack.get_state_change_message') as messageBuilder:
            with patch('mafiaManageSlack.boto3'):
                slackClient = slackClientConstructor.return_value
                mafiaManageSlack.lambda_handler(createSqsEvent({'state':repo._serializeGame(game), 'action':'ACTION', 'source': testExecutorId, 'target':testTargetId}), None)
                slackClient.chat_postMessage.assert_called_with(channel=testMainChannelId, text=messageBuilder.return_value)
                messageBuilder.assert_called_with(ANY, True, 'ACTION', testExecutorId, testTargetId)