import json
from data_access.dataRepos import GameStateRepo
from util.slack_payload_parser import parse_payload

def new_game(gameId):
    repo = GameStateRepo()
    
    state = repo.CreateNewGame(gameId)
    
    return state

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    slack_body = event.get("body")
    slack_event = parse_payload(slack_body)
    print(f"Slack data:\n{slack_event}")
    id = extractIdParameter(slack_event)
    game = new_game(id)
    state = None
    if game == None:
        message = json.dumps('Game already exists.')
    else:
        message = json.dumps('Marshalling new game')
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': json.dumps({ 
            'message': message,
            'game_id': id,
            'game_state': state
        }),
        'isBase64Encoded' : False
    }
    return response

def extractIdParameter(event):
    if 'team_id' in event:
        return event['team_id']
    else:
        raise ValueError('Missing team_id parameter')

if __name__ == "__main__":
    print(new_game(None))