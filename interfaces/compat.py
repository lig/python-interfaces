import collections.abc
import typing

import interfaces.base


__all__ = ['Object']


class Object:
    def __init_subclass__(
        cls,
        implements: typing.Union[
            typing.Iterable[interfaces.base.Interface], interfaces.base.Interface
        ],
        **kwargs,
    ):
        if not isinstance(implements, collections.abc.Iterable):
            implements = (implements,)

        for iface in implements:
            if not issubclass(iface, interfaces.base.Interface):
                raise TypeError(
                    "Arguments to `implements` must be subclasses of `interface`,"
                    " not `%r`",
                    iface,
                )

        for iface in implements:
            interfaces.base._isimplementation(cls, iface, raise_errors=True)

        super().__init_subclass__(**kwargs)
