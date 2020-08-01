import pytest
from models.gameState import State, Constants

def test_defaultGameState():
    systemUnderTest = State()
    assert systemUnderTest.state == Constants.MARSHALLING