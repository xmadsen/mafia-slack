from mafiaUpdateGame import lambda_handler, convert_to_action
from util.messagetext import MessageText as txt
import os
from unittest.mock import patch, MagicMock
os.environ['QUEUE_URL'] = 'test_url'


def test_ValidRequest_Returns200():
    teamId = 'test'
    userId = 'testUser'
    with patch('mafiaUpdateGame.GameStateRepo') as mockRepo:
        with patch('mafiaUpdateGame.getInstance') as mockStateManager:
            with patch('mafiaUpdateGame.json.dumps'):
                with patch('mafiaUpdateGame.boto3'):
                    result = lambda_handler(
                        {
                            "body": f"team_id={teamId}&user_id={userId}&channel_id=channel",
                            "action": "ADD_PLAYER",
                            "isBase64Encoded": False},
                        None)

    assert result['statusCode'] == 200


def test_SuccessfulRequestWithOptionalArgs_SendsDataToManageSlackQueue():
    teamId = 'test'
    userId = 'testUser'
    action = 'ADD_PLAYER'
    with patch('mafiaUpdateGame.GameStateRepo'):
        with patch('mafiaUpdateGame.MafiaSerializer') as mockSerializer:
            mockState = mockSerializer.return_value.SerializeGame.return_value
            with patch('mafiaUpdateGame.getInstance') as mockStateManager:
                transition_result = mockStateManager.return_value.transition.return_value = True
                with patch('mafiaUpdateGame.json.dumps') as mockJsonDumper:
                    with patch('mafiaUpdateGame.boto3') as mockboto3:
                        mockAwsClient = mockboto3.client.return_value
                        with patch('mafiaUpdateGame.extract_user_id') as idExtractor:
                            result = lambda_handler(
                                {
                                    "body": f"team_id={teamId}&user_id={userId}&text=testTest&channel_id=channel",
                                    "action": action,
                                    "isBase64Encoded": False},
                                None)
                            mockAwsClient.send_message.assert_called_with(
                                QueueUrl='test_url', MessageBody=mockJsonDumper.return_value)
                            mockJsonDumper.assert_any_call(
                                {'state': mockState, 'action': action, 'source': userId, 'target': idExtractor.return_value})

    assert result['statusCode'] == 200


def test_SuccessfulRequestWithActionInText_CorrectActionExtracted():
    teamId = 'test'
    userId = 'testUser'
    action = 'join'
    with patch('mafiaUpdateGame.GameStateRepo'):
        with patch('mafiaUpdateGame.MafiaSerializer') as mockSerializer:
            mockState = mockSerializer.return_value.SerializeGame.return_value
            with patch('mafiaUpdateGame.getInstance') as mockStateManager:
                transition_result = mockStateManager.return_value.transition.return_value = True
                with patch('mafiaUpdateGame.json.dumps') as mockJsonDumper:
                    with patch('mafiaUpdateGame.boto3') as mockboto3:
                        mockAwsClient = mockboto3.client.return_value
                        with patch('mafiaUpdateGame.extract_user_id') as idExtractor:
                            result = lambda_handler(
                                {
                                    "body": f"team_id={teamId}&user_id={userId}&text={action}+testTest&channel_id=channel",
                                    "isBase64Encoded": False},
                                None)
                            mockAwsClient.send_message.assert_called_with(
                                QueueUrl='test_url', MessageBody=mockJsonDumper.return_value)
                            mockJsonDumper.assert_any_call({'state': mockState, 'action': convert_to_action(
                                action.upper()), 'source': userId, 'target': idExtractor.return_value})


def test_help_message():
    teamId = 'test'
    userId = 'testUser'
    action = 'test'
    with patch('mafiaUpdateGame.GameStateRepo') as mockRepo:
        mockState = mockRepo.return_value._serializeGame.return_value
        with patch('mafiaUpdateGame.getInstance') as mockStateManager:
            transition_result = mockStateManager.return_value.transition.return_value = True
            with patch('mafiaUpdateGame.json.dumps') as mockJsonDumper:
                with patch('mafiaUpdateGame.boto3') as mockboto3:
                    mockAwsClient = mockboto3.client.return_value
                    with patch('mafiaUpdateGame.extract_user_id') as idExtractor:
                        result = lambda_handler(
                            {
                                "body": f"team_id={teamId}&user_id={userId}&text={action}+testTest&channel_id=channel",
                                "isBase64Encoded": False},
                            None)
                        mockJsonDumper.assert_any_call(
                            {'response_type': 'ephemeral', 'text': txt.HELP_MESSAGE})
    assert result['statusCode'] == 200
