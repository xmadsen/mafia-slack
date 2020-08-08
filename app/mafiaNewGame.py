import json
from data_access.dataRepos import GameStateRepo

def new_game(gameId):
    repo = GameStateRepo()
    
    state = repo.CreateNewGame(gameId)
    
    return state

def generate_new_game_state():
    return {
        '_id' : 'a',
        'state': 'marshalling',
        'players': []
    }

def lambda_handler(event, context):
    try:
        game = new_game(event['game_id'])
        print(game)
        state = None
        if game == None:
            message = json.dumps('Game already exists.')
        else:
            message = json.dumps('Marshalling new game')
            state = game['state']
        response = {
            'statusCode': 200,
            'body': { 
                'message': message,
                'game_id': event['game_id'],
                'game_state': state
            }
        }
    except Exception as e:
        print(e)
        response = {
            'statusCode': 500,
            'body': json.dumps('Error creating game!')
        }
    return response

if __name__ == "__main__":
    print(new_game(None))