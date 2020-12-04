import pytest
from models.player import Player, Roles, States


def test_defaultState():
    systemUnderTest = Player()
    assert systemUnderTest.role == Roles.NONE
    assert systemUnderTest.state == States.ALIVE
    assert systemUnderTest.id is None
