import boto3
from boto3.dynamodb.conditions import Attr

class GameStateRepo(object):
    def __init__(self, dynamo_endpoint = None):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('gameState')

    def GetGameState(self, gameId):
        state =self.table.get_item(Key={'_id': gameId})
        if 'Item' in state:
            return state['Item']
        return None

    def CreateNewGame(self, gameId):
        if 'Item' in self.table.get_item(Key = {'_id' : gameId}):
            return None
        newGameState = GameStateRepo.GetNewGameState(gameId)
        self.table.put_item(
            Item = newGameState
        )
        return newGameState

    def UpdateGame(self, gameState):
        return self.table.put_item(Item = gameState)

    @staticmethod
    def GetNewGameState( gameId):
        return {
            '_id' : gameId,
            'state': 'marshalling',
            'players': []
        }


class PlayerRepo(object):
    def __init__(self, dynamo_endpoint = None):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('players')

    def GetPlayer(self, playerId):
        player = self.table.get_item(Key={'_id': playerId})
        if 'Item' in player:
            return player['Item']
        return None
        
    def CreatePlayer(self, playerId):
        if 'Item' in self.table.get_item(Key = {'_id' : playerId}):
            return None
        newPlayer = PlayerRepo.GetNewPlayer(playerId)
        self.table.put_item(
            Item = newPlayer
        )
        return newPlayer

    def UpdatePlayer(self, gameState):
        return self.table.put_item(Item = gameState)

    @staticmethod
    def GetNewPlayer(playerId):
        return {'_id': playerId}