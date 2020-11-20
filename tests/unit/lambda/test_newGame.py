from mafiaUpdateGame import lambda_handler
from unittest.mock import patch
import json
import os
os.environ['QUEUE_URL'] = 'test_url'


def test_ValidRequest_Returns200():
    teamId = 'test'
    with patch('mafiaUpdateGame.GameStateRepo') as mockRepoConstructor:
        mockRepo = mockRepoConstructor.return_value
        result = lambda_handler(
            {"body": f"team_id={teamId}&user_id=test&channel_id=channel&text=new", "isBase64Encoded": False}, None)
        mockRepo.CreateNewGame.assert_called_once_with(
            teamId, {'channel_id': 'channel'})
    resultBody = json.loads(result['body'])

    assert result['statusCode'] == 200
    assert resultBody['game_id'] == teamId
