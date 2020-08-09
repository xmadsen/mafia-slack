import json
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import GameStateManager

def lambda_handler(event, context):
    try:
        game_id = event['game_id']
        player_id = event['player_id']
        action = event['action']

        gameRepo = GameStateRepo()

        gameState = gameRepo.GetGameState(game_id)
        if gameState == None:
            return None
        manager = GameStateManager(gameState)
        manager.transition(action,player_id)

        gameRepo.UpdateGame(gameState)
        response = {
            'statusCode': 200,
            'body': json.dumps('Game state updated'),
            'game': gameRepo._serializeGame(gameState)
        }
    except Exception as e:
        print(e)
        response = {
            'statusCode': 500,
            'body': json.dumps('Error updating game!')
        }
    return response

if __name__ == "__main__":
    p_id = 'def'
    g_id = 1
    print(add_player(p_id, g_id))