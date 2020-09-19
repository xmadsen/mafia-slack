import json
from data_access.dataRepos import GameStateRepo
from util.slack_payload_parser import parse_payload

def new_game(gameId, gameChannel):
    repo = GameStateRepo()
    
    state = repo.CreateNewGame(gameId, {'channel_id': gameChannel})
    
    return state

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    slack_body = event.get("body")
    slack_event = parse_payload(slack_body)
    print(f"Slack data:\n{slack_event}")
    team_id, channel_id = extractIdParameters(slack_event)
    game = new_game(team_id, channel_id)
    if game == None:
        response_type = 'ephemeral'
        message = json.dumps('Game already exists.')
    else:
        response_type = 'in_channel'
        message = json.dumps('A new game of mafia is about to start. type /joinmafia to get in on the action.')
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': json.dumps({ 
            'response_type' : response_type,
            'text': message,
            'game_id': team_id
        }),
        'isBase64Encoded' : False
    }
    return response

def extractIdParameters(event):
    return event['team_id'], event['channel_id']

if __name__ == "__main__":
    print(new_game(None))