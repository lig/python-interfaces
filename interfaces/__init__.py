"""A new approach to interfaces in Python
"""
from .base import interface
from .compat import InterfaceImplementationBase
from .exceptions import InterfaceNotImplementedError


__version__ = '0.1.0-dev'

__all__ = ['interface', 'InterfaceImplementationBase', 'InterfaceNotImplementedError']
