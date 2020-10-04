import json, os
import boto3
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import GameStateManager, Actions
from models.player import Roles
from util.slack_payload_parser import parse_payload, extract_user_id
from util.game_message_builder import get_state_change_message
from util.env import getEnvVar

QUEUE_URL = getEnvVar('QUEUE_URL')

def updateSlack(state, action, executor, target):
    client = boto3.client('sqs')
    client.send_message(QueueUrl = QUEUE_URL, MessageBody=json.dumps({'state':state, 'action':action, 'source':executor, 'target':target}))

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    
    game_id, action, player_id, target_id = extractParameters(event)
    gameRepo = GameStateRepo()

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
    player_id = slack_event['user_id']
    args = None
    action = None
    
    if 'action' in event:
        action = event['action']
    elif 'pathParameters' in event:
        if 'action' in event['pathParameters']:
            action = event['pathParameters']['action']
    

    if 'text' in slack_event:
        args = extract_user_id(slack_event['text'])
        if action == None:
            split_text = slack_event['text'].split()
            action = split_text[0].upper()

    return game_id, action, player_id, args

if __name__ == "__main__":
    p_id = 'def'
    g_id = 1
    print(add_player(p_id, g_id))