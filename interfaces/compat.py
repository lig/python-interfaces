import collections.abc
import typing

import interfaces.base
import interfaces.util


__all__ = ['Object']


class Object:
    def __init_subclass__(
        cls,
        implements: typing.Optional[
            typing.Union[
                typing.Iterable[typing.Type[interfaces.base.Interface]],
                typing.Type[interfaces.base.Interface],
            ]
        ] = None,
    ) -> None:
        if implements is None:
            implements = ()

        if not isinstance(implements, collections.abc.Iterable):
            implements = (implements,)

        for iface in implements:
            if not isinstance(iface, interfaces.base._InterfaceMeta):
                raise TypeError(
                    "Arguments to `implements` must be subclasses of `interface`,"
                    " not `%r`",
                    iface,
                )

        for iface in implements:
            interfaces.util._isimplementation(cls, iface, raise_errors=True)

        super().__init_subclass__()
