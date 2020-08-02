import pytest
from models.gameState import Game, States

def test_defaultGameState():
    systemUnderTest = Game()
    assert systemUnderTest.state == States.MARSHALLING
    assert len(systemUnderTest.players) == 0