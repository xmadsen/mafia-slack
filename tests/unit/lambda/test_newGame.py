from unittest.mock import patch
from mafiaNewGame import lambda_handler
import json

def test_ValidRequest_Returns200():
    teamId = 'test'
    with patch('mafiaNewGame.GameStateRepo') as mockRepo:
        result = lambda_handler({"body": f"team_id={teamId}", "isBase64Encoded": False},None)
    resultBody = json.loads(result['body'])
    
    assert result['statusCode'] == 200
    assert resultBody['game_id'] == teamId
