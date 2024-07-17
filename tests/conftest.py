import pytest
from chess import env as _env


@pytest.fixture(scope="session")
def env():
    return _env
