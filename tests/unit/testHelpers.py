
from models.player import Player, Roles, States as PlayerStates


def createVillager(id=None):
    player = Player(id)
    player.state = PlayerStates.ALIVE
    player.role = Roles.VILLAGER
    return player


def createMafia(id=None):
    player = Player(id)
    player.state = PlayerStates.ALIVE
    player.role = Roles.MAFIA
    return player
