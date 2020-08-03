
from models.player import Player, Roles, States as PlayerStates
def createVillager():
    player = Player()
    player.state = PlayerStates.ALIVE
    player.role = Roles.VILLAGER
    return player

def createMafia():
    player = Player()
    player.state = PlayerStates.ALIVE
    player.role = Roles.MAFIA
    return player