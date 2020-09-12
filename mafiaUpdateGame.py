import json, os
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import GameStateManager, Actions
from models.player import Roles
from util.slack_payload_parser import parse_payload
from util.game_message_builder import get_state_change_message
from slack import WebClient

def updateSlack(state, action):
    client = WebClient(token=os.environ["SLACK_API_TOKEN"])
    if action == Actions.START_GAME:
        #create a private channel for the mafia
        mafiaMembers = ','.join([p.id for p in state.players if p.role == Roles.MAFIA])
        mafiaChannelName = 'mafia-secrets'
        response = client.conversations_list(types='private_channel')
        mafiaChannels = [c for c in response['channels'] if c['name'] == mafiaChannelName]
        if len(mafiaChannels) > 0:
            print('Unarchiving mafia channel')
            channelId = mafiaChannels[0]['id']
            response = client.conversations_unarchive(channel=channelId)
        else:
            print('Creating mafia channel')
            response = client.conversations_create(name=mafiaChannel, is_private=True)
            channelId = response['channel']['id']
        print(f'Inviting {mafiaMembers} to mafia channel')
        client.conversations_invite(channel=channelId, users=mafiaMembers)
        


def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    
    game_id, action, player_id = extractParameters(event)
    gameRepo = GameStateRepo()

    gameState = gameRepo.GetGameState(game_id)
    if gameState == None:
        return None
    manager = GameStateManager(gameState)
    success = manager.transition(action,player_id)
    response_type = 'ephemeral'
    if success:
        response_type = 'in_channel'
        updateSlack(gameState, action)
    response_text = get_state_change_message(gameState, success, action, player_id)
    gameRepo.UpdateGame(gameState)
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': json.dumps({
            'response_type' : response_type,
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