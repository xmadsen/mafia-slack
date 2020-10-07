from unittest.mock import patch
import json, os
os.environ['QUEUE_URL'] = 'test_url'
from mafiaUpdateGame import new_game_lambda_handler as lambda_handler


def test_ValidRequest_Returns200():
    teamId = 'test'
    with patch('mafiaUpdateGame.GameStateRepo') as mockRepoConstructor:
        mockRepo = mockRepoConstructor.return_value
        result = lambda_handler({"body": f"team_id={teamId}&channel_id=channel", "isBase64Encoded": False},None)
        mockRepo.CreateNewGame.assert_called_once_with(teamId, {'channel_id':'channel'})
    resultBody = json.loads(result['body'])
    
    assert result['statusCode'] == 200
    assert resultBody['game_id'] == teamId
