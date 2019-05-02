"""A new approach to interfaces in Python
"""
from interfaces.base import interface
from interfaces.compat import object
from interfaces.exceptions import (
    InterfaceNoInstanceAllowedError,
    InterfaceNotImplementedError,
)


__version__ = '0.1.0-dev'

__all__ = [
    'interface',
    'object',
    'InterfaceNoInstanceAllowedError',
    'InterfaceNotImplementedError',
]
