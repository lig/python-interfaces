"""A new approach to interfaces in Python
"""
import interfaces.base
import interfaces.compat
import interfaces.exceptions
import interfaces.spec
import interfaces.util


__version__ = '0.1.0-dev1'


__all__ = ['Interface', 'Object', 'isimplementation']


interface = Interface = interfaces.base.Interface
object = Object = interfaces.compat.Object

InterfaceNoInstanceAllowedError = interfaces.exceptions.InterfaceNoInstanceAllowedError
InterfaceNotImplementedError = interfaces.exceptions.InterfaceNotImplementedError
InterfaceOverloadingError = interfaces.exceptions.InterfaceOverloadingError

interface_spec = interfaces.spec.interface_spec

isimplementation = interfaces.util.isimplementation
