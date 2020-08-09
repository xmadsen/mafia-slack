import json
from data_access.dataRepos import GameStateRepo
from stateManagers.gameStateManager import GameStateManager

def lambda_handler(event, context):
    #try:
    game_id, action, player_id = extractParameters(event)
    gameRepo = GameStateRepo()

    gameState = gameRepo.GetGameState(game_id)
    if gameState == None:
        return None
    manager = GameStateManager(gameState)
    manager.transition(action,player_id)

    gameRepo.UpdateGame(gameState)
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': json.dumps({
            'message' : json.dumps('Game state updated'),
            'game': gameRepo._serializeGame(gameState)
            }),
        'isBase64Encoded' : False
    }
    # except Exception as e:
    #     print(e)
    #     response = {
    #         'statusCode': 500,
    #         'headers' : {},
    #         'body': json.dumps('Error updating game!'),
    #         'isBase64Encoded' : False
    #     }
    return response

def extractParameters(event):
    if 'game_id' in event:
        game_id = event['game_id']
    elif 'pathParameters' in event:
        if 'game_id' in event['pathParameters']:
            game_id = event['pathParameters']['game_id']
    else:
        raise ValueError('Missing game_id parameter')

    if 'action' in event:
        action = event['action']
    elif 'pathParameters' in event:
        if 'action' in event['pathParameters']:
            action = event['pathParameters']['action']
    else:
        raise ValueError('Missing action parameter')

    player_id = None
    if 'player_id' in event:
        player_id = event['player_id']
    elif 'pathParameters' in event:
        if 'player_id' in event['pathParameters']:
            player_id = event['pathParameters']['player_id']

    return game_id, action, player_id

if __name__ == "__main__":
    p_id = 'def'
    g_id = 1
    print(add_player(p_id, g_id))