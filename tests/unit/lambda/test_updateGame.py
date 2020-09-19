from unittest.mock import patch, MagicMock
from mafiaUpdateGame import lambda_handler
import json

def test_ValidRequest_Returns200():
    teamId = 'test'
    userId = 'testUser'
    with patch('mafiaUpdateGame.GameStateRepo') as mockRepo:
        with patch('mafiaUpdateGame.GameStateManager') as mockStateManager:
            with patch('mafiaUpdateGame.json.dumps'):
                with patch('mafiaUpdateGame.boto3'):
                    result = lambda_handler({"body": f"team_id={teamId}&user_id={userId}", "action" : "ADD_PLAYER", "isBase64Encoded": False},None)
    
    assert result['statusCode'] == 200

def test_ValidRequestWithOptionalArgs_Returns200():
    teamId = 'test'
    userId = 'testUser'
    action = 'ADD_PLAYER'
    with patch('mafiaUpdateGame.GameStateRepo') as mockRepo:
        mockState = mockRepo.return_value.GetGameState.return_value
        with patch('mafiaUpdateGame.GameStateManager') as mockStateManager:
            transition_result = mockStateManager.return_value.transition.return_value
            with patch('mafiaUpdateGame.json.dumps'):
                with patch('mafiaUpdateGame.boto3'):
                    with patch('mafiaUpdateGame.get_state_change_message') as messageBuilder:
                        with patch('mafiaUpdateGame.extract_user_id') as idExtractor:
                            result = lambda_handler({"body": f"team_id={teamId}&user_id={userId}&text=testTest", "action" : action, "isBase64Encoded": False},None)
                            messageBuilder.assert_called_with(mockState, transition_result, action, userId, idExtractor.return_value)
    
    assert result['statusCode'] == 200
