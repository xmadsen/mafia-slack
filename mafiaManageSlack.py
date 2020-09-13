import json, os
from slack import WebClient
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import Actions
from models.player import Roles
from util.env import getEnvVar

API_TOKEN = getEnvVar('SLACK_API_TOKEN')

def processRecords(recoredList):
    client = WebClient(token=API_TOKEN)
    repo = GameStateRepo()
    for r in recoredList:
        body = json.loads(r['body'])
        state = repo._deserializeGame(body['state'])
        action = body['action']
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
                response = client.conversations_create(name=mafiaChannelName, is_private=True)
                print(response)
                channelId = response['channel']['id']
            print(f'Inviting {mafiaMembers} to mafia channel')
            client.conversations_invite(channel=channelId, users=mafiaMembers)

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    
    processRecords(event['Records'])
    
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': {}
    }
    return response