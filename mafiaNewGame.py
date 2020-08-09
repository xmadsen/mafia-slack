import json
from data_access.dataRepos import GameStateRepo


def new_game(gameId):
    repo = GameStateRepo()
    
    state = repo.CreateNewGame(gameId)
    
    return state

def lambda_handler(event, context):
    print(event)
    print(context)
    #try:
    id = extractIdParameter(event)
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
    # except Exception as e:
    #     print(e)
    #     response = {
    #         'statusCode': 500,
    #         'body': json.dumps('Error creating game!')
    #     }
    return response

def extractIdParameter(event):
    if 'game_id' in event:
        return event['game_id']
    elif 'pathParameters' in event:
        if 'game_id' in event['pathParameters']:
            return event['pathParameters']['game_id']
    else:
        raise ValueError('Missing game_id parameter')

if __name__ == "__main__":
    print(new_game(None))