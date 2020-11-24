import json
import os
from unittest.mock import patch, ANY
import mafiaManageSlack
from tests.unit.testHelpers import createMafia
from models.gameState import Game, States
from stateManagers.gameStateManager import Actions
from data_access.dataRepos import MafiaSerializer

os.environ['DYNAMODB_TABLE'] = 'test_table'
os.environ['TOKEN_SOURCE'] = 'test_table2'


def createSqsEvent(body):
    return {
        'Records': [
            {
                'body': json.dumps(body)
            }
        ]
    }


def test_StartGame_CreatesChannelAndInvitesMafia():
    serializer = MafiaSerializer()
    game = Game()
    testpId = 'test'
    testMafiaChannelId = 'testChannel'
    game.players = [createMafia(id=testpId)]
    game.state = States.NIGHT
    game.meta = {'channel_id': 'channel'}
    with patch('mafiaManageSlack.WebClient') as slackClientConstructor:
        with patch('mafiaManageSlack.get_state_change_message') as messageBuilder:
            messageBuilder.return_value = "message","header"
            with patch('mafiaManageSlack.get_blocks_for_message') as blockBuilder:
                with patch('data_access.dataRepos.boto3'):
                    with patch('mafiaManageSlack.boto3'):
                        slackClient = slackClientConstructor.return_value
                        slackClient.conversations_create.return_value = {
                            'channel': {'id': testMafiaChannelId}}
                        mafiaManageSlack.lambda_handler(createSqsEvent({'state': serializer.SerializeGame(
                            game), 'action': Actions.START_GAME, 'source': 'initiator', 'target': None}), None)
                        slackClient.conversations_create.assert_called_with(
                            name='mafia-secrets', is_private=True)
                        slackClient.conversations_invite.assert_called_with(
                            channel=testMafiaChannelId, users=testpId)
                        slackClient.chat_postMessage.assert_called_with(
                            channel=testMafiaChannelId, blocks=blockBuilder.return_value)


def test_RecordReceived_GenerateMessageAndBroadcastToChannel():
    serializer = MafiaSerializer()
    game = Game()
    testExecutorId = 'source'
    testTargetId = 'target'
    testMainChannelId = 'testChannel'
    game.meta = {'channel_id': testMainChannelId}
    with patch('mafiaManageSlack.GameStateRepo'):
        with patch('mafiaManageSlack.WebClient') as slackClientConstructor:
            with patch('mafiaManageSlack.get_state_change_message') as messageBuilder:
                messageBuilder.return_value = "message","header"
                with patch('mafiaManageSlack.get_blocks_for_message') as blockBuilder:
                    with patch('mafiaManageSlack.boto3'):
                        slackClient = slackClientConstructor.return_value
                        mafiaManageSlack.lambda_handler(createSqsEvent({'state': serializer.SerializeGame(
                            game), 'action': 'ACTION', 'source': testExecutorId, 'target': testTargetId}), None)
                        blockBuilder.assert_called_with(messageBuilder.return_value[0],messageBuilder.return_value[1]) #assert the block builder is invoked with message builder output
                        slackClient.chat_postMessage.assert_called_with(
                            channel=testMainChannelId, blocks=blockBuilder.return_value) #assert the block builder output is posted to slack
                        messageBuilder.assert_called_with(
                            ANY, True, 'ACTION', testExecutorId, testTargetId)
