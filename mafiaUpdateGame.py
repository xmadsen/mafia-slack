import json
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import GameStateManager
from util.slack_payload_parser import parse_payload
from util.game_message_builder import get_state_change_message

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    
    game_id, action, player_id = extractParameters(event)
    gameRepo = GameStateRepo()

    gameState = gameRepo.GetGameState(game_id)
    if gameState == None:
        return None
    manager = GameStateManager(gameState)
    success = manager.transition(action,player_id)
    response_text = get_state_change_message(gameState, success, action, player_id)
    gameRepo.UpdateGame(gameState)
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': json.dumps({
            'response_type' : 'in_channel',
            'text' : response_text,
            'game_id' : game_id
            }),
        'isBase64Encoded' : False
    }
    return response

def extractParameters(event):

    slack_body = event.get("body")
    slack_event = parse_payload(slack_body)
    print(f"Slack data:\n{slack_event}")
    
    game_id = slack_event['team_id']

    if 'action' in event:
        action = event['action']
    elif 'pathParameters' in event:
        if 'action' in event['pathParameters']:
            action = event['pathParameters']['action']
    else:
        raise ValueError('Missing action parameter')

    player_id = slack_event['user_id']

    return game_id, action, player_id

if __name__ == "__main__":
    p_id = 'def'
    g_id = 1
    print(add_player(p_id, g_id))