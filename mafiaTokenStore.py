import json, os, boto3
from slack import WebClient
from slack.errors import SlackApiError
from util.env import getEnvVar
from util.slack_payload_parser import parse_payload

APP_CLIENT_ID = getEnvVar('APP_CLIENT_ID')
APP_CLIENT_SECRET = getEnvVar('APP_CLIENT_SECRET')
TOKEN_SOURCE = getEnvVar('TOKEN_SOURCE')
def extractParameters(event):

    query_params = event.get("queryStringParameters")
    return query_params.get('code')

def getTokenAndTeam(code):
    client = WebClient()
    response = client.oauth_v2_access(
            client_id=APP_CLIENT_ID,
            client_secret=APP_CLIENT_SECRET,
            code=code
        )
    print(response)
    return response['access_token'], response['team']['id']

def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    dynamoClient = boto3.resource('dynamodb')
    table = dynamoClient.Table(TOKEN_SOURCE)

    code = extractParameters(event)
    token, team_id = getTokenAndTeam(code)
    table.put_item(
        Item = {
            '_id':team_id,
            'token':token
        }
    )
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': 'Installation is Complete!'
    }
    return response