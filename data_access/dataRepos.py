import boto3
from models.gameState import Game
from models.player import Player

class GameStateRepo(object):
    def __init__(self, dynamo_endpoint = None):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('gameState')

    def GetGameState(self, gameId):
        state =self.table.get_item(Key={'_id': gameId})
        if 'Item' in state:
            return self._deserializeGame(state['Item'])
        return None

    def CreateNewGame(self, gameId, meta=None):
        if 'Item' in self.table.get_item(Key = {'_id' : gameId}):
            return None
        newGameState = Game(gameId)
        newGameState.meta = meta
        self.table.put_item(
            Item = self._serializeGame(newGameState)
        )
        return newGameState

    def UpdateGame(self, gameState):
        return self.table.put_item(Item = self._serializeGame(gameState))

    def _serializeGame(self, game):
        return {
            '_id' : game.id,
            'state' : game.state,
            'players' : [self._serializePlayer(p) for p in game.players],
            'meta':game.meta
        }
        
    def _serializePlayer(self, player):
        return {
            '_id' : player.id,
            'state' : player.state,
            'role' : player.role,
            'vote' :player.vote
        }

    def _deserializeGame(self,game):
        g = Game()
        g.id = game['_id']
        g.state = game['state']
        g.players = [self._deserializePlayer(p) for p in game['players']]
        if 'meta' in game:
            g.meta = game['meta']
        return g

    def _deserializePlayer(self,player):
        p = Player()
        p.id = player['_id']
        p.state = player['state']
        p.role = player['role']
        p.vote = player['vote']
        return p
    