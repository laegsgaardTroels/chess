from chess._version import __version__
from chess._environment import Environment


env = Environment()


__version__ = __version__
__all__ = ["__version__", "env"]
