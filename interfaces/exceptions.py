from __future__ import annotations

import typing


if typing.TYPE_CHECKING:
    import interfaces.base


__all__ = [
    'InterfaceNoInstanceAllowedError',
    'InterfaceNotImplementedError',
    'InterfaceOverloadingError',
]


class InterfaceError(Exception):
    pass


class InterfaceNoInstanceAllowedError(InterfaceError):
    def __init__(self, *, iface: typing.Type[interfaces.base.Interface]) -> None:
        self._iface = iface

    def __str__(self) -> str:
        return (
            f"Attempted to create an instance of interface `{self._iface!r}` which is"
            " not allowed"
        )


class InterfaceNotImplementedError(InterfaceError):
    def __init__(
        self,
        *,
        klass: typing.Type,
        method_name: str,
        iface: typing.Type[interfaces.base.Interface],
    ) -> None:
        self._klass = klass
        self._method_name = method_name
        self._iface = iface

    def __str__(self) -> str:
        return (
            f"`{self._klass!r}` must fully implement `{self._method_name!s}` method of"
            f" `{self._iface}`"
        )


class InterfaceOverloadingError(InterfaceError):
    def __init__(
        self,
        *,
        method_names: typing.Container[str],
        ancestor_iface: typing.Type[interfaces.base.Interface],
        descendant_iface: typing.Type[interfaces.base.Interface],
    ) -> None:
        self._method_names = method_names
        self._ancestor_iface = ancestor_iface
        self._descendant_iface = descendant_iface

    def __str__(self) -> str:
        return (
            f"Attempted to overload method(s) `{self._method_names!s}` of"
            f" `{self._ancestor_iface!r}` in `{self._descendant_iface!r}`"
        )
