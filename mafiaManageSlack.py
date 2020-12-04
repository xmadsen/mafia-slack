import json
import os
import boto3
from slack import WebClient
from slack.errors import SlackApiError
from data_access.dataRepos import MafiaSerializer, GameStateRepo
from stateManagers.gameStateManager import Actions
from models.player import Roles
from models.gameState import States as GameStates
from util.env import getEnvVar
from util.constants import Header
from util.game_message_builder import (
    get_state_change_message, get_blocks_for_message)
from util.messagetext import MessageText as txt


def getToken(id):
    dynamodb = boto3.resource('dynamodb')
    tokenStore = dynamodb.Table(getEnvVar('TOKEN_SOURCE'))
    result = tokenStore.get_item(Key={'_id': id})
    print(f'Getting token for {id}')
    if 'Item' in result:
        return result['Item']['token']


def processRecords(record_list):
    serializer = MafiaSerializer()
    for r in record_list:
        try:
            body = json.loads(r['body'])
            state = serializer.DeserializeGame(body['state'])
            token = getToken(state.id)
            client = WebClient(token=token)
            action = body['action']
            sourcePlayer = body['source']
            targetPlayer = body['target']
            mainChannel = state.meta['channel_id']
            message, header = get_state_change_message(
                state, True, action, sourcePlayer, targetPlayer)
            blocks = get_blocks_for_message(message, header)
            client.chat_postMessage(channel=mainChannel, blocks=blocks)
            if action == Actions.START_GAME:
                # create a private channel for the mafia
                mafiaMembers = ','.join(
                    [p.id for p in state.players if p.role == Roles.MAFIA])
                mafiaChannelName = 'mafia-secrets'
                response = client.conversations_list(types='private_channel')
                mafiaChannels = [c for c in response['channels']
                                 if c['name'] == mafiaChannelName]
                if len(mafiaChannels) > 0:
                    print('Unarchiving mafia channel')
                    channelId = mafiaChannels[0]['id']
                    response = client.conversations_unarchive(
                        channel=channelId)
                else:
                    print('Creating mafia channel')
                    response = client.conversations_create(
                        name=mafiaChannelName, is_private=True)
                    print(response)
                    channelId = response['channel']['id']
                print(f'Inviting {mafiaMembers} to mafia channel')
                client.conversations_invite(
                    channel=channelId, users=mafiaMembers)
                message = txt.MAFIA_TEAM_INTRO
                header = Header.MAFIA_ONLY
                blocks = get_blocks_for_message(message, header)
                client.chat_postMessage(channel=channelId, blocks=blocks)
                # store the mafia channel
                state.meta['mafia_channel'] = channelId
                repo = GameStateRepo()
                repo.UpdateGame(state)
            elif state.state == GameStates.GAME_OVER:
                # clean up the mafia channel and archive it
                mafia_channel = state.meta['mafia_channel']
                for player_id in [
                        p.id for p in state.players if p.role == Roles.MAFIA]:
                    print(f'kicking {player_id} from mafia channel')
                    client.conversations_kick(
                        channel=mafia_channel, user=player_id)

                print(f'archiving channel {mafia_channel}')
                client.conversations_archive(channel=mafia_channel)
        except SlackApiError as e:
            print(e)


def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")

    processRecords(event['Records'])

    response = {
        'statusCode': 200,
        'headers': {},
        'body': {}
    }
    return response
