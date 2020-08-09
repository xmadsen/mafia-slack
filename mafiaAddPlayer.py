import json
from dataRepos import PlayerRepo, GameStateRepo

def add_player(player_id, game_id):
    gameRepo = GameStateRepo()
    playerRepo = PlayerRepo()

    gameState = gameRepo.GetGameState(game_id)
    if gameState == None:
        return None
    player_match = [p for p in gameState['players'] if p['_id'] == player_id]

    if len(player_match) == 0:
        player = playerRepo.GetPlayer(player_id)
        if player == None:
            player = playerRepo.CreatePlayer(player_id)
        gameState['players'].append(player)
        gameRepo.UpdateGame(gameState)
    else:
        player = player_match[0]
    return player

def lambda_handler(event, context):
    try:
        print(event)
        player = add_player(event['player_id'], event['game_id'])
        response = {
            'statusCode': 200,
            'body': json.dumps('Player added to game'),
            'player_id': player['_id'],
            'game_id': event['game_id']
        }
    except Exception as e:
        print(e)
        response = {
            'statusCode': 500,
            'body': json.dumps('Error adding player!')
        }
    return response

if __name__ == "__main__":
    p_id = 'def'
    g_id = 1
    print(add_player(p_id, g_id))