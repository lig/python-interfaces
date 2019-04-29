import collections.abc
import typing

from .base import _isimplementation, interface


__all__ = ['InterfaceImplementationBase']


class InterfaceImplementationBase:
    def __init_subclass__(
        cls, implements: typing.Union[typing.Iterable[interface], interface], **kwargs
    ):
        if not isinstance(implements, collections.abc.Iterable):
            implements = (implements,)

        for iface in implements:
            if not issubclass(iface, interface):
                raise TypeError(
                    "Arguments to `implements` must be subclasses of `interface`,"
                    " not `%r`",
                    iface,
                )

        for iface in implements:
            _isimplementation(cls, iface, raise_errors=True)

        super().__init_subclass__(**kwargs)
