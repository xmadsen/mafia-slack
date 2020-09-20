import json, os
from slack import WebClient
from slack.errors import SlackApiError
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import Actions
from models.player import Roles
from models.gameState import States as GameStates
from util.env import getEnvVar
from util.game_message_builder import get_state_change_message

API_TOKEN = getEnvVar('SLACK_API_TOKEN')

def processRecords(recoredList):
    client = WebClient(token=API_TOKEN)
    repo = GameStateRepo()
    for r in recoredList:
        try:
            body = json.loads(r['body'])
            state = repo._deserializeGame(body['state'])
            action = body['action']
            sourcePlayer = body['source']
            targetPlayer = body['target']
            mainChannel = state.meta['channel_id']
            message = get_state_change_message(state,True,action,sourcePlayer,targetPlayer)
            client.chat_postMessage(channel=mainChannel,text=message)
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
                client.chat_postMessage(channel=channelId, text='You are members of the local mafia. Rabble-rousers in the village have decided to make a stand against you. It is time you taught them a lesson...')
                #store the mafia channel
                state.meta['mafia_channel'] = channelId
                repo.UpdateGame(state)
            elif state.state == GameStates.GAME_OVER:
                #clean up the mafia channel and archive it
                mafia_channel = state.meta['mafia_channel']
                for player_id in [p.id for p in state.players if p.role == Roles.MAFIA]:
                    print(f'kicking {player_id}')
                    client.conversations_kick(channel=mafia_channel, user=player_id)
                    
                print(f'archiving channel {mafia_channel}')
                client.conversations_archive(channel=mafia_channel)
        except SlackApiError as e:
            print(e)

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    
    processRecords(event['Records'])
    
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': {}
    }
    return response