from unittest.mock import patch
from mafiaNewGame import lambda_handler
import json

def test_ValidRequest_Returns200():
    teamId = 'test'
    with patch('mafiaNewGame.GameStateRepo') as mockRepoConstructor:
        mockRepo = mockRepoConstructor.return_value
        result = lambda_handler({"body": f"team_id={teamId}&channel_id=channel", "isBase64Encoded": False},None)
        mockRepo.CreateNewGame.assert_called_once_with(teamId, {'channel_id':'channel'})
    resultBody = json.loads(result['body'])
    
    assert result['statusCode'] == 200
    assert resultBody['game_id'] == teamId
