import json, os
import boto3
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import GameStateManager, Actions
from models.player import Roles
from util.slack_payload_parser import parse_payload, extract_user_id
from util.game_message_builder import get_state_change_message
from util.env import getEnvVar

QUEUE_URL = getEnvVar('QUEUE_URL')

HELP = 'help'
NEW_GAME = 'new'
action_table = {
    'START':Actions.START_GAME,
    'ACCUSE':Actions.ACCUSE,
    'KILL':Actions.MURDER,
    'VOTE-GUILTY':Actions.GUILTY,
    'VOTE-INNOCENT':Actions.NOT_GUILTY,
    'JOIN':Actions.ADD_PLAYER,
    'LEAVE':Actions.REMOVE_PLAYER,
    'NEW':NEW_GAME
}
def updateSlack(state, action, executor, target):
    client = boto3.client('sqs')
    client.send_message(QueueUrl = QUEUE_URL, MessageBody=json.dumps({'state':state, 'action':action, 'source':executor, 'target':target}))

def convert_to_action(arg):
    if arg in action_table:
        return action_table[arg]
    else:
        return HELP

def get_help_message():
    return '\n'.join([
        'Welcome to mafia slack bot! Valid commands are:',
        '/mafia new - create a new game',
        '/mafia join - join a game that has not yet started',
        '/mafia leave - leave a game that has not yet started',
        '/mafia start - starts the game',
        '/mafia kill [@who] - kill the target player (only valid during the night phase by the mafia)',
        '/mafia accuse [@who] - accuse the target player of being in the mafia',
        '/mafia vote-guilty - vote the accused and on trial player guilty of being in the mafia',
        '/mafia vote-innocent - vote the accused and on trial player innocent of being in the mafia',
    ])

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    gameRepo = GameStateRepo()

    game_id, channel_id, action, player_id, target_id = extractParameters(event)
    if action == HELP:
        response = {
            'statusCode': 200,
            'headers' : {},
            'body': json.dumps({
                'response_type' : 'ephemeral',
                'text' : get_help_message()
                }),
            'isBase64Encoded' : False
        }
    elif action == NEW_GAME:
        state = gameRepo.CreateNewGame(game_id, {'channel_id': channel_id})
        if state == None:
            response_type = 'ephemeral'
            message = json.dumps('Game already exists.')
        else:
            response_type = 'in_channel'
            message = json.dumps('A new game of mafia is about to start. type "/mafia join" to get in on the action.')
        response = {
            'statusCode': 200,
            'headers' : {},
            'body': json.dumps({ 
                'response_type' : response_type,
                'text': message,
                'game_id': game_id
            }),
            'isBase64Encoded' : False
        }
    else:
        gameState = gameRepo.GetGameState(game_id)
        if gameState == None:
            return None
        manager = GameStateManager(gameState)
        success = manager.transition(action,executor=player_id, data=target_id)
        response_type = 'ephemeral'
        if success:
            updateSlack(gameRepo._serializeGame(gameState), action, player_id, target_id)
            response_text='Got it!'
        else:
            response_text = get_state_change_message(gameState, False, action, player_id, target_id)
        print(f'Response message: {response_text}')
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
    channel_id = slack_event['channel_id']
    player_id = slack_event['user_id']
    args = None
    action = None

    if 'action' in event:
        action = event['action']
    elif 'pathParameters' in event and event['pathParameters']:
        if 'action' in event['pathParameters']:
            action = event['pathParameters']['action']

    if 'text' in slack_event:
        args = extract_user_id(slack_event['text'])
        if action == None:
            split_text = slack_event['text'].split('+')
            action = convert_to_action(split_text[0].upper())

    return game_id, channel_id, action, player_id, args