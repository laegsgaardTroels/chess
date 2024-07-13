import pytest
from chess._environment import Environment

ENV = Environment()


@pytest.fixture
def env():
    return ENV
