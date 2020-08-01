import pytest
from models.player import Player

def test_defaultState():
    systemUnderTest = Player()
    assert systemUnderTest.role == 'NONE'
    assert systemUnderTest.state == 'ALIVE'