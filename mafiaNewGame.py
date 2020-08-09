import json
from data_access.dataRepos import GameStateRepo

def new_game(gameId):
    repo = GameStateRepo()
    
    state = repo.CreateNewGame(gameId)
    
    return state

def lambda_handler(event, context):
    try:
        id = event['game_id']
        game = new_game(id)
        state = None
        if game == None:
            message = json.dumps('Game already exists.')
        else:
            message = json.dumps('Marshalling new game')
        response = {
            'statusCode': 200,
            'body': { 
                'message': message,
                'game_id': id,
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