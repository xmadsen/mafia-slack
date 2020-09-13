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
