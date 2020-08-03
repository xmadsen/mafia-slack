
from models.player import Player, Roles, States as PlayerStates
def createVillager(id = None):
    player = Player()
    player.state = PlayerStates.ALIVE
    player.role = Roles.VILLAGER
    player.id = id
    return player

def createMafia(id=None):
    player = Player()
    player.state = PlayerStates.ALIVE
    player.role = Roles.MAFIA
    player.id = id
    return player